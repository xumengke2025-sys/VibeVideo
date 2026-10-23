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
  if(u>=.999&&v>=.64&&size*cam.z/scale>=26){
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

// One continuous machine, one A01 dossier; all actions are functions of absolute time.
let realTime=0;
const E=Object.fromEntries(plan.soundtrack.events.map(e=>[e.id,e.at]));
const ST={intake:[1200,1100],collect:[3500,1100],hall:[6200,1100],industry:[9000,1100],knowledge:[9000,3600],assembly:[6200,3600],follow:[3500,3600]};
const ep=(id,before=0,after=.8)=>ease(p(realTime,E[id]+before,E[id]+after));
function inkLayer(a,fn){if(a<.002)return;const old=visibility;visibility*=a;fn();visibility=old;}
function localVisible(x,y,w=1200,h=800){const q=S(x,y);return q[0]>-w*cam.z&&q[0]<W+w*cam.z&&q[1]>-h*cam.z&&q[1]<H+h*cam.z;}
function check(x,y,s=1,u=1){L([[x-12*s,y],[x-3*s,y+9*s],[x+17*s,y-14*s]],u,3.2,.98);}
function cross(x,y,s=1,u=1){L([[x-10*s,y-10*s],[x+10*s,y+10*s]],u,2,.65);L([[x+10*s,y-10*s],[x-10*s,y+10*s]],u,2,.65);}
function icon(type,x,y,s=1,u=1){
 if(type==='paper'){doc(x-24*s,y-30*s,48*s,60*s,u,.85);detail(x-15*s,y-7*s,28*s,3,u);}
 if(type==='clock'){C(x,y,26*s,u,.9,1.7);L([[x,y-17*s],[x,y],[x+15*s,y+8*s]],u,2,.9);}
 if(type==='person'){C(x,y-14*s,12*s,u,.9,1.7);L([[x-24*s,y+28*s],[x-20*s,y+8*s],[x+20*s,y+8*s],[x+24*s,y+28*s]],u,2,.9);}
 if(type==='lens'){C(x-5*s,y-5*s,20*s,u,.9,1.8);L([[x+11*s,y+11*s],[x+29*s,y+29*s]],u,4,.9);}
 if(type==='chain'){C(x-15*s,y,19*s,u,.9,1.8);C(x+15*s,y,19*s,u,.9,1.8);}
 if(type==='flag'){L([[x-15*s,y+29*s],[x-15*s,y-27*s],[x+25*s,y-27*s],[x+12*s,y-7*s],[x-15*s,y-7*s]],u,2.2,.9);}
}
function plateName(title,x=0,y=-390){TX(title,x,y,53,1,{align:'center'});}
function subLabel(s,x,y){TX(s,x,y,29,1,{align:'center',v:.8});}
function machineBase(w=1600,y=330){
 panel(-w/2,y,w,34,1,.58,16);truss(-w/2,y+77,w/2,y+77,Math.round(w/160));
 for(const x of[-w/2+75,w/2-75]){panel(x-34,y+33,68,106,1,.5,16);bolt(x,y+55);panel(x-63,y+139,126,19,1,.5,12);}
}
function drive(x,y,clock=realTime,active=1,s=1){
 const a=clock*.68;
 gear(x,y,24,5*s,a,1,.8,18*s);gear(x+120*s,y,24,5*s,meshAngle(a,24,24,[x,y],[x+120*s,y]),1,.68,18*s);
 shaft([[x-140*s,y],[x-67*s,y]],1,.55);bearing(x-104*s,y);shaft([[x+187*s,y],[x+300*s,y]],1,.55);bearing(x+250*s,y);
}
function flywheel(x,y,r,a){
 C(x,y,r,1,.9,3);C(x,y,r-10,1,.48,1.4);C(x,y,r*.2,1,.9,2);C(x,y,r*.07,1,.9,1.5);
 for(let i=0;i<6;i++){const b=a+i*TAU/6;L([[x+Math.cos(b)*r*.22,y+Math.sin(b)*r*.22],[x+Math.cos(b)*r*.89,y+Math.sin(b)*r*.89]],1,4,.65);}
}
function beltWheel(x,y,r,a){flywheel(x,y,r,a);for(let i=0;i<12;i++){const b=a+i*TAU/12;L([[x+Math.cos(b)*(r-7),y+Math.sin(b)*(r-7)],[x+Math.cos(b)*(r+4),y+Math.sin(b)*(r+4)]],1,1.4,.55);}}
function conveyor(x0,x1,y,t=realTime,speed=70){
 const r=24,a=t*speed/r;L([[x0,y-r],[x1,y-r]],1,2.5,.8);L([[x0,y+r],[x1,y+r]],1,1.5,.45);
 beltWheel(x0,y,r,a);beltWheel(x1,y,r,a);
 for(let x=x0+35;x<x1-20;x+=65){C(x,y,12,1,.45,1.4);L([[x-12*Math.cos(a),y-12*Math.sin(a)],[x+12*Math.cos(a),y+12*Math.sin(a)]],1,1,.45);}
 for(let i=0;i<Math.ceil((x1-x0)/70);i++){const x=x0+((i*70+t*speed)%(x1-x0));L([[x-5,y-r-5],[x+5,y-r+5]],1,1,.6);}
}
function screwRail(x0,x1,y,t=realTime){
 shaft([[x0,y],[x1,y]],1,.7);for(let x=x0;x<x1;x+=24){const z=x+((t*15)%24);L([[z,y-10],[z+14,y+10]],1,1.5,.65);}
 bearing(x0,y);bearing(x1,y);
}
function stampPress(x,y,t,down){
 // Gear eccentric drives a connecting rod and a constrained vertical crosshead.
 const a=mix(-Math.PI/2,Math.PI*1.5,down),r=32,l=133;
 const pin=[x+r*Math.sin(a),y+r*Math.cos(a)],slide=y+r*Math.cos(a)+Math.sqrt(l*l-r*r*Math.sin(a)**2);
 gear(x,y,24,5,a,1,.8,20);C(...pin,9,1,.95,2);L([pin,[x,slide]],1,9,.8);C(x,slide,10,1,.95,2);
 for(const xx of[x-84,x+84]){shaft([[xx,y+54],[xx,y+240]],1,.5);panel(xx-12,y+237,24,24,1,.5,5);}
 panel(x-110,slide-12,220,32,1,.85,14);L([[x,slide+20],[x,slide+53]],1,10,.7);panel(x-79,slide+53,158,22,1,.9,10);
 return slide+75;
}
function sourceSlip(x,y,kind,s=1,alpha=1){inkLayer(alpha,()=>{doc(x-54*s,y-38*s,108*s,76*s,1,.8);icon(kind,x-17*s,y,.48*s);L([[x+11*s,y-12*s],[x+35*s,y-12*s]],1,1.6,.65);L([[x+11*s,y+7*s],[x+28*s,y+7*s]],1,1.3,.45);});}

const caseKnots=[[20.8,1200,1060],[23.2,1450,1220],[24,1450,1220],[27.2,3930,1200],[40,3930,1200],[43.6,6200,1530],[54.4,6200,1530],[58.4,9250,1200],[67.2,9250,1200],[71.2,9420,3780],[80,9420,3780],[84,6580,3710],[96,6580,3710],[99.2,3930,3670],[104,3930,3670],[112,1450,1220],[120,1450,1220]];
const bends={3:[[2350,1220],[2900,1200]],5:[[4620,1200],[5100,1530]],7:[[7200,1530],[8200,1200]],9:[[10120,1200],[10120,3780]],11:[[8450,3780],[7500,3710]],13:[[5700,3710],[4700,3670]],15:[[1700,5000],[-600,1900]]};
function caseState(t){
 if(t<=caseKnots[0][0])return {x:1200,y:1060,u:0};
 let i=1;while(i<caseKnots.length-1&&t>caseKnots[i][0])i++;
 const a=caseKnots[i-1],b=caseKnots[i],u=ease(p(t,a[0],b[0]));
 if(bends[i]){const [c,d]=bends[i],q=bez([a[1],a[2]],c,d,[b[1],b[2]],100),v=pathPoint(q,u);return{x:v[0],y:v[1],u};}
 return{x:mix(a[1],b[1],u),y:mix(a[2],b[2],u),u};
}
function caseDossier(){
 if(realTime<20.8)return;
 const c=caseState(realTime),m=ease(p(realTime,20.8,23.2)),w=mix(248,300,m),h=mix(312,180,m);
 const done=ep('file',-.1,.4),researched=ep('evidence',0,.3),cited=ep('retrieve',0,.3),ready=ep('page3',0,.5),recorded=ep('record',0,.4);
 at(c.x,c.y,()=>{
   for(let j=2;j>0;j--)doc(-w/2-j*7,-h/2-j*6,w,h,1,.27);
   doc(-w/2,-h/2,w,h,1,.98);
   inkLayer(1-m,()=>{TX('股东服务',0,mix(-53,-24,m),35,1,{align:'center'});icon('clock',0,mix(27,51,m),mix(1.13,1.2,m));});
   inkLayer(m,()=>{TX('A01',-w/2+23,-h/2+44,35,1,{font:MONO});TX('示例客户信息',0,1,32,1,{align:'center'});
     const tabs=[done,researched,cited,ready,recorded];tabs.forEach((u,i)=>{if(u>.01){const x=-108+i*51;R(x-14,30,28,27,1,.78,1.3);check(x,43,.55,u);}});
   });
 });
}
function machineChassis(){
 at(0,0,()=>{
  R(170,180,10740,4740,1,.2,1.2);R(195,205,10690,4690,1,.1,1);
  for(let x=500;x<10800;x+=400){L([[x,180],[x,205]],1,1,.27);mono(String((x-100)/400),x+12,240,18,1,{v:.26});}
  for(let x=400;x<10800;x+=300)for(let y=400;y<4700;y+=300){L([[x-8,y],[x+8,y]],1,.9,.075);L([[x,y-8],[x,y+8]],1,.9,.075);}
  for(const i of[3,5,7,9,11,13,15]){const a=caseKnots[i-1],b=caseKnots[i],q=bez([a[1],a[2]],...bends[i],[b[1],b[2]],120).map(([x,y])=>[x,y+112]);rail(q,.3);}
  // A single visible drive spine beneath the working cells, with support bearings.
  for(const [x0,x1,y]of[[350,10070,1750],[2600,10130,4260]]){shaft([[x0,y],[x1,y]],1,.25);for(let x=x0+170;x<x1;x+=440){bearing(x,y);}}
  shaft([[10130,1750],[10130,4260]],1,.2);
 });
}
function intake(){at(...ST.intake,()=>{
 const t=realTime,pain=1-ease(p(t,9.6,11.2)),open=ep('engage',0,1),turn=Math.max(0,t-E.engage);
 machineBase(1650,333);conveyor(-730,720,264,turn);
 const driverX=-625;
 gear(driverX,325,24,5,turn*.7,1,.78,18);
 const dx=mix(188,120,open);gear(driverX+dx,325,24,5,meshAngle(turn*.7,24,24,[driverX,325],[driverX+dx,325]),1,.7,18);
 shaft([[driverX+dx+65,325],[600,325]],1,.35);
 inkLayer(pain,()=>{
  plateName('忙着搜资料，何时做研判？');
  // Repeated paper shuttling and a blocked gate communicate wasted preparation.
  for(let i=0;i<8;i++){const u=(t*.19+i*.127)%1,x=-580+u*920,y=-100+(i%3)*103;
    sourceSlip(x,y,['paper','clock','person'][i%3],1);}
  panel(390,-212,35,420,1,.8,24);L([[410,-180],[440,-143],[410,-104],[440,-67],[410,-28],[440,9],[410,49],[440,87],[410,128],[440,166]],1,2,.65);
  expertFigure(640,-52,2.1,0);TX('客户经理',640,124,31,1,{align:'center'});
  const labels=['搜、筛、抄','背景拼不齐','专家难协同'];const k=Math.min(2,Math.floor(t/3.2));TX(labels[k],0,-280,34,1,{align:'center',v:.9});
 });
 inkLayer(ease(p(t,10.4,12)),()=>{
   plateName('商机查询');
   inkLayer(1-ease(p(t,20.4,21.6)),()=>{
     icon('paper',-470,-260,.7);TX('公开公告',-365,-249,29,1,{align:'center'});icon('clock',250,-260,.7);TX('解禁日历',366,-249,29,1,{align:'center'});
   });
   const f=ep('fan',-.8,1.2),sel=ease(p(t,20,20.8));
   const names=['再融资','并购重组','股东服务','风险管理','股份回购'];
   for(const i of[0,4,1,3,2]){
     if(i===2&&t>=20.8)continue;
     const x=mix(580,(i-2)*300,f),y=mix(165,i===2?-40*sel:Math.abs(i-2)*17,f),a=f*(1-(i===2?0:ease(p(t,21.2,23.2))));
     inkLayer(a,()=>{doc(x-124,y-156,248,312,1,i===2?.97:.68);TX(names[i],x,y-53,35,1,{align:'center'});icon(i===2?'clock':i===1?'chain':'paper',x,y+27,1.13);TX(i===2?'解禁日历':'公告线索',x,y+115,25,1,{align:'center',v:.7});});
   }
   inkLayer(ease(p(t,21.6,22.4)),()=>{TX('减持商机 · 本次示例',-377,-58,32,1,{align:'center'});TX('半导体衬底企业',-377,-10,28,1,{align:'center',v:.8});});
 });
});}

function collect(){at(...ST.collect,()=>{
 machineBase(1650,333);plateName('AI 归集 · 辅助研判');
 conveyor(-760,730,227,Math.max(0,realTime-27.2));
 const a=Math.max(0,realTime-27.2)*1.1;
 // Twin counterrotating rollers physically accept duplicate source slips.
 for(const y of[-65,65]){beltWheel(-80,y,57,y<0?a:-a);bearing(-80,y);}
 for(const x of[-165,5]){panel(x-13,-161,26,322,1,.45,16);bolt(x,-142);bolt(x,142);}
 const kinds=['paper','paper','clock','clock','person','person'];
 for(let i=0;i<6;i++){
  const u=ease(p(realTime,28+i*.56,29.4+i*.56));if(u<1)sourceSlip(mix(-655,-80,u),mix(-124+(i%3)*124,0,u),kinds[i],.95,1-ease(p(u,.85,1)));
 }
 ['公告','解禁','股东'].forEach((s,i)=>{subLabel(s,-677,-210+i*121);for(let j=2;j>=0;j--)sourceSlip(-527+j*7,-218+i*121-j*7,['paper','clock','person'][i],.66,.45);});
 const out=ep('merge',0,3.2);
 for(let i=0;i<3;i++){const u=ease(p(realTime,30.4+i*.8,31.5+i*.8));if(u>0&&u<1)sourceSlip(mix(-25,260,u),mix(0,100,u),['paper','clock','person'][i],.68,Math.sin(Math.PI*u));}
 // The assessment mask aligns three independent conditions, rather than equating a signal with intent.
 const j=ep('judge',-2.2,0);
 for(let i=0;i<3;i++){
  const x=120+i*175,y=mix(-272-(2-i)*32,-252,j);panel(x-65,y,130,72,1,.78,10);icon(['clock','paper','person'][i],x,y+36,.63);
  L([[x,y+72],[x,-128],[430,-128],[430,8]],j,2.5,.75);
 }
 const hit=ep('file',-.55,0);L([[18,0],[165,0],[260,100]],out,3,.9);
 gear(-452,335,24,5,a,1,.7,18);gear(-332,335,24,5,meshAngle(a,24,24,[-452,335],[-332,335]),1,.7,18);
 const lift=18*Math.sin(a);L([[-392,335],[-392,290+lift]],1,4,.7);panel(-443,260+lift,102,25,1,.68,8);
 inkLayer(hit,()=>check(592,145,1.2,hit));
 inkLayer(ep('judge',0,.45),()=>TX('关注重点',435,-154,34,1,{align:'center'}));
});}

function hall(){at(...ST.hall,()=>{
 const t=realTime;plateName('AI 专家会商',0,-623);
 domains.forEach((s,i)=>TX(s,i<5?-880+i*440:-855+(i-5)*570,i<5?-521:-465,34,1,{align:'center',v:.8}));
 panel(-275,-404,550,88,1,.7,12);TX('FirmBuddy',0,-344,59,1,{align:'center',font:'Georgia'});
 for(let row=0;row<5;row++){
  const rx=1140-row*120,ry=370-row*40,cy=100+row*40,n=[11,11,9,8,7][row],arc=ellipse(0,cy,rx,ry,Math.PI+.045,TAU-.045,90),front=arc.map(([x,y])=>[x,y+43]);
  for(let j=0;j<n;j++){const a=Math.PI+.14+j*(Math.PI-.28)/(n-1),x=Math.cos(a)*(rx-10),y=cy+Math.sin(a)*(ry-12);expertFigure(x,y-30,.69,.1*Math.sin(t+j));}
  solid(pts([...arc,...front.slice().reverse()]),{u:1,w:2,v:.63,th:8});L(arc,1,2.3,.85);L(front,1,1.3,.5);
  for(let j=0;j<n;j++){const a=Math.PI+.14+j*(Math.PI-.28)/(n-1),x=Math.cos(a)*(rx-10),y=cy+Math.sin(a)*(ry-12);panel(x-54,y+5,108,25,1,.4,0);L([[x-28,y+17],[x+28,y+17]],1,1,.24);}
 }
 const ex=[[-730,178,'股东增减持专家','需求','expert1'],[0,198,'解禁预警专家','时机','expert2'],[730,178,'拜访策略专家','切入','expert3']];
 ex.forEach(([x,y,name,role,id],i)=>{
  const u=ep(id,-.6,0),z=ep(id,0,1.4);expertFigure(x,y-48,1.45,u*.8);panel(x-255,y-10,510,90,1,.8,15);TX(name,x,y+49,41,1,{align:'center'});
  const q=[[x,y+90],[x,y+155],[x*.45,329],[0,337]];L(q,u,2.7,.85);
  if(u>0&&z<1){const v=pathPoint(q,z);panel(v[0]-50,v[1]-28,100,56,1,.9,8);TX(role,v[0],v[1]+13,29,1,{align:'center'});}
 });
 // Three inputs drive one common combining shaft; it starts only after the consultation outputs arrive.
 const turn=Math.max(0,t-E.consult)*.7;
 for(const [x,n]of[[-216,24],[-72,24],[72,24],[216,24]])gear(x,646,n,6,(x===-216||x===72)?turn:meshAngle(turn,24,24,[x-144,646],[x,646]),1,.67,18);
 shaft([[-1150,646],[-300,646]],1,.43);shaft([[300,646],[1150,646]],1,.43);bearing(-890,646);bearing(890,646);
 ['知识装备','业务方法','培养试炼'].forEach((s,i)=>{const x=-745+i*745;icon('paper',x,532,.55);TX(s,x+53,541,32,1,{v:.8});});
 machineBase(2400,725);
});}

function industryCell(){at(...ST.industry,()=>{
 plateName('AI 辅助产业研究');machineBase(1730,365);
 const nodes=[[-650,-151,'材料'],[-650,20,'装备'],[-280,-70,'晶体生长'],[150,-70,'衬底'],[610,-70,'外延']];
 const links=[[0,2],[1,2],[2,3],[3,4]];
 links.forEach(([i,j],k)=>{const a=nodes[i],b=nodes[j],q=bez([a[0]+40,a[1]],[a[0]+150,a[1]],[b[0]-150,b[1]],[b[0]-40,b[1]],40);L(q,1,2,.4);L(q,ease(p(realTime,58.7+k*.4,59.6+k*.4)),3,.9);});
 nodes.forEach(([x,y,s],i)=>{C(x,y,42,1,.85,2);icon(i===3?'flag':'chain',x,y,.57);TX(s,x,y+91,34,1,{align:'center'});});
 // A screw-driven inspection lens locates the same customer's substrate node.
 screwRail(-710,680,-275,Math.max(0,realTime-58.4));
 const u=ep('industry',-2,0),x=mix(-650,150,u);panel(x-55,-295,110,41,1,.8,14);L([[x,-254],[x,-170]],1,4,.6);C(x,-70,69,1,.95,3);C(x,-70,77,1,.4,1.4);
 const ref=ep('evidence',-2,0);
 ['年报','专利','财务'].forEach((s,i)=>{const x=-660+i*228,y=228;doc(x-84,y-51,168,102,1,.77);TX(s,x,y+11,31,1,{align:'center'});const z=ease(p(realTime,63.2+i*.55,64.4+i*.55));if(z>0&&z<1)sourceSlip(mix(x,250,z),mix(y,100,z),'paper',.52,Math.sin(Math.PI*z));});
 L([[150,0],[150,100],[250,100]],u,2.5,.8);
 gear(-696,368,24,5,realTime*.48,1,.65,18);gear(-576,368,24,5,meshAngle(realTime*.48,24,24,[-696,368],[-576,368]),1,.6,18);
});}

function knowledgeCell(){at(...ST.knowledge,()=>{
 plateName('AI 按需查证');machineBase(1730,365);
 const labels=['核心规范','监管规则','产品能力','案例经验','研究资料','补充资料'];
 const pulled=ep('drawer',-.8,.4),transfer=ep('retrieve',-2.4,0);
 for(let i=0;i<6;i++){
  const x=-775+i*246;panel(x,-235,218,330,1,.66,22);R(x+12,-222,194,301,1,.35,1.3);
  for(let j=0;j<4;j++){
   const selected=(i===1&&j===1)||(i===3&&j===2)||(i===4&&j===0),d=selected?pulled*54:0,yy=-207+j*70+d*.35;
   panel(x+24,yy,170,51,1,selected?.92:.42,selected?12+d:8);panel(x+82,yy+17,54,10,1,.5,2);
   for(let k=0;k<3;k++)L([[x+35+k*8,yy+12],[x+35+k*8,yy+38]],1,1,.28);
  }
  TX(labels[i],x+109,-274,28,1,{align:'center',v:.8});
 }
 // Gantry X carriage and telescoping gripper extract an evidence strip from the bank.
 screwRail(-760,760,162,Math.max(0,realTime-71.2));
 const x=mix(-420,420,transfer),jaw=1-ease(p(transfer,.8,1));
 panel(x-72,140,144,43,1,.8,15);for(const xx of[x-46,x+46])L([[xx,183],[xx,239]],1,4,.7);
 L([[x-46,239],[x-46+16*jaw,257]],1,3,.9);L([[x+46,239],[x+46-16*jaw,257]],1,3,.9);
 if(pulled>.01&&transfer<1){doc(x-125,206,250,87,1,.9);TX('规则 · 案例 · 研究',x,260,27,1,{align:'center'});}
 drive(-642,368,Math.max(0,realTime-71.2),1,.85);
});}

function assemblyCell(){at(...ST.assembly,()=>{
 plateName('AI 整理沟通准备');machineBase(1750,365);conveyor(-770,760,234,Math.max(0,realTime-84));
 const ids=['page1','page2','page3'],titles=['关注依据','沟通重点','跟进安排'];
 titles.forEach((s,i)=>{
  const u=ep(ids[i],-1.3,0),x=mix(-180,380,u),y=mix(-40,110,u),alpha=1-ease(p(u,.85,1));
  if(realTime>=E[ids[i]]-1.3&&alpha>.01)inkLayer(alpha,()=>{doc(x-150,y-60,300,120,1,.85);TX(s,x,y+10,35,1,{align:'center'});});
  const z=ep(ids[i],0,.45);inkLayer(z,()=>{const yy=-228+i*77;icon(['flag','person','clock'][i],-605,yy,.55);TX(s,-550,yy+11,31,1,{v:.9});check(-344,yy,.7);});
 });
 // Eccentric-driven press, with a mechanical interlock actuated by the human reviewer.
 const down=p(realTime,91.6,93.2);
 const press=stampPress(380,-220,realTime,down);
 panel(220,208,320,22,1,.75,16);
 const approval=ep('human',-.6,0);expertFigure(-655,92,1.2,approval);
 TX('人工审阅',-624,194,30,1,{align:'center'});
 const leverA=mix(-1.2,0,approval);C(-506,195,15,1,.9,2);L([[-506,195],[-506+95*Math.cos(leverA),195+95*Math.sin(leverA)]],1,7,.9);C(-506+95*Math.cos(leverA),195+95*Math.sin(leverA),11,1,.9,2);
 const gateY=mix(95,-80,approval);panel(615,gateY,23,132,1,.8,12);L([[626,gateY],[626,-94]],1,3,.6);
 drive(-550,368,Math.max(0,realTime-84),1,.8);
});}

function followCell(){at(...ST.follow,()=>{
 plateName('记录回流 · 持续跟进');machineBase(1730,365);conveyor(-760,750,234,Math.max(0,realTime-99.2));
 expertFigure(-600,19,1.65,.4);expertFigure(-335,19,1.65,.4);
 // The speech shape becomes structured lines on a record sheet, not a claim of a completed sale.
 const u=ep('record',-1.8,0),z=ep('record',0,.7);
 inkLayer(1-z,()=>{L([[-630,-170],[-303,-170],[-303,-65],[-423,-65],[-454,-30],[-454,-65],[-630,-65],[-630,-170]],1,2,.8);detail(-596,-139,235,3);});
 const x=mix(-465,430,u),y=mix(-105,70,u);
 if(u>0&&z<1)inkLayer(1-z,()=>{doc(x-100,y-65,200,130,1,.9);detail(x-74,y-31,145,4);});
 const pin=ep('record',-.3,.2);L([[430,-220],[430,-92]],pin,4,.85);C(430,-220,13,1,.9,2);panel(392,-244,76,24,1,.8,10);
 inkLayer(z,()=>{check(635,95,1.2);TX('沟通记录',430,-151,34,1,{align:'center'});});
 drive(-563,368,Math.max(0,realTime-99.2),1,.85);
});}

function overlay(){
 const ctx=ov,t=realTime,shot=plan.shots.find(s=>t>=s.start&&t<s.end);if(!shot)return;
 const a=ease(p(t,shot.start+.5,shot.start+1.1))*(1-ease(p(t,shot.end-.7,shot.end-.1)));
 if(t<113&&a>0){ctx.save();ctx.scale(scale,scale);ctx.globalAlpha=a;const grad=ctx.createLinearGradient(0,963,0,1080);grad.addColorStop(0,'#071b3000');grad.addColorStop(.55,'#071b30c9');grad.addColorStop(1,'#071b30df');ctx.fillStyle=grad;ctx.fillRect(0,963,1920,117);ctx.textAlign='center';ctx.font=`400 34px ${FONT}`;ctx.fillStyle='#e0eef7';ctx.fillText(shot.benefit,960,1033);ctx.restore();}
 if(t>=113){const a=ease(p(t,113,114.4));ctx.save();ctx.scale(scale,scale);ctx.globalAlpha=a;
  const grad=ctx.createLinearGradient(0,0,0,260);grad.addColorStop(0,'#071b30');grad.addColorStop(.8,'#071b30ee');grad.addColorStop(1,'#071b3000');ctx.fillStyle=grad;ctx.fillRect(0,0,1920,260);
  ctx.textAlign='center';ctx.fillStyle='#eef5fa';ctx.font='700 60px Georgia';ctx.fillText('FirmBuddy',960,101);ctx.font=`400 37px ${FONT}`;ctx.fillText('AI 辅助准备，业务专注判断',960,174);
  ctx.font=`400 31px ${FONT}`;ctx.fillText('少搜资料       少做拼接       多做研判',960,1011);ctx.restore();
 }
}

// Continuous paper cinematography: follow the same dossier between dedicated work cells.
const cameraKeys=[
 [0,1200,1100,.96,-.008],[9.6,1200,1100,.96,0],[21.6,1200,1100,.96,0],
 [24,1450,1180,.94,0],[25.5,2650,1180,.88,-.014,980,0,0,0],[27.2,3500,1100,.94,0],[39.6,3500,1100,.94,0],
 [41.6,4920,1320,.71,.013,1100,40,-.02,0],[43.6,6200,1160,.66,0],[54.4,6200,1160,.66,0],
 [56.2,7550,1230,.70,-.016,1000,-20,.02,0],[58.4,9000,1100,.94,0],[67.2,9000,1100,.94,0],
 [69.2,10020,2490,.72,.026,0,1100,0,0],[71.2,9000,3600,.94,0],[80,9000,3600,.94,0],
 [82,7550,3690,.83,-.016,-1100,0,0,0],[84,6200,3600,.94,0],[96,6200,3600,.94,0],
 [97.6,4900,3670,.83,.016,-1100,0,0,0],[99.2,3500,3600,.94,0],[104,3500,3600,.94,0],
 [108,1000,3350,.66,-.016,-400,-650,-.02,0],[112,1450,1220,.84,0],[113,1450,1220,.84,0],
 [116.6,5500,2550,.161,0],[120,5500,2550,.161,0]
];
function sampleCamera(t){let i=1;while(i<cameraKeys.length-1&&t>cameraKeys[i][0])i++;const a=cameraKeys[i-1],b=cameraKeys[i],h=b[0]-a[0],u=p(t,a[0],b[0]),c={};for(const[j,k]of['x','y','z','r'].entries()){const v=j===2?Math.log(a[j+1]):a[j+1],w=j===2?Math.log(b[j+1]):b[j+1];c[k]=quint(v,w,a[j+5]||0,b[j+5]||0,h,u);if(j===2)c[k]=Math.exp(c[k]);}return c;}
const cells=[['intake',intake],['collect',collect],['hall',hall],['industry',industryCell],['knowledge',knowledgeCell],['assembly',assemblyCell],['follow',followCell]];
window.renderAt=(t,type='image/png',quality=.95)=>{
 realTime=Math.max(0,Math.min(plan.duration,t));T=realTime;bounds=[];const c=sampleCamera(realTime);setCam({...c,z:c.z*scale});proj.k=.43;clear();NIBS.length=0;
 machineChassis();for(const[name,draw]of cells){const[x,y]=ST[name];if(localVisible(x,y,name==='hall'?1500:1150,name==='hall'?950:650))draw();}
 caseDossier();overlay();compose(inkC,fxC,ovC,{sheet:[11200,5300],cam,seed:19});return type?canvas.toDataURL(type,quality):null;
};
window.cameraAt=sampleCamera;window.caseAt=caseState;
window.stateAt=t=>{window.renderAt(t,null);return{time:t,camera:sampleCamera(t),case:caseState(t),buffer:[W,H],duration:120,shot:plan.shots.find(s=>t>=s.start&&t<s.end)?.id,bounds,caseId:'A01'};};
window.design={cameraKeys,shots:plan.shots,duration:plan.duration};window.__ready=true;window.renderAt(0,null);
const audio=new Audio('./audio/mix.wav'),seek=document.querySelector('#seek'),display=document.querySelector('#time'),button=document.querySelector('#play');let playing=false,started=0,base=0;
seek.max=120;seek.oninput=()=>{base=+seek.value;audio.currentTime=base;started=performance.now();window.renderAt(base,null);display.textContent=base.toFixed(2)+' / 120';};
button.onclick=()=>{playing=!playing;button.textContent=playing?'暂停':'播放';if(playing){base=+seek.value;if(base>=120)base=0;started=performance.now();audio.currentTime=base;audio.play().catch(()=>{});}else{base=+seek.value;audio.pause();}};
function tick(){if(playing){const t=Math.min(120,base+(performance.now()-started)/1000);window.renderAt(t,null);seek.value=t;display.textContent=t.toFixed(2)+' / 120';if(t>=120){playing=false;audio.pause();button.textContent='播放';}}requestAnimationFrame(tick);}if(!Q.has('render'))tick();
