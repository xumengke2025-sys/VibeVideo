import {THREE,clamp,mix,noise,billboard,rod} from '../scenes/common.mjs';
import {solveTwoBone} from './contacts.mjs';
export async function loadActors(registry){const lib={};await Promise.all(registry.map(async r=>{const im=new Image();im.src=r.path;await im.decode();const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.filter='saturate(0.06)';g.drawImage(im,0,0);const tx=new THREE.CanvasTexture(c);tx.colorSpace=THREE.SRGBColorSpace;lib[r.id]={tx,im,record:r}}));return lib}
// Absolute gait phase: stance travels back under the moving hip; swing clears the ground.
export function footAt(t,speed,phase=0,stride=.58){const rate=Math.abs(speed)/stride;const p=((t*rate+phase)%1+1)%1;if(p<.62)return {x:stride*(.5-p/.62),y:0,stance:true};const q=(p-.62)/.38;return {x:stride*(-.5+q),y:.18*Math.sin(q*Math.PI),stance:false}}
export function makeActor(lib,id,height=1.75){
 const asset=lib[id];if(!asset)throw Error('Missing actor '+id);const width=height*asset.im.width/asset.im.height;
 const normalized=asset.record.rig_legs||(id==='infantry-lead'?[[[.48,.59],[.32,.77],[.25,1]],[[.60,.59],[.70,.75],[.88,.955]]]:id==='napoleon-2'?[[[.46,.48],[.37,.70],[.37,1]],[[.63,.46],[.78,.51],[.80,.725]]]:[[[.40,.44],[.34,.72],[.32,1]],[[.60,.44],[.66,.72],[.68,1]]]);
 const rest=normalized.map(chain=>chain.map(([u,v])=>[(u-.5)*width,(1-v)*height,0]));
 const xs=[...new Set([...Array.from({length:13},(_,i)=>-width/2+i*width/12),...rest.flat().map(p=>p[0])])].sort((a,b)=>a-b),ys=[...new Set([...Array.from({length:31},(_,i)=>i*height/30),...rest.flat().map(p=>p[1])])].sort((a,b)=>a-b),pos=[],uv=[],ix=[];
 ys.forEach((y,j)=>xs.forEach((x,i)=>{pos.push(x,y,0);uv.push(x/width+.5,y/height);if(i<xs.length-1&&j<ys.length-1){const a=j*xs.length+i;ix.push(a,a+1,a+xs.length,a+1,a+xs.length+1,a+xs.length)}}));
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));geo.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));geo.setIndex(ix);geo.computeVertexNormals();
 const base=geo.attributes.position.array.slice(),mesh=new THREE.Mesh(geo,new THREE.MeshBasicMaterial({map:asset.tx,transparent:true,alphaTest:.035,depthWrite:true,side:THREE.DoubleSide}));
 const group=new THREE.Group();group.add(mesh);const p=geo.attributes.position;
 function binding(x,y){let best=null;for(let side=0;side<2;side++)for(let bone=0;bone<2;bone++){const a=rest[side][bone],b=rest[side][bone+1],dx=b[0]-a[0],dy=b[1]-a[1],q=clamp(((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)),d=(x-a[0]-q*dx)**2+(y-a[1]-q*dy)**2;if(!best||d<best.d)best={side,bone,q,d,fade:clamp((rest[side][0][1]+height*.025-y)/(height*.025))};}return best;}
 const bindings=Array.from({length:p.count},(_,i)=>binding(base[i*3],base[i*3+1])),footIndices=rest.map(r=>{let best=0,d=Infinity;for(let i=0;i<p.count;i++){const e=(base[i*3]-r[2][0])**2+(base[i*3+1]-r[2][1])**2;if(e<d){d=e;best=i}}return best;});
 const actor={id,group,mesh,height,width,rigState:null,update(t,c,{speed=0,phase=0,lean=0,pose='walk',reach=null,stride=.58,contactTrack=null,footTargets=null}={}){
  billboard(group,c);const f=[footAt(t,speed,phase,stride),footAt(t,speed,phase+.5,stride)];
  group.updateMatrixWorld(true);const contacts=footTargets||contactTrack?.feetAt(t),chains=contacts?.map((contact,i)=>{const target=group.worldToLocal(new THREE.Vector3(...contact.point)).toArray(),r=rest[i],l1=Math.max(height*.31,new THREE.Vector3(...r[0]).distanceTo(new THREE.Vector3(...r[1]))*1.12),l2=Math.max(height*.31,new THREE.Vector3(...r[1]).distanceTo(new THREE.Vector3(...r[2]))*1.12);return solveTwoBone(r[0],target,l1,l2,[0,0,.8]);});
  const deltas=chains?.map((s,side)=>[s.hip,s.knee,s.foot].map((v,bone)=>v.map((n,k)=>n-rest[side][bone][k])));
  function skin(x,y,binding){const {side,bone,q,fade}=binding,a=deltas[side][bone],b=deltas[side][bone+1];return [x+(a[0]+q*(b[0]-a[0]))*fade,y+(a[1]+q*(b[1]-a[1]))*fade,(a[2]+q*(b[2]-a[2]))*fade];}
  for(let i=0;i<p.count;i++){
   const x=base[i*3],y=base[i*3+1],q=y/height,side=x<0?0:1;
   const leg=clamp((.56-q)/.56),knee=Math.sin(leg*Math.PI),foot=f[side];
   const dx=speed?foot.x*leg+Math.abs(foot.y)*knee*.4:0,dy=speed?foot.y*leg:0;
   const hem=(q>.27&&q<.62)?Math.sin(t*4.6+x*6+phase)*.015*(Math.abs(speed)>.01?1:.2):0;
   if(chains){const v=skin(x,y,bindings[i]);p.setXYZ(i,v[0]+lean*clamp(q-.56)*.08+hem*clamp(q-.56),v[1],v[2]+Math.sin(t*2+x*3+phase)*.006*clamp(q-.56));}
   else p.setXYZ(i,x+dx+lean*q*.08+hem,y+dy,Math.sin(t*2+x*3+phase)*.006*clamp(q-.35));
  }
  if(reach){group.updateMatrixWorld(true);const target=group.worldToLocal(new THREE.Vector3(...reach));const rest=new THREE.Vector3(width*.45,height*.7,0),delta=target.sub(rest);
   for(let i=0;i<p.count;i++){const x=base[i*3],y=base[i*3+1],weight=clamp((x-width*.06)/(width*.32))*clamp(1-Math.abs(y-height*.7)/(height*.18));p.setXYZ(i,p.getX(i)+delta.x*weight,p.getY(i)+delta.y*weight,p.getZ(i)+delta.z*weight)}
  }p.needsUpdate=true;mesh.rotation.z=chains?0:lean*.035;
  actor.rigState=chains?{feet:chains.map((s,i)=>({world:group.localToWorld(new THREE.Vector3(...s.foot)).toArray(),meshWorld:group.localToWorld(new THREE.Vector3(p.getX(footIndices[i]),p.getY(footIndices[i]),p.getZ(footIndices[i]))).toArray(),target:contacts[i].point,stance:contacts[i].stance,cycle:contacts[i].cycle,reachError:s.reachError,lengthErrors:s.lengthErrors})),maxReachError:Math.max(...chains.map(s=>s.reachError)),meshContactError:Math.max(...chains.map((s,i)=>new THREE.Vector3(p.getX(footIndices[i]),p.getY(footIndices[i]),p.getZ(footIndices[i])).distanceTo(new THREE.Vector3(...s.foot))))}:null;
 }};return actor;
}
export {makeHorse} from './horse.mjs';
