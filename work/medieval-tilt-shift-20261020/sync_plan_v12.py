import json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent;HISTORY=ROOT/'history/v11';HISTORY.mkdir(exist_ok=True)
for name in ['plan.json','视频制作计划.md','source-adoption.json']:
 if not (HISTORY/name).exists():shutil.copy2(ROOT/name,HISTORY/name)
timeline=json.loads((ROOT/'v12-timeline.json').read_text(encoding='utf8'))
p=ROOT/'plan.json';d=json.loads(p.read_text(encoding='utf8'));d['version']='v12';d['status']='rendering'
d['revision']={'previous_version':'history/v11/plan.json','reason':'修复已定位闪帧，增加祭司、巴比伦巡逻军队、埃及使团、全长大道居民和彩绘船只、船员及纤夫。','duration_reason':'沿用76秒与既有音乐节选。'}
d['assets_status']='model/babylon-city-v12.blend；8种角色模块、180名新增近景居民、8582名新增中远景居民、彩绘船只与两组纤夫。'
d['user_requirements']=list(dict.fromkeys(d['user_requirements']+['修复屏幕闪动','祭司、巴比伦军队、埃及使团与不同社会活动','最终全景主干道全长繁华人群','细化彩绘船体、船员、纤夫及牵引关系']))
actions={1:'持礼物和执扇的埃及使者在门楼外，由祭司和巴比伦守卫迎接；保留国王像。',2:'持盾持矛巡逻队穿过市集，市民按散点路线活动，驮畜和山羊保持独立分布。',3:'沿运河看彩绘货船、船工、货物和两组岸上纤夫；绳索连接实际船体和人物，纤道位于真实河岸高度。',5:'白袍祭司与侍祭在神像供奉前庭活动，保留神像朝向和器物。',6:'庭院神庙有祭司和侍祭，通道和楼梯保持连通。',8:'升高揭示巨城，主干道从近城一直延伸至城深处均有居民，并补充横街、桥梁与河岸人流。'}
for i,s in enumerate(d['shots']):
 ev=timeline['events'][i];s['id']=ev['id'];s['intent']=ev['name'];s['camera']['subjectId']=ev['id'];s['camera']['path']=timeline['shots'][i][2:]
 if i in actions:s['action']=actions[i]
 for read in s.get('reads',[]):read['item']=ev['name']
d['events']=timeline['events'];d['v12_revision']={'revision_plan':'v12-修复计划.md','sample_evidence':'qa/v12/production-sample-observations.json','model_evidence':'qa/v12/model-evidence.json','frozen_manifest':'render/frozen-v12-manifest.json','final_renderer':'render_city_v12.py','postprocess':'GPU separable multi-level Gaussian with physical depth and tilted clear band; replaces Defocus','render_samples':32,'temporal_validation':'all source frames and all encoded frames; strong-green and isolated two-sided discontinuity candidates','independent_review':'No new round; historical one-round budget unchanged.'}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
p=ROOT/'source-adoption.json';a=json.loads(p.read_text(encoding='utf8'));a['current_revision']='v12';a['current_renderer']='render_city_v12.py';a['adoption']['current_blender']='v12沿用原样例的真实深度+倾斜清晰带、独立8Hz世界活动和逐帧平滑相机；将不稳定Defocus换成GPU多级高斯混合，保留暖侧光、蓝釉与原创城邦建模。不是原WebGL gather着色器的逐行复刻。';a['verification']['v12']='37张最终模型正式尺寸样帧已渲染并检查强绿色异常；实际观察范围见qa/v12/production-sample-observations.json。完整1824帧渲染进行中。';p.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf8')
plan='''# 暮河城 · 巴比伦巨城 v12

沿用76秒、1080×1920竖屏、24fps，以及用户提供的《Dream of Babylon》29.5–105.5秒连续节选。保留地平线显城、连续城市路网、蓝釉与泥砖、暖侧光和移轴清晰带。

## 本次反馈修复

- 已定位上一版1.00秒及46.46秒的异常偏绿亮帧。新版以多级高斯合成替换Defocus，并在源帧及编码后执行全帧异常颜色、瞬间亮度和色彩跳变检查；机器检查不等同于完整审美审核。
- 城门外增加埃及使团的礼物及执扇人物，由祭司和巴比伦守卫迎接。市集有10人持盾持矛巡逻队。神庙及供奉前庭增加祭司与侍祭；平民保留独立路线、停留、工作及牲畜活动。
- 另加180名近处居民、8582名中远景居民，其中936人独立微动；覆盖长大道、横街、河岸与桥梁。远处按实际投影大小使用实体简模。
- 商船增加孔雀绿、靛蓝、赭红船体、彩边方帆、护舷、舵桨、缆绳、甲板和船员；货驳增加彩绘船舷与货物色彩。两组8名纤夫沿真实高度的连续纤道通行，牵引绳连接船体与人物，避免被房屋遮挡。

## 镜头时间表

| 时间 | 场景 |
| --- | --- |
| 0–8秒 | 地平线显城 |
| 8–16秒 | 蓝釉门楼、国王像与埃及使团 |
| 16–27秒 | 市集、居民与巴比伦巡逻军队 |
| 27–36.5秒 | 彩绘商船、船员与纤夫 |
| 36.5–44.5秒 | 王宫台地花园 |
| 44.5–53.5秒 | 神像与祭司供奉 |
| 53.5–62.2秒 | 庭院神庙仪式 |
| 62.2–67.6秒 | 粮仓码头 |
| 67.6–76秒 | 全长大道与无际巨城 |

## 音乐和工程

音轨沿用上一版：开头0.15秒渐入、末尾3秒渐出，环境声低混并以2秒交叉淡化衔接。未声称已实际听音或主观音画同步通过。

模型入口 model/babylon-city-v12.blend，建模脚本 model/revise_city_v12.py；摄影及后期 render_city_v12.py；交通缓存 traffic-v12.npz；镜头 v12-timeline.json；整片渲染 render_pipeline_v12.py；视频合成 assemble_city_v12.py。冻结输入见 render/frozen-v12-manifest.json。当前正在完整渲染，正式交付及实际检查范围会写入CHECKPOINT和qa/v12。

用户选择的既有独立审核一轮预算不重置；本轮为用户反馈后的制作修订。历史v11计划保存在 history/v11。巴比伦城邦、服饰和外交场景为幻想演绎，不作为特定历史事件或考古复原。
'''
(ROOT/'视频制作计划.md').write_text(plan,encoding='utf8')
print('V12_PLAN_SYNCED')
