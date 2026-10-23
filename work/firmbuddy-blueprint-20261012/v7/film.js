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
function carrier(q,u,label='',w=196){const [x,y]=pathPoint(q,u);at(x+ox,y+oy,()=>{doc(-w/2,-52,w,104,1);C(-w/2+16,-35,5,1,.75,1);if(label)TX(label,0,15,30,1,{align:'center'});else detail(-w/2+32,-13,w-56,3);});return[x,y];}
function rail(q,v=.46){
 L(q.map(([x,y])=>[x,y-24]),1,2.3,v);L(q.map(([x,y])=>[x,y+24]),1,2.3,v);L(q.map(([x,y])=>[x,y+45]),1,1.2,v*.7);L(q,1,1,v*.5,'center');
 let acc=0,next=0;for(let i=1;i<q.length;i++){const a=q[i-1],b=q[i],len=Math.hypot(b[0]-a[0],b[1]-a[1]);while(next<=acc+len){const u=(next-acc)/(len||1),x=mix(a[0],b[0],u),y=mix(a[1],b[1],u);C(x,y,7,1,v,1.3);if(Math.round(next/90)%4===0){R(x-16,y-33,32,88,1,v,1.2);L([[x,y+55],[x,y+120]],1,1.5,v*.6);R(x-28,y+120,56,12,1,v*.6,1);}next+=90;}acc+=len;}
}
function plaque(s,x,y,w,size=42,u=1){const h=Math.max(80,size*1.65);panel(x,y,w,h,u,.9,8);R(x+7,y+7,w-14,h-14,u,.4,1);for(const a of[x+12,x+w-12]){C(a,y+12,3,u,.8,1);C(a,y+h-12,3,u,.8,1);}TX(s,x+w/2,y+h*.7,size,u,{align:'center'});}
function pointer(x,y){L([[x-18,y-8],[x,y],[x-18,y+8]],1,1.6,.55);}
function movingRoute(q,start,end){route(q,start,end,3.5,.95);if(T>=start&&T<=end)carrier(q,ease(p(T,start,end)),'',146);}
function frameBase(x,y,w,h){R(x,y,w,h,1,.42,1.7);truss(x,y+h+32,x+w,y+h+32,Math.max(4,Math.round(w/130)));for(const xx of[x,x+w]){L([[xx,y+h],[xx,y+h+120]],1,2,.48);panel(xx-40,y+h+115,80,24,1,.4,10);bolt(xx-24,y+h+126);bolt(xx+24,y+h+126);}}
function intro(){at(...centers.intro,()=>{
 mono('FIRMBUDDY / CLIENT OPERATIONS',-670,-378,24,1,{v:.6});TX('一句业务问题，启动专业协作',-670,-300,50,1);
 const labels=['商机查询','业务答疑','拜访准备'];
 labels.forEach((s,i)=>{const y=-133+i*170,u=show(.2+i*.16);plaque(s,-650,y-53,300,43,u);solid(pts([[-316,y-47],[-230,y-47],[-249,y+2],[-296,y+2]]),{u,v:.7,w:2,th:12});gear(-267,y+60,18,4,T*.8,u,.65,12);shaft([[-217,y+60],[510,y+60]],u,.55);for(let j=0;j<6;j++)C(-140+j*107,y+60,6,u,.5,1);bearing(120,y+60,u);pointer(456,y+60);});
 TX('自然语言 · 随时进入',-650,387,35,show(1),{v:.85});
 if(T<5.8){const u=ease(p(T,1.2,5.8));carrier([[-110,-73],[510,-73],...paths.query.slice(1).map(([x,y])=>[x-1050,y-1070])],u,'示例客户',222);}
 });}
