import fs from 'node:fs';
import {general,hospital,alpine,coronation} from './rig-v2.js';
import {sceneAt} from './math.js';
// Exercise every exported-frame pose without rasterization. Test reach and floor
// contact rather than visual quality, which needs actual rendered images.
const context=()=>new Proxy({canvas:{width:1080,height:1920},globalAlpha:1,getTransform:()=>({})},{get:(o,k)=>k in o?o[k]:(()=>{})});
globalThis.document={createElement:()=>({width:0,height:0,getContext:()=>context()})};
const g=context(),imgs={},stats={frames:0,maxBoneError:0,maxTargetError:0,maxContactError:0,maxFloorError:0,failures:[]};
const d=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
for(let i=0;i<1536;i++){
 const t=i/24,s=sceneAt(t),r=s==='arcole'?general(g,imgs,t):s==='jaffa'?hospital(g,imgs,t):s==='alps'?alpine(g,imgs,t):coronation(g,imgs,t);
 const bones=[...(r.arms||[]),...(r.legs||[])];
 for(const b of bones){stats.maxBoneError=Math.max(stats.maxBoneError,b.boneError);stats.maxTargetError=Math.max(stats.maxTargetError,b.error);if(!Number.isFinite(b.error)||b.error>.1)stats.failures.push({t,scene:s,error:b.error});}
 if(r.contactError!=null)stats.maxContactError=Math.max(stats.maxContactError,r.contactError);
 if(s==='arcole'||s==='jaffa')for(let n=0;n<2;n++)stats.maxFloorError=Math.max(stats.maxFloorError,d(r.legs[n].sole,(s==='arcole'?[[343,1540],[648,1540]]:[[295,1540],[571,1540]])[n]));
 if(s==='alps')for(const b of r.legs)stats.maxFloorError=Math.max(stats.maxFloorError,d(b.sole,b.targetSole));
 stats.frames++;
}
fs.mkdirSync('out/motion-v2-verification',{recursive:true});fs.writeFileSync('out/motion-v2-verification/constraints.json',JSON.stringify(stats,null,2));console.log(JSON.stringify(stats));
if(stats.failures.length||stats.maxFloorError>.1||stats.maxContactError>.1)process.exit(1);
