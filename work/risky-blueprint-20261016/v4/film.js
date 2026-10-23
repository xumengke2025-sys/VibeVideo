import {W,H,g,ov,inkC,fxC,ovC,setCam,clear,cam,line,text,rect,circ,solid,hatch,trunc,NIBS,S,proj,gearPts} from './vendor/draw.js';
import {makePaper} from './vendor/paper.js';
const canvas=document.querySelector('#c');canvas.width=W;canvas.height=H;
const compose=makePaper(canvas,W,H),scale=W/1920;
const plan=await (await fetch('./plan.json')).json(),Q=new URLSearchParams(location.search);
if(Q.has('render'))document.body.classList.add('render');
await document.fonts.load('400 48px "Microsoft YaHei"');
const FONT='"Microsoft YaHei",sans-serif',MONO='Consolas,monospace',TAU=Math.PI*2;
const clamp=x=>Math.max(0,Math.min(1,x)),p=(t,a,b)=>clamp((t-a)/(b-a));
const ease=x=>{x=clamp(x);return x*x*x*(x*(x*6-15)+10)},mix=(a,b,u)=>a+(b-a)*u;
let T=0,ox=0,oy=0,visibility=1,bounds=[];
const show=(a,b=.36)=>p(T,a,a+b);
const at=(x,y,fn,v=1)=>{const old=[ox,oy,visibility];ox=x;oy=y;visibility*=v;fn();[ox,oy,visibility]=old;};
const pts=q=>q.map(([x,y])=>[x+ox,y+oy]);
function L(q,u=1,w=2,v=1,dash){if(visibility<.01)return;line(pts(q),{u,w,v:v*visibility,dash,nib:false});}
function R(x,y,w,h,u=1,v=1,lw=2){L([[x,y],[x+w,y],[x+w,y+h],[x,y+h],[x,y]],u,lw,v);}
function C(x,y,r,u=1,v=1,w=2){L(circ(x,y,r,64),u,w,v);}
function panel(x,y,w,h,u=1,v=1,th=0){solid(pts(rect(x,y,x+w,y+h)),{u,v:v*visibility,w:2.2,th});}
function TX(str,x,y,size=44,u=1,o={}){
  if(u<=0||visibility<.01)return;const v=(o.v??1)*visibility;
  text(str,ox+x,oy+y,{size,u,font:FONT,nib:false,...o,v});
  if(u>=.999&&v>=.64&&size*cam.z/scale>=30){
    g.font=`${o.weight||400} ${size}px ${o.font||FONT}`;const width=g.measureText(str).width;
    const dx=o.align==='center'?-width/2:o.align==='right'?-width:0;
    const corners=[[x+dx,y-size*.95],[x+dx+width,y-size*.95],[x+dx+width,y+size*.22],[x+dx,y+size*.22]].map(([a,b])=>S(ox+a,oy+b));
    bounds.push({id:o.id||str,text:str,box:[Math.min(...corners.map(q=>q[0]))/scale,Math.min(...corners.map(q=>q[1]))/scale,Math.max(...corners.map(q=>q[0]))/scale,Math.max(...corners.map(q=>q[1]))/scale],size:size*cam.z/scale});
  }
}
const mono=(s,x,y,size=21,u=1,o={})=>TX(s,x,y,size,u,{font:MONO,...o});
function doc(x,y,w,h,u=1,v=1){solid(pts([[x,y],[x+w-26,y],[x+w,y+26],[x+w,y+h],[x,y+h]]),{u,v:v*visibility,w:2.2});L([[x+w-26,y],[x+w-26,y+26],[x+w,y+26]],u,1,v*.6);}
function detail(x,y,w,n=4,u=1){for(let i=0;i<n;i++)L([[x,y+i*17],[x+w*(i===n-1?.65:1),y+i*17]],clamp(u*n-i),1,.28);}
function route(q,a,b,w=2.8,v=.95){const u=p(T,a,b);L(q,u,w,v);const tip=trunc(q,u)[1];if(tip&&u>0&&u<1){C(tip[0],tip[1],7,1,.95,1.5);C(tip[0],tip[1],13,1,.3,1);}}
function bolt(x,y,u=1){C(x,y,7,u,.65,1.3);L([[x-3,y+3],[x+3,y-3]],u,1,.5);}
function center(x,y,r,u=1){L([[x-r-24,y],[x+r+24,y]],u,1,.27,'center');L([[x,y-r-24],[x,y+r+24]],u,1,.27,'center');}
function dim(x,y,w,s,u=1){L([[x,y-12],[x,y+16]],u,1,.4);L([[x+w,y-12],[x+w,y+16]],u,1,.4);L([[x,y],[x+w,y]],u,1,.4);L([[x+12,y-5],[x,y],[x+12,y+5]],u,1,.4);L([[x+w-12,y-5],[x+w,y],[x+w-12,y+5]],u,1,.4);mono(s,x+w/2,y-16,18,u,{align:'center',v:.45});}
function leader(s,q,u=1,size=31){L(q,u,1.4,.7);C(q[0][0],q[0][1],4,u,.7,1);TX(s,q.at(-1)[0],q.at(-1)[1]-12,size,u);}
function bearing(x,y,u=1){panel(x-22,y-34,44,68,u,.55,15);C(x,y,13,u,.6,1.5);bolt(x-14,y-25,u);bolt(x+14,y+25,u);}
function shaft(q,u=1,v=.42){L(q.map(([x,y])=>[x,y-9]),u,1.7,v);L(q.map(([x,y])=>[x,y+9]),u,1.7,v);L(q,u,1,v*.65,'center');}
function truss(x0,y0,x1,y1,n=8,u=1){const dx=x1-x0,dy=y1-y0,len=Math.hypot(dx,dy),nx=-dy/len*24,ny=dx/len*24;L([[x0+nx,y0+ny],[x1+nx,y1+ny]],u,1.8,.4);L([[x0-nx,y0-ny],[x1-nx,y1-ny]],u,1.8,.4);for(let i=0;i<n;i++){const a=i/n,b=(i+1)/n;L([[x0+dx*a+nx,y0+dy*a+ny],[x0+dx*b-nx,y0+dy*b-ny]],u,1,.3);L([[x0+dx*a-nx,y0+dy*a-ny],[x0+dx*b+nx,y0+dy*b+ny]],u,1,.22);}}
// Reference mesh equation: opposing tooth phase, pitch radii proportional to tooth count.
function meshAngle(a,T1,T2,c1,c2){const phi=Math.atan2(c2[1]-c1[1],c2[0]-c1[0]);return phi+Math.PI-Math.PI/T2-(a-phi)*T1/T2;}
function toothAngle(t){const ticks=Math.max(0,(t-11)/.25),i=Math.floor(ticks),u=ticks-i;return(i+1-(1-u)**3)*Math.PI/20;}
function gear(x,y,teeth,m,a,u=1,v=1,depth=22){
  const r=teeth*m/2;center(x,y,r,u);solid(pts(gearPts(x,y,teeth,m,a)),{th:depth,u,w:2.6,v:v*visibility,conn:false});
  C(x,y,r*.77,u,v*.7,1.4);C(x,y,r*.21,u,v,2.2);C(x,y,r*.08,u,v*.6,1.2);
  for(let i=0;i<6;i++){const b=a+i*TAU/6;L([[x+Math.cos(b)*r*.23,y+Math.sin(b)*r*.23],[x+Math.cos(b)*r*.72,y+Math.sin(b)*r*.72]],u,2,v*.75);C(x+Math.cos(b+.22)*r*.52,y+Math.sin(b+.22)*r*.52,r*.075,u,v*.6,1.1);}
}

