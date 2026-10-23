// A single absolute-distance clock for feet, body attitude and the score.
export const STRIDE=280, STANCE=.52;
export const distanceAt=t=>550*t+5*t*t;
export const timeAtDistance=d=>(-550+Math.sqrt(550**2+20*d))/10;
export const cycleAt=t=>((distanceAt(t)/STRIDE)%1+1)%1;
const smooth=u=>u*u*(3-2*u);
function hermite(a,b,va,vb,u,span){return (2*u**3-3*u*u+1)*a+(u**3-2*u*u+u)*va*span+(-2*u**3+3*u*u)*b+(u**3-u*u)*vb*span;}
export function footAt(cycle,offset,size=510){
 const p=(cycle+offset)%1,stance=p<STANCE,rear=.76-STRIDE/size*STANCE;
 if(stance)return {p,stance,x:.76-STRIDE/size*p,y:.84,flex:0};
 const f=(p-STANCE)/(1-STANCE),xs=[rear,.54,.74,.85,.76],ts=[0,.22,.56,.80,1],vs=[-STRIDE/size*(1-STANCE),0,1.0,0,-STRIDE/size*(1-STANCE)];
 let k=0;while(k<3&&f>ts[k+1])k++;
 const span=ts[k+1]-ts[k],u=(f-ts[k])/span,x=hermite(xs[k],xs[k+1],vs[k],vs[k+1],u,span);
 const heights=[0,.235,.26,.175,0],lift=heights[k]+(heights[k+1]-heights[k])*smooth(u);
 return {p,stance,x,y:.84-lift,flex:Math.sin(Math.PI*f),f};
}
export function bodyPoint(p,bob,angle,size=510){const pivot=[.44,.57],dx=p[0]-pivot[0],dy=p[1]-pivot[1];return [pivot[0]+Math.cos(angle)*dx-Math.sin(angle)*dy,pivot[1]+Math.sin(angle)*dx+Math.cos(angle)*dy+bob/size];}
