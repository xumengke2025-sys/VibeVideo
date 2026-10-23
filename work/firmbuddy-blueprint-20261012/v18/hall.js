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