// V4: one case, immutable source snapshot, explicit conditional experiments.
const domains=['投行业务','机构业务','财富业务','资管业务','国际业务','投资业务','期货与衍生品','行业研究','综合专家'];
const atTime=id=>plan.events.find(e=>e.id===id).at;
const eventProgress=(id,duration=1)=>ease(p(T,atTime(id)-duration,atTime(id)));
const ellipse=(x,y,rx,ry,a0=0,a1=TAU,n=96)=>Array.from({length:n+1},(_,i)=>{const a=mix(a0,a1,i/n);return[x+rx*Math.cos(a),y+ry*Math.sin(a)]});
function bez(a,b,c,d,n=180){return Array.from({length:n+1},(_,i)=>{const u=i/n,v=1-u;return[v*v*v*a[0]+3*v*v*u*b[0]+3*v*u*u*c[0]+u*u*u*d[0],v*v*v*a[1]+3*v*v*u*b[1]+3*v*u*u*c[1]+u*u*u*d[1]]});}
const paths={evidence:bez([1000,1200],[1700,1200],[2100,1100],[3200,1100]),hall:bez([3200,1100],[4100,1100],[4400,1600],[5900,1600]),snapshot:bez([5900,1600],[7300,1600],[7400,2900],[6600,2900]),trial:bez([6600,2900],[6000,2900],[5700,2500],[5000,2500]),record:bez([5000,2500],[3100,2350],[1700,2650],[1100,3250]),return:bez([1100,3250],[1000,2100],[4400,2080],[5900,1600]),monitor:bez([5900,1600],[4500,2000],[2100,2050],[1000,1200])};
const pathPoint=(q,u)=>u<=0?q[0]:u>=1?q.at(-1):trunc(q,u)[1];
// Trapezoidal travel: long uniform middle, smooth acceleration and deceleration.
function travel(u){u=clamp(u);const a=.2,k=1/(1-a);if(u<a)return k*(u/2-a*Math.sin(Math.PI*u/a)/(2*Math.PI));if(u>1-a)return 1-travel(1-u);return k*(u-a/2);}
const moving=(name,t,a,b)=>pathPoint(paths[name],travel(p(t,a,b)));
const keys=[
 [0,1000,1010,1.0],[4,1010,1010,1.025],[8,1030,1040,1.0],[11,1080,1070,.97],
 [12,1280,1110,.84],[14,2200,1080,.79],[16,3200,1020,.87],[18,3200,1020,.90],
 [20,3360,1090,.81],[22,4430,1330,.66],[24,5830,1160,.65],[28,5920,1100,.69],
 [30,5940,1120,.70],[32,5940,1180,.70],[34,5940,1230,.72],[36,5950,1270,.73],
 [38,6020,1540,.78],[40,...moving('snapshot',40,38,42),.70],[42,6600,2810,.90],[44,6600,2810,.94],
 [46,6270,2790,.79],[48,4890,2670,.58],[50,3500,3130,.52],[54,3500,3130,.52],[58,3500,3130,.52],[61,3550,3090,.50],
 [63,4600,2630,.59],[64,...moving('record',64,64,68),.60],[65,...moving('record',65,64,68),.65],[66,...moving('record',66,64,68),.77],
 [67,...moving('record',67,64,68),.82],[68,1100,3090,.89],[69,1100,3090,.89],[70,...moving('return',70,69,75),.72],[71,...moving('return',71,69,75),.63],[72,...moving('return',72,69,75),.61],[73,...moving('return',73,69,75),.65],[74,...moving('return',74,69,75),.70],[75,5950,1450,.70],
 [76.5,5650,1900,.46],[79,4100,2350,.225],[80,4100,2350,.225]
];
// Shape-preserving cubic interpolation: shared endpoint velocity, no camera clamps.
function camSlope(i,k){if(i===0||i===keys.length-1)return 0;const a=keys[i-1],b=keys[i],c=keys[i+1],val=q=>k===3?Math.log(q[k]):q[k],d0=(val(b)-val(a))/(b[0]-a[0]),d1=(val(c)-val(b))/(c[0]-b[0]);return d0*d1<=0?0:2*d0*d1/(d0+d1);}
function cameraAt(t){let i=1;while(i<keys.length-1&&t>keys[i][0])i++;const a=keys[i-1],b=keys[i],h=b[0]-a[0],u=p(t,a[0],b[0]);const vals=[1,2,3].map(k=>{const aa=k===3?Math.log(a[k]):a[k],bb=k===3?Math.log(b[k]):b[k];const v=(2*u**3-3*u*u+1)*aa+(u**3-2*u*u+u)*h*camSlope(i-1,k)+(-2*u**3+3*u*u)*bb+(u**3-u*u)*h*camSlope(i,k);return k===3?Math.exp(v):v;});return{x:vals[0],y:vals[1],z:vals[2],r:0};}
function rail(q,v=.2){L(q.map(([x,y])=>[x,y-18]),1,1.4,v);L(q.map(([x,y])=>[x,y+18]),1,1.4,v);L(q,1,.8,v*.4,'center');}
function plaque(s,x,y,w,size=36){const h=Math.max(72,size*1.8);panel(x,y,w,h,1,.9,10);R(x+7,y+7,w-14,h-14,1,.4,1);bolt(x+14,y+h/2);bolt(x+w-14,y+h/2);TX(s,x+w/2,y+h*.71,size,1,{align:'center'});}
function base(x,y,w,h){R(x,y,w,h,1,.5,2);truss(x,y+h+24,x+w,y+h+24,Math.round(w/100));for(const xx of[x+35,x+w-35]){panel(xx-17,y+h+50,34,90,1,.6,12);panel(xx-44,y+h+133,88,20,1,.7,10);bolt(xx-24,y+h+143);bolt(xx+24,y+h+143);}}
function goldLine(q,width=3,color='#cdb77b',alpha=.9){ov.save();ov.strokeStyle=color;ov.globalAlpha=alpha*visibility;ov.lineWidth=width*Math.pow(cam.z,.65);ov.beginPath();q.forEach(([x,y],i)=>{const pt=S(x+ox,y+oy);i?ov.lineTo(...pt):ov.moveTo(...pt)});ov.stroke();ov.restore();}
function goldDot(x,y,r,color='#d1b878'){const q=S(x+ox,y+oy);ov.save();ov.fillStyle=color;ov.globalAlpha=visibility;ov.beginPath();ov.arc(...q,r*cam.z,0,TAU);ov.fill();ov.restore();}
function dial(x,y,r,value,label){C(x,y,r,1,.9,2.7);C(x,y,r-12,1,.6,1.5);for(let i=0;i<=20;i++){const a=Math.PI*.78+i*Math.PI*1.44/20;L([[x+Math.cos(a)*(r-22),y+Math.sin(a)*(r-22)],[x+Math.cos(a)*(r-(i%5?30:40)),y+Math.sin(a)*(r-(i%5?30:40))]],1,1.5,.6);}const a=Math.PI*.78+value*Math.PI*1.44;goldLine([[x,y],[x+Math.cos(a)*(r-35),y+Math.sin(a)*(r-35)]],5);C(x,y,12,1,.9,2);TX(label,x,y+r*.48,26,1,{align:'center'});bearing(x,y+r+30);}
function screw(x0,x1,y,phase){shaft([[x0,y],[x1,y]],1,.65);for(let x=x0+12;x<x1-12;x+=22){const a=x+phase%22;L([[a,y-9],[a+12,y+9]],1,1.2,.5);}bearing(x0,y);bearing(x1,y);}

