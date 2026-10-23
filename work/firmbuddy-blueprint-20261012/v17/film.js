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
    const rot=o.rot||0;const corners=[[dx,-size*.95],[dx+width,-size*.95],[dx+width,size*.22],[dx,size*.22]].map(([a,b])=>S(ox+x+a*Math.cos(rot)-b*Math.sin(rot),oy+y+a*Math.sin(rot)+b*Math.cos(rot)));
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
function spec(x=-695,y=307,u=1){mono('DEMO /',x,y,18,u,{v:.55});TX('流程示例',x+100,y,27,u,{v:.7});}

// The opening uses world coordinates and the same blueprint ink/paper pipeline.
let filmTime=0;
function pen(ctx,color,width=1){ctx.strokeStyle=color;ctx.lineWidth=width;ctx.lineCap='round';ctx.lineJoin='round';}
function ot(ctx,s,x,y,size,color='#dbe9f1',align='left',weight=400){ctx.font=`${weight} ${size}px ${FONT}`;ctx.fillStyle=color;ctx.textAlign=align;ctx.fillText(s,x,y);if(ctx.globalAlpha>=.64&&size>=30){const w=ctx.measureText(s).width,dx=align==='center'?-w/2:align==='right'?-w:0,m=ctx.getTransform(),q=[[x+dx,y-size*.95],[x+dx+w,y-size*.95],[x+dx+w,y+size*.22],[x+dx,y+size*.22]].map(([a,b])=>[(m.a*a+m.c*b+m.e)/scale,(m.b*a+m.d*b+m.f)/scale]);bounds.push({text:s,id:s,box:[Math.min(...q.map(v=>v[0])),Math.min(...q.map(v=>v[1])),Math.max(...q.map(v=>v[0])),Math.max(...q.map(v=>v[1]))],size});}}
function ol(ctx,q,color='#a9c5da',width=1){pen(ctx,color,width);ctx.beginPath();q.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.stroke();}
function inkLayer(alpha,fn){if(alpha<.002)return;const v=visibility;g.save();g.globalAlpha*=alpha;visibility*=alpha;fn();visibility=v;g.restore();}
function openingPulse(q,start,end){const u=ease(p(filmTime,start,end));L(q,u,2.9,.92);if(u>0&&u<1){const z=pathPoint(q,u);C(...z,7,1,.95,2);}}
function bench(){
  panel(-918,-475,1836,918,1,.46,20);R(-902,-459,1804,884,1,.23,1);
  for(const x of[-888,888])for(const y of[-445,413]){bolt(x,y);C(x,y,13,1,.35,1);}
  truss(-918,481,918,481,14);L([[-918,443],[-918,512]],1,2,.4);L([[918,443],[918,512]],1,2,.4);
  for(let x=-830;x<880;x+=80)L([[x,425],[x,414]],1,1,.25);
  mono('FIRMBUDDY / CLIENT OPPORTUNITY WORKBENCH',-856,-422,20,1,{v:.48});
}
function painBay(x,y,id,title,line1,line2){
  R(x,y,802,293,1,.27,1.2);L([[x,y+47],[x+802,y+47]],1,1.3,.28);
  mono('0'+(id+1),x+19,y+34,23,1,{v:.6});TX(title,x+72,y+35,39,1);
  TX(line1,x+26,y+229,32,1,{v:.88});TX(line2,x+26,y+273,32,1,{v:.88});
  const t=filmTime;
  if(id===0){
    ['公告','解禁','名单'].forEach((s,i)=>{const xx=x+34+i*163,yy=y+80+(i===1?10:0);for(let k=2;k>=0;k--)doc(xx+k*7,yy-k*7,137,78,1,.4+k*.1);TX(s,xx+68,yy+49,30,1,{align:'center'});});
    L([[x+540,y+105],[x+735,y+105],[x+735,y+170],[x+540,y+170]],1,1.8,.6);pointer(x+735,y+105);pointer(x+540,y+170);
    const u=(Math.sin(t*1.6)+1)/2;doc(x+540+u*90,y+118,84,41,1,.9);detail(x+551+u*90,y+130,60,2);
  }
  if(id===1){
    C(x+110,y+123,41,1,.75,1.7);L([[x+110,y+89],[x+110,y+123],[x+132,y+136]],1,2,.9);
    L([[x+161,y+124],[x+255,y+124],[x+293,y+91],[x+707,y+91]],1,1.6,.5);L([[x+255,y+124],[x+293,y+157],[x+707,y+157]],1,1.6,.5);
    ['联系谁','何时联系'].forEach((s,i)=>{panel(x+372,y+66+i*66,236,53,1,.6,0);TX(s,x+490,y+104+i*66,31,1,{align:'center'});});
    const u=ease(p(t,3.6,5.2));L([[x+192,y+124],[x+268,y+124-21*u]],1,5,.95);C(x+192,y+124,9,1,.9,1.5);
  }
  if(id===2){
    ['企业背景','股东信息','行业位置'].forEach((s,i)=>{const xx=x+33+i*245;doc(xx,y+80,220,86,1,i===2?.35:.76);TX(s,xx+110,y+133,31,1,{align:'center',v:i===2?.5:.85});});
    L([[x+252,y+122],[x+278,y+122]],1,1.8,.55,'hidden');L([[x+497,y+122],[x+523,y+122]],1,1.8,.4,'hidden');
    L([[x+580,y+173],[x+650,y+173]],1,1.4,.45,'hidden');
  }
  if(id===3){
    ['行业判断','合规条件','经营策略'].forEach((s,i)=>{const xx=x+142+i*246;C(xx,y+109,25,1,.5,1.6);L([[xx-40,y+161],[xx-33,y+143],[xx+33,y+143],[xx+40,y+161]],1,1.8,.6);TX(s,xx,y+196,29,1,{align:'center',v:.75});});
    L([[x+182,y+125],[x+348,y+125]],1,1.4,.4,'hidden');L([[x+428,y+125],[x+594,y+125]],1,1.4,.4,'hidden');
  }
}
function painDraft(){
  const t=filmTime;TX('找到了线索，业务为什么仍难推进？',0,-344,49,1,{align:'center'});
  const a=1-.46*ease(p(t,8,9)),b=.3+.7*ease(p(t,7.6,8.4));
  inkLayer(a,()=>{painBay(-842,-284,0,'收集耗时：每天重复搜、筛、抄','公告与名单分散，同一事件反复出现','整理占去时间，真正研判迟迟未开始');painBay(40,-284,1,'切入不明：有信号，怎么跟？','公司解禁、股东动态只是起点','联系谁、何时谈、先谈什么，都要判断');});
  inkLayer(b,()=>{painBay(-842,53,2,'背景不全：客户资料拼不齐','企业、股东、行业信息难串成一条线','准备沟通时，仍缺关键背景与依据');painBay(40,53,3,'专业难找：一个问题跨多领域','行业、合规、客户经营需要共同研判','缺少专家协作，难形成清晰服务方案');});
  const y=t<8?23:366,u=ease(p(t,t<8?.4:8,t<8?1.2:8.8));L([[-840,y],[840,y]],u,3,.8);
  TX('把时间用在判断业务机会与服务客户上',0,400,31,ease(p(t,12.4,13)),{align:'center',v:.8});
}
function sourceDraft(){
  const t=filmTime;TX('商机查询：商机线索从哪里来？',0,-344,49,1,{align:'center'});
  ['市场扫描','客户定向','监控名单'].forEach((s,i)=>{const x=-590+i*590;plaque(s,x-240,-286,480,35,1);});
  [[-150,'公开公告','东方财富公告源'],[85,'解禁日历','结构化时间数据']].forEach(([y,s,desc],i)=>{
    doc(-815,y,425,176,1,.9);TX(s,-785,y+58,43,1);TX(desc,-785,y+119,31,1,{v:.8});mono('SOURCE / 0'+(i+1),-785,y+156,16,1,{v:.45});
    const q=[[-390,y+83],[-255,y+83],[-220,55],[-152,55]];L(q,1,1.4,.4);openingPulse(q,19.2+i*.8,20.4+i*.8);
  });
  gear(0,55,36,8,t*.17,1,.72,24);C(0,55,106,1,.6,1.8);
  panel(-105,-3,210,118,1,.85,0);TX('规则识别',0,42,38,1,{align:'center'});TX('事件分类',0,91,32,1,{align:'center',v:.8});
  const q=[[150,55],[260,55],[310,-85],[379,-85]];L(q,1,1.4,.4);openingPulse(q,21.2,22.4);
  [[-154,'公告事件','融资 · 并购等线索'],[66,'解禁窗口','股东服务线索']].forEach(([y,s,desc],i)=>{doc(380,y,425,168,1,.8);TX(s,414,y+57,38,ease(p(t,22+i*.8,22.4+i*.8)));TX(desc,414,y+116,32,ease(p(t,22.4+i*.8,22.8+i*.8)),{v:.8});});
  openingPulse([[260,55],[310,146],[379,146]],22.1,23.2);
  TX('来源留在卡上 · 按业务分类呈现',0,326,35,ease(p(t,23.2,24)),{align:'center'});
  TX('规则筛选线索，AI 辅助解读与后续研判',0,389,32,ease(p(t,24,24.6)),{align:'center',v:.82});
}
const scenarioSources=[['再融资','融资预案','投行业务'],['并购重组','并购公告','投行业务'],['股东服务','解禁日历','财富业务'],['风险管理','套保公告','机构业务'],['股份回购','回购预案','财富业务']];
function blueprintCard(i,cx,cy,w,h,rot=0,morph=0,alpha=1){
  if(alpha<.01)return;
  at(cx,cy,()=>inkLayer(alpha,()=>{
    const tr=([x,y])=>[x*Math.cos(rot)-y*Math.sin(rot),x*Math.sin(rot)+y*Math.cos(rot)];
    const q=[[-w/2,-h/2],[w/2-24,-h/2],[w/2,-h/2+24],[w/2,h/2],[-w/2,h/2],[-w/2,-h/2]].map(tr);
    solid(pts(q),{u:1,v:.96*visibility,w:2.4,th:12*(1-morph)});L([[-w/2+10,-h/2+14],[-w/2+10,h/2-14],[w/2-10,h/2-14]].map(tr),1,1,.3);
    const label=(s,x,y,size,v=1)=>{const a=tr([x,y]);TX(s,...a,size,1,{align:'center',rot,v});};
    inkLayer(1-ease(p(morph,0,.45)),()=>{
      mono('0'+(i+1),...tr([-w/2+28,-h/2+39]),21,1,{rot,v:.48});const a=scenarioSources[i];label(a[2],0,-h/2+87,29,.72);label(a[0],0,-h/2+161,43);
      L([[-w/2+23,-h/2+189],[w/2-23,-h/2+189]].map(tr),1,1.1,.48);label('来源',0,-h/2+239,27,.66);label(a[1],0,-h/2+286,33);label(i===2?'公司级线索':'业务事件线索',0,h/2-37,27,.68);
    });
    inkLayer(ease(p(morph,.42,.9)),()=>{C(...tr([-w/2+16,-h/2+17]),5,1,.7,1);label('示例客户信息',0,15,34);});
  }));
}
function cardsDraft(){
  const t=filmTime,opening=ease(p(t,27.4,28.6)),extract=ease(p(t,32,33.2)),travel=ease(p(t,35.2,38));
  inkLayer(1-ease(p(t,35,36)),()=>at(...centers.intro,()=>{
    TX('商机查询 · 从业务场景抽出一条线索',0,-344,48,1,{align:'center'});TX('每张卡片，都带着可追溯的公告或日历来源',0,-274,31,1,{align:'center',v:.8});
    L(ellipse(0,347,859,128,Math.PI,TAU),1,1.3,.42);shaft([[-850,390],[850,390]],1,.45);for(let x=-800;x<=800;x+=100)C(x,390,8,1,.4,1.3);
  }));
  for(const i of[0,4,1,3]){const d=i-2;blueprintCard(i,mix(1642,1050+d*342,opening),mix(1215,1070+56+Math.abs(d)*29,opening),306,390,d*.025*opening,0,opening*(1-ease(p(t,34.8,36))));}
  const q=[[-110,-73],[510,-73],...paths.query.slice(1).map(([x,y])=>[x-1050,y-1070])],v=pathPoint(q,ease(p(T,1.2,5.8))),target=[v[0]+1050,v[1]+1070];
  blueprintCard(2,mix(mix(1642,1050,opening),target[0],travel),mix(mix(1215,1126-100*extract,opening),target[1],travel),mix(326,270,travel),mix(420,104,travel),0,travel,opening);
  if(t>=32&&t<35.6)inkLayer(ease(p(t,32,32.4))*(1-ease(p(t,35,35.6))),()=>at(...centers.intro,()=>{
    TX('A01 · 示例客户信息｜半导体衬底企业',0,346,33,1,{align:'center'});TX('以解禁线索切入，开展减持商机研判',0,403,32,1,{align:'center',v:.85});
  }));
}
function opening(){
  if(filmTime>=38)return;
  at(...centers.intro,()=>{inkLayer(1-ease(p(filmTime,35,36.8)),()=>bench());inkLayer(1-ease(p(filmTime,16.4,18)),()=>painDraft());inkLayer(ease(p(filmTime,17.4,18.4))*(1-ease(p(filmTime,26.7,28))),()=>sourceDraft());});
  if(filmTime>=27.4)cardsDraft();
}
function businessNarrative(t){const q=plan.business_messages.find(q=>t>=q.start&&t<q.end);if(!q)return;
  const a=ease(p(t,q.start,q.start+.32))*(1-ease(p(t,q.end-.32,q.end))),ctx=ov;
  ctx.save();ctx.scale(scale,scale);ctx.globalAlpha=a;ctx.fillStyle='rgb(5,23,42)';ctx.fillRect(0,0,1920,105);
  ol(ctx,[[96,108],[1824,108]],'rgba(165,197,218,.43)',1);ot(ctx,q.pain,960,74,36,'#d7e8f3','center',500);
  const z=ctx.createLinearGradient(0,987,0,1080);z.addColorStop(0,'rgba(5,23,42,0)');z.addColorStop(.45,'rgba(5,23,42,.94)');z.addColorStop(1,'rgba(5,23,42,.94)');ctx.fillStyle=z;ctx.fillRect(0,987,1920,93);ot(ctx,q.result,960,1044,34,'#e0ecf4','center');ctx.restore();
}

