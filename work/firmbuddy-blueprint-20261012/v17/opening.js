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
