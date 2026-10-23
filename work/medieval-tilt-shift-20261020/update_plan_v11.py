from pathlib import Path
from datetime import datetime
import json
ROOT=Path(__file__).resolve().parent
timeline=json.loads((ROOT/'v11-timeline.json').read_text(encoding='utf8'))
plan=json.loads((ROOT/'plan.json').read_text(encoding='utf8'))
actions=[
 '相机越过前景沙坡逐渐抬高，固定城市从遮挡后显露。',
 '沿蓝釉门楼和国王雕像缓慢推进，保留大道通行空间。',
 '伴随市集大道向前，居民独立穿行、停留交谈，驮畜零散分布。',
 '沿同一运河观看有船工与货物的驳船，保留桥梁与岸坡连接。',
 '从台地侧面读出实体楼梯、柱廊和层叠花园。',
 '从南入口斜看不同神像正面，读出冠饰、伏狮与供奉器物。',
 '沿横街进入西侧新神庙，展现柱廊院落与蓝釉神龛。',
 '斜俯东岸粮仓和装卸院落，码头工人与牲畜占据真实开放空间。',
 '升高拉远，重新交代大道、运河、公共建筑和延伸至远方的住宅街区。'
]
plan.update(version='v11',status='production',duration=76,frame_count=1824,
 intent='以同一座巴比伦幻想巨城的街巷、河运、仪式与贸易生活，呈现宏伟而精细的移轴微缩城市。',
 assets_status='model/babylon-city-v11.blend；新庭院神庙、粮仓码头、独立交通与面向入口的多种雕像。')
plan['revision']={'previous_version':'history/v10/plan.json','reason':'用户反馈行人牲畜列队、神像朝向与丰富度不足，授权增加建筑和片长。','duration_reason':'56秒扩为76秒，增加独立神庙与粮仓镜头，并保留原有巨城街景段落。'}
plan['shots']=[];plan['connections']=[];plan['events']=timeline['events']
for i,(shot,event,action) in enumerate(zip(timeline['shots'],timeline['events'],actions)):
 a,b=shot[:2];span=b-a
 plan['shots'].append({'id':event['id'],'start':a,'end':b,'intent':event['name'],'states':{'establish':round(a+min(1,span*.15),3),'action':round(a+span*.5,3),'result':round(b-.6,3)},'action':action,'camera':{'mode':'共享三维世界中的平滑位置/看向点摄影','subjectId':event['id'],'handoff':'同一城市的景别切换，保留地理关系。','path':shot[2:]},'reads':[{'item':event['name'],'appear':a,'readable':a+min(1,span*.15),'leave':b}],'risks':[[max(a,b-1.0),b-.04]]})
 if i:plan['connections'].append({'time':a,'kind':'同一三维世界中的景别切换','anchor':'持续的主干道、运河与近东建筑材料','window':[a-.5,a+.5]})
audio=plan['audio'];audio.update(master_clock='原曲29.5–105.5秒连续节选；摄影按已有候选能量起音编排，未实际听音。',source_status='用户本地音乐；连续节选延长至76秒，低混环境声循环采用2秒交叉淡化。',notes='音乐能量候选仅为时序依据；实际听音不可用。',source_excerpt_seconds=[29.5,105.5],fade_out_seconds=[73,76],cues=[{'start':0,'end':.15,'music':'原曲29.5秒起，0.15秒渐入'},{'start':.15,'end':73,'music':'连续电影原曲与低混环境声'},{'start':73,'end':76,'music':'3秒渐出'}])
plan['v11_revision']={'traffic':'traffic-v11.npz，8Hz固定步长、独立路线、停顿、局部避让和间距回退约束。','new_buildings':['西侧庭院神庙','东岸粮仓和工作码头'],'sculpture':'南向主像与向庭院侧像；不同材料、冠饰、伏狮、供桌和铭文石碑。','review':'用户反馈修订；既有独立审核预算未重置，当前版本由制作角色检查。'}
plan['evidence']={'status':'v11 production; current render and output evidence pending','directory':'qa/v11','timeline':'v11-timeline.json'}
(ROOT/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
cp=json.loads((ROOT/'CHECKPOINT.json').read_text(encoding='utf8'))
cp.update(status='v11_final_proofs_pending',updated_at=datetime.now().isoformat(timespec='seconds'),next_action='Inspect final cleared civic sites, baked-pose actors and widened statue focus, then render continuous street sample and freeze full film.')
cp['v11_revision'].update(traffic_clearance='All 609 8Hz states passed radius checks before final static-site cleanup; see qa/v11/traffic-check.json.',additional_fixes=['Clear realised residential meshes from new civic sites.','Move grain visitors to open inner courtyard; separate dock workers.','Bake each shared stride collection into a single mesh.','Widen diagonal sculpture focus band for both figures.'])
(ROOT/'CHECKPOINT.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf8')
print('V11_PLAN_UPDATED')
