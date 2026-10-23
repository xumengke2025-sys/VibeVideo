from pathlib import Path
import re

R=Path(__file__).parent
s=(R.parent/'v1'/'scene.js').read_text(encoding='utf-8')
s=s.replace("scene.fog=new T.FogExp2('#242b2c',.009)","scene.fog=new T.FogExp2('#242b2c',.004)")
s=s.replace('box(31,.24,22,M.wood,[4,-.25,-2]','box(59,.24,26,M.wood,[-3.5,-.25,-2]')
s=s.replace('box(30.85,.025,21.85,M.polish,[4,-.111,-2]','box(58.85,.025,25.85,M.polish,[-3.5,-.111,-2]')
s=s.replace("box(30.7,.055,21.7,standard('#27312e',.08,.71),[4,-.07,-2]","box(58.7,.055,25.7,standard('#27312e',.08,.71),[-3.5,-.07,-2]")
s=s.replace('left:-24,right:24,top:19,bottom:-19','left:-38,right:38,top:28,bottom:-28').replace('far:65','far:95')
s=s.replace('rail(inputCurve);','')
s=s.replace("box(1.22,.07,.96,M.ink,[0,.43,0],o,.04);box(1.16,.10,.9,M.ivory,[0,.50,0],o,.065);label('A17',.72,.36,[0,.559,0],o,M.ivory,true);", "const lid=group([0,.43,-.48],o);box(1.22,.07,.96,M.ink,[0,0,.48],lid,.04);box(1.16,.10,.9,M.ivory,[0,.07,.48],lid,.065);label('A17',.72,.36,[0,.129,.48],lid,M.ivory,true);o.userData.lid=lid;")
s=s.replace('screw(x,.562,z,o,.6)', 'screw(x,.132,z+.48,lid,.6)')
insert=r'''
// Complete film: one physical case visits evidence, relationships and consultation.
function lectern(p,title,w=5.4,d=3.8){const g=group(p);base(w,d,g);for(const x of [-w/2+.25,w/2-.25]){turned([x,.44,-.7],.45,.16,g);bar([x,.86,-.7],[x,4.9,-.7],.055,M.brass,g);turned([x,4.85,-.7],.32,.15,g);sphere(.085,M.polish,[x,5.2,-.7],g);}bar([-w/2+.25,4.9,-.7],[w/2-.25,4.9,-.7],.06,M.brass,g);label(title,w-.5,.52,[0,4.64,-.45],g);return g;}
function paperCard(lines,w=1.6,h=1.05,parent=scene){const g=group([0,0,0],parent);box(w+.12,h+.12,.07,M.brass,[0,0,0],g,.055);label(lines,w,h,[0,0,.06],g,M.paper);for(const x of [-w*.36,w*.36]){box(.11,.22,.08,M.blue,[x,h/2+.025,.10],g,.02);}return g;}
const intake=lectern([-26,0,0],'先确认公司和事件',5.4);
label('公司',1.8,.38,[-1.2,3.65,-.25],intake);label('事情',1.8,.38,[1.2,3.65,-.25],intake);
for(const x of [-1.2,1.2]){box(1.95,.14,.56,M.dark,[x,2.74,-.27],intake);bar([x-.8,.7,-.56],[x-.8,3.3,-.56],.035,M.brass,intake);}
const identityCards=[paperCard(['借款公司 A','示例公司'],1.85,.77),paperCard(['还款有压力','示例事件'],1.85,.77)];
const sourceStation=lectern([-20,0,0],'先看资料，再作判断',6.1,4);
const evidenceCards=[0,1,2].map(i=>{const pivot=group([-1.85+i*1.85,3.25,-.2],sourceStation);const card=paperCard([['公告原文','出处：示例资料'],['担保文件','出处：示例资料'],['待核验消息','先保留疑问']][i],1.52,1.17,pivot);bar([0,-2.7,-.16],[0,.7,-.16],.035,M.brass,pivot);return pivot;});
const verifiedCards=[paperCard(['已核对','公告原文'],1.3,.65),paperCard(['已核对','担保文件'],1.3,.65)];
const pendingCard=paperCard(['仍待核验','不作为已知事实'],1.55,.75);
box(2,.25,1.2,M.wood,[2.5,.8,1.5],sourceStation);label('待核验',1.5,.32,[2.5,.9,2.13],sourceStation);
const relationStation=lectern([-12.8,0,-.2],'看看还涉及哪些公司',7.5,4.4);
const relFace=group([0,0,0],relationStation);
const relPs=[[-2.1,2.85,-.10],[0,3.85,-.10],[2.1,2.85,-.10]];
const relNodes=relPs.map((P,i)=>{const o=group(P,relFace);box(1.94,.72,.22,M.brass,[0,0,0],o,.07);label(['借款公司 A','担保方 B','集团企业 C'][i],1.81,.51,[0,0,.13],o);bar([0,-2.35,-.18],[0,-.38,-.18],.04,M.brass,o);return o;});
const relLinks=[[0,1],[1,2]].map(([a,b],i)=>{const g=group([0,0,0],relFace);const A=new T.Vector3(...relPs[a]),B=new T.Vector3(...relPs[b]),D=B.clone().sub(A).normalize();A.addScaledVector(D,.65);B.addScaledVector(D,-.65);A.z=B.z=.07;bar(A.toArray(),B.toArray(),.045,M.polish,g);for(const v of [A,B]){sphere(.10,M.polish,v.toArray(),g);}const mid=A.add(B).multiplyScalar(.5);label(i?'同属集团':'担保关系',1.35,.32,[mid.x,2.10,.15],g);return g;});
const backgroundRelation=paperCard(['行业相近','不直接接入试验'],1.95,.77,relationStation);backgroundRelation.position.set(0,1.13,1.5);
// The consultation circle has four real seats; documents travel to and from them.
const council=group([-6,0,-2]);const councilFoot=group([0,0,-.8],council);base(6.4,7.2,councilFoot);
for(const x of [-2.3,2.3]){turned([x,.44,-1.5],1.4,.25,council);bar([x,1.4,-1.5],[x,2.1,-1.5],.07,M.brass,council);}
const table=cyl(2.6,.16,M.wood,[0,1.65,-2.6],council);table.scale.z=.65;const tableRim=ring(2.58,.035,M.polish,[0,1.75,-2.6],council);tableRim.scale.y=.65;
label('带着资料，请专家一起看',5.2,.46,[0,4.75,-2.45],council);
for(const x of [-2.8,2.8]){turned([x,.44,-2.6],.4,.18,council);bar([x,.84,-2.6],[x,4.96,-2.6],.055,M.brass,council);sphere(.10,M.polish,[x,5,-2.6],council);}
const expertNames=['尽调评估专家','产业授信评估专家','合规风险专家','风险监控专家'];
const experts=expertNames.map((name,i)=>{const P=[(i-1.5)*1.52,2.9,-2.1-Math.sin((i+.5)/4*Math.PI)*.65];const g=group(P,council);box(1.36,.95,.43,M.wood,[0,0,0],g,.09);box(1.21,.77,.06,M.ebony,[0,.03,.245],g);label(name,1.27,.38,[0,-.12,.30],g);for(const x of [-.5,.5])turned([x,-1.3,-.03],.85,.13,g);const lamp=ring(.21,.028,M.polish,[0,.68,0],g,[0,0,0]);const pupil=cyl(.15,.07,M.ivory,[0,.68,0],g);pupil.rotation.x=Math.PI/2;return {g,P,parcel:paperCard(['A17','同一份资料'],.90,.52,council)};});
const opinionCards=[paperCard(['先核对','担保责任'],1.36,.75,council),paperCard(['还要查','资金到位时间'],1.65,.75,council)];
const reviewCards=[paperCard(['按现有情况','保留已有压力'],1.6,.76,council),paperCard(['情况变差','相关方影响增大'],1.6,.76,council),paperCard(['假设采取措施','仍需复核'],1.6,.76,council)];
const followup=paperCard(['待查事项','资金何时到位？'],2.0,.85,council);
box(2.3,.24,1.25,M.wood,[2.15,.8,1.5],council);
for(const x of [-1.9,0,1.9])bar([x,1.74,-1.15],[x,2.1,-1.15],.028,M.brass,council);
const earlyNodes=[[-26,1.18,0],[-20,1.18,0],[-12.8,1.18,0],[-6,1.18,-2],[-4.2,1.18,0],[0,1.18,0]];
const earlyPaths=earlyNodes.slice(0,-1).map((a,i)=>{const b=earlyNodes[i+1];return new T.CatmullRomCurve3([new T.Vector3(...a),new T.Vector3((a[0]+b[0])/2,1.18,a[2]),new T.Vector3(...b)],false,'centripetal');});earlyPaths.forEach(c=>rail(c));
const recordPath=new T.CatmullRomCurve3([new T.Vector3(0,1.18,0),new T.Vector3(2,1.18,1.2),new T.Vector3(8,1.18,2),new T.Vector3(15,1.18,2),new T.Vector3(18.5,1.18,1.3)],false,'centripetal');rail(recordPath);
// Two separate paper tracks: company actions and simulated messages, never news claims.
const logRig=group([18.5,0,-.8]);
recorder.visible=false;base(4.8,3.4,logRig);
for(const x of [-2.1,2.1]){turned([x,.44,-.7],.4,.16,logRig);bar([x,.84,-.7],[x,5.4,-.7],.06,M.brass,logRig);sphere(.10,M.polish,[x,5.4,-.7],logRig);}
bar([-2.1,5.15,-.7],[2.1,5.15,-.7],.065,M.brass,logRig);label('每一步，都能回头查',4,.48,[0,5.05,-.4],logRig);
const logs=[];for(let i=0;i<2;i++){const x=i?1.10:-1.10;label(i?'模拟消息':'公司应对',1.9,.40,[x,4.4,.10],logRig);box(1.90,2.6,.12,M.ebony,[x,2.95,-.10],logRig);const roll=cyl(.26,1.95,M.paper,[x,4.0,.06],logRig);roll.rotation.z=Math.PI/2;const roll2=cyl(.26,1.95,M.paper,[x,1.62,.06],logRig);roll2.rotation.z=Math.PI/2;for(const y of [1.62,4])for(const dx of [-1.02,1.02]){bar([x+dx,y,-.5],[x+dx,y,.25],.05,M.brass,logRig);}const lines=(i?['模拟讨论增加','关注担保责任','不是真实新闻']:['与公司沟通核验','假设寻求资金','记录措施与变化']).map((txt,j)=>{const g=paperCard([txt,'示例过程'],1.7,.53,logRig);g.position.set(x,3.56-j*.72,.13);return g;});logs.push({roll,roll2,lines});}
const resultBundle=paperCard(['A17 · 试验记录','条件、过程、待查问题'],2.8,.85);
resultBundle.rotation.order='YXZ';
'''
s=s.replace('// Background stays quiet so the company relationships remain the focus.',insert)
# Keep the validated 24-second trial mechanics, retimed into the full film.
sample=s[s.index(' const t=Math.max'):s.index(' const pose=cameraAt(t);')]
sample=sample.replace('const t=Math.max(0,Math.min(24,seconds))','const t=Math.max(0,Math.min(24,seconds-32))')
sample=sample.replace('mainCase.position.set(-4.2+4.2*travel,1.43,0);','')
sample=sample.replace('return values;','return values;')
poses=[
(0,[-26.5,5.0,9],[-26,2.65,0],39),(2,[-26.5,5,9],[-26,2.65,0],39),(5.5,[-25.3,4.5,8],[-26,2.1,0],39),
(8.7,[-20,5.2,10],[-20,2.55,0],39),(13,[-19.6,5.1,10],[-20,2.5,0],39),
(16.5,[-12.8,6.1,11],[-12.8,2.8,0],40),(21.5,[-12.6,5.8,10.6],[-12.8,2.9,0],40),
(25,[-5.7,6.7,10],[-6,2.3,-3],40),(29,[-5.7,6.7,10],[-6,2.3,-3],40),
(32,[-5.5,4.2,7.3],[-3.3,1.7,0],36),
(34.2,[-3.1,4.5,7.4],[0,1.85,0],36),(36.2,[-2.8,4.7,7.7],[.1,1.9,0],36),
(39,[6.4,7.2,10],[6,2,-2.5],39),(41.4,[11,9,13.5],[10.1,3.1,-6],40),
(43.6,[6,5.4,1.4],[5.2,3.4,-6.15],42),(45,[6,5.4,1.4],[5.2,3.4,-6.15],42),
(46.4,[10.5,5.4,1.4],[10.1,3.4,-6.15],42),(49,[10.5,5.4,1.4],[10.1,3.4,-6.15],42),
(50.4,[15.4,5.4,1.4],[15,3.4,-6.15],42),(53,[15.4,5.4,1.4],[15,3.4,-6.15],42),
(55,[11,9,13.5],[10.1,3.1,-6],40),
(57,[9,5.4,10],[8,1.9,1.7],41),(59.5,[18.7,5.7,9],[18.5,2.8,-.2],40),(65,[18.7,5.7,9],[18.5,2.8,-.2],40),
(67,[17,6.3,12],[16,1.9,3.5],41),(69,[7,6.5,13],[6,1.9,4.7],41),(71,[-3,6.5,11],[-4,1.9,3],41),
(73,[-5.7,6.7,10],[-6,2.3,-3],40),(76.7,[-5.7,6.7,10],[-6,2.3,-3],40),
(80,[-3,30,51],[-3.5,1.4,-2],43)]
posejs='const poses='+str([dict(t=t,P=P,L=L,v=[0,0,0],lv=[0,0,0],f=f) for t,P,L,f in poses]).replace("'",'"')+';'
s=re.sub(r'const poses=\[.*?\n\];',posejs,s,flags=re.S)
start=s.index('function textOverlay(t)')
s=s[:start]+r'''
const captions=[
 [0,'Risky 风险视角','围绕一件事，把资料和判断连起来'],
 [2.5,'先确认是哪家公司、哪件事','同一案件 A17'],
 [7,'先看资料从哪里来','公告、文件和消息，都要有出处'],
 [10,'核对过的资料，随案保存','还没查清的，单独留下'],
 [15,'看看还涉及哪些公司','担保、集团等关系，要有资料支持'],
 [19,'有关系，也要分清是什么关系','行业相近，不等于一定受到影响'],
 [23,'带着同一份资料，请专家一起看','从业务、行业、合规等角度讨论'],
 [27,'把意见和疑问都留下','还有什么没查清，接着查'],
 [32,'固定这次使用的资料','后面比较时，起点保持一致'],
 [36.4,'选好条件，确认后再试','需要比较时，再分别设置其他条件'],
 [41.4,'A 还款有压力，B 为它担保','黄柱越高，示例中的影响越大'],
 [45.5,'如果融资更难，先看 A 的变化','再沿着关系，看看可能影响谁'],
 [49.9,'假设获得资金支持','压力可能减轻，仍需看后续变化'],
 [54,'把不同条件下的结果放在一起','这些是条件假设，不是事情一定会发生'],
 [57,'结果怎样来的，每一步都留下','公司如何应对，和模拟消息分开看'],
 [61,'模拟消息，不是真实新闻','回看当时的条件、过程和资料'],
 [66,'带着结果和问题，回到同一件事','原来的资料、专家意见都还在'],
 [72,'再请专家复核，留下待查事项','例如：资金支持何时能够到位？'],
 [77,'查资料 · 请专家 · 换条件 · 再复核','Risky 风险视角']
];
function textOverlay(t){const s=W/1920;ctx.save();ctx.scale(s,s);let cap=captions[0];for(const c of captions)if(t>=c[0])cap=c;const a=Math.min(ramp(t,0,.7),1-ramp(t,79.2,80));const gr=ctx.createLinearGradient(0,878,0,1080);gr.addColorStop(0,'rgba(8,14,14,0)');gr.addColorStop(1,'rgba(8,14,14,.84)');ctx.fillStyle=gr;ctx.fillRect(0,878,1920,202);ctx.globalAlpha=a;ctx.textAlign='center';ctx.fillStyle='#f3ead5';ctx.font='400 34px "Microsoft YaHei"';ctx.fillText(cap[1],960,970);ctx.fillStyle='#d4c9b2';ctx.font='25px "Microsoft YaHei"';ctx.fillText(cap[2],960,1013);ctx.fillStyle='#b5ac98';ctx.font='19px "Microsoft YaHei"';ctx.fillText('合成案例 · 机制示意，不是实际预测',960,1053);ctx.restore();}
function interpolatePosition(o,a,b,u){o.position.fromArray(a.map((v,j)=>mix(v,b[j],u)));}
window.renderAt=(seconds,{overview=false}={})=>{
 const full=Math.max(0,Math.min(80,seconds));
''' + sample + r'''
 // Every moving item is a deterministic function of absolute time.
 const earlyTimings=[[6,8.5],[14,16.2],[22,24.5],[30,32],[32,34.35]];
 let which=0,uu=0;for(let i=0;i<earlyTimings.length;i++){if(full>=earlyTimings[i][0]){which=i;uu=ramp(full,...earlyTimings[i]);}}
 place(mainCase,earlyPaths[which],uu,.25);
 if(full>=55)place(mainCase,recordPath,ramp(full,55,59),.25);
 if(full>=66)place(mainCase,returning,ramp(full,66,72),.25);
 const lidOpen=(a,b,c,d)=>ramp(full,a,b)-ramp(full,c,d);mainCase.userData.lid.rotation.x=-1.45*Math.max(lidOpen(1.5,2.3,5.2,5.8),lidOpen(10,10.7,13.2,13.8),lidOpen(26.4,27,29.3,29.8),lidOpen(71.9,72.4,72.9,73.4));
 identityCards.forEach((o,i)=>{const q=ramp(full,2.4+i*1.5,3.5+i*1.5);o.visible=full<3.6+i*1.5;o.scale.setScalar(1-.65*q);interpolatePosition(o,[-27.2+i*2.4,3.15,.25],[-26,1.65,0],q);});
 evidenceCards.forEach((o,i)=>{o.rotation.y=(i-1)*.98*(1-ramp(full,8.7,10.2));});
 verifiedCards.forEach((o,i)=>{const q=ramp(full,10.8+i*.8,12+i*.8);o.visible=full>=10.7+i*.8&&full<13.5;o.scale.setScalar(1-.45*q);interpolatePosition(o,[-21.85+i*1.85,3.25,.12],[-20,1.75,0],q);});
 {const q=ramp(full,11.7,13.1);pendingCard.visible=full>=11.7;interpolatePosition(pendingCard,[-18.15,3.25,.12],[-17.5,1.32,1.5],q);}
 relNodes.forEach((o,i)=>o.rotation.y=(i-1)*1.15*(1-ramp(full,16.4,18)));
 relLinks.forEach((o,i)=>{o.visible=full>=17+i*.6;o.scale.setScalar(Math.max(.001,ramp(full,17+i*.6,18.3+i*.6)));});
 experts.forEach((e,i)=>{const q=ramp(full,24.8+i*.25,26.2+i*.25);e.parcel.visible=full>=24.8+i*.25&&full<30;e.parcel.scale.setScalar(.8);interpolatePosition(e.parcel,[0,2,0],[e.P[0],e.P[1]+.7,e.P[2]+.65],q);});
 opinionCards.forEach((o,i)=>{const q=ramp(full,27+i*.5,28.6+i*.5);o.visible=full>=27+i*.5&&full<30;o.scale.setScalar(1-.45*q);interpolatePosition(o,[-1.5+i*3,3.1,-1.7],[0,1.85,0],q);});
 logs.forEach((log,i)=>{const q=ramp(full,59,65);log.roll.rotation.x=q*TAU*2;log.roll2.rotation.x=q*TAU*2;log.lines.forEach((o,j)=>{const a=59.2+j*1.3+i*.35;o.visible=full>=a;o.position.y=3.56-j*.72-.13*(1-ramp(full,a,a+.5));});});
 drum.rotation.x=ramp(full,59,65)*TAU*2;
 {const q=ramp(full,64.4,65.7);resultBundle.visible=full>=64.4&&full<72;const start=[18.5,3.4,.8],end=[18.5,2.05,1.3];interpolatePosition(resultBundle,start,end,q);if(full>=66){resultBundle.position.copy(mainCase.position);resultBundle.position.y+=.62;resultBundle.rotation.y=mainCase.rotation.y;}else resultBundle.rotation.y=0;resultBundle.rotation.x=-Math.PI/2*q;resultBundle.scale.setScalar(1-.5*q);}
 reviewCards.forEach((o,i)=>{const q=ramp(full,72.2+i*.3,73.5+i*.3);o.visible=full>=72.2+i*.3;interpolatePosition(o,[0,1.95,0],[-1.9+i*1.9,2.48,-1.15],q);});
 {const q=ramp(full,74.1,75.6);followup.visible=full>=74.1;interpolatePosition(followup,[1.55,3.1,-1.5],[2.15,1.45,1.5],q);}
 const pose=cameraAt(full);if(overview){pose.P=[-3,35,56];pose.L=[-3,1.5,-2];pose.f=44;}camera.position.fromArray(pose.P);camera.lookAt(new T.Vector3(...pose.L));camera.fov=pose.f;camera.updateProjectionMatrix();renderer.render(scene,camera);ctx.clearRect(0,0,W,H);ctx.drawImage(renderer.domElement,0,0,W,H);if(!overview)textOverlay(full);if(full>79.2){ctx.fillStyle=`rgba(12,18,17,${ramp(full,79.2,80)})`;ctx.fillRect(0,0,W,H);}
 return {t:full,trialTime:t,travel,clamp:closed,round,illustrativeStates,notEngineResults:true,case:mainCase.position.toArray(),copies:clones.map(o=>({visible:o.visible,p:o.position.toArray()})),camera:pose,parts:partCount,calls:renderer.info.render.calls,triangles:renderer.info.render.triangles};
};
window.capture=(type='image/png',quality=.97)=>canvas.toDataURL(type,quality);
window.sceneInfo={parts:partCount,three:T.REVISION,width:W,height:H,duration:80,style:'eighteenth-century-instrument',purpose:'full-risky-user-explainer',businessMapping:'../BUSINESS-MAPPING.md',notEngineResults:true};
window.renderAt(0);window.ready=true;
'''
(R/'scene.js').write_text(s,encoding='utf-8')
render=(R/'render.cjs').read_text(encoding='utf-8').replace('args.duration||24','args.duration||80')
(R/'render.cjs').write_text(render,encoding='utf-8')
print('Built full scene:',len(s),'characters')
