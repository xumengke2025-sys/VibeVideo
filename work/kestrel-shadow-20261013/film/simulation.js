import{COUNT,DURATION,clamp,targetAt,heroAt,OBSTACLES,mulberry,ramp}from'./math.js';
// Fixed-step local-neighbour Boids. Animation rendering never mutates this simulation.
export const DT=1/120,SEED=13719;
export function simulate({threat=true}={}){
 const rng=mulberry(SEED),birds=Array.from({length:COUNT},(_,id)=>({id,x:240+(id%5)*153+rng()*18,y:1430+Math.floor(id/5)*74+rng()*14,vx:0,vy:0,phase:rng()*Math.PI*2,size:.94+rng()*.14,launch:6.05+id%5*.075+Math.floor(id/5)*.085,flight:0}));
 const frames=[],steps=Math.round(DURATION/DT);let minDistance=Infinity,avoidanceUpdates=0,fleeUpdates=0;
 const limited=(x,y,limit)=>{const s=Math.hypot(x,y);return s>limit?[x*limit/s,y*limit/s]:[x,y]};
 for(let step=0;step<=steps;step++){
  const t=step*DT,h=heroAt(t),next=[];
  if(step%5===0)frames.push(birds.map(b=>[+b.x.toFixed(4),+b.y.toFixed(4),+b.vx.toFixed(4),+b.vy.toFixed(4),+b.flight.toFixed(4)]));
  for(const b of birds){
   if(t<b.launch){next.push({...b,vx:0,vy:0,flight:0});continue;}
   const flight=ramp(t,b.launch,b.launch+.8),target=targetAt(t+.55),emergency=t>11.4&&t<16.2;
   let tx=target[0],ty=target[1]+(b.id%2?1:-1)*(emergency?95:26),dx=tx-b.x,dy=ty-b.y,dd=Math.max(1,Math.hypot(dx,dy)),speed=175+80*ramp(t,6.2,8)+25*ramp(t,11,12);
   let ax=(dx/dd*speed-b.vx)*1.45,ay=(dy/dd*speed-b.vy)*1.45;
   let sx=0,sy=0,mx=0,my=0,mvx=0,mvy=0,n=0;
   for(const o of birds){if(o.id===b.id||t<o.launch)continue;const ux=b.x-o.x,uy=b.y-o.y,d=Math.hypot(ux,uy);minDistance=Math.min(minDistance,d);
    if(d<260){mx+=o.x;my+=o.y;mvx+=o.vx;mvy+=o.vy;n++;if(d<145&&d>.001){const g=900*(1-d/145);sx+=ux/d*g;sy+=uy/d*g;}}
   }
   // Separation is highest priority; alignment/cohesion use only neighbours.
   ax+=sx*2.1;ay+=sy*2.1;
   if(n){ax+=(mvx/n-b.vx)*.95+(mx/n-b.x)*.24;ay+=(mvy/n-b.vy)*.95+(my/n-b.y)*.24;}
   if(threat&&t>5&&t<21){const ux=b.x-h[0],uy=b.y-h[1],d=Math.max(1,Math.hypot(ux,uy));if(d<455){const f=780*(1-d/455)**2;ax+=ux/d*f;ay+=uy/d*f;fleeUpdates++;}}
   for(const o of OBSTACLES){const px=b.x+b.vx*.33,py=b.y+b.vy*.33,ux=px-o.x,uy=py-o.y,d=Math.max(1,Math.hypot(ux,uy)),r=o.r+92;if(d<r){const f=1000*(1-d/r);ax+=ux/d*f;ay+=uy/d*f;avoidanceUpdates++;}}
   ay+=Math.sin(t*1.7+b.phase)*12;
   [ax,ay]=limited(ax,ay,430);let[vx,vy]=limited(b.vx+ax*DT,b.vy+ay*DT,speed+40);if(t<b.launch+.8){vy-=30*DT;}
   next.push({...b,x:b.x+vx*DT,y:b.y+vy*DT,vx,vy,flight});
  }
  birds.splice(0,birds.length,...next);
 }
 return {duration:DURATION,fps:24,count:COUNT,seed:SEED,dt:DT,meta:birds.map(({id,phase,size,launch})=>({id,phase,size,launch})),obstacles:OBSTACLES,metrics:{minDistance,avoidanceUpdates,fleeUpdates},frames};
}
export function sampleCache(cache,t){const p=clamp(t,0,DURATION)*cache.fps,a=Math.min(cache.frames.length-1,Math.floor(p)),b=Math.min(cache.frames.length-1,a+1),u=p-a;return cache.frames[a].map((v,i)=>v.map((x,k)=>x+(cache.frames[b][i][k]-x)*u));}