function card(x,y,w,h,label,sub='',col='#c9b781',alpha=1){const q=S(x,y);ov.save();ov.setTransform(cam.z,0,0,cam.z,q[0],q[1]);ov.globalAlpha=alpha;ov.fillStyle='#081a29';ov.fillRect(-w/2+7,-h/2+9,w,h);ov.strokeStyle='#304e60';ov.lineWidth=1.5;ov.strokeRect(-w/2+7,-h/2+9,w,h);ov.fillStyle='#102b3d';ov.fillRect(-w/2,-h/2,w,h);ov.strokeStyle=col;ov.lineWidth=2;ov.strokeRect(-w/2,-h/2,w,h);ov.fillStyle=col;ov.fillRect(-w/2,-h/2,5,h);ov.textAlign='center';ov.fillStyle='#edf1ed';ov.font=`500 ${w>400?40:sub?32:34}px ${FONT}`;ov.fillText(label,0,sub?-2:11);if(sub){ov.font=`23px ${FONT}`;ov.fillStyle='#a6bcc5';ov.fillText(sub,0,30);}ov.restore();}
function caseBox(x,y){const status=T<10?'待核实线索':T<36?'原文索引 E-01':T<44?'会商条件已附':T<64?'共同快照 S-001':'附三份情景记录';card(x,y,290,110,'案件 A-001',status,'#c9b781',ease(p(T,9.5,10)));}
function casePosition(t){if(t<12)return[1000,1200];if(t<16)return moving('evidence',t,12,16);if(t<20)return[3200,1100];if(t<24)return moving('hall',t,20,24);if(t<38)return[5900,1600];if(t<42)return moving('snapshot',t,38,42);if(t<46)return[6600,2900];if(t<48)return moving('trial',t,46,48);if(t<64)return[5000,2500];if(t<68)return moving('record',t,64,68);if(t<69)return[1100,3250];if(t<75)return moving('return',t,69,75);return[5900,1600];}
function mainCase(){if(T<9.5)return;const pt=casePosition(T);caseBox(...pt);if(T>=75)goldLine(trunc(paths.monitor,ease(p(T,75.5,79)))[0],3,'#bba972',.65);}
function signal(){at(1000,1000,()=>{
 base(-650,-300,1300,600);mono('01 / SIGNAL & EVIDENCE',-640,-345,24,1,{v:.6});
 for(let i=0;i<3;i++){const x=-550+i*260;C(x,-245,33,1,.7,2);C(x,25,33,1,.7,2);panel(x-62,-245,124,270,1,.7,8);['公告','财务','司法'].forEach((s,j)=>{if(i===j)TX(s,x,-164,38,1,{align:'center'});});detail(x-42,-120,84,6);shaft([[x,-270],[x,55]],1,.25);}
 dial(390,-95,157,.30+.47*ease(p(T,1.5,3)),'异常信号');
 const slide=mix(-540,0,ease(p(T,6.5,9)));shaft([[-580,140],[470,140]],1,.6);bearing(-580,140);bearing(470,140);
 gear(-540,140,20,5,ease(p(T,6,10))*TAU,1,.65,16);panel(slide-45,108,90,64,1,.9,14);L([[slide,108],[slide,28]],1,5,.8);panel(slide-80,8,160,26,1,.7,8);
 if(T>=6){const u=ease(p(T,7,atTime('bind')));doc(-180,-220,310,260,1,.85);TX('企业 A',-145,-157,40);TX('重大诉讼信号',-145,-98,31);TX('原文索引 E-01',-145,-41,25);L([[-145,-20],[90,-20]],1,2,.65);C(mix(-400,30,u),-70,65,1,.9,3);C(mix(-400,30,u),-70,58,1,.3,1);}
 
 plaque('示例案件 · A-001',-620,345,430,33);TX('AI 检索 · 提取 · 来源比对',-140,392,35);
 if(T>2&&T<6)goldDot(390+120,-180,12,'#d2a45b');
 });}