// V6 original world geometry. Every stage occupies this one persistent sheet.
const centers={intro:[1050,1070],signals:[2800,1200],experts:[5600,1450],knowledge:[3600,2880],visit:[6200,2980],follow:[7460,3130]};
const domains=['投行业务','机构业务','财富业务','资管业务','国际业务','投资业务','期货与衍生品','行业研究','综合专家'];
const ellipse=(x,y,rx,ry,a0=0,a1=TAU,n=100)=>Array.from({length:n+1},(_,i)=>{const a=mix(a0,a1,i/n);return[x+rx*Math.cos(a),y+ry*Math.sin(a)]});
function bez(a,b,c,d,n=80){return Array.from({length:n+1},(_,i)=>{const u=i/n,v=1-u;return[v*v*v*a[0]+3*v*v*u*b[0]+3*v*u*u*c[0]+u*u*u*d[0],v*v*v*a[1]+3*v*v*u*b[1]+3*v*u*u*c[1]+u*u*u*d[1]]});}
const paths={
 query:bez([1560,997],[2010,997],[2070,1250],[2408,1250]),
 bypass:bez([1560,1167],[2750,1610],[3720,1800],[4540,1610]),
 toHall:bez([3500,1250],[3860,1250],[4210,1570],[4590,1570]),
 knowledge:bez([5260,1890],[5200,2270],[4680,2450],[4220,2700]),
 output:bez([4320,3020],[4900,3000],[4930,3020],[5560,3020]),
 task:bez([6880,3070],[7080,3070],[7130,3140],[7240,3140]),
 feedback:bez([7780,3220],[8050,3220],[8050,3750],[7520,3780]).concat(bez([7520,3780],[6400,3800],[3600,3800],[1020,3800]).slice(1)).concat(bez([1020,3800],[460,3800],[460,3270],[460,3030]).slice(1)).concat(bez([460,3030],[460,2310],[470,1320],[660,1080]).slice(1))
};
// Quintic Hermite with shared endpoint derivatives and zero acceleration: C2 joins.
// Nonzero velocities on travel waypoints; only explicit reading windows stop the camera.
const keys=[
 [0,1050,1070,.95,0],[2.9,1050,1070,.95,0],
 [4.8,2000,1140,.94,-.025,600,45,-.015,-.003],
 [6,2800,1200,1.05,0],[8.25,2800,1200,1.05,0],
 [10.4,4070,1370,.84,.02,900,100,-.16,0],
 [12,5600,1390,.70,0],[16.1,5600,1390,.70,0],
 [17.8,5390,1810,.91,-.025,-390,450,.07,0],
 [19.6,4340,2580,.88,-.018,-480,300,-.035,.015],
 [21,3650,2830,.94,0],[25.6,3650,2830,.94,0],
 [27.4,4760,2950,1.0,.022,750,70,.035,0],
 [29.3,6200,2950,.94,0],[34.7,6200,2950,.94,0],
 [36.6,7130,3100,1.0,-.02,460,65,.04,0],
 [38,7260,3150,1.06,0],[40.1,7260,3150,1.06,0],
 [42.6,6940,3560,.82,.035,-450,260,-.24,0],
 [44.3,5900,3710,.54,.01,-650,-150,-.35,-.02],
 [47.5,4900,2480,.18,0],[48.4,4900,2480,.18,0],
 [50.4,4900,2510,.185,0],[52,4900,2510,.185,0]
];
function quint(a,b,va,vb,h,u){const d=b-a,A=va*h,B=vb*h;return a+A*u+(10*d-6*A-4*B)*u**3+(-15*d+8*A+7*B)*u**4+(6*d-3*A-3*B)*u**5;}
function cameraAt(t){let i=1;while(i<keys.length-1&&t>keys[i][0])i++;const a=keys[i-1],b=keys[i],h=b[0]-a[0],u=p(t,a[0],b[0]);const c={};for(const [j,k]of['x','y','z','r'].entries()){const v=j===2?Math.log(a[j+1]):a[j+1],w=j===2?Math.log(b[j+1]):b[j+1];c[k]=quint(v,w,a[j+5]||0,b[j+5]||0,h,u);if(j===2)c[k]=Math.exp(c[k]);}return c;}
function pathPoint(q,u){if(u<=0)return q[0];if(u>=1)return q.at(-1);return trunc(q,u)[1];}
function feedbackProgress(t){const k=[[40.3,0,0],[42.6,.05,.07],[44.3,.28,.17],[49.2,1,0]];if(t<=40.3)return 0;if(t>=49.2)return 1;let i=1;while(t>k[i][0])i++;const a=k[i-1],b=k[i];return clamp(quint(a[1],b[1],a[2],b[2],b[0]-a[0],p(t,a[0],b[0])));}
function carrier(q,u,label='',w=196){const [x,y]=pathPoint(q,u);at(x+ox,y+oy,()=>{doc(-w/2,-52,w,104,1);C(-w/2+16,-35,5,1,.75,1);if(label)TX(label,0,15,34,1,{align:'center'});else detail(-w/2+32,-13,w-56,3);});return[x,y];}
function rail(q,v=.46){
 L(q.map(([x,y])=>[x,y-24]),1,2.3,v);L(q.map(([x,y])=>[x,y+24]),1,2.3,v);L(q.map(([x,y])=>[x,y+45]),1,1.2,v*.7);L(q,1,1,v*.5,'center');
 let acc=0,next=0;for(let i=1;i<q.length;i++){const a=q[i-1],b=q[i],len=Math.hypot(b[0]-a[0],b[1]-a[1]);while(next<=acc+len){const u=(next-acc)/(len||1),x=mix(a[0],b[0],u),y=mix(a[1],b[1],u);C(x,y,7,1,v,1.3);if(Math.round(next/90)%4===0){R(x-16,y-33,32,88,1,v,1.2);L([[x,y+55],[x,y+120]],1,1.5,v*.6);R(x-28,y+120,56,12,1,v*.6,1);}next+=90;}acc+=len;}
}
function plaque(s,x,y,w,size=42,u=1){const h=Math.max(80,size*1.65);panel(x,y,w,h,u,.9,8);R(x+7,y+7,w-14,h-14,u,.4,1);for(const a of[x+12,x+w-12]){C(a,y+12,3,u,.8,1);C(a,y+h-12,3,u,.8,1);}TX(s,x+w/2,y+h*.7,size,u,{align:'center'});}
function pointer(x,y){L([[x-18,y-8],[x,y],[x-18,y+8]],1,1.6,.55);}
function movingRoute(q,start,end){route(q,start,end,3.5,.95);if(T>=start&&T<=end)carrier(q,ease(p(T,start,end)),'',146);}
function frameBase(x,y,w,h){R(x,y,w,h,1,.42,1.7);truss(x,y+h+32,x+w,y+h+32,Math.max(4,Math.round(w/130)));for(const xx of[x,x+w]){L([[xx,y+h],[xx,y+h+120]],1,2,.48);panel(xx-40,y+h+115,80,24,1,.4,10);bolt(xx-24,y+h+126);bolt(xx+24,y+h+126);}}
function intro(){at(...centers.intro,()=>{
 mono('FIRMBUDDY / CLIENT OPERATIONS',-670,-378,24,1,{v:.6});TX('找到这家客户的业务切入点',-670,-300,50,1);
 const labels=['商机查询','业务问题答疑','客户拜访准备'];
 labels.forEach((s,i)=>{const y=-133+i*170,u=show(.2+i*.16);plaque(s,-650,y-53,300,39,u);solid(pts([[-316,y-47],[-230,y-47],[-249,y+2],[-296,y+2]]),{u,v:.7,w:2,th:12});gear(-267,y+60,18,4,T*.8,u,.65,12);shaft([[-217,y+60],[510,y+60]],u,.55);for(let j=0;j<6;j++)C(-140+j*107,y+60,6,u,.5,1);bearing(120,y+60,u);pointer(456,y+60);});
 TX('AI 辅助识别问题、调用工具',-650,387,35,show(1),{v:.85});
 if(T<5.8){const priorVisibility=visibility;visibility*=filmTime>=38?1:0;const u=ease(p(T,1.2,5.8));carrier([[-110,-73],[510,-73],...paths.query.slice(1).map(([x,y])=>[x-1050,y-1070])],u,'示例客户信息',270);visibility=priorVisibility;}
 });}
