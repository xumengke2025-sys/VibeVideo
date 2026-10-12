// Pure absolute-time contact tracks and a constrained two-bone chain.
const add=(a,b)=>a.map((v,i)=>v+b[i]),sub=(a,b)=>a.map((v,i)=>v-b[i]),mul=(a,k)=>a.map(v=>v*k),dot=(a,b)=>a.reduce((n,v,i)=>n+v*b[i],0),len=a=>Math.hypot(...a);
const unit=(a,f=[1,0,0])=>len(a)>1e-10?mul(a,1/len(a)):f;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)),smooth=x=>{x=clamp(x);return x*x*x*(10+x*(-15+6*x))},mix=(a,b,q)=>a.map((v,i)=>v+(b[i]-v)*q);
export function solveTwoBone(root,target,l1,l2,pole=[0,0,1]){
 const offset=sub(target,root),raw=len(offset),d=clamp(raw,Math.abs(l1-l2)+1e-8,l1+l2-1e-8),axis=unit(offset,[0,-1,0]);
 let bend=sub(pole,mul(axis,dot(pole,axis)));if(len(bend)<1e-8)bend=sub([1,0,0],mul(axis,axis[0]));bend=unit(bend,[0,0,1]);
 const along=(l1*l1+d*d-l2*l2)/(2*d),height=Math.sqrt(Math.max(0,l1*l1-along*along));
 const knee=add(root,add(mul(axis,along),mul(bend,height))),foot=add(root,mul(axis,d));
 return {hip:root,knee,foot,requested:target,reachError:len(sub(target,foot)),lengthErrors:[Math.abs(len(sub(knee,root))-l1),Math.abs(len(sub(foot,knee))-l2)]};
}
// Exact interpolation of the existing 36x50 triangular desert ground mesh.
export function groundY(x,z){
 const gx=clamp((x+60)/120*36,0,35.999999),gz=clamp((z+38)/160*50,0,49.999999),i=Math.floor(gx),j=Math.floor(gz),u=gx-i,v=gz-j;
 const h=(ix,iz)=>-.08+.04*Math.sin((-60+ix*120/36)*.6)*Math.cos((80-iz*160/50)*.5),a=h(i,j),b=h(i,j+1),c=h(i+1,j+1),d=h(i+1,j);
 return u+v<=1?a+(d-a)*u+(b-a)*v:c+(b-c)*(1-u)+(d-c)*(1-v);
}
export function createContactTrack(path,start,end,{stride=.58,phase=0,ground=groundY,lateral=.12}={}){
 const times=[],positions=[],distances=[];let distance=0;
 for(let k=0,n=Math.ceil((end-start)*120);k<=n;k++){const t=start+(end-start)*k/n,p=path(t);if(k)distance+=Math.hypot(p[0]-positions[k-1][0],p[2]-positions[k-1][2]);times.push(t);positions.push(p);distances.push(distance)}
 const find=(a,x)=>{let l=0,h=a.length-1;while(l<h){const m=Math.ceil((l+h)/2);if(a[m]<=x)l=m;else h=m-1}return Math.min(a.length-2,l)};
 function atTime(t){const i=find(times,clamp(t,start,end)),q=clamp((t-times[i])/(times[i+1]-times[i]));return {position:mix(positions[i],positions[i+1],q),distance:distances[i]+(distances[i+1]-distances[i])*q}}
 function atDistance(d){const i=find(distances,clamp(d,0,distance)),q=clamp((d-distances[i])/Math.max(1e-12,distances[i+1]-distances[i]));return mix(positions[i],positions[i+1],q)}
 function planted(d,side){const p=atDistance(d),a=atDistance(d-.03),b=atDistance(d+.03),dir=unit([b[0]-a[0],0,b[2]-a[2]],[0,0,1]);p[0]+=dir[2]*lateral*(side?1:-1);p[2]-=dir[0]*lateral*(side?1:-1);p[1]=ground(p[0],p[2],d);return p}
 function feetAt(t){const {distance:d}=atTime(t);return [0,1].map(side=>{const ph=phase+side*.5,cycle=d/stride+ph,k=Math.floor(cycle),p=cycle-k,previous=(k-ph+.31)*stride,next=previous+stride;let point;
  if(p<.62)point=planted(previous,side);else{const q=(p-.62)/.38;point=mix(planted(previous,side),planted(next,side),smooth(q));point[1]+=.16*Math.sin(Math.PI*q)}
  if(t>=end){const rest=planted(distance,side);point=mix(point,rest,smooth((t-end)/.3))}return {point,stance:t>=end?t>=end+.3:p<.62,cycle:k,phase:p};})}
 function touchdownTimes(){const result=[];for(let side=0;side<2;side++){const ph=phase+side*.5;for(let k=Math.ceil(ph);(k-ph)*stride<distance;k++){const d=(k-ph)*stride,i=find(distances,d),q=clamp((d-distances[i])/Math.max(1e-12,distances[i+1]-distances[i]));result.push({at:times[i]+(times[i+1]-times[i])*q,side})}}return result.sort((a,b)=>a.at-b.at)}
 return {feetAt,atTime,touchdownTimes,start,end,stride,totalDistance:distance};
}
