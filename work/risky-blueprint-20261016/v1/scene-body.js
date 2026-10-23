// Original Risky world. Paper-space engineering illustration, not physical simulation.
const domains=['投行业务','机构业务','财富业务','资管业务','国际业务','投资业务','期货与衍生品','行业研究','综合专家'];
const ellipse=(x,y,rx,ry,a0=0,a1=TAU,n=96)=>Array.from({length:n+1},(_,i)=>{const a=mix(a0,a1,i/n);return[x+rx*Math.cos(a),y+ry*Math.sin(a)]});
function bez(a,b,c,d,n=100){return Array.from({length:n+1},(_,i)=>{const u=i/n,v=1-u;return[v*v*v*a[0]+3*v*v*u*b[0]+3*v*u*u*c[0]+u*u*u*d[0],v*v*v*a[1]+3*v*v*u*b[1]+3*v*u*u*c[1]+u*u*u*d[1]]});}
const paths={
 evidence:bez([1000,1200],[1700,1200],[2100,1100],[3200,1100]),
 hall:bez([3200,1100],[4100,1100],[4400,1600],[5900,1600]),
 snapshot:bez([5900,1600],[7400,1600],[7450,2900],[6600,2900]),
 trial:bez([6600,2900],[6000,2900],[5700,2500],[5000,2500]),
 record:bez([3200,3500],[2450,3500],[1900,3250],[1100,3250]),
 return:bez([1100,3250],[650,3850],[1400,4180],[2800,4180]).concat(bez([2800,4180],[4700,4180],[7900,4400],[7900,3000]).slice(1)).concat(bez([7900,3000],[7900,1600],[7180,1600],[5900,1600]).slice(1)),
 monitor:bez([5900,1600],[4700,2050],[2000,2050],[1000,1200])
};
const keys=[
 [0,1000,1000,1.12,0],[4,1000,1000,1.12,0],[6,1110,1050,.98,0],[12.8,1110,1050,.98,0],
 [15,2170,1100,.89,.012,650,0,-.03,0],[17,3200,1000,.92,0],[23.6,3200,1000,.92,0],
 [25.8,4380,1300,.72,-.012,650,100,-.07,0],[28,5950,1170,.69,0],[32,5950,1170,.69,0],
 [34.2,5940,800,.88,0],[36.7,5940,800,.88,0],[38,6130,1510,.98,0],[39,6130,1510,.98,0],
 [40.5,7160,2210,.87,.015,50,700,0,0],[42,6600,2870,1.05,0],[45.6,6600,2870,1.05,0],
 [47.7,5500,2620,.72,-.01,-660,-80,-.16,0],[50,3550,3000,.60,0],[54,3550,3000,.60,0],
 [57,3550,3060,.62,0],[62,3550,3060,.62,0],[64,2600,3370,.72,0,-650,0,.06,0],
 [66,1100,3090,1,0],[67,1100,3090,1,0],[69,2570,4010,.55,0,1400,0,-.25,0],
 [70.5,5400,3900,.45,0,1400,-300,0,0],[72.8,6520,1740,.74,0],[74,6150,1530,.74,0],
 [77.5,4100,2350,.225,0],[80,4100,2350,.225,0]
];
function quint(a,b,va,vb,h,u){const d=b-a,A=va*h,B=vb*h;return a+A*u+(10*d-6*A-4*B)*u**3+(-15*d+8*A+7*B)*u**4+(6*d-3*A-3*B)*u**5;}
function cameraAt(t){let i=1;while(i<keys.length-1&&t>keys[i][0])i++;const a=keys[i-1],b=keys[i],h=b[0]-a[0],u=p(t,a[0],b[0]),c={};for(const[j,k]of['x','y','z','r'].entries()){c[k]=quint(j===2?Math.log(a[j+1]):a[j+1],j===2?Math.log(b[j+1]):b[j+1],a[j+5]||0,b[j+5]||0,h,u);if(j===2)c[k]=Math.exp(c[k]);}return c;}
const pathPoint=(q,u)=>u<=0?q[0]:u>=1?q.at(-1):trunc(q,u)[1];
function rail(q,v=.38){L(q.map(([x,y])=>[x,y-24]),1,2.2,v);L(q.map(([x,y])=>[x,y+24]),1,2.2,v);L(q,1,1,v*.5,'center');for(let i=0;i<q.length;i+=6){const[x,y]=q[i];R(x-10,y-32,20,64,1,v*.55,1);C(x,y,5,1,v,1);}}
function plaque(s,x,y,w,size=36){panel(x,y,w,72,1,.9,10);R(x+7,y+7,w-14,58,1,.4,1);bolt(x+14,y+36);bolt(x+w-14,y+36);TX(s,x+w/2,y+48,size,1,{align:'center'});}
function base(x,y,w,h){R(x,y,w,h,1,.5,2);truss(x,y+h+24,x+w,y+h+24,Math.round(w/100));for(const xx of[x+35,x+w-35]){panel(xx-17,y+h+50,34,90,1,.6,12);panel(xx-44,y+h+133,88,20,1,.7,10);bolt(xx-24,y+h+143);bolt(xx+24,y+h+143);}}
function goldLine(q,width=3,color='#cdb77b',alpha=.9){ov.save();ov.strokeStyle=color;ov.globalAlpha=alpha*visibility;ov.lineWidth=width*Math.pow(cam.z,.65);ov.beginPath();q.forEach(([x,y],i)=>{const pt=S(x+ox,y+oy);i?ov.lineTo(...pt):ov.moveTo(...pt)});ov.stroke();ov.restore();}
function goldDot(x,y,r,color='#d1b878'){const q=S(x+ox,y+oy);ov.save();ov.fillStyle=color;ov.globalAlpha=visibility;ov.beginPath();ov.arc(...q,r*cam.z,0,TAU);ov.fill();ov.restore();}
function caseBox(x,y,label='A-001',v=1){at(x,y,()=>{panel(-113,-49,226,98,1,.95,18);R(-105,-41,210,82,1,.65,1);for(const xx of[-96,96]){bolt(xx,-31);bolt(xx,31);}TX(label,0,12,35,1,{align:'center'});goldLine([[-83,30],[83,30]],4);for(let j=0;j<Math.min(4,Math.floor(T/14));j++)C(-54+j*35,-30,5,1,.9,2);},v);}
function carrier(q,a,b){const pt=pathPoint(q,ease(p(T,a,b)));caseBox(...pt);goldLine(trunc(q,ease(p(T,a,b)))[0],3);return pt;}
function dial(x,y,r,value,label){C(x,y,r,1,.9,2.7);C(x,y,r-12,1,.6,1.5);for(let i=0;i<=20;i++){const a=Math.PI*.78+i*Math.PI*1.44/20;L([[x+Math.cos(a)*(r-22),y+Math.sin(a)*(r-22)],[x+Math.cos(a)*(r-(i%5?30:40)),y+Math.sin(a)*(r-(i%5?30:40))]],1,1.5,.6);}const a=Math.PI*.78+value*Math.PI*1.44;goldLine([[x,y],[x+Math.cos(a)*(r-35),y+Math.sin(a)*(r-35)]],5);C(x,y,12,1,.9,2);TX(label,x,y+r*.48,26,1,{align:'center'});bearing(x,y+r+30);}
function signal(){at(1000,1000,()=>{
 base(-650,-300,1300,600);mono('01 / SIGNAL & EVIDENCE',-640,-345,24,1,{v:.6});
 for(let i=0;i<3;i++){const x=-550+i*260;C(x,-245,33,1,.7,2);C(x,25,33,1,.7,2);panel(x-62,-245,124,270,1,.7,8);['公告','财务','司法'].forEach((s,j)=>{if(i===j)TX(s,x,-164,38,1,{align:'center'});});detail(x-42,-120,84,6);shaft([[x,-270],[x,55]],1,.25);}
 dial(390,-95,157,.30+.47*ease(p(T,1.5,3)),'异常信号');
 const slide=mix(-540,0,ease(p(T,6.5,9)));shaft([[-580,140],[470,140]],1,.6);bearing(-580,140);bearing(470,140);
 gear(-540,140,20,5,T*.38,1,.65,16);panel(slide-45,108,90,64,1,.9,14);L([[slide,108],[slide,28]],1,5,.8);panel(slide-80,8,160,26,1,.7,8);
 if(T>=6){const u=ease(p(T,7,10));doc(-180,-220,310,260,1,.85);TX('企业 A',-145,-157,40);TX('重大诉讼信号',-145,-98,31);TX('原文索引 E-01',-145,-41,25);L([[-145,-20],[90,-20]],1,2,.65);C(mix(-400,30,u),-70,65,1,.9,3);C(mix(-400,30,u),-70,58,1,.3,1);}
 if(T>=9&&T<=13.1)caseBox(1000,1200);
 plaque('示例案件 · A-001',-620,345,430,33);TX('AI 检索 · 提取 · 来源比对',-140,392,35);
 if(T>2&&T<6)goldDot(390+120,-180,12,'#d2a45b');
 });if(T>=13.1&&T<=17)carrier(paths.evidence,13.1,17);}
