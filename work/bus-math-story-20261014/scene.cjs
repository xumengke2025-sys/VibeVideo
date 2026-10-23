// Original deterministic SVG scene. Time is explicit; no browser or wall-clock animation.
const fs=require('fs');const path=require('path');
const C={ink:'#49392f',cream:'#f5ecd9',paper:'#fffaf0',gold:'#edba54',blue:'#4c849b',coral:'#c87057',green:'#719879'};
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));const lerp=(a,b,p)=>a+(b-a)*p;
const smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const width=s=>[...s].reduce((n,c)=>n+(/[\u3000-\uffff]/.test(c)?1:.59),0);
const txt=(x,y,s,size=38,color=C.ink,weight=700,anchor='middle',maxWidth=940)=>`<text x="${x}" y="${y}" text-anchor="${anchor}" fill="${color}" font-size="${Math.min(size,maxWidth/Math.max(1,width(s)))}" font-weight="${weight}">${esc(s)}</text>`;
const card=(x,y,w,h,fill=C.paper,r=30)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="#ddceb2" stroke-width="3"/>`;
const tag=(x,y,s,color=C.ink,w=260)=>`${card(x-w/2,y-44,w,64)}${txt(x,y,s,32,color,700,'middle',w-28)}`;
function arrow(x1,y,x2,color=C.ink,lw=7){let d=Math.sign(x2-x1);return `<path d="M${x1} ${y} H${x2} M${x2-d*17} ${y-16} L${x2} ${y} L${x2-d*17} ${y+16}" fill="none" stroke="${color}" stroke-width="${lw}" stroke-linecap="round" stroke-linejoin="round"/>`;}
function ruler(x1,x2,y,label,color=C.ink){return `<g stroke="${color}" stroke-width="4"><path d="M${x1} ${y-15} V${y+15} M${x1} ${y} H${x2} M${x2} ${y-15} V${y+15}" fill="none"/></g>${tag((x1+x2)/2,y-21,label,color,Math.min(420,Math.max(190,width(label)*34+32)))}`;}
function flag(x,y){let d=x>850?-1:1;return `<g transform="translate(${x} ${y})"><path d="M0 0 V170" stroke="${C.ink}" stroke-width="7"/><path d="M${4*d} 4 H${125*d} L${96*d} 32 L${125*d} 63 H${4*d} Z" fill="#dd9062" stroke="${C.ink}" stroke-width="3"/>${txt(55*d,43,'起点',27,C.paper)}<ellipse cx="0" cy="173" rx="29" ry="7" fill="#9b8663" opacity=".3"/></g>`;}

function bus(x,y,w=824,t=0){const k=w/824;return `<g transform="translate(${x} ${y}) scale(${k})" stroke="${C.ink}" stroke-linejoin="round" stroke-width="5">
<ellipse cx="414" cy="298" rx="411" ry="21" fill="#6c6654" opacity=".19" stroke="none"/>
<path d="M11 238 L11 75 Q17 14 99 6 L727 6 Q811 13 824 62 L824 244 Z" fill="${C.gold}" stroke="#fffdf3" stroke-width="20"/>
<path d="M11 238 L11 75 Q17 14 99 6 L727 6 Q811 13 824 62 L824 244 Z" fill="${C.gold}"/>
<path d="M14 175 L823 175 L823 242 L14 242 Z" fill="#e59d40" stroke="none"/>
<path d="M89 35 Q49 40 42 87 L42 143 L155 143 L155 35 Z" fill="#bbd9d7"/>
${[183,309,435,561,687].map(q=>`<rect x="${q}" y="38" width="101" height="100" rx="14" fill="#c4dedb"/><path d="M${q+14} 58 H${q+49} L${q+14} 93" fill="#e6f1e8" stroke="none"/>`).join('')}
<path d="M104 40 V137" stroke="#739395" stroke-width="4"/>
<circle cx="43" cy="200" r="17" fill="#fff3b6"/><path d="M40 224 Q55 239 75 220" fill="none" stroke-width="4"/>
<rect x="781" y="187" width="15" height="35" rx="5" fill="#bd6146"/><path d="M2 241 H835" stroke="#f7df9b" stroke-width="17"/>
${[160,666].map(q=>`<g transform="translate(${q} 252) rotate(${-t*95})"><circle r="46" fill="#403c3c"/><circle r="25" fill="#faf0d6"/><path d="M0 -20 V20 M-20 0 H20" stroke="#a59273" stroke-width="5"/><circle r="8" fill="#82715d"/></g>`).join('')}
<rect x="307" y="157" width="284" height="64" rx="18" fill="#fff6df" stroke-width="3"/>${txt(449,202,'长长巴士',40)}
<path d="M33 13 Q371 -11 789 22" fill="none" stroke="#ffdd84" stroke-width="8"/>
</g>`;}

function kid(x,foot,color,dir,t=0,scale=.8,run=true,name='',pose='run'){
  // Face is a smooth round silhouette; no cheek balls or ball-shaped nose.
  const phase=t*7.7,leg=run?Math.sin(phase)*27:5,arm=run?Math.sin(phase+Math.PI)*18:0,bounce=run?Math.abs(Math.sin(phase))*5:0;
  const y=foot-300*scale-bounce;
  return `<g transform="translate(${x} ${y}) scale(${scale})"><ellipse cx="0" cy="300" rx="88" ry="12" fill="#9b896b" opacity=".17"/>
  <g transform="scale(${dir} 1)" stroke="${C.ink}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
  <g stroke="#fffdf5" stroke-width="17"><path d="M-30 192 L${-45-leg} 245 L${-67-leg} 289 M28 192 L${45+leg} 248 L${68+leg} 288" fill="none"/>${pose==='highfive'?'':`<path d="M-35 132 L-65 ${164+arm} L-88 ${138+arm} M35 132 L63 ${162-arm} L88 ${131-arm}" fill="none"/>`}</g>
  <path d="M-30 192 L${-45-leg} 245 L${-67-leg} 285" fill="none" stroke="#374960" stroke-width="27"/><path d="M28 192 L${45+leg} 248 L${68+leg} 284" fill="none" stroke="#374960" stroke-width="27"/>
  <path d="M${-81-leg} 278 Q${-111-leg} 279 ${-105-leg} 299 H${-57-leg} Q${-47-leg} 285 ${-65-leg} 278 Z" fill="#f9ecd7"/><path d="M${59+leg} 277 Q${54+leg} 296 ${75+leg} 300 H${108+leg} Q${111+leg} 285 ${88+leg} 277 Z" fill="#f9ecd7"/>
  ${pose==='highfive'?'':`<path d="M-35 132 L-65 ${164+arm} L-88 ${138+arm}" fill="none" stroke="${color}" stroke-width="24"/><path d="M35 132 L63 ${162-arm} L88 ${131-arm}" fill="none" stroke="${color}" stroke-width="24"/><circle cx="-90" cy="${134+arm}" r="13" fill="#f3c7a4"/><circle cx="90" cy="${127-arm}" r="13" fill="#f3c7a4"/>`}
  <path d="M-39 117 Q0 104 39 117 L44 205 Q0 219 -44 205 Z" fill="${color}" stroke="#fffdf5" stroke-width="16"/>
  <path d="M-39 117 Q0 104 39 117 L44 205 Q0 219 -44 205 Z" fill="${color}"/>
  <path d="M-14 103 V122 Q0 132 14 122 V103" fill="#f3c7a4"/>
  <path d="M-64 27 Q-68 -20 -24 -36 Q11 -54 52 -19 Q71 2 65 41 L64 66 Q61 111 0 118 Q-60 110 -65 65 Z" fill="#f6cdaa" stroke="#fffdf5" stroke-width="17"/>
  <path d="M-64 27 Q-68 -20 -24 -36 Q11 -54 52 -19 Q71 2 65 41 L64 66 Q61 111 0 118 Q-60 110 -65 65 Z" fill="#f6cdaa"/>
  <path d="M-65 46 Q-78 4 -58 -22 L-41 -30 L-44 -42 L-16 -37 Q8 -60 21 -38 Q51 -39 65 -17 Q83 4 63 49 L48 27 Q34 9 16 13 Q-3 30 -19 14 Q-38 27 -47 52 Z" fill="#604833"/>
  <path d="M-35 45 Q-29 40 -22 43 M18 42 Q25 37 32 42" fill="none" stroke-width="3"/>
  <ellipse cx="-27" cy="60" rx="7" ry="9" fill="${C.ink}" stroke="none"/><ellipse cx="25" cy="60" rx="7" ry="9" fill="${C.ink}" stroke="none"/>
  <circle cx="-29" cy="57" r="2" fill="#fffaf0" stroke="none"/><circle cx="23" cy="57" r="2" fill="#fffaf0" stroke="none"/>
  <ellipse cx="-42" cy="79" rx="11" ry="6" fill="#e9a08b" stroke="none" opacity=".72"/><ellipse cx="41" cy="79" rx="11" ry="6" fill="#e9a08b" stroke="none" opacity=".72"/>
  <path d="M0 72 l-2 4 4 1" fill="none" stroke="#b48262" stroke-width="2.5"/>
  <path d="M-14 86 Q0 91 16 86 Q13 104 1 104 Q-11 104 -14 86 Z" fill="#a6624e" stroke-width="3"/>
  <path d="M-9 88 Q0 91 11 88" stroke="#fffaf0" stroke-width="4"/>
  </g>${name?`${card(-58,145,116,51)}${txt(0,184,name,32,color)}`:''}
  ${pose==='highfive'?`<g stroke="${C.ink}" stroke-width="4"><path d="M${-dir*35} 137 L${-dir*65} 175 L${-dir*72} 200" stroke="${color}" stroke-width="23" fill="none"/><circle cx="${-dir*72}" cy="205" r="13" fill="#f3c7a4"/><path d="M${dir*39} 130 L${dir*73} 81 L${dir*90} 55" stroke="${color}" stroke-width="23" fill="none"/><ellipse cx="${dir*93}" cy="49" rx="13" ry="20" fill="#f3c7a4"/></g>`:''}
  </g>`;
}

function background(cam=0){const offset=((cam*3)%250+250)%250;return `<g clip-path="url(#world)">
<rect x="48" y="326" width="984" height="958" rx="54" fill="#dbe8df"/>
<circle cx="877" cy="464" r="54" fill="#ecc974"/><circle cx="864" cy="453" r="48" fill="#f4dca0"/>
<g fill="#f5f1e4"><ellipse cx="206" cy="467" rx="73" ry="17"/><ellipse cx="242" cy="452" rx="40" ry="23"/><ellipse cx="697" cy="550" rx="70" ry="19"/></g>
<path d="M-90 808 Q160 497 455 756 Q744 470 1160 795 V981 H-90 Z" fill="#abc7ac"/>
<path d="M-70 900 Q220 650 531 817 Q865 676 1180 918 V981 H-70 Z" fill="#93b592"/>
${[-1,0,1,2,3,4].map(i=>`<g transform="translate(${i*300+offset-80} 760)"><path d="M0 139 V12" stroke="#647b55" stroke-width="9"/><path d="M-45 109 Q-81 47 -34 21 Q6 -18 30 20 Q88 31 60 89 Q39 131 -45 109 Z" fill="#779d78" stroke="#f5f2e6" stroke-width="8"/></g>`).join('')}
<rect x="48" y="944" width="984" height="133" fill="#8f9990"/><path d="M48 957 H1032" stroke="#eae4d1" stroke-width="6"/>
<path d="M${-200+offset} 1017 H1300" stroke="#eee6cf" stroke-width="8" stroke-dasharray="60 70"/>
<rect x="48" y="1077" width="984" height="207" fill="#e8dcbc"/><path d="M48 1083 H1032" stroke="#fcf2d7" stroke-width="15"/>
<path d="M48 1212 H1032 ${[-1,0,1,2,3,4].map(i=>`M${i*270+offset} 1083 V1212`).join(' ')}" stroke="#d2c6a8" stroke-width="3"/>
</g>`;}

function bubble(x,y,s,w=400){return `<path d="M${x-w/2} ${y} q0 -22 24 -22 h${w-48} q24 0 24 22 v42 q0 22 -24 22 h${-w/2+20} l-30 23 7 -23 h${-w/2+33} q-24 0 -24 -22 Z" fill="${C.paper}" stroke="${C.ink}" stroke-width="3"/>${txt(x,y+29,s,32,C.ink,700,'middle',w-40)}`;}

const titles={intro:'长长巴士的相遇谜案',mystery:'同一辆车，两个感觉',units:'先找到巴士的速度',passA:'同向跑：一点点超过',solveA:'小甲每秒跑多远？',passB:'迎面跑：两边一起靠近',solveB:'小乙每秒跑多远？',flag:'从车尾出发，插一面旗',mapbus:'车尾走了160米',mapA:'小甲走了80米',gap:'两人还相隔多远？',close:'空隙，每秒少多少？',answer:'再过多久，他们碰面？',ending:'击掌！谜案破解啦'};
const kickers={intro:'巴士生日会 · 路上的一道谜题',mystery:'先看故事，再找秘密',units:'车身长15米 · 车速18千米/小时',passA:'西 ←  巴士与小甲同向跑',solveA:'同向：看每秒多赶上多少',passB:'巴士向西 ←   → 小乙向东',solveB:'迎面：看每秒一起靠近多少',flag:'重要：车头遇到，车尾离开',mapbus:'共同起点 · 共同经过32秒',mapA:'共同起点 · 共同经过32秒',gap:'此刻：车尾刚离开小乙',close:'小甲与小乙，迎面跑',answer:'从车尾离开小乙开始计时',ending:'同向看差 · 迎面看和'};

function lesson(title,formula,detail='',color=C.ink){return `${card(66,1322,948,333)}${txt(540,1391,title,34,color)}${txt(540,1498,formula,67,color,800,'middle',860)}${txt(540,1590,detail,31,C.ink,500,'middle',856)}`;}
function caption(s){const max=24,lines=[];let chars=[...s];while(chars.length){lines.push(chars.splice(0,max).join(''));}return `${card(66,1700,948,162)}${lines.slice(0,3).map((line,i)=>txt(540,lines.length>2?1745+i*42:1766+i*52,line,36,C.ink,500,'middle',870)).join('')}`;}

function contactScene(type,local,freeze=false){
 const duration=type==='A'?6:2, u=freeze?duration:clamp(local-1,0,duration), speed=type==='A'?2.5:-2.5;
 const cam=((5*u-7.5)+speed*u)/2,sc=34;
 const X=x=>540-(x-cam)*sc,front=X(5*u),rear=X(5*u-15),runner=X(speed*u);
 return background(cam)+`<path d="M${runner} 799 V1225" stroke="${type==='A'?C.blue:C.coral}" stroke-width="3" stroke-dasharray="10 10" opacity=".58"/>`+
 bus(front,818,15*sc,u)+kid(runner,1232,type==='A'?C.blue:C.coral,type==='A'?-1:1,u,.84,true,type==='A'?'小甲':'小乙')+
 ruler(front,rear,717,'整段车身：15米','#a58245')+tag(540,410,`经过 ${u.toFixed(u===Math.floor(u)?0:1)} 秒`,C.ink,340)+
 tag(front,790,'车头',C.ink,130)+tag(rear,790,'车尾',C.ink,130)+
 (u===0?tag(540,535,'车头与人齐平',C.ink,380):u===duration?tag(540,535,'车尾与人齐平',C.ink,380):'')+
 arrow(runner+(type==='A'?75:-75),1280,runner+(type==='A'?-75:75),type==='A'?C.blue:C.coral);
}

function mapScene(mode,elapsed=32){
 const t=elapsed,cam=(5*t+15)/2,sc=Math.min(34,880/(5*t+28)),X=x=>540-(x-cam)*sc;
 const rear=X(5*t),front=X(5*t+15),A=X(2.5*t),B=X(240-2.5*t),origin=X(0);
 let s=background(cam)+bus(front,982-15*sc*300/824,15*sc,t)+flag(origin,930);
 if(B>90&&B<990)s+=kid(B,1217,C.coral,1,t,.68,t>0,'小乙');
 s+=kid(A,1229,C.blue,-1,t,.68,t>0,'小甲');
 s+=tag(540,408,`从起点经过 ${t.toFixed(t===Math.floor(t)?0:1)} 秒`,C.ink,570);
 if(t>=29.95&&t<31.8)s+=tag(540,546,'车头遇到小乙',C.ink,450);
 if(t>=32)s+=tag(540,546,'车尾刚好与小乙齐平',C.ink,590);
 if(mode==='flag')s+=`<path d="M${rear} 795 V1150" stroke="${C.coral}" stroke-width="4" stroke-dasharray="10 9"/>`+tag(rear,775,'盯住车尾',C.coral,210);
 if(mode==='mapbus')s+=ruler(rear,origin,705,'车尾：160米','#b78632');
 if(mode==='mapA')s+=ruler(A,origin,695,'小甲：80米',C.blue);
 if(mode==='gap')s+=ruler(B,A,703,'空隙：80米',C.coral);
 if(t===32){s+=`${txt(origin,1270,'0米',28)}${txt(A,1270,'80米',28,C.blue)}${txt(B,1270,'160米',28,C.coral)}`;}
 return s;
}

function compareScene(type,t){const p=clamp((t-1)/3),x=665,unit=60;
 let s=background(p*5)+bus(x-5*unit*p,850,360,t);
 s+=ruler(x-5*unit,x,704,'巴士：每秒5米','#a58245');
 if(type==='A')s+=kid(x-2.5*unit*p,1230,C.blue,-1,p,.8,true,'小甲')+ruler(x-2.5*unit,x,572,'小甲：每秒2.5米',C.blue);
 else s+=kid(210+2.5*unit*p,1230,C.coral,1,p,.8,true,'小乙')+ruler(210,210+2.5*unit,572,'小乙：每秒2.5米',C.coral);
 s+=tag(540,426,'放大比较：1秒钟的路程',C.ink,610);return s;
}

function meetScene(u,t,ending=false){let A=80+2.5*u,B=160-2.5*u;const X=x=>540-(x-120)*9;
 let s=background(120)+`<path d="M48 660 Q540 480 1032 660" stroke="#927657" stroke-width="5" fill="none"/>`;
 if(ending){s+=Array.from({length:13},(_,i)=>`<path d="M${75+i*74} ${626-Math.sin(i/12*Math.PI)*113} l40 7 -20 37 Z" fill="${[C.gold,C.blue,C.coral][i%3]}"/>`).join('');s+=tag(540,440,'生日快乐，长长巴士！',C.ink,670)+bus(89,890,417,t);}
 const xA=X(A)+85*clamp(u/16),xB=X(B)-85*clamp(u/16);
 s+=kid(xA,1223,C.blue,-1,t,.95,u<16,'小甲',u>=16?'highfive':'run')+kid(xB,1223,C.coral,1,t,.95,u<16,'小乙',u>=16?'highfive':'run');
 if(!ending){s+=tag(540,424,`再经过 ${u.toFixed(u===Math.floor(u)?0:1)} 秒`,C.ink,460);if(u<16)s+=ruler(X(B),X(A),680,`还剩 ${Math.max(0,80-5*u).toFixed(u===Math.floor(u)?0:1)} 米`,C.coral);else s+=tag(540,621,'碰面啦！',C.coral,360);}
 if(u>=16){let a=(Math.sin(t*2)+1)*.25+.45;s+=`<g opacity="${a}" stroke="#c78d34" stroke-width="5"><path d="M540 958 V930 M520 966 L500 946 M560 966 L581 946"/></g>`;}
 return s;
}

function renderShort(t,plan){
 const stage=plan.stages.find(s=>t>=s.start&&t<s.end)||plan.stages.at(-1),id=stage.id,l=t-stage.start;
 let scene='',panel='';
 if(id==='intro'){
  scene=background(t)+bus(128,678,824,t)+kid(790,1232,C.blue,-1,t,.9,true,'小甲')+kid(281,1232,C.coral,1,t+.4,.9,true,'小乙')+ruler(140,952,588,'车身长15米','#a58245');
  panel=lesson('巴士生日会 · 先算碰面时间','离开小乙后，多久相遇？','车速18千米/小时；甲向西，乙向东');
 }else if(id==='mystery'){
  const A=l<1.6,u=A?6*clamp(l/1.3):2*clamp((l-2)/1.2);
  scene=contactScene(A?'A':'B',1+u);
  if(l>=1.6&&l<2)scene+=tag(540,610,'再过30秒，车头遇乙',C.ink,640);
  panel=lesson('同一辆巴士，速度一直没变',A?'同向通过：6秒':'迎面通过：2秒','完整车身15米；从车头齐平到车尾齐平',A?C.blue:C.coral);
 }else if(id==='units'){
  scene=background(l)+bus(118,772,844,t)+ruler(133,960,647,'15米车身','#a58245');
  panel=lesson('先把巴士速度换成米/秒','18000 ÷ 3600 = 5','18千米＝18000米；1小时＝3600秒');
 }else if(id==='solveA'){
  scene=contactScene('A',1+6*clamp(l/2.2));
  panel=lesson('同向：巴士速度 − 速度差','5 − 15 ÷ 6 = 2.5','15÷6是每秒多赶上的米数；甲速2.5米/秒',C.blue);
 }else if(id==='solveB'){
  scene=contactScene('B',1+2*clamp(l/2.2));
  panel=lesson('迎面：速度和 − 巴士速度','15 ÷ 2 − 5 = 2.5','15÷2是每秒一起靠近的米数；乙速2.5米/秒',C.coral);
 }else if(id==='flag'){
  const elapsed=l<2?30*clamp(l/2):30+2*clamp((l-2)/.7);
  scene=mapScene('flag',elapsed);
  panel=lesson('车尾与甲同起点，到车尾离开乙','30 + 2 = 32秒','先30秒车头遇乙，再2秒车尾离乙');
 }else if(id==='mapbus'){
  scene=mapScene('mapbus');panel=lesson('32秒，车尾从旗子走了','5 × 32 = 160米','车尾与乙齐平，所以乙在160米处','#a58245');
 }else if(id==='mapA'){
  scene=mapScene('mapA');panel=lesson('32秒，小甲从旗子走了','2.5 × 32 = 80米','同一个起点，同样32秒',C.blue);
 }else if(id==='gap'){
  scene=mapScene('gap');panel=lesson('甲在80米处，乙在160米处','160 − 80 = 80米','这就是两人还剩的距离',C.coral);
 }else if(id==='close'){
  scene=meetScene(clamp(l/1.4),t);panel=lesson('两边一起跑，空隙每秒减少','2.5 + 2.5 = 5','两人的相遇速度：5米/秒',C.coral);
 }else if(id==='answer'){
  scene=meetScene(16*clamp(l/2),t);panel=lesson('剩下距离 ÷ 相遇速度','80 ÷ 5 = 16秒','从车尾离开小乙开始计时',C.coral);
 }else{
  scene=meetScene(16,t,true);panel=lesson('谜案破解！一起去生日会','再过16秒相遇！','同向看差，迎面看和',C.coral);
 }
 const row=plan.captions.find(r=>t>=r.start&&t<r.end)||plan.captions.at(-1);
 return frameSVG(t,plan,id,scene,panel,row.text,'30秒精简版 · 动作加速示意');
}

function frameSVG(t,plan,id,scene,panel,line,subheading){
 const fade=clamp(t/.25)*clamp((plan.duration-t)/.35);
 return `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920"><defs><clipPath id="world"><rect x="48" y="326" width="984" height="958" rx="54"/></clipPath><pattern id="papergrain" width="86" height="83" patternUnits="userSpaceOnUse"><circle cx="9" cy="13" r=".7" fill="#886c4b" opacity=".10"/><path d="M27 41 l7 -1 M68 64 l9 1" stroke="#8e7150" stroke-width=".8" opacity=".09"/></pattern></defs><rect width="1080" height="1920" fill="${C.cream}"/><g opacity="${fade}" font-family="Microsoft YaHei, SimHei, sans-serif">${txt(540,90,kickers[id],28,'#8a725d',500)}${txt(540,185,titles[id],65,C.ink,800,'middle',955)}${txt(540,258,subheading,32,'#9a785b',500)}${scene}${panel}${caption(line)}<path d="M66 1890 H${66+948*clamp(t/plan.duration)}" stroke="${C.coral}" stroke-width="5" stroke-linecap="round"/></g><rect width="1080" height="1920" fill="url(#papergrain)"/></svg>`;
}