function sourceStation(){at(...centers.signals,()=>{
 TX('资料归集：先看清同一家客户',-730,-335,46,1);mono('01 / DISCOVER · CONNECT · FILTER',-730,-390,22,1,{v:.5});
 frameBase(-685,-245,1380,475);rail([[-720,220],[700,220]],.42);
 const sources=['公司公告','股东动态','解禁信息'];
 sources.forEach((label,i)=>{const u=ease(p(T,6.1+i*.2,7+i*.2)),x=mix(-658,145,u),y=mix(-180+i*134,-80,u),v=1-ease(p(u,.6,1));
   panel(-658,-180+i*134,382,96,1,.28,12);TX(label,-628,-116+i*134,36,1,{v:.48});
   route([[-258,-132+i*134],[-65,-132+i*134],[95,-80],[145,-80]],6.1+i*.2,7+i*.2,2.5,.65);
   if(v>.01){const prior=visibility;visibility*=v;doc(x,y,382,96,1);TX(label,x+30,y+64,36,1);visibility=prior;}
 });
 gear(-460,225,24,6,T*.7,1,.6,18);gear(-310,225,26,6,meshAngle(T*.7,24,26,[-460,225],[-310,225]),1,.55,18);
 doc(145,-208,517,393,1,.85);TX('A01 · 示例半导体企业',175,-158,28,1,{v:.7});
 TX('股东服务线索',175,-81,46,show(6.5));L([[175,-43],[620,-43]],show(6.6),1.4,.5);
 TX('主体 · 事件 · 时间',175,22,38,show(6.7));TX('原文依据 · 来源可追溯',175,87,32,show(6.9));
 TX('AI 辅助解读客户线索',175,147,32,show(7.1));
 });if(T>8.4&&T<11.7)movingRoute(paths.toHall,8.4,11.7);}
