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
function spec(x=-695,y=307,u=1){mono('DEMO /',x,y,18,u,{v:.55});TX('流程示例',x+100,y,27,u,{v:.7});}
// Screen-space drafting table above the same paper shader. Absolute-time poses.
let filmTime=0;
const cardScenes=[['治理整改','信披与公司治理','合规治理'],['并购重组','资本运作新线索','资本运作'],['股东减持','股东服务新需求','股东服务'],['风险管理','汇率与商品风险','跨境经营'],['上市与分拆','企业成长新阶段','成长融资']];
function pen(ctx,color,width=1){ctx.strokeStyle=color;ctx.lineWidth=width;ctx.lineCap='round';ctx.lineJoin='round';}
function ot(ctx,s,x,y,size,color='#edf1ea',align='left',weight=400){ctx.font=`${weight} ${size}px ${FONT}`;ctx.fillStyle=color;ctx.textAlign=align;ctx.fillText(s,x,y);if(ctx.globalAlpha>=.64&&size>=30){const w=ctx.measureText(s).width,dx=align==='center'?-w/2:align==='right'?-w:0,m=ctx.getTransform(),q=[[x+dx,y-size*.95],[x+dx+w,y-size*.95],[x+dx+w,y+size*.22],[x+dx,y+size*.22]].map(([a,b])=>[(m.a*a+m.c*b+m.e)/scale,(m.b*a+m.d*b+m.f)/scale]);bounds.push({text:s,id:s,box:[Math.min(...q.map(v=>v[0])),Math.min(...q.map(v=>v[1])),Math.max(...q.map(v=>v[0])),Math.max(...q.map(v=>v[1]))],size});}}
function ol(ctx,q,color='#c1d3df',width=1){pen(ctx,color,width);ctx.beginPath();q.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.stroke();}
function ring(ctx,x,y,r,color='#cfb77d',width=1){pen(ctx,color,width);ctx.beginPath();ctx.arc(x,y,r,0,TAU);ctx.stroke();}
function icon(ctx,x,y,id,s=1,color='#c9b17a'){
 ctx.save();ctx.translate(x,y);ctx.scale(s,s);pen(ctx,color,2);
 if(id===0){ring(ctx,0,0,39,color,2);ring(ctx,0,0,31,color,.7);ol(ctx,[[0,-22],[0,0],[18,12]],color,3);for(let i=0;i<12;i++){let a=i*TAU/12;ol(ctx,[[Math.cos(a)*34,Math.sin(a)*34],[Math.cos(a)*38,Math.sin(a)*38]],color);}}
 if(id===1){ol(ctx,[[-38,30],[-17,30],[-17,-21],[13,-21],[13,4],[37,4]],color,2);ol(ctx,[[25,-7],[37,4],[25,16]],color,2);ring(ctx,-38,30,5,color,2);ring(ctx,-17,-21,5,color,2);}
 if(id===2){for(let i=0;i<3;i++){ctx.save();ctx.translate(i*12-17,-i*9);ctx.strokeRect(-27,-23,54,60);ol(ctx,[[-17,-7],[15,-7]],color);ol(ctx,[[-17,7],[15,7]],color);ctx.restore();}}
 if(id===3){for(const [xx,yy] of [[-29,16],[0,-16],[29,16]]){ring(ctx,xx,yy,12,color,2);ol(ctx,[[xx-18,yy+30],[xx-18,yy+23],[xx+18,yy+23],[xx+18,yy+30]],color,2);}ol(ctx,[[-20,1],[-10,-9]],color);ol(ctx,[[10,-9],[20,1]],color);}
 if(id===4){ol(ctx,[[-33,30],[-33,-12],[0,-35],[33,-12],[33,30],[-33,30]],color,2);ol(ctx,[[-13,30],[-13,2],[13,2],[13,30]],color,2);}
 ctx.restore();
}
function card(ctx,i,x,y,w,h,r,alpha=1,morph=0){
 ctx.save();ctx.globalAlpha*=alpha;ctx.translate(x,y);ctx.rotate(r);
 const cream=1-morph,cut=mix(12,26*.95,morph),gold=morph<.7?'#c9ad72':'#d7e8f3';
 ctx.shadowColor=`rgba(0,10,23,${.4*cream})`;ctx.shadowBlur=22*cream;ctx.shadowOffsetY=15*cream;
 const rgb=(a,b)=>a.map((v,j)=>Math.round(mix(v,b[j],morph))).join(',');const fillAlpha=1-ease(p(morph,.8,1));
 const grad=ctx.createLinearGradient(-w/2,-h/2,w/2,h/2);grad.addColorStop(0,`rgba(${rgb([250,247,235],[21,52,81])},${fillAlpha})`);grad.addColorStop(1,`rgba(${rgb([228,221,200],[21,52,81])},${fillAlpha})`);
 ctx.fillStyle=grad;pen(ctx,gold,mix(1.5,2.2,morph));ctx.beginPath();ctx.moveTo(-w/2,-h/2);ctx.lineTo(w/2-cut,-h/2);ctx.lineTo(w/2,-h/2+cut);ctx.lineTo(w/2,h/2);ctx.lineTo(-w/2,h/2);ctx.closePath();ctx.fill();ctx.stroke();ctx.shadowColor='transparent';
 ctx.save();ctx.globalAlpha*=1-ease(p(morph,.02,.4));ctx.beginPath();ctx.rect(-w/2,-h/2,w,h);ctx.clip();
 pen(ctx,'#b9a170',.8);ctx.strokeRect(-w/2+9,-h/2+9,w-18,h-18);ctx.strokeRect(-w/2+14,-h/2+14,w-28,h-28);
 for(const sx of [-1,1])for(const sy of [-1,1]){ctx.save();ctx.translate(sx*(w/2-23),sy*(h/2-23));ctx.scale(-sx,-sy);ol(ctx,[[0,21],[0,0],[21,0]],'#b79a60',1.3);ring(ctx,5,5,3,'#b79a60');ctx.restore();}
 // Fine diagonal paper guilloche is deterministic, not a flattened screenshot.
 ctx.save();ctx.beginPath();ctx.rect(-w/2+19,-h/2+19,w-38,h-38);ctx.clip();for(let k=-h;k<w+h;k+=27)ol(ctx,[[k-w/2,-h/2],[k-w/2+h,h/2]],'rgba(188,169,131,.09)',.7);ctx.restore();
 const a=cardScenes[i],left=-w/2+31;
 ot(ctx,'SCENARIO / 0'+(i+1),left,-h/2+54,15,'#a28a56');
 icon(ctx,0,-h/2+134,i===2?4:i,.84,'#345570');
 ot(ctx,a[0],0,-h/2+228,i===4?33:37,'#183d5a','center',600);
 ol(ctx,[[left,-h/2+252],[w/2-31,-h/2+252]],'#c7b68f',1);
 ot(ctx,a[1],0,-h/2+295,24,'#587086','center');
 ot(ctx,a[2],0,-h/2+337,19,'#9c885e','center');
 ctx.fillStyle='#1c4261';ctx.fillRect(left,h/2-71,w-62,39);ot(ctx,'发现业务机会  →',0,h/2-44,19,'#f7f2e5','center');ctx.restore();
 if(morph>0){ctx.save();ctx.globalAlpha*=ease(p(morph,.45,.9));ring(ctx,-w/2+16*.95,-h/2+17*.95,5*.95,'#d7e8f3',1);ot(ctx,'示例客户信息',0,15*.95,34*.95,'#d7e8f3','center');ol(ctx,[[w/2-cut,-h/2],[w/2-cut,-h/2+cut],[w/2,-h/2+cut]],'#a5c4db',1);ctx.restore();}
 ctx.restore();
}
function opening(t){if(t>=11)return;const ctx=ov;ctx.save();ctx.scale(scale,scale);
 // Open drafting geometry: registration ticks, rails and a broad arc reserve motion space.
 const backdrop=1-ease(p(t,7.9,8.5));ctx.save();ctx.globalAlpha=backdrop;
 pen(ctx,'rgba(174,204,224,.16)',1);ctx.strokeRect(60,52,1800,976);
 for(let x=100;x<1860;x+=80)for(let y=100;y<1000;y+=80){ol(ctx,[[x-3,y],[x+3,y]],'rgba(185,211,226,.10)');ol(ctx,[[x,y-3],[x,y+3]],'rgba(185,211,226,.10)');}
 ot(ctx,'FIRMBUDDY  /  OPPORTUNITY ENGINE',96,98,18,'#8daec5');ot(ctx,'客户经营 · 业务场景',1824,98,18,'#8daec5','right');
 const painAlpha=1-ease(p(t,3.5,4.3));ctx.save();ctx.globalAlpha*=painAlpha;
 ot(ctx,'B 端商机，为什么总是慢一步？',960,226,64,'#f0f2e8','center',600);
 ot(ctx,'时间花在找资料，精力耗在做准备',960,291,29,'#9db9cf','center');
 const pains=[['商机收集耗时长','线索散落，搜集整理耗费精力'],['不知从何入手','发现信号，缺少清晰切入路径'],['专业支持难找','跨领域问题，需要专业判断'],['跟进准备重复','拜访材料、沟通重点反复整理']];
 pains.forEach((a,i)=>{const u=ease(p(t,.1+i*.21,.6+i*.21));const x=200+(i%2)*850,y=440+Math.floor(i/2)*250;ctx.save();ctx.globalAlpha*=u;ctx.translate(0,(1-u)*22);icon(ctx,x+57,y-12,i,1.03);ot(ctx,a[0],x+144,y-2,45,'#eef2eb');ot(ctx,a[1],x+144,y+53,27,'#a8c1d3');ol(ctx,[[x+144,y+88],[x+650,y+88]],'rgba(170,204,224,.35)');ot(ctx,'0'+(i+1),x+654,y+5,16,'#c2ab75','right');ctx.restore();});
 ot(ctx,'让时间回到判断需求、服务客户、推进合作上',960,942,30,'#d1bb87','center');ctx.restore();
 const cardsAlpha=ease(p(t,3.7,4.5));ctx.save();ctx.globalAlpha*=cardsAlpha*(1-ease(p(t,7.6,8.1)));
 ot(ctx,'商机查询',960,211,63,'#f3f0e5','center',600);ctx.save();ctx.globalAlpha*=1-ease(p(t,6.4,6.9));ot(ctx,'多种业务场景，从一张商机卡开始',960,270,29,'#b1c7d7','center');ctx.restore();
 pen(ctx,'rgba(202,178,119,.35)',1.2);ctx.beginPath();ctx.ellipse(960,799,817,170,0,Math.PI,TAU);ctx.stroke();
 ctx.save();ctx.globalAlpha*=1-ease(p(t,6.4,6.9));ot(ctx,'治理整改  ·  并购重组  ·  股东服务  ·  风险管理  ·  上市与分拆',960,978,26,'#b5cad9','center');ctx.restore();ctx.restore();ctx.restore();
 const reveal=ease(p(t,3.8,4.8)),extract=ease(p(t,6.4,7.7)),travel=ease(p(t,8,10.7));
 for(const i of [0,4,1,3]){const d=i-2;card(ctx,i,960+d*315,655+Math.abs(d)*28+(1-reveal)*430,288,449,d*.085,cardsAlpha*(1-ease(p(t,7.5,8.6))),0);}
 if(cardsAlpha>0){
   const q=[[-110,-73],[510,-73],...paths.query.slice(1).map(([x,y])=>[x-1050,y-1070])];const v=pathPoint(q,ease(p(T,1.2,5.8)));const target=S(v[0]+1050,v[1]+1070).map(x=>x/scale);
   const x=mix(960,target[0],travel),y=mix(620-112*extract+(1-reveal)*430,target[1],travel),w=mix(326+24*extract,270*cam.z/scale,travel),h=mix(488+16*extract,104*cam.z/scale,travel);
   card(ctx,2,x,y,w,h,-.025*Math.sin(extract*Math.PI)*(1-travel),cardsAlpha*(1-ease(p(t,10.7,11))),travel);
   ctx.save();ctx.globalAlpha=extract*(1-ease(p(t,7.9,8.5)));ot(ctx,'以股东减持为例，进入专业研判',960,978,32,'#e4d2a6','center');ctx.restore();
 }
 ctx.restore();
}