function relations(){at(3200,1000,()=>{
 mono('02 / EVIDENCE BEFORE EDGE',-690,-360,23,1,{v:.6});base(-700,-290,1400,590);
 const u=ease(p(T,17.6,20.5));const nodes=[[-450,-140,'控股主体'],[0,-205,'企业 A'],[480,-100,'关联企业'],[-370,230,'司法材料'],[410,220,'业务关系']];
 for(let i=0;i<nodes.length;i++){const[x0,y0,s]=nodes[i],x=x0*u,y=y0*u;shaft([[0,40],[x,y]],1,.28);if(i!==1){L([[0,-205*u],[x,y]],1,2,.7,i===4?[12,8]:undefined);C(x*.5,(y-205*u)*.5,12,1,.5,1);}panel(x-112,y-46,224,92,1,.85,18);TX(s,x,y+10,33,1,{align:'center'});bolt(x-94,y-29);bolt(x+94,y+29);}
 TX('控制',-310,-235,28,show(20.5));TX('股权',220,-205,28,show(20.5));TX('来源 E-01 / E-02',-640,374,28);
 L([[-650,-430],[650,-430]],1,1,.35,[12,8]);TX('行业背景参考层',0,-450,30,1,{align:'center',v:.6});
 if(T>=17&&T<=23.6)caseBox(3200,1100);
 });if(T>23.6&&T<=28)carrier(paths.hall,23.6,28);}