function signals(){at(...centers.signals,()=>{
 TX('从信息中，筛出值得核实的线索',-730,-335,46,1);mono('01 / SOURCE FILTER',-730,-390,22,1,{v:.5});
 frameBase(-685,-245,1380,475);rail([[-720,50],[700,50]],.5);
 for(let i=0;i<4;i++){doc(-663+i*88,-197,70,120,1,.42);detail(-653+i*88,-171,49,4);}
 TX('市场信息 / 客户名单',-663,-223,28,1,{v:.7});
 const ca=[-392,52],cb=[-147,52],angle=T*.7;
 gear(...ca,30,10,angle,1,.85,25);gear(...cb,19,10,meshAngle(angle,30,19,ca,cb),1,.8,25);
 const scan=mix(-620,-63,ease(p(T,5.1,6.3)));if(T>5&&T<6.5){L([[scan,-210],[scan,225]],1,2.6,.9,'phantom');C(scan,-210,8);}
 doc(130,-208,532,393,1,.85);mono('CANDIDATE / DEMO',165,-158,20,1,{v:.55});
 TX('扩产相关披露',165,-79,49,show(5.9));L([[165,-43],[620,-43]],show(6),1.4,.5);
 TX('待核实',165,24,43,show(6.1));TX('保留来源 · 再做研判',165,93,33,show(6.3));
 TX('流程示例',165,148,27,show(6.4),{v:.7});
 });if(T>8.4&&T<11.7)movingRoute(paths.toHall,8.4,11.7);}
function experts(){at(...centers.experts,()=>{
 TX('数十位 AI 专家 · 按议题协作',0,-622,55,1,{align:'center'});
 // System taxonomy is a separate nine-domain directory above the auditorium.
 domains.forEach((s,i)=>{const x=-1070+(i%3)*735,y=-520+Math.floor(i/3)*65;TX(s,x,y,43,1,{v:.92});if(i%3<2)L([[x+640,y-34],[x+640,y+8]],1,1,.4);});
 L([[-1110,-336],[1110,-336]],1,1.5,.45);
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
 const chosen=[[-720,97,'产业链洞察'],[0,-121,'财务诊断'],[720,97,'拜访策略']];
 chosen.forEach(([x,y,s],i)=>{const u=show(12.1+i*.4,.4);panel(x-52,y-34,104,63,u,1,10);plaque(s,x-175,y-149,350,43,u);route([[x,y+30],[x*.65,260],[0,365]],12.7+i*.4,14+i*.4,2.8,.92);});
 doc(-266,307,532,142,1);TX('扩产，就一定需要融资吗？',0,364,36,show(13),{align:'center'});TX('示例议题',0,415,26,show(13.1),{align:'center',v:.6});
 mono('DISCUSS / RETRIEVE / VERIFY',-1110,610,23,1,{v:.55});
 });if(T>=16.3&&T<=20.6)movingRoute(paths.knowledge,16.3,20.6);}
