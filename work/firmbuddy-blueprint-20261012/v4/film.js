import {W,H,g,ov,inkC,fxC,ovC,setCam,clear,cam,line,text,rect,circ,ell,solid,hatch,knock,trunc,NIBS,S,proj} from './vendor/draw.js';
import {makePaper} from './vendor/paper.js';

const canvas = document.querySelector('#c');
canvas.width=W; canvas.height=H;
const compose=makePaper(canvas,W,H), scale=W/1920;
const plan=await (await fetch('./plan.json')).json();
const Q=new URLSearchParams(location.search);
if(Q.has('render'))document.body.classList.add('render');
await document.fonts.load('400 48px "Microsoft YaHei"');
await document.fonts.load('600 48px "Microsoft YaHei"');
const FONT='"Microsoft YaHei",sans-serif',MONO='Consolas,monospace';
const clamp=x=>Math.max(0,Math.min(1,x));
const p=(t,a,b)=>clamp((t-a)/(b-a));
const ease=x=>{x=clamp(x);return x*x*x*(x*(x*6-15)+10)};
const mix=(a,b,u)=>a+(b-a)*u;
const show=(a,b=.45)=>p(T,a,a+b);
let T=0, ox=0, oy=0, visibility=1, bounds=[];
proj.k=.58;
const at=(x,y,fn,v=1)=>{const prev=[ox,oy,visibility];ox=x;oy=y;visibility*=v;fn();[ox,oy,visibility]=prev;};
const pts=q=>q.map(([x,y])=>[x+ox,y+oy]);
function L(q,u=1,w=2,v=1,dash){if(visibility<.01)return;line(pts(q),{u,w,v:v*visibility,dash,nib:false});}
function R(x,y,w,h,u=1,v=1,lw=2){L([[x,y],[x+w,y],[x+w,y+h],[x,y+h],[x,y]],u,lw,v);}
function C(x,y,r,u=1,v=1,w=2){L(circ(x,y,r,48),u,w,v);}
function panel(x,y,w,h,u=1,v=1,th=0){if(u<=0)return;solid(pts(rect(x,y,x+w,y+h)),{u,v:v*visibility,w:2.2,th});}
function TX(str,x,y,size=44,u=1,o={}){
  if(u<=0||visibility<.01)return;
  const v=(o.v??1)*visibility;
  text(str,ox+x,oy+y,{size,u,font:FONT,nib:false,...o,v});
  if(u>=.999&&v>=.64&&size*cam.z/scale>=30){
    g.font=`${o.weight||400} ${size}px ${o.font||FONT}`;
    const width=g.measureText(str).width;
    const align=o.align||'left',dx=align==='center'?-width/2:align==='right'?-width:0;
    const a=S(ox+x+dx,oy+y-size*.95),b=S(ox+x+dx+width,oy+y+size*.22);
    bounds.push({id:o.id||str,text:str,box:[a[0]/scale,a[1]/scale,b[0]/scale,b[1]/scale],size:size*cam.z/scale});
  }
}
function mono(s,x,y,size=21,u=1,o={}){TX(s,x,y,size,u,{font:MONO,...o});}
function detail(x,y,w,n=4,u=1){for(let i=0;i<n;i++)L([[x,y+i*17],[x+w*(i===n-1?.63:1),y+i*17]],clamp(u*n-i),1,.3);}
function port(x,y,u=1,r=7){C(x,y,r,u,.9,1.7);C(x,y,r+6,u,.25,1);}
function route(q,a,b,w=2.6,v=.8){const u=p(T,a,b);L(q,u,w,v);if(u>0&&u<1){const tip=trunc(q,u)[1];if(tip)C(tip[0],tip[1],5,1,.85,1.4);}}
function ruledTag(s,x,y,w,u=1,size=38){panel(x,y,w,66,u);TX(s,x+18,y+46,size,u);L([[x+w-17,y+15],[x+w-17,y+51]],u,1,.45);}
function head(n,title,english,a){const u=show(a);mono(n,-720,-357,24,u,{v:.55});TX(title,-638,-345,53,u);L([[-720,-310],[720,-310]],u,1.4,.5);mono(english,720,-344,18,u,{v:.45,align:'right'});}
function specimen(x=-720,y=303,u=1){mono('DEMO',x,y,18,u,{v:.55});TX('流程示例',x+74,y,27,u,{v:.65});}
function cross(x,y,v=.16){L([[x-12,y],[x+12,y]],1,1,v);L([[x,y-12],[x,y+12]],1,1,v);}
function doc(x,y,w,h,u=1,v=1){const q=[[x,y],[x+w-36,y],[x+w,y+36],[x+w,y+h],[x,y+h]];solid(pts(q),{u,v:v*visibility,w:2.4});L([[x+w-36,y],[x+w-36,y+36],[x+w,y+36]],u,1.6,v*.65);}
function dimension(x,y,w,s,u=1){L([[x,y-10],[x,y+14]],u,1,.5);L([[x+w,y-10],[x+w,y+14]],u,1,.5);L([[x,y],[x+w,y]],u,1,.45);TX(s,x+w/2,y-15,23,u,{align:'center',v:.45});}
function folder(x,y,w,h,title,u=1,v=1){
  for(let k=3;k>0;k--)R(x+k*7,y-k*7,w,h,u,v*.23,1.1);
  const q=[[x,y+25],[x+32,y],[x+132,y],[x+155,y+25],[x+w,y+25],[x+w,y+h],[x,y+h]];
  solid(pts(q),{u,w:2.2,v:v*visibility});
  L([[x,y+62],[x+w,y+62]],u,1,v*.55);
  C(x+w*.5,y+83,7,u,v);C(x+w*.5,y+132,7,u,v);
  L([[x+w*.5,y+76],[x+w*.5+7,y+131],[x+w*.5-7,y+140],[x+w*.5-5,y+85]],u,1.3,v*.8);
  TX(title,x+22,y+h-29,31,u,{v});mono('V / REF.',x+w-22,y+54,15,u,{align:'right',v:v*.6});
}