// Editorial drafting notes outside the camera: problem and practical business result.
function businessNarrative(t){const q=plan.business_messages.find(q=>t>=q.start&&t<q.end);if(!q)return;
 const a=ease(p(t,q.start,q.start+.32))*(1-ease(p(t,q.end-.32,q.end))),ctx=ov;
 ctx.save();ctx.scale(scale,scale);ctx.globalAlpha=a;
 const shade=(y,h)=>{const z=ctx.createLinearGradient(0,y,0,y+h);z.addColorStop(0,'rgba(5,23,42,.0)');z.addColorStop(.45,'rgba(5,23,42,.94)');z.addColorStop(1,'rgba(5,23,42,.94)');ctx.fillStyle=z;ctx.fillRect(0,y,1920,h);};
 ctx.fillStyle='rgba(5,23,42,.9)';ctx.fillRect(0,0,1920,105);
 ol(ctx,[[96,108],[1824,108]],'rgba(190,171,117,.43)',1);
 ot(ctx,q.pain,960,74,36,'#e4c992','center',500);
 shade(987,93);ot(ctx,q.result,960,1044,34,'#edf2eb','center',400);
 ctx.restore();}

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
 [47.5,4140,2480,.22,0],[48.4,4140,2480,.22,0],
 [50.4,4140,2510,.228,0],[52,4140,2510,.228,0]
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
 mono('FIRMBUDDY / CLIENT OPERATIONS',-670,-378,24,1,{v:.6});TX('找到客户经营的业务切入点',-670,-300,50,1);
 const labels=['商机查询','业务问题答疑','客户拜访准备'];
 labels.forEach((s,i)=>{const y=-133+i*170,u=show(.2+i*.16);plaque(s,-650,y-53,300,39,u);solid(pts([[-316,y-47],[-230,y-47],[-249,y+2],[-296,y+2]]),{u,v:.7,w:2,th:12});gear(-267,y+60,18,4,T*.8,u,.65,12);shaft([[-217,y+60],[510,y+60]],u,.55);for(let j=0;j<6;j++)C(-140+j*107,y+60,6,u,.5,1);bearing(120,y+60,u);pointer(456,y+60);});
 TX('AI 辅助识别问题、调用工具',-650,387,35,show(1),{v:.85});
 if(T<5.8){const priorVisibility=visibility;visibility*=ease(p(filmTime,10.7,11));const u=ease(p(T,1.2,5.8));carrier([[-110,-73],[510,-73],...paths.query.slice(1).map(([x,y])=>[x-1050,y-1070])],u,'示例客户信息',270);visibility=priorVisibility;}
 });}