function relations(){at(3200,1000,()=>{mono('02 / EVIDENCE BEFORE CONNECTION',-690,-350,23,1,{v:.5});base(-700,-290,1400,590);const u=eventProgress('edge',1.5);const ns=[[-450,-140,'控股主体'],[0,-205,'企业 A'],[480,-100,'关联企业'],[-370,230,'司法材料'],[410,230,'业务关系']];const links=[[1,0,'控制',true],[1,2,'股权',true],[0,3,'原文依据',true],[2,4,'待核实',false]];links.forEach(([a,b,label,known])=>{const A=ns[a],B=ns[b],q=[[A[0]*u,A[1]*u],[B[0]*u,B[1]*u]];L(q,1,known?2.5:1.5,known?.7:.38,known?undefined:[8,10]);const x=(A[0]+B[0])*.5*u,y=(A[1]+B[1])*.5*u;TX(label,x,y-16,25,show(18.2,.6),{align:'center',v:.65});});ns.forEach(([x,y,label])=>{panel(x*u-112,y*u-46,224,92,1,.85,16);TX(label,x*u,y*u+10,33,1,{align:'center'});bolt(x*u-94,y*u-29);});TX('行业背景：参考层，不作为传播边',0,-440,32,1,{align:'center',v:.6});L([[-620,-400],[620,-400]],1,1,.25,[8,12]);TX('可能路径 ≠ 必然传导',0,380,38,1,{align:'center'});});}
function hall(){at(5950,1200,()=>{
 mono('03 / KNOWLEDGE · METHODS · EXPERTS',-1060,-670,24,1,{v:.6});
 // Knowledge archive behind the amphitheatre, with one extracted active loadout.
 for(let bank=0;bank<3;bank++){const x=-980+bank*690;panel(x,-590,620,228,1,.7,26);TX(['专业知识库','专业方法','知识装备'][bank],x+310,-540,39,1,{align:'center'});for(let j=0;j<6;j++){const pull=(bank===1&&j===2)?100*ease(p(T,29.5,31)):0;panel(x+20+j*96,-505+pull,84,112,1,.65,12);R(x+46+j*96,-470+pull,32,10,1,.5,1);} }
 domains.forEach((s,i)=>TX(s,-1010+(i%3)*730,-285+Math.floor(i/3)*60,34,1,{v:.85}));
 for(let row=0;row<3;row++){const rx=1000-row*150,ry=480-row*105,cy=390;const q=ellipse(0,cy,rx,ry,Math.PI,TAU);L(q,1,2.8,.8);L(q.map(([x,y])=>[x,y+40]),1,1.6,.5);for(let j=0;j<11;j++){const a=Math.PI+.10+j*(Math.PI-.2)/10,x=Math.cos(a)*(rx-25),y=cy+Math.sin(a)*(ry-20);panel(x-34,y-24,68,43,1,.65,12);L([[x-22,y+22],[x-22,y+45],[x+22,y+45],[x+22,y+22]],1,1.4,.4);if(row===1&&[3,5,7].includes(j)&&T>27){goldLine([[x-25,y+5],[x+25,y+5]],4);if(T<30)goldLine([[x,y+45],[0,390]],2,'#ccb778',show(27+(j-3)*.25,.5));}}}
 for(const x of[-1040,1040]){panel(x-22,360,44,220,1,.65,15);panel(x-52,570,104,22,1,.7,12);}
 L(ellipse(0,405,520,105),1,3,.85);L(ellipse(0,425,520,105),1,1.6,.6);truss(-420,545,420,545,8);bearing(-340,520);bearing(340,520);
 ['尽调评估专家','合规风险专家','风险监控专家'].forEach((s,i)=>plaque(s,-650+i*460,230,410,31));
 
 if(T>=30&&T<34){const previousVisibility=visibility;visibility*=ease(p(T,30,30.4))*(1-ease(p(T,33.4,34)));const z=ease(p(T,30,atTime('knowledge')));doc(-100,-360+z*260,200,150,1,.9);TX('检索依据',0,-300+z*260,29,1,{align:'center'});detail(-75,-270+z*260,150,3);visibility=previousVisibility;}
 if(T>35.5){const labels=T>=75?['补充核查','持续跟踪','监测事项']:['共同依据','保留分歧','推演条件'];labels.forEach((s,i)=>plaque(s,-650+i*460,605,410,34));}
 });}

