import {THREE,C,ground,backdrop,camera,pose,vecmix,progress,mix,noise,rock,flag,rod,aimRod,puff,puffTexture,box,texture} from './common.mjs';
import {makeActor,makeHorse} from '../actors/rig.mjs';
import {createContactTrack,groundY} from '../actors/contacts.mjs';
export function createLand(lib,plan){
 const scene=new THREE.Scene();ground(scene);backdrop(scene);const cam=camera(scene,[-7,5,-18],[0,.4,2],44);
 const soldiers=[],size=8.8,n=13;
 // Two ranks, individual IDs shared by marching, formation, resistance and result.
 for(let rank=0;rank<2;rank++)for(let side=0;side<4;side++)for(let j=0;j<n;j++){
  const index=soldiers.length,u=(j+.5)/n,half=size/2+rank*.45;
  const dest=side===0?[-half+u*2*half,0,2-half]:side===1?[half,0,2-half+u*2*half]:side===2?[half-u*2*half,0,2+half]:[-half,0,2+half-u*2*half];
  const actor=makeActor(lib,'infantry-station-'+[2,1,0,1][side],1.68+noise(index)*.13);scene.add(actor.group);
  const gun=rod([.15,1.08,0],[.8,1.25,0],.014,'#404139');actor.group.add(gun);const bayonet=rod([.8,1.25,0],[1.1,1.35,0],.008,'#a3a99b');actor.group.add(bayonet);
   const start=[(index%8-3.5)*.48,0,Math.floor(index/8)*.52-4],path=t=>{const march=marchAt(Math.min(t,14)),p=vecmix(start.map((v,k)=>v+march[k]),dest,progress(t,14.7,17.3));p[1]=groundY(p[0],p[2]);return p;};
   soldiers.push({actor,id:'soldier-'+index,side,dest,start,gun,bayonet,path,track:createContactTrack(path,9,17.3,{stride:plan.gait.stride,phase:index*.17,lateral:.09})});
 }
 const standard=flag();standard.group.position.set(-1,0,2);scene.add(standard.group);
 for(let i=0;i<3;i++){const b=box(.7,.48,.5,'#9b9789',texture('wood',21+i));b.position.set(i*.8-1,.25,1.5);scene.add(b)}
 const napoleon=makeActor(lib,'napoleon-1',1.83);scene.add(napoleon.group);napoleon.group.position.set(-5,0,-3);
 const lead=makeActor(lib,'infantry-lead',1.84);scene.add(lead.group);
 const horses=[];for(let i=0;i<12;i++){const h=makeHorse(lib,i%3,2.1+noise(i+80)*.2);scene.add(h.group);horses.push(h)}
 const tx=puffTexture(),smoke=[];for(let i=0;i<18;i++){const p=puff(tx);scene.add(p);smoke.push(p)}
 const event=(id,def)=>plan.events.find(e=>e.id===id)?.at??def,shotTime=event('land-volley',20.6);
 function marchAt(t){return [mix(0,1,progress(t,9,12.8)),0,mix(-2,5,progress(t,9,12.8))]}
 function update(t){
  const formation=progress(t,14.7,17.3),march=marchAt(t);
  soldiers.forEach((s,i)=>{const start=t<14?[s.start[0]+march[0],0,s.start[2]+march[2]]:s.start.map((v,k)=>v+marchAt(14)[k]);const dest=s.dest;
   s.actor.group.position.fromArray(vecmix(start,dest,formation));s.actor.update(t,cam,{speed:t<12.8?plan.gait.marchSpeed:t<17.3&&t>14.7?.7:0,phase:i*.17});s.gun.visible=t>=14;s.bayonet.visible=t>=14;
   const r=progress(t,16,17.2);s.gun.rotation.z=-.32*r;s.bayonet.rotation.z=-.32*r;
  });
  horses.forEach((h,i)=>{const approach=progress(t,17.4+i*.035,20.8),retreat=progress(t,21.15+i*.03,23.5);const z=mix(21+i*.2,8+i*.15,approach)+retreat*(15+i*.3),x=mix(8+i*.7,4+i*.22,approach)+Math.sin(retreat*Math.PI)*2+retreat*5;
   h.group.position.set(x,groundY(x,z),z);h.update(t,cam,retreat?2.1:2.5,retreat>.12);h.group.visible=t>=17&&t<24;});
  smoke.forEach((p,i)=>{const age=t-shotTime-i*.012;p.visible=age>=0&&age<1.7;if(p.visible){p.position.set(4.8+(i%4)*.2,.95+age*.6,-1+i*.4+age*.6);p.scale.setScalar(.2+age*1.1);p.material.opacity=Math.max(0,.62-age*.35)}});
  napoleon.group.visible=t>=24;napoleon.update(t,cam,{speed:0});standard.update(t);standard.group.visible=t>=14;
  if(t<14){const s=marchAt(t);pose(cam,[s[0]-5,.95,s[2]-12],[s[0],.82,s[2]+2.6],40)}
  else if(t<19){const q=progress(t,14,18);pose(cam,vecmix([-7,2.4,-14],[-10,10,-21],q),vecmix([-1,1,0],[.7,.3,3],q),44)}
  else if(t<24)pose(cam,[-11,8,-21],[2,.55,4],44);
  else {const q=progress(t,24,26.7);pose(cam,vecmix([-8.7,2,-12.6],[-8,2.2,-12],q),vecmix([-5,1.05,-3],[-1.7,2.2,1.5],progress(t,25.6,26.6)),36)}
  // World contacts and mesh bones are evaluated afresh after the current camera pose.
  const recoil=t>=shotTime&&t<shotTime+.42?.07*Math.sin(Math.PI*progress(t,shotTime,shotTime+.42)):0;
  soldiers.forEach((s,i)=>{s.actor.group.position.fromArray(s.path(t));s.actor.update(t,cam,{contactTrack:s.track,phase:i*.17});s.actor.mesh.material.map=lib['infantry-station-'+([2,1,0,1][s.side]+(cam.position.y>4?3:0))].tx;s.actor.group.updateMatrixWorld(true);const normal=[[0,0,-1],[1,0,0],[0,0,1],[-1,0,0]][s.side],root=s.actor.group.position;
   const muzzle=s.actor.group.worldToLocal(new THREE.Vector3(root.x+normal[0]*(1.15-recoil),root.y+1.23,root.z+normal[2]*(1.15-recoil))),tip=s.actor.group.worldToLocal(new THREE.Vector3(root.x+normal[0]*(1.42-recoil),root.y+1.23,root.z+normal[2]*(1.42-recoil)));aimRod(s.gun,[.15-recoil,1.08,0],muzzle.toArray());aimRod(s.bayonet,muzzle.toArray(),tip.toArray());
  });
  lead.group.visible=t<14;soldiers[0].actor.group.visible=t>=14;lead.group.position.copy(soldiers[0].actor.group.position);lead.update(t,cam,{contactTrack:soldiers[0].track});
  horses.forEach((h,i)=>h.update(t,cam,plan.gait.horseRate/1.6,progress(t,21.15+i*.03,23.5)>.12));napoleon.update(t,cam,{speed:0,lean:.15*Math.sin(progress(t,24.6,26.6)*Math.PI)});standard.group.rotation.z=-.06*Math.sin(progress(t,24.6,26.8)*Math.PI);
 }
 return {scene,camera:cam,update,snapshot(t){update(t);return {ids:soldiers.map(s=>s.id),positions:soldiers.map(s=>s.actor.group.position.toArray()),contacts:soldiers.map(s=>s.actor.rigState),leadContact:lead.rigState,horses:horses.filter(h=>h.group.visible).map(h=>h.rigState),footEvents:soldiers[0].track.touchdownTimes().filter(e=>e.at<12.8),camera:cam.position.toArray(),target:t<19?[.7,.3,3]:[2,.55,4],formation:progress(t,14.7,17.3),volley:shotTime}}};
}