const centers={intro:[4400,1100],signals:[6500,1100],experts:[6500,2250],answer:[4400,2250],visit:[4600,3450],follow:[6500,3450]};
const keys=[
  [0,4400,1100,1.04],[5.25,4400,1100,1.04],[6.8,6500,1100,1.04],[14.35,6500,1100,1.04],
  [16,6500,2250,1.04],[23.999,6500,2250,1.04],[24,4400,2250,1.04],[35.999,4400,2250,1.04],
  [36,4600,3450,1.04],[45.5,4600,3450,1.04],[47,6500,3450,1.04],[54.9,6500,3450,1.04],
  [55.6,5580,2310,.29],[60.9,5580,2310,.29],[64.5,3800,2200,.215],[68,3800,2200,.215],
];
function cameraAt(t){let a=keys[0],b=keys[1];for(let i=1;i<keys.length;i++){b=keys[i];if(t<=b[0])break;a=b;}const u=ease(p(t,a[0],b[0]));return{x:mix(a[1],b[1],u),y:mix(a[2],b[2],u),z:Math.exp(mix(Math.log(a[3]),Math.log(b[3]),u)),r:0};}

function intro(){at(...centers.intro,()=>{
  mono('FIRMBUDDY / CLIENT OPERATIONS',-710,-345,23,1,{v:.55,ls:2});
  TX('firmbuddy',-710,-183,112,1,{font:'Arial',weight:700});
  TX('券商客户经营 · AI专家平台',-710,-101,45,1);
  L([[-710,-63],[680,-63]],show(.5),1.5,.55);
  ['查商机','问业务','备拜访'].forEach((s,i)=>{const x=-710+i*455,u=show(1.4+i*.32);R(x,0,410,96,u,i===0?.9:.6);TX(s,x+205,64,46,u,{align:'center'});port(x+410,48,u);});
  const u=show(3);panel(-710,149,1390,120,u);mono('>',-679,220,41,u);TX('谁值得先跟进？',-626,223,51,show(3.2));
  L([[574,185],[618,209],[574,233]],show(4.5),2.6,.9);mono('INPUT',680,307,18,show(3),{align:'right',v:.4});
  route([[680,209],[845,209],[845,0],[1340,0]],5,6.8);
});}