function snapshot(){at(6600,2900,()=>{mono('04 / ONE IMMUTABLE STARTING STATE',-630,-365,24,1,{v:.5});base(-640,-290,1280,560);rail([[-650,0],[650,0]],.5);const close=eventProgress('freeze',1.8)*(1-ease(p(T,45,46)));screw(-535,535,105,close*220);for(const side of[-1,1]){const x=side*mix(340,169,close);panel(x-35,78,70,54,1,.85,14);L([[x,78],[x,-95]],1,5,.7);panel(x-24,-95,48,180,1,.9,16);}const drive=close*TAU;gear(-535,105,24,5,drive,1,.75,18);gear(-640,105,18,5,meshAngle(drive,24,18,[-535,105],[-640,105]),1,.6,16);for(let i=0;i<3;i++){panel(-535+i*375,-250,320,110,1,.6,10);TX(['证据来源','主体关系','初始状态'][i],-375+i*375,-185,37,1,{align:'center'});}plaque('锁定版本  S-001',-440,170,880,44);TX('固定起点，不代表确认结论',0,365,36,1,{align:'center'});});}
const trialXs=[2450,3500,4550],trialColors=['#c7b987','#d39880','#8cbeb5'];
function hypothesis(i){return eventProgress('assumptions',1.5);}
function trialState(i,u){const initial=.34*(1-Math.exp(-u*5));return i===0?initial:i===1?initial+.24*(1-Math.exp(-u*6)):initial*(1-.62*ease(p(u,.3,1)));}
function traces(cx,i){const run=p(T,atTime('run'),atTime('records')),col=trialColors[i];at(cx,3100,()=>{base(-440,-365,880,890);plaque(['基准情景','不利情景','缓释情景'][i],-400,-770,800,52);TX('快照 S-001',0,-405,29,1,{align:'center',v:.6});panel(-165,-275,490,100,1,.45,12);L([[-236,-175],[-165,-175],[-165,-225]],1,2,.5);
 const drive=TAU*1.3*run;gear(-320,-175,24,4,drive,1,.65,16);gear(-236,-175,18,4,meshAngle(drive,24,18,[-320,-175],[-236,-175]),1,.5,13);screw(-340,340,385,run*220);
 for(let layer=0;layer<2;layer++){const yy=-35+layer*205;TX(['业务路径','舆情路径'][layer],-375,yy-48,31);const pts=[[-245,yy],[0,yy-60],[265,yy],[-25,yy+70]],links=[[0,1],[1,2],[0,3],[3,2]],lr=p(T,54+layer*2,60+layer*2);links.forEach(([a,b],j)=>{const q=[pts[a],pts[b]];L(q,1,1.6,.25,[8,9]);const active=j<2?clamp(lr*1.7-j*.24):j===2&&i===1?clamp(lr*1.5-.65):0;if(active>0)goldLine(trunc(q,active)[0],3.5,col,i===2?.75:.9);});pts.forEach(([x,y],j)=>{panel(x-42,y-34,84,68,1,.4,10);C(x,y,28,1,.65,1.8);const active=(j<3||i===1)?trialState(i,clamp(lr-j*.14)):0;const a=-Math.PI*.68+active*Math.PI*1.7;goldLine([[x,y],[x+Math.cos(a)*22,y+Math.sin(a)*22]],2.5,col);});if(i===2){const u=hypothesis(i);L([[105,yy-83],[105,yy-30]],1,2,.55);C(105,yy-87,21,1,.7,2);goldLine([[105-18*Math.cos(u*Math.PI/2),yy-87-18*Math.sin(u*Math.PI/2)],[105+18*Math.cos(u*Math.PI/2),yy-87+18*Math.sin(u*Math.PI/2)]],3,col);}}
 panel(-310,430,620,130,1,.55,20);L(ellipse(-310,495,18,65),1,1.8,.7);L(ellipse(310,495,18,65),1,1.8,.7);for(let j=1;j<4;j++)L([[-285,430+j*32],[285,430+j*32]],1,.8,.15);
 // Continuous endpoint: include the exact current u, not just integer plot samples.
 const curve=[];for(let j=0;j<=100;j++){const u=Math.min(run,j/100);curve.push([-280+560*u,535-170*trialState(i,u)]);if(u===run)break;}if(run>0){goldLine(curve,3,col);const[x,y]=curve.at(-1);panel(x-28,365,56,40,1,.7,10);L([[x,405],[x,y]],1,2,.65);C(x,y,5,1,.9,1.4);}
 TX('假设下的相对变化 · 示意',0,612,29,1,{align:'center'});
 });}
