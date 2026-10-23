"""Bounded render batches, resumable PNGs, filtered logs, final assembly."""
from pathlib import Path
import subprocess,json,time,collections,sys,hashlib,os,re
from PIL import Image,ImageStat
ROOT=Path(__file__).resolve().parent
BLENDER=ROOT.parents[1]/'tools/blender-portable/blender-4.5.3-windows-x64/blender.exe'
OUT=ROOT/'render';FRAMES=OUT/'frames-v9';LOGS=OUT/'batch-logs-v9';LOGS.mkdir(parents=True,exist_ok=True)
FRAMES.mkdir(parents=True,exist_ok=True)
start=time.time();failures=0
state={'stage':'rendering','frames':1344,'width':1080,'height':1920,'fps':24,'engine':'Cycles '+os.environ.get('CITY_DEVICE','CUDA'),'tiling':False,'denoiser':'OpenImageDenoise GPU','samples':24,'compositor':'GPU','cache':'persistent; 32-frame processes','model_sha256':hashlib.sha256((ROOT/'model/babylon-city-v9.blend').read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256((ROOT/'render_city_v9.py').read_bytes()).hexdigest(),'timeline_sha256':hashlib.sha256((ROOT/'v8-timeline.json').read_bytes()).hexdigest()}
status=OUT/'pipeline-status-v9.json'
if status.exists():
 previous=json.loads(status.read_text(encoding='utf8'))
 for k in ['model_sha256','renderer_sha256','timeline_sha256']:
  if previous.get(k)!=state[k] and any(FRAMES.glob('*.png')):raise SystemExit('Source changed; preserve and separate existing frames before rendering.')
def valid_frame(i):
 path=FRAMES/f'{i:05d}.png'
 if not path.exists():return False
 try:
  with Image.open(path) as im:
   if im.size!=(1080,1920):return False
   im.load();im.thumbnail((64,114));mean=sum(ImageStat.Stat(im.convert('RGB')).mean)/3
   if 6<=i<=1320 and mean<1:return False
  return True
 except Exception:return False
def save():
 state['completed_frames']=sum((FRAMES/f'{i:05d}.png').exists() for i in range(1344));state['elapsed_seconds']=time.time()-start;status.write_text(json.dumps(state,indent=2),encoding='utf8')
for i in range(1344):
 if (FRAMES/f'{i:05d}.png').exists() and not valid_frame(i):raise SystemExit(f'Invalid existing frame {i}; inspect before resume.')
# A resumed job may skip complete early batches before the first renderer launch.
# Initialize the progress count before those batches are reported.
save()
for a in range(0,1344,32):
 b=min(1344,a+32)
 while any(not (FRAMES/f'{i:05d}.png').exists() for i in range(a,b)):
  save();tail=collections.deque(maxlen=40)
  with (LOGS/f'{a:05d}-{b-1:05d}.log').open('a',encoding='utf8') as log:
   p=subprocess.Popen([str(BLENDER),'--background','--python',str(ROOT/'render_city_v9.py'),'--','range',str(a),str(b)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf8',errors='replace')
   state['process_id']=p.pid;save()
   for line in p.stdout:
    tail.append(line)
    if any(t in line for t in ['FRAME_READY','Error','Traceback','Exception','Calloc','Writing:','Blender quit']):
     log.write(line);log.flush()
    if 'FRAME_READY' in line:
     frame=int(re.search(r'FRAME_READY\s+(\d+)',line).group(1))
     if not valid_frame(frame):
      p.terminate();p.wait();state['stage']='invalid_render_output';state['invalid_frame']=frame;save();raise SystemExit(f'Frame {frame} failed PNG/dimension/black-output check.')
     save()
   p.wait()
   if p.returncode:
    log.write('\nFAILURE TAIL\n'+''.join(tail));failures+=1;state['last_failure']=p.returncode;save()
    if failures>=2:state['stage']='render_failed';save();raise SystemExit('Repeated renderer failure; inspect batch log')
   else:failures=0
  save()
 print(json.dumps({'batch_complete':[a,b-1],'total_frames':state['completed_frames'],'elapsed_seconds':round(time.time()-start)}),flush=True)
state['stage']='encoding';save()
assert all(valid_frame(i) for i in range(1344))
subprocess.run([sys.executable,str(ROOT/'assemble_city_v9.py')],check=True)
state['stage']='candidate_ready_for_one_review';save();print('CANDIDATE_READY',flush=True)
