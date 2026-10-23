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
  const image=images[id],c=document.createElement('canvas');c.width=image.width;c.height=image.height;const p=c.getContext('2d');p.drawImage(image,0,0);p.globalCompositeOperation='source-in';
  const color=id.includes('horse')?'#293b3f':id.includes('british')?'#6c3a36':id==='eagle'?'#ab8850':id==='musket'?'#695a43':id==='cannon'||id==='wheel'?'#283b3c':'#263849';
  p.fillStyle=color;p.fillRect(0,0,c.width,c.height);
  let box=[0,0,c.width,c.height];if(id==='musket'){const d=p.getImageData(0,0,c.width,c.height).data;let l=c.width,r=0,b=0,top=c.height;for(let y=0;y<c.height;y++)for(let q=0;q<c.width;q++)if(d[(y*c.width+q)*4+3]>96){l=Math.min(l,q);r=Math.max(r,q);top=Math.min(top,y);b=Math.max(b,y)}box=[l,top,r-l+1,b-top+1]}
  const m=sheet({w,h,ax,ay,ppm:Math.min(650,1800/Math.max(w,h)),U,trans:.08,finish:{grainA:.65,rim:.34,under:.40,rimPx:2},draw:x=>{x.save();x.scale(1,-1);x.drawImage(c,...box,-w/2,-h/2,w,h);x.restore()}});
  m.material.side=THREE.DoubleSide;m.material.alphaToCoverage=false;m.position.set(0,0,0);cache.set(key,m);
 }
 const source=cache.get(key),m=source.clone();m.customDepthMaterial=source.customDepthMaterial;m.position.z=depth;return m;
}
export function slab(w,h,draw,options={}){
 const m=sheet({w,h,ppm:w>20?75:240,U,trans:.16,draw,finish:{grainA:.65,rim:.30,under:.38},...options});m.material.side=THREE.DoubleSide;m.material.alphaToCoverage=false;return m;
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
 const weapon=slab(.19,1.95,x=>{x.fillStyle='#a8956a';x.fillRect(-.025,-.65,.05,1.40);x.fillStyle='#c4b68d';x.beginPath();x.moveTo(-.025,.72);x.lineTo(0,.97);x.lineTo(.025,.72);x.closePath();x.fill();x.fillStyle='#77644a';x.beginPath();x.moveTo(-.025,-.45);x.lineTo(.055,-.67);x.lineTo(.09,-.90);x.lineTo(-.045,-.9);x.lineTo(-.05,-.54);x.closePath();x.fill()},{shadow:false,ax:0,ay:-.3,trans:.05});weapon.position.set(.30,1.04,.08);g.add(weapon);
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
 weapon.rotation.z=state==='aim'?Math.PI/2:(retreat?-.3:.02*Math.sin(p));
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
 const flag=slab(2.9,1.95,x=>{for(let i=0;i<3;i++){x.fillStyle=['#29465a','#c6b58c','#773a35'][i];x.fillRect(-1.45+i*2.9/3,-.975,2.9/3,1.95)}},{trans:.22});flag.position.set(.02,5.49,.065);
 const geo=new THREE.PlaneGeometry(2.9,1.95,30,20);geo.translate(1.45,-.94,0);flag.geometry=geo;const base=geo.attributes.position.array.slice();g.add(flag);
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
export function regiment(kind,count=30,phase=0,slope=0){
 const w=count*.48,h=1.55+Math.abs(slope*w);
 const m=slab(w,h,x=>{
  x.fillStyle=kind==='british'?'#674641':kind==='prussian'?'#3c4648':'#3a4a50';
  for(let k=0;k<count;k++){
   const px=-w/2+.25+k*.48+(seed(k+phase*10)-.5)*.06,py=-.60+px*slope+(seed(k+42)-.5)*.09,s=.85+seed(k+31)*.13;
   x.save();x.translate(px,py);x.scale(s,s);x.beginPath();x.moveTo(-.10,0);x.lineTo(-.12,.47);x.lineTo(-.17,.57);x.lineTo(-.13,.77);x.lineTo(-.1,.90);x.lineTo(-.12,1.13);x.lineTo(.11,1.13);x.lineTo(.13,.88);x.lineTo(.11,.77);x.lineTo(.19,.62);x.lineTo(.13,.45);x.lineTo(.15,0);x.lineTo(.07,0);x.lineTo(.01,.36);x.lineTo(-.02,0);x.closePath();x.fill();
   x.fillRect(.22,.23,.035,1.05);x.beginPath();x.moveTo(.22,1.27);x.lineTo(.238,1.44);x.lineTo(.255,1.27);x.fill();x.restore();
  }
 },{trans:.19,shadow:true});m.userData={phase};return m;
}
export function smokeTexture(){
 const c=document.createElement('canvas');c.width=c.height=256;const x=c.getContext('2d');
 const R=n=>seed(n+701);for(let k=0;k<38;k++){
  const px=55+R(k*3)*146,py=65+R(k*3+1)*128,r=20+R(k*3+2)*48;
  const gr=x.createRadialGradient(px,py,0,px,py,r);gr.addColorStop(0,'rgba(192,183,158,.1)');gr.addColorStop(.5,'rgba(151,154,147,.05)');gr.addColorStop(1,'rgba(151,154,147,0)');x.fillStyle=gr;x.fillRect(px-r,py-r,2*r,2*r);
 }return tex(c);
}
