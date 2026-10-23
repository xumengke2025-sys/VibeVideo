import * as T from 'three';
export const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
export const mix=(a,b,t)=>a+(b-a)*t;
export const smooth=x=>{x=clamp(x);return x*x*x*(x*(x*6-15)+10)};
export const seg=(t,a,b)=>smooth((t-a)/(b-a));
export const V=(...a)=>new T.Vector3(...a);
export function rng(seed=47){return ()=>{let t=seed+=0x6D2B79F5;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return ((t^t>>>14)>>>0)/4294967296}}
// Analytic integral of the rate curve, independent of request history.
export function clock(t){if(t<18)return t*12;if(t<23){let u=t-18;return 216+12*u-1.1*u*u}if(t<40)return 248.5+t-23;if(t<44){let u=t-40;return 265.5+u+.625*u*u}return 279.5+(t-44)*6}
export function worldTime(t){const rate=t<18?12:t<23?12-11*(t-18)/5:t<40?1:t<44?1+5*(t-40)/4:6;const hz=rate>=6?8:rate>=2?12:0;return clock(hz?Math.floor(t*hz+1e-8)/hz:t)}
