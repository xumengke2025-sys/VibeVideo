from pathlib import Path
import json, subprocess, os, hashlib, time
ROOT=Path(__file__).resolve().parent
config=json.loads((ROOT/'qa/v11/render-choice.json').read_text(encoding='utf8'))
files={'model':'model/babylon-city-v11.blend','renderer':'render_city_v11.py','traffic':'traffic-v11.npz','timeline':'v11-timeline.json','mix':'audio/final-mix-v11.wav'}
record={'engine':config['engine'],'hashes':{k:hashlib.sha256((ROOT/v).read_bytes()).hexdigest() for k,v in files.items()},'frames':[588,659],'actual_viewed':False,'actual_listened':False}
(ROOT/'qa/v11/sample-source.json').write_text(json.dumps(record,indent=2),encoding='utf8')
env=os.environ.copy();env.update(CITY_DEVICE='OPTIX',CITY_DENOISER='OPENIMAGEDENOISE',CITY_DENOISE_GPU='1',CITY_COMPOSITOR='GPU',CITY_TILING='0',CITY_FRAME_DIR='sample-v11')
if config['engine']=='EEVEE':env['CITY_ENGINE']='EEVEE'
else:env.pop('CITY_ENGINE',None)
blender=ROOT.parents[1]/'tools/blender-portable/blender-4.5.3-windows-x64/blender.exe'
with (ROOT/'qa/v11/continuous-sample.log').open('w',encoding='utf8') as log:
    subprocess.run([str(blender),'--background','--python-exit-code','1','--python',str(ROOT/'render_city_v11.py'),'--','range','588','660'],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
assert all((ROOT/f'render/sample-v11/{f:05d}.png').exists() for f in range(588,660))
ff='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
output=ROOT/'delivery/v11-街景修复样段.mp4'
subprocess.run([ff,'-y','-hide_banner','-loglevel','error','-framerate','24','-start_number','588','-i',str(ROOT/'render/sample-v11/%05d.png'),'-ss','24.5','-i',str(ROOT/'audio/final-mix-v11.wav'),'-t','3','-c:v','libx264','-crf','17','-threads:v','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',str(output)],check=True)
record.update(video=str(output),sha256=hashlib.sha256(output.read_bytes()).hexdigest(),status='rendered; producer continuous-frame inspection pending')
(ROOT/'qa/v11/sample-source.json').write_text(json.dumps(record,indent=2),encoding='utf8')
print('V11_SAMPLE_READY',str(output),flush=True)
