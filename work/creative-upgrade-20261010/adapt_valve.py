from pathlib import Path
p=Path('work/creative-upgrade-20261010/valve/film.js');s=p.read_text(encoding='utf-8')
def replace(a,b):
    global s
    assert a in s,a[:100]
    s=s.replace(a,b)
replace("const W=1080,H=1920,c=document.querySelector('#film'),g=c.getContext('2d');", "const W=1080,H=1920,c=document.querySelector('#film'),g=c.getContext('2d');\nconst scale=window.__previewScale||1;c.width=Math.round(W*scale);c.height=Math.round(H*scale);")
s="import {valveState} from './mechanical.mjs';\n"+s
a=s.index('function stateAt(t)');b=s.index('function renderAt(',a)
s=s[:a]+'''const fade=(t,a,b)=>ease(clamp((t-a)/(b-a)));
function stateAt(t){
 const pressure=2.65*fade(t,.15,.55)*(1-fade(t,1.15,1.55))+2.9*fade(t,5,6.7)*(1-fade(t,8.7,10.1))-1.5*fade(t,11,11.5);
 const v=valveState({pressure,area:1,preload:1,stiffness:.014,stroke:128,restLength:403,seat:824});
 return {...v,pressure,draw:1,section:fade(t,2.5,3.8),ex:0,opened:v.displacement/128,settle:fade(t,12.4,14),zoom:1+.62*fade(t,3.8,5)-.62*fade(t,12.2,14)};
}
''' +s[b:]
replace("g.setTransform(1,0,0,1,0,0);", "g.setTransform(scale,0,0,scale,0,0);")
replace("text('只向一个方向',88,275,76);text('弹簧止回阀',94,340,38,faint);", "text(t<12.5?'一条路，两种结果':'只向一个方向',88,275,68);text(t<2.5?'先看流动，再看里面':'弹簧止回阀',94,340,36,faint);")
replace("const zoom=1+.035*s.section-.035*s.settle;g.save();g.translate(480,990);g.scale(zoom,zoom);g.translate(-480,-990);", "const zoom=s.zoom;g.save();g.translate(480,1000);g.scale(zoom,zoom);g.translate(-480,-1000);")
replace("disc=824+94*s.opened", "disc=s.disc")
replace("line([[480,disc+18],[480,1245]],{width:3});block(440,1245,80,22);", "block(440,1245,80,22);")
replace("if(s.opened>.01)", "if(s.displacement>20)")
replace("[480+lane*30,835],[480+lane*95,disc-8]", "[480+lane*30,824+s.displacement*.45],[480+lane*95,824+s.displacement*.5]")
replace("(xx-x)/mag*22,(yy-y)/mag*22,cyan,2.8", "(xx-x)/mag*12,(yy-y)/mag*12,cyan,2.8")
replace("}else if(s.section>.9&&t<6.3){arrow(480,670,0,80,faint,3);}", "}")
replace("if(s.section>.88){leader('阀座',750,755,590,812);leader('阀瓣',750,990,545,disc+8);leader('弹簧',750,1165,510,1150);}", '''if(s.section>.88&&zoom<1.25){leader('阀座',750,755,590,812);leader('阀瓣',750,990,545,disc+8);leader('弹簧',750,1165,510,1150);}
 if(t>4.4&&t<10.5){
  const down=Math.max(0,s.pressure)/2.9,up=s.springForce/2.9;
  arrow(480,disc-115,0,80*down,cyan,6);arrow(575,disc+145,0,-80*up,'#e6b77a',6);
  text('压差',375,disc-100,24,cyan);text('弹簧力',590,disc+130,24,'#e6b77a');
 }
 if(t>=10.5){
  const reverse=fade(t,10.5,11.5),stop=disc+48;
  for(let j=0;j<5;j++){const y=1325-j*80-110*reverse;if(y>stop+28)arrow(480,y,0,-24,'#e19e87',4);}
  line([[418,disc+18],[542,disc+18]],{color:'#e19e87',width:5,alpha:reverse});
 }''')
replace("g.restore();\n text('IN'", """g.restore();
 if(t<2.5){
  if(t<1.6){for(let j=0;j<4;j++)arrow(225,680+((t*250+j*145)%570),0,45,cyan,5);text('通过',200,1395,28,cyan);}
  else{const travel=fade(t,1.6,2.15);arrow(785,1300-travel*320,0,-65,'#e19e87',5);line([[755,850],[815,850]],{color:'#e19e87',width:5});text('停住',750,1395,28,'#e19e87');}
 }
 text('IN'""")
replace("const cap=captionAt(plan,t);", "const cap=captionAt(plan,t);")
replace("text('正向压差开启 · 弹簧复位关闭',94,1722,26,faint);", "text(t<12.4?'载荷控制行程 · 固定端保持原位':'正向压差开启 · 卸载与逆压关闭',94,1722,26,faint);")
replace("window.__film={...plan,width:W,height:H,cuts:plan.connections.map(v=>v.time)}", "window.__film={...plan,width:Math.round(W*scale),height:Math.round(H*scale),cuts:[]}")
p.write_text(s,encoding='utf-8')
print('Adapted existing valve drawing and retained original helpers')
