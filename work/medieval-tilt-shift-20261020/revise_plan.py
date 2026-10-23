from pathlib import Path
import json
root=Path(__file__).parent
p=json.loads((root/'plan.json').read_text(encoding='utf-8-sig'))
p.update(title='暮河城 · 街巷与运河',version='v3',status='model_first_quality_rebuild',intent='先建立精细巴比伦城邦模型，再以连续摄影与移轴表现城市街景的日常生命。')
p['removed']=['龙','送火','降落','火种接触','点燃仪式','由送火触发的灯链']
p['assets_status']='旧Three预演未达标；正在制作Blender Cycles城门与街区模型质量样板。'
p['user_requirements'] += ['先做好模型','不要龙，城市街景即可']
p['world']['route']=['城外地平线','蓝釉城门','门内市集','运河与码头','阶梯神庙','全城']
p['world']['materials']=['独立倒角釉砖','有真实厚度的拱洞与浮雕','泥砖与磨损石材','深窗与木梁','织物棚布','陶罐','有反射的水面']
p['clock_design']['hero']='已取消角色表演；船只与行人只作尺度和日常活动。'
p['audio']['cues']=[
 {'start':0,'end':8,'music':'风与稀疏拨弦起，低弦随地平线显城渐入'},
 {'start':8,'end':18,'music':'木管四音城市主题、细拨弦和轻框鼓'},
 {'start':18,'end':28,'music':'鼓减弱，给市集环境、棚布和脚步留空间'},
 {'start':28,'end':38,'music':'沿运河展开旋律，水流和船桨近远变化'},
 {'start':38,'end':48,'music':'神庙入画时主题扩宽，克制铜质共鸣'},
 {'start':48,'end':56,'music':'52秒落定，停止新旋律，保留自然余韵'}]
p['audio']['source_status']='已找到本地GeneralUser GS音源及授权文件；尚未编曲、生成或实际听音。'
p['audio']['foley']=['风','水流','船桨','远人群','棚布','足步']
specs=[
 ('horizon-city',0,8,'城市从地平线上逐层显露','镜头升高解除土坡遮挡；神庙、城门、城墙先后可辨。','低位升机，逐步建立城市体量'),
 ('glazed-gate',8,18,'蓝釉门楼和微缩街区','在斜俯机位辨认蓝釉、立体浮雕、厚拱洞以及穿门街道。','约45–55度斜俯，缓推并偏移建立真实视差'),
 ('market-street',18,28,'城内日常与材质','看见棚布、陶罐、木梁、院落与少量行人，不安排复杂角色表演。','顺街道移动，保持前中后景与屋顶锚点'),
 ('canal-quay',28,38,'水面、船只与街巷关系','沿码头进入纵深运河，船慢行，水面反射随视角变化。','顺河斜俯侧移；桥和岸墙构成尺度参照'),
 ('terraced-temple',38,48,'城市的神庙核心','露台、阶梯、蓝釉饰带和种植层逐层展开。','从河道抬升，先对准神庙再移动机位'),
 ('whole-city',48,56,'局部重新回到整座城','城门、运河与神庙同处一幅画面，52秒起落定。','高位斜俯拉远，保留四秒收束')]
p['shots']=[]
for key,a,b,intent,action,cam in specs:
 p['shots'].append({'id':key,'start':a,'end':b,'intent':intent,'states':{'establish':a+1,'action':(a+b)/2,'result':b-1},'action':action,'camera':{'mode':cam,'subjectId':key,'handoff':'保留共同城邦坐标与相邻地标'},'reads':[{'item':intent,'appear':a,'readable':a+2,'leave':b}],'risks':[[max(a,b-2),b-.1]]})
