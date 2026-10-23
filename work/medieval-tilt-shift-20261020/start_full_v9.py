from pathlib import Path
import json,hashlib,shutil,subprocess,sys,os,datetime
ROOT=Path(__file__).resolve().parent
hashes={key:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for key,path in [('model_sha256','model/babylon-city-v9.blend'),('renderer_sha256','render_city_v9.py'),('timeline_sha256','v8-timeline.json'),('mix_sha256','audio/final-mix-v8.wav')]}
proof=ROOT/'render/proof-v9';dest=ROOT/'render/frames-v9';dest.mkdir(exist_ok=True)
for f in [168,744,800,1296]:
    if not (dest/f'{f:05d}.png').exists():shutil.copy2(proof/f'{f:05d}.png',dest/f'{f:05d}.png')
os.environ.update(CITY_DEVICE='OPTIX',CITY_DENOISER='OPENIMAGEDENOISE',CITY_DENOISE_GPU='1',CITY_COMPOSITOR='GPU',CITY_TILING='0')
os.environ.pop('CITY_FRAME_DIR',None);os.environ.pop('CITY_SAMPLES',None)
manifest={**hashes,'version':'v9','repair_round':1,'proof_frames_reused':[168,744,800,1296],'samples':24,'engine':'OptiX + GPU OIDN + GPU compositor','source_freeze':'No model, renderer, camera, timeline or mix changes during rendering','proofs_actually_viewed_by_maker':[168,744],'proof_limit':'static production check, not independent video review'}
(ROOT/'render/frozen-v9-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
cp=json.loads((ROOT/'CHECKPOINT.json').read_text(encoding='utf8'));cp.update(status='v9_full_rendering',updated_at=datetime.datetime.now().isoformat(),next_action='Render complete v9 from frozen sources, encode with retained v8 mix, full decode check, same reviewer local recheck and deliver.')
cp['completed'].append('v9模型已实际生成：24处砖墩木梁桥、实体引坡和4艘载货驳船；正式尺寸24采样试帧完成，已查看7秒与31秒画面。')
cp['v9_model']='model/babylon-city-v9.blend';cp['v9_render_manifest']='render/frozen-v9-manifest.json';cp['unresolved'][0]='v9全片1344帧渲染进行中，4张正式参数试帧复用'
(ROOT/'CHECKPOINT.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf8')
print('V9_FULL_RENDER_START; four matching formal-size proof frames reused',flush=True)
subprocess.run([sys.executable,str(ROOT/'render_pipeline_v9.py')],check=True)
cp=json.loads((ROOT/'CHECKPOINT.json').read_text(encoding='utf8'));cp.update(status='v9_candidate_ready_local_recheck_pending',updated_at=datetime.datetime.now().isoformat(),next_action='Extract targeted repair evidence and give same reviewer necessary local recheck; deliver complete video with actual coverage limitations.')
cp['completed'].append('v9全部1344帧正式渲染、音乐编码及全片解码检查完成。');cp['unresolved'][0]='v9改动及相邻镜头复核待完成'
report=json.loads((ROOT/'delivery/engineering-check-v9.json').read_text(encoding='utf8'));cp['final_candidate']=report['video'];cp['final_candidate_sha256']=report['sha256'];cp['verification']['render']='v9全部1344帧，1080×1920、24fps、56秒；完整音视频解码检查通过。'
(ROOT/'CHECKPOINT.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf8')
