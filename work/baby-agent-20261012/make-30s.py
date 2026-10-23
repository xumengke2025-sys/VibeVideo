from pathlib import Path
import shutil, json, re
src=Path(__file__).resolve().parent
dst=src.parent/'baby-agent-30s-20261012'
dst.mkdir(exist_ok=True)
for name in ['index.html','film.mjs','server.mjs','render.mjs','make_audio.py','package-delivery.py','brief.json','plan.json','events.json']:
    shutil.copy2(src/name,dst/name)
for folder,names in {'assets':['head-atlas.png','LICENSE-lemo.txt'],'audio':['mix.wav','audio-info.json']}.items():
    (dst/folder).mkdir(exist_ok=True)
    for name in names: shutil.copy2(src/folder/name,dst/folder/name)
f=(dst/'film.mjs').read_text(encoding='utf-8')
f=f.replace("const cv=document.querySelector('#c'),g=cv.getContext('2d',{alpha:false,willReadFrequently:true});", "const cv=document.querySelector('#c');let g=cv.getContext('2d',{alpha:false,willReadFrequently:true});const mainContext=g;")
f='\n'.join(line for line in f.splitlines() if not line.startswith(('function text(','function tag(','function stamp(')))
f=f.replace('for(let k=0;k<3;k++)line(-w*.42,-h*.27+k*38,-w*.16,-h*.27+k*38,C.shade,5);','ellipse(-w*.25,0,h*.18,h*.18,C.yellow,606);poly([[-w*.38,h*.28],[-w*.23,-h*.24],[-w*.08,h*.28]],C.red,607);')
scenes={
'opening':'''function opening(t){ground(C.ink);diag(C.red,350,490);g.save();camera(540,830,lerp(1.36,.95,ease(seg(t,.2,3))));page(540,960,885,1320,-.075);baby(550,1430,1.15,{face:t<4.2?0:1,tilt:-.03+Math.sin(t)*.016,right:[192,-127]});g.save();g.translate(540,455);g.rotate(-.075);duck(0,0,.72);g.restore();g.restore();}''',
'touch':'''function touch(t){const d=t-7.5,u=tw(d);ground(C.paper);diag(C.red,-80,160);rect(60,940,960,730,'#d8c8aa',99);ellipse(550,1270,440,180,C.white,96);const reach=ease(seg(u,1.8,3.3)),release=seg(u,3.3,5.7);const rs=[lerp(192,232,reach),lerp(-127,-84.4175,reach)];baby(470,1280,1.03,{face:d>3.25?1:0,tilt:lerp(.025,-.045,reach),right:rs,pointRight:true,rightFixed:true});const flip=seg(u,.4,1.5);book(515,1260,790,300,{flip,duck:d<3.3});g.save();g.translate(470,1280);g.scale(1.03,1.03);arm(1,rs,true,true);g.restore();if(d>=3.3){const p=eo(release),x=lerp(709,798,p),y=lerp(1260,600,p)-Math.sin(p*Math.PI)*170;duck(x,y,1,-.12*Math.sin(p*TAU));if(d<3.65){for(let k=0;k<8;k++){const a=k/8*TAU;line(709+Math.cos(a)*85,1260+Math.sin(a)*85,709+Math.cos(a)*128,1260+Math.sin(a)*128,C.red,7)}}}}''',
'paperWorld':'''function paperWorld(t){const pu=ease(seg(t,15,26.25)),u=tw(t);ground(C.red);const bx=260+1150*pu,by=1460-355*pu;g.save();camera(bx+140,by-300,1);for(let i=0;i<7;i++){const xx=80+i*340,yy=780-i*105;page(xx,yy,180+(i%3)*50,230,-.30,i%2?C.paper:'#972e21');poly([[xx-70,yy+55],[xx+10,yy-60],[xx+70,yy+55]],i%2?C.red:C.paper,710+i);line(xx-200,yy+330,xx+560,yy+95,C.ink,16)}poly([[-700,1756],[2300,830],[2300,930],[-700,1856]],C.ink,680);poly([[-700,1754],[2300,828],[2300,909],[-700,1835]],C.paper,681);crawl(bx,by,.82,{time:t,face:1,rot:-.30});const dx=bx+335+45*Math.sin(pu*9),dy=by-275-45*Math.abs(Math.sin(u*3));duck(dx,dy,.75,.12*Math.sin(u*3));for(let i=0;i<3;i++)dot(dx-60-i*20,dy+22+i*8,5,C.yellow);g.restore();}''',
'hide':'''function hide(t){const d=t-26.25,st=t>=31.4&&t<32.8,tt=st?31.4:t,dw=tw(tt)-26.25;ground(C.ink);const grow=ease(seg(d,0,.65));g.save();camera(540,960,lerp(1.08,1,grow));poly([[170,530],[435,330],[900,420],[955,1480],[290,1540]],C.paper,820);poly([[350,665],[535,505],[760,565],[795,1310],[425,1360]],C.red,821);const peek=ease(seg(dw,.55,1.75));baby(lerp(180,315,peek),1440,.88,{face:dw<3.2?0:1,tilt:dw<3.2?.08:-.08,right:[220,-200],left:[-130,-150]});poly([[480,430],[950,360],[950,1520],[600,1450]],C.ink,824);if(dw>2.2&&t<32.8){const p=ease(seg(dw,2.2,3.0));duck(730-100*p,760,.72,.1)}if(t>=32.8){const p=seg(t,32.8,33.75);duck(630+580*eo(p),760-250*Math.sin(p*Math.PI/2),.72,-.2)}g.restore();}''',
'ending':'''function ending(t){const d=t-52.5,u=tw(d);ground(C.paper);diag(C.red,-330,100);diag(C.ink,1430,80);g.save();g.translate(0,-200);baby(550,1460,1.06,{face:2,tilt:.023*Math.sin(u*2),right:[175,-110-18*Math.sin(u*6)*seg(d,2,3)],left:[-178,-150]});book(540,1490,850,270,{spiral:true});g.save();g.translate(550,1460);g.scale(1.06,1.06);arm(1,[175,-110-18*Math.sin(u*6)*seg(d,2,3)]);g.restore();duck(760,1450,.74,.05*Math.sin(u*3));g.restore();}'''
}
lines=f.splitlines()
for i,line in enumerate(lines):
    for name,new in scenes.items():
        if line.startswith('function '+name+'('): lines[i]=new
    if line.startswith('function connect('):
        line=re.sub(r"text\('[FIND]'[^;]+;",'',line)
        line=line[:line.index("if(d>7)tag")]+ '}'
        lines[i]=line
    if line.startswith('function returning('): lines[i]=line[:line.index('if(d>5.8)')]+ '}'
