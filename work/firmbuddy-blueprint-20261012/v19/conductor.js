// Continuous paper cinematography: follow the same dossier between dedicated work cells.
const cameraKeys=[
 [0,1200,1100,.96,-.008],[9.6,1200,1100,.96,0],[21.6,1200,1100,.96,0],
 [24,1450,1180,.94,0],[25.5,2650,1180,.88,-.014,980,0,0,0],[27.2,3500,1100,.94,0],[39.6,3500,1100,.94,0],
 [41.6,4920,1320,.71,.013,1100,40,-.02,0],[43.6,6200,1160,.66,0],[54.4,6200,1160,.66,0],
 [56.2,7550,1230,.70,-.016,1000,-20,.02,0],[58.4,9000,1100,.94,0],[67.2,9000,1100,.94,0],
 [69.2,10020,2490,.72,.026,0,1100,0,0],[71.2,9000,3600,.94,0],[80,9000,3600,.94,0],
 [82,7550,3690,.83,-.016,-1100,0,0,0],[84,6200,3600,.94,0],[96,6200,3600,.94,0],
 [97.6,4900,3670,.83,.016,-1100,0,0,0],[99.2,3500,3600,.94,0],[104,3500,3600,.94,0],
 [108,1000,3350,.66,-.016,-400,-650,-.02,0],[112,1450,1220,.84,0],[113,1450,1220,.84,0],
 [116.6,5500,2550,.161,0],[120,5500,2550,.161,0]
];
function sampleCamera(t){let i=1;while(i<cameraKeys.length-1&&t>cameraKeys[i][0])i++;const a=cameraKeys[i-1],b=cameraKeys[i],h=b[0]-a[0],u=p(t,a[0],b[0]),c={};for(const[j,k]of['x','y','z','r'].entries()){const v=j===2?Math.log(a[j+1]):a[j+1],w=j===2?Math.log(b[j+1]):b[j+1];c[k]=quint(v,w,a[j+5]||0,b[j+5]||0,h,u);if(j===2)c[k]=Math.exp(c[k]);}return c;}
const cells=[['intake',intake],['collect',collect],['hall',hall],['industry',industryCell],['knowledge',knowledgeCell],['assembly',assemblyCell],['follow',followCell]];
window.renderAt=(t,type='image/png',quality=.95)=>{
 realTime=Math.max(0,Math.min(plan.duration,t));T=realTime;bounds=[];const c=sampleCamera(realTime);setCam({...c,z:c.z*scale});proj.k=.43;clear();NIBS.length=0;
 machineChassis();for(const[name,draw]of cells){const[x,y]=ST[name];if(localVisible(x,y,name==='hall'?1500:1150,name==='hall'?950:650))draw();}
 caseDossier();overlay();compose(inkC,fxC,ovC,{sheet:[11200,5300],cam,seed:19});return type?canvas.toDataURL(type,quality):null;
};
window.cameraAt=sampleCamera;window.caseAt=caseState;
window.stateAt=t=>{window.renderAt(t,null);return{time:t,camera:sampleCamera(t),case:caseState(t),buffer:[W,H],duration:120,shot:plan.shots.find(s=>t>=s.start&&t<s.end)?.id,bounds,caseId:'A01'};};
window.design={cameraKeys,shots:plan.shots,duration:plan.duration};window.__ready=true;window.renderAt(0,null);
const audio=new Audio('./audio/mix.wav'),seek=document.querySelector('#seek'),display=document.querySelector('#time'),button=document.querySelector('#play');let playing=false,started=0,base=0;
seek.max=120;seek.oninput=()=>{base=+seek.value;audio.currentTime=base;started=performance.now();window.renderAt(base,null);display.textContent=base.toFixed(2)+' / 120';};
button.onclick=()=>{playing=!playing;button.textContent=playing?'暂停':'播放';if(playing){base=+seek.value;if(base>=120)base=0;started=performance.now();audio.currentTime=base;audio.play().catch(()=>{});}else{base=+seek.value;audio.pause();}};
function tick(){if(playing){const t=Math.min(120,base+(performance.now()-started)/1000);window.renderAt(t,null);seek.value=t;display.textContent=t.toFixed(2)+' / 120';if(t>=120){playing=false;audio.pause();button.textContent='播放';}}requestAnimationFrame(tick);}if(!Q.has('render'))tick();