// Reference translation: tiered curved desks, seated specialists, nameplates and brand backdrop.
function expertFigure(x,y,s=1,active=0){
  const q=v=>v.map(([a,b])=>[x+a*s,y+b*s]);
  panel(x-20*s,y-12*s,40*s,49*s,1,.35,8*s);
  C(x,y-35*s,14*s,1,.9,1.6);L(q([[-5,-22],[-5,-14],[5,-14],[5,-22]]),1,1.1,.7);
  solid(pts(q([[-12,-15],[-25,-6],[-31,27],[-11,34],[14,34],[29,22],[22,-5],[11,-15]])),{u:1,w:1.7,v:.8*visibility,th:4*s});
  L(q([[-11,-13],[0,5],[11,-13]]),1,1.2,.95);L(q([[0,5],[-4,21],[0,28],[4,21],[0,5]]),1,1.1,.7);
  L(q([[-18,-3],[-21,13],[-6,22]]),1,1.8,.85);
  L(q([[18,-3],[24,12-14*active],[40,18-36*active]]),1,2,.95);C(x+40*s,y+(18-36*active)*s,3*s,1,.85,1.1);
  L(q([[-30,34],[30,34]]),1,1.4,.6);
}
const hallSeatNames=[
 ['企业洞察','客户洞察','财务质量','财务诊断','合规风险','信披合规','舆情监控','企业画像','文档识别','PDF文档','报告编排'],
 ['客户方案','话术策略','商机诊断','客户经营','经营韧性','销售陪练','产业授信','财务查询','跨境经营','协同推送'],
 ['产业链研判','半导体研究','工业母机','智能传感器','具身智能','商业航天','低空经济','固态电池','合成生物'],
 ['产业资本','并购整合','资本运作','股份回购','股权激励','股票质押','企业理财','风险对冲'],
 ['量子计算','边界扫描','半导体调压阀','痕量分析','分子筛脱氯','反渗透净水','企业家规划']
];
function experts(){at(...centers.experts,()=>{
  TX('专业会商：这家客户应该怎样跟进？',0,-630,55,1,{align:'center'});
  TX('知识装备、业务方法与培养试炼，支撑专业判断',0,-566,36,1,{align:'center',v:.8});
  domains.forEach((s,i)=>{const x=i<5?-880+i*440:-855+(i-5)*570,y=i<5?-496:-434;TX(s,x,y,44,1,{align:'center',v:.88});});
  panel(-280,-403,560,92,1,.65,12);TX('FirmBuddy',0,-339,59,1,{align:'center',font:'Georgia'});
  for(const x of[-335,335]){L([[x,-400],[x,-300]],1,3,.6);L([[x+10,-400],[x+10,-300]],1,1,.4);}
  for(let row=0;row<5;row++){
    const rx=1140-row*120,ry=370-row*40,cy=100+row*40,names=hallSeatNames[row];
    const arc=ellipse(0,cy,rx,ry,Math.PI+.045,TAU-.045,90),front=arc.map(([x,y])=>[x,y+43]);
    names.forEach((s,j)=>{const a=Math.PI+.14+j*(Math.PI-.28)/(names.length-1),x=Math.cos(a)*(rx-10),y=cy+Math.sin(a)*(ry-12);expertFigure(x,y-30,.69,0);});
    const wall=[...arc,...front.slice().reverse()];solid(pts(wall),{u:1,w:2,v:.65,th:8});L(arc,1,2.4,.85);L(front,1,1.4,.5);
    for(let j=0;j<12;j++){const a=Math.PI+.07+j*(Math.PI-.14)/11,x=Math.cos(a)*rx,y=cy+Math.sin(a)*ry;L([[x,y+43],[x,y+61]],1,1,.3);}
    names.forEach((s,j)=>{const a=Math.PI+.14+j*(Math.PI-.28)/(names.length-1),x=Math.cos(a)*(rx-10),y=cy+Math.sin(a)*(ry-12);panel(x-76,y+5,152,35,1,.65,0);TX(s,x,y+30,21,1,{align:'center',v:.82});});
  }
  // Three foreground specialists visibly turn the same customer file into a shared assessment.
  const chosen=[[-730,185,'股东增减持专家','股份管理需求'],[0,210,'解禁预警专家','联系时机'],[730,185,'拜访策略专家','服务切入点']];
  const tt=filmTime-20;
  chosen.forEach(([x,y,name,role],i)=>{
    const u=ease(p(tt,50.4+i*1.2,50.8+i*1.2));
    const gesture=(.4+.6*Math.sin(Math.PI*p(tt,50.4+i*1.2,54+i*1.2)))*u;
    expertFigure(x,y-47,1.45,gesture);
    panel(x-255,y-12,510,95,1,.8,16);L([[x-235,y+8],[x+235,y+8]],1,1.1,.45);
    TX(name,x,y+54,44,1,{align:'center'});
    TX(role,x,y+118,39,u,{align:'center',v:.85});
    const path=[[x,y+130],[x,y+155],[x*.55,335],[0,355]];
    const z=ease(p(tt,52+i*.5,54+i*.5));L(path,z,2.7,.83);
  });
  const result=ease(p(tt,55,55.6));
  doc(-440,356,880,112,1);TX('A01 · 股东服务研判',0,405,43,1,{align:'center'});TX('结合客户背景，形成服务思路',0,450,34,result,{align:'center',v:.85});
  ['专业知识装备','业务方法沉淀','培养与试炼'].forEach((s,i)=>{const x=-1100+i*750;plaque(s,x,495,700,43,1);});
  for(const x of[-1155,1155]){L([[x,60],[x,540]],1,2.4,.5);panel(x-42,536,84,24,1,.55,12);bolt(x-25,547);bolt(x+25,547);}
});}