function signals(){at(...centers.signals,()=>{
 TX('把分散线索，变成可跟进的客户机会',-730,-335,46,1);mono('01 / DISCOVER · CONNECT · FILTER',-730,-390,22,1,{v:.5});
 frameBase(-685,-245,1380,475);rail([[-720,220],[700,220]],.42);
 const sources=['公司公告','股东动态','客户资料'];
 sources.forEach((label,i)=>{const u=ease(p(T,6.1+i*.2,7+i*.2)),x=mix(-658,145,u),y=mix(-180+i*134,-80,u),v=1-ease(p(u,.6,1));
   panel(-658,-180+i*134,382,96,1,.28,12);TX(label,-628,-116+i*134,36,1,{v:.48});
   route([[-258,-132+i*134],[-65,-132+i*134],[95,-80],[145,-80]],6.1+i*.2,7+i*.2,2.5,.65);
   if(v>.01){const prior=visibility;visibility*=v;doc(x,y,382,96,1);TX(label,x+30,y+64,36,1);visibility=prior;}
 });
 gear(-460,225,24,6,T*.7,1,.6,18);gear(-310,225,26,6,meshAngle(T*.7,24,26,[-460,225],[-310,225]),1,.55,18);
 doc(145,-208,517,393,1,.85);TX('减持商机示例',175,-158,28,1,{v:.7});
 TX('客户线索归集',175,-81,46,show(6.5));L([[175,-43],[620,-43]],show(6.6),1.4,.5);
 TX('重点客户与业务线索',175,22,38,show(6.7));TX('原文依据 · 来源可追溯',175,87,32,show(6.9));
 TX('AI 辅助解读客户线索',175,147,32,show(7.1));
 });if(T>8.4&&T<11.7)movingRoute(paths.toHall,8.4,11.7);}
