"""Frozen render, bounded processes, flash-frame isolation and lossless rerender."""
from pathlib import Path
import os,sys,json,time,hashlib,subprocess,collections,re,shutil
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent;QA=ROOT/'qa/v13';OUT=ROOT/'render'
BLENDER=ROOT.parents[1]/'tools/blender-portable/blender-4.5.3-windows-x64/blender.exe'
SAMPLE=sorted(set([396,528,636,660,744,864,168,1752]+list(range(516,540))+list(range(732,756))))
mode=sys.argv[1] if len(sys.argv)>1 else 'full';folder=OUT/('sample-v13' if mode=='sample' else 'frames-v13');folder.mkdir(parents=True,exist_ok=True)
logs=OUT/'batch-logs-v13';logs.mkdir(exist_ok=True)
env=os.environ.copy();env.update(CITY_DEVICE='OPTIX',CITY_DENOISER='OPENIMAGEDENOISE',CITY_DENOISE_GPU='1',CITY_COMPOSITOR='GPU',CITY_TILING='0',CITY_FRAME_DIR=folder.name,CITY_SAMPLES='32')
files=['model/babylon-city-v13.blend','render_city_v13.py','traffic-v13.npz','v13-timeline.json','audio/final-mix-v11.wav']
hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files}
manifest={'files':hashes,'samples':32,'width':1080,'height':1920,'fps':24,'duration':76,'frames':1824,'compositor':'GPU separable multi-level Gaussian; physical depth + screen tilt band','denoiser':'OIDN GPU; fallback OPTIX GPU'}
mp=OUT/'frozen-v13-manifest.json'
if mp.exists():assert json.loads(mp.read_text(encoding='utf8'))==manifest,'Frozen inputs changed. Preserve the old sequence.'
else:mp.write_text(json.dumps(manifest,indent=2),encoding='utf8')
def thumb(path):
 with Image.open(path) as im:
  assert im.size==(1080,1920);im.load();return np.asarray(im.resize((180,320)),np.float32)
def corruption(im):
 r,g,b=np.moveaxis(im,-1,0)
 return float(np.mean((g>r+12)&(g>b+10)))>.35
rejected=[]
def isolate(f,why):
 p=folder/f'{f:05d}.png';dest=OUT/'rejected-v13';dest.mkdir(exist_ok=True)
 shutil.move(p,dest/f'{f:05d}-{len(rejected):02d}.png');rejected.append({'frame':f,'reason':why})
 (QA/'rejected-frames.json').write_text(json.dumps(rejected,indent=2),encoding='utf8')