function cabinet(x,y,s,i){
 panel(x,y,204,350,1,.68,32);R(x+13,y+15,178,315,1,.4,1.3);
 for(let j=0;j<5;j++){panel(x+22,y+36+j*53,160,43,1,.55,8);R(x+76,y+48+j*53,53,12,1,.45,1);for(let k=0;k<4;k++)L([[x+31+k*7,y+44+j*53],[x+31+k*7,y+67+j*53]],1,1,.25);}
 TX(s,x+102,y-30,33,1,{align:'center',v:.85});mono(String(i+1).padStart(2,'0'),x+101,y+391,21,1,{align:'center',v:.45});
}
function knowledge(){at(...centers.knowledge,()=>{
 TX('回到同一客户：把依据带入服务判断',-730,-359,48,1);mono('02 / EVIDENCE · SECTION A–A',-730,-410,21,1,{v:.5});
 frameBase(-728,-224,1438,397);
 ['核心规范','监管规则','产品能力','案例经验','研究资料','补充资料'].forEach((s,i)=>cabinet(-714+i*238,-190,s,i));
 const cut=mix(-740,740,ease(p(T,19.9,21.4)));
 if(T<21.4){panel(Math.max(-728,cut),-224,710-Math.max(-728,cut),397,1,.5,16);if(cut<0){TX('专业装配 / 按需检索',-460,5,44,1);}}
 if(T>=19.9&&T<21.4){L([[cut,-256],[cut,210]],1,2.7,.95,'phantom');TX('A',cut-20,-275,28);}
 const u=ease(p(T,21.4,22.5));
 if(u>0){
   const x=mix(-693,-593,u),y=mix(-153,-162,u),ww=mix(160,623,u),hh=mix(120,303,u);
   L([[-616,-148],[x+ww/2,y+hh]],1,1.3,.4,'hidden');
   for(let i=2;i>0;i--)doc(x+i*13,y-i*12,ww,hh,1,.4);doc(x,y,ww,hh,1);
   TX('A01 · 研究与规则依据',x+28,y+65,39,show(22.2));L([[x+28,y+90],[x+ww-28,y+90]],show(22.3),1,.45);
   TX('规则 · 案例 · 研究依据',x+28,y+164,45,show(22.5));TX('AI 辅助检索与交叉查证',x+28,y+229,30,show(22.7),{v:.75});
 }
 if(T>=23.1){panel(129,-109,559,222,show(23.1),1,10);TX('明确客户服务方向',156,-45,39,show(23.2));TX('了解股份管理安排',156,25,43,show(23.4));TX('服务方向：股份管理',156,77,30,show(23.5),{v:.75});route([[33,-10],[128,-10]],22.8,23.4,3);}
 TX('专业培养的专家团 · 多源知识库 · 可追溯依据',-730,365,34,1,{v:.8});
 });if(T>=25.8&&T<=29.1)movingRoute(paths.output,25.8,29.1);}
