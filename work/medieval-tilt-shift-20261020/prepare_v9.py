from pathlib import Path
import shutil,json,hashlib
ROOT=Path(__file__).resolve().parent
hist=ROOT/'history/v8';hist.mkdir(parents=True,exist_ok=True)
for name in ['CHECKPOINT.json','plan.json','视频制作计划.md','source-adoption.json']:
    if not (hist/name).exists():shutil.copy2(ROOT/name,hist/name)
src=(ROOT/'render_city_v8.py').read_text(encoding='utf8').replace('babylon-city-v8.blend','babylon-city-v9.blend').replace('babylon-film-v8.blend','babylon-film-v9.blend')
# This patch changes model and output addresses only. The camera, timeline,
# world-time equations, sampling, compositor and audio are byte-for-byte retained.
src=src.replace('sample-v8','sample-v9').replace('proof-v8-final','proof-v9').replace('benchmark-v8','benchmark-v9').replace('eevee-test-v8','eevee-test-v9').replace('preview-v8','preview-v9').replace('frames-v8','frames-v9')
compile(src,'render_city_v9.py','exec');(ROOT/'render_city_v9.py').write_text(src,encoding='utf8')
src=(ROOT/'render_pipeline_v8.py').read_text(encoding='utf8').replace('frames-v8','frames-v9').replace('batch-logs-v8','batch-logs-v9').replace('pipeline-status-v8','pipeline-status-v9').replace('babylon-city-v8.blend','babylon-city-v9.blend').replace('render_city_v8.py','render_city_v9.py').replace('assemble_city_v8.py','assemble_city_v9.py')
(ROOT/'render_pipeline_v9.py').write_text(src,encoding='utf8')
src=(ROOT/'assemble_city_v8.py').read_text(encoding='utf8').replace('frames-v8','frames-v9').replace('Dream-of-Babylon-v8.mp4','Dream-of-Babylon-v9.mp4').replace('engineering-check-v8','engineering-check-v9').replace('ffprobe-v8','ffprobe-v9')
(ROOT/'assemble_city_v9.py').write_text(src,encoding='utf8')
cp=json.loads((ROOT/'CHECKPOINT.json').read_text(encoding='utf8'))
cp.update(version='v9',status='v9_targeted_model_repair',next_action='Build 24 pier/timber crossings and four mastless cargo barges; inspect formal-size stills, freeze sources, render complete v9 and ask same reviewer for local recheck.')
cp['review_budget']['repair_rounds_used']=1
cp['v9_revision']={'scope':['brick-pier timber bridges','legacy triangular sail boats converted to cargo barges'],'preserved':['1080x1920 56s 24fps','v8 camera timeline','v8 38px depth+tilt band','v8 music excerpt 29.5–85.5s','8Hz world motion'],'review':'same reviewer, necessary local recheck only; full coverage and actual audio perception remain incomplete'}
cp['unresolved']=['v9模型修复与全片渲染尚未完成','全片独立画面审核未完成，v8仅实际查看0–149帧','听音能力不可用，不能验证高潮听感与整体音画节奏']
(ROOT/'CHECKPOINT.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf8')
plan=json.loads((ROOT/'plan.json').read_text(encoding='utf8'));plan['v9_revision']=cp['v9_revision'];(ROOT/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
with (ROOT/'视频制作计划.md').open('a',encoding='utf8') as f:
    f.write('\n\n## v9 本轮一次针对性修复（2026-10-21）\n\n把24处近远景石拱桥统一改为砖墩承托木梁、平木板桥面，实体坡道连接两岸横街；四艘遗留三角帆船改为载货驳船，加入货包绑绳和艄公。v8新增四艘方帆船保留。依据希罗多德1.186及Encyclopaedia Iranica的桥梁资料作形式调整，尺寸与整体城市仍为艺术重构。摄影、音乐、38px移轴后期和8Hz世界运动保持；全片重新渲染以包含反射与阴影。沿用同一审片者，仅做改动和相邻镜头的必要复核，已用一次修复；全片与听音覆盖缺口如实保留。\n')
print('V9_SOURCES_PREPARED',flush=True)
