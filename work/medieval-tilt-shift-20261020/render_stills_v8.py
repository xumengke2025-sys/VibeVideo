from pathlib import Path
import subprocess,sys,shutil
ROOT=Path(__file__).resolve().parent
BL=ROOT.parents[1]/'tools/blender-portable/blender-4.5.3-windows-x64/blender.exe'
bad=ROOT/'render/proof-v8/00168.png'
if bad.exists() and not (ROOT/'qa/v8/failed-optix-00168.png').exists():
    shutil.move(str(bad),str(ROOT/'qa/v8/failed-optix-00168.png'))
for f in [168,288,744,960,1152,1296]:
    with (ROOT/f'render/proof-v8-cuda-{f}.log').open('w',encoding='utf8') as log:
        subprocess.run([str(BL),'--background','--python',str(ROOT/'render_city_v8.py'),'--','stills',str(f)],stdout=log,stderr=subprocess.STDOUT,check=True)
    print('STILL_READY',f,flush=True)