function experts(){at(...centers.experts,()=>{
 TX('看清客户需求，找到服务切入点',0,-622,55,1,{align:'center'});
 // System taxonomy is a separate nine-domain directory above the auditorium.
 domains.forEach((s,i)=>{const x=-1070+(i%3)*735,y=-520+Math.floor(i/3)*65;TX(s,x,y,43,1,{v:.92});if(i%3<2)L([[x+640,y-34],[x+640,y+8]],1,1,.4);});
 L([[-1110,-336],[1110,-336]],1,1.5,.45);
 TX('专业培养的 AI 专家团 · 九大业务领域协作',0,-286,46,1,{align:'center',v:.9});
 // Four stepped semi-elliptical terraces: named seats, no human figures.
 for(let row=0;row<4;row++){
   const rx=1100-row*118,ry=530-row*90,cy=285;
   const arc=ellipse(0,cy,rx,ry,Math.PI,TAU,100);
   L(arc,1,2.8,.82);L(arc.map(([x,y])=>[x,y+42]),1,1.7,.6);L(arc.map(([x,y])=>[x,y+67]),1,1,.4);
   for(let j=0;j<14;j++){
     const a=Math.PI+.10+j*(Math.PI-.20)/13,x=Math.cos(a)*(rx-20),y=cy+Math.sin(a)*(ry-18);
     L([[x-19,y+12],[x-19,y+38],[x+19,y+38],[x+19,y+12]],1,1.5,.5);
     panel(x-34,y-25,68,43,1,.72,12);R(x-7,y-36,14,11,1,.5,1);
     L([[x-22,y-4],[x+22,y-4]],1,1,.3);
   }
 }
 for(const x of[-1120,1120]){panel(x-24,242,48,260,1,.5,18);panel(x-49,480,98,23,1,.6,13);bolt(x-31,493);bolt(x+31,493);}
 const ring=ellipse(0,365,347,139);L(ring,1,2.7,.95);L(ellipse(0,405,347,139),1,1.7,.6);L(ellipse(0,365,290,108),1,1.4,.55);
 for(let i=0;i<18;i++){const a=i*TAU/18;bolt(Math.cos(a)*321,365+Math.sin(a)*124);}
 const chosen=[[-720,97,'客户需求'],[0,-121,'联系时机'],[720,97,'服务切入点']];
 chosen.forEach(([x,y,s],i)=>{const u=show(12.1+i*.4,.4);panel(x-52,y-34,104,63,u,1,10);plaque(s,x-175,y-149,350,43,u);route([[x,y+30],[x*.65,260],[0,365]],12.7+i*.4,14+i*.4,2.8,.92);});
 doc(-266,307,532,142,1);TX('客户需求与服务思路',0,364,44,show(13),{align:'center'});TX('AI 辅助多专业会商',0,415,35,show(13.1),{align:'center',v:.6});
 // Knowledge equipment supplies the specialist seats. Each clutch engages on an existing music beat.
 const foundations=['专业知识装备','业务方法沉淀','培养与试炼'];
 foundations.forEach((label,i)=>{const x=-1045+i*710,u=show(12.1+i*.4,.4);
   plaque(label,x,480,670,44,u);
   const seat=chosen[i],port=[x+335,480],side=i===0?-1170:i===2?1170:380;
   route([port,[port[0],455],[side,455],[side,seat[1]+55],[seat[0],seat[1]+55],[seat[0],seat[1]+31]],12.1+i*.4,12.5+i*.4,2.8,.72);
 });
 });if(T>=16.3&&T<=20.6)movingRoute(paths.knowledge,16.3,20.6);}
