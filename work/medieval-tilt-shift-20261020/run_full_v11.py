"""Freeze a selected proven render configuration and resume only matching frames."""
from pathlib import Path
from datetime import datetime
import os, sys, subprocess, hashlib, json, shutil
ROOT=Path(__file__).resolve().parent
config=json.loads((ROOT/'qa/v11/render-choice.json').read_text(encoding='utf8'))
files={'model':'model/babylon-city-v11.blend','renderer':'render_city_v11.py','traffic':'traffic-v11.npz','timeline':'v11-timeline.json','mix':'audio/final-mix-v11.wav'}
hashes={k:hashlib.sha256((ROOT/v).read_bytes()).hexdigest() for k,v in files.items()}
manifest={**hashes,'files':files,'engine':config['engine'],'samples':config['samples'],'width':1080,'height':1920,'fps':24,'frames':1824,'duration':76,'review':'User feedback revision; existing independent round remains exhausted.'}
mp=ROOT/'render/frozen-v11-manifest.json'
if mp.exists():assert json.loads(mp.read_text(encoding='utf8'))==manifest,'Source/configuration changed; do not mix frame sequences'
else:mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
env=os.environ.copy();env.update(CITY_DEVICE='OPTIX',CITY_DENOISER='OPENIMAGEDENOISE',CITY_DENOISE_GPU='1',CITY_COMPOSITOR='GPU',CITY_TILING='0')
if config['engine']=='EEVEE':env['CITY_ENGINE']='EEVEE'
else:env.pop('CITY_ENGINE',None)
for k in ['CITY_SAMPLES','CITY_FRAME_DIR']:env.pop(k,None)
# Reuse a sample only if every input hash and render engine matches the frozen film.
sample=ROOT/'qa/v11/sample-source.json'
dest=ROOT/'render/frames-v11';dest.mkdir(parents=True,exist_ok=True)
proof=ROOT/'qa/v11/proof-source-cycles.json'
if proof.exists():
    old=json.loads(proof.read_text(encoding='utf8'))
    expected={files[k]:hashes[k] for k in ['model','renderer','traffic','timeline']}
    if old.get('hashes')==expected and old.get('engine')==config['engine'] and config['samples']==24:
        for frame in old['frames']:
            p=ROOT/old['folder']/f'{frame:05d}.png'
            if p.exists() and not (dest/p.name).exists():shutil.copy2(p,dest/p.name)
if sample.exists():
    old=json.loads(sample.read_text(encoding='utf8'))
    if old.get('hashes')==hashes and old.get('engine')==config['engine']:
        for p in (ROOT/'render/sample-v11').glob('*.png'):
            if p.stem.isdigit() and not (dest/p.name).exists():shutil.copy2(p,dest/p.name)
cp=json.loads((ROOT/'CHECKPOINT.json').read_text(encoding='utf8'))
cp.update(status='v11_full_rendering',updated_at=datetime.now().isoformat(timespec='seconds'),next_action='Finish frozen 1824-frame render and encoding; producer verification of current output, then deliver with honest review/audio limits.')
cp['v11_revision'].update(frozen_manifest='render/frozen-v11-manifest.json',render_configuration=config)
(ROOT/'CHECKPOINT.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf8')
subprocess.run([sys.executable,'-X','utf8',str(ROOT/'render_pipeline_v11.py')],env=env,check=True)
print('V11_FULL_FILM_READY',flush=True)
