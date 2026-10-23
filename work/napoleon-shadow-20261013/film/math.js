export const DURATION=64,FPS=24,COUNT=160;
export const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
export const smooth=x=>{x=clamp(x);return x*x*x*(x*(6*x-15)+10)};
export const ramp=(t,a,b)=>smooth((t-a)/(b-a));
export const mix=(a,b,u)=>a+(b-a)*u;
export const rng=seed=>()=>{seed|=0;seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296};
export const transitions=[[12.4,17.6],[28.4,35.6],[46.8,52.2]];
export const sceneAt=t=>t<15?'arcole':t<32.6?'jaffa':t<49.6?'alps':'coronation';
export function cameraAt(t){
 let x=540,y=960,z=1;
 if(t<13){z=mix(1.13,1,ramp(t,1,9));x=mix(440,540,ramp(t,1,9));}
 else if(t<28){z=1+.07*ramp(t,19,23);x=540+35*ramp(t,19,23);y=960+12*ramp(t,19,23);}
 else if(t<35){x=575-35*ramp(t,28,34);z=1.07-.07*ramp(t,28,34);}
 else if(t<49){const u=ramp(t,35,42);x=540;y=960-25*u;z=1+.02*u;}
 else{x=540-50*ramp(t,53,56);y=960-20*ramp(t,53,56);z=1+.065*ramp(t,53,56)-.065*ramp(t,61,64);x+=50*ramp(t,61,64);y+=20*ramp(t,61,64);}
 return{x,y,z};
}