function signals(){at(...centers.signals,()=>{
  head('01','查商机：从变化中发现线索','QUERY / WATCHLIST',6.2);
  const a=show(6.8);
  TX('市场事件',-705,-220,40,a);TX('客户名单',-705,58,40,a);
  // Sources retain separate rails; a scan selects a candidate rather than converting it into a deal.
  for(let i=0;i<5;i++){
    const x=-694+i*118;doc(x,-180,98,132,a,.45);mono('0'+(i+1),x+13,-151,17,a,{v:.4});detail(x+13,-124,72,3,a);
    R(x,95,98,104,a,.35,1.2);L([[x+18,121],[x+70,121]],a,1.5,.55);detail(x+18,144,68,2,a);
  }
  dimension(-695,241,575,'QUERY  /  MONITOR',a);
  const scan=ease(p(T,7.2,9));if(scan>0&&scan<1){const x=-708+scan*602;L([[x,-196],[x,216]],1,2.4,.9);L([[x-9,-196],[x+9,-196]],1,2,.7);}
  route([[-118,-104],[15,-104],[15,-40],[90,-40]],8.6,9.6);
  port(90,-40,show(9));
  doc(104,-229,608,483,show(9),1);
  mono('CANDIDATE  /  SOURCE',137,-176,21,show(9.3),{v:.6});
  TX('扩产相关披露',137,-93,51,show(10));L([[137,-58],[669,-58]],show(10),1.3,.45);
  TX('待核实',137,21,44,show(11));L([[340,-10],[602,-10]],show(11),1.4,.4,'hidden');
  TX('保留来源 · 再做研判',137,88,31,show(11.5),{v:.7});
  ruledTag('查看来源 →',137,143,350,show(12),33);mono('01',664,224,28,show(12),{align:'right',v:.5});
  specimen(-710,303,show(9));
  route([[706,12],[860,12],[860,740],[780,740]],14,16);
});}

function experts(){at(...centers.experts,()=>{
  head('02','AI专家：按专业分工','PROFESSIONAL COLLABORATION',15);
  const a=show(15.2,.65);
  for(let row=0;row<4;row++){
    const rx=674-row*48,ry=160-row*15,yy=-8+row*45;
    L(ell(0,yy,rx,ry,0,72,Math.PI,Math.PI*2),a,1.8,.65);
    L(ell(0,yy+20,rx,ry,0,72,Math.PI,Math.PI*2),a,1,.3);
    for(let j=0;j<14;j++){const angle=Math.PI+.1+(Math.PI-.2)*j/13,x=Math.cos(angle)*rx,y=yy+Math.sin(angle)*ry;R(x-16,y-19,32,19,a,.5,1.2);L([[x-20,y+6],[x+20,y+6]],a,1,.25);}
  }
  TX('数十位 · 多领域AI专家',0,-219,41,a,{align:'center'});
  const names=['行业研究','财务诊断','资本运作'];
  const duties=['看扩产逻辑','查资金安排','研判服务方向'];
  for(let i=0;i<3;i++){
    const x=-700+i*480,u=show(17+i*.9,.5);
    panel(x,40,435,175,u);mono('0'+(i+1),x+23,73,18,u,{v:.5});
    TX(names[i],x+22,119,43,u);TX(duties[i],x+22,176,33,u,{v:.8});
    route([[x+217,-40],[x+217,40]],17+i*.9,17.6+i*.9);
    port(x+217,-40,u);
  }
  const u=show(21);panel(-406,245,812,70,u);TX('候选线索＋待核实问题',0,294,42,u,{align:'center'});
  route([[-483,215],[-483,231],[-173,231],[-173,245]],20.5,21.2);
  route([[477,215],[477,231],[175,231],[175,245]],20.5,21.2);
  specimen(-715,308,a);
});}

