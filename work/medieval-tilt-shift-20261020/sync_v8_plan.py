from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parent
p=ROOT/'plan.json';backup=ROOT/'history/v8/plan-before-current-sync.json'
backup.parent.mkdir(parents=True,exist_ok=True)
if not backup.exists():shutil.copy2(p,backup)
d=json.loads(p.read_text(encoding='utf8'));tl=json.loads((ROOT/'v8-timeline.json').read_text(encoding='utf8'))
d['version']='v8';d['status']='full_render_in_progress'
d['clock_design']={'camera':'24fps连续影片时间，每镜独立smoothstep路径；镜头之间为同城切镜。','world':'qt=floor(t*8)/8；居民与牲畜使用mt=qt*2.4；船用qt、水面用连续t。','hero':'城市生活为主体，无龙或复杂人物表演。','speed_curve':[{'start':0,'end':56,'actors':2.4,'boats':1.0}]}
actions=['镜头从低位逐渐升高，由城门和神庙建立城市位置。','从门前空地俯视国王雕像，蓝釉门楼和浮雕在后景。','俯拍市场行人和驮畜，棚布、陶器与道路形成前后层次。','沿运河斜俯移动，船队、码头和台地神庙构成空间参照。','俯拍台地花园，展示蓝釉饰带、实体折返楼梯与种植层。','镜头对准神庙前庭两尊雕像；斜清晰带同时穿过两尊雕像。','拉远回到大道、运河、王宫与神庙组成的巨型城市，尾段渐暗。']
anchors=['gate-01 + temple-01','gate-01 + market-01','market-01 + canal-01','canal-01 + garden-01','garden-01 + temple-01','temple-01 + gate-01']
d['shots']=[]
for i,e in enumerate(tl['events']):
 a=e['start'];b=e['end'];span=b-a
 d['shots'].append({'id':e['id'],'start':a,'end':b,'intent':e['name'],'states':{'establish':a+min(1,span*.2),'action':(a+b)/2,'result':b-min(.8,span*.15)},'action':actions[i],'camera':{'mode':'低位升机后俯拍' if i==0 else '高位斜俯移动','subjectId':e['id'],'handoff':'固定城市坐标，镜头之间切镜；不声称无剪辑长镜头。','path':e['camera']},'reads':[{'item':e['name'],'appear':a,'readable':a+min(1,span*.2),'leave':b}],'risks':[[max(a,b-1.5),b-.05]]})
d['connections']=[{'time':s[0],'kind':'同一三维城市中的切镜','anchor':anchors[i],'window':[s[0]-1,s[0]+1]} for i,s in enumerate(tl['shots'][1:])]
d['events']=[{'id':e['id'],'at':e['start'],'end':e['end'],'trigger':'依据候选音乐能量段落安排，未实际听音确认乐句','response':actions[i]} for i,e in enumerate(tl['events'])]
d['quality_contract']['status']='frozen_model_and_sample_verified_full_rendering'
d['quality_contract']['final_sampling']='Cycles OptiX 24 samples，adaptive threshold .065，OpenImageDenoise GPU，GPU Defocus合成；1080×1920原生、无内部分块，真实持久缓存。关键图32 samples；未使用WebGL Gather或超采样。'
d['quality_contract']['proof_times']=[.5,3,7,12,21,31,40,45,48,50.833,54]
d['quality_contract']['motion_blur']='未开启全局运动模糊；保留8Hz微缩延时步进。'
d['pilot']={'window':[25.5,28.5],'frames':72,'status':'encoded_sample_engineering_passed','video':'delivery/移轴强化-v8-市集到运河-3秒样段.mp4','viewed':'18张间隔4帧联系表；非完整实时观看；未实际听音。'}
d['evidence'].update({'validation_scope':'v8关键图与72帧样段真实输出；已看关键图和18张样段联系表；全片尚未完成。','engineering_report':'qa/v8/sample-engineering.json','frame_audit':'qa/v8/sample-contact.png','heard_audio':False})
d['v8_revision']['events']=tl['events'];d['v8_revision']['tilt_shift'].update({'world_motion':'8Hz，人物及牲畜2.4倍活动时间；相机连续。','divine_band_half_height':.095,'divine_band_tilt':-.45,'standard_band_tilt':.07})
d['v8_revision']['authoritative_timeline']='v8-timeline.json';d['v8_revision']['frozen_manifest']='render/frozen-v8-manifest.json'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print('V8 plan synchronized with frozen renderer and timeline.')