p['revision']={'previous_version':'history/v2-before-streets/plan.json','reason':'用户指出质感不足，要求模型优先并删除龙；保留认可的近东巴比伦、地平线显城、竖屏和一次AI审核。','duration_reason':'保留原56秒作为编排起点；模型验证后按空间与音乐调整。'}
p['concept']={'status':'approved_direction_retained','paths':['concepts/city-overview-v1.png','concepts/city-reveal-early-v1.png'],'user_feedback':'保留建筑视觉方向，删除龙；实际渲染需先提升模型质感。'}
p['connections']=[{'time':t,'kind':'连续世界中的注意交接','anchor':a,'window':[t-1.5,t+1.5]} for t,a in [(8,'gate-01 + temple-01'),(18,'gate-01 + market-01'),(28,'market-01 + quay-01'),(38,'canal-01 + temple-01'),(48,'temple-01 + gate-01')]]
p['events']=[{'id':'horizon-reveal','at':2,'end':8,'trigger':'机位升高','response':'土坡遮挡逐渐解除'}, {'id':'street-slow','at':18,'end':23,'trigger':'进入街区细节','response':'背景活动速度降至正常'}, {'id':'quay-pass','at':28,'end':38,'trigger':'转入运河','response':'船、水、码头与桥呈现空间关系'}, {'id':'temple-rise','at':38,'end':48,'trigger':'神庙逐层揭示','response':'镜头与配乐渐展开'}, {'id':'hold','at':52,'end':56,'trigger':'全城关系完整','response':'相机落定，音乐留尾韵'}]
p['quality_contract']['asset_priority']=['城门拱洞与蓝釉浮雕','门内街巷、屋顶与布棚','阶梯神庙','码头船只与水面','远景街区']
p['quality_contract']['dof_risks']=['有符号CoC抵消','棕榈和屋檐边缘漏色','水面深度','釉面高光过曝','焦点跳变']
p['quality_contract']['encoding']='对照无损源帧与MP4，重点检查砖缝、水面、植被和细小人物。'
p['quality_contract']['proof_times']=[3.5,11,23,33,44,51]
p['pilot']={'material':[8,12],'primary':[15,23],'secondary':[28,33],'status':'awaiting_model_quality_proof','notes':'先完成无景深模型样板，再验证城门向街巷及运河的连续空间移动。'}
(root/'plan.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'视频制作计划.md').write_text('''# 暮河城 · 街巷与运河（v3）

用户已取消龙，改为近东巴比伦城市街景；先做好真实三维模型，再展开视频。旧版的送火、降落、接触、点灯与灯链全部取消。原计划保存在 history/v2-before-streets。

## 已确认规格

竖屏 9:16，1080×1920；AI 审核一轮，再交付。保留56秒、24fps作为编排起点。用户认可建筑概念方向，但认为第一版实际渲染缺乏质感，故转为模型优先。

## 模型质量优先

先做蓝釉城门及相邻街区：真实独立倒角砖、深门洞、拱券厚度、立体狮形浮雕、非均匀釉面、磨损石材、深窗与梁头、屋顶陶器、织物棚布、棕榈及码头。用三个关闭景深的实际视角检查整体结构、材料近景与反向街景。概念图不能代替模型，模型参数不能代替实际渲染检查。

当前模型入口：model/build_city.py。Blender Cycles样板负责验证实际光照、阴影、反射及细节。待质量成立后再扩展完整城邦和神庙，并决定模型与最终渲染链的连接方式。

## 六段摄影

| 时间 | 内容 | 摄影任务 |
|---|---|---|
| 0–8秒 | 地平线显城 | 镜头升高解除土坡遮挡，城市固定，先见神庙再见城门与城墙 |
| 8–18秒 | 蓝釉城门 | 斜俯看清釉砖、浮雕、拱洞与城门后的街道 |
| 18–28秒 | 街巷市集 | 顺街移动，展示棚布、陶罐、木梁、院落和少量日常活动 |
| 28–38秒 | 运河码头 | 沿河移动，真实水面反射、船只、桥与岸墙形成尺度关系 |
| 38–48秒 | 阶梯神庙 | 露台、阶梯、蓝釉饰带逐层进入画面 |
| 48–56秒 | 全城收束 | 城门、河道和神庙同框，52秒起落定并保留余韵 |

## 参考样例代码

参考 Lemo《Toy Town Rush Hour》的实际 post.js、main.js、story.js，而非仅模仿概念：真实深度与屏幕清晰带结合；相机连续，背景活动独立量化；机位和看向点分轨，视线先到目标；物理焦深改为相机前向深度，避免直接使用离轴欧氏距离。最终采用范围必须在真实模型渲染后记录。旧Three预演只作为失败分析与代码来源，不能交付为新版影片。

## 音乐与现场声

90 BPM、4/4、21小节对应56秒。现代近东幻想配器，不称历史音乐复原。以气息木管四音主题、细拨弦、低弦和轻框鼓形成由稀疏到展开、最后收束的结构。城门段引入主题；市集段减鼓给环境留白；运河段扩展旋律；神庙段扩宽音区；52秒结束新乐句，留下四秒自然余韵。

删除龙翼、脚爪落地、火种接触与点火的声音。保留风、水流、船桨、远人群、棚布和足步，分轨混合。已找到本地GeneralUser GS音源与授权文件，尚未编曲或实际听音。48kHz，约−16至−14 LUFS和≤−1dBTP为初始混音目标，需实际试听核实。

## 检查与交付

模型样板与内部运镜样段由制作主角色检查；不另派审片。完整候选片完成后，才用一个独立审片角色做用户选择的一轮视听审核，最多一次修复及必要局部复核。工具无法实际听音时必须说明，不能写听音通过。
''',encoding='utf-8')
cp=json.loads((root/'CHECKPOINT.json').read_text(encoding='utf-8-sig'));cp['version']='v3';cp['project_title']=p['title'];cp['verification']['plan_structure']='v2验证为历史；v3城市街景计划待重新检查';cp['completed'] += ['保存v2历史，取消龙与送火链，重排六段城市街景','编写模型优先质量样板脚本model/build_city.py，尚未渲染'];cp['next_action']='启动Blender模型构建与三个无景深验证视角，实际查看后再决定能否扩展整城';(root/'CHECKPOINT.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf-8')
