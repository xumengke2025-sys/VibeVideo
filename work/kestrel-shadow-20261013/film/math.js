export const DURATION=30,FPS=24,COUNT=14;
export const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
export const mix=(a,b,u)=>a+(b-a)*u;
export const smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
export const ramp=(t,a,b)=>smooth((t-a)/(b-a));
export function spline(keys,t){
 if(t<=keys[0][0])return keys[0].slice(1);if(t>=keys.at(-1)[0])return keys.at(-1).slice(1);
 let i=0;while(t>keys[i+1][0])i++;const a=keys[i],b=keys[i+1],p=keys[Math.max(0,i-1)],q=keys[Math.min(keys.length-1,i+2)],dt=b[0]-a[0],u=(t-a[0])/dt;
 return a.slice(1).map((x,k)=>{const j=k+1,m0=(b[j]-p[j])/(b[0]-p[0]),m1=(q[j]-a[j])/(q[0]-a[0]);return (2*u**3-3*u*u+1)*x+(u**3-2*u*u+u)*dt*m0+(-2*u**3+3*u*u)*b[j]+(u**3-u*u)*dt*m1;});
}
export const HERO_KEYS=[[0,230,590],[4.5,230,590],[5,260,555],[5.8,450,710],[7.4,850,1430],[8.5,1030,1230],[10.5,1180,800],[12,1280,720],[13.7,1530,910],[15.2,1780,1070],[17,1950,840],[18.6,2070,690],[20,2050,680],[21,1840,750],[23,1370,720],[25,850,690],[27,330,580],[28,230,590],[30,230,590]];
export const TARGET_KEYS=[[0,610,1500],[6,610,1500],[7,750,1220],[9,980,960],[11,1190,790],[13,1350,820],[15,1640,1060],[17,1830,820],[19,2080,660],[21,2300,610],[24,2650,500],[30,3250,480]];
export const heroAt=t=>spline(HERO_KEYS,t);
export const targetAt=t=>spline(TARGET_KEYS,t);
export function heroState(t){const p=heroAt(t),a=heroAt(Math.max(0,t-.035)),b=heroAt(Math.min(DURATION,t+.035)),vx=(b[0]-a[0])/.07,vy=(b[1]-a[1])/.07,flight=ramp(t,4.8,5.45)*(1-ramp(t,27.2,28.2));return {x:p[0],y:p[1],vx,vy,flight,face:Math.cos(Math.PI*ramp(t,20,20.9))*(1-ramp(t,28.3,28.9))+ramp(t,28.3,28.9),grab:ramp(t,11.7,12.25)*(1-ramp(t,12.9,13.4))+.85*ramp(t,14.7,15.2)*(1-ramp(t,15.7,16.2))};}
export const OBSTACLES=[{id:'elm-branch',x:1450,y:935,r:92},{id:'willow-branch',x:2040,y:770,r:82}];
export function mulberry(a){return()=>{let t=a+=0x6D2B79F5;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296;};}