function visit(){at(...centers.visit,()=>{
 TX('少做重复准备，多花精力服务客户',-730,-379,49,1);mono('03 / OUTPUT CARRIAGE',-730,-432,21,1,{v:.5});
 frameBase(-734,-251,1458,510);shaft([[-721,-184],[720,-184]],1,.6);
 for(let x=-700;x<700;x+=29)L([[x,-199],[x+17,-169]],1,1.2,.4);bearing(-701,-184);bearing(700,-184);
 doc(-50,-123,738,328,1);TX('A01 · 客户沟通准备包',-12,-65,43,1);L([[-12,-40],[645,-40]],1,1.2,.5);
 ['拜访资料','沟通重点','后续安排'].forEach((label,i)=>{const z=ease(p(T,29.5+i*.25,31.1+i*.25)),v=1-ease(p(z,.65,1));if(v>.01){const prior=visibility;visibility*=v;const xx=mix(-707,-50,z),yy=mix(-110+i*92,-20,z);doc(xx,yy,430,72,1);TX(label,xx+28,yy+49,34,1);visibility=prior;}});
 const x=mix(-492,243,ease(p(T,29.4,31.2))),u=1-ease(p(T,31.1,31.6));
 panel(x-100,-218,200,67,1,.6,16);bolt(x-76,-195);bolt(x+76,-195);L([[x,-151],[x,-32]],1,2,.5);
 if(u>.01){panel(x-245,-22,490,85,1,u);TX('形成客户沟通准备',x,35,41,1,{align:'center',v:u});}
 TX('联系目的：了解股份管理安排',-12,35,36,show(31.2));TX('结合产业背景，准备沟通问题',-12,116,33,show(31.8));TX('AI 辅助整理材料与跟进建议',-12,173,32,show(32.2),{v:.8});
 gear(-530,134,26,7,T*.45,1,.68,24);gear(-376,134,18,7,meshAngle(T*.45,26,18,[-530,134],[-376,134]),1,.6,20);
 ['研判有结论','沟通有重点','跟进有计划'].forEach((s,i)=>plaque(s,-734+i*498,286,468,39,show(32.8+i*.2)));
 TX('按需生成',-730,267,25,show(32.8),{v:.7});
 },mix(1,.18,ease(p(T,35,37))*(1-ease(p(T,43.8,45)))));if(T>=35&&T<=37.5)movingRoute(paths.task,35,37.5);}
function follow(){if(T<35)return;at(...centers.follow,()=>{
 TX('保留经营记录，后续跟进接得上',-450,-300,49,1);mono('04 / CONFIRM · FOLLOW THROUGH',-450,-353,21,1,{v:.5});
 // Human confirmation admits a candidate to follow-up; it does not confirm a reduction intention.
 plaque('人工审核',-580,-152,375,42,1);gear(-145,-21,24,6,T*.25,1,.67,20);
 const a=mix(-1.08,0,ease(p(T,37.4,37.9)));L([[-145,-21],[-145+Math.cos(a)*150,-21+Math.sin(a)*150]],1,7,.9);C(-145+Math.cos(a)*150,-21+Math.sin(a)*150,17,1,.95,2.5);
 shaft([[12,-21],[220,-21]],1,.6);
 if(T>=37.9){C(63,-21,29,show(37.9));L([[46,-22],[60,-6],[83,-40]],show(37.9),3.5);}
 doc(173,-162,466,240,show(38));TX('A01 · 沟通记录',205,-85,38,show(38.1));TX('沟通需求 · 服务安排',205,-14,33,show(38.3));TX('跟进事项 · 经营进展',205,39,31,show(38.4),{v:.8});
 doc(-563,162,1202,129,show(39));TX('沟通记录支持持续跟进',-528,241,43,show(39.2));
 TX('AI 辅助梳理记录，支持后续研判',-563,350,31,show(39.4),{v:.8});
 });if(T>=40.3&&T<=49.2){const u=feedbackProgress(T);carrier(paths.feedback,u,'跟进记录',245);L(trunc(paths.feedback,u)[0],1,3.1,.8);}}
function chassis(){at(0,0,()=>{
 R(115,115,9570,4570,1,.26,1.4);R(150,150,9500,4500,1,.13,1);
 for(let x=400;x<9600;x+=400){L([[x,115],[x,150]],1,1,.3);mono(String(x/400),x+10,188,23,1,{v:.35});}
 for(let y=400;y<4600;y+=400){L([[115,y],[150,y]],1,1,.3);mono(String.fromCharCode(64+y/400),164,y+10,23,1,{v:.35});}
 for(let x=320;x<9650;x+=240)for(let y=280;y<4550;y+=240){L([[x-9,y],[x+9,y]],1,.8,.105);L([[x,y-9],[x,y+9]],1,.8,.105);}
 // The support network exists from frame zero, so new regions are discovered, not replaced.
 for(const q of Object.values(paths))rail(q,.4);
 rail(bez([1560,1337],[2800,1960],[3870,1970],[4700,1770]),.3);
 for(const [x,y,n]of[[2150,940,18],[3900,1370,24],[4850,2390,22],[4860,3020,20],[7870,3570,28],[675,3670,32]]){gear(x,y,n,5,T*.28,1,.4,14);}
 if(T>44){
   const u=show(44,.7);plaque('问题入口',880,470,1120,127,u);plaque('线索归集',2450,660,1140,127,u);
   plaque('专业研判',5130,325,1240,136,u);plaque('产业研究',7750,610,1260,136,u);plaque('知识依据',3050,2240,1250,144,u);
   plaque('跟进准备',5600,2370,1400,142,u);plaque('持续经营',3390,3890,1350,136,u);
 }
 // Same-sheet title block. No sudden brand push and no lifecycle grid.
 const u=show(46,.8);if(u>0){panel(1240,4180,6660,390,u,.9,0);R(1270,4210,6600,330,u,.4,1);L([[3260,4210],[3260,4540]],u,2,.5);TX('FirmBuddy',1420,4423,271,u,{font:'Georgia',weight:700});TX('让商机有线索，研判有依据，跟进有准备',3480,4375,141,u);TX('把时间用在理解客户、匹配服务与推进合作',3480,4490,94,u,{v:.75});}
 });}

