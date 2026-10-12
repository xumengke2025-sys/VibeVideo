import {THREE,C,clamp,progress,mix,vecmix,noise,ground,camera,pose,material,texture,rod,line,box,rock} from './common.mjs';
import {makeActor} from '../actors/rig.mjs';
import {makeShip} from './sea.mjs';
import {follow3D} from '../camera/subject-camera.mjs';
import {createContactTrack,groundY} from '../actors/contacts.mjs';
export function makeTender(id='landing-boat',gait={oarOrigin:52.5,oarPeriod:1.1}){
 const group=new THREE.Group(),wood=texture('wood',71),v=[],uv=[],ix=[],N=20;
 for(let level=0;level<3;level++)for(let i=0;i<=N;i++)for(let side of [-1,1]){const z=-1.9+i*3.8/N,w=.1+.6*Math.sin(i/N*Math.PI);v.push(w*side*[.35,.8,1][level],[-.16,.18,.52][level]+.05*(z*z),z);uv.push(i/N,level/2)}
 for(let j=0;j<2;j++)for(let i=0;i<N;i++)for(let s=0;s<2;s++){const a=(j*(N+1)+i)*2+s,b=a+2,c=a+(N+1)*2,d=c+2;ix.push(a,b,c,b,d,c)}
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(v,3));geo.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));geo.setIndex(ix);group.add(new THREE.Mesh(geo,material('#a29d8d',wood)));
 const floor=box(.65,.06,2.9,'#aaa494',wood);floor.position.y=.16;group.add(floor);
 for(let z of [-1,0,1]){const seat=box(1,.08,.28,'#979282',wood);seat.position.set(0,.38,z);group.add(seat)}
 for(let s of [-1,1]){const pts=[];for(let i=0;i<=N;i++){const z=-1.9+i*3.8/N;pts.push([s*(.1+.6*Math.sin(i/N*Math.PI)),.55+.05*z*z,z])}group.add(line(pts,'#51564a'))}
 const oars=[];for(let s of [-1,1]){const o=new THREE.Group();o.position.set(s*.55,.53,.4);o.add(rod([0,0,0],[s*1.65,0,.25],.018,'#747464'));const blade=box(.4,.025,.15,'#777562',wood);blade.position.set(s*1.6,0,.25);o.add(blade);group.add(o);oars.push({group:o,side:s})}
 return {id,group,oars,update(t,row=0){group.rotation.z=Math.sin(t*1.1)*.015;for(const o of oars){o.group.rotation.y=row?o.side*(.35*Math.cos((t-gait.oarOrigin)*2*Math.PI/gait.oarPeriod)):.9*o.side;o.group.rotation.z=row?.12*o.side*Math.sin((t-gait.oarOrigin)*2*Math.PI/gait.oarPeriod):.1*o.side;}}};
}
export function createShore(lib,plan){
 const scene=new THREE.Scene();ground(scene,'desert',44);scene.fog=new THREE.Fog(C.paper,15,54);
 const water=new THREE.Mesh(new THREE.PlaneGeometry(80,80,20,20),material('#b9c0b5',texture('wash',55)));water.rotation.x=-Math.PI/2;water.position.set(0,.02,-39.4);scene.add(water);
 const rockA=rock(scene,-2,1.25,.8);rock(scene,2.8,5,.45);rock(scene,-3.2,7,.3);
 const boat=makeTender('landing-boat',plan.gait);boat.group.position.set(-.9,0,-1.45);scene.add(boat.group);
 const departing=makeTender('departure-tender',plan.gait);scene.add(departing.group);
 const land=makeActor(lib,'napoleon-0',1.83),depart=makeActor(lib,'napoleon-2',1.83);scene.add(land.group,depart.group);
 const bootGeo=new THREE.PlaneGeometry(.94*lib['boot-contact'].im.width/lib['boot-contact'].im.height,.94,10,24);bootGeo.translate(0,.47,0);const boot=new THREE.Mesh(bootGeo,new THREE.MeshBasicMaterial({map:lib['boot-contact'].tx,transparent:true,alphaTest:.03,side:THREE.DoubleSide}));scene.add(boot);
 const others=[];for(let i=0;i<3;i++){const a=makeActor(lib,'infantry-'+(i%3),1.7);scene.add(a.group);a.path=t=>{const p=[-1.1+i*.9,0,mix(-.5-i*.4,5.3+i*.6,progress(t,4.7+i*.4,8.4))];p[1]=groundY(p[0],p[2]);return p;};a.track=createContactTrack(a.path,4.7+i*.4,8.4,{stride:plan.gait.stride,phase:i*.24});others.push(a)}
 const rower=makeActor(lib,'infantry-0',1.6);departing.group.add(rower.group);rower.group.position.set(0,-.6,.4);
 const crates=[];for(let i=0;i<3;i++){const b=box(.48,.4,.42,'#96917f',texture('wood',40+i));scene.add(b);crates.push(b)}
 const far=makeShip({id:'departure-distant-vessel',scale:.55,masts:2});far.group.position.set(-8,0,-32);scene.add(far.group);
 const footprints=[];for(let i=0;i<8;i++){const p=new THREE.Mesh(new THREE.PlaneGeometry(.12,.28),new THREE.MeshBasicMaterial({color:'#71796a',transparent:true,opacity:.38,side:THREE.DoubleSide}));p.rotation.x=-Math.PI/2;p.rotation.z=i%2?.18:-.18;p.position.set((i%2?.16:-.16),.023,.35+i*.34);scene.add(p);footprints.push(p)}
 const tideGeo=new THREE.PlaneGeometry(14,3,80,3),ta=tideGeo.attributes.position,tb=ta.array.slice();tideGeo.rotateX(-Math.PI/2);const tide=new THREE.Mesh(tideGeo,new THREE.MeshBasicMaterial({color:'#b3bdaf',transparent:true,opacity:.67,side:THREE.DoubleSide}));scene.add(tide);
 const cam=camera(scene,[-2.7,1.5,-5],[0,.8,1],42);
 const subject=t=>{const p=[mix(-.4,1.4,progress(t,4,7.6)),0,mix(.35,4.5,progress(t,4,7.6))];p[1]=groundY(p[0],p[2]);return p;};
 const landTrack=createContactTrack(subject,4,7.6,{stride:plan.gait.stride});
 const approach=t=>{const p=vecmix([.8,0,1.05],[-.22,0,.05],progress(t,49,50.2));p[1]=groundY(p[0],p[2]);return p;},approachTrack=createContactTrack(approach,49,50.2,{stride:.46});
 const follow=follow3D({subject,range:[4,9],offset:[-2.7,1.5,-4.4],space:'world',lookOffset:[.3,.85,1.1],fov:42,response:.11});
 function departureBoat(t){const elapsed=Math.max(0,t-52.4),pull=.42*(elapsed-Math.sin(elapsed*2*Math.PI/plan.gait.oarPeriod)/(2*Math.PI/plan.gait.oarPeriod));return [-.85-pull*.65,0,-1.3-pull*1.8]}
 function update(t){
  const isDeparture=t>=49;land.group.visible=t>=4&&!isDeparture;boot.visible=t<4;depart.group.visible=t>=49&&t<55;boat.group.visible=!isDeparture;departing.group.visible=isDeparture;far.group.visible=isDeparture;rower.group.visible=isDeparture;
  scene.background=new THREE.Color(isDeparture?'#d0d1c5':C.paper);scene.fog.color.set(isDeparture?'#d0d1c5':C.paper);
  let pos;if(t<4){const contact=plan.events.find(e=>e.id==='boot-contact').at,q=progress(t,.7,contact);pos=[mix(-.4,0,q),mix(.2,.005,q)+.23*Math.sin(q*Math.PI),mix(-.65,.35,q)];boot.position.fromArray(pos);boot.rotation.y=Math.atan2(.65-pos[0],-1.6-pos[2]);boot.rotation.z=mix(-.15,0,q);pose(cam,[.65,.7,-2.1],[-.12,.38,.24],40);}
  else if(t<9){pos=subject(t);land.group.position.fromArray(pos);const p=follow(t);pose(cam,p.position,vecmix(p.target,[1.4,.8,7],progress(t,7.3,8.8)),42);land.update(t,cam,{contactTrack:landTrack});}
  if(isDeparture){departing.group.position.fromArray(departureBoat(t));const b=departing.group.position;const board=progress(t,50.2,51.8);depart.group.position.fromArray(t<50.2?approach(t):vecmix(approach(50.2),[b.x+.1,.42,b.z+.9],board));departing.update(t,t>=52.4?1:0);far.update(t,{anchored:false});
   if(t<52.2)pose(cam,[-3.1,1.75,-6.8],[mix(.8,-.8,board),1,-.4],42);
   else if(t<55)pose(cam,[-3.1,1.75,-6.8],vecmix([b.x,1,b.z],[0,.2,1],progress(t,54.2,55)),42);
   else {const q=progress(t,55,57.8);pose(cam,vecmix([.6,.55,-2.1],[.6,1.2,-3.2],q),vecmix([0,.05,.8],[-.4,.2,-3.5],q),42);}
   const reach=t>=50.2&&t<=52.2?[b.x+.56,.58,b.z+.75]:null;
   const feet=approachTrack.feetAt(50.51).map((f,i)=>{const q=progress(t,i?50.2:50.8,i?51:51.8),target=[b.x+(i?.24:-.06),.42,b.z+.9],point=vecmix(f.point,target,q);point[1]+=.2*Math.sin(Math.PI*q);return {point,stance:q===0||q===1};});
   depart.update(t,cam,{contactTrack:t<50.2?approachTrack:null,footTargets:t>=50.2?feet:null,reach});rower.update(t,cam,{speed:0});
  }
  others.forEach((a,i)=>{a.group.visible=t>=4&&t<9||t>=49&&t<55;if(t<9)a.group.position.fromArray(a.path(t));else{const x=-1.1+i*.9,z=3.6+i*.7;a.group.position.set(x,groundY(x,z),z);}a.update(t,cam,{contactTrack:t<9?a.track:null,speed:0,phase:i*.24})});
  crates.forEach((b,i)=>{b.position.set(-1.1+i*.6,t<9?mix(.58,.2,progress(t,5.2+i*.4,6.2+i*.4)):.2,t<9?mix(-.8,.6,progress(t,5.2+i*.4,6.2+i*.4)):2.6)});
  boat.update(t);const surge=t>=55?mix(.1,2.8,progress(t,55.8,57.8)):(.2+.23*Math.sin(t*1.4));tide.position.set(0,.024,surge-1.7);const p=tide.geometry.attributes.position;
  for(let i=0;i<p.count;i++){const x=p.getX(i);p.setY(i,.005*Math.sin(x*3+t*1.6));}p.needsUpdate=true;
  footprints.forEach((p,i)=>{p.visible=t>=2.35&&(!isDeparture||t>=55);p.material.opacity=.38*(1-progress(surge,p.position.z-.18,p.position.z+.15))});
 }
 return {scene,camera:cam,update,snapshot(t){update(t);return {camera:cam.position.toArray(),boot:boot.position.toArray(),bootGround:t>=2.35&&t<4?boot.position.y:0,landingContact:land.rigState,departureContact:depart.rigState,footEvents:landTrack.touchdownTimes(),landingPosition:land.group.position.toArray(),departurePosition:depart.group.position.toArray(),boat:departing.group.position.toArray(),footprints:footprints.map(p=>p.material.opacity),shoreRock:rockA.position.toArray(),guards:others.filter(a=>a.group.visible).length}}};
}