function answer(){at(...centers.answer,()=>{
  head('03','问业务：让判断有依据','KNOWLEDGE / EVIDENCE',24);
  const input=show(24,.35);panel(-720,-262,1440,84,input);mono('>',-696,-211,30,input);TX('有扩产计划，就有融资需求吗？',-640,-203,44,show(24.2));
  const unfold=ease(p(T,27,28.6));
  // The expertise loadout is already connected. Only retrieval moves during this request.
  for(let i=0;i<3;i++)folder(-707+i*164,-115,149,197,['业务规范','研究资料','项目资料'][i],show(27),.38);
  TX('知识库',-707,144,37,show(27));
  L([[-707,166],[-198,166]],show(27),1,.45);
  TX('专家已装配',-707,210,31,show(27),{v:.7});mono('SOURCE / VERSION',-707,255,18,show(27),{v:.4});
  // A cutaway separates the cover, the selected page, and the source index.
  const x=-179-105*unfold,y=-107-20*unfold;
  if(unfold>0){
    doc(x+12,y+12,291,220,show(27),.3);
    doc(x,y,291,220,show(27),1);
    TX('示例资料',x+23,y+53,34,show(28));
    TX('扩产计划',x+23,y+111,34,show(29));
    TX('资金安排未提供',x+23,y+167,30,show(30));
    mono('REF / DEMO',x+23,y+205,17,show(28.5),{v:.6});
    L([[x,y-12],[x+291,y-12]],show(28),1,.5,'center');
  }
  const u=show(27);panel(164,-92,539,124,u);TX('财务诊断 · AI专家',190,-23,39,u);
  port(145,-28,u);
  L([[-198,184],[109,184],[109,-28],[145,-28]],u,1.4,.45,'hidden');
  mono('LOADOUT / CONFIGURED',186,14,17,u,{v:.5});
  const sourceU=p(T,30.5,32.2);L([[x+291,y+124],[121,y+124],[121,104],[202,104]],sourceU,2.8,.95);
  const tip=trunc([[x+291,y+124],[121,y+124],[121,104],[202,104]],sourceU)[1];
  if(tip&&sourceU<1)C(...tip,5,1,.9,1.4);
  const q=show(28.4);L([[190,104],[643,104],[643,180],[190,180]],q,1.6,.65,'hidden');
  if(T<33){TX('融资服务？',220,155,46,q);TX('初步方向 · 待确认',202,223,29,q,{v:.65});}
  const revise=ease(p(T,32.8,33.6));
  if(revise>0){panel(173,80,540,197,revise);TX('先确认',201,141,40,revise);TX('资金来源与缺口',201,207,45,revise);TX('依据：资料尚未给出资金安排',201,251,26,revise,{v:.7});port(173,179,revise);}
  specimen(-715,307,input);
});}

function visit(){at(...centers.visit,()=>{
  head('04','备拜访：把缺项变成提问','VISIT STRATEGY / QUESTIONS',36);
  panel(-720,-260,1440,83,show(36,.35));mono('>',-694,-209,30,show(36));TX('帮我准备这次拜访',-640,-204,45,show(36.2));
  const fold=ease(p(T,38.5,39.3));
  for(let k=2;k>0;k--)R(-720+k*10,-91-k*7,746,368,show(38.5),.24,1.2);
  doc(-720,-91,746,368,show(38.5));
  mono('VISIT STRATEGY',-685,-46,21,show(38.5),{v:.5});
  const move=ease(p(T,39,40.2));
  const x=mix(131,-676,move),y=mix(69,24,move);
  // The same information gap physically crosses into a question row; text switches only at contact.
  if(T<40.2){panel(x-7,y-43,418,75,show(39));TX('资金安排待核实',x+12,y+10,34,show(39));}
  else{
    TX('资金怎么安排？',-674,45,48,1);L([[-674,72],[-50,72]],1,1.3,.55);
    TX('何时落地？',-674,129,46,show(41));L([[-674,154],[-50,154]],show(41),1.2,.35);
    TX('谁参与决策？',-674,212,46,show(41.5));
  }
  if(fold>0){
    const opening=220*fold;L([[26,-91],[26+opening,-109],[26+opening,245],[26,277]],show(38.5),1.3,.4);hatch(pts([[26,-91],[26+opening,-109],[26+opening,245],[26,277]]),{u:1,v:.12,sp:22});
  }
  const a=show(38.5);TX('拜访策略包',333,-49,46,a);
  ['目标','提问','话术材料'].forEach((s,i)=>{const u=show(40.5+i*.4);R(331,18+i*82,349,63,u,.7,1.7);TX(s,356,62+i*82,36,u);mono('0'+(i+1),649,60+i*82,21,u,{align:'right',v:.45});});
  specimen(-715,308,show(36));
  route([[680,133],[852,133],[852,-150],[1200,-150]],45.3,47);
});}

