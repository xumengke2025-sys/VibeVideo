"""Bounded versioned Blender entry, environment local to subprocess."""
from pathlib import Path
import os,sys,subprocess
P=Path(__file__).resolve().parent
env=os.environ.copy();env.update(CITY_DEVICE='OPTIX',CITY_DENOISER='OPENIMAGEDENOISE',CITY_DENOISE_GPU='1',CITY_COMPOSITOR='GPU',CITY_TILING='0',CITY_SAMPLES='32')
args=sys.argv[1:] or ['proof']
if args[0]=='character':env['CITY_FRAME_DIR']='character-v15-r4'
elif args[0]=='preview':env.update(CITY_FRAME_DIR='preview-v15',CITY_SCALE='35',CITY_SAMPLES='12');args=['stills']+args[1:]
elif args[0]=='audit':pass
elif args[0]=='sample':env['CITY_FRAME_DIR']='sample-v15';args=['stills']+args[1:]
else:env['CITY_FRAME_DIR']='proof-v15'
logs=P/'render/batch-logs-v15';logs.mkdir(parents=True,exist_ok=True)
with (logs/('manual-'+args[0]+'.log')).open('a',encoding='utf8') as log:
 proc=subprocess.Popen([str(P.parents[1]/'tools/blender-portable/blender-4.5.3-windows-x64/blender.exe'),'--background','--python-exit-code','1','--python',str(P/'render_city_v15.py'),'--']+args,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf8',errors='replace')
 for line in proc.stdout:
  if any(k in line for k in ['FRAME_READY','Error','Traceback','V15_','out of memory','Blender quit','Saved:']):log.write(line);log.flush();print(line.strip(),flush=True)
 raise SystemExit(proc.wait())
