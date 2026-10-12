import assert from 'node:assert/strict';
import {writeFileSync} from 'node:fs';
import {springFrom,springTrack,logZoom,morphPoints} from 'file:///D:/Codex/skills/vibe-video/assets/continuity.mjs';
// Independent integration of x'' = w²(target-x) - 2*z*w*x'.
function integrate(end,{from,to,velocity=0,frequency=3,damping=1},events=[]){
 const n=Math.ceil(end/0.00002),dt=end/n,w=2*Math.PI*frequency;let x=from,v=velocity;
 const derivative=(position,speed,target)=>[speed,w*w*(target-position)-2*damping*w*speed];
 for(let i=0;i<n;i++){
  let target=to;for(const event of events)if(i*dt>=event.time-1e-10)target=event.value;
  const a=derivative(x,v,target),b=derivative(x+a[0]*dt/2,v+a[1]*dt/2,target),c=derivative(x+b[0]*dt/2,v+b[1]*dt/2,target),d=derivative(x+c[0]*dt,v+c[1]*dt,target);
  x+=dt*(a[0]+2*b[0]+2*c[0]+d[0])/6;v+=dt*(a[1]+2*b[1]+2*c[1]+d[1])/6;
 }return x;
}
const errors=[];
for(const damping of [.65,1,1.8])for(const t of [.1,.3,1]){
 const parameters={from:20,to:180,velocity:35,frequency:3,damping};
 const error=Math.abs(springFrom(t,parameters)-integrate(t,parameters));errors.push(error);assert(error<1e-6);
}
const events=[{time:.2,value:150},{time:.4,value:50},{time:.7,value:200}];
for(const damping of [.8,1,1.6]){
 const actual=springTrack(1,20,events,{frequency:3,damping}),reference=integrate(1,{from:20,to:20,frequency:3,damping},events);
 assert(Math.abs(actual-reference)<.005);
 const t=.4,h=1e-6,left=(springTrack(t,20,events,{damping})-springTrack(t-h,20,events,{damping}))/h,right=(springTrack(t+h,20,events,{damping})-springTrack(t,20,events,{damping}))/h;
 assert(Math.abs(left-right)<.03);
}
const values=[.1,.8,.2,.8,0,1].map(t=>springTrack(t,20,events));assert.equal(values[1],values[3]);
const ratios=Array.from({length:4},(_,i)=>logZoom(1,256,(i+1)/4)/logZoom(1,256,i/4));ratios.forEach(r=>assert(Math.abs(r-4)<1e-12));
const a=[{x:0,y:0},{x:3,y:5}],b=[{x:10,y:20},{x:13,y:25}];assert.deepEqual(morphPoints(a,b,.5),[{x:5,y:10},{x:8,y:15}]);assert.deepEqual(a,[{x:0,y:0},{x:3,y:5}]);
assert.throws(()=>morphPoints(a,[b[0]],.5));assert.throws(()=>springTrack(1,0,[{time:2,value:1},{time:1,value:2}]));
const result={status:'passed',numerical_spring_max_error:Math.max(...errors),checked:['underdamped/critical/overdamped against RK4','multiple target changes','velocity continuity at retarget','repeat out-of-order values','constant logarithmic zoom speed','point correspondence and no mutation','invalid topology/event order rejected']};
writeFileSync(new URL('./continuity-verification.json',import.meta.url),JSON.stringify(result,null,2));console.log(JSON.stringify(result));