function renderAt(t,plan){
 if(plan.short)return renderShort(t,plan);
 const stage=plan.stages.find(s=>t>=s.start&&t<s.end)||plan.stages.at(-1),id=stage.id,l=t-stage.start;
  const rows=plan.captions||plan.narration;
  const row=rows.find(r=>t>=r.start&&t<r.end)||rows.at(-1);
  const group=rows.filter(r=>r.stage===id),i=Math.max(0,group.indexOf(row));
 let scene='',panel='';
 if(id==='intro'){
  scene=background(t)+bus(128-28*Math.sin(clamp(l/8)*Math.PI),678,824,t)+kid(790,1232,C.blue,-1,t,.9,true,'小甲')+kid(281,1232,C.coral,1,t+.4,.9,true,'小乙')+ruler(140,952,588,'车身长15米','#a58245');
  panel=lesson('今天的任务','帮两位伙伴找到碰面时间','让长长巴士，变成一把会动的尺子');
 }else if(id==='mystery'){
  const A=i<2,q=t-row.start;
  scene=contactScene(A?'A':'B',i===0?q:i===2?0:i===3?q:9,i===1||i===4);
  if(i===1||i===3)scene+=bubble(540,610,A?'咦，怎么还没过去？':'哇，一下就过去啦！',540);
  if(i===2)scene+=tag(540,610,'离开甲后，再过30秒',C.ink,610);
  if(i===4)scene+=bubble(540,610,'我没变速！快来当相遇侦探！',670);
  panel=lesson('同一辆巴士，速度一直没变',i<2?'同向通过：6秒':i===2?'再过30秒，车头遇乙':i===3?'迎面通过：2秒':'离开乙后，还要多久碰面？','先猜一猜，再用车身量一量',A?C.blue:C.coral);
 }else if(id==='units'){
  scene=background(l)+bus(118,772,844,t)+ruler(133,960,647,'15米车身','#a58245');
  panel=i===0?lesson('题目给出的车速','18千米/小时','先把单位换成“米/秒”'):i===1?lesson('换成米和秒','18000米 ÷ 3600秒','18千米＝18000米；1小时＝3600秒'):lesson('巴士每秒的路程','18000 ÷ 3600 = 5','巴士速度：5米/秒','#a58245');
 }else if(id==='passA'){
  scene=contactScene('A',l);panel=lesson('同向：巴士一点点超过小甲','6秒，多超过15米','从车头齐平，到车尾齐平',C.blue);
 }else if(id==='solveA'){
  scene=compareScene('A',l);panel=i===0?lesson('先求每秒多赶上的路程','15 ÷ 6 = 2.5','巴士每秒比小甲多走2.5米',C.blue):lesson('再求小甲的速度','5 − 2.5 = 2.5','小甲速度：2.5米/秒',C.blue);
 }else if(id==='passB'){
  scene=contactScene('B',l);panel=i===0?lesson('迎面：两边一起靠近','2秒，一起通过15米','巴士和小乙的路程加在一起',C.coral):lesson('两边每秒一起靠近','15 ÷ 2 = 7.5','这7.5米，包含巴士和小乙两份',C.coral);
 }else if(id==='solveB'){
  scene=compareScene('B',l);panel=i===0?lesson('去掉巴士贡献的5米','7.5 − 5 = 2.5','小乙速度：2.5米/秒',C.coral):lesson('两人的速度分别算出来了','小甲 = 小乙 = 2.5米/秒','不是提前假设，是题目告诉了我们',C.coral);
 }else if(id==='flag'){
  let elapsed=0;if(i===2){const q=t-group[i].start;elapsed=q<4?30*clamp(q/4):q<4.7?30:30+clamp(q-4.7,0,2);}scene=mapScene('flag',elapsed);
  panel=i===0?lesson('追踪同一个部位','只盯住：车尾','避免把车头和车尾当成同一个点'):i===1?lesson('此刻车尾与小甲齐平','插下起点旗','车尾和小甲，从同一位置开始算'):lesson('从离开甲，到离开乙','30 + 2 = 32秒','长等待加速回看；关键接触停留');
 }else if(id==='mapbus'){
  scene=mapScene('mapbus');panel=lesson('车尾从起点走的路程','5 × 32 = 160米','车尾与小乙齐平：小乙就在160米处','#a58245');
 }else if(id==='mapA'){
  scene=mapScene('mapA');panel=lesson('小甲从起点走的路程','2.5 × 32 = 80米','同一个起点，同样经过32秒',C.blue);
 }else if(id==='gap'){
  scene=mapScene('gap');panel=lesson('从两人的位置，找到中间空隙','160 − 80 = 80米','此刻车尾刚离开小乙，空隙还剩80米',C.coral);
 }else if(id==='close'){
  const u=clamp(l/4,0,1);scene=meetScene(u,t)+tag(540,538,'慢放看清：1秒内的变化',C.ink,590);
  panel=lesson('两边一起跑，中间一起变短','2.5 + 2.5 = 5','甲走2.5米，乙走2.5米：空隙少5米',C.coral);
 }else if(id==='answer'){
  const u=16*clamp(l/7);scene=meetScene(u,t);panel=lesson('80米空隙，每秒少5米','80 ÷ 5 = 16秒','车尾离开乙之后，再过16秒相遇',C.coral);
 }else{
  scene=meetScene(16,t,true);panel=i<2?lesson('答案：车尾离开乙后','再过16秒相遇！','两位伙伴碰面，一起去生日会',C.coral):lesson('你也成为相遇小侦探啦','同向看差，迎面看和','再用剩下的距离，除以靠近的速度',C.blue);
 }
 const fade=clamp(t/.5)*clamp((plan.duration-t)/.55);
 return `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920"><defs><clipPath id="world"><rect x="48" y="326" width="984" height="958" rx="54"/></clipPath><pattern id="papergrain" width="86" height="83" patternUnits="userSpaceOnUse"><circle cx="9" cy="13" r=".7" fill="#886c4b" opacity=".10"/><path d="M27 41 l7 -1 M68 64 l9 1" stroke="#8e7150" stroke-width=".8" opacity=".09"/></pattern></defs><rect width="1080" height="1920" fill="${C.cream}"/><g opacity="${fade}" font-family="Microsoft YaHei, SimHei, sans-serif">${txt(540,90,kickers[id],28,'#8a725d',500)}${txt(540,185,titles[id],65,C.ink,800,'middle',955)}${txt(540,258,id==='intro'?'一个有故事的解题小冒险':id==='answer'?'时间加速示意 · 起算时刻要看清':'先看动作 → 再读算式',32,'#9a785b',500)}${scene}${panel}${caption(row.text)}<path d="M66 1890 H${66+948*clamp(t/plan.duration)}" stroke="${C.coral}" stroke-width="5" stroke-linecap="round"/></g><rect width="1080" height="1920" fill="url(#papergrain)"/></svg>`;
}
module.exports={renderAt,kid,bus,math:{clamp,lerp,smooth},titles};
