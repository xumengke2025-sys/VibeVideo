import {THREE,C,clamp,progress,mix,vecmix,noise,ground,camera,pose,material,texture,rod,line,box,rock} from './common.mjs';
import {makeActor} from '../actors/rig.mjs';
import {follow3D} from '../camera/subject-camera.mjs';
import {createContactTrack,groundY} from '../actors/contacts.mjs';
export function createStudy(lib,plan){
 const scene=new THREE.Scene();ground(scene,'desert',24);scene.fog=new THREE.Fog(C.paper,15,55);const stone=texture('wash',88);
 // Doorway consists of separated solids: the moving camera sees through an actual opening.
 for(let x of [-1.8,1.8]){const col=box(.72,4.6,.95,'#9e9a88',stone);col.position.set(x,2.25,-.3);scene.add(col);const cap=box(.95,.45,1.15,'#a5a18d',stone);cap.position.set(x,4.5,-.3);scene.add(cap);for(let j=0;j<8;j++)scene.add(line([[x-.36,j*.56,-.8],[x+.36,j*.56,-.8]],'#656b5c',.3))}
 const lintel=box(4.5,.65,1.2,'#aaa48f',stone);lintel.position.set(0,4.7,-.3);scene.add(lintel);
 for(let i=0;i<8;i++){const x=(i%4-1.5)*3.2,z=11+Math.floor(i/4)*4;const col=new THREE.Mesh(new THREE.CylinderGeometry(.56,.63,5.6,12),material('#aaa591',stone));col.position.set(x,2.8,z);scene.add(col);const cap=box(1.5,.55,1.5,'#aaa28e',stone);cap.position.set(x,5.7,z);scene.add(cap);for(let j=0;j<12;j++){const y=.5+j*.38;scene.add(line([[x-.5,y,z-.5],[x+.4,y,z-.5]],'#767869',.18))}}
 for(let z of [11,15]){const beam=box(12,1,1.4,'#b0aa95',stone);beam.position.set(0,6.25,z);scene.add(beam)}
 for(let i=0;i<20;i++)rock(scene,(noise(i+12)-.5)*16,noise(i+45)*15+6,.12+noise(i+3)*.2);
 const scholar=makeActor(lib,'scholar-0',1.76),assistant=makeActor(lib,'scholar-1',1.72);scene.add(scholar.group,assistant.group);assistant.group.position.set(1.7,0,3.6);
 const instrument=new THREE.Group();instrument.position.set(.6,0,3.7);scene.add(instrument);for(let a of [0,2*Math.PI/3,4*Math.PI/3])instrument.add(rod([0,1.12,0],[Math.cos(a)*.4,0,Math.sin(a)*.4],.025,'#707264'));
 const head=new THREE.Group();head.position.y=1.15;instrument.add(head);head.add(rod([-.27,.08,0],[.27,.08,0],.045,'#666d62'));const dial=new THREE.Mesh(new THREE.CylinderGeometry(.12,.12,.055,24),material('#999c86'));head.add(dial);
 const cam=camera(scene,[-3,1.55,-4],[-.5,.9,2],40);const subject=t=>{const p=[mix(-.9,-.05,progress(t,38.5,40.8)),0,mix(.1,3.45,progress(t,38.5,40.8))];p[1]=groundY(p[0],p[2]);return p;};const contactTrack=createContactTrack(subject,38.5,40.8,{stride:plan.gait.stride});
 const follow=follow3D({subject,range:[38,43],offset:[-1.7,1.65,-4.8],lookOffset:[.2,.9,.6],space:'world',fov:40,response:.1});
 const adjustAt=plan.events.find(e=>e.id==='survey-adjust').at;
 function update(t){scholar.group.position.fromArray(subject(t));const p=follow(t),handoff=progress(t,40.5,41.4);pose(cam,vecmix(p.position,[-3.3,1.85,-1.7],handoff),vecmix(p.target,[.6,1.35,5],handoff),40);scholar.update(t,cam,{contactTrack});assistant.update(t,cam,{speed:0});head.rotation.y=.32*progress(t,adjustAt-.45,adjustAt+.4);head.rotation.z=.08*Math.sin((t-adjustAt)*7)*Math.exp(-Math.abs(t-adjustAt)*4)}
 return {scene,camera:cam,update,snapshot(t){update(t);return {camera:cam.position.toArray(),subject:subject(t),contacts:scholar.rigState,footEvents:contactTrack.touchdownTimes(),instrument:instrument.position.toArray(),headRotation:head.rotation.toArray().slice(0,3),apertureWidth:2.88}}};
}
// Close contact is drawn in a local 2.5D work-surface space. The stone and paper never morph into one another.
export function createRecord(lib,plan){
 const canvas=document.createElement('canvas');canvas.width=1080;canvas.height=1920;const g=canvas.getContext('2d');
 const face=lib['stone-face'].im,brush=lib['brush-hand'].im,pen=lib['pen-hand'].im;
 const marks=[];for(let band=0;band<3;band++)for(let row=0;row<(band===0?4:band===1?5:7);row++)for(let col=0;col<14;col++){
  const x=col*19+20,y=band*90+row*10+20;marks.push([[x,y],[x+3+noise(col+row)*6,y-2],[x+8,y+2]])}
 const brushAt=plan.events.find(e=>e.id==='stone-brush').at,penAt=plan.events.find(e=>e.id==='record-contact').at;
 let state={};
 function drawHand(im,tip,size,alpha=1,angle=0){g.save();g.globalAlpha=alpha;g.translate(...tip);g.rotate(angle);g.filter='saturate(0.03)';g.drawImage(im,-size*.04,-size*(im.height/im.width)*.985,size,size*im.height/im.width);g.restore()}
 function update(t){g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;g.fillStyle=C.paper;g.fillRect(0,0,1080,1920);const pullback=progress(t,47.6,48.5),zoom=mix(1.12,.95,pullback);g.translate(540,1000);g.scale(zoom,zoom);g.translate(-540,-1000);
  // Rubble and tabletop stay in the scene's local coordinates.
  for(let i=0;i<32;i++){const x=noise(i+31)*1080,y=850+noise(i+41)*730;g.fillStyle=`rgba(104,108,94,${.07+noise(i)*.15})`;g.beginPath();g.moveTo(x,y);g.lineTo(x+18+noise(i+11)*46,y+8);g.lineTo(x+25,y+29+noise(i+8)*25);g.closePath();g.fill()}
  const sx=110,sy=650,sw=540,sh=sw*face.height/face.width;g.filter='saturate(0.02)';g.drawImage(face,sx,sy,sw,sh);g.filter='none';
  const reveal=progress(t,44,46),dustFront=mix(sy+60,sy+sh-35,reveal);g.save();g.beginPath();g.rect(sx,Math.max(sy,dustFront),sw,sy+sh-Math.max(sy,dustFront));g.clip();g.fillStyle='#9a998c98';g.fillRect(sx,sy,sw,sh);for(let i=0;i<2200;i++){g.fillStyle='#b9b5a74a';g.fillRect(sx+noise(i)*sw,sy+noise(i+78)*sh,1+noise(i+5)*3,1+noise(i+88)*2)}g.restore();
  const paper={x:620,y:1040,w:350,h:465};g.save();g.translate(paper.x,paper.y);const curl=(t<48.1?.018*Math.sin((t-47.3)*6)*Math.exp(-Math.abs(t-47.3)*2):0);g.transform(1,curl,0,1,0,0);g.fillStyle='#d6d0c0';g.fillRect(6,8,paper.w,paper.h);g.fillStyle='#ebe6d9';g.fillRect(0,0,paper.w,paper.h);g.strokeStyle='#9a9a8850';g.lineWidth=1;g.strokeRect(0,0,paper.w,paper.h);
  const writing=clamp((t-46.3)/1.7),index=Math.floor(writing*marks.length);g.strokeStyle='#666d5c';g.lineWidth=1.2;for(let i=0;i<index;i++){const m=marks[i];g.beginPath();m.forEach(([x,y],j)=>j?g.lineTo(x,y):g.moveTo(x,y));g.stroke()}g.strokeStyle='#717561';g.lineWidth=1.5;g.beginPath();g.moveTo(13,13);g.lineTo(295,13);g.lineTo(310,320);g.lineTo(13,320);g.closePath();if(writing>.06)g.stroke();g.restore();
  const brushTip=[sx+sw*.46+.11*sw*Math.sin(reveal*5*Math.PI),dustFront];if(t>=43.9&&t<46.05)drawHand(brush,brushTip,610,Math.min(1,(t-43.9)*5)*Math.min(1,(46.05-t)*6),-.08);
  const current=marks[Math.min(marks.length-1,index)]?.[0]??[20,20],penTip=[paper.x+current[0],paper.y+current[1]];if(t>=46.3&&t<48.4)drawHand(pen,[penTip[0],penTip[1]-progress(t,48,48.4)*70],410,Math.min(1,(t-46.3)*6)*Math.min(1,(48.4-t)*6),.08);
  state={stone:{x:sx,y:sy,w:sw,h:sh,thickness:.14},paper,brushTip,penTip,reveal,recorded:index,marks:marks.length,cameraZoom:zoom,brushContact:t>=44&&t<=46,penContact:t>=46.3&&t<=48};
 }
 return {canvas,update,snapshot(t){update(t);return state}};
}
