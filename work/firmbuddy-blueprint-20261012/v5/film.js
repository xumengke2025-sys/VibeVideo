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
const centers={intro:[2000,1000],signals:[2000,2050],experts:[4050,1950],knowledge:[4050,3250],visit:[6100,3250],follow:[6200,1700]};
const signalSlider=t=>[mix(1340,1850,ease(p(t,5.3,7.2))),2000];
const evidencePath=[[4136,3278],[4350,3278],[4350,3340],[4470,3340]];
const evidenceFront=t=>trunc(evidencePath,p(t,25,26.6))[1]||evidencePath.at(-1);
const gapCarriage=t=>[mix(5650,6010,ease(p(t,30.3,32.4))),mix(3250,3235,ease(p(t,30.3,32.4)))];
// Four sections use motivated hard cuts; continuous motion follows a scan, shaft, citation or carriage.
const keys=[
 [0,2000,1000,1.02,0],[3.8,2000,1000,1.02,0],[4.999,1950,1400,1.04,-.018],
 [5,1700,2050,1.25,0],[5.3,1700,2050,1.25,0],[7.2,2210,2050,1.05,0],[7.9,2000,2050,1.05,0],[10.1,2000,2050,1.05,0],[10.999,3000,2030,1.1,.025],
 [11,3600,1985,2.05,0],[12.2,3740,1985,1.85,0],[13.3,3900,1970,1.38,0],[14.3,4050,1930,1.02,0],[18.1,4050,1930,1.02,0],
 [18.999,4170,2750,1.25,-.018],[19,4050,3250,1.02,0],[24.9,4050,3250,1.02,0],[26.6,4160,3280,1.05,0],[28.999,4160,3280,1.05,0],
 [29,6100,3250,1.02,0],[30.3,6000,3250,1.06,0],[32.4,6100,3250,1.02,0],[36.2,6100,3250,1.02,0],
 [36.999,6200,2430,1.12,.02],[37,6200,1700,1.02,0],[41.1,6200,1700,1.02,0],[42.2,6100,1830,.92,0],[43.8,6100,1830,.92,0],
 [45.1,4230,2380,.26,0],[47.5,4230,2380,.26,0],[49.6,4250,4230,1.13,0],[52,4250,4230,1.13,0]
];
function cameraAt(t){let a=keys[0],b=keys[1];for(let i=1;i<keys.length;i++){b=keys[i];if(t<=b[0])break;a=b;}const u=ease(p(t,a[0],b[0]));const c={x:mix(a[1],b[1],u),y:mix(a[2],b[2],u),z:Math.exp(mix(Math.log(a[3]),Math.log(b[3]),u)),r:mix(a[4],b[4],u)};
  if(t>=5.3&&t<7.2)c.x=signalSlider(t)[0]+360;
  if(t>=25&&t<26.6){const v=ease(p(t,25,26.6));c.x=mix(4050,Math.max(4050,evidenceFront(t)[0]-310),v);c.y=mix(3250,3280,v);}
  if(t>=30.3&&t<32.4)c.x=gapCarriage(t)[0]+350-mix(0,260,ease(p(t,30.3,32.4)));
  return c;
}
function intro(){at(...centers.intro,()=>{
  mono('FIRMBUDDY / MECHANISM OF CLIENT OPERATIONS',-700,-344,22,1,{v:.5});
  TX('firmbuddy',-700,-193,105,1,{font:'Arial',weight:700});TX('券商客户经营 · AI专家平台',-700,-117,43,1);
  L([[-700,-74],[690,-74]],show(.25),1.5,.45);
  const names=['查商机','问业务','备拜访'];
  names.forEach((s,i)=>{const x=-475+i*475,u=show(.5+i*.2);C(x,52,89,u,.8,2.5);C(x,52,72,u,.38,1);center(x,52,110,u);TX(s,x,68,39,u,{align:'center'});for(let j=0;j<12;j++){const a=j*TAU/12;L([[x+Math.cos(a)*94,52+Math.sin(a)*94],[x+Math.cos(a)*105,52+Math.sin(a)*105]],u,1.2,.4);}L([[x,156],[x,209]],u,2,.55);bolt(x-123,52,u);bolt(x+123,52,u);});
  shaft([[-475,209],[475,209]],show(1.5),.6);panel(-446,237,892,73,show(2));mono('>',-421,286,30,show(2));TX('一句问题 · 随时进入',0,287,41,show(2.3),{align:'center'});
  route([[475,209],[775,209],[775,900],[250,900]],3.4,5.6);mono('NATURAL LANGUAGE / INPUT',-700,347,17,show(2),{v:.35});
});}
function signals(){at(...centers.signals,()=>{
  const u=show(5);TX('查询 / 监测',-685,-330,49,u);mono('01 · SIGNAL FILTER',690,-330,20,u,{align:'right',v:.45});
  TX('市场事件',-690,-243,32,u);TX('客户名单',-690,74,32,u);
  for(let row=0;row<2;row++){const yy=-204+row*314;R(-712,yy,647,147,u,.38,1.8);for(let j=0;j<6;j++){const x=-686+j*99;doc(x,yy+20,76,100,u,.4);detail(x+11,yy+57,55,3,u);}gear(-715,yy+73,16,4,toothAngle(T)*2,u,.5,10);gear(-46,yy+73,16,4,-toothAngle(T)*2,u,.5,10);L([[-681,yy+138],[-65,yy+138]],u,1,.3,'center');}
  const slide=signalSlider(T)[0]-2000;
  if(T>=5.3&&T<7.2){L([[slide,-217],[slide,266]],1,2.6,.9);C(slide,-217,12,1,.8,2);C(slide,266,12,1,.8,2);}
  route([[-34,-131],[65,-131],[65,-12],[164,-12]],6.8,7.8);
  panel(175,-239,525,474,show(7.3),1,28);for(const x of[193,682])for(const y of[-221,217])bolt(x,y,show(7.3));
  mono('CANDIDATE / SOURCE',208,-186,20,show(7.7),{v:.5});TX('扩产相关披露',208,-104,47,show(8));
  L([[208,-70],[663,-70]],show(8),1,.4);TX('待核实',208,9,44,show(8.4));TX('保留来源 · 再做研判',208,72,31,show(8.6));
  R(208,113,310,68,show(9),.7,1.4);TX('查看来源 →',230,161,34,show(9));spec(-680,322,u);
  dim(-682,301,615,'QUERY / WATCHLIST',u);shaft([[702,0],[1130,0]],show(9.5));bearing(850,0,show(9.5));route([[702,0],[1580,0]],9.6,11.8);
});}
function experts(){at(...centers.experts,()=>{
  const u=show(10.1);TX('数十位 · 多领域AI专家',0,-324,44,show(13.5),{align:'center'});
  // Socket bank conveys scale without representing real people or implying every expert is selected.
  for(let i=0;i<56;i++){const x=-690+(i%14)*99,y=-274+Math.floor(i/14)*26;R(x,y,73,17,show(13.4+i*.009),.32,1);C(x+10,y+8,3,show(13.4),.45,1);}
  const c1=[-450,35],c2=[-130,35],c3=[70,35],a1=toothAngle(T),a2=meshAngle(a1,40,24,c1,c2),a3=meshAngle(a2,24,16,c2,c3);
  truss(-720,231,693,231,14,u);shaft([[-745,35],[697,35]],u,.3);bearing(-714,35,u);bearing(284,35,u);
  gear(...c1,40,10,a1,u);gear(...c2,24,10,a2,show(10.35));gear(...c3,16,10,a3,show(10.55));
  leader('行业研究',[[-546,124],[-650,259],[-650,285]],show(13.4),38);TX('看扩产逻辑',-650,329,29,show(14),{v:.8});
  leader('财务诊断',[[-139,142],[-229,260],[-229,285]],show(14),38);TX('查资金安排',-229,329,29,show(14.4),{v:.8});
  leader('资本运作',[[128,90],[180,183],[180,285]],show(14.5),38);TX('研判服务方向',180,329,29,show(15),{v:.8});
  panel(385,-128,318,310,show(15.7),1,26);bolt(403,-110,show(15.7));bolt(685,164,show(15.7));
  mono('OUTPUT',411,-74,18,show(15.7),{v:.5});TX('候选线索',409,-9,37,show(16));TX('＋',535,52,38,show(16),{align:'center'});TX('待核实问题',409,112,37,show(16.3));
  route([[293,35],[385,35]],15.4,16.2);mono('专业匹配 / 互补协作',-688,-386,22,show(14.2),{v:.5});spec(395,225,show(16.3));
  shaft([[175,35],[175,715],[0,715],[0,923]],show(17));truss(215,183,215,1040,9,show(17));route([[175,35],[175,715],[0,715],[0,1060]],17.1,20.4);
});}
function cartridge(x,y,w,h,title,u=1,v=1){panel(x,y,w,h,u,v,14);for(let i=0;i<3;i++)L([[x+12,y+h+5+i*5],[x+w-12,y+h+5+i*5]],u,1,v*.3);R(x+12,y+14,w-24,19,u,v*.4,1);C(x+w/2,y+58,8,u,v*.65,1.4);L([[x+w/2-16,y+72],[x+w/2+16,y+72]],u,1,v*.6);TX(title,x+w/2,y+h-18,30,u,{align:'center',v});}
function knowledge(){at(...centers.knowledge,()=>{
  const u=show(19);TX('有扩产计划，就有融资需求吗？',-690,-330,43,u);
  mono('02 · KNOWLEDGE / SECTION A–A',-690,-381,20,u,{v:.45});
  const x0=-690,y0=-247,w=799,h=459,cut=mix(x0-20,x0+w+20,ease(p(T,20.5,22.6)));
  R(x0,y0,w,h,u,.85,2.8);R(x0+19,y0+19,w-38,h-38,u,.4,1.3);
  for(let row=0;row<2;row++)for(let col=0;col<3;col++)cartridge(-657+col*246,-214+row*177,218,147,['项目资料','研究资料','业务规范','交易结构','风险合规','案例档案'][row*3+col],u,.65);
  for(const y of[-51,124]){L([[-671,y],[93,y]],u,1.5,.4);hatch(pts(rect(-680,y,99,y+12)),{u,v:.22,sp:9});}
  // Right shell occludes the already-configured interior until the section plane passes.
  if(cut<x0+w){panel(Math.max(x0,cut),y0,x0+w-Math.max(x0,cut),h,u,.7,25);if(cut<x0+220){TX('知识库',-536,-43,59,u);TX('专家已装配',-536,34,35,u);mono('ACTIVE LOADOUT',-536,94,19,u,{v:.5});}}
  if(T>=20.5&&T<23){L([[cut,y0-45],[cut,y0+h+45]],1,2.5,.9,'phantom');mono('A',cut-29,y0-56,29,1);mono('A',cut-29,y0+h+75,29,1);}
  // Selected source page separates from an existing cartridge, not newly trained knowledge.
  const e=ease(p(T,22.7,24.2)),px=-639+405*e,py=-208+69*e;
  if(e>0){L([[-548,-129],[px+140,py+80]],1,1,.4,'hidden');for(let k=2;k>0;k--)doc(px+k*13,py-k*11,320,270,1,.3);doc(px,py,320,270,1);mono('REF / DEMO',px+22,py+40,18,show(23),{v:.55});TX('示例资料',px+22,py+92,32,show(23.2));TX('扩产计划',px+22,py+147,36,show(23.4));TX('资金安排未提供',px+22,py+205,30,show(23.8));dim(px,py+300,320,'SOURCE / VERSION',1);}
  TX('知识库 · 多类资料',-690,278,35,show(22.8));mono('预先装配 / 可见范围内检索',-690,319,21,show(22.8),{v:.5});
  panel(255,-216,445,143,show(24),1,26);TX('财务诊断 · AI专家',277,-154,36,show(24.1));mono('EVIDENCE / RETRIEVAL',277,-107,18,show(24.1),{v:.5});
  gear(173,-140,16,5,-toothAngle(T),show(24),.6,16);shaft([[118,-140],[254,-140]],show(24),.4);
  const q=evidencePath.map(([x,y])=>[x-4050,y-3250]);route(q,25,26.6);
  panel(245,31,455,192,show(26.1),1,22);TX('先核实',271,89,37,show(26.4));TX('资金来源与缺口',271,151,43,show(26.6));TX('依据：资金信息缺失',271,197,27,show(26.8),{v:.75});
  spec(255,300,u);shaft([[700,135],[1260,135]],show(27));bearing(852,135,show(27));route([[700,135],[1450,135]],27.6,30);
});}
function visit(){at(...centers.visit,()=>{
  const u=show(29);TX('帮我准备这次拜访',-690,-332,48,u);mono('03 · VISIT CARRIAGE',690,-333,20,u,{align:'right',v:.5});
  R(-712,-255,1434,518,u,.25,1.6);for(const x of[-695,704])for(const y of[-238,245])bolt(x,y,u);
  // Lead screw, sliding block and fixed frame share paper coordinates.
  shaft([[-700,-174],[700,-174]],u,.55);for(let x=-674;x<690;x+=23)L([[x,-187],[x+12,-162]],u,1,.35);bearing(-680,-174,u);bearing(678,-174,u);
  truss(-712,283,722,283,14,u);doc(-11,-121,714,363,show(29.4));mono('VISIT STRATEGY',19,-77,20,show(29.4),{v:.5});
  const gap=gapCarriage(T),x=gap[0]-6100,y=gap[1]-3250;
  panel(x-95,-207,190,65,show(29.7),.6,18);bolt(x-78,-186,show(29.7));bolt(x+78,-186,show(29.7));L([[x,-142],[x,y-36]],show(29.7),2,.6);
  if(T<32.4){panel(x-212,y-36,424,84,show(29.7));TX('资金安排待核实',x,y+20,37,show(29.8),{align:'center'});}
  else{TX('资金怎么安排？',23,7,46,1);L([[23,31],[656,31]],1,1.3,.5);}
  TX('何时落地？',23,87,43,show(33));L([[23,111],[656,111]],show(33),1,.35);TX('谁参与决策？',23,169,43,show(33.4));
  gear(-520,143,24,5,toothAngle(T),u,.55,14);leader('拜访策略包',[[-500,83],[-309,-43],[-309,-70]],show(32.5),40);
  TX('目标',-353,101,38,show(34));TX('提问',-353,163,38,show(34.3));TX('话术材料',-353,225,38,show(34.6));
  spec(-684,337,u);shaft([[705,34],[862,34],[862,-900]],show(35));route([[705,34],[862,34],[862,-1160],[510,-1160]],35.1,38.5);
});}
function follow(){at(...centers.follow,()=>{
  const u=show(37);TX('持续经营 · 把反馈接回行动',-690,-334,46,u);mono('04 · FOLLOW-UP LOOP',690,-334,20,u,{align:'right',v:.45});
  panel(-694,-240,400,176,u,1,26);TX('确认跟进',-665,-170,43,u);TX('由用户确认',-665,-112,29,u,{v:.75});
  C(-241,-151,26,u,.7,2);L([[-252,-156],[-241,-138],[-221,-171]],show(37.8),3);shaft([[-214,-151],[-147,-151]],show(38));
  // The latch remains open until the user's confirmation, then the task outlet connects.
  const latch=ease(p(T,37.8,38.2));L([[-190,-177],[-160,-177+26*latch]],1,3,.9);
  doc(-122,-240,817,176,show(38.2));TX('跟进任务',-92,-170,44,show(38.3));TX('待跟进',510,-170,33,show(38.3));detail(-92,-119,410,2,show(38.3));
  route([[288,-64],[288,-6],[-552,-6],[-552,48]],38.8,39.7);doc(-694,49,1389,110,show(39.6));TX('跟进记录：资金安排尚未明确',-660,123,40,show(39.7));
  route([[288,159],[288,196],[-284,196],[-284,225]],40.4,41.1);panel(-694,226,1389,95,show(41));TX('商机诊断',-660,289,35,show(41));TX('下一步：补问资金计划',-379,290,43,show(41.2));
  spec(-690,373,u);shaft([[704,274],[870,274],[870,-445],[-748,-445],[-748,-170]],show(41.6),.3);
  route([[704,274],[870,274],[870,-445],[160,-445]],41.6,43.5,1.5,.6);
});}
function chassis(){at(0,0,()=>{
  R(110,110,7980,4580,1,.23,1.5);R(139,139,7922,4522,1,.13,1);for(let x=400;x<8050;x+=400){L([[x,110],[x,140]],1,1,.25);mono(String(x/400),x+8,164,18,1,{v:.25});}
  for(let y=400;y<4670;y+=400){L([[110,y],[140,y]],1,1,.25);mono(String.fromCharCode(65+y/400),155,y+7,18,1,{v:.25});}
  for(let x=1150;x<7200;x+=260)for(let y=560;y<3890;y+=260){L([[x-10,y],[x+10,y]],1,1,.065);L([[x,y-10],[x,y+10]],1,1,.065);}
  truss(1020,3900,7310,3900,36,show(5));truss(1090,1530,1090,3900,20,show(5));truss(7420,1100,7420,3900,22,show(11));
  for(const x of[1090,2250,3900,5450,7420]){panel(x-70,3910,140,60,show(11),.3,22);bolt(x-43,3932,show(11));bolt(x+43,3932,show(11));}
  dim(1090,4040,6330,'FIRMBUDDY / EXPERT + KNOWLEDGE + ACTION',show(44));
  const u=show(44,.55),ports=[['商机查询',2000,2460],['业务答疑',4050,3650],['拜访准备',6100,3650],['商机诊断',6200,2170],['销售陪练',2750,3480],['经营计划',6200,1050]];
  ports.forEach(([s,x,y],i)=>{if(u<=0)return;panel(x-305,y-108,610,164,u);C(x-327,y-20,14,u,.7,2);TX(s,x,y+22,128,u,{align:'center'});mono('P'+(i+1),x+274,y-75,21,u,{align:'right',v:.5});});
  if(u>0){shaft([[2750,3350],[2750,2920],[3335,2920]],u,.4);gear(2750,3265,24,7,-toothAngle(T),u,.5,20);TX('专家 × 知识 × 行动',4210,700,128,u,{align:'center'});}
  // Ending is a genuine title block in this same sheet, with no lifecycle matrix.
  const brand=show(48,.5);if(brand>0){panel(3480,4025,1550,388,brand,1,10);R(3500,4045,1510,348,brand,.5,1);L([[3500,4290],[5010,4290]],brand,1,.5);TX('firmbuddy',3560,4212,139,brand,{font:'Arial',weight:700});TX('把业务问题，变成有依据的行动',3560,4270,42,brand);TX('券商客户经营 · AI专家平台',3560,4360,36,brand,{v:.8});mono('EXPERTS / KNOWLEDGE / ACTION',4958,4349,14,brand,{align:'right',v:.5});}
});}
function caption(){const shot=plan.shots.find(s=>T>=s.start&&T<s.end);if(!shot||!shot.voiceover)return;
  const alpha=Math.min(p(T,shot.start,shot.start+.18),p(shot.end-T,0,.16));ov.save();ov.setTransform(scale,0,0,scale,0,0);ov.globalAlpha=alpha;ov.font=`400 31px ${FONT}`;
  let rows=[''];for(const c of [...shot.voiceover]){const i=rows.length-1;if(ov.measureText(rows[i]+c).width>1360)rows.push(c);else rows[i]+=c;}
  if(rows.length===2){const chars=[...shot.voiceover],middle=Math.ceil(chars.length/2),candidates=chars.map((c,i)=>({c,i})).filter(({c,i})=>/[，。；？]/.test(c)&&i>middle-12&&i<middle+12);const split=candidates.length?candidates.sort((a,b)=>Math.abs(a.i-middle)-Math.abs(b.i-middle))[0].i+1:middle;rows=[chars.slice(0,split).join(''),chars.slice(split).join('')];}
  const width=Math.max(...rows.map(s=>ov.measureText(s).width))+160,height=rows.length===1?80:120,x=96,y=1080-64-height;
  ov.fillStyle='rgba(12,33,65,.94)';ov.fillRect(x,y,width,height);ov.strokeStyle='#c3d8ec';ov.lineWidth=1;ov.strokeRect(x,y,width,height);ov.beginPath();ov.moveTo(x+103,y+12);ov.lineTo(x+103,y+height-12);ov.stroke();ov.fillStyle='#e9f1f9';ov.font='17px Consolas';ov.fillText('NOTE',x+25,y+30);ov.font='23px Consolas';ov.fillText(String(plan.shots.indexOf(shot)+1).padStart(2,'0'),x+35,y+61);ov.font=`400 31px ${FONT}`;rows.forEach((s,i)=>ov.fillText(s,x+123,y+(rows.length===1?52:43)+i*43));bounds.push({id:'subtitle',box:[x,y,x+width,y+height]});ov.restore();
}
window.renderAt=(t,type='image/png',quality=.95)=>{T=Math.max(0,Math.min(52,t));bounds=[];const c=cameraAt(T);setCam({...c,z:c.z*scale});proj.k=.42*ease(p(T,10.5,12));clear();NIBS.length=0;chassis();intro();signals();experts();knowledge();visit();follow();caption();compose(inkC,fxC,ovC,{sheet:[8200,4800],cam,seed:19});return type?canvas.toDataURL(type,quality):null;};
window.stateAt=t=>{window.renderAt(t,null);return{time:t,camera:cameraAt(t),buffer:[W,H],duration:52,shot:plan.shots.find(s=>t>=s.start&&t<s.end)?.id,bounds,subjects:{signalSlider:signalSlider(t),evidenceFront:evidenceFront(t),gapCarriage:gapCarriage(t)}};};
window.__ready=true;window.renderAt(0,null);
const audio=new Audio('./audio/mix.wav'),seek=document.querySelector('#seek'),display=document.querySelector('#time'),button=document.querySelector('#play');let playing=false,started=0,base=0;
seek.oninput=()=>{base=+seek.value;audio.currentTime=base;started=performance.now();window.renderAt(base,null);display.textContent=base.toFixed(2)+' / 52';};
button.onclick=()=>{playing=!playing;button.textContent=playing?'暂停':'播放';if(playing){base=+seek.value;if(base>=52)base=0;started=performance.now();audio.currentTime=base;audio.play().catch(()=>{});}else{base=+seek.value;audio.pause();}};
function tick(){if(playing){const t=Math.min(52,base+(performance.now()-started)/1000);window.renderAt(t,null);seek.value=t;display.textContent=t.toFixed(2)+' / 52';if(t>=52){playing=false;audio.pause();button.textContent='播放';}}requestAnimationFrame(tick);}if(!Q.has('render'))tick();