function hall(){at(5950,1200,()=>{
 mono('03 / KNOWLEDGE · METHODS · EXPERTS',-1060,-670,24,1,{v:.6});
 // Knowledge archive behind the amphitheatre, with one extracted active loadout.
 for(let bank=0;bank<3;bank++){const x=-980+bank*690;panel(x,-590,620,228,1,.7,26);TX(['专业知识库','专业方法','知识装备'][bank],x+310,-540,39,1,{align:'center'});for(let j=0;j<6;j++){const pull=(bank===1&&j===2)?100*ease(p(T,33.3,34.3)):0;panel(x+20+j*96,-505+pull,84,112,1,.65,12);R(x+46+j*96,-470+pull,32,10,1,.5,1);} }
 domains.forEach((s,i)=>TX(s,-1010+(i%3)*730,-285+Math.floor(i/3)*60,34,1,{v:.85}));
 for(let row=0;row<3;row++){const rx=1000-row*150,ry=480-row*105,cy=390;const q=ellipse(0,cy,rx,ry,Math.PI,TAU);L(q,1,2.8,.8);L(q.map(([x,y])=>[x,y+40]),1,1.6,.5);for(let j=0;j<11;j++){const a=Math.PI+.10+j*(Math.PI-.2)/10,x=Math.cos(a)*(rx-25),y=cy+Math.sin(a)*(ry-20);panel(x-34,y-24,68,43,1,.65,12);L([[x-22,y+22],[x-22,y+45],[x+22,y+45],[x+22,y+22]],1,1.4,.4);if(row===1&&[3,5,7].includes(j)&&T>28.8){goldLine([[x-25,y+5],[x+25,y+5]],4);if(T<39)goldLine([[x,y+45],[0,390]],2,'#ccb778',show(29+(j-3)*.5));}}}
 for(const x of[-1040,1040]){panel(x-22,360,44,220,1,.65,15);panel(x-52,570,104,22,1,.7,12);}
 L(ellipse(0,405,520,105),1,3,.85);L(ellipse(0,425,520,105),1,1.6,.6);truss(-420,545,420,545,8);bearing(-340,520);bearing(340,520);
 ['尽调评估专家','合规风险专家','风险监控专家'].forEach((s,i)=>plaque(s,-650+i*460,230,410,31));
 if(T>=28&&T<=39)caseBox(5900,1600);
 if(T>=34&&T<37.8){const z=ease(p(T,34,36.5));doc(-100,-360+z*550,200,150,1,.9);TX('检索依据',0,-300+z*550,29,1,{align:'center'});detail(-75,-270+z*550,150,3);}
 if(T>36.7){const labels=T>=72?['补充核查','持续跟踪','监测事项']:['共同依据','保留分歧','推演条件'];labels.forEach((s,i)=>plaque(s,-650+i*460,605,410,34));}
 });if(T>=39&&T<=42)carrier(paths.snapshot,39,42);}