function cabinet(x,y,s,i){
 panel(x,y,204,350,1,.68,32);R(x+13,y+15,178,315,1,.4,1.3);
 for(let j=0;j<5;j++){panel(x+22,y+36+j*53,160,43,1,.55,8);R(x+76,y+48+j*53,53,12,1,.45,1);for(let k=0;k<4;k++)L([[x+31+k*7,y+44+j*53],[x+31+k*7,y+67+j*53]],1,1,.25);}
 TX(s,x+102,y-30,33,1,{align:'center',v:.85});mono(String(i+1).padStart(2,'0'),x+101,y+391,21,1,{align:'center',v:.45});
}
function knowledge(){at(...centers.knowledge,()=>{
 TX('复杂业务研判，有专业依据可用',-730,-359,48,1);mono('02 / EVIDENCE · SECTION A–A',-730,-410,21,1,{v:.5});
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
   TX('为业务判断补齐依据',x+28,y+65,39,show(22.2));L([[x+28,y+90],[x+ww-28,y+90]],show(22.3),1,.45);
   TX('规则 · 案例 · 研究依据',x+28,y+164,45,show(22.5));TX('AI 辅助检索与交叉查证',x+28,y+229,30,show(22.7),{v:.75});
 }
 if(T>=23.1){panel(129,-109,559,222,show(23.1),1,10);TX('明确客户服务方向',156,-45,39,show(23.2));TX('存量股东服务回访',156,25,43,show(23.4));TX('服务方向：股份管理',156,77,30,show(23.5),{v:.75});route([[33,-10],[128,-10]],22.8,23.4,3);}
 TX('专业培养的专家团 · 多源知识库 · 可追溯依据',-730,365,34,1,{v:.8});
 });if(T>=25.8&&T<=29.1)movingRoute(paths.output,25.8,29.1);}
