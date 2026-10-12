// Original absolute-time subject rigs. No engine dependency or frame-history state.
const add=(a,b)=>a.map((x,i)=>x+b[i]);
const sub=(a,b)=>a.map((x,i)=>x-b[i]);
const mul=(a,k)=>a.map(x=>x*k);
const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const length=a=>Math.hypot(...a);
const unit=(a,fallback)=>length(a)>1e-7?mul(a,1/length(a)):[...fallback];
const value=(a,t)=>typeof a==='function'?a(t):a;
const position=(a,n)=>{
  if(!Array.isArray(a)||a.length!==n||!a.every(Number.isFinite))throw Error(`Subject must return ${n} finite coordinates`);
  return [...a];
};

// Finite, normalized trailing exponential convolution, evaluated afresh at every t.
// response is seconds, not a per-frame lerp coefficient. Zero response gives exact sampling.
function sampler(subject,n,{response=0.10,history=0.6,samples=24,range=[-Infinity,Infinity]}={}){
  if(![response,history].every(x=>Number.isFinite(x)&&x>=0)||!Number.isInteger(samples)||samples<2)throw Error('Invalid smoothing settings');
  if(!(range.length===2&&range[0]<=range[1]))throw Error('Invalid subject range');
  const raw=t=>position(subject(Math.max(range[0],Math.min(range[1],t))),n);
  return t=>{
    if(response===0||history===0)return raw(t);
    const dt=history/samples;
    let sum=Array(n).fill(0),weight=0;
    for(let i=0;i<=samples;i++){
      const age=i*dt,w=Math.exp(-age/response)*(i===0||i===samples?0.5:1);
      sum=add(sum,mul(raw(t-age),w));weight+=w;
    }
    return mul(sum,1/weight);
  };
}

/** subject(t) -> [x,y,z]. offset [right,world-up,back] in world units;
 * space='heading' follows the smoothed horizontal tangent, 'world' uses XYZ offset.
 * lag is a delay, response is smoothing, lead is velocity anticipation; all in seconds.
 * No collision avoidance, auto-framing, depth-of-field, or focus-distance simulation.
 */
export function follow3D({subject,offset=[4,2,7],space='heading',up=[0,1,0],forward=[0,0,1],
  lag=0.04,lead=0.12,lookOffset=[0,0,0],fov=42,roll=0,velocityStep=1/120,...smoothing}){
  if(typeof subject!=='function'||!['heading','world'].includes(space))throw Error('Invalid follow3D subject/space');
  if(!(velocityStep>0&&Number.isFinite(velocityStep))||![lag,lead].every(Number.isFinite))throw Error('Invalid time settings');
  const sample=sampler(subject,3,smoothing),worldUp=unit(position(up,3),[0,1,0]);
  const fallbackRight=unit(cross(position(forward,3),worldUp),[1,0,0]);
  const timeRange=smoothing.range||[-Infinity,Infinity];
  const headingTime=t=>Math.max(timeRange[0],Math.min(timeRange[1],t));
  const derivative=t=>mul(sub(sample(t+velocityStep),sample(t-velocityStep)),1/(2*velocityStep));
  return t=>{
    // At the opening, infer the heading at the valid boundary rather than the clamped pre-roll.
    const velocity=derivative(headingTime(t-lag)),right=unit(cross(velocity,worldUp),fallbackRight);
    const heading=unit(cross(worldUp,right),forward);
    const o=position(value(offset,t),3);
    const relative=space==='world'?o:add(add(mul(right,o[0]),mul(worldUp,o[1])),mul(heading,-o[2]));
    const p=add(sample(t-lag),relative);
    const target=add(add(sample(t),mul(derivative(t),lead)),position(value(lookOffset,t),3));
    const lens=value(fov,t),bank=value(roll,t);
    if(!(lens>0&&lens<180&&Number.isFinite(bank))||length(sub(target,p))<1e-7)throw Error('Invalid camera pose');
    return {position:p,target,fov:lens,roll:bank};
  };
}

/** subject(t) -> [x,y]. Camera center in world units; zoom is world-to-screen scale.
 * Render world: translate(width/2,height/2), scale(zoom), translate(-x,-y).
 * offset moves the camera center, so the subject appears on the opposite screen side.
 */
export function follow2D({subject,offset=[0,0],lag=0.04,lead=0.12,zoom=1,velocityStep=1/120,...smoothing}){
  if(typeof subject!=='function'||!(velocityStep>0&&Number.isFinite(velocityStep))||![lag,lead].every(Number.isFinite))throw Error('Invalid follow2D settings');
  const sample=sampler(subject,2,smoothing);
  return t=>{
    const velocity=mul(sub(sample(t+velocityStep),sample(t-velocityStep)),1/(2*velocityStep));
    const center=add(add(sample(t-lag),mul(velocity,lead)),position(value(offset,t),2));
    const z=value(zoom,t);if(!(z>0&&Number.isFinite(z)))throw Error('Invalid zoom');
    return {x:center[0],y:center[1],zoom:z};
  };
}

/** Blend a follow pose into a separately designed reveal/next-target pose.
 * Linear position/target interpolation requires inspection of the actual spatial corridor.
 * Continuous weight plus endpoint poses provides position continuity, not automatic C1 velocity.
 */
export function blendPose(a,b,w){
  w=Math.max(0,Math.min(1,w));
  const mix=(x,y)=>x+(y-x)*w;
  return {position:a.position.map((x,i)=>mix(x,b.position[i])),target:a.target.map((x,i)=>mix(x,b.target[i])),
    fov:mix(a.fov,b.fov),roll:mix(a.roll||0,b.roll||0)};
}