function follow(){at(...centers.follow,()=>{
  head('05','持续经营：反馈推动下一步','FOLLOW UP / DIAGNOSIS',46);
  const u=show(46);panel(-720,-248,476,177,u);TX('确认跟进',-681,-178,45,u);
  TX('由用户确认',-681,-121,31,u,{v:.65});
  const check=show(47.2,.32);L([[-324,-160],[-304,-139],[-271,-185]],check,3.3);
  route([[-244,-162],[-121,-162]],47.5,48.1);
  doc(-102,-248,813,177,show(48));TX('跟进任务',-67,-174,45,show(48.1));TX('待跟进',513,-175,36,show(48.2));
  detail(-67,-126,440,2,show(48));
  mono('AFTER FOLLOW-UP',-710,-21,19,show(49),{v:.5});TX('跟进后',-710,25,36,show(49));
  doc(-478,-28,1189,128,show(49));TX('记录：资金安排尚未明确',-443,46,42,show(49.2));
  route([[96,100],[96,148],[-224,148],[-224,191]],50.6,51.9);
  const b=show(51.6);panel(-478,189,1189,105,b);TX('商机诊断',-444,257,36,b);L([[-229,210],[-229,272]],b,1,.55);TX('下一步：补问资金计划',-196,257,43,show(52));
  specimen(-715,312,show(46));
});}

function sheet(){at(0,0,()=>{
  R(90,90,7420,4220,1,.22,1.3);R(118,118,7364,4164,1,.15,1);
  for(let x=400;x<7500;x+=400){L([[x,90],[x,125]],1,1,.28);mono(String(x/400),x+7,149,18,1,{v:.25});}
  for(let y=400;y<4300;y+=400)L([[90,y],[125,y]],1,1,.25);
  for(let x=3800;x<7400;x+=250)for(let y=600;y<3950;y+=250)cross(x,y,.09);
  // Connectors exist in the same coordinates as the scenes; no replacement map is used at the end.
  route([[5090,1309],[5260,1309],[5260,1100],[5780,1100]],5,6.8);
  route([[7211,1112],[7360,1112],[7360,2020],[7220,2020]],14,16);
  const u=show(61,.8);
  if(u>0){
    const stages=[{x:320,w:1660,title:'上市前'},{x:2140,w:1660,title:'上市中'},{x:3970,w:3320,title:'上市后'}];
    stages.forEach((s,i)=>{R(s.x,670,s.w,3380,u,.45,2.2);TX(s.title,s.x+s.w/2,540,232,u,{align:'center'});mono('0'+(i+1),s.x+35,617,70,u,{v:.45});if(i<2){
      const names=i===0?['财务顾问','行业研究','资本规划']:['IPO / 保荐承销','战略配售','专业护航'];
      names.forEach((name,j)=>{TX(name,s.x+110,1120+j*850,105,u,{v:.4});L([[s.x+110,1190+j*850],[s.x+s.w-110,1190+j*850]],u,2,.25);});
    }});
    ['投行','机构','财富','资管','国际','投资'].forEach((s,i)=>{TX(s,400+i*350,3810,103,u,{v:.5});});
    TX('期货服务 · 贯穿全生命周期',430,4010,75,u,{v:.4});
  }
  const brand=show(64,.5);
  if(brand>0){panel(320,3940,6970,370,brand);TX('firmbuddy',520,4200,344,brand,{font:'Arial',weight:700});TX('把业务问题，变成有依据的行动',7060,4174,220,brand,{align:'right'});}
});}

function indexLayer(){at(0,0,()=>{
  const indexes=[['商机查询',6500,820],['业务答疑',4400,1810],['拜访准备',4600,3010],['商机诊断',6500,3010],['销售陪练',4480,3530],['经营计划',6430,3530]];
  indexes.forEach(([s,x,y],i)=>{
    const active=T<61&&(T<58?i<3:i>=3),a=show(i<3?55:58,.45);
    if(a<=0)return;
    const width=s.length*153+150;panel(x-width/2,y-135,width,185,a,active?1:.23);
    TX(s,x,y+1,144,a,{align:'center',v:active?1:.23});
  });
});}

