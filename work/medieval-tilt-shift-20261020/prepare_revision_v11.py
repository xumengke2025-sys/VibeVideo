from pathlib import Path
from datetime import datetime
import json, shutil

ROOT=Path(__file__).resolve().parent
history=ROOT/'history/v10';history.mkdir(parents=True,exist_ok=True)
for name in ['CHECKPOINT.json','plan.json','视频制作计划.md','source-adoption.json']:
    if not (history/name).exists():shutil.copy2(ROOT/name,history/name)
shots=[
 [0,8,[-48,-153,6],[-60,-89,104],[15,72,8],[14,61,9],45,48],
 [8,16,[15,-36,34],[14,-25,36],[-4.8,-12,3.7],[-4.8,-12,3.7],46,46],
 [16,27,[23,9,41],[22,37,42],[0,29,1],[0,57,1],52,52],
 [27,36.5,[6,38,47],[12,63,49],[33,63,0],[34,85,1],52,52],
 [36.5,44.5,[-8,21,78],[-9,53,70],[-48,69,9],[-49,84,12],47,47],
 [44.5,53.5,[33,24,29],[34,29,29.5],[51.5,48.7,8.2],[51.5,48.7,8.2],45,47],
 [53.5,62.2,[-17,108,46],[-20,114,43],[-47,141,6],[-47,145,6],47,47],
 [62.2,67.6,[22,113,40],[23,121,38],[56,140,3.8],[57,142,3.8],47,47],
 [67.6,76,[-105,-140,180],[-151,-197,248],[10,113,5],[8,140,6],43,43]
]
names=['地平线显城','蓝釉门楼与国王','自然市集人畜','运河货船','王宫台地花园','神像与供奉前庭','庭院神庙','粮仓码头','无际巨城']
timeline={'duration':76,'fps':24,'frame_count':1824,'shots':shots,'events':[{'id':f'v11-shot-{i}','start':s[0],'end':s[1],'name':names[i],'music_source_time':29.5+s[0]} for i,s in enumerate(shots)],'music':{'source':str(ROOT/'audio/user-provided-Dream-Of-Babylon.mp3'),'excerpt_start':29.5,'excerpt_end':105.5,'audio_perceived':False,'note':'Continuous source excerpt. Final city reveal at source 97.1 s, previously measured onset/energy candidate; not perceptually confirmed.'}}
(ROOT/'v11-timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf8')
text=(ROOT/'render_city_v10.py').read_text(encoding='utf8')
text=text.replace('56s Blender','76s Blender').replace('v10','v11').replace('v8-timeline.json','v11-timeline.json')
text=text.replace('scene.frame_end=1344','scene.frame_end=1824').replace('range(1344)','range(1824)')
text=text.replace("if mode=='stills':scene.cycles.samples=32","if mode=='stills':scene.cycles.samples=24")
text=text.replace("if mode=='eevee':", "if mode=='eevee' or os.environ.get('CITY_ENGINE')=='EEVEE':")
text=text.replace('scene.eevee.taa_render_samples=32','scene.eevee.taa_render_samples=64')
text=text.replace("def at(t):", "traffic=np.load(ROOT/'traffic-v11.npz')\nv11actors=[bpy.data.objects[str(n)] for n in traffic['names']]\nv11poses=[[bpy.data.collections[n] for n in json.loads(o['stride_modules'])] for o in v11actors]\n\ndef at(t):")
text=text.replace(" noise.inputs['W'].default_value=t*.09", " row=min(len(traffic['state'])-1,int(math.floor(t*8)))\n for ob,poses,s in zip(v11actors,v11poses,traffic['state'][row]):\n  ob.location=(float(s[0]),float(s[1]),float(s[2]));ob.rotation_euler.z=float(s[3])\n  pose=poses[int(s[4])]\n  if ob.instance_collection!=pose:ob.instance_collection=pose\n noise.inputs['W'].default_value=t*.09")
text=text.replace('(t-54.5)/1.5','(t-74.5)/1.5')
text=text.replace('frames=[168,288,504,744,960,1152,1296]','frames=[168,288,504,756,972,1176,1392,1560,1752]')
(ROOT/'render_city_v11.py').write_text(text,encoding='utf8')
cp=json.loads((ROOT/'CHECKPOINT.json').read_text(encoding='utf8'))
cp.update(version='v11',status='v11_model_build_and_proofs_pending',duration=76,frame_count=1824,updated_at=datetime.now().isoformat(timespec='seconds'),objective='按用户反馈修复列队人畜、神像朝向和丰富度；新增庭院神庙与粮仓码头，完成76秒竖屏巴比伦巨城移轴影片。',next_action='Build v11 model and baked traffic; inspect final-resolution street, sculpture, new buildings and continuous sample, then freeze sources and render full film.')
cp['feedback'].append('v11用户指出行人与牲畜过于整齐、神像朝向和丰富度不足；授权新增建筑并延长片长。')
cp['v11_revision']={'duration':76,'frame_count':1824,'source_model':'model/babylon-city-v10.blend','model':'model/babylon-city-v11.blend','traffic':'traffic-v11.npz','renderer':'render_city_v11.py','timeline':'v11-timeline.json','changes':['Independent obstacle-aware pedestrian routes, conversations and working pauses','Small scattered donkey groups and browsing goats with independent gait','Distinct statues oriented to the actual entrance, lower three-quarter photography, lions and offerings','Courtyard temple and grain exchange with connected cross street and quay'],'review':'User feedback revision; existing independent review budget unchanged. Producer checks only; no claimed new independent pass.'}
(ROOT/'CHECKPOINT.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf8')
(ROOT/'v11-修复计划.md').write_text('''# v11 用户反馈修复

正式规格：1080×1920、24fps、76秒（1824帧）。沿用本片画幅、Dream of Babylon音乐、蓝釉与土金材质、地平线开场、真实深度加窄清晰带的移轴后期。v10和旧记录保留。

112名主要通行行人使用各自路线、速度、停顿与局部避让；另有摊前顾客、对话小组、庭院访客、码头工人与供奉者。驮畜改为小组停靠、零散通行，山羊在市集局部活动；固定8Hz缓存保证任意帧寻址一致，不用整列正弦平移。步态为共享六姿态，属于微缩风格化动作。

神像沿实际南侧台阶轴线布置，主像面向入口，侧像转向庭院。主像改为不同冠饰和材料，新增伏狮、供桌、祭盆与铭文石碑。摄影从极高俯视调整到能看到正面和持物的斜俯角，保留前后微缩散焦。

新增西侧庭院神庙和东岸粮仓码头，分别为柱廊与仪式院落、厚墙仓房与露天装卸场；接入现有路网，留出大道、运河和船只通行空间。两段新增镜头服务建筑差异与工作场景，不靠延长原镜头凑时长。

0–8地平线显城；8–16蓝釉城门与国王；16–27市集；27–36.5运河；36.5–44.5花园；44.5–53.5神像；53.5–62.2庭院神庙；62.2–67.6粮仓码头；67.6–76巨城全景。

音乐采用原曲29.5–105.5秒连续节选，延续开场，结尾巨城拉远对齐原曲97.1秒的既有能量/起音候选。保持低混环境声，末3秒收束。能量分析不等于实际听音，听感限制保留。

先验证市集的非列队分布和连续运动、神像正面与新建筑正式尺寸渲染，再冻结源码扩展全片。用户反馈修复沿用本片已有审核选择与一轮预算，不重新启动独立审核。所有新结论绑定新片哈希，制作复核不称独立审核通过。
''',encoding='utf8')
print('V11_RENDERER_TIMELINE_AND_CHECKPOINT_READY')
