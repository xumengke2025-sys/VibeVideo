// One case, one continuous blueprint. Original drawing helpers and apparatus are retained.
const clockKnots=[[0,0],[9,3.5],[10,4.3],[13.2,6.4],[15.2,8],[18,11]];
function linearClock(t,k){if(t<=k[0][0])return k[0][1];for(let i=1;i<k.length;i++)if(t<=k[i][0])return mix(k[i-1][1],k[i][1],p(t,k[i-1][0],k[i][0]));return k.at(-1)[1];}
function openingClock(t){return linearClock(t,clockKnots);}
const storyClock=[[0,0],[15.2,0],[18,2.9],[28,7.3],[32,8.25],[46,8.25],[50,12],[60,16.1],[73.2,16.1],[76,21],[83,25.6],[87,29.3],[92,34.7],[94,38],[96,40.1],[104,52]];
function originalTime(t){if(t>=35.2&&t<38)return quint(0,2.9,0,.44,2.8,p(t,35.2,38));return linearClock(t-20,storyClock);}
const industryCenter=[8350,1510];
const industryIn=bez([5866,1815],[6590,1815],[6980,1940],[7390,1940]);
const industryOut=bez([9310,1940],[9650,2350],[5070,2250],[4220,2700]);
const detourKeys=[[60,5600,1390,.70,0],[63.2,7230,1470,.64,-.015,930,45,.04,0],[65.2,8350,1510,.67,0],[72.8,8350,1510,.67,0],[74.6,6450,2230,.60,.016,-2350,300,-.08,0],[76,3650,2830,.94,0]];
function sampleKeys(t,kk){let i=1;while(i<kk.length-1&&t>kk[i][0])i++;const a=kk[i-1],b=kk[i],h=b[0]-a[0],u=p(t,a[0],b[0]),c={};for(const[j,k]of['x','y','z','r'].entries()){let v=j===2?Math.log(a[j+1]):a[j+1],w=j===2?Math.log(b[j+1]):b[j+1];c[k]=quint(v,w,a[j+5]||0,b[j+5]||0,h,u);if(j===2)c[k]=Math.exp(c[k]);}return c;}
const openingKeys=[[0,1050,1105,.94,-.006],[7.4,1050,1105,.96,0],[9.2,1050,1105,.96,0],[16.4,1050,1105,.95,0],[18.4,1050,1070,.95,0],[27.4,1050,1070,.95,0],[32,1050,1070,.95,0],[35.2,1050,1070,.95,0],[38,1050,1070,.95,0]];
function storyCamera(t){if(t<=38)return sampleKeys(t,openingKeys);const old=t-20;return old>=60&&old<=76?sampleKeys(old,detourKeys):cameraAt(originalTime(t));}
function liveRoute(q,a,b,v=.9){const u=ease(p(filmTime-20,a,b));L(q,u,3,v);if(u>0&&u<1){const z=pathPoint(q,u);C(...z,8,1,.95,2);}}

function judgment(){at(...centers.signals,()=>{
 const t=filmTime-20;
 TX('业务研判：这条线索，怎样跟进？',-730,-335,47,1);
 mono('A01 / SHAREHOLDER SERVICE ASSESSMENT',-730,-390,22,1,{v:.55});
 frameBase(-685,-245,1380,475);rail([[-720,220],[700,220]],.42);
 const items=[['关注信号','公司解禁窗口'],['核对主体','公司 · 股东资料'],['明确切入','股份管理安排']];
 items.forEach(([a,b],i)=>{const u=ease(p(t,32.5+i*1.4,33.2+i*1.4)),x=-650+i*450;
   panel(x,-205,420,155,u,.9,14);mono('0'+(i+1),x+20,-164,22,u,{v:.6});TX(a,x+210,-150,37,u,{align:'center'});TX(b,x+210,-88,33,u,{align:'center'});
   liveRoute([[x+210,-47],[x+210,4],[15,4],[15,48]],35.8+i*.5,37.5+i*.5,.8);
 });
 const u=ease(p(t,38.8,39.5));doc(-620,47,1240,143,u);TX('跟进重点：了解股份事务接口与服务需求',0,104,39,u,{align:'center'});
 TX('AI 辅助整理关注理由、业务条件与沟通问题',0,161,31,u,{align:'center',v:.82});
 gear(-460,225,24,6,t*.38,1,.6,18);gear(-310,225,26,6,meshAngle(t*.38,24,26,[-460,225],[-310,225]),1,.55,18);
 TX('A01 · 示例客户信息 · 半导体企业',-650,345,35,1,{v:.9});
 });}
