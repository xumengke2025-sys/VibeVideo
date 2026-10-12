import * as THREE from 'three';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
import {follow3D,blendPose} from './subject-camera.mjs';
import {pathAt} from './mechanical.mjs';
const plan=await (await fetch('./plan.json')).json();
const event=id=>plan.events.find(e=>e.id===id);
const W=1080,H=1920,DURATION=8;
const scale=window.__previewScale||1;
const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setSize(Math.round(W*scale),Math.round(H*scale));renderer.setPixelRatio(1);
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.15;document.body.appendChild(renderer.domElement);
const scene=new THREE.Scene();scene.background=new THREE.Color('#071821');scene.fog=new THREE.Fog('#071821',25,95);
const pmrem=new THREE.PMREMGenerator(renderer);const env=new RoomEnvironment();scene.environment=pmrem.fromScene(env).texture;env.dispose();pmrem.dispose();
const camera=new THREE.PerspectiveCamera(42,W/H,.1,150);
scene.add(new THREE.HemisphereLight('#b4e7ec','#102836',2.1));
const sun=new THREE.DirectionalLight('#fff0d1',3);sun.position.set(-12,25,4);scene.add(sun);
const cold=new THREE.DirectionalLight('#4facbc',2);cold.position.set(10,8,-20);scene.add(cold);
const mat=(color,metalness=.5,roughness=.35)=>new THREE.MeshStandardMaterial({color,metalness,roughness});
const floor=new THREE.Mesh(new THREE.PlaneGeometry(160,200),mat('#102832',.35,.6));floor.rotation.x=-Math.PI/2;floor.position.z=40;floor.position.y=-1;scene.add(floor);
const track=new THREE.Mesh(new THREE.PlaneGeometry(14,170),mat('#102a32',.5,.3));track.rotation.x=-Math.PI/2;track.position.set(0,-.98,45);scene.add(track);
for(let z=-14;z<90;z+=4){
 for(const x of [-8,8]){
  const column=new THREE.Mesh(new THREE.BoxGeometry(.3,7,.45),mat('#254652',.75,.28));column.position.set(x,2.5,z);scene.add(column);
  const cap=new THREE.Mesh(new THREE.BoxGeometry(.06,5,.08),new THREE.MeshBasicMaterial({color:'#5cb4bc'}));cap.position.set(x-.17,2.5,z-.25);scene.add(cap);
 }
 const mark=new THREE.Mesh(new THREE.BoxGeometry(.7,.025,.15),mat('#62949b',.3,.4));mark.position.set(0,-.94,z);scene.add(mark);
}
for(let i=0;i<34;i++){
 const x=(i%2?1:-1)*(14+(i%5)*3),z=-8+i*3.6,height=4+(i%7)*1.1;
 const tower=new THREE.Mesh(new THREE.BoxGeometry(2,height,2),mat('#21414b',.4,.48));tower.position.set(x,height/2-1,z);scene.add(tower);
}
const drone=new THREE.Group();scene.add(drone);
const shell=new THREE.Mesh(new THREE.SphereGeometry(1,48,24),mat('#edb066',.75,.22));shell.scale.set(.46,.28,1.2);drone.add(shell);
const dark=new THREE.Mesh(new THREE.SphereGeometry(1,32,16),mat('#0c2631',.6,.18));dark.scale.set(.32,.13,.51);dark.position.set(0,.24,.22);drone.add(dark);
const wingShape=new THREE.Shape();wingShape.moveTo(.2,0);wingShape.lineTo(1.5,-.65);wingShape.lineTo(1.2,-.85);wingShape.lineTo(.2,-.35);wingShape.closePath();
const wingGeometry=new THREE.ExtrudeGeometry(wingShape,{depth:.055,bevelEnabled:true,bevelThickness:.018,bevelSize:.025,bevelSegments:2,steps:1});
for(const side of [-1,1]){const wing=new THREE.Mesh(wingGeometry,mat('#9d6e39',.8,.27));wing.rotation.x=Math.PI/2;wing.scale.x=side;drone.add(wing);}
const engine=new THREE.Mesh(new THREE.SphereGeometry(.18,24,16),new THREE.MeshBasicMaterial({color:'#8de5ed'}));engine.position.z=-1.07;drone.add(engine);
const trail=Array.from({length:16},(_,i)=>{const m=new THREE.Mesh(new THREE.SphereGeometry(.035,8,6),new THREE.MeshBasicMaterial({color:'#8bc8cf',transparent:true,opacity:.23*(1-i/16)}));scene.add(m);return m;});
const doors=[];
for(const side of [-1,1]){
 const group=new THREE.Group();scene.add(group);
 const panel=new THREE.Mesh(new THREE.BoxGeometry(6.8,7,.65),mat('#1e404b',.7,.35));panel.position.y=2.5;group.add(panel);
 const seam=new THREE.Mesh(new THREE.BoxGeometry(.065,6.1,.08),new THREE.MeshBasicMaterial({color:'#dc9867'}));seam.position.set(-side*3.35,2.4,-.37);group.add(seam);
 for(const y of [.2,2.4,4.6]){const rib=new THREE.Mesh(new THREE.BoxGeometry(5.7,.08,.09),mat('#63828a',.4,.6));rib.position.set(0,y,-.38);group.add(rib);}
 doors.push({group,side,seam});
}
const scanner=new THREE.Mesh(new THREE.RingGeometry(.08,.14,48),new THREE.MeshBasicMaterial({color:'#eeb976',transparent:true,opacity:0,side:THREE.DoubleSide}));scene.add(scanner);
const knots=[{t:0,p:[0,1.6,-3],v:[0,0,4]},{t:2.4,p:[0,1.6,7],v:[0,0,0]},{t:3.65,p:[0,1.6,7],v:[0,0,0]},{t:5.8,p:[0,1.9,19],v:[.4,.2,7]},{t:8,p:[2.4,2.8,33],v:[1,.4,5]}];
const subject=t=>pathAt(t,knots);
const follow=follow3D({subject,range:[0,8],space:'world',offset:[3.5,2.4,-9.5],lead:.1});
const smooth=x=>{x=Math.max(0,Math.min(1,x));return x*x*x*(x*(x*6-15)+10);};
function poseAt(t){
 const a=follow(t),s=subject(t),k=smooth((t-6)/2);
 const reveal={position:[10,21,-2],target:[1,1.4,21],fov:48,roll:0};
 return blendPose(a,reveal,k);
}
function stateAt(t){return {pose:(()=>{const p=poseAt(t);return {...p,position:new THREE.Vector3(...p.position),target:new THREE.Vector3(...p.target)};})()};}
window.renderAt=(t,type='image/png',quality=.96)=>{
 t=Math.max(0,Math.min(DURATION,t));const p=poseAt(t),s=subject(t),d=subject(Math.min(8,t+.12)).map((v,i)=>v-subject(Math.max(0,t-.04))[i]),tangent=new THREE.Vector3(...d);if(tangent.length()<.001)tangent.set(0,0,1);tangent.normalize();
 drone.position.fromArray(s);drone.quaternion.setFromUnitVectors(new THREE.Vector3(0,0,1),tangent);
 drone.rotateZ(-.16*smooth((t-4.8)/.7)*(1-smooth((t-6.3)/.8)));
 const ev=event('gate-open'),open=smooth((t-ev.at)/ev.duration);
 doors.forEach(({group,side,seam})=>{group.position.set(side*(3.4+6.5*open),0,14);seam.material.color.set(t<3.05?'#dc9867':'#9edbdd');});
 const request=smooth((t-2.4)/.15)*(1-smooth((t-3.1)/.18));scanner.visible=request>.001;scanner.position.set(0,1.6,8.35);scanner.scale.setScalar(1+7*smooth((t-2.4)/.7));scanner.material.opacity=.8*request;
 trail.forEach((m,i)=>{const past=t-(i+1)*.055;m.visible=past>=0;if(m.visible)m.position.fromArray(subject(past));});
 camera.position.fromArray(p.position);camera.up.set(0,1,0);camera.lookAt(new THREE.Vector3(...p.target));camera.fov=p.fov;camera.updateProjectionMatrix();camera.updateMatrixWorld(true);
 renderer.render(scene,camera);return renderer.domElement.toDataURL(type,quality);
};
window.__film={width:Math.round(W*scale),height:Math.round(H*scale),duration:DURATION,fps:24,cuts:[],stateAt};window.subjectAt=subject;window.gateAt=t=>{const e=event('gate-open');return smooth((t-e.at)/e.duration);};window.ready=true;window.renderAt(0);
if(!location.search.includes('render')){const started=performance.now();function tick(){window.renderAt(((performance.now()-started)/1000)%DURATION);requestAnimationFrame(tick);}tick();}
