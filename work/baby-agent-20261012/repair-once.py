from pathlib import Path
import json
root=Path(__file__).resolve().parent
p=root/'film.mjs';s=p.read_text(encoding='utf-8')
s=s.replace('arm(1,o.right||[192,-127],o.pointRight);','arm(1,o.right||[192,-127],o.pointRight,o.rightFixed);')
s=s.replace('任务：打开这本书','任务：点一下小鸭')
start=s.index('function touch(t)');end=s.index('function paperWorld(t)')
part=s[start:end]
part=part.replace('lerp(-127,82,reach)','lerp(-127,-84.4175,reach)')
part=part.replace('baby(470,1150,1.03','baby(470,1280,1.03')
part=part.replace('pointRight:true','pointRight:true,rightFixed:true')
part=part.replace('book(515,1300,790','book(515,1260,790')
part=part.replace('g.translate(470,1150)','g.translate(470,1280)')
part=part.replace('arm(1,rs,true)','arm(1,rs,true,true)')
part=part.replace('lerp(1300,600,p)','lerp(1260,600,p)')
part=part.replace('1300+Math.sin(a)','1260+Math.sin(a)')
s=s[:start]+part+s[end:]
s=s.replace('if(dw>2.2){','if(dw>2.2&&t<32.8){')
p.write_text(s,encoding='utf-8')
b=json.loads((root/'brief.json').read_text(encoding='utf-8'))
b['review']={'initial_reviews':1,'repairs':1,'reviewer':'/root/baby_av_review','status':'v1 full visual reviewed; audio/realtime unavailable; v2 local recheck pending'}
(root/'brief.json').write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf-8')
plan=json.loads((root/'plan.json').read_text(encoding='utf-8'))
plan['shots'][0]['intent']='认出专注宝宝，接到点触小鸭任务'
plan['shots'][0]['reads']='宝宝脸→档案纸片→点一下小鸭任务'
plan['shots'][0]['action']='摄影从脸部拉开，档案纸片与标记显露'
plan['shots'][1]['action']='书页展开后，固定135/118局部单位上臂/前臂长度，以肘关节折转把指尖伸向小鸭，点触后鸭跳开'
(root/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
with (root/'CHECKPOINT.md').open('a',encoding='utf-8') as f:
 f.write('\n- 唯一审片者 /root/baby_av_review 已实际查看v1全部0–1439帧接触表及原尺寸疑点图，盲看记录已写盘。正常速度与实际听音未完成。\n- 一次修复（repair=1）：V1-01 双鸭旧图在32.8秒后隐藏；V1-02 点书构图使书靠近手，右臂采用固定135/118长度和IK肘关节；V1-03 任务改“点一下小鸭”。五官、肤色、爬行和其他动作保持。\n- 即将导出out/final-v2/video.mp4，之后只请原审片者对修复处与相邻镜头局部复核，不开启第二轮全片审核。\n')
