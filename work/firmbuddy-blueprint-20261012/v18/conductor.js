// Original V17 clocks remain intact, offset six seconds after the new opening.
const closeStart=legacyCamera(122);
function legacyDerivative(t){const h=.00001,a=legacyCamera(t-h),b=legacyCamera(t+h);return[(b.x-a.x)/(2*h),(b.y-a.y)/(2*h),(Math.log(b.z)-Math.log(a.z))/(2*h),(b.r-a.r)/(2*h)];}
const frontEnd=legacyCamera(18);
const closeKeys=[[128,closeStart.x,closeStart.y,closeStart.z,closeStart.r,...legacyDerivative(122)], [130.4,4900,4130,.37,0,0,840,.47,0], [133.2,4900,5550,.91,0], [154,4900,5550,.91,0]];
const frontKeys=[[0,1050,1070,.95,-.008],[5.8,1050,1070,.95,0],[21.6,1050,1070,.95,0],[24,frontEnd.x,frontEnd.y,frontEnd.z,frontEnd.r,...legacyDerivative(18)]];
function finalCamera(t){if(t<24)return sampleKeys(t,frontKeys);if(t>=128)return sampleKeys(t,closeKeys);return legacyCamera(t-6);}
window.renderAt=(t,type='image/png',quality=.95)=>{
  realTime=Math.max(0,Math.min(154,t));filmTime=realTime<23.4?Math.max(0,realTime-6):Math.min(124,realTime-6);T=originalTime(filmTime);bounds=[];
  const c=finalCamera(realTime);setCam({...c,z:c.z*scale});proj.k=.43;clear();NIBS.length=0;
  chassis();at(0,0,()=>{rail(industryIn,.43);rail(industryOut,.35);});
  inkLayer(ease(p(filmTime,35.2,37.2)),()=>intro());
  signals();experts();knowledge();visit();follow();industry();
  narrativeOpening();outcomeWorld();businessNarrative(realTime);
  compose(inkC,fxC,ovC,{sheet:[9800,6500],cam,seed:19});return type?canvas.toDataURL(type,quality):null;
};
window.cameraAt=finalCamera;
window.stateAt=t=>{window.renderAt(t,null);return{time:t,camera:finalCamera(t),buffer:[W,H],duration:154,shot:plan.shots.find(s=>t>=s.start&&t<s.end)?.id,bounds,caseId:'A01',originalTime:T};};
window.__ready=true;window.renderAt(0,null);
const audio=new Audio('./audio/mix.wav'),seek=document.querySelector('#seek'),display=document.querySelector('#time'),button=document.querySelector('#play');let playing=false,started=0,base=0;
seek.max=154;
seek.oninput=()=>{base=+seek.value;audio.currentTime=base;started=performance.now();window.renderAt(base,null);display.textContent=base.toFixed(2)+' / 154';};
button.onclick=()=>{playing=!playing;button.textContent=playing?'暂停':'播放';if(playing){base=+seek.value;if(base>=154)base=0;started=performance.now();audio.currentTime=base;audio.play().catch(()=>{});}else{base=+seek.value;audio.pause();}};
function tick(){if(playing){const t=Math.min(154,base+(performance.now()-started)/1000);window.renderAt(t,null);seek.value=t;display.textContent=t.toFixed(2)+' / 154';if(t>=154){playing=false;audio.pause();button.textContent='播放';}}requestAnimationFrame(tick);}if(!Q.has('render'))tick();
