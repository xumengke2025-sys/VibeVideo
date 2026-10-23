// V18: one customer dossier is the narrative object from task to usable output.
let realTime=0;
const resultCenter=[4900,5550];
function phase(a,b,fn,fade=.6){inkLayer(ease(p(realTime,a,a+fade))*(1-ease(p(realTime,b-fade,b))),fn);}
function clutch(x,y,engaged,clock,s=1){
  // Pitch radii 72+78=150. The driven gear joins before the pair turns.
  const shift=90*(1-engaged),a=Math.max(0,clock)*.6;
  gear(x-75*s,y,24,6*s,a,1,.8,15*s);
  gear(x+(75+shift)*s,y,26,6*s,meshAngle(a,24,26,[x-75*s,y],[x+(75+shift)*s,y]),1,.8,15*s);
  shaft([[x-320*s,y],[x-150*s,y]],1,.48);shaft([[x+(165+shift)*s,y],[x+380*s,y]],1,.48);
  bearing(x-235*s,y);bearing(x+315*s,y);
  if(engaged<1)L([[x+20*s,y-115*s],[x+20*s,y+115*s]],1,1.4,.5,'hidden');
}
function taskArchive(cx,cy,s=1,complete=false){
  const x=cx-270*s,y=cy-180*s,w=540*s,h=360*s;
  for(let i=2;i>0;i--)doc(x+i*14*s,y-i*11*s,w,h,1,.28);
  doc(x,y,w,h,1,.95);mono('A01 / CLIENT DOSSIER',x+30*s,y+44*s,22*s,1,{v:.65});
  TX('示例客户信息',cx,y+119*s,49*s,1,{align:'center'});
  TX('半导体衬底企业',cx,y+178*s,35*s,1,{align:'center',v:.86});
  L([[x+30*s,y+209*s],[x+w-30*s,y+209*s]],1,1.3,.4);
  TX(complete?'依据 · 判断 · 行动':'任务：找到服务切入点',cx,y+266*s,35*s,1,{align:'center'});
  TX('围绕同一家客户展开',cx,y+319*s,28*s,1,{align:'center',v:.6});
}
function taskOpening(){
  const t=realTime;
  TX('客户经理，怎样找到这家企业的服务切入点？',0,-345,46,1,{align:'center'});
  // Seated manager at the drafting desk; visible hands, papers and a task track.
  expertFigure(-565,9,2.7,.45);
  panel(-770,97,435,38,1,.7,18);L([[-748,135],[-748,268],[-366,268],[-366,135]],1,2,.5);
  doc(-708,69,170,38,1,.7);L([[-500,76],[-375,76],[-375,102]],1,2,.7);
  TX('客户经理',-565,337,42,1,{align:'center'});
  taskArchive(350,25);
  const q=[[-330,132],[-180,132],[-115,90],[62,90]];L(q,1,2,.45);openingPulse(q,.7,2.2);
  TX('有线索，还要有依据、有判断、有准备',0,-254,32,ease(p(t,.4,1.1)),{align:'center',v:.8});
  ['客户资料','业务线索','专业意见'].forEach((s,i)=>{const u=ease(p(t,.8+i*.5,2.4+i*.5)),xx=mix(-320+i*70,-255+i*93,u);doc(xx,-146-i*12,64,61,1,.45);detail(xx+10,-126-i*12,40,2);});
}
function pairedPain(first){
  const data=first?[
    [0,'收集耗时：每天重复搜、筛、抄','公告与名单分散，同一事件反复出现','整理占去时间，研判还没有开始'],
    [1,'切入不明：有信号，怎么跟？','解禁与股东动态，需要结合业务背景','联系谁、何时谈、先谈什么？']
  ]:[
    [2,'背景不全：客户资料拼不齐','企业、股东、行业信息难串成一条线','缺少完整背景，沟通难以深入'],
    [3,'专业难找：一个问题跨多领域','行业、合规、客户经营需要共同研判','专业意见分散，服务思路难成形']
  ];
  TX('同一次客户准备，卡在这些地方',0,-345,49,1,{align:'center'});
  mono('A01 / SAME CLIENT · SAME TASK',0,-280,21,1,{align:'center',v:.55});
  data.forEach(([id,a,b,c],i)=>painBay(-842+i*882,-180,id,a,b,c));
  // A01 remains on the common carriage while the missing pieces are exposed.
  shaft([[-838,218],[838,218]],1,.5);doc(-288,157,576,116,1,.9);
  TX('A01 · 示例客户信息',0,211,40,1,{align:'center'});TX('半导体衬底企业',0,252,28,1,{align:'center',v:.72});
  TX(first?'代价：搜集挤占研判时间，线索难排出轻重缓急':'代价：准备反复返工，客户跟进缺少明确方向',0,366,36,1,{align:'center'});
}
function stalledTask(){
  TX('一条线索，卡在行动之前',0,-344,59,1,{align:'center'});
  TX('客户经理需要的，是从信息到服务动作的完整路径',0,-265,36,1,{align:'center',v:.8});
  const stages=[[-660,'线索'],[0,'研判'],[660,'行动']];
  stages.forEach(([x,s],i)=>{doc(x-185,-168,370,119,1,.8);TX(s,x,-91,48,1,{align:'center'});if(i<2)L([[x+195,-108],[x+463,-108]],1,2,.45,'hidden');});
  clutch(0,104,0,0,1.15);
  TX('把资料归集、专业研判与客户跟进接起来',0,298,43,1,{align:'center'});
  TX('FirmBuddy · 让 AI 辅助这条业务流程',0,376,35,1,{align:'center',v:.85});
}
function narrativeOpening(){
  if(realTime>=44)return;
  at(...centers.intro,()=>{
    inkLayer(1-ease(p(filmTime,35,36.8)),()=>bench());
    phase(-.6,6.4,taskOpening,.6);
    phase(5.8,13,()=>pairedPain(true),.6);
    phase(12.4,19.8,()=>pairedPain(false),.6);
    phase(19.2,24.4,stalledTask,.6);
    inkLayer(ease(p(filmTime,17.4,18.4))*(1-ease(p(filmTime,26.7,28))),sourceDraft);
  });
  if(filmTime>=27.4)cardsDraft();
}
function foldSheet(x,y,w,h,unfold,alpha=1){
  const ww=mix(w*.92,w,unfold);
  doc(x-ww/2,y,ww,h,1,alpha);
  if(unfold<.98){L([[x-ww/2+32,y+24],[x-ww/2+32,y+h-24]],1,1.2,.4);L([[x+ww/2-32,y+24],[x+ww/2-32,y+h-24]],1,1.2,.4);}
}
const outcomePages=[
  {title:'为什么关注',lines:['公司解禁窗口','结合股东与企业资料','形成股东服务研判'],before:'分散线索',after:'关注依据'},
  {title:'与谁沟通',lines:['了解股份事务接口','结合产业研究背景','准备有针对性的问题'],before:'零散疑问',after:'沟通重点'},
  {title:'下一步做什么',lines:['人工审阅沟通提纲','安排联系与后续跟进','记录回流客户档案'],before:'临时准备',after:'行动安排'}
];
function outcomeWorld(){
  if(realTime<128)return;
  at(...resultCenter,()=>inkLayer(ease(p(realTime,128,130)),()=>{
    const t=realTime,u=ease(p(t,132.4,134.4)),end=ease(p(t,147.6,148.4));
    frameBase(-928,-473,1856,948);
    mono('A01 / RESULT DRAWING · SAME CLIENT · SAME WORKFLOW',-865,-426,20,1,{v:.5});
    TX('这次准备，最终得到什么？',0,-350,54,1,{align:'center'});
    TX('A01 · 示例客户信息｜半导体衬底企业 · 流程示意',0,-291,29,1,{align:'center',v:.75});
    // The single dossier unfolds into three usable sheets, never into three clients.
    outcomePages.forEach((q,i)=>{
      const local=ease(p(t,132.4+i*.23,134+i*.23)),x=mix((i-1)*24,(i-1)*574,local),y=-232;
      foldSheet(x,y,520,407,local,.9);
      inkLayer(ease(p(local,.75,1)),()=>{
        mono('0'+(i+1),x-222,y+44,24,1,{v:.65});
        TX(q.title,x,y+104,46,1,{align:'center'});
        L([[x-224,y+136],[x+224,y+136]],1,1.3,.5);
        q.lines.forEach((s,j)=>TX(s,x,y+194+j*52,33,1,{align:'center',v:j===0?.95:.84}));
        L([[x-224,y+324],[x+224,y+324]],1,1.2,.4);
        TX(q.before+' → '+q.after,x,y+372,31,1,{align:'center'});
      });
      const hi=ease(p(t,135+i*2.5,135.6+i*2.5));
      if(hi>0){L([[x-245,y+11],[x-245,y+395],[x+245,y+395]],hi,3,.85);C(x+222,y+41,14,hi,.9,1.7);L([[x+214,y+41],[x+220,y+47],[x+231,y+32]],hi,2.3,.95);}
    });
    inkLayer(1-ease(p(t,132.7,133.5)),()=>{
      mono('A01 / CLIENT DOSSIER',0,-169,24,1,{align:'center',v:.7});
      TX('示例客户信息',0,-81,48,1,{align:'center'});
      TX('半导体衬底企业',0,-12,35,1,{align:'center'});
      TX('依据 · 判断 · 行动',0,92,39,1,{align:'center'});
    });
    const eng=ease(p(t,142.4,143.2));
    inkLayer(1-ease(p(t,147,147.6)),()=>{
      clutch(0,299,eng,Math.max(0,t-143.2),.72);
      TX('同一客户',-654,310,38,1,{align:'center'});TX('持续跟进',666,310,38,1,{align:'center'});
      L([[-502,298],[-280,298]],eng,2.6,.8);L([[300,298],[502,298]],eng,2.6,.8);
      TX('专业数据 × 知识装备 × 业务流程',0,423,38,1,{align:'center',v:.86});
    });
    inkLayer(end,()=>{
      TX('FirmBuddy',0,288,65,1,{align:'center',font:'Georgia',weight:700});
      TX('把分散线索，变成有依据的客户行动',0,364,45,1,{align:'center'});
      TX('同一流程，延伸至融资、并购、回购等业务场景',0,431,31,1,{align:'center',v:.8});
    });
  }));
}
