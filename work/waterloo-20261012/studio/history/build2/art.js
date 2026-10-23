import * as THREE from 'three';
import {sheet,paperMat,tex,finish} from './vendor/paper.js';
import{seed,clamp,mix}from'./timeline.js';
export const U={uLight:{value:new THREE.Vector3(-3,4,-6)},uLightR:{value:10},uLightCol:{value:new THREE.Color('#e7c791')},uLit:{value:.6}};
const ids=['horse-body','horse-front-upper','horse-front-lower','horse-back-upper','horse-back-lower','horse-tail','rider-body','rider-arm','rider-leg','guard-body','british-body','prussian-body','leg-upper','leg-lower','guard-arm','british-arm','musket','napoleon','eagle','flag','cannon','wheel','battlefield','elevated-horse'];
export const images={};
await Promise.all(ids.map(async id=>{const im=new Image();im.src='./assets/'+id+'.png';await im.decode();images[id]=im}));
const cache=new Map(), allMaterials=[];
export function matte(mat,amount=.74){
 mat.roughness=1;mat.metalness=0;const original=mat.onBeforeCompile;
 mat.onBeforeCompile=s=>{original(s);s.fragmentShader=s.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
 {float lum=dot(diffuseColor.rgb,vec3(.2126,.7152,.0722));
 float q=(floor(lum*6.0)+.5)/6.0;
 vec3 ink=diffuseColor.rgb*mix(1.0,q/max(.06,lum),${amount.toFixed(2)});
 ink=mix(vec3(dot(ink,vec3(.2126,.7152,.0722))),ink,.76);
 float hatch=step(.79,fract((vWP.x*.69+vWP.y)*73.0));
 ink*=1.0-hatch*.085*(1.0-smoothstep(.2,.67,lum));
 diffuseColor.rgb=mix(ink,vec3(.80,.72,.59),.042);}`)};
 mat.customProgramCacheKey=()=>`engraved-paper-${amount}`;allMaterials.push(mat);return mat;
}
export function sprite(id,w,h,ax=0,ay=0,depth=0){
 const key=[id,w,h,ax,ay].join('/');
 if(!cache.has(key)){
  const image=images[id];const m=sheet({w,h,ax,ay,ppm:Math.min(500,1600/Math.max(w,h)),U,trans:.22,finish:{grainA:.13,rim:.12,under:.10},draw:x=>{x.save();x.scale(1,-1);x.drawImage(image,-w/2,-h/2,w,h);x.restore()}});
  matte(m.material);m.position.set(0,0,0);cache.set(key,m);
 }
 const m=cache.get(key).clone();m.position.z=depth;return m;
}
export function slab(w,h,draw,options={}){
 const m=sheet({w,h,ppm:w>20?65:180,U,trans:.12,draw,finish:{grainA:.4,rim:.25,under:.4},...options});matte(m.material,.45);return m;
}
export function line(points,color,width=.025,z=.02){
 const shape=new THREE.Shape();for(let i=0;i<points.length;i++){const p=points[i];if(!i)shape.moveTo(...p);else shape.lineTo(...p)}
 const positions=[];for(let i=0;i<points.length-1;i++){const [x,y]=points[i],[a,b]=points[i+1],L=Math.hypot(a-x,b-y),nx=-(b-y)/L*width/2,ny=(a-x)/L*width/2;positions.push(x+nx,y+ny,z,x-nx,y-ny,z,a+nx,b+ny,z,a+nx,b+ny,z,x-nx,y-ny,z,a-nx,b-ny,z)}
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));return new THREE.Mesh(geo,new THREE.MeshStandardMaterial({color,roughness:1,side:THREE.DoubleSide}));
}
export function infantry(kind='guard',phase=0){
 const g=new THREE.Group();const legs=[];
 for(let k=0;k<2;k++){
  const pivot=new THREE.Group();pivot.position.set(k?.08:-.08,.80,k?.03:-.04);
  const upper=sprite('leg-upper',.22,.42,0,.21);pivot.add(upper);
  const knee=new THREE.Group();knee.position.set(0,-.35,.01);knee.add(sprite('leg-lower',.26,.46,0,.23));pivot.add(knee);g.add(pivot);legs.push({pivot,knee});
 }
 const body=sprite(kind+'-body',.62,.80,0,-.40,.02);body.position.y=.73;g.add(body);
 const skirt=slab(.43,.31,x=>{x.fillStyle=kind==='british'?'#7d2523':'#202f43';x.beginPath();x.moveTo(-.18,.15);x.lineTo(.18,.15);x.lineTo(.22,-.15);x.lineTo(-.22,-.15);x.closePath();x.fill()},{shadow:false});skirt.position.set(0,.72,.03);g.add(skirt);
 const arm=new THREE.Group();arm.position.set(.13,1.08,.06);const a=sprite(kind==='british'?'british-arm':'guard-arm',.49,.35,-.17,.08);arm.add(a);g.add(arm);
 const weapon=sprite('musket',.17,1.72,0,-.30,.075);weapon.position.set(.36,1.04,.08);g.add(weapon);
 const shadow=slab(.75,.11,x=>{x.fillStyle='#131821';x.beginPath();x.ellipse(0,0,.36,.048,0,0,Math.PI*2);x.fill()},{shadow:false,finish:{grain:false,rim:0,under:0},trans:0});shadow.position.set(.1,-.025,-.08);g.add(shadow);
 g.userData={legs,body,arm,weapon,phase};return g;
}
export function poseInfantry(g,time,speed=1,state='march',amount=1){
 const {legs,phase,arm,weapon}=g.userData;const p=time*speed*7+phase;
 const retreat=state==='retreat',kneel=state==='kneel';
 for(let k=0;k<2;k++){
  const a=p+k*Math.PI;legs[k].pivot.rotation.z=Math.sin(a)*.32*amount+(kneel?(k?.7:-.8):0);
  legs[k].knee.rotation.z=Math.max(0,Math.cos(a))*.48*amount+(kneel?.9:0);
 }
 arm.rotation.z=.04*Math.sin(p-1)*amount;
 weapon.rotation.z=state==='aim'?1.3:(retreat?-.3:.02*Math.sin(p));
 g.rotation.z=kneel?.12:(retreat?-.09:0);
}
export function cavalry(phase=0){
 const g=new THREE.Group();const legs=[];
 for(let k=0;k<4;k++){
  const front=k>1;const p=new THREE.Group();p.position.set(front?.60:-.65,.89,k%2?.045:-.06);
  const upper=sprite(front?'horse-front-upper':'horse-back-upper',front?.37:.44,.64,front?-.07:-.02,.25);
  p.add(upper);const knee=new THREE.Group();knee.position.set(front?.07:.09,-.48,.01);knee.add(sprite(front?'horse-front-lower':'horse-back-lower',.31,.65,0,.27));p.add(knee);legs.push({p,knee});g.add(p);
 }
 const torso=sprite('horse-body',2.4,1.62,0,-.48,.04);torso.position.y=1.14;g.add(torso);
 const tail=sprite('horse-tail',.6,1.05,0,.47,.02);tail.position.set(-.99,1.64,.01);g.add(tail);
 const rider=new THREE.Group();rider.position.set(-.13,1.55,.075);
 rider.add(sprite('rider-leg',.44,.80,0,.23,.01));const rb=sprite('rider-body',.73,1.03,0,-.39,.015);rb.position.set(0,.23,.01);rider.add(rb);
 const arm=sprite('rider-arm',.6,.45,-.20,.10,.04);arm.position.set(.18,.61,.05);rider.add(arm);
 const reins=line([[1.04,2.00],[.58,2.03],[.28,2.36]],'#30291f',.025,.15);g.add(reins);
 g.add(rider);g.userData={legs,tail,rider,phase,torso,reins};return g;
}
export function poseCavalry(g,t,speed=1,turn=0){
 const {legs,tail,rider,phase,torso}=g.userData;const p=t*10*speed+phase;
 for(let k=0;k<4;k++){const a=p+[.3,2.6,Math.PI,5.1][k];legs[k].p.rotation.z=Math.sin(a)*.65;legs[k].knee.rotation.z=Math.max(0,Math.cos(a+.7))*.95-.09}
 tail.rotation.z=.12+Math.sin(p*.6)*.15;rider.rotation.z=Math.sin(p-.6)*.055;
 torso.rotation.z=Math.sin(p)*.018;g.rotation.z=-turn*.10;return Math.max(0,Math.sin(p*2))*.09;
}
export function standard(){
 const g=new THREE.Group();const pole=line([[0,0],[0,5.8]],'#665237',.062,.08);g.add(pole);
 const cap=sprite('eagle',1.30,1.36,0,-.67,.13);cap.position.y=5.66;g.add(cap);
 const flag=sprite('flag',2.9,2.58,-1.45,1.18,.06);flag.position.set(.02,5.49,.065);
 const geo=new THREE.PlaneGeometry(2.9,2.58,30,20);geo.translate(1.45,-1.18,0);flag.geometry=geo;const base=geo.attributes.position.array.slice();g.add(flag);
 const cord=line([[0,5.5],[.06,4.18],[.12,3.40]],'#ab8b53',.025,.10);g.add(cord);
 g.userData={flag,base,cap,pole};return g;
}
export function poseStandard(g,t,loss=0){
 const {flag,base}=g.userData;const a=flag.geometry.attributes.position;
 for(let i=0;i<a.count;i++){
  const x=base[i*3],y=base[i*3+1];const f=x/2.9;
  a.setXYZ(i,x*(1-loss*.2),y-loss*.68*f+Math.sin(t*2.3-f*4.3)*.10*f,Math.sin(t*2.3-f*4.3+y)*(.15+.17*loss)*f);
 }a.needsUpdate=true;flag.geometry.computeVertexNormals();
 g.rotation.z=-.025*Math.sin(t*1.5)-loss*.24;
}
export function cannon(){
 const g=new THREE.Group();const b=sprite('cannon',2.8,1.38,0,-.48,.02);g.add(b);
 const wheel=sprite('wheel',1.29,1.29,0,0,.085);wheel.position.set(.35,.69,.09);g.add(wheel);
 g.userData={wheel,baseX:0};return g;
}
export function regiment(kind,count=30,phase=0){
 const w=count*.28,h=1.55;
 const im=images[kind+'-body'];const arm=images[kind==='british'?'british-arm':'guard-arm'];
 const m=sheet({w,h,U,ppm:135,shadow:false,trans:.18,finish:{grainA:.18,rim:.1,under:.1},draw:x=>{
  x.save();x.scale(1,-1);
  for(let k=0;k<count;k++){
   const px=-w/2+k*.28;
   x.drawImage(images['leg-upper'],px+.10,.05,.12,.3);x.drawImage(images['leg-lower'],px+.10,.31,.14,.3);
   x.drawImage(images['leg-upper'],px+.01,.05,.12,.3);x.drawImage(images['leg-lower'],px-.01,.31,.14,.3);
   x.fillStyle=kind==='british'?'#792a27':'#223145';x.fillRect(px,-.10,.25,.28);
   x.drawImage(im,px-.035,-.75,.42,.65);x.drawImage(arm,px+.11,-.46,.25,.23);
   x.drawImage(images.musket,px+.3,-.85,.08,1.45);
  }x.restore();
 }});matte(m.material,.8);m.userData={phase};return m;
}
export function smokeTexture(){
 const c=document.createElement('canvas');c.width=c.height=256;const x=c.getContext('2d');
 const R=n=>seed(n+701);for(let k=0;k<38;k++){
  const px=55+R(k*3)*146,py=65+R(k*3+1)*128,r=20+R(k*3+2)*48;
  const gr=x.createRadialGradient(px,py,0,px,py,r);gr.addColorStop(0,'rgba(192,183,158,.1)');gr.addColorStop(.5,'rgba(151,154,147,.05)');gr.addColorStop(1,'rgba(151,154,147,0)');x.fillStyle=gr;x.fillRect(px-r,py-r,2*r,2*r);
 }return tex(c);
}