function caption(){
  if(T>=64.5)return;
  const shot=plan.shots.find(s=>T>=s.start&&T<s.end);if(!shot)return;
  const alpha=Math.min(p(T,shot.start,shot.start+.2),p(shot.end-T,0,.18));
  ov.save();ov.setTransform(scale,0,0,scale,0,0);ov.globalAlpha=alpha;
  ov.font=`400 31px ${FONT}`;
  const max=1360,chars=[...shot.voiceover];let rows=[''];
  for(const c of chars){const idx=rows.length-1;if(ov.measureText(rows[idx]+c).width>max)rows.push(c);else rows[idx]+=c;}
  if(rows.length===2){
    const midpoint=Math.ceil(chars.length/2);
    const candidates=chars.map((c,i)=>({c,i})).filter(({c,i})=>/[，。；：]/.test(c)&&i>midpoint-10&&i<midpoint+10);
    const split=candidates.length?candidates.sort((a,b)=>Math.abs(a.i-midpoint)-Math.abs(b.i-midpoint))[0].i+1:midpoint;
    rows=[chars.slice(0,split).join(''),chars.slice(split).join('')];
  }
  const width=Math.max(...rows.map(s=>ov.measureText(s).width))+160,height=rows.length===1?80:120,x=96,y=1080-64-height;
  ov.fillStyle='rgba(12,33,65,.93)';ov.fillRect(x,y,width,height);ov.strokeStyle='#c3d8ec';ov.lineWidth=1;ov.strokeRect(x,y,width,height);
  ov.beginPath();ov.moveTo(x+103,y+12);ov.lineTo(x+103,y+height-12);ov.stroke();ov.fillStyle='#e9f1f9';ov.font='17px Consolas';ov.fillText('NOTE',x+26,y+30);ov.font='23px Consolas';ov.fillText(String(plan.shots.indexOf(shot)+1).padStart(2,'0'),x+35,y+61);ov.font=`400 31px ${FONT}`;
  rows.forEach((row,i)=>ov.fillText(row,x+123,y+(rows.length===1?52:43)+i*43));
  bounds.push({id:'subtitle',text:rows.join(''),box:[x,y,x+width,y+height],size:31});ov.restore();
}

window.renderAt=(t,type='image/png',quality=.95)=>{
  T=Math.max(0,Math.min(68,t));bounds=[];const c=cameraAt(T);setCam({...c,z:c.z*scale});clear();NIBS.length=0;
  sheet();intro();signals();experts();answer();visit();follow();indexLayer();caption();
  compose(inkC,fxC,ovC,{sheet:[7600,4400],cam,seed:19});
  return type?canvas.toDataURL(type,quality):null;
};
window.stateAt=t=>{window.renderAt(t,null);return{time:t,camera:cameraAt(t),buffer:[W,H],duration:68,shot:plan.shots.find(s=>t>=s.start&&t<s.end)?.id,bounds};};
window.__ready=true;window.renderAt(0,null);
const audio=new Audio('./audio/mix.wav'),seek=document.querySelector('#seek'),display=document.querySelector('#time'),button=document.querySelector('#play');
let playing=false,started=0,base=0;
seek.oninput=()=>{base=+seek.value;audio.currentTime=base;started=performance.now();window.renderAt(base,null);display.textContent=base.toFixed(2)+' / 68';};
button.onclick=()=>{playing=!playing;button.textContent=playing?'暂停':'播放';if(playing){base=+seek.value;if(base>=68)base=0;started=performance.now();audio.currentTime=base;audio.play().catch(()=>{});}else{base=+seek.value;audio.pause();}};
function tick(){if(playing){const t=Math.min(68,base+(performance.now()-started)/1000);window.renderAt(t,null);seek.value=t;display.textContent=t.toFixed(2)+' / 68';if(t>=68){playing=false;audio.pause();button.textContent='播放';}}requestAnimationFrame(tick);}
if(!Q.has('render'))tick();
