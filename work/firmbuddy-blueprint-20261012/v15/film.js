import {W,H,g,ov,inkC,fxC,ovC,setCam,clear,cam} from './vendor/draw.js';
import {makePaper} from './vendor/paper.js';
const canvas=document.querySelector('#c');canvas.width=W;canvas.height=H;
const compose=makePaper(canvas,W,H),scale=W/1920,Q=new URLSearchParams(location.search);
const plan=await(await fetch('./plan.json')).json();
if(Q.has('render'))document.body.classList.add('render');
await document.fonts.load('400 40px "Microsoft YaHei"');
const C=ov,TAU=Math.PI*2,FONT='"Microsoft YaHei",sans-serif';
const blue='#14364e',dark='#102c43',soft='#819da9',white='#d3dcd7',gold='#d8b16a';
const clamp=x=>Math.max(0,Math.min(1,x)),p=(t,a,b)=>clamp((t-a)/(b-a));
const ease=u=>{u=clamp(u);return u*u*u*(10+u*(-15+6*u));},mix=(a,b,u)=>a+(b-a)*u;
let T=0,bounds=[];
function line(q,color=soft,w=1.3,a=1){C.save();C.globalAlpha*=a;C.strokeStyle=color;C.lineWidth=w;C.lineCap='round';C.lineJoin='round';C.beginPath();q.forEach(([x,y],i)=>i?C.lineTo(x,y):C.moveTo(x,y));C.stroke();C.restore();}
function poly(q,fill=blue,stroke=soft,w=1.3,a=1){C.save();C.globalAlpha*=a;C.beginPath();q.forEach(([x,y],i)=>i?C.lineTo(x,y):C.moveTo(x,y));C.closePath();C.fillStyle=fill;C.fill();if(stroke){C.strokeStyle=stroke;C.lineWidth=w;C.stroke();}C.restore();}
function box(x,y,w,h,fill=dark,stroke=soft,a=1){poly([[x,y],[x+w,y],[x+w,y+h],[x,y+h]],fill,stroke,1.2,a);}
function circle(x,y,r,color=soft,w=1.3,fill=null,a=1){C.save();C.globalAlpha*=a;C.beginPath();C.arc(x,y,r,0,TAU);if(fill){C.fillStyle=fill;C.fill();}C.strokeStyle=color;C.lineWidth=w;C.stroke();C.restore();}
function txt(s,x,y,size=26,color=white,align='left',a=1,weight=400){C.save();C.globalAlpha*=a;C.font=`${weight} ${size}px ${FONT}`;C.fillStyle=color;C.textAlign=align;C.fillText(s,x,y);C.restore();}
function at(x,y,fn,s=1){C.save();C.translate(x,y);C.scale(s,s);fn();C.restore();}
function label(s,x,y,w=200){line([[x,y+10],[x+w,y+10]],soft,.8,.5);txt(s,x,y,24,white);}
function bolt(x,y){circle(x,y,3,soft,1,null,.6);line([[x-2,y+2],[x+2,y-2]],soft,.7,.7);}
function gear(x,y,r,teeth,angle,active=false){at(x,y,()=>{C.rotate(angle);const q=[];for(let i=0;i<teeth*4;i++){let a=i/teeth/4*TAU,rr=r*(i%4===1||i%4===2?1:.85);q.push([Math.cos(a)*rr,Math.sin(a)*rr]);}poly(q,dark,active?gold:soft,1.5);circle(0,0,r*.66,active?gold:soft,1);for(let i=0;i<5;i++){const a=i/5*TAU;line([[Math.cos(a)*r*.2,Math.sin(a)*r*.2],[Math.cos(a)*r*.59,Math.sin(a)*r*.59]],soft,3,.6);}circle(0,0,r*.18,soft,1,blue);circle(0,0,3,gold,1);});}
function machineBase(x,y,w,h){box(x,y,w,h,dark,soft,.95);poly([[x,y],[x+18,y-15],[x+w+18,y-15],[x+w,y]],'#21445a',soft);poly([[x+w,y],[x+w+18,y-15],[x+w+18,y+h-15],[x+w,y+h]],'#0c263c',soft);for(const a of[x+12,x+w-12])for(const b of[y+12,y+h-12])bolt(a,b);for(let k=0;k<5;k++)line([[x+22+k*11,y+h-28],[x+22+k*11,y+h-13]],soft,.9,.6);}
function page(x,y,w=95,h=122,accent=false){box(x,y,w,h,'#17394f',accent?gold:soft);poly([[x+w-16,y],[x+w-16,y+16],[x+w,y+16]],blue,soft,.8);for(let i=0;i<5;i++)line([[x+12,y+25+i*14],[x+w-14-(i%2)*14,y+25+i*14]],i===0&&accent?gold:soft,1,.7);}
function dossier(x,y,s=1,rot=0,opened=0){at(x,y,()=>{C.rotate(rot);poly([[-3,-7],[36,-7],[45,0],[105,0],[105,72],[-3,72]],'#1a3a50',gold,2);line([[7,5],[7,67]],gold,1,.7);if(opened>0){poly([[10,7],[10-90*opened,4],[10-90*opened,68],[10,68]],'#23465a',gold,1.4);}for(let i=0;i<3;i++)line([[22,22+i*13],[85-(i%2)*17,22+i*13]],soft,1.1);box(73,48,18,12,'#9a7b45',null,.65);},s);}
const heroKeys=[[0,760],[12,760],[18.4,2010],[27.2,2010],[33.6,3280],[41.6,3280],[48,4560],[68,4560],[74.4,5970],[82.4,5970],[86.4,7160],[90,7160]];
function track(keys,t){let i=1;while(i<keys.length-1&&t>keys[i][0])i++;let a=keys[i-1],b=keys[i];return mix(a[1],b[1],ease(p(t,a[0],b[0])));}
const heroAt=t=>[track(heroKeys,t),840];
const cameraKeys=[[0,1050,560,1.08,0],[8,1050,560,1.08,0],[12,1050,560,1.03,0],[18.4,2240,550,1.02,-.012],[27.2,2320,550,1.04,0],[33.6,3540,550,1.02,.012],[41.6,3610,550,1.03,0],[48,4870,555,1.02,-.012],[55.6,4870,555,1.07,0],[59.2,5140,510,.95,0],[63.2,5140,510,.95,0],[68,4870,555,1.02,0],[74.4,6280,555,1.03,.01],[82.4,6280,555,1.03,0],[86.4,7470,560,1.05,0],[90,6350,600,.46,0]];
function cameraAt(t){let i=1;while(i<cameraKeys.length-1&&t>cameraKeys[i][0])i++;const a=cameraKeys[i-1],b=cameraKeys[i],u=ease(p(t,a[0],b[0]));return{x:mix(a[1],b[1],u),y:mix(a[2],b[2],u),z:Math.exp(mix(Math.log(a[3]),Math.log(b[3]),u)),r:mix(a[4],b[4],u)};}
function joint(a,b,l1,l2,side=1){const dx=b[0]-a[0],dy=b[1]-a[1],d=Math.min(Math.hypot(dx,dy),l1+l2-.001),theta=Math.atan2(dy,dx),q=Math.acos(Math.max(-1,Math.min(1,(l1*l1+d*d-l2*l2)/(2*l1*Math.max(d,.001)))));return[a[0]+Math.cos(theta+side*q)*l1,a[1]+Math.sin(theta+side*q)*l1];}
function limb(a,b,w1,w2,color,alpha=1){const dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1,n=[-dy/d,dx/d];poly([[a[0]+n[0]*w1,a[1]+n[1]*w1],[b[0]+n[0]*w2,b[1]+n[1]*w2],[b[0]-n[0]*w2,b[1]-n[1]*w2],[a[0]-n[0]*w1,a[1]-n[1]*w1]],color,soft,.9,alpha);}
function arm(a,b,side=1,back=false){const e=joint(a,b,65,62,side),col=back?'#193a4e':'#2a4a5b';limb(a,e,14,11,col,.92);limb(e,b,11,8,col,.92);circle(b[0],b[1],8,soft,.9,'#59727c',.85);}
function person(x,y,{walk=0,phase=0,reach=null,lean=0,expert=false,sitting=false,tone=0,ask=0,carrying=false,alpha=1,prop=true}={}){
let hand;at(x,y,()=>{C.globalAlpha*=alpha;const stride=Math.sin(phase)*34*walk,bob=(1-Math.cos(phase*2))*2.2*walk;const hip=[0,-133-bob],shoulder=[lean*17,-235-bob],head=[lean*25+3,-285-bob];
const feet=sitting?[[52,0],[85,-3]]:[[-18+stride,-Math.max(0,Math.cos(phase))*13*walk],[19-stride,-Math.max(0,-Math.cos(phase))*13*walk]];
feet.forEach((f,i)=>{const h=[hip[0]+(i?10:-10),hip[1]],ik=joint(h,[f[0],f[1]-8],67,69,i?-1:1),neutral=[i?18:-18,-66],k=sitting?[60+(i?9:0),-85]:[mix(neutral[0],ik[0],walk),mix(neutral[1],ik[1],walk)];limb(h,k,13,10,i?'#284555':'#1b384c');limb(k,[f[0],f[1]-8],10,7,i?'#284555':'#1b384c');poly([[f[0]-12,f[1]-9],[f[0]+9,f[1]-9],[f[0]+22,f[1]-1],[f[0]+20,f[1]+3],[f[0]-13,f[1]+3]],'#173146',soft,.8);});
const leftHand=[-36-stride*.45,-148];arm([shoulder[0]-21,shoulder[1]+14],leftHand,-1,true);
poly([[shoulder[0]-28,shoulder[1]],[shoulder[0]+24,shoulder[1]-2],[hip[0]+25,hip[1]+3],[hip[0]-25,hip[1]+3]],tone?'#42596a':'#294b5f',soft,1.3);
line([[shoulder[0]-15,shoulder[1]+6],[hip[0]-12,hip[1]-3]],soft,.8,.35);
if(!expert)line([[shoulder[0]+11,shoulder[1]+20],[shoulder[0]+19,shoulder[1]+20]],gold,3,.85);
limb([shoulder[0]+1,shoulder[1]-2],[head[0],head[1]+24],8,8,'#43616e');
C.save();C.translate(...head);C.rotate(.11+lean*.11);C.beginPath();C.ellipse(0,0,22,29,0,0,TAU);C.fillStyle='#416272';C.fill();C.strokeStyle='#9bafb3';C.lineWidth=1.2;C.stroke();line([[-13,-17],[-17,0],[-9,23]],'#76909a',.8,.3);C.restore();
hand=reach||[shoulder[0]+35+ask*46,-150-ask*61-stride*.45];arm([shoulder[0]+22,shoulder[1]+15],hand,1);
if(carrying&&prop)dossier(hand[0]-8,hand[1]+2,.62,-.04);
});return[x+hand[0],y+hand[1]];}
function motorAmount(start,end){return mix(.06,1,ease(p(T,start,start+.8))*(1-ease(p(T,end,end+.8))));}
function driveTime(t,a,b,r=.6){const I=u=>2.5*u**4-3*u**5+u**6;if(t<=a)return 0;if(t<a+r)return r*I((t-a)/r);if(t<=b)return t-a-r/2;if(t<b+r){const u=(t-b)/r;return b-a-r/2+r*(u-I(u));}return b-a;}
function gearDrive(x,y,start,end){const u=clamp((T-start)/(end-start)),angle=driveTime(T,start,end)*1.7,active=T>=start&&T<=end+.6;
gear(x,y,58,18,angle,active);gear(x+92,y,36,12,-angle*1.5+Math.PI/12,active);line([[x,y],[x+92,y]],soft,2,.6);machineBase(x-80,y+69,225,38);for(const xx of[x,x+92]){line([[xx,y+8],[xx,y+66]],soft,4);circle(xx,y,9,white,1.2,blue);}
// The output shaft reaches the working bed; the crank drives a constrained slider.
const crank=[x+92+Math.cos(-angle*1.5)*21,y+Math.sin(-angle*1.5)*21],slider=[x+193+Math.cos(-angle*1.5)*20,y-36];
line([crank,slider],active?gold:soft,3,.8);circle(...crank,4,soft,1,blue);box(slider[0]-16,slider[1]-8,32,16,blue,active?gold:soft);line([[x+153,y-45],[x+242,y-45]],soft,2);line([[x+153,y-26],[x+242,y-26]],soft,2);line([[x+92,y-12],[x+92,y-91],[x+262,y-91]],active?gold:soft,2,.65);circle(x+92,y-91,5,soft,1,blue);return u;}
function conveyor(x1,x2,y,active=true){line([[x1,y],[x2,y]],soft,3,.7);line([[x1,y+29],[x2,y+29]],soft,1.1,.5);for(let x=x1;x<x2;x+=70){circle(x,y+14,13,soft,1,blue,.65);const a=T*(active?2:.1)+x;line([[x+Math.cos(a)*9,y+14+Math.sin(a)*9],[x-Math.cos(a)*9,y+14-Math.sin(a)*9]],soft,1,.6);if(x%210<70){line([[x,y+30],[x,y+71]],soft,2,.45);line([[x-17,y+72],[x+17,y+72]],soft,2,.45);}}}
function scaffold(){
for(let x=0;x<8800;x+=80){line([[x,180],[x,1000]],soft,.6,x%400===0?.13:.05);line([[0,180+(x%800)],[8800,180+(x%800)]],soft,.5,.03);}
line([[0,870],[8700,870]],soft,2,.5);line([[0,888],[8700,888]],soft,.8,.4);
for(let x=80;x<8600;x+=320){line([[x,889],[x-18,913]],soft,1,.35);circle(x,870,4,soft,1,null,.5);}
// One continuous mechanical backbone: each bearing and rail belongs to this world.
conveyor(750,7800,924,false);
for(let x=850;x<7900;x+=650){gear(x,971,25,12,T*.19,false);line([[x,937],[x,971]],soft,2,.25);}
}
function initialDesk(){at(1000,0,()=>{
label('商机查询 · 从客户任务出发',-330,355,570);txt('下次客户沟通，从哪里切入？',-330,409,32);
machineBase(-280,710,675,30);line([[-240,740],[-240,841]],soft,3);line([[350,740],[350,841]],soft,3);
const scan=.5+.5*Math.sin(T*1.8);for(let i=0;i<4;i++){at(-70+i*100,635+(i%2)*14,()=>{C.rotate((i-1.5)*.1);page(0,0,85,68,i===Math.floor(T/1.6)%4);});}
txt('公告',-29,615,23,soft);txt('客户信息',100,610,23,soft);txt('解禁日历',245,635,23,soft);
line([[-160,675],[-125,661],[-78,661]],gold,1,.5*scan);
if(T>=6.4&&T<12){const a=ease(p(T,6.4,7.6))*(1-ease(p(T,10.8,12)));C.save();C.globalAlpha*=a;const labels=['融资','并购','股东服务','风险管理'];labels.forEach((s,i)=>{const selected=i===2,u=selected?ease(p(T,9.6,10.4)):0;at(-215+i*142,480-u*27,()=>{C.rotate((i-1.5)*.065*(1-u));box(0,0,124,81,dark,selected?gold:soft);txt(s,62,46,24,selected?gold:white,'center');});});C.restore();}
});}
function sorter(){at(2300,0,()=>{
label('01 / 线索归集',-340,355,580);txt('搜集耗时，信息还不全',-340,410,32);
machineBase(-185,560,530,180);for(let i=0;i<3;i++){const y=585+i*46;box(-160,y,165,28,blue,soft);txt(['公开公告','解禁日历','客户资料'][i],-146,y+21,20);line([[18,y+14],[120,y+14],[165,646]],soft,1.5,.75);}
box(160,591,150,109,blue,gold);txt('归集',235,632,25,white,'center');txt('摘要',235,668,23,soft,'center');
gearDrive(-70,810,19.2,24);conveyor(40,350,755,T>=19.2&&T<24);
const u=ease(p(T,19.2,20.8));for(let i=0;i<3;i++){if(T>=19.2&&T<21.6){let q=ease(p(T,19.2+i*.35,20.8+i*.2));page(mix(-120,193,q),mix(565+i*46,604+i*5,q),64,78,true);}}
if(T>20.8){const a=ease(p(T,20.8,21.6));C.save();C.globalAlpha*=a;txt('示例客户信息',-160,500,25,gold);txt('来源汇总 · 线索摘要',20,500,23,white);line([[-160,516],[320,516]],gold,1,.5);C.restore();}
});}
const logicRows=[['融资','融资预案','筹划阶段 / 募资用途'],['并购','重组、收购公告','交易阶段 / 对价来源'],['股东服务','减持披露、解禁日历','股东身份 / 窗口条件']];
function logic(){at(3600,0,()=>{
label('02 / 业务研判',-350,337,700);txt('有信号，还要找到服务切入点',-350,389,32);
machineBase(-200,438,740,265);const row=Math.min(2,Math.floor(p(T,34,38.4)*3));
logicRows.forEach((q,i)=>{const y=470+i*68,active=T>=34&&T<=41.6&&i===row;txt(q[0],-175,y+2,23,active?gold:white);txt(q[1],-35,y+2,22,soft);txt(q[2],190,y+2,22,active?white:soft);line([[-174,y+24],[512,y+24]],soft,.8,.3);if(active){line([[-185,y-26],[-185,y+12]],gold,3);gear(475,y-10,13,10,T*1.6,true);}});
txt('减持商机仅为业务示例',-180,679,20,soft);gearDrive(-80,795,34,40.8);
if(T>38.4){let a=ease(p(T,38.4,39.2));txt('研判要点 → 服务方向 → 沟通问题',-185,745,25,gold,'left',a);}
});}
const categories=['投行业务','机构业务','财富业务','资管业务','国际业务','投资业务','期货与衍生品','行业研究','综合专家'];
function amphitheatre(){at(4900,0,()=>{
label('03 / 专业协作',-420,307,880);txt('找到对口专家，一起研判',-420,359,32);
for(let tier=2;tier>=0;tier--){const y=445+tier*66;C.save();C.beginPath();C.ellipse(125,y,440-tier*36,90,0,Math.PI,TAU);C.strokeStyle=soft;C.lineWidth=1.5;C.stroke();C.beginPath();C.ellipse(125,y+18,440-tier*36,90,0,Math.PI,TAU);C.strokeStyle='#527084';C.lineWidth=1;C.stroke();C.restore();}
for(let i=8;i>=0;i--){const col=i%5,row=Math.floor(i/5),xx=-225+col*156+(row?58:0),yy=640-row*49;at(xx,yy,()=>person(0,0,{expert:true,sitting:true,tone:i%3,ask:.25*Math.sin(T*.9+i),alpha:1}),.29);}
txt('专业知识装备 · 业务方法沉淀 · 培养与试炼',-330,412,22,soft);
categories.forEach((s,i)=>{const x=-265+(i%3)*245,y=448+Math.floor(i/3)*31;box(x-8,y-22,222,28,'#15364d',null,.87);txt(s,x,y,20,white);});
});}
function meetingTable(){at(4900,0,()=>{
// Specialist nearest the task, all experts use the same abstract rig.
person(160,840,{expert:true,sitting:true,tone:1,ask:ease(p(T,52,53.6))*.6});
person(365,840,{expert:true,sitting:true,tone:0,ask:.35+.1*Math.sin(T)});
poly([[-260,682],[420,682],[478,717],[-310,717]],'#15374e',soft,1.6);box(-310,717,788,22,dark,soft);line([[-245,740],[-245,845]],soft,4);line([[420,740],[420,845]],soft,4);
page(-63,637,125,68,true);line([[70,665],[144,665]],gold,1.3,.8);
if(T>54.4)txt('需求 · 时机 · 服务切入点',-165,781,25,gold,'left',ease(p(T,54.4,55.2)));
});}
const slots=['核心规范','监管规则','产品能力','案例经验','研究资料','补充资料'];
function archive(){at(5550,0,()=>{
label('04 / 知识依据',-180,287,490);machineBase(-185,337,492,260);
slots.forEach((s,i)=>{const x=-165+(i%2)*236,y=355+Math.floor(i/2)*76,u=i===1?Math.sin(Math.PI*p(T,59.2,63.2))*30:0;box(x+u,y,212,60,blue,soft,.8);txt(s,x+u+18,y+36,23,white);line([[x+u+151,y+24],[x+u+185,y+24]],gold,2,.7);bolt(x+u+190,y+47);});
gearDrive(-90,704,59.2,64);line([[-92,638],[-92,597]],gold,3,.6);txt('检索依据，回到客户问题',-175,813,23,soft);
});
conveyor(4810,5600,615,T>=60.8&&T<=64);
if(T>=60.8){const u=ease(p(T,60.8,64)),x=mix(5510,4880,u),y=mix(556,623,u);page(x,y,92,68,true);if(T>64){txt('依据已纳入客户档案',4830,591,22,gold,'left',ease(p(T,64,64.8)));}}
}
function preparation(){at(6300,0,()=>{
label('05 / 沟通准备与经营接续',-350,355,750);txt('材料少重复，记录接得上',-350,408,32);
machineBase(-200,660,720,80);for(let i=0;i<3;i++){const u=ease(p(T,74.8+i*.4,76+i*.4)),x=mix(-150+i*190,60+i*7,u),y=mix(513,566+i*6,u);page(x,y,142,92,i===0);if(T<76){txt(['沟通要点','问题清单','跟进材料'][i],-150+i*190,490,25,white);}}
gearDrive(-70,814,74.8,79.2);
const press=ease(p(T,77.2,78))*(1-ease(p(T,79.2,80)));line([[45,449],[305,449]],soft,6);line([[72,450],[72,496+press*95]],gold,5);line([[280,450],[280,496+press*95]],gold,5);machineBase(35,496+press*95,280,25);
if(T>79.2){txt('一份客户档案，持续积累',-180,603,28,gold,'left',ease(p(T,79.2,80)));}
if(T>80){const u=ease(p(T,80,81.6));line([[470,700],[590,700],[590,786],[240,786]],gold,1.4,u);page(mix(470,240,u),mix(728,752,u),72,44,true);txt('沟通记录',398,835,22,soft);}
});}
function client(){at(7500,0,()=>{
label('06 / 客户沟通',-320,355,700);txt('带着依据和准备，走向客户',-320,408,32);
person(285,840,{expert:true,sitting:true,ask:.45,tone:1});poly([[-260,700],[410,700],[452,730],[-290,730]],'#16384e',soft,1.6);line([[-240,731],[-240,842]],soft,4);line([[400,731],[400,842]],soft,4);
if(T>85.6){page(99,654,125,57,true);}
});}
function heroState(t){const x=heroAt(t)[0],v=(heroAt(Math.min(90,t+.015))[0]-heroAt(Math.max(0,t-.015))[0])/.03,walk=clamp(Math.abs(v)/80),phase=x*.064;
let reach=null,lean=0,ask=0,carrying=true,handOff=null;
if(t<10.4){lean=.5;reach=[mix(62,105,.5+.5*Math.sin(t*1.5)),-165];carrying=false;}
if(t>=10.4&&t<12){const u=ease(p(t,10.4,12));lean=.5*(1-u);reach=[mix(88,35,u),mix(-152,-150,u)];}
if(t>=18.4&&t<=24.8){const u=ease(p(t,18.4,19.2))*(1-ease(p(t,24,24.8)));reach=[35+u*74,-150-u*24];lean=u*.5;carrying=t<19.2||t>=24;handOff='collection';}
if(t>=33.6&&t<=40.8){const u=ease(p(t,33.6,34.4))*(1-ease(p(t,40,40.8)));ask=.75*u;lean=.25*u;reach=[mix(35,104,u),mix(-150,-188+Math.sin(t*.8)*8,u)];}
if(t>=48&&t<=68){const u=ease(p(t,48,51.2))*(1-ease(p(t,67.2,68)));reach=[mix(35,105,u),-150];lean=.55*u;ask=.5;carrying=t<51.2||t>=67.2;handOff='meeting';}
if(t>=74.4&&t<=82.4){const u=ease(p(t,74.4,75.2))*(1-ease(p(t,81.6,82.4)));reach=[mix(35,107,u),-150];lean=.45*u;carrying=t<75.2||t>=81.6;handOff='preparation';}
if(t>=86.4){const u=ease(p(t,86.4,87.2));reach=[mix(35,112,u),-150];lean=.4*u;carrying=false;}
return{x,v,walk,phase,reach,lean,ask,carrying,handOff};}
function heldPose(t){const h=heroState(t),hand=h.reach||[h.lean*17+35+h.ask*46,-150-h.ask*61-Math.sin(h.phase)*34*h.walk*.45];return[h.x+hand[0]-8,842+hand[1]];}
function dossierPose(t){
if(t<10.4)return{x:840,y:690,owner:'desk',open:.25};
if(t>=19.2&&t<24){const a=heldPose(19.2),b=heldPose(24);let u;if(t<20.8){u=ease(p(t,19.2,20.8));return{x:mix(a[0],2530,u),y:mix(a[1],691,u),owner:'sorter',open:0};}u=ease(p(t,21.6,24));return{x:mix(2530,b[0],u),y:mix(691,b[1],u),owner:'sorter',open:0};}
if(t>=51.2&&t<67.2){const a=heldPose(51.2);return{x:a[0],y:a[1],owner:'expert-table',open:.7*ease(p(t,51.2,52))};}
if(t>=75.2&&t<81.6){const a=heldPose(75.2);return{x:a[0],y:a[1],owner:'preparation',open:.7*(1-ease(p(t,78.4,79.2)))};}
if(t>=87.2){const a=heldPose(87.2);return{x:a[0],y:a[1],owner:'client-table',open:.7};}
const a=heldPose(t);return{x:a[0],y:a[1],owner:'hero-hand',open:0};
}
function protagonist(){const h=heroState(T);person(h.x,840,{...h,prop:false});return h;}
function captions(){C.save();C.setTransform(scale,0,0,scale,0,0);let shot=plan.shots.find(s=>T>=s.start&&T<s.end)||plan.shots.at(-1);const a=Math.min(ease(p(T,shot.start+.15,shot.start+.75)),1-ease(p(T,shot.end-.5,shot.end)));C.globalAlpha=a;
txt('FIRMBUDDY  /  BUSINESS IN MOTION',88,67,17,soft);txt(shot.title,88,132,46,white,'left',1,500);
line([[88,160],[1832,160]],soft,1,.35);txt(shot.result,88,988,29,white);if(shot.ai)txt(shot.ai,1830,987,22,soft,'right');
if(T>=12&&T<28)txt('商机查询：融资 / 并购 / 股东服务 / 风险管理等',1830,204,22,soft,'right');
if(T>=84){txt('专业支持在身后，客户任务在眼前',88,204,27,gold);}
C.restore();}
function world(t){T=Math.max(0,Math.min(90,t));bounds=[];const ca=cameraAt(T);setCam({...ca,z:ca.z*scale});clear();
C.save();C.translate(W/2,H/2);C.scale(ca.z*scale,ca.z*scale);C.rotate(ca.r);C.translate(-ca.x,-ca.y);
scaffold();initialDesk();sorter();logic();amphitheatre();archive();preparation();client();
protagonist();meetingTable();
const dp=dossierPose(T);dossier(dp.x,dp.y,.62,0,dp.open);
// Foreground bearings offer physical occlusion during travel, below task/action zones.
for(const x of[1650,2950,4250,5650,6900]){machineBase(x,835,70,105);gear(x+36,894,34,14,T*.4,false);line([[x+35,835],[x+35,797]],soft,5,.5);}
C.restore();captions();compose(inkC,fxC,ovC,{sheet:[10000,2000],cam,seed:19});}
window.renderAt=(t,type='image/png',quality=.95)=>{world(t);return type?canvas.toDataURL(type,quality):null;};
window.cameraAt=cameraAt;window.heroAt=heroAt;window.stateAt=t=>({time:t,camera:cameraAt(t),hero:heroAt(t),pose:heroState(t),dossier:dossierPose(t),buffer:[W,H],duration:90,bounds});
window.__ready=true;world(0);
const audio=new Audio('./audio/mix.wav'),seek=document.querySelector('#seek'),display=document.querySelector('#time'),button=document.querySelector('#play');let playing=false,started=0,base=0;
seek.oninput=()=>{base=+seek.value;audio.currentTime=base;started=performance.now();world(base);display.textContent=base.toFixed(2)+' / 90';};
button.onclick=()=>{playing=!playing;button.textContent=playing?'暂停':'播放';if(playing){base=+seek.value;if(base>=90)base=0;started=performance.now();audio.currentTime=base;audio.play().catch(()=>{});}else{base=+seek.value;audio.pause();}};
function tick(){if(playing){const t=Math.min(90,base+(performance.now()-started)/1000);world(t);seek.value=t;display.textContent=t.toFixed(2)+' / 90';if(t>=90){playing=false;audio.pause();button.textContent='播放';}}requestAnimationFrame(tick);}if(!Q.has('render'))tick();