function visit(){at(...centers.visit,()=>{
 TX('少做重复准备，多花精力服务客户',-730,-379,49,1);mono('03 / OUTPUT CARRIAGE',-730,-432,21,1,{v:.5});
 frameBase(-734,-251,1458,510);shaft([[-721,-184],[720,-184]],1,.6);
 for(let x=-700;x<700;x+=29)L([[x,-199],[x+17,-169]],1,1.2,.4);bearing(-701,-184);bearing(700,-184);
 doc(-50,-123,738,328,1);TX('客户跟进准备包',-12,-65,43,1);L([[-12,-40],[645,-40]],1,1.2,.5);
 ['拜访资料','沟通重点','后续安排'].forEach((label,i)=>{const z=ease(p(T,29.5+i*.25,31.1+i*.25)),v=1-ease(p(z,.65,1));if(v>.01){const prior=visibility;visibility*=v;const xx=mix(-707,-50,z),yy=mix(-110+i*92,-20,z);doc(xx,yy,430,72,1);TX(label,xx+28,yy+49,34,1);visibility=prior;}});
 const x=mix(-492,243,ease(p(T,29.4,31.2))),u=1-ease(p(T,31.1,31.6));
 panel(x-100,-218,200,67,1,.6,16);bolt(x-76,-195);bolt(x+76,-195);L([[x,-151],[x,-32]],1,2,.5);
 if(u>.01){panel(x-245,-22,490,85,1,u);TX('形成客户沟通准备',x,35,41,1,{align:'center',v:u});}
 TX('联系时机 · 服务切入点',-12,35,43,show(31.2));TX('开场话术 · 沟通重点',-12,116,37,show(31.8));TX('AI 辅助整理材料与跟进建议',-12,173,32,show(32.2),{v:.8});
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
 doc(173,-162,466,240,show(38));TX('客户经营记录',205,-85,45,show(38.1));TX('沟通需求 · 服务安排',205,-14,33,show(38.3));TX('跟进事项 · 经营进展',205,39,31,show(38.4),{v:.8});
 doc(-563,162,1202,129,show(39));TX('沟通记录支持持续跟进',-528,241,43,show(39.2));
 TX('AI 辅助梳理记录，支持后续研判',-563,350,31,show(39.4),{v:.8});
 });if(T>=40.3&&T<=49.2){const u=feedbackProgress(T);carrier(paths.feedback,u,'跟进记录',245);L(trunc(paths.feedback,u)[0],1,3.1,.8);}}
