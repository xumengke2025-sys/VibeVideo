from pathlib import Path
import json,hashlib,shutil,subprocess,sys,os
ROOT=Path(__file__).resolve().parent
e=json.loads((ROOT/'qa/v8/sample-engineering.json').read_text(encoding='utf8'))
for key,path in [('model_sha256','model/babylon-city-v8.blend'),('renderer_sha256','render_city_v8.py'),('timeline_sha256','v8-timeline.json')]:
 assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==e[key],key+' changed after the sample'
dest=ROOT/'render/frames-v8';dest.mkdir(exist_ok=True)
for f in range(612,684):
 p=dest/f'{f:05d}.png'
 if not p.exists():shutil.copy2(ROOT/'render/sample-v8'/p.name,p)
os.environ['CITY_DEVICE']='OPTIX';os.environ['CITY_DENOISER']='OPENIMAGEDENOISE';os.environ['CITY_DENOISE_GPU']='1';os.environ['CITY_COMPOSITOR']='GPU';os.environ['CITY_TILING']='0'
os.environ.pop('CITY_FRAME_DIR',None);os.environ.pop('CITY_SAMPLES',None)
(ROOT/'render/frozen-v8-manifest.json').write_text(json.dumps({'sample':e,'engine':'OptiX + OpenImageDenoise GPU + GPU compositor','full_samples':24,'reused_sample_frames':[612,683],'total_frames':1344,'source_freeze':'No visual source changes during render.'},ensure_ascii=False,indent=2),encoding='utf8')
cp=json.loads((ROOT/'CHECKPOINT.json').read_text(encoding='utf8'));cp['status']='v8_full_rendering';cp['v8_visual_validation']['pending']='Full film and actual audio perception';cp['v8_visual_validation']['current_proofs']='render/proof-v8-frozen/';cp['next_action']='Render remaining 1272 frames, encode and decode-check complete v8; retain exact review limitations.'
cp['v8_continuous_sample']='delivery/移轴强化-v8-市集到运河-3秒样段.mp4';cp['v8_full_render_manifest']='render/frozen-v8-manifest.json';cp['v8_runtime_note']='72帧连续OptiX + GPU OIDN + GPU合成通过，无分块；末帧约2.94秒。以32帧进程渲染完整片，复用同源码72帧样段。'
(ROOT/'CHECKPOINT.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf8')
adopt=json.loads((ROOT/'source-adoption.json').read_text(encoding='utf8'))
adopt['adoption']['current_blender']='render_city_v8.py：从样例迁移深度+屏幕清晰带和独立8Hz世界运动、连续摄影；Blender Cycles Z pass + Defocus，非WebGL Gather。v8采用7.5%半宽、38px最大虚化；神像用9.5%斜清晰带穿过两尊人物，人畜活动时间2.4倍。'
adopt['verification']['v8']='模型与八关键帧已实际生成查看；市集→运河72帧实际样段完成并查看18张间隔4帧联系表。全片正在渲染；实际听音尚未完成。'
(ROOT/'source-adoption.json').write_text(json.dumps(adopt,ensure_ascii=False,indent=2),encoding='utf8')
print('V8_FULL_RENDER_START; 72 matching frames reused',flush=True)
subprocess.run([sys.executable,str(ROOT/'render_pipeline_v8.py')],check=True)
