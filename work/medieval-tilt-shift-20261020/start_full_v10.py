from pathlib import Path
from datetime import datetime
import os,sys,json,hashlib,shutil,subprocess
ROOT=Path(__file__).resolve().parent
hashes={key:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for key,path in [('model_sha256','model/babylon-city-v10.blend'),('renderer_sha256','render_city_v10.py'),('timeline_sha256','v8-timeline.json'),('mix_sha256','audio/final-mix-v8.wav')]}
manifest={**hashes,'version':'v10','scope':'Follow-up parenting correction and historical-style verification; no additional independent review round.','changed_object':'Boat crossbench.001','samples':24,'engine':'OptiX + GPU OIDN + GPU compositor','source_freeze':'No model, renderer, timeline or mix changes during full rendering','formal_proof_frames_reused':[744,852],'proof_frames_actually_viewed':[744,852]}
mp=ROOT/'render/frozen-v10-manifest.json'
if mp.exists():
    old=json.loads(mp.read_text(encoding='utf8'))
    assert all(old[k]==v for k,v in hashes.items()),'Frozen sources changed'
else:mp.write_text(json.dumps(manifest,indent=2),encoding='utf8')
dest=ROOT/'render/frames-v10';dest.mkdir(exist_ok=True)
for f in [744,852]:
    if not (dest/f'{f:05d}.png').exists():shutil.copy2(ROOT/'render/proof-v10'/f'{f:05d}.png',dest/f'{f:05d}.png')
os.environ.update(CITY_DEVICE='OPTIX',CITY_DENOISER='OPENIMAGEDENOISE',CITY_DENOISE_GPU='1',CITY_COMPOSITOR='GPU',CITY_TILING='0')
for key in ['CITY_FRAME_DIR','CITY_SAMPLES']:os.environ.pop(key,None)
cp=json.loads((ROOT/'CHECKPOINT.json').read_text(encoding='utf8'))
cp.update(status='v10_full_rendering',updated_at=datetime.now().isoformat(timespec='seconds'),next_action='Finish frozen full 1344-frame render; era-style and tilt evidence; encode and full decode; deliver current video with honest review limits.')
cp['completed'].append('v10修复第四艘船坐板层级；正式尺寸744与852帧已实际查看，河中孤立木条消失，坐板回到船内。')
cp['v10_model']='model/babylon-city-v10.blend';cp['v10_render_manifest']='render/frozen-v10-manifest.json'
(ROOT/'CHECKPOINT.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf8')
print('V10_FROZEN_FULL_RENDER_STARTED',flush=True)
subprocess.run([sys.executable,'-X','utf8',str(ROOT/'render_pipeline_v10.py')],check=True)
cp=json.loads((ROOT/'CHECKPOINT.json').read_text(encoding='utf8'))
eng=json.loads((ROOT/'delivery/engineering-check-v10.json').read_text(encoding='utf8'))
cp.update(status='v10_candidate_rendered',final_candidate=eng['video'],final_candidate_sha256=eng['sha256'],updated_at=datetime.now().isoformat(timespec='seconds'),next_action='Inspect current encoded era/tilt and targeted correction evidence; finalize current output and delivery report.')
cp['completed'].append('v10全部1344帧正式尺寸渲染完成；56秒音画编码、解码及规格检查通过。')
(ROOT/'CHECKPOINT.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf8')
print('V10_FULL_CANDIDATE_READY',eng['sha256'],flush=True)