function chassis(){at(0,0,()=>{
 R(115,115,7970,4570,1,.26,1.4);R(150,150,7900,4500,1,.13,1);
 for(let x=400;x<8000;x+=400){L([[x,115],[x,150]],1,1,.3);mono(String(x/400),x+10,188,23,1,{v:.35});}
 for(let y=400;y<4600;y+=400){L([[115,y],[150,y]],1,1,.3);mono(String.fromCharCode(64+y/400),164,y+10,23,1,{v:.35});}
 for(let x=320;x<8050;x+=240)for(let y=280;y<4550;y+=240){L([[x-9,y],[x+9,y]],1,.8,.105);L([[x,y-9],[x,y+9]],1,.8,.105);}
 // The support network exists from frame zero, so new regions are discovered, not replaced.
 for(const q of Object.values(paths))rail(q,.4);
 rail(bez([1560,1337],[2800,1960],[3870,1970],[4700,1770]),.3);
 for(const [x,y,n]of[[2150,940,18],[3900,1370,24],[4850,2390,22],[4860,3020,20],[7870,3570,28],[675,3670,32]]){gear(x,y,n,5,T*.28,1,.4,14);}
 if(T>44){
   const u=show(44,.7);plaque('问题入口',880,470,1120,127,u);plaque('线索归集',2450,660,1140,127,u);
   plaque('专业研判',5130,325,1240,136,u);plaque('知识依据',3050,2240,1250,144,u);
   plaque('跟进准备',5600,2370,1400,142,u);plaque('持续经营',3390,3890,1350,136,u);
 }
 // Same-sheet title block. No sudden brand push and no lifecycle grid.
 const u=show(46,.8);if(u>0){panel(1240,4180,6660,390,u,.9,0);R(1270,4210,6600,330,u,.4,1);L([[3260,4210],[3260,4540]],u,2,.5);TX('FirmBuddy',1420,4423,271,u,{font:'Georgia',weight:700});TX('让商机有线索，研判有依据，跟进有准备',3480,4375,141,u);TX('把时间用在理解客户、匹配服务与推进合作',3480,4490,94,u,{v:.75});}
 });}
// Music-only edition: business labels remain in world space.
function caption(){}
window.renderAt=(t,type='image/png',quality=.95)=>{filmTime=Math.max(0,Math.min(60,t));T=Math.max(0,filmTime-8);bounds=[];const c=cameraAt(T);setCam({...c,z:c.z*scale});proj.k=.43;clear();NIBS.length=0;if(filmTime>8){chassis();intro();signals();experts();knowledge();visit();follow();const a=ease(p(filmTime,8,10.7));if(a<1){g.setTransform(1,0,0,1,0,0);g.globalCompositeOperation='destination-in';g.fillStyle=`rgba(0,0,0,${a})`;g.fillRect(0,0,W,H);g.globalCompositeOperation='source-over';}}opening(filmTime);businessNarrative(filmTime);compose(inkC,fxC,ovC,{sheet:[8200,4800],cam,seed:19});return type?canvas.toDataURL(type,quality):null;};
window.cameraAt=t=>cameraAt(Math.max(0,t-8));window.cameraKeys=keys.map(k=>[k[0]+8,...k.slice(1)]);
window.stateAt=t=>{window.renderAt(t,null);return{time:t,camera:cameraAt(T),buffer:[W,H],duration:60,shot:plan.shots.find(s=>t>=s.start&&t<s.end)?.id,bounds,opening:t<11,selectedCard:'opportunity-reduction-example'};};
window.__ready=true;window.renderAt(0,null);
const audio=new Audio('./audio/mix.wav'),seek=document.querySelector('#seek'),display=document.querySelector('#time'),button=document.querySelector('#play');let playing=false,started=0,base=0;
seek.oninput=()=>{base=+seek.value;audio.currentTime=base;started=performance.now();window.renderAt(base,null);display.textContent=base.toFixed(2)+' / 60';};
button.onclick=()=>{playing=!playing;button.textContent=playing?'暂停':'播放';if(playing){base=+seek.value;if(base>=60)base=0;started=performance.now();audio.currentTime=base;audio.play().catch(()=>{});}else{base=+seek.value;audio.pause();}};
function tick(){if(playing){const t=Math.min(60,base+(performance.now()-started)/1000);window.renderAt(t,null);seek.value=t;display.textContent=t.toFixed(2)+' / 60';if(t>=60){playing=false;audio.pause();button.textContent='播放';}}requestAnimationFrame(tick);}if(!Q.has('render'))tick();
