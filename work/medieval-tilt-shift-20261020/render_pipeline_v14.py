"""Frozen v14 inputs, bounded rendering, technical frame checks and final encode."""
from pathlib import Path
import os,sys,json,time,hashlib,subprocess,collections,shutil
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent;QA=ROOT/'qa/v14';OUT=ROOT/'render'
BLENDER=ROOT.parents[1]/'tools/blender-portable/blender-4.5.3-windows-x64/blender.exe'
SAMPLE=sorted(set([48,288,528,934,1115,1752]+list(range(720,792))+list(range(1320,1494))))
mode=sys.argv[1] if len(sys.argv)>1 else 'full'
folder=OUT/('sample-v14' if mode=='sample' else 'frames-v14');folder.mkdir(parents=True,exist_ok=True)
logs=OUT/'batch-logs-v14';logs.mkdir(exist_ok=True)
env=os.environ.copy();env.update(CITY_DEVICE='OPTIX',CITY_DENOISER='OPENIMAGEDENOISE',CITY_DENOISE_GPU='1',CITY_COMPOSITOR='GPU',CITY_TILING='0',CITY_FRAME_DIR=folder.name,CITY_SAMPLES='32')
files=['model/babylon-city-v14.blend','render_city_v14.py','v14_motion.py','traffic-v14.npz','v14-timeline.json','audio/final-mix-v14.wav']
hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files}
manifest={'files':hashes,'samples':32,'width':1080,'height':1920,'fps':24,'duration':76,'frames':1824,'compositor':'GPU separable multi-level Gaussian; physical depth + tracked screen tilt band','denoiser':'OIDN GPU; fallback OPTIX GPU','render_environment':{k:v for k,v in env.items() if k.startswith('CITY_') and k!='CITY_FRAME_DIR'}}
mp=OUT/'frozen-v14-manifest.json'
if mp.exists():assert json.loads(mp.read_text(encoding='utf8'))==manifest,'Frozen inputs changed. Preserve the old sequence.'
else:mp.write_text(json.dumps(manifest,indent=2),encoding='utf8')
def thumb(path):
    with Image.open(path) as im:
        assert im.size==(1080,1920);im.load();return np.asarray(im.resize((180,320)),np.float32)
def corruption(im):
    r,g,b=np.moveaxis(im,-1,0)
    return float(np.mean((g>r+12)&(g>b+10)))>.35
rejected=[]
def wait_for_device():
    # Other locally running films share this 8GB GPU. Do not stop them or
    # repeatedly fail allocations: start a new batch only while it is free.
    last_report=0
    while True:
        query="@(Get-CimInstance Win32_Process -Filter \"name = 'blender.exe'\" | Where-Object { $_.CommandLine -match '--background' } | Select-Object -ExpandProperty ProcessId) | ConvertTo-Json -Compress"
        result=subprocess.run(['powershell','-NoProfile','-Command',query],capture_output=True,text=True)
        active=result.stdout.strip()
        if result.returncode:raise RuntimeError('Could not check shared Blender device ownership')
        if not active or active=='[]':
            if 'status' in globals():status['stage']='rendering_'+mode;status.pop('other_blender_pids',None);save()
            return
        if time.time()-last_report>55:
            print('WAITING_SHARED_GPU',active,flush=True);last_report=time.time()
            if 'status' in globals():status['stage']='waiting_shared_gpu';status['other_blender_pids']=json.loads(active);save()
        time.sleep(15)
def isolate(f,why):
    p=folder/f'{f:05d}.png';dest=OUT/'rejected-v14';dest.mkdir(exist_ok=True)
    shutil.move(p,dest/f'{f:05d}-{time.time_ns()}.png');rejected.append({'frame':f,'reason':why})
    (QA/'rejected-frames.json').write_text(json.dumps(rejected,indent=2),encoding='utf8')