function trials(){rail([[2450,2500],[5000,2500]],.35);trialXs.forEach((cx,i)=>{rail(bez([5000,2500],[cx,2500],[cx,2500],[cx,2720]),.28);traces(cx,i);});at(3500,3830,()=>{L([[-1400,0],[1400,0]],1,1.6,.45);for(let j=0;j<=8;j++)L([[-1400+j*350,-10],[-1400+j*350,10]],1,1.5,.4);goldDot(-1400+2800*p(T,54,62),0,10);TX('同一证据快照 / 同一轮次 / 仅假设不同',0,65,42,1,{align:'center'});});}
function trialCards(){trialXs.forEach((cx,i)=>{if(T>=48&&T<50){const q=bez([5000,2500],[cx,2500],[cx,2500],[cx,2695]);card(...pathPoint(q,travel(p(T,48,50))),250,88,'S-001',['基准副本','不利副本','缓释副本'][i],trialColors[i]);}else if(T>=50){card(cx,2695,250,88,'S-001',['基准副本','不利副本','缓释副本'][i],trialColors[i]);}
 if(T>=50.5){const h=hypothesis(i),y=mix(2800,2875,h),alpha=ease(p(T,50.5,51));card(cx+80,y,470,95,['不追加冲击','追加不利冲击','加入缓释干预'][i],'输入假设',trialColors[i],alpha);}
 if(T>=62&&T<64){const u=travel(p(T,atTime('records')+i*.25,[atTime('record0'),atTime('record1'),atTime('collect')][i])),q=bez([cx,3580],[cx-470,3650],[cx-480,2500],[5000,2500]);card(...pathPoint(q,u),230,105,['基准记录','不利记录','缓释记录'][i],'保留条件与依据',trialColors[i],1-.75*ease(p(u,.88,1)));}
 });}
