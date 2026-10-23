import {W,H,g,ov,inkC,fxC,ovC,setCam,clear,cam,line,text,rect,circ,ell,solid,hatch,balloon,NIBS,S} from './vendor/draw.js';
import {makePaper} from './vendor/paper.js';
const canvas=document.querySelector('#c');canvas.width=W;canvas.height=H;const compose=makePaper(canvas,W,H);
const Q=new URLSearchParams(location.search);if(Q.has('render'))document.body.classList.add('render');
await document.fonts.load('400 44px "Microsoft YaHei"');
const FONT='"Microsoft YaHei", sans-serif',MONO='Consolas, monospace';
const clamp=x=>Math.max(0,Math.min(1,x));const ease=x=>{x=clamp(x);return x*x*x*(x*(x*6-15)+10)};const p=(t,a,b)=>clamp((t-a)/(b-a));
let T=0,ox=0,oy=0;const at=(x,y,fn)=>{const a=ox,b=oy;ox=x;oy=y;fn();ox=a;oy=b};
const pts=q=>q.map(([x,y])=>[x+ox,y+oy]);
const L=(q,u=1,w=2,v=1,dash)=>line(pts(q),{u,w,v,dash,nib:false});
const R=(x,y,w,h,u=1,v=1,lw=2)=>L([[x,y],[x+w,y],[x+w,y+h],[x,y+h],[x,y]],u,lw,v);
const C=(x,y,r,u=1,v=1,w=2)=>L(circ(x,y,r,60),u,w,v);
function TX(str,x,y,size=34,u=1,o={}){text(str,ox+x,oy+y,{size,u,font:FONT,nib:false,...o})}
function mono(str,x,y,size=20,u=1,o={}){TX(str,x,y,size,u,{font:MONO,...o})}
function fill(q){solid(pts(q),{u:1,w:2});}
function cross(x,y,s=14,v=.35){L([[x-s,y],[x+s,y]],1,1,v);L([[x,y-s],[x,y+s]],1,1,v)}
function label(str,x,y,w,u=1,size=30){if(u<=0)return;solid(pts(rect(x,y,x+w,y+58)),{u,w:1.5});TX(str,x+w/2,y+40,size,p(u,0.25,1),{align:'center'})}
function sect(n,title,english,t0){const u=p(T,t0,t0+.7);mono('FIG. '+n,-610,-355,22,u,{ls:2,v:.65});TX(title,-455,-350,42,u);L([[-610,-320],[610,-320]],u,1.5,.7);mono(english,610,-353,17,u,{align:'right',v:.6})}
function linesOfText(x,y,w,n,u=1){for(let i=0;i<n;i++)L([[x,y+i*16],[x+w*(i===n-1?.63:1),y+i*16]],clamp(u*n-i),1,.45)}
function icon(kind,x,y,s,u=1){at(ox+x,oy+y,()=>{const k=s/70;const path=q=>L(q.map(([a,b])=>[a*k,b*k]),u,2.4);if(kind==='building'){path([[-28,28],[28,28],[28,-14],[0,-35],[-28,-14],[-28,28]]);path([[-16,28],[-16,-9],[16,-9],[16,28]]);for(let i=0;i<3;i++)path([[-20,-3+i*10],[20,-3+i*10]])}else if(kind==='chart'){path([[-30,-30],[-30,30],[32,30]]);path([[-22,17],[-8,1],[5,8],[25,-19]]);path([[10,-19],[25,-19],[25,-4]])}else if(kind==='shield'){path([[-26,-24],[0,-34],[26,-24],[22,7],[0,31],[-22,7],[-26,-24]]);path([[-13,-3],[-2,10],[15,-13]])}else {path([[-24,-32],[11,-32],[26,-17],[26,33],[-24,33],[-24,-32]]);path([[11,-32],[11,-17],[26,-17]]);for(let i=0;i<4;i++)path([[-14,-6+i*9],[15,-6+i*9]])}})}
function route(q,start,end){L(q,p(T,start,end),2.8,.9);const u=p(T,start,end);if(u>0&&u<1){let total=0;for(let i=1;i<q.length;i++)total+=Math.hypot(q[i][0]-q[i-1][0],q[i][1]-q[i-1][1]);let a=total*u;for(let i=1;i<q.length;i++){let d=Math.hypot(q[i][0]-q[i-1][0],q[i][1]-q[i-1][1]);if(a<=d){C(q[i-1][0]+(q[i][0]-q[i-1][0])*a/d,q[i-1][1]+(q[i][1]-q[i-1][1])*a/d,5,1,1,2);break}a-=d}}}
function issue(x,y,u=1,compact=false){if(u<=0)return;const w=compact?240:420,h=compact?110:175;solid(pts([[x,y],[x+w-26,y],[x+w,y+26],[x+w,y+h],[x,y+h]]),{u,w:2.6});mono('Q-01',x+20,y+35,compact?22:25,p(u,.15,.5));TX(compact?'业务问题':'当前业务问题',x+20,y+(compact?80:87),compact?30:40,p(u,.2,.7));if(!compact)TX('上市制造企业 · 演示',x+20,y+137,27,p(u,.4,1),{v:.7})}
const centers={task:[5650,1100],opportunity:[7150,1100],experts:[7150,2300],knowledge:[5550,2300],strategy:[6370,3480]};
function task(){at(...centers.task,()=>{sect('01','商机业务，一站协同','VISIT / QUESTIONS / OPPORTUNITIES',0);
const cards=[['拜访准备','客户情况 · 沟通重点','document'],['业务答疑','有问题，随时问','shield'],['商机查询','找线索 · 看来源','chart']];
cards.forEach(([title,note,kind],i)=>{const x=-590+i*410,a=p(T,.05+i*.55,.65+i*.55);R(x,-230,370,350,a,.9,2.3);icon(kind,x+185,-135,85,a);mono('0'+(i+1),x+25,-190,23,a,{v:.6});TX(title,x+185,0,45,p(T,.4+i*.55,1+i*.55),{align:'center'});TX(note,x+185,65,26,p(T,.7+i*.55,1.3+i*.55),{align:'center',v:.8});route([[x+185,120],[x+185,205],[0,205]],2+i*.3,3+i*.3)});
label('找商机 · 解疑问 · 做方案 · 推跟进',-340,242,680,p(T,3.3,3.8),34);route([[0,205],[640,205],[720,260]],5.6,7.2);
})}
function opportunity(){at(...centers.opportunity,()=>{sect('02','主动查询商机','FIND SIGNALS / CHECK SOURCES',7.1);const u=p(T,7.2,8.3);for(let i of [0,2,1]){const x=-565+i*360,y=i===1?-245:-215,ww=330,hh=i===1?500:430,active=i===1;const a=p(T,7.3+i*.28,8.2+i*.28);if(a<=0)continue;solid(pts(rect(x,y,x+ww,y+hh)),{u:a,w:active?3:1.5,v:active?1:.55});R(x+8,y+8,ww-16,hh-16,a,active?.75:.3,1);for(let dx of [18,ww-18]){L([[x+dx,y+38],[x+dx,y+18],[x+(dx<100?38:ww-38),y+18]],a,1.3,.6)}mono('No.00'+(i+1),x+22,y+42,19,a,{v:.65});icon(['chart','building','document'][i],x+62,y+114,65,a);TX(active?'公告线索':['客户动态','','行业信号'][i],x+23,y+194,active?40:34,a,{v:active?1:.7});L([[x+20,y+219],[x+ww-20,y+219]],a,1,.5);TX('待研判',x+23,y+272,31,p(T,8.7,9.2),{v:active?1:.5});linesOfText(x+25,y+302,ww-50,3,a);if(active){label('查看来源 →',x+20,y+398,ww-40,p(T,10.1,10.5),27)}}
const a=p(T,10.3,11.3);R(-225,-269,370,548,a,1,2.8);TX('① 标题级信号',-545,304,27,p(T,11.2,11.7));TX('② 公告来源',-130,304,27,p(T,11.8,12.3));TX('③ 待核实问题',270,304,27,p(T,12.4,12.9));route([[120,5],[580,5],[580,450]],15.6,17.3);mono('来源可追溯 · 机会仍需研判',-190,354,23,p(T,13.1,13.6),{v:.65})})}
function experts(){at(...centers.experts,()=>{sect('03','多领域专家，协同答疑','EXPERT NETWORK / BUSINESS SUPPORT',17.2);
TX('数十位专家 · 多领域覆盖',0,-276,32,p(T,17.5,18.1),{align:'center',v:.8});
for(let row=0;row<4;row++){const yy=-25+row*62,rx=590-row*43,ry=205-row*14;const a=p(T,17.4+row*.22,18.1+row*.22);L(ell(0,yy,rx,ry,0,100,Math.PI,Math.PI*2),a,2,.75);L(ell(0,yy+22,rx,ry,0,100,Math.PI,Math.PI*2),a,1,.4);for(let j=0;j<14;j++){const angle=Math.PI+.12+(Math.PI-.24)*j/13,x=Math.cos(angle)*rx,y=yy+Math.sin(angle)*ry;R(x-14,y-22,28,20,a,.7,1.4);L([[x-19,y],[x+19,y]],a,1,.45)}}
const labels=['企业画像','行业研究','财务诊断','资本运作','信披合规','客户经营'];labels.forEach((v,i)=>{const x=-430+i%3*430,y=i<3?-126:-24,t=19.8+i*.55,a=p(T,t,t+.5);label(v,x-140,y,280,a,31);route([[x,y+58],[x,106],[0,106],[0,157]],t+.5,t+1.1)});
issue(-120,157,p(T,19,19.7),true);const a=p(T,25.1,25.8);L([[0,267],[0,312],[-440,312]],a,2.2);TX('单专家提问 · 多专家会商',-440,355,28,a);label('依据 [1] [2]',210,287,340,p(T,26,26.5),29);route([[210,316],[-720,316]],27.8,29.3)
})}
function knowledge(){at(...centers.knowledge,()=>{sect('04','丰富知识库，按需调用','ARCHIVES / DOCUMENTS / SOURCE CATALOG',29.1);
const kinds=['核心规范','监管规则','产品能力','案例经验','研究资料','补充资料'];kinds.forEach((v,i)=>{const x=-590+i%3*215,y=-252+Math.floor(i/3)*211,a=p(T,29.3+i*.18,30.1+i*.18);for(let k=2;k>=0;k--)R(x+k*5,y-k*6,195,176,a,k?.30:.85,k?1:2);L([[x,y+31],[x+29,y+10],[x+76,y+10],[x+93,y+31],[x+195,y+31]],a,1.5);C(x+97,y+60,8,a);C(x+97,y+105,8,a);L([[x+97,y+52],[x+103,y+100],[x+92,y+113],[x+90,y+62]],a,1.1);TX(v,x+97,y+150,29,p(T,30+i*.18,30.5+i*.18),{align:'center'});mono('V'+(i%2+1),x+145,y+58,15,a,{v:.6})});
R(-387,-258,207,190,p(T,32,32.6),1,2.7);TX('档案库 · 文档资产 · 来源目录',-590,234,28,p(T,31.4,32),{v:.85});L([[-590,263],[45,263]],p(T,32,32.5),1,.4);TX('多类资料沉淀为可检索知识',-590,311,27,p(T,32.2,32.8),{v:.7});
label('检索、引用、追溯',160,-245,420,p(T,33.4,34),33);['查找业务相关资料','定位原文与出处','保留来源和版本'].forEach((v,i)=>{const a=p(T,34+i*.55,34.4+i*.55);C(178,-118+i*95,5,a);TX(v,202,-106+i*95,30,a);L([[202,-87+i*95],[576,-87+i*95]],a,1,.4)});route([[160,156],[105,156],[105,319],[-115,319]],36,37.4);mono('KNOWLEDGE → EXPERTS → ANALYSIS',150,251,18,p(T,36.7,37.2),{v:.7});mono('SOURCE / VERSION / REF.',160,310,20,p(T,37.3,37.8),{v:.7});route([[50,323],[180,323],[180,670]],39,40.5)
})}
function strategy(){at(...centers.strategy,()=>{sect('05','商机经营，全流程支持','DISCOVER / ANALYZE / PLAN / FOLLOW UP',40.2);const a=p(T,40.2,41.1);R(-590,-240,700,530,a,.85,2.5);TX('多种业务成果，按需生成',-552,-178,37,p(T,40.8,41.4));
const names=['商机研判','企业画像','行业研究','会商纪要','拜访策略包','客户经营计划'];names.forEach((v,i)=>{const x=-554+i%2*327,y=-120+Math.floor(i/2)*119,a=p(T,41.5+i*.4,42+i*.4);for(let k=1;k>=0;k--)R(x+k*5,y+k*5,293,94,a,k?.3:.8,k?1:1.7);TX(v,x+18,y+38,v.length>5?27:30,a);linesOfText(x+18,y+59,247,2,a)});TX('成果可预览、下载，版本化留存',-550,275,23,p(T,44,44.6),{v:.7});
issue(270,-232,p(T,41.5,42.1),true);const u=p(T,47,47.6);label(T<48.2?'确认创建':'',250,-45,310,u,36);if(T>48.2){L([[281,-15],[298,1],[326,-32]],p(T,48.2,48.5),3);TX('确认创建',338,-5,28,p(T,48.3,48.6));}route([[405,13],[405,105]],48.6,49.3);const b=p(T,49.3,49.9);R(224,105,380,181,b);TX('跟进任务',252,157,38,b);TX('待跟进 · 由客户经理确认',252,213,23,p(T,49.8,50.3),{v:.75});mono('NEXT ACTION',253,260,20,b,{v:.5});route([[110,62],[180,62],[180,195],[224,195]],45.5,46.5)
})}
function sheet(){at(0,0,()=>{R(110,110,7970,4300,1,.25,1.5);R(135,135,7920,4250,1,.2,1);for(let x=400;x<8050;x+=400){L([[x,110],[x,145]],1,1,.3);mono(String(x/400),x+8,172,18,1,{v:.3})}for(let y=500;y<4200;y+=400){L([[110,y],[145,y]],1,1,.3)}for(let x=500;x<8000;x+=500)for(let y=500;y<4300;y+=500)cross(x,y,14,.10);
// A sparse construction grid ties all figures to the same drawing sheet.
for(let x=4800;x<=8000;x+=250)L([[x,650],[x,4010]],1,.5,.07,'center');for(let y=650;y<=4000;y+=250)L([[4800,y],[8000,y]],1,.5,.07,'center');
const u=p(T,52.7,55);if(u>0){TX('企业客户全生命周期',370,380,176,u);mono('FIRMBUDDY / CLIENT LIFECYCLE',375,485,56,u,{v:.7});const stages=[{x:1300,w:1600,n:'01',title:'上市前',note:'构建资本化基础'},{x:3040,w:1600,n:'02',title:'上市中',note:'专业护航'},{x:4780,w:3100,n:'03',title:'上市后',note:'持续客户经营'}];stages.forEach((s,i)=>{R(s.x,710,s.w,3245,u,.6,3);mono(s.n,s.x+70,650,133,u,{v:.6});TX(s.title,s.x+350,650,163,u);if(i<2){TX(s.note,s.x+100,1000,94,u,{v:.6});(i===0?['财务顾问','行业研究','股权激励','Pre-IPO 资管','境外 IPO 顾问','私募股权']:['IPO / 保荐承销','投价报告','战略配售基金','员工持股计划','GDR 全球存托','战略配售跟投']).forEach((v,j)=>{L([[s.x+70,1340+j*390],[s.x+s.w-70,1340+j*390]],u,2,.35);TX(v,s.x+95,1490+j*390,99,u,{v:.7});L([[s.x+100,1550+j*390],[s.x+s.w-120,1550+j*390]],u,3,.16)});}else{ // preserve the workflow, reveal its boundary rather than redrawing it
TX('商机经营 · 全流程协同',s.x+85,3890,90,u,{v:.6});}});
['投行','机构','财富','资管','国际','投资'].forEach((v,j)=>{TX(v,400,1450+j*390,125,u,{v:.8});L([[850,1410+j*390],[1170,1410+j*390]],u,2,.5)});TX('期货服务 · 贯穿全生命周期',1320,4150,100,u,{v:.65});}
if(T>55.3){const u=p(T,55.3,56.3);solid(rect(4350,4120,7930,4380),{u,w:3});TX('firmbuddy',4480,4300,205,u,{font:'Arial',weight:700});TX('从发现到行动，一站协同',5770,4275,87,p(T,56,56.7));TX('企业综合金融服务平台',5780,4345,48,p(T,56,56.7),{v:.7});}
})}
const keys=[
 [0,5650,1110,1.06],[5.6,5650,1110,1.06],[7.7,7150,1110,1.06],[15.7,7150,1110,1.06],
 [18.1,7150,2300,1.06],[27.8,7150,2300,1.06],[30.1,5550,2300,1.06],[38.8,5550,2300,1.06],
 [41.3,6370,3480,1.06],[51.9,6370,3480,1.06],[56.6,4180,2300,.205],[60,4180,2300,.205]
];
function cameraAt(t){let a=keys[0],b=keys[1];for(let i=1;i<keys.length;i++){b=keys[i];if(t<=b[0])break;a=b}const u=ease(p(t,a[0],b[0]));return{x:a[1]+(b[1]-a[1])*u,y:a[2]+(b[2]-a[2])*u,z:Math.exp(Math.log(a[3])+(Math.log(b[3])-Math.log(a[3]))*u),r:0}}
export const captions=[
[.2,3.2,'找商机、准备拜访、业务答疑'],[3.2,6.6,'FirmBuddy，一站式专业支持'],
[8.1,11.9,'发现线索、查客户、研判需求'],[12,16.1,'从查询到核实，串联商机流程'],
[18.4,22.7,'数十位专家，覆盖多类业务'],[23,27.8,'行业、财务、资本、合规，协同答疑'],
[30.6,34.3,'规则、案例、研究，多类知识汇聚'],[34.4,39,'检索原文，追溯来源与版本'],
[41.6,47.15,'研判、方案、报告、拜访，按需形成成果'],[47.2,51,'确认后创建任务，推进跟进'],
[52.3,55.8,'商机经营全流程，一站协同支持'],[56,60,'FirmBuddy，从发现到行动，一站协同']];
function subtitle(){const s=captions.find(x=>T>=x[0]&&T<x[1]);if(!s)return;const alpha=Math.min(p(T,s[0],s[0]+.2),p(s[1]-T,0,.15));const c=ov;c.save();c.setTransform(1,0,0,1,0,0);c.font=`400 32px ${FONT}`;const w=Math.max(...s.slice(2).map(x=>c.measureText(x).width))+165;const x=96,y=s.length>3?890:928,h=s.length>3?124:84;c.globalAlpha=alpha;c.fillStyle='rgba(17,41,79,.94)';c.fillRect(x,y,w,h);c.strokeStyle='#c3d8ed';c.lineWidth=1.2;c.strokeRect(x,y,w,h);c.strokeRect(x+5,y+5,w-10,h-10);c.beginPath();c.moveTo(x+101,y+12);c.lineTo(x+101,y+h-12);c.stroke();c.fillStyle='#e6eff8';c.font='17px Consolas';c.fillText('NOTE',x+28,y+30);c.font='24px Consolas';c.fillText(String(captions.indexOf(s)+1).padStart(2,'0'),x+35,y+62);c.font=`400 32px ${FONT}`;s.slice(2).forEach((v,i)=>c.fillText(v,x+123,y+(s.length>3?44:53)+i*46));c.restore()}
window.stateAt=t=>({time:t,camera:cameraAt(t*1.25),width:W,height:H,caption:captions.find(s=>t*1.25>=s[0]&&t*1.25<s[1])||null});
window.renderAt=(t,type='image/png',quality=.95)=>{T=clamp(t/48)*60;setCam(cameraAt(T));clear();NIBS.length=0;sheet();at(0,0,()=>{route([[6370,1360],[6520,1360],[6520,1100],[6585,1100]],6.4,8);route([[7730,1550],[7730,1920],[7710,1920],[7710,2160]],16,18.4);route([[6430,2605],[6250,2605],[6250,2055],[6130,2055]],28,30.4);route([[5730,2970],[5730,3080],[5780,3080],[5780,3248]],39.2,41.2)});task();opportunity();experts();knowledge();strategy();subtitle();compose(inkC,fxC,ovC,{sheet:[8200,4540],cam,seed:19});return type?canvas.toDataURL(type,quality):null};
window.__ready=true;window.renderAt(0,null);
const audio=new Audio('./audio/mix.wav');let playing=false,started=0,base=0;
const seek=document.querySelector('#seek'),display=document.querySelector('#time'),button=document.querySelector('#play');
seek.oninput=()=>{base=+seek.value;audio.currentTime=base;started=performance.now();window.renderAt(base,null);display.textContent=base.toFixed(2)+' / 48'};
button.onclick=()=>{playing=!playing;button.textContent=playing?'暂停':'播放';if(playing){base=+seek.value;if(base>=48)base=0;started=performance.now();audio.currentTime=base;audio.play().catch(()=>{});}else{base=+seek.value;audio.pause()}};
function tick(){if(playing){const t=Math.min(48,base+(performance.now()-started)/1000);window.renderAt(t,null);seek.value=t;display.textContent=t.toFixed(2)+' / 48';if(t>=48){playing=false;audio.pause();button.textContent='播放'}}requestAnimationFrame(tick)}if(!Q.has('render'))tick();
