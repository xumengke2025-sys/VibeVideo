"""Bounded render batches, resumable PNGs, filtered logs, final assembly."""
from pathlib import Path
import subprocess,json,time,collections,sys,hashlib
ROOT=Path(__file__).resolve().parent
BLENDER=ROOT.parents[1]/'tools/blender-portable/blender-4.5.3-windows-x64/blender.exe'
OUT=ROOT/'render';FRAMES=OUT/'frames-v6';LOGS=OUT/'batch-logs-v6';LOGS.mkdir(parents=True,exist_ok=True)
start=time.time();failures=0
state={'stage':'rendering','frames':1344,'width':1080,'height':1920,'fps':24,'engine':'Cycles OptiX, 256px tiles','samples':24,'compositor':'GPU','cache':'persistent; 32-frame processes','model_sha256':hashlib.sha256((ROOT/'model/babylon-city-v6.blend').read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256((ROOT/'render_city.py').read_bytes()).hexdigest()}
def save():
 state['completed_frames']=sum((FRAMES/f'{i:05d}.png').exists() for i in range(1344));state['elapsed_seconds']=time.time()-start;(OUT/'pipeline-status.json').write_text(json.dumps(state,indent=2),encoding='utf8')
for a in range(0,1344,32):
 b=min(1344,a+32)
 while any(not (FRAMES/f'{i:05d}.png').exists() for i in range(a,b)):
  save();tail=collections.deque(maxlen=40)
  with (LOGS/f'{a:05d}-{b-1:05d}.log').open('a',encoding='utf8') as log:
   p=subprocess.Popen([str(BLENDER),'--background','--python',str(ROOT/'render_city.py'),'--','range',str(a),str(b)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf8',errors='replace')
   state['process_id']=p.pid;save()
   for line in p.stdout:
    tail.append(line)
    if any(t in line for t in ['FRAME_READY','Error','Traceback','Exception','Calloc','Writing:','Blender quit']):
     log.write(line);log.flush()
    if 'FRAME_READY' in line:save()
   p.wait()
   if p.returncode:
    log.write('\nFAILURE TAIL\n'+''.join(tail));failures+=1;state['last_failure']=p.returncode;save()
    if failures>=2:state['stage']='render_failed';save();raise SystemExit('Repeated renderer failure; inspect batch log')
   else:failures=0
  save()
 print(json.dumps({'batch_complete':[a,b-1],'total_frames':state['completed_frames'],'elapsed_seconds':round(time.time()-start)}),flush=True)
state['stage']='encoding';save()
subprocess.run([sys.executable,str(ROOT/'assemble_city.py')],check=True)
state['stage']='candidate_ready_for_one_review';save();print('CANDIDATE_READY',flush=True)
