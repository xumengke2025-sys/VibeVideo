const fs=require('node:fs'),path=require('node:path');
function inspect(dir){const src=fs.readFileSync(path.join(dir,'scene.js'),'utf8');const start=src.indexOf('const clamp='),end=src.indexOf('function place(');const {at,poses}=new Function(src.slice(start,end)+';return {at:cameraAt,poses};')();
 const d=(t,dt=.001)=>at(t+dt).P.map((v,j)=>(v-at(t-dt).P[j])/(2*dt)),norm=v=>Math.hypot(...v);
 const samples=poses.slice(1,-1).map((k,i)=>{const a=poses[i],b=poses[i+2],isTransit=norm(k.P.map((v,j)=>v-a.P[j]))>.2&&norm(b.P.map((v,j)=>v-k.P[j]))>.2;return {time:k.t,transit:isTransit,speed:norm(d(k.t)),velocityJump:norm(d(k.t+.002).map((v,j)=>v-d(k.t-.002)[j]))};});
 return {source:'cameraAt from actual scene.js (offline numeric diagnostics, not visual judgement)',movingNodes:samples.filter(x=>x.transit),stopsAtTransitNodes:samples.filter(x=>x.transit&&x.speed<.01).length,maxVelocityJumpAtKnots:Math.max(...samples.map(x=>x.velocityJump))};}
const report={v2:inspect(path.join(__dirname,'..','v2')),v3:inspect(__dirname)};
fs.writeFileSync(path.join(__dirname,'qa','camera-continuity.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify({v2Stops:report.v2.stopsAtTransitNodes,v3Stops:report.v3.stopsAtTransitNodes,v2VelocityJump:report.v2.maxVelocityJumpAtKnots,v3VelocityJump:report.v3.maxVelocityJumpAtKnots}));
