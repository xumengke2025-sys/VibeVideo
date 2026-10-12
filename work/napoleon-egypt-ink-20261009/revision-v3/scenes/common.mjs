import * as THREE from '../vendor/three.module.js';
import {mk,draw,blot} from '../vendor/ink.js';
export {THREE};
export const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
export const smooth=x=>{x=clamp(x);return x*x*x*(x*(x*6-15)+10)};
export const progress=(t,a,b)=>smooth((t-a)/(b-a));
export const mix=(a,b,q)=>a+(b-a)*q;
export const vecmix=(a,b,q)=>a.map((v,i)=>mix(v,b[i],q));
export const noise=(i)=>{let x=Math.sin(i*127.1+311.7)*43758.5453123;return x-Math.floor(x)};
export const C={paper:'#e6e1d7',ink:'#30312d',mid:'#777870',pale:'#bcbdb2',blue:'#696f70',red:'#756960'};
export function texture(mode='wash',seed=1){
 const c=document.createElement('canvas');c.width=c.height=512;const g=c.getContext('2d');
 g.fillStyle=mode==='sail'?'#d4d1c6':mode==='wood'?'#72746a':'#aaa99d';g.fillRect(0,0,512,512);
 for(let i=0;i<2000;i++){const x=noise(i+seed)*512,y=noise(i+seed+1000)*512;g.fillStyle=`rgba(28,32,28,${.006+noise(i+700)*.055})`;g.beginPath();g.ellipse(x,y,1+noise(i+11)*26,1+noise(i+400)*10,noise(i+32)*3,0,Math.PI*2);g.fill()}
 if(mode==='wood')for(let i=0;i<35;i++){g.strokeStyle=`rgba(28,29,25,${.06+noise(i)*.14})`;g.lineWidth=.6+noise(i+45)*1.4;g.beginPath();g.moveTo(0,i*15);g.bezierCurveTo(150,i*15+5,330,i*15-5,512,i*15);g.stroke()}
 if(mode==='sail')for(let x=30;x<512;x+=60){g.strokeStyle='#93968a50';g.lineWidth=1;g.beginPath();g.moveTo(x,0);g.lineTo(x+5,512);g.stroke()}
 const wet=document.createElement('canvas'),dry=document.createElement('canvas');wet.width=dry.width=512;wet.height=dry.height=512;const wg=wet.getContext('2d'),dg=dry.getContext('2d');
 for(let i=0;i<40;i++){const x=noise(i+seed)*512,y=noise(i+seed+500)*512;const s=mk([[x-70,y-4,.4],[x,y,1],[x+90,y+5,.2]],{w:mode==='wood'?3:14+noise(i+77)*20,tone:.12,dry:.4,wet:.5,seed:seed*100+i,nb:9});draw({wet:wg,dry:dg},s,1,.38)}
 g.save();g.globalAlpha=.25;g.filter='blur(1.3px)';g.drawImage(wet,0,0);g.filter='none';g.globalAlpha=.5;g.drawImage(dry,0,0);g.restore();
 const tx=new THREE.CanvasTexture(c);tx.colorSpace=THREE.SRGBColorSpace;return tx;
}
export function material(color=C.mid,map=null){return new THREE.MeshBasicMaterial({color,map,side:THREE.DoubleSide})}
export function box(w,h,d,color=C.mid,map=null){return new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material(color,map))}
export function line(points,color=C.ink,opacity=1){const geo=new THREE.BufferGeometry().setFromPoints(points.map(p=>new THREE.Vector3(...p)));return new THREE.Line(geo,new THREE.LineBasicMaterial({color,transparent:opacity<1,opacity}))}
export function rod(a,b,r=.025,color=C.ink){const va=new THREE.Vector3(...a),vb=new THREE.Vector3(...b),m=new THREE.Mesh(new THREE.CylinderGeometry(r*.85,r,va.distanceTo(vb),7),material(color));m.position.copy(va.clone().add(vb).multiplyScalar(.5));m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),vb.sub(va).normalize());return m}
export function aimRod(mesh,a,b){const va=new THREE.Vector3(...a),vb=new THREE.Vector3(...b),delta=vb.clone().sub(va);mesh.position.copy(va.add(vb).multiplyScalar(.5));mesh.scale.y=delta.length()/mesh.geometry.parameters.height;mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),delta.normalize());}
export function ground(scene,type='desert',seed=2){
 const g=new THREE.PlaneGeometry(120,160,36,50),p=g.attributes.position;
 for(let i=0;i<p.count;i++){const x=p.getX(i),y=p.getY(i);p.setZ(i,type==='sea'?0:.04*Math.sin(x*.6)*Math.cos(y*.5));}
 g.rotateX(-Math.PI/2);const m=new THREE.Mesh(g,material(type==='sea'?'#c2c5ba':'#d1cbbd',texture('wash',seed)));m.position.z=42;m.position.y=-.08;scene.add(m);
 for(let i=0;i<90;i++){const x=(noise(i+seed)-.5)*46,z=noise(i+seed+100)*80;const pts=[];for(let j=0;j<12;j++)pts.push([x+j*.23,.007,z+.05*Math.sin(j*.9+i)]);scene.add(line(pts,type==='sea'?'#7f8c8650':'#77796e',.1+noise(i+300)*.2))}
 scene.fog=new THREE.Fog(C.paper,20,75);return m;
}
export function rock(scene,x,z,s=1){const m=new THREE.Mesh(new THREE.DodecahedronGeometry(s,0),material('#88897c',texture('wash',Math.floor(x*10+z))));m.scale.y=.55;m.position.set(x,.12,z);scene.add(m);return m}
export function backdrop(scene,kind='desert'){
 if(kind==='desert'){
  for(let i=0;i<3;i++){const m=new THREE.Mesh(new THREE.ConeGeometry(7-i,7-i,4),material('#aaa99c',texture('wash',20+i)));m.rotation.y=Math.PI/4;m.position.set(-8+i*11,3-i*.5,51+i*7);scene.add(m)}
  for(let i=0;i<15;i++)rock(scene,(noise(i+20)-.5)*28,noise(i+50)*28+10,.1+noise(i)*.28);
 }
}
export function camera(scene,pos,target,fov=42){const c=new THREE.PerspectiveCamera(fov,9/16,.05,180);c.position.fromArray(pos);c.lookAt(new THREE.Vector3(...target));c.updateMatrixWorld(true);return c}
export function pose(c,pos,target,fov=c.fov){c.position.fromArray(pos);c.lookAt(new THREE.Vector3(...target));c.fov=fov;c.updateProjectionMatrix();c.updateMatrixWorld(true)}
export function billboard(mesh,c){mesh.rotation.y=Math.atan2(c.position.x-mesh.position.x,c.position.z-mesh.position.z)}
export function flag(){const grp=new THREE.Group(),pole=rod([0,0,0],[0,3.7,0],.025);grp.add(pole);const g=new THREE.PlaneGeometry(1.05,.67,20,8),a=g.attributes.position,base=a.array.slice();g.translate(.525,3.26,0);const can=document.createElement('canvas');can.width=300;can.height=180;const ctx=can.getContext('2d');['#727d80','#d0cdc1','#7c7069'].forEach((c,i)=>{ctx.fillStyle=c;ctx.fillRect(i*100,0,100,180)});const t=new THREE.CanvasTexture(can),m=new THREE.Mesh(g,material('#c8c7bb',t));grp.add(m);return {group:grp,update(t){for(let i=0;i<a.count;i++){const x=base[i*3]+.525;a.setZ(i,.12*x*Math.sin(t*2.1-x*3+base[i*3+1]*4));}a.needsUpdate=true;}}}
export function puffTexture(){const c=document.createElement('canvas');c.width=c.height=128;const g=c.getContext('2d'),r=g.createRadialGradient(64,64,5,64,64,62);r.addColorStop(0,'rgba(71,73,66,.65)');r.addColorStop(.45,'rgba(84,87,78,.22)');r.addColorStop(1,'rgba(90,91,84,0)');g.fillStyle=r;g.fillRect(0,0,128,128);return new THREE.CanvasTexture(c)}
export function puff(tx=puffTexture()){const m=new THREE.Sprite(new THREE.SpriteMaterial({map:tx,transparent:true,depthWrite:false}));return m}
