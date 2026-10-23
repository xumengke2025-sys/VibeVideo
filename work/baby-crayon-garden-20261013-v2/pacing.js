// Monotonic presentation/story clock shared by scene, camera and sound.
export const PACING=[[0,0],[1.2,1.8],[1.8,3.2],[2.8,5.2],[6,10.2],[7.8,12],[9.5,14.8],[10.5,17.5],[16,27],[17,28.5],[18.8,30.1],[20.4,32.5],[21.2,34],[22.4,35.8],[24.5,39.8],[25.7,42],[27.5,44.1],[29,46.4],[30.5,48.7],[31.1,49.6],[33,52.4],[33.5,53],[35,55],[37.7,57.8],[39.4,59.4],[40,60]];
// Monotonic Hermite clock: continuous velocity at every pacing anchor.
const rates=PACING.slice(1).map(([p,s],i)=>(s-PACING[i][1])/(p-PACING[i][0]));
const tangents=PACING.map((_,i)=>i===0?rates[0]:i===PACING.length-1?rates.at(-1):2/(1/rates[i-1]+1/rates[i]));
export function storyTime(t){
 t=Math.max(0,Math.min(40,t));let i=0;while(i<PACING.length-2&&t>PACING[i+1][0])i++;
 const [a,b]=PACING[i],[c,d]=PACING[i+1],h=c-a,u=(t-a)/h;
 return (2*u**3-3*u*u+1)*b+(u**3-2*u*u+u)*h*tangents[i]+(-2*u**3+3*u*u)*d+(u**3-u*u)*h*tangents[i+1];
}
export function presentationTime(s){
 let lo=0,hi=40;for(let i=0;i<40;i++){const m=(lo+hi)/2;if(storyTime(m)<s)lo=m;else hi=m;}return(lo+hi)/2;
}