// One case, one continuous blueprint. Original drawing helpers and apparatus are retained.
const clockKnots=[[0,0],[9,3.5],[10,4.3],[13.2,6.4],[15.2,8],[18,11]];
function linearClock(t,k){if(t<=k[0][0])return k[0][1];for(let i=1;i<k.length;i++)if(t<=k[i][0])return mix(k[i-1][1],k[i][1],p(t,k[i-1][0],k[i][0]));return k.at(-1)[1];}
function openingClock(t){return linearClock(t,clockKnots);}
const storyClock=[[0,0],[15.2,0],[18,2.9],[28,7.3],[32,8.25],[46,8.25],[50,12],[60,16.1],[73.2,16.1],[76,21],[83,25.6],[87,29.3],[92,34.7],[94,38],[96,40.1],[104,52]];
function originalTime(t){if(t>=35.2&&t<38)return quint(0,2.9,0,.44,2.8,p(t,35.2,38));return linearClock(t-20,storyClock);}
const industryCenter=[8350,1510];
const industryIn=bez([5866,1815],[6590,1815],[6980,1940],[7390,1940]);
const industryOut=bez([9310,1940],[9650,2350],[5070,2250],[4220,2700]);
const detourKeys=[[60,5600,1390,.70,0],[63.2,7230,1470,.64,-.015,930,45,.04,0],[65.2,8350,1510,.67,0],[72.8,8350,1510,.67,0],[74.6,6450,2230,.60,.016,-2350,300,-.08,0],[76,3650,2830,.94,0]];
function sampleKeys(t,kk){let i=1;while(i<kk.length-1&&t>kk[i][0])i++;const a=kk[i-1],b=kk[i],h=b[0]-a[0],u=p(t,a[0],b[0]),c={};for(const[j,k]of['x','y','z','r'].entries()){let v=j===2?Math.log(a[j+1]):a[j+1],w=j===2?Math.log(b[j+1]):b[j+1];c[k]=quint(v,w,a[j+5]||0,b[j+5]||0,h,u);if(j===2)c[k]=Math.exp(c[k]);}return c;}
const openingKeys=[[0,1050,1105,.94,-.006],[7.4,1050,1105,.96,0],[9.2,1050,1105,.96,0],[16.4,1050,1105,.95,0],[18.4,1050,1070,.95,0],[27.4,1050,1070,.95,0],[32,1050,1070,.95,0],[35.2,1050,1070,.95,0],[38,1050,1070,.95,0]];
function storyCamera(t){if(t<=38)return sampleKeys(t,openingKeys);const old=t-20;return old>=60&&old<=76?sampleKeys(old,detourKeys):cameraAt(originalTime(t));}
function liveRoute(q,a,b,v=.9){const u=ease(p(filmTime-20,a,b));L(q,u,3,v);if(u>0&&u<1){const z=pathPoint(q,u);C(...z,8,1,.95,2);}}

function judgment(){at(...centers.signals,()=>{
 const t=filmTime-20;
 TX('业务研判：这条线索，怎样跟进？',-730,-335,47,1);
 mono('A01 / SHAREHOLDER SERVICE ASSESSMENT',-730,-390,22,1,{v:.55});
 frameBase(-685,-245,1380,475);rail([[-720,220],[700,220]],.42);
 const items=[['关注信号','公司解禁窗口'],['核对主体','公司 · 股东资料'],['明确切入','股份管理安排']];
 items.forEach(([a,b],i)=>{const u=ease(p(t,32.5+i*1.4,33.2+i*1.4)),x=-650+i*450;
   panel(x,-205,420,155,u,.9,14);mono('0'+(i+1),x+20,-164,22,u,{v:.6});TX(a,x+210,-150,37,u,{align:'center'});TX(b,x+210,-88,33,u,{align:'center'});
   liveRoute([[x+210,-47],[x+210,4],[15,4],[15,48]],35.8+i*.5,37.5+i*.5,.8);
 });
 const u=ease(p(t,38.8,39.5));doc(-620,47,1240,143,u);TX('跟进重点：了解股份事务接口与服务需求',0,104,39,u,{align:'center'});
 TX('AI 辅助整理关注理由、业务条件与沟通问题',0,161,31,u,{align:'center',v:.82});
 gear(-460,225,24,6,t*.38,1,.6,18);gear(-310,225,26,6,meshAngle(t*.38,24,26,[-460,225],[-310,225]),1,.55,18);
 TX('A01 · 示例客户信息 · 半导体企业',-650,345,35,1,{v:.9});
 });}
function signals(){
 const k=ease(p(filmTime-20,31.7,32.5));
 if(k<1){const old=visibility;visibility*=1-k;sourceStation();visibility=old;}
 if(k>0){const old=visibility;visibility*=k;judgment();visibility=old;}
 if(T>8.4&&T<11.7)movingRoute(paths.toHall,8.4,11.7);
}