function signals(){
 const k=ease(p(filmTime-20,31.7,32.5));
 if(k<1){const old=visibility;visibility*=1-k;sourceStation();visibility=old;}
 if(k>0){const old=visibility;visibility*=k;judgment();visibility=old;}
 if(T>8.4&&T<11.7)movingRoute(paths.toHall,8.4,11.7);
}

function industry(){at(...industryCenter,()=>{
 const t=filmTime-20;
 frameBase(-1050,-520,2100,1050);
 TX('产业研判：更懂眼前这家客户',0,-595,60,1,{align:'center'});
 TX('A01 · 示例客户信息｜半导体衬底企业（流程示意）',0,-545,34,1,{align:'center',v:.85});
 // A drafting screen grows from the same table, not a screenshot plane.
 panel(-996,-463,1992,600,1,.72,14);
 mono('INDUSTRY ATLAS / EVIDENCE-BASED RESEARCH',-958,-421,22,1,{v:.5});
 const nodes=[[-770,-240,'材料耗材'],[-770,0,'制造装备'],[-300,-140,'晶体生长'],[210,-140,'衬底'],[710,-140,'外延']];
 const links=[[0,2],[1,2],[2,3],[3,4]];
 links.forEach(([a,b],i)=>{const A=nodes[a],B=nodes[b],q=bez([A[0]+56,A[1]],[A[0]+190,A[1]],[B[0]-190,B[1]],[B[0]-58,B[1]],36);L(q,1,1.8,.25);liveRoute(q,63.8+i*.45,64.7+i*.45,.92);});
 nodes.forEach(([x,y,label],i)=>{const u=ease(p(t,63.4+i*.25,64.2+i*.25));C(x,y,61,1,.35,1.5);C(x,y,53,u,.95,2.7);mono('0'+(i+1),x,y+10,29,u,{align:'center'});TX(label,x,y+106,46,u,{align:'center'});});
 // The case marker lands on the customer's explicit illustrative substrate position.
 const marked=ease(p(t,65.4,66.4));
 if(marked>0){const x=mix(-860,210,marked),y=mix(394,-274,marked);doc(x-220,y-40,440,90,1);TX('A01 · 本次客户',x,y+19,46,1,{align:'center'});L([[x,y+50],[210,-215]],marked,2.3,.9);C(210,-140,75,marked,.9,2);}
 const eu=ease(p(t,67.2,68));
 const sources=[['公司年报','产业位置与业务结构'],['专利原文','技术路线与证据'],['财务披露','经营背景与阶段']];
 sources.forEach(([s,d],i)=>{const x=-785+i*535,u=ease(p(t,67.2+i*.45,68+i*.45));doc(x,173,500,140,u);TX(s,x+250,226,46,u,{align:'center'});TX(d,x+250,282,29,u,{align:'center',v:.82});liveRoute([[210,-45],[210,97],[x+250,97],[x+250,173]],66.7+i*.45,68+i*.45,.72);});
 // Reference-inspired roundtable and three accurately scoped participants.
 L(ellipse(0,443,925,130),1,2.7,.9);L(ellipse(0,473,925,130),1,1.5,.5);L(ellipse(0,443,845,101),1,1.2,.45);
 const experts=[[-660,'产业链研判专家','产业位置'],[0,'第三代／宽禁带半导体','技术与产业化'],[660,'股东增减持专家','服务切入点']];
 experts.forEach(([x,s,d],i)=>{const u=ease(p(t,63+i*.4,63.8+i*.4));panel(x-35,347,70,46,1,.7,12);C(x,329,18,1,.8,1.5);if(i===1){panel(x-290,483,580,110,1,.9,8);TX(s,x,528,38,1,{align:'center'});TX('产业研究专家',x,574,35,1,{align:'center'});}else plaque(s,x-290,483,580,43,1);TX(d,x,432,29,u,{align:'center',v:.85});});
 const result=ease(p(t,70.8,71.5));if(result>0){doc(-465,352,930,108,result);TX('研究成果回到 A01：客户背景与沟通重点',0,420,36,result,{align:'center'});}
 gear(-1044,453,26,6,t*.25,1,.55,20);gear(1044,453,26,6,-t*.25,1,.55,20);
 });
 if(filmTime>=80&&filmTime<=84)at(0,0,()=>carrier(industryIn,ease(p(filmTime-20,60,64)),'A01',220));
 if(filmTime>=92.8&&filmTime<=96)at(0,0,()=>carrier(industryOut,ease(p(filmTime-20,72.8,76)),'A01 · 研究依据',320));
}
function caseTag(){} // Case identity lives on the archive and station labels, not over titles.
function ending(){if(filmTime<120)return;const a=ease(p(filmTime-20,100,100.8));ov.save();ov.scale(scale,scale);ov.globalAlpha=a;const grad=ov.createLinearGradient(0,770,0,1080);grad.addColorStop(0,'rgba(5,23,42,0)');grad.addColorStop(.4,'rgba(5,23,42,.96)');grad.addColorStop(1,'rgba(5,23,42,.96)');ov.fillStyle=grad;ov.fillRect(0,770,1920,310);ot(ov,'FirmBuddy',960,904,76,'#f0f1e8','center',600);ot(ov,'商机发现有方向 · 业务研判有依据 · 客户跟进有准备',960,985,39,'#d7e8f3','center');ov.restore();}
window.renderAt=(t,type='image/png',quality=.95)=>{
 filmTime=Math.max(0,Math.min(124,t));T=originalTime(filmTime);bounds=[];
 const c=storyCamera(filmTime);setCam({...c,z:c.z*scale});proj.k=.43;clear();NIBS.length=0;
 chassis();at(0,0,()=>{rail(industryIn,.43);rail(industryOut,.35);});
 inkLayer(ease(p(filmTime,35.2,37.2)),()=>intro());
 signals();experts();knowledge();visit();follow();industry();
 opening();businessNarrative(filmTime);caseTag();ending();
 compose(inkC,fxC,ovC,{sheet:[9800,4800],cam,seed:19});return type?canvas.toDataURL(type,quality):null;
};
window.cameraAt=storyCamera;window.cameraKeys=[...openingKeys,...storyClock.map(k=>[k[0]+20]),...detourKeys.map(k=>[k[0]+20,...k.slice(1)])].sort((a,b)=>a[0]-b[0]);
window.stateAt=t=>{window.renderAt(t,null);return{time:t,camera:storyCamera(t),buffer:[W,H],duration:124,shot:plan.shots.find(s=>t>=s.start&&t<s.end)?.id,bounds,caseId:'A01',originalTime:T};};
window.__ready=true;window.renderAt(0,null);
const audio=new Audio('./audio/mix.wav'),seek=document.querySelector('#seek'),display=document.querySelector('#time'),button=document.querySelector('#play');let playing=false,started=0,base=0;
seek.oninput=()=>{base=+seek.value;audio.currentTime=base;started=performance.now();window.renderAt(base,null);display.textContent=base.toFixed(2)+' / 124';};
button.onclick=()=>{playing=!playing;button.textContent=playing?'暂停':'播放';if(playing){base=+seek.value;if(base>=124)base=0;started=performance.now();audio.currentTime=base;audio.play().catch(()=>{});}else{base=+seek.value;audio.pause();}};
function tick(){if(playing){const t=Math.min(124,base+(performance.now()-started)/1000);window.renderAt(t,null);seek.value=t;display.textContent=t.toFixed(2)+' / 124';if(t>=124){playing=false;audio.pause();button.textContent='播放';}}requestAnimationFrame(tick);}if(!Q.has('render'))tick();