function cabinet(x,y,s,i){
 panel(x,y,204,350,1,.68,32);R(x+13,y+15,178,315,1,.4,1.3);
 for(let j=0;j<5;j++){panel(x+22,y+36+j*53,160,43,1,.55,8);R(x+76,y+48+j*53,53,12,1,.45,1);for(let k=0;k<4;k++)L([[x+31+k*7,y+44+j*53],[x+31+k*7,y+67+j*53]],1,1,.25);}
 TX(s,x+102,y-30,33,1,{align:'center',v:.85});mono(String(i+1).padStart(2,'0'),x+101,y+391,21,1,{align:'center',v:.45});
}
function knowledge(){at(...centers.knowledge,()=>{
 TX('知识库 · 已装配的专业资料',-730,-359,48,1);mono('02 / EVIDENCE · SECTION A–A',-730,-410,21,1,{v:.5});
 frameBase(-728,-224,1438,397);
 ['项目资料','研究资料','业务规范','交易结构','风险合规','案例档案'].forEach((s,i)=>cabinet(-714+i*238,-190,s,i));
 const cut=mix(-740,740,ease(p(T,19.9,21.4)));
 if(T<21.4){panel(Math.max(-728,cut),-224,710-Math.max(-728,cut),397,1,.5,16);if(cut<0){TX('预先装配 / 按范围检索',-460,5,44,1);}}
 if(T>=19.9&&T<21.4){L([[cut,-256],[cut,210]],1,2.7,.95,'phantom');TX('A',cut-20,-275,28);}
 const u=ease(p(T,21.4,22.5));
 if(u>0){
   const x=mix(-693,-593,u),y=mix(-153,-162,u),ww=mix(160,623,u),hh=mix(120,303,u);
   L([[-616,-148],[x+ww/2,y+hh]],1,1.3,.4,'hidden');
   for(let i=2;i>0;i--)doc(x+i*13,y-i*12,ww,hh,1,.4);doc(x,y,ww,hh,1);
   TX('示例资料 · 扩产计划',x+28,y+65,39,show(22.2));L([[x+28,y+90],[x+ww-28,y+90]],show(22.3),1,.45);
   TX('资金安排未提供',x+28,y+164,48,show(22.5));TX('保留来源 / 不补造事实',x+28,y+229,30,show(22.7),{v:.75});
 }
 if(T>=23.1){panel(129,-109,559,222,show(23.1),1,10);TX('先核实',156,-45,43,show(23.2));TX('资金来源与缺口',156,25,46,show(23.4));TX('依据：资金信息缺失',156,77,30,show(23.5),{v:.75});route([[33,-10],[128,-10]],22.8,23.4,3);}
 TX('可见范围内检索 · 引用可回查',-730,305,34,1,{v:.8});
 });if(T>=25.8&&T<=29.1)movingRoute(paths.output,25.8,29.1);}
function visit(){at(...centers.visit,()=>{
 TX('把信息缺项，变成拜访提问',-730,-379,49,1);mono('03 / OUTPUT CARRIAGE',-730,-432,21,1,{v:.5});
 frameBase(-734,-251,1458,510);shaft([[-721,-184],[720,-184]],1,.6);
 for(let x=-700;x<700;x+=29)L([[x,-199],[x+17,-169]],1,1.2,.4);bearing(-701,-184);bearing(700,-184);
 doc(-50,-123,738,328,1);TX('拜访策略包',-12,-65,43,1);L([[-12,-40],[645,-40]],1,1.2,.5);
 const x=mix(-492,243,ease(p(T,29.4,31.2))),u=1-ease(p(T,31.1,31.6));
 panel(x-100,-218,200,67,1,.6,16);bolt(x-76,-195);bolt(x+76,-195);L([[x,-151],[x,-32]],1,2,.5);
 if(u>.01){panel(x-245,-22,490,85,1,u);TX('资金安排待核实',x,35,41,1,{align:'center',v:u});}
 TX('资金怎么安排？',-12,35,47,show(31.2));TX('何时落地？谁参与决策？',-12,116,39,show(31.8));TX('目标 · 提问 · 话术材料',-12,173,32,show(32.2),{v:.8});
 gear(-530,134,26,7,T*.45,1,.68,24);gear(-376,134,18,7,meshAngle(T*.45,26,18,[-530,134],[-376,134]),1,.6,20);
 ['商机诊断','销售陪练','客户经营计划'].forEach((s,i)=>plaque(s,-734+i*498,286,468,39,show(32.8+i*.2)));
 TX('按需生成',-730,267,25,show(32.8),{v:.7});
 },mix(1,.18,ease(p(T,35,37))*(1-ease(p(T,43.8,45)))));if(T>=35&&T<=37.5)movingRoute(paths.task,35,37.5);}
