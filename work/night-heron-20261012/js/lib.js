// 通用小工具（引擎原库 core/lib.js 在本拷贝中缺失，这里自备等价物）
export const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
export const lerp=(a,b,u)=>a+(b-a)*u;
export const ss=(a,b,x)=>{const t=clamp((x-a)/(b-a));return t*t*(3-2*t)};
export const ease=u=>{u=clamp(u);return u*u*(3-2*u)};
export const eio=x=>{x=clamp(x);return x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2};
export const eo=x=>1-Math.pow(1-clamp(x),3);
export const ei=x=>clamp(x)**3;
export const back=x=>{x=clamp(x);const c=1.70158,c3=c+1;return 1+c3*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
export const seg=(t,a,b)=>clamp((t-a)/(b-a));
// 种子随机（确定性）
export const rng=seed=>{let s=seed>>>0;return()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296}};
const h2=(x,y)=>{const n=Math.sin(x*127.1+y*311.7)*43758.5453;return n-Math.floor(n)};
// 值噪声（可平铺）
export function vnoise(x,y,period=64){
  const i=Math.floor(x),j=Math.floor(y),fx=x-i,fy=y-j,u=fx*fx*(3-2*fx),v=fy*fy*(3-2*fy);
  const w=(a,b)=>h2(((a%period)+period)%period,((b%period)+period)%period);
  return (w(i,j)*(1-u)+w(i+1,j)*u)*(1-v)+(w(i,j+1)*(1-u)+w(i+1,j+1)*u)*v;
}
export const hash=(...a)=>h2(a[0]*7.3+a[1]*3.1,a[2]===undefined?1.7:a[2]*5.9);
// 阻尼弹簧（预模拟用）
export function springChain(n,len,damp,stiff,rate,drive){
  const p=new Array(n).fill(0),v=new Array(n).fill(0),out=new Float32Array(drive.length);
  const dt=1/rate;
  for(let k=0;k<drive.length;k++){
    const acc=drive[k];
    for(let i=0;i<n;i++){
      const up=i===0?acc:(p[i-1]-p[i])*stiff;
      v[i]+=(up-p[i]*stiff)*dt; v[i]*=damp; p[i]+=v[i]*dt;
    }
    out[k]=p[n-1];
  }
  return out;
}
