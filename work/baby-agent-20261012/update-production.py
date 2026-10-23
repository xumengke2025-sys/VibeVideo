from pathlib import Path
import json
root=Path(__file__).resolve().parent
p=root/'film.mjs'
s=p.read_text(encoding='utf-8')
s=s.replace('yy=1260-i*105','yy=780-i*105')
s=s.replace('for(let i=0;i<5;i++)dot(dx-100-i*36,dy+35+i*14,5,C.yellow)','for(let i=0;i<3;i++)dot(dx-60-i*20,dy+22+i*8,5,C.yellow)')
s=s.replace('dot(795,750,135*q,C.paper);duck(795,750,.9*q,-.08)','dot(940,530,100*q,C.paper);duck(940,530,.9*q,-.08)')
s=s.replace('dot(795,495,135,C.paper);duck(795,495,.9)','dot(940,530,100,C.paper);duck(940,530,.9)')
p.write_text(s,encoding='utf-8')
b=json.loads((root/'brief.json').read_text(encoding='utf-8'))
b['character']+=' 用户进一步明确：宝宝移动必须为爬行；四肢肤色依据认可脸部素材像素取样统一为#f8c28b。'
b['story']='宝宝翻书，点中小鸭。小鸭跃出书页，宝宝用交替手掌与膝盖撑地的爬行进入字母世界，循图形线索找到小鸭，抱回书里，最后任务完成。'
(root/'brief.json').write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf-8')
plan=json.loads((root/'plan.json').read_text(encoding='utf-8'))
shot=plan['shots'][2]
shot.update(intent='宝宝爬行追寻小鸭进入字母世界',reads='鸭离开圆框→宝宝沿纸路爬行→鸭藏入O',action='手掌和膝盖交替撑地，低位躯干前移，背景大字随伴随摄影产生相对位移',subjectPath='x=260+1150*ease(p),y=1460-355*ease(p)',cameraPath='x=baby.x+140,y=baby.y-300,z=1')
plan['shots'][4]['action']='宝宝沿纸路爬行接近线索，路线依次点亮，到达终点时小鸭在上方出现'
(root/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
with (root/'CHECKPOINT.md').open('a',encoding='utf-8') as f:
 f.write('\n- 续接完成代表帧检查：修正点书/拍书的前景手遮挡，以及连线场景的左缘裁切。\n- 用户新增约束：移动用爬行，四肢颜色与脸一致。已实现交替手掌/膝盖低位爬行rig，字母追寻与连线段使用爬行；坐姿仅翻书/抱鸭/结尾。\n- 脸部atlas实际像素取样约(250,192,137)/(249,194,138)，四肢统一#f8c28b；不改变认可五官。\n- out/stills-v5 已查看17/35/40.5秒大图：爬行姿态成立；继续调整终点鸭圆框避免覆盖宝宝脸，移开字母世界背景文字与点粒子。独立审核仍0次。\n')