function snapshot(){at(6600,2900,()=>{
 mono('04 / FREEZE THE STARTING STATE',-630,-365,24,1,{v:.6});base(-640,-290,1280,560);rail([[-650,0],[650,0]],.55);
 const close=ease(p(T,42.5,44));for(const side of[-1,1]){const x=side*mix(340,145,close);shaft([[side*530,-160],[side*140,-160]],1,.6);bearing(side*460,-160);gear(side*520,-160,20,4,side*T*.5,1,.65,14);panel(x-24,-95,48,190,1,.9,18);panel(x-side*22-25,-55,50,110,1,.8,14);}
 for(let i=0;i<3;i++)dial(-420+i*420,-190,75,[.65,.5,.28][i]*ease(p(T,42,44)),['冲击','范围','恢复'][i]);
 if(T>=42&&T<=45.6)caseBox(6600,2900);
 plaque('证据 · 关系 · 假设 · 版本',-565,150,1130,38);TX('同源快照  S-001',0,365,40,1,{align:'center'});
 if(T>=44){goldLine([[-145,-65],[-145,65],[145,65],[145,-65]],4);}
 });if(T>45.6&&T<=48.6)carrier(paths.trial,45.6,48.6);}
const trialXs=[2450,3500,4550],trialColors=['#c8b478','#d58a6f','#9fc8bb'];
function trials(){
 // Shared inlet, equal-scale experimental beds, same timing axis.
 rail([[2450,2500],[5000,2500]],.55);for(const x of trialXs)rail([[x,2500],[x,2720]],.5);
 trialXs.forEach((cx,i)=>at(cx,3100,()=>{
 const col=trialColors[i];base(-440,-365,880,710);plaque(['基准情景','不利情景','缓释情景'][i],-400,-480,800,56);
 TX(['保留初始状态','加入不利冲击','施加缓释假设'][i],0,-300,33,1,{align:'center'});
 const run=p(T,51,61),reach=[.53,.94,.41][i];
 for(let layer=0;layer<2;layer++){
 const yy=-135+layer*220;TX(['业务','舆情'][layer],-375,yy-45,35);shaft([[-270,yy],[340,yy]],1,.3);
 const nodePts=[[-250,yy],[0,yy-70],[270,yy],[-30,yy+70]];
 const links=[[0,1],[1,2],[0,3],[3,2]];
 links.forEach(([a,b],j)=>{L([nodePts[a],nodePts[b]],1,2,.6);const amount=clamp((run*(i===1?1.8:1.1)-j*.17)*2);if(amount>0)goldLine(trunc([nodePts[a],nodePts[b]],amount)[0],4,col,.9);});
 nodePts.forEach(([x,y],j)=>{const activation=clamp((run-j*.12)*2);C(x,y,38,1,.7,2);C(x,y,30,1,.4,1);if(activation>0)goldDot(x,y,8+activation*(i===1?18:12)*(i===2?(1-run*.65):1),col);if(j===0)TX('A',x,y+8,25,1,{align:'center'});});
 }
 // Recording pen draws a model-state trajectory, not a probability graph.
 const plot=[];for(let j=0;j<=80;j++){const u=j/80;if(u>run)break;plot.push([-310+u*620,280-(.12+reach*Math.sin(u*Math.PI*.7)*(i===2?1-u*.7:1))*100]);}
 L([[-310,165],[-310,290],[330,290]],1,1.4,.55);if(plot.length>1){goldLine(plot,3,col);const[x,y]=plot.at(-1);C(x,y,8,1,.85,1.5);L([[x,160],[x,y]],1,2,.6);}
 TX('逐轮记录',-370,380,27);TX('模型状态示意',130,380,27);
 if(T>=48.6&&T<51){const y=mix(2500,2720,ease(p(T,48.6,50)));caseBox(cx,y,'A-001');}
 }));
 at(3500,3650,()=>{L([[-1450,0],[1450,0]],1,2,.65);for(let j=0;j<=8;j++){const x=-1400+j*350;L([[x,-12],[x,14]],1,2,.65);}const x=-1400+2800*p(T,51,61);goldDot(x,0,14);TX('同一起点 / 同一轮次轴 / 共同尺度',0,92,47,1,{align:'center'});});
 if(T>=62&&T<66)carrier(paths.record,62,66);
}
function recorder(){at(1100,3100,()=>{
 mono('06 / RECORD · REVIEW · FOLLOW',-570,-400,23,1,{v:.6});base(-580,-310,1160,570);
 for(const xx of[-420,420])bearing(xx,-30);shaft([[-420,-30],[420,-30]],1,.65);
 panel(-350,-225,700,390,1,.8,40);L(ellipse(-350,-30,65,195),1,2.5,.8);L(ellipse(350,-30,65,195),1,2.5,.8);
 for(let j=0;j<11;j++){const y=-195+j*32;L([[-300,y],[300,y]],1,1,.3);}
 const amount=ease(p(T,64,66));doc(-240,-130,480,150+170*amount,1,.9);TX('推演过程与依据',0,-65,40,1,{align:'center'});TX('快照 S-001 / 案件 A-001',0,0,28,1,{align:'center'});TX('路径 · 范围 · 恢复',0,64,33,show(65),{align:'center'});gear(-470,190,24,5,T*.4,1,.7,20);
 if(T>=66&&T<67)caseBox(1100,3250);plaque('记录携回 · 专家复核',-540,330,1080,43);
 });if(T>=67&&T<73)carrier(paths.return,67,73);if(T>=73){caseBox(5900,1600);goldLine(trunc(paths.monitor,ease(p(T,73.8,78)))[0],4,'#c4b273',.8);}}