def render(frames,label,fallback=False):
    if not frames:return
    assert len(frames)<=48
    wait_for_device()
    runenv=env.copy()
    if fallback:runenv.update(CITY_DENOISER='OPTIX')
    args=['range',str(frames[0]),str(frames[-1]+1)] if frames==list(range(frames[0],frames[-1]+1)) else ['stills']+[str(f) for f in frames]
    tail=collections.deque(maxlen=25)
    with (logs/(label+'.log')).open('a',encoding='utf8') as log:
        p=subprocess.Popen([str(BLENDER),'--background','--python-exit-code','1','--python',str(ROOT/'render_city_v14.py'),'--']+args,env=runenv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf8',errors='replace')
        ready=0
        for line in p.stdout:
            tail.append(line)
            if any(s in line for s in ['FRAME_READY','Error','Traceback','out of memory','System is out','Blender quit']):log.write(line);log.flush()
            if line.startswith('FRAME_READY'):
                ready+=1
                if ready%10==0:print('RENDER_PROGRESS',label,line.strip(),flush=True)
        p.wait()
        if p.returncode:log.write(''.join(tail));raise RuntimeError(('Renderer failure',p.returncode,label))
def bounded(frames,label,fallback=False):
    for i in range(0,len(frames),48):render(frames[i:i+48],label+'-'+str(i),fallback)
def check_frames(frames):
    bad=[]
    for f in frames:
        p=folder/f'{f:05d}.png'
        if not p.exists():raise RuntimeError(('Missing frame',f))
        if corruption(thumb(p)):isolate(f,'abnormal green cast');bad.append(f)
    if bad:
        bounded(bad,'isolated-fallback-'+str(bad[0]),True)
        for f in bad:assert not corruption(thumb(folder/f'{f:05d}.png')),('Fallback remains corrupt',f)
start=time.time()
status={'stage':'rendering_'+mode,'frame_count':len(SAMPLE) if mode=='sample' else 1824,'width':1080,'height':1920,'fps':24,'samples':32,'completed_frames':0,'source_manifest':str(mp),'pipeline_pid':os.getpid()}
targets=SAMPLE if mode=='sample' else list(range(1824))
def save():
    status['completed_frames']=sum((folder/f'{i:05d}.png').exists() for i in targets);status['elapsed_seconds']=time.time()-start
    (OUT/'pipeline-status-v14.json').write_text(json.dumps(status,indent=2),encoding='utf8')
if mode!='sample':
    source=QA/'sample-source.json'
    if source.exists():
        d=json.loads(source.read_text(encoding='utf8'))
        if d['manifest']==manifest:
            for f in d['frames']:
                p=Path(d['folder'])/f'{f:05d}.png'
                if p.exists() and not (folder/p.name).exists():shutil.copy2(p,folder/p.name)
    (QA/'frame-provenance.json').write_text(json.dumps({'reused_prior_versions':0,'rerendered_shots':list(range(9)),'sample_reuse_requires_exact_manifest':True,'reason':'All nine shots use frozen v14 world and focus.'},indent=2),encoding='utf8')
save()
for i in range(0,len(targets),48):
    chunk=targets[i:i+48];missing=[f for f in chunk if not (folder/f'{f:05d}.png').exists()]
    for attempt in range(3):
        try:
            render(missing,f'{chunk[0]:05d}-{chunk[-1]:05d}');break
        except RuntimeError:
            if attempt==2:raise
            print('RETRY_AFTER_RENDER_FAILURE',chunk[0],attempt+1,flush=True)
            time.sleep(15)
            missing=[f for f in chunk if not (folder/f'{f:05d}.png').exists()]
    check_frames(chunk);save();print('BATCH_READY',chunk[0],chunk[-1],status['completed_frames'],round(time.time()-start),flush=True)
if mode=='sample':
    (QA/'sample-source.json').write_text(json.dumps({'manifest':manifest,'frames':SAMPLE,'folder':str(folder),'elapsed':time.time()-start},indent=2),encoding='utf8')
    status['stage']='sample_ready';save();print('SAMPLE_READY',len(SAMPLE),time.time()-start,flush=True);sys.exit(0)
status['stage']='temporal_scan';save()
cuts=[round(s[0]*24) for s in json.loads((ROOT/'v14-timeline.json').read_text(encoding='utf8'))['shots'][1:]]
bad=[];d=[];previous=thumb(folder/'00000.png');current=thumb(folder/'00001.png')
for f in range(1,1823):
    following=thumb(folder/f'{f+1:05d}.png');before=float(np.abs(current-previous).mean());after=float(np.abs(following-current).mean());d.append(before)
    if 10<f<1786 and all(abs(f-c)>=3 for c in cuts) and before>18 and after>18 and np.abs(previous-following).mean()<max(before,after)*.7:
        isolate(f,'isolated temporal discontinuity');bad.append(f)
    previous,current=current,following
if bad:bounded(bad,'temporal-fallback',True)
(QA/'temporal-scan.json').write_text(json.dumps({'frames':1824,'cut_frames':cuts,'peak_non_cut_difference':float(max(d[i] for i in range(len(d)) if all(abs(i+1-c)>2 for c in cuts) and 10<i<1786)),'temporal_repaired_frames':bad,'isolated_rejections':rejected,'method':'180x320 all-frame RGB differences and strong green cast detector; mechanical check, not aesthetic review or subtle shimmer approval'},indent=2),encoding='utf8')
status['stage']='encoding';save()
subprocess.run([sys.executable,'-X','utf8',str(ROOT/'assemble_city_v14.py')],check=True)
status['stage']='candidate_ready_for_producer_verification';save();print('V14_CANDIDATE_READY',flush=True)
