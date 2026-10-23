import{COUNT,DURATION,FPS,rng,ramp,clamp,transitions}from'./math.js';
export const DT=1/60,SEED=17961804;
function limit(x,y,n){const d=Math.hypot(x,y);return d>n?[x*n/d,y*n/d]:[x,y]}
function target(id,t){
 const [a,b]=transitions.find(([a,b])=>t>=a&&t<b)||[0,0],u=b?clamp((t-a)/(b-a)):0,phi=id/COUNT*Math.PI*2;
 if(!b)return[540+Math.cos(phi)*320,850+Math.sin(phi)*280];
 if(u<.32){const r=210+id%9*18;return[400+u*680+Math.cos(phi+u*4)*r,820+Math.sin(phi+u*4)*r*.9];}
 if(a<20){const p=id/COUNT*Math.PI;return[540+Math.cos(p)*430,940-Math.sin(p)*380+(id%3)*9];}
 if(a<40){const p=id/COUNT;return[990-p*870,1470-p*640+(id%5)*10];}
 const p=id/COUNT*Math.PI*2;return[420+Math.cos(p)*105,890+Math.sin(p)*65-(id%5)*8];
}
export function simulate({social=true}={}){
 const R=rng(SEED),b=Array.from({length:COUNT},(_,id)=>({id,x:320+R()*450,y:600+R()*420,vx:0,vy:0})),frames=[];let interactions=0;
 for(let k=0;k<=DURATION/DT;k++){
  const t=k*DT;
  if(k%5===0)frames.push(b.map(o=>[+o.x.toFixed(3),+o.y.toFixed(3),+o.vx.toFixed(3),+o.vy.toFixed(3)]));
  const cells=new Map();for(const o of b){const key=Math.floor(o.x/130)+','+Math.floor(o.y/130);if(!cells.has(key))cells.set(key,[]);cells.get(key).push(o);}
  const next=[];for(const o of b){
   const [tx,ty]=target(o.id,t),dx=tx-o.x,dy=ty-o.y;let ax=dx*2.7-o.vx*2.8,ay=dy*2.7-o.vy*2.8,n=0,mx=0,my=0,mvx=0,mvy=0,sx=0,sy=0;
   if(social){const cx=Math.floor(o.x/130),cy=Math.floor(o.y/130);for(let ix=-1;ix<=1;ix++)for(let iy=-1;iy<=1;iy++)for(const v of cells.get((cx+ix)+','+(cy+iy))||[]){if(v.id===o.id)continue;const ux=o.x-v.x,uy=o.y-v.y,d=Math.hypot(ux,uy);if(d<130){n++;mx+=v.x;my+=v.y;mvx+=v.vx;mvy+=v.vy;interactions++;if(d<28&&d>.01){sx+=ux/d*(28-d)*24;sy+=uy/d*(28-d)*24;}}}
    ax+=sx;ay+=sy;if(n){ax+=(mvx/n-o.vx)*.7+(mx/n-o.x)*.12;ay+=(mvy/n-o.vy)*.7+(my/n-o.y)*.12;}}
   const tr=transitions.find(([a,b])=>t>=a&&t<b);if(tr&&t<tr[0]+1.8){const s=ramp(t,tr[0],tr[0]+.5)*(1-ramp(t,tr[0]+1.15,tr[0]+1.8));ax+=(850-o.y)*s*1.6;ay+=(o.x-540)*s*1.6;}
   [ax,ay]=limit(ax,ay,1400);const[vx,vy]=limit(o.vx+ax*DT,o.vy+ay*DT,610);next.push({...o,x:o.x+vx*DT,y:o.y+vy*DT,vx,vy});
  }b.splice(0,b.length,...next);
 }
 return{fps:12,dt:DT,seed:SEED,count:COUNT,duration:DURATION,social,interactions,frames};
}
export function sample(cache,t){const p=clamp(t,0,DURATION)*cache.fps,i=Math.min(cache.frames.length-1,Math.floor(p)),j=Math.min(cache.frames.length-1,i+1),u=p-i;return cache.frames[i].map((a,k)=>a.map((v,c)=>v+(cache.frames[j][k][c]-v)*u));}