function follow(){if(T<35)return;at(...centers.follow,()=>{
 TX('确认后，创建跟进任务',-450,-300,49,1);mono('04 / CONFIRM · FOLLOW THROUGH',-450,-353,21,1,{v:.5});
 // Confirmation is a gate only for task creation, not for reading or querying.
 plaque('用户确认',-580,-152,375,42,1);gear(-145,-21,24,6,T*.25,1,.67,20);
 const a=mix(-1.08,0,ease(p(T,37.4,37.9)));L([[-145,-21],[-145+Math.cos(a)*150,-21+Math.sin(a)*150]],1,7,.9);C(-145+Math.cos(a)*150,-21+Math.sin(a)*150,17,1,.95,2.5);
 shaft([[12,-21],[220,-21]],1,.6);
 if(T>=37.9){C(63,-21,29,show(37.9));L([[46,-22],[60,-6],[83,-40]],show(37.9),3.5);}
 doc(173,-162,466,240,show(38));TX('跟进任务',205,-85,48,show(38.1));TX('待跟进',205,-14,37,show(38.3));TX('用户确认后创建',205,39,28,show(38.4),{v:.8});
 doc(-563,162,1202,129,show(39));TX('用户记录 → 更新商机判断',-528,241,43,show(39.2));
 TX('示例：补问资金安排',-563,350,31,show(39.4),{v:.8});
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
   const u=show(44,.7);plaque('三种入口',880,470,1120,127,u);plaque('线索筛选',2450,660,1140,127,u);
   plaque('专家协作',5130,325,1240,136,u);plaque('知识库',3050,2240,1250,144,u);
   plaque('方案与行动',5600,2370,1400,142,u);plaque('记录反馈',3390,3890,1350,136,u);
 }
 // Same-sheet title block. No sudden brand push and no lifecycle grid.
 const u=show(46,.8);if(u>0){panel(1240,4180,6660,390,u,.9,0);R(1270,4210,6600,330,u,.4,1);L([[3260,4210],[3260,4540]],u,2,.5);TX('FirmBuddy',1420,4423,271,u,{font:'Georgia',weight:700});TX('把业务问题，变成有依据的行动',3480,4375,141,u);TX('券商客户经营 · AI 专家协作平台',3480,4490,94,u,{v:.75});}
 });}
// Music-only edition: business labels remain in world space.
function caption(){}
window.renderAt=(t,type='image/png',quality=.95)=>{T=Math.max(0,Math.min(52,t));bounds=[];const c=cameraAt(T);setCam({...c,z:c.z*scale});proj.k=.43;clear();NIBS.length=0;chassis();intro();signals();experts();knowledge();visit();follow();caption();compose(inkC,fxC,ovC,{sheet:[8200,4800],cam,seed:19});return type?canvas.toDataURL(type,quality):null;};
window.cameraAt=cameraAt;window.cameraKeys=keys;
window.stateAt=t=>{window.renderAt(t,null);return{time:t,camera:cameraAt(t),buffer:[W,H],duration:52,shot:plan.shots.find(s=>t>=s.start&&t<s.end)?.id,bounds,subjects:{query:pathPoint(paths.toHall,ease(p(t,8.4,11.7))),evidence:pathPoint(paths.knowledge,ease(p(t,16.3,20.6))),gap:pathPoint(paths.output,ease(p(t,25.8,29.1))),feedback:pathPoint(paths.feedback,feedbackProgress(t))}};};
window.__ready=true;window.renderAt(0,null);
const audio=new Audio('./audio/mix.wav'),seek=document.querySelector('#seek'),display=document.querySelector('#time'),button=document.querySelector('#play');let playing=false,started=0,base=0;
seek.oninput=()=>{base=+seek.value;audio.currentTime=base;started=performance.now();window.renderAt(base,null);display.textContent=base.toFixed(2)+' / 52';};
button.onclick=()=>{playing=!playing;button.textContent=playing?'暂停':'播放';if(playing){base=+seek.value;if(base>=52)base=0;started=performance.now();audio.currentTime=base;audio.play().catch(()=>{});}else{base=+seek.value;audio.pause();}};
function tick(){if(playing){const t=Math.min(52,base+(performance.now()-started)/1000);window.renderAt(t,null);seek.value=t;display.textContent=t.toFixed(2)+' / 52';if(t>=52){playing=false;audio.pause();button.textContent='播放';}}requestAnimationFrame(tick);}if(!Q.has('render'))tick();
