"""Create a scoped v13 revision while preserving delivered v12 and its frames."""
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone

root=Path(__file__).resolve().parent
qa=root/'qa/v13';qa.mkdir(exist_ok=True)
history=root/'history/v12';history.mkdir(exist_ok=True)
for name in ['CHECKPOINT.json','plan.json','source-adoption.json']:
    if not (history/name).exists():shutil.copy2(root/name,history/name)
for old,new in [('v12-timeline.json','v13-timeline.json'),('traffic-v12.npz','traffic-v13.npz')]:
    shutil.copy2(root/old,root/new)
source=(root/'render_city_v12.py').read_text(encoding='utf8')
source=source.replace('v12','v13').replace('V12','V13')
# Scene metadata and inherited actor collections retain their established names.
source=source.replace("scene['v13_special']","scene['v12_special']").replace("scene['v13_mid_crowd']","scene['v12_mid_crowd']").replace("scene['v13_tows']","scene['v12_tows']")
source=source.replace('p=(phase%math.tau)/math.tau*6;i=int(p);f=p-i','count=len(keys)+1;p=(phase%math.tau)/math.tau*count;i=int(p);f=p-i').replace('(i+1)%6','(i+1)%count')
source=source.replace("if kind=='patrol':p[1]+=wt*ev['speed'];phase+=wt*ev['speed']*4.6", "if kind=='patrol':\n   p[1]+=t*ev['speed'];phase+=math.tau*t*ev['speed']/ev['stride_length']")
(root/'render_city_v13.py').write_text(source,encoding='utf8')
for old,new in [('assemble_city_v12.py','assemble_city_v13.py'),('finalize_delivery_v12.py','finalize_delivery_v13.py')]:
    text=(root/old).read_text(encoding='utf8').replace('v12','v13')
    # The existing music is deliberately unchanged.
    (root/new).write_text(text,encoding='utf8')
pipeline=(root/'render_pipeline_v12.py').read_text(encoding='utf8').replace('v12','v13')
pipeline=pipeline.replace("SAMPLE=sorted(set([23,24,25,288,528,756,1114,1115,1116,1176,1392,1560,1752]+list(range(732,756))))", "SAMPLE=sorted(set([396,528,636,660,744,864,168,1752]+list(range(516,540))+list(range(732,756))))")
pipeline=pipeline.replace("source=QA/'sample-source.json'", """# Preserve established shots outside the four views containing the changes.
# In these shots the new river paths/patrol are outside the camera view;
# separate layout evidence records the scoped reuse decision.
reuse_ranges=[(192,384),(876,1623)]
parent_manifest=json.loads((OUT/'frozen-v12-manifest.json').read_text(encoding='utf8'))
for name,digest in parent_manifest['files'].items():
 assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,('Parent inputs changed',name)
reused=[]
for a,b in reuse_ranges:
 for f in range(a,b):
  src=OUT/'frames-v12'/f'{f:05d}.png';dest=folder/src.name
  assert src.exists(),src
  if not dest.exists():shutil.copy2(src,dest)
  reused.append(f)
(QA/'frame-provenance.json').write_text(json.dumps({'parent_manifest':'render/frozen-v12-manifest.json','reused_ranges_exclusive':reuse_ranges,'reused_count':len(reused),'rerendered_shots':[0,2,3,8],'reason':'Changes affect river and patrol views. Gate reception, garden, statue, courtyard temple and grain exchange retain the delivered v12 frames.'},indent=2),encoding='utf8')
source=QA/'sample-source.json'""")
(root/'render_pipeline_v13.py').write_text(pipeline,encoding='utf8')
checkpoint=json.loads((root/'CHECKPOINT.json').read_text(encoding='utf8'))
checkpoint.update(objective='将纤夫分到运河两岸，改进士兵队形、脚步和持械协调；交付76秒v13。',version='v13',status='v13_model_preparing',updated_at=datetime.now(timezone.utc).isoformat())
checkpoint['v13_revision']={'requests':['纤夫在河流两边拉纤','士兵动作与队形更协调'],'preserved':['76s','1080x1920','24fps','music excerpt','v12 stable tilt-shift compositor'],'model':'model/babylon-city-v13.blend','renderer':'render_city_v13.py','pipeline':'render_pipeline_v13.py','new_review_round':False,'next_action':'Build revised model, inspect formal-size stills and short continuous samples before scoped full render.'}
checkpoint['next_action']=checkpoint['v13_revision']['next_action']
(root/'CHECKPOINT.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2),encoding='utf8')
(root/'v13-修复计划.md').write_text('v13：两岸拉纤与协调巡逻\n\n沿用76秒竖屏1080×1920、24fps、原音乐、稳定移轴合成。两组纤夫分置x=23.35和41.35的两岸实体纤道；保持各自与船只的系缆关系。士兵采用共享步频、12姿态插值、交替支撑脚、明确手部兵器连接，巡逻队缩为合理步速并保持双列间距。\n\n先验证市集、运河正式尺寸样帧和各1秒连续样段；然后重渲开场、巡逻、运河、片尾全景，复用已交付的其余未改镜头。复用清单保存qa/v13/frame-provenance.json，历史v12完整保留。\n\n本轮为用户反馈修改，不重开独立审核；实际查看范围和听音限制按证据记录。\n',encoding='utf8')
print('V13_PREPARED',flush=True)