function chassis(){R(130,130,7940,4460,1,.35,1.5);R(160,160,7880,4400,1,.15,1);for(let x=400;x<8000;x+=400){L([[x,130],[x,170]],1,1,.35);mono(String(x/400),x+10,205,23,1,{v:.4});}for(let x=350;x<8000;x+=280)for(let y=350;y<4400;y+=280){L([[x-8,y],[x+8,y]],1,.7,.09);L([[x,y-8],[x,y+8]],1,.7,.09);}Object.values(paths).forEach(q=>rail(q));
 if(T>=75||Q.has('concept')){const u=Q.has('concept')?1:show(75,1);at(0,0,()=>{TX('Risky 风险视角',400,450,190,u,{weight:700});TX('有据研判 · 情景推演 · 持续跟踪',400,680,83,u);TX('发现一个异常，看清它的来路，试验它的去向。',4100,4500,87,u,{align:'center'});});}}
function caption(){if(Q.has('concept'))return;const shot=plan.shots.find(s=>T>=s.start&&T<s.end)||plan.shots.at(-1);const alpha=Math.min(p(T,shot.start,shot.start+.5),p(shot.end-T,0,.45));ov.save();ov.setTransform(scale,0,0,scale,0,0);ov.globalAlpha=alpha;ov.fillStyle='rgba(6,22,35,.88)';ov.fillRect(120,916,1680,112);ov.fillStyle='#eee8d9';ov.textAlign='center';ov.font='500 39px "Microsoft YaHei"';ov.fillText(shot.caption,960,981);ov.font='19px "Microsoft YaHei"';ov.fillStyle='#bbbdaf';ov.textAlign='right';ov.fillText(T>=40&&T<74?'合成案件 · 情景推演机制示意':'合成案件 A-001 · 流程示例',1790,890);ov.restore();}
window.renderAt=(t,type='image/png',quality=.95)=>{T=Math.max(0,Math.min(80,t));bounds=[];const c=Q.has('concept')?{x:4100,y:2350,z:.225,r:0}:cameraAt(T);setCam({...c,z:c.z*scale});proj.k=.43;clear();NIBS.length=0;chassis();signal();relations();hall();snapshot();trials();recorder();caption();compose(inkC,fxC,ovC,{sheet:[8200,4800],cam,seed:27});return type?canvas.toDataURL(type,quality):null;};
window.stateAt=t=>{window.renderAt(t,null);return{time:t,camera:cameraAt(t),buffer:[W,H],bounds,caseId:'A-001',snapshotId:'S-001'};};window.cameraAt=cameraAt;window.cameraKeys=keys;window.__ready=true;window.renderAt(Q.has('concept')?60:0,null);
const audio=new Audio('./audio/mix.wav');let playing=false,started=0,baseTime=0;const seek=document.querySelector('#seek'),button=document.querySelector('#play');seek.oninput=()=>{baseTime=+seek.value;audio.currentTime=baseTime;started=performance.now();window.renderAt(baseTime,null);};button.onclick=()=>{playing=!playing;if(playing){baseTime=+seek.value;started=performance.now();audio.currentTime=baseTime;audio.play();}else audio.pause();};function tick(){if(playing){const t=Math.min(80,baseTime+(performance.now()-started)/1000);window.renderAt(t,null);seek.value=t;if(t>=80){playing=false;audio.pause();}}requestAnimationFrame(tick);}if(!Q.has('render'))tick();
