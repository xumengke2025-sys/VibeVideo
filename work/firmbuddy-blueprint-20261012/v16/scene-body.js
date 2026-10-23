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
 if(T<5.8){const priorVisibility=visibility;visibility*=ease(p(openingClock(filmTime),10.7,11));const u=ease(p(T,1.2,5.8));carrier([[-110,-73],[510,-73],...paths.query.slice(1).map(([x,y])=>[x-1050,y-1070])],u,'示例客户信息',270);visibility=priorVisibility;}
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
function experts(){at(...centers.experts,()=>{
 TX('专业会商：这家客户应该怎样跟进？',0,-622,55,1,{align:'center'});
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
 const chosen=[[-720,97,'股份管理需求'],[0,-121,'联系时机'],[720,97,'服务切入点']];
 chosen.forEach(([x,y,s],i)=>{const u=show(12.1+i*.4,.4);panel(x-52,y-34,104,63,u,1,10);plaque(s,x-175,y-149,350,43,u);route([[x,y+30],[x*.65,260],[0,365]],12.7+i*.4,14+i*.4,2.8,.92);});
 doc(-266,307,532,142,1);TX('A01 · 股东服务研判',0,364,44,show(13),{align:'center'});TX('结合客户背景，形成服务思路',0,415,35,show(13.1),{align:'center',v:.6});
 // Knowledge equipment supplies the specialist seats. Each clutch engages on an existing music beat.
 const foundations=['专业知识装备','业务方法沉淀','培养与试炼'];
 foundations.forEach((label,i)=>{const x=-1045+i*710,u=show(12.1+i*.4,.4);
   plaque(label,x,480,670,44,u);
   const seat=chosen[i],port=[x+335,480],side=i===0?-1170:i===2?1170:380;
   route([port,[port[0],455],[side,455],[side,seat[1]+55],[seat[0],seat[1]+55],[seat[0],seat[1]+31]],12.1+i*.4,12.5+i*.4,2.8,.72);
 });
 });/* V16: archive travels through connected industry table. */}
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
