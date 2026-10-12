// Original quasi-static illustration helpers; seconds/units are supplied by caller.
// No fluid solver, inertia, damping or impact simulation. Preload is a force.
export function valveState({pressure,area=1,preload=1,stiffness=1,stroke=1,restLength=2,seat=0}){
  if(![pressure,area,preload,stiffness,stroke,restLength,seat].every(Number.isFinite)||area<=0||preload<0||stiffness<=0||stroke<=0||restLength<=stroke)throw new RangeError('Invalid valve parameters');
  const drive=pressure*area,raw=(drive-preload)/stiffness;
  const displacement=Math.max(0,Math.min(stroke,raw));
  return {displacement,disc:seat+displacement,springLength:restLength-displacement,
    springForce:preload+stiffness*displacement,drive,open:displacement>1e-8,
    contact:displacement<=1e-8,limited:raw>=stroke};
}

// Cubic Hermite path: explicit positions and velocities; no hidden frame state.
export function pathAt(t,knots){
  if(!Number.isFinite(t)||!Array.isArray(knots)||knots.length<2)throw new RangeError('Invalid path');
  const n=knots[0].p?.length;
  if(!n||knots.some((k,i)=>!Number.isFinite(k.t)||(i>0&&k.t<=knots[i-1].t)||![k.p,k.v].every(a=>Array.isArray(a)&&a.length===n&&a.every(Number.isFinite))))throw new RangeError('Invalid knots');
  if(t<=knots[0].t)return [...knots[0].p];if(t>=knots.at(-1).t)return [...knots.at(-1).p];
  const i=knots.findIndex(k=>k.t>t),a=knots[i-1],b=knots[i],d=b.t-a.t,u=(t-a.t)/d;
  return a.p.map((v,j)=>(2*u**3-3*u*u+1)*v+(u**3-2*u*u+u)*d*a.v[j]+(-2*u**3+3*u*u)*b.p[j]+(u**3-u*u)*d*b.v[j]);
}