def render(frames,label,fallback=False):
 if not frames:return
 runenv=env.copy()
 if fallback:runenv.update(CITY_COMPOSITOR='GPU',CITY_DENOISER='OPTIX')
 args=['range',str(frames[0]),str(frames[-1]+1)] if frames==list(range(frames[0],frames[-1]+1)) else ['stills']+[str(f) for f in frames]
 tail=collections.deque(maxlen=30)
 with (logs/(label+'.log')).open('a',encoding='utf8') as log:
  p=subprocess.Popen([str(BLENDER),'--background','--python-exit-code','1','--python',str(ROOT/'render_city_v13.py'),'--']+args,env=runenv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf8',errors='replace')
  ready=0
  for line in p.stdout:
   tail.append(line)
   if any(s in line for s in ['FRAME_READY','Error','Traceback','out of memory','Blender quit']):log.write(line);log.flush()
   if line.startswith('FRAME_READY'):
    ready+=1
    if ready%10==0:print('RENDER_PROGRESS',label,line.strip(),flush=True)
  p.wait()
  if p.returncode:log.write(''.join(tail));raise RuntimeError(('Renderer failure',p.returncode,label))
def check_frames(frames):
 bad=[]
 for f in frames:
  p=folder/f'{f:05d}.png'
  if not p.exists():raise RuntimeError(('Missing frame',f))
  if corruption(thumb(p)):isolate(f,'abnormal green cast');bad.append(f)
 if bad:
  render(bad,'isolated-fallback-'+str(bad[0]),True)
  for f in bad:assert not corruption(thumb(folder/f'{f:05d}.png')),('Fallback remains corrupt',f)
start=time.time()
if mode=='sample':
 render([f for f in SAMPLE if not (folder/f'{f:05d}.png').exists()],'production-sample')
 check_frames(SAMPLE)
 (QA/'sample-source.json').write_text(json.dumps({'manifest':manifest,'frames':SAMPLE,'folder':str(folder),'elapsed':time.time()-start},indent=2),encoding='utf8')
 print('SAMPLE_READY',len(SAMPLE),time.time()-start,flush=True);sys.exit(0)
# Revised pedestrian avoidance, east quay and cargo vessel also affect distant
# views. Render every shot from the same frozen v13 world.
reuse_ranges=[]
parent_manifest=json.loads((OUT/'frozen-v12-manifest.json').read_text(encoding='utf8'))
for name,digest in parent_manifest['files'].items():
 assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,('Parent inputs changed',name)
reused=[]
for a,b in reuse_ranges:
 for f in range(a,b):
  src=OUT/'frames-v12'/f'{f:05d}.png';dest=folder/src.name
  assert src.exists(),src
  if not dest.exists():shutil.copy2(src,dest)
  reused.append(f)
(QA/'frame-provenance.json').write_text(json.dumps({'parent_manifest':'render/frozen-v12-manifest.json','reused_ranges_exclusive':reuse_ranges,'reused_count':len(reused),'rerendered_shots':list(range(9)),'reason':'All shots rendered from frozen v13 inputs because revised traffic, east quay and cargo position can also affect distant views.'},indent=2),encoding='utf8')
source=QA/'sample-source.json'
if source.exists():
 d=json.loads(source.read_text(encoding='utf8'))
 if d['manifest']==manifest:
  for f in d['frames']:
   p=Path(d['folder'])/f'{f:05d}.png'
   if p.exists() and not (folder/p.name).exists():shutil.copy2(p,folder/p.name)
status={'stage':'rendering','frame_count':1824,'width':1080,'height':1920,'fps':24,'samples':32,'completed_frames':0,'source_manifest':str(mp)}
def save():
 status['completed_frames']=sum((folder/f'{i:05d}.png').exists() for i in range(1824));status['elapsed_seconds']=time.time()-start
 (OUT/'pipeline-status-v13.json').write_text(json.dumps(status,indent=2),encoding='utf8')
save()
# Bound later restarts to 48 frames after observed shared-host-memory exhaustion
# in a long process. This changes process lifetime, not pixel inputs or quality.
for a in range(0,1824,48):
 b=min(a+48,1824);missing=[f for f in range(a,b) if not (folder/f'{f:05d}.png').exists()]
 for attempt in range(2):
  try:render(missing,f'{a:05d}-{b-1:05d}');break
  except RuntimeError:
   if attempt:raise
   missing=[f for f in range(a,b) if not (folder/f'{f:05d}.png').exists()]
 check_frames(list(range(a,b)));save();print('BATCH_READY',a,b-1,status['completed_frames'],round(time.time()-start),flush=True)
# Whole-film temporal scan catches isolated colour/brightness faults beyond the
# explicit green-buffer signature. Hard cuts and intentional fades are excluded.
status['stage']='temporal_scan';save()
cuts=[round(s[0]*24) for s in json.loads((ROOT/'v13-timeline.json').read_text(encoding='utf8'))['shots'][1:]]
bad=[];d=[];previous=thumb(folder/'00000.png');current=thumb(folder/'00001.png')
for f in range(1,1823):
 following=thumb(folder/f'{f+1:05d}.png');before=float(np.abs(current-previous).mean());after=float(np.abs(following-current).mean());d.append(before)
 if 10<f<1786 and all(abs(f-c)>=3 for c in cuts) and before>18 and after>18 and np.abs(previous-following).mean()<max(before,after)*.7:
  isolate(f,'isolated temporal discontinuity');bad.append(f)
 previous,current=current,following
if bad:render(bad,'temporal-fallback',True)
(QA/'temporal-scan.json').write_text(json.dumps({'frames':1824,'cut_frames':cuts,'peak_non_cut_difference':float(max(d[i] for i in range(len(d)) if all(abs(i+1-c)>2 for c in cuts) and 10<i<1786)),'temporal_repaired_frames':bad,'isolated_rejections':rejected,'method':'180x320 all-frame RGB differences and strong green cast detector; mechanical check, not independent aesthetic review'},indent=2),encoding='utf8')
status['stage']='encoding';save()
subprocess.run([sys.executable,'-X','utf8',str(ROOT/'assemble_city_v13.py')],check=True)
status['stage']='candidate_ready_for_producer_verification';save();print('V13_CANDIDATE_READY',flush=True)