function recorder(){at(1100,3100,()=>{mono('06 / RECORD THE CONDITIONS',-570,-400,23,1,{v:.5});base(-580,-310,1160,570);panel(-350,-225,700,390,1,.7,30);L(ellipse(-350,-30,55,195),1,2,.7);L(ellipse(350,-30,55,195),1,2,.7);const u=eventProgress('archive',1.4);doc(-260,-160,520,180+100*u,1,.85);TX('三份情景记录',0,-85,43,1,{align:'center'});TX('依据 · 条件 · 可能路径',0,-15,32,1,{align:'center'});TX('待核查项，不是确定结论',0,55,30,show(67,.6),{align:'center'});gear(-470,190,24,5,u*TAU,1,.65,18);plaque('同一案件 · 保留差异',-540,330,1080,43);});}
function chassis(){R(130,130,7940,4460,1,.22,1.1);R(160,160,7880,4400,1,.08,.8);Object.values(paths).forEach(q=>rail(q));if(T>=76||Q.has('concept')){const u=Q.has('concept')?1:ease(p(T,76,78));TX('Risky 风险视角',400,460,190,u,{weight:700});TX('证据不变，假设改变。',400,590,85,u);TX('让研判有据，让行动有准备。',4100,4500,85,u,{align:'center'});}}
function captions(t){if(Q.has('concept'))return;const shot=plan.shots.find(s=>t>=s.start&&t<s.end)||plan.shots.at(-1),alpha=Math.min(ease(p(t,shot.start,shot.start+.45)),ease(p(shot.end-t,0,.35)));ov.save();ov.setTransform(scale,0,0,scale,0,0);ov.globalAlpha=alpha;const grad=ov.createLinearGradient(0,935,0,1080);grad.addColorStop(0,'rgba(5,16,26,0)');grad.addColorStop(1,'rgba(5,16,26,.94)');ov.fillStyle=grad;ov.fillRect(0,935,1920,145);ov.fillStyle='#eceee7';ov.font=`500 38px ${FONT}`;ov.textAlign='center';ov.fillText(shot.caption,960,1027);ov.fillStyle='#a2b4bb';ov.font=`20px ${FONT}`;ov.fillText(t>=40&&t<76?'合成案例 · 假设推演示意，非预测结果':'合成案例 A-001 · 流程示意',960,1062);ov.restore();}
function drawAt(t,captionTime=t){T=clamp(t/80)*80;bounds=[];const c=Q.has('concept')?{x:4100,y:2350,z:.225,r:0}:cameraAt(T);setCam({...c,z:c.z*scale});proj.k=.36;clear();NIBS.length=0;chassis();signal();relations();hall();snapshot();trials();recorder();trialCards();mainCase();captions(captionTime);compose(inkC,fxC,ovC,{sheet:[8200,4800],cam,seed:27});}
// Small shutter integration in export; the frame count remains the requested 30 fps.
const blendCanvas=document.createElement('canvas');blendCanvas.width=W;blendCanvas.height=H;const blend=blendCanvas.getContext('2d');
window.renderAt=(t,type='image/png',quality=.95)=>{const blur=Q.has('shutter')&&type==='image/jpeg';if(blur){blend.clearRect(0,0,W,H);for(let j=0;j<3;j++){drawAt(t+(j-1)/180,t);blend.globalAlpha=1/(j+1);blend.drawImage(canvas,0,0);}blend.globalAlpha=1;return blendCanvas.toDataURL(type,quality);}drawAt(t);return type?canvas.toDataURL(type,quality):null;};
window.stateAt=t=>{drawAt(t);const pt=casePosition(t),c=cameraAt(t);return{time:t,camera:c,caseWorld:pt,caseScreen:[960+(pt[0]-c.x)*c.z,540+(pt[1]-c.y)*c.z],buffer:[W,H],bounds};};window.cameraAt=cameraAt;window.cameraKeys=keys;window.casePosition=casePosition;window.__ready=true;drawAt(Q.has('concept')?60:0);
const audio=new Audio('./audio/mix.wav');let playing=false;const seek=document.querySelector('#seek'),button=document.querySelector('#play');seek.oninput=()=>{audio.currentTime=+seek.value;drawAt(+seek.value);};button.onclick=()=>{playing=!playing;if(playing){audio.currentTime=+seek.value;audio.play();}else audio.pause();};function tick(){if(playing){const t=Math.min(80,audio.currentTime);drawAt(t);seek.value=t;if(audio.ended||t>=80)playing=false;}requestAnimationFrame(tick);}if(!Q.has('render'))tick();
