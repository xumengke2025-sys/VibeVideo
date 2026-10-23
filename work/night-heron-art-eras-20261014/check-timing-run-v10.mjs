import fs from 'node:fs';
import {cycleAt,footAt,bodyPoint,STRIDE,distanceAt,timeAtDistance} from './src/run-v10-gait.mjs';
const audio=JSON.parse(fs.readFileSync('audio/events-run-v10.json')),plan=JSON.parse(fs.readFileSync('production-plan-run-v10.json'));
let maxPhaseError=0,maxLockedFootError=0,maxLift=0,minReach=9,maxReach=0,maxBoundaryJump=0;
for(const e of audio.footfalls){const f=footAt(cycleAt(e.time),e.leg==='near'?0:.5),phaseError=Math.min(f.p,1-f.p);maxPhaseError=Math.max(maxPhaseError,phaseError);}
for(let j=0;j<3000;j++){
 const c=j/3000,bob=-17*Math.sin(c*Math.PI*2)**2,angle=-.025+.045*Math.sin(c*Math.PI*2);
 for(const [o,x]of[[0,.47],[.5,.42]]){const f=footAt(c,o),h=bodyPoint([x,.588],bob,angle),d=Math.hypot(f.x-h[0],f.y-h[1]);minReach=Math.min(minReach,d);maxReach=Math.max(maxReach,d);maxLift=Math.max(maxLift,(.84-f.y)*510);}
}
for(let n=2;n<105;n++){
 const o=n%2? .5:0,t=timeAtDistance(n*STRIDE/2),vals=[];
 for(const dt of [.001,.05,.10]){const f=footAt(cycleAt(t+dt),o);if(f.stance)vals.push(distanceAt(t+dt)+f.x*510);}
 if(vals.length>1)maxLockedFootError=Math.max(maxLockedFootError,Math.max(...vals)-Math.min(...vals));
}
for(const c of [0,.54,.54+.46*.22,.54+.46*.56,.54+.46*.8]){const a=footAt((c+1-1e-7)%1,0),b=footAt((c+1e-7)%1,0);maxBoundaryJump=Math.max(maxBoundaryJump,Math.hypot(a.x-b.x,a.y-b.y)*510);}
const sync=audio.sync.map((e,i)=>{const s=plan.timeline.shots[i],at=k=>(s.startFrame+s.events[k])/24;return {era:i+1,grab:e.grab-at('grab'),headUp:e.headUp-at('headUp'),gulp:e.gulp-at('swallowStart'),gone:e.gone-at('fishGone'),cut:e.cut-s.startFrame/24};});
const out={footfalls:audio.footfalls.length,maxPhaseError,maxLockedFootError,maxLiftPixels:maxLift,linkReach:{min:minReach,max:maxReach,allowed:[.035,.415]},maxBoundaryJumpPixels:maxBoundaryJump,sync,audioStatistics:audio.statistics,perception:'timing and signal analysis only; not listened'};
if(maxPhaseError>1e-8||maxLockedFootError>1e-7||minReach<.035||maxReach>.415||maxBoundaryJump>.01||sync.some(s=>Object.values(s).slice(1).some(v=>v!==0)))throw Error(JSON.stringify(out));
fs.mkdirSync('qa/run-v10-timing',{recursive:true});fs.writeFileSync('qa/run-v10-timing/summary.json',JSON.stringify(out,null,2));console.log(JSON.stringify(out));
