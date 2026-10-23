export const DURATION=36;
const knots=[[0,0],[6,10],[9,15],[17,27],[21.5,32],[27,41],[31.5,45],[36,50]];
const remap=(value,from,to)=>{const t=Math.max(0,Math.min(knots.at(-1)[from],value));for(let i=1;i<knots.length;i++){const a=knots[i-1],b=knots[i];if(t<=b[from])return a[to]+(b[to]-a[to])*(t-a[from])/(b[from]-a[from])}return knots.at(-1)[to]};
export const sourceAt=t=>remap(t,0,1);
export const mediaAt=t=>remap(t,1,0);
export const LAUGH_BEATS=[45.65,46.03,46.41,47.04,47.42,47.80,48.43,48.81,49.19];
export function laughAt(t,delay=0){let pulse=0;for(const b of LAUGH_BEATS){const u=(t-b-delay)/.26;if(u>=0&&u<1)pulse=Math.max(pulse,Math.sin(Math.PI*u)**.7)}return pulse}