f='\n'.join(lines)+'\n'
old=next(x for x in f.splitlines() if x.startswith('export function render('))
new='''const sceneFns=[opening,touch,paperWorld,hide,connect,returning,ending];
const layers=[0,1].map(()=>{const c=document.createElement('canvas');c.width=cv.width;c.height=cv.height;return c});
function paintScene(ctx,index,time){g=ctx;g.setTransform(S,0,0,S,0,0);g.globalAlpha=1;g.globalCompositeOperation='source-over';sceneFns[index](time);}
// A single diagonal page edge reveals the next shot without crossfade ghosting.
export function render(outputTime){const t=clamp(outputTime,0,29.9999)*2;let scene=cuts.findIndex((a,i)=>t>=a&&t<cuts[i+1]);const half=.56;let boundary=-1;for(let i=1;i<cuts.length-1;i++)if(Math.abs(t-cuts[i])<half){boundary=i;break}
if(boundary<0)paintScene(mainContext,scene,t);else{const cut=cuts[boundary],p=ease(seg(t,cut-half,cut+half));paintScene(layers[0].getContext('2d'),boundary-1,Math.min(t,cut-.0001));paintScene(layers[1].getContext('2d'),boundary,Math.max(t,cut));g=mainContext;g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;g.drawImage(layers[0],0,0);g.setTransform(S,0,0,S,0,0);const edge=lerp(-80,W+.32*H+80,p);g.save();g.beginPath();g.moveTo(-100,-100);g.lineTo(edge+.32*100,-100);g.lineTo(edge-.32*(H+100),H+100);g.lineTo(-100,H+100);g.closePath();g.clip();g.setTransform(1,0,0,1,0,0);g.drawImage(layers[1],0,0);g.restore();g.setTransform(S,0,0,S,0,0);poly([[edge-12,-100],[edge+12,-100],[edge+12-.32*(H+100),H+100],[edge-12-.32*(H+100),H+100]],C.white,1200,false);}
g=mainContext;g.setTransform(1,0,0,1,0,0);g.save();g.globalAlpha=.28;g.globalCompositeOperation='multiply';g.drawImage(tex,0,0);g.restore();window.LAST={t:outputTime,storyTime:t,scene,width:cv.width,height:cv.height};}'''
f=f.replace(old,new).replace('current>=59.99','current>=29.99').replace('current>=60','current>=30').replace('current=59.999','current=29.999').replace(" / 60.0'"," / 30.0'")
assert not re.search(r'fillText|strokeText|function text|function tag|function stamp',f)
(dst/'film.mjs').write_text(f,encoding='utf-8')
h=(dst/'index.html').read_text(encoding='utf-8').replace('一分钟的书页冒险','30秒 · 无字书页冒险').replace('max="60"','max="30"').replace('/ 60.0','/ 30.0')
(dst/'index.html').write_text(h,encoding='utf-8')
r=(dst/'render.mjs').read_text(encoding='utf-8').replace("'1,5,8.5,10.75,12.5,17,23,28,31.5,35,40.5,45.5,49,54,58.5'","'0.5,2.5,4.25,5.375,6.25,8.5,11.5,14,15.75,17.5,20.25,22.75,24.5,27,29.25'").replace('[5,10.75,28]','[2.5,5.375,14]').replace('args.duration||60','args.duration||30')
(dst/'render.mjs').write_text(r,encoding='utf-8')
e=json.loads((dst/'events.json').read_text(encoding='utf-8'));e['duration']=30;e['bpm']=256;e['scenes']=[x/2 for x in e['scenes']];e['stop_time']=[x/2 for x in e['stop_time']]
for event in e['foley']:event['t']/=2
e['audio_processing']='Original 60-second mix; FFmpeg atempo=2, pitch preserved.'
(dst/'events.json').write_text(json.dumps(e,ensure_ascii=False,indent=2),encoding='utf-8')
b=json.loads((dst/'brief.json').read_text(encoding='utf-8'));b['duration']=30;b['story']='宝宝翻书点中小鸭，小鸭跃出；宝宝沿纸路爬行追寻，通过洞口和路线线索找到它，抱回书旁，笑脸收尾。';b['style']='1960年代间谍片头剪纸，墨黑/奶油白/朱红/暖黄，保留认可五官。全片无文字、字母、数字或印章。六次0.56秒斜向纸页擦拭。';b['audio']='原创60秒音乐与拟音经atempo=2压缩到30秒，保持音高，无旁白。';b['review']['history_version']='final-v2 (60s)';b['review']['current_version']='30s-final-v1';b['review']['current_sha256']=None;b['review']['status']='Prior one-review budget exhausted; user-requested revision with engineering checks and maker inspection; no new independent review.'
b['sources'][0]['adoption']='固定局部剪边、纸纹、绝对时间节拍、纸偶、跟随摄影。原文字场景改为纸片、路径与不规则洞口。'
(dst/'brief.json').write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf-8')
p=json.loads((dst/'plan.json').read_text(encoding='utf-8'));p['duration']=30
descriptions=[('认出宝宝','宝宝→小鸭纸片线索','摄影从脸部拉开到宝宝纸片'),('点中小鸭','手指→图案→鸭跃出','保留原接触动作'),('爬行追鸭','纸路→小鸭→爬行宝宝','沿几何纸片世界追鸭'),('洞口找鸭','不规则洞口→侧头宝宝→鸭出现','探头、短停顿、鸭跳出'),('循路线找鸭','三节点→指尖点亮→小鸭','沿纸路爬行并点亮路线'),('抱回小鸭','手接近→抱鸭→打开的书','平滑接到手部锚点并抱持'),('笑脸收尾','笑脸宝宝→书与鸭','无标题、无印章，主体上移')]
for shot,desc in zip(p['shots'],descriptions):
    shot['start']/=2;shot['end']/=2;shot['states']={k:v/2 for k,v in shot['states'].items()};shot['intent'],shot['reads'],shot['action']=desc;shot['camera']=shot['camera'].replace('O孔','洞口').replace('保留片名阅读3秒','稳定笑脸收尾');shot['sound']='原创配乐与拟音同步2倍速，保持音高'
for c in p['connections']:c['time']/=2;c['kind']='diagonal paper wipe';c['anchor']='斜向纸页边缘';c['window']=[c['time']-.28,c['time']+.28]
(dst/'plan.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
(dst/'CHECKPOINT.md').write_text('''# 宝宝30秒无字版
- delivery_mode: ai_review_once（沿用；一轮预算已在60秒版本用完）
- 用户最新要求：加快至30秒、画面完全无文字、转场顺畅。
- 保留认可head-atlas与肤色#f8c28b；移动为爬行。
- 已建立独立变体，保留原60秒源码与成片。
- 已去除文字绘制API、标题、字母、数字、标签和印章，书页模拟文字改图形。
- 时间映射outputTime*2；六处0.56秒斜向纸页擦拭，无交叉淡化。
- 下一步：音频atempo=2、代表帧/切口连续序列查看、30秒正式渲染、机械检查与源码打包。
- 不开启第二轮独立审核。正常速度观看/实际听音尚未完成。
''',encoding='utf-8')
print(dst)