function industry(){at(...industryCenter,()=>{
 const t=filmTime-20;
 frameBase(-1050,-520,2100,1050);
 TX('产业研判：更懂眼前这家客户',0,-595,60,1,{align:'center'});
 TX('A01 · 示例客户信息｜半导体衬底企业（流程示意）',0,-545,34,1,{align:'center',v:.85});
 // A drafting screen grows from the same table, not a screenshot plane.
 panel(-996,-463,1992,600,1,.72,14);
 mono('INDUSTRY ATLAS / EVIDENCE-BASED RESEARCH',-958,-421,22,1,{v:.5});
 const nodes=[[-770,-240,'材料耗材'],[-770,0,'制造装备'],[-300,-140,'晶体生长'],[210,-140,'衬底'],[710,-140,'外延']];
 const links=[[0,2],[1,2],[2,3],[3,4]];
 links.forEach(([a,b],i)=>{const A=nodes[a],B=nodes[b],q=bez([A[0]+56,A[1]],[A[0]+190,A[1]],[B[0]-190,B[1]],[B[0]-58,B[1]],36);L(q,1,1.8,.25);liveRoute(q,63.8+i*.45,64.7+i*.45,.92);});
 nodes.forEach(([x,y,label],i)=>{const u=ease(p(t,63.4+i*.25,64.2+i*.25));C(x,y,61,1,.35,1.5);C(x,y,53,u,.95,2.7);mono('0'+(i+1),x,y+10,29,u,{align:'center'});TX(label,x,y+106,46,u,{align:'center'});});
 // The case marker lands on the customer's explicit illustrative substrate position.
 const marked=ease(p(t,65.4,66.4));
 if(marked>0){const x=mix(-860,210,marked),y=mix(394,-274,marked);doc(x-220,y-40,440,90,1);TX('A01 · 本次客户',x,y+19,46,1,{align:'center'});L([[x,y+50],[210,-215]],marked,2.3,.9);C(210,-140,75,marked,.9,2);}
 const eu=ease(p(t,67.2,68));
 const sources=[['公司年报','产业位置与业务结构'],['专利原文','技术路线与证据'],['财务披露','经营背景与阶段']];
 sources.forEach(([s,d],i)=>{const x=-785+i*535,u=ease(p(t,67.2+i*.45,68+i*.45));doc(x,173,500,140,u);TX(s,x+250,226,46,u,{align:'center'});TX(d,x+250,282,29,u,{align:'center',v:.82});liveRoute([[210,-45],[210,97],[x+250,97],[x+250,173]],66.7+i*.45,68+i*.45,.72);});
 // Reference-inspired roundtable and three accurately scoped participants.
 L(ellipse(0,443,925,130),1,2.7,.9);L(ellipse(0,473,925,130),1,1.5,.5);L(ellipse(0,443,845,101),1,1.2,.45);
 const experts=[[-660,'产业链研判专家','产业位置'],[0,'第三代／宽禁带半导体','技术与产业化'],[660,'股东增减持专家','服务切入点']];
 experts.forEach(([x,s,d],i)=>{const u=ease(p(t,63+i*.4,63.8+i*.4));panel(x-35,347,70,46,1,.7,12);C(x,329,18,1,.8,1.5);if(i===1){panel(x-290,483,580,110,1,.9,8);TX(s,x,528,38,1,{align:'center'});TX('产业研究专家',x,574,35,1,{align:'center'});}else plaque(s,x-290,483,580,43,1);TX(d,x,432,29,u,{align:'center',v:.85});});
 const result=ease(p(t,70.8,71.5));if(result>0){doc(-465,352,930,108,result);TX('研究成果回到 A01：客户背景与沟通重点',0,420,36,result,{align:'center'});}
 gear(-1044,453,26,6,t*.25,1,.55,20);gear(1044,453,26,6,-t*.25,1,.55,20);
 });
 if(filmTime>=80&&filmTime<=84)at(0,0,()=>carrier(industryIn,ease(p(filmTime-20,60,64)),'A01',220));
 if(filmTime>=92.8&&filmTime<=96)at(0,0,()=>carrier(industryOut,ease(p(filmTime-20,72.8,76)),'A01 · 研究依据',320));
}
function caseTag(){} // Case identity lives on the archive and station labels, not over titles.
function ending(){if(filmTime<120)return;const a=ease(p(filmTime-20,100,100.8));ov.save();ov.scale(scale,scale);ov.globalAlpha=a;const grad=ov.createLinearGradient(0,770,0,1080);grad.addColorStop(0,'rgba(5,23,42,0)');grad.addColorStop(.4,'rgba(5,23,42,.96)');grad.addColorStop(1,'rgba(5,23,42,.96)');ov.fillStyle=grad;ov.fillRect(0,770,1920,310);ot(ov,'FirmBuddy',960,904,76,'#f0f1e8','center',600);ot(ov,'商机发现有方向 · 业务研判有依据 · 客户跟进有准备',960,985,39,'#d7e8f3','center');ov.restore();}
window.renderAt=(t,type='image/png',quality=.95)=>{
 filmTime=Math.max(0,Math.min(124,t));T=originalTime(filmTime);bounds=[];
 const c=storyCamera(filmTime);setCam({...c,z:c.z*scale});proj.k=.43;clear();NIBS.length=0;
 chassis();at(0,0,()=>{rail(industryIn,.43);rail(industryOut,.35);});
 inkLayer(ease(p(filmTime,35.2,37.2)),()=>intro());
 signals();experts();knowledge();visit();follow();industry();
 opening();businessNarrative(filmTime);caseTag();ending();
 compose(inkC,fxC,ovC,{sheet:[9800,4800],cam,seed:19});return type?canvas.toDataURL(type,quality):null;
};
window.cameraAt=storyCamera;window.cameraKeys=[...openingKeys,...storyClock.map(k=>[k[0]+20]),...detourKeys.map(k=>[k[0]+20,...k.slice(1)])].sort((a,b)=>a[0]-b[0]);
window.stateAt=t=>{window.renderAt(t,null);return{time:t,camera:storyCamera(t),buffer:[W,H],duration:124,shot:plan.shots.find(s=>t>=s.start&&t<s.end)?.id,bounds,caseId:'A01',originalTime:T};};
window.__ready=true;window.renderAt(0,null);
const audio=new Audio('./audio/mix.wav'),seek=document.querySelector('#seek'),display=document.querySelector('#time'),button=document.querySelector('#play');let playing=false,started=0,base=0;
seek.oninput=()=>{base=+seek.value;audio.currentTime=base;started=performance.now();window.renderAt(base,null);display.textContent=base.toFixed(2)+' / 124';};
button.onclick=()=>{playing=!playing;button.textContent=playing?'暂停':'播放';if(playing){base=+seek.value;if(base>=124)base=0;started=performance.now();audio.currentTime=base;audio.play().catch(()=>{});}else{base=+seek.value;audio.pause();}};
function tick(){if(playing){const t=Math.min(124,base+(performance.now()-started)/1000);window.renderAt(t,null);seek.value=t;display.textContent=t.toFixed(2)+' / 124';if(t>=124){playing=false;audio.pause();button.textContent='播放';}}requestAnimationFrame(tick);}if(!Q.has('render'))tick();
