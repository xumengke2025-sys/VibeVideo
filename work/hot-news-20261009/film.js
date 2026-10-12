import * as T from 'three';
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';
import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';
import {UnrealBloomPass} from 'three/addons/postprocessing/UnrealBloomPass.js';
import {OutputPass} from 'three/addons/postprocessing/OutputPass.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
const W=1080,H=1920,canvas=document.querySelector('#film'),g=canvas.getContext('2d');
const clamp=x=>Math.max(0,Math.min(1,x)),smooth=x=>{x=clamp(x);return x*x*(3-2*x)},mix=(a,b,p)=>a+(b-a)*p;
let seed=9913;const rand=()=>{seed=(1664525*seed+1013904223)>>>0;return seed/4294967296};
const photo=new Image();photo.src='assets/antarctica.jpg';await photo.decode();
const gl=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true,alpha:false});gl.setSize(W,H);gl.setPixelRatio(1);gl.toneMapping=T.ACESFilmicToneMapping;gl.toneMappingExposure=1.1;
const scene=new T.Scene();scene.background=new T.Color('#010914');scene.fog=new T.FogExp2('#011324',.012);
const pmrem=new T.PMREMGenerator(gl);scene.environment=pmrem.fromScene(new RoomEnvironment(),.04).texture;
const camera=new T.PerspectiveCamera(43,W/H,.05,160);
scene.add(new T.HemisphereLight('#7dd8ff','#01081a',2.7));
const key=new T.DirectionalLight('#b9efff',5);key.position.set(-4,5,4);scene.add(key);
const warm=new T.PointLight('#ffd395',20,25,2);warm.position.set(2,1,3);scene.add(warm);
const composer=new EffectComposer(gl);composer.addPass(new RenderPass(scene,camera));const bloom=new UnrealBloomPass(new T.Vector2(W,H),.8,.6,.7);composer.addPass(bloom);composer.addPass(new OutputPass());
// Optical module: schematic glass pressure housing, equatorial band and a downward-facing PMT bowl.
const hero=new T.Group();scene.add(hero);
const glass=new T.MeshPhysicalMaterial({color:'#91b4c6',metalness:.15,roughness:.12,transparent:true,opacity:.12,side:T.FrontSide,clearcoat:1});
hero.add(new T.Mesh(new T.SphereGeometry(1,64,48),glass));
const rimMat=new T.MeshStandardMaterial({color:'#4e6066',metalness:.85,roughness:.23});
const band=new T.Mesh(new T.TorusGeometry(1.004,.045,12,96),rimMat);band.rotation.x=Math.PI/2;hero.add(band);
const bowl=new T.Mesh(new T.SphereGeometry(.79,48,32,0,Math.PI*2,Math.PI/2,Math.PI/2),new T.MeshStandardMaterial({color:'#b09661',metalness:.9,roughness:.19,side:T.DoubleSide}));hero.add(bowl);
const inner=new T.Mesh(new T.SphereGeometry(.63,48,32,0,Math.PI*2,Math.PI/2,Math.PI/2),new T.MeshStandardMaterial({color:'#111920',metalness:.8,roughness:.21,side:T.DoubleSide}));inner.position.y=.11;hero.add(inner);
const pcb=new T.Mesh(new T.CylinderGeometry(.69,.69,.08,48),new T.MeshStandardMaterial({color:'#193b38',metalness:.3,roughness:.5}));pcb.position.y=.22;hero.add(pcb);
for(let i=0;i<14;i++){const a=i/14*Math.PI*2;const b=new T.Mesh(new T.BoxGeometry(.1,.08,.14),rimMat);b.position.set(Math.cos(a)*.87,.025,Math.sin(a)*.87);b.rotation.y=-a;hero.add(b);}
const cable=new T.Mesh(new T.CylinderGeometry(.026,.026,60,10),rimMat);scene.add(cable);
// 86 strings × 60 modules = 5,160; positions and spacings are a stylized schematic.
const locations=[];for(let a=-6;a<=6;a++)for(let b=-6;b<=6;b++){let x=a*1.5+b*.75,z=b*1.299;locations.push({x,z,d:x*x+z*z});}locations.sort((a,b)=>a.d-b.d);locations.length=86;
const positions=[],colors=[],sizes=[],trunks=[];
for(const l of locations){trunks.push(l.x,-12,l.z,l.x,12,l.z);for(let j=0;j<60;j++){positions.push(l.x,(j-30)*.4,l.z);colors.push(.13,.37,.55);sizes.push(1);}}
const geom=new T.BufferGeometry();geom.setAttribute('position',new T.Float32BufferAttribute(positions,3));geom.setAttribute('color',new T.Float32BufferAttribute(colors,3));geom.setAttribute('power',new T.Float32BufferAttribute(sizes,1));
const nodeMat=new T.ShaderMaterial({transparent:true,depthWrite:false,blending:T.AdditiveBlending,vertexColors:true,uniforms:{uScale:{value:1150}},vertexShader:`attribute float power;uniform float uScale;varying vec3 vCol;void main(){vCol=color;vec4 mv=modelViewMatrix*vec4(position,1.);gl_Position=projectionMatrix*mv;gl_PointSize=clamp(uScale*(.12+.06*power)/(-mv.z),3.,42.);}`,fragmentShader:`varying vec3 vCol;void main(){float r=length(gl_PointCoord-.5)*2.;if(r>1.)discard;float a=exp(-r*r*5.);gl_FragColor=vec4(vCol*(1.+2.2*exp(-r*r*20.)),a);}`});
const array=new T.Group();scene.add(array);array.add(new T.Points(geom,nodeMat));
const trunkGeom=new T.BufferGeometry();trunkGeom.setAttribute('position',new T.Float32BufferAttribute(trunks,3));const stringMat=new T.LineBasicMaterial({color:'#4296b1',transparent:true,opacity:.09});array.add(new T.LineSegments(trunkGeom,stringMat));
// Light path is an illustrative secondary charged-particle track, not light emitted by a neutrino itself.
const beamMat=new T.MeshBasicMaterial({color:'#7fe9ff',transparent:true,opacity:.9});const beam=new T.Mesh(new T.CylinderGeometry(.025,.025,1,12),beamMat);scene.add(beam);
const beamStart=new T.Vector3(-1,3,0),beamEnd=new T.Vector3(2,-9,0),dir=beamEnd.clone().sub(beamStart).normalize();beam.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),dir);
const flash=new T.PointLight('#6adfff',0,30,1.2);flash.position.copy(beamStart);scene.add(flash);
const cone=new T.Mesh(new T.ConeGeometry(5,10,80,1,true),new T.ShaderMaterial({transparent:true,depthWrite:false,side:T.DoubleSide,blending:T.AdditiveBlending,uniforms:{alpha:{value:0}},vertexShader:`varying vec3 n;varying vec3 v;void main(){vec4 p=modelViewMatrix*vec4(position,1.);n=normalize(normalMatrix*normal);v=normalize(-p.xyz);gl_Position=projectionMatrix*p;}`,fragmentShader:`uniform float alpha;varying vec3 n;varying vec3 v;void main(){float f=pow(1.-abs(dot(normalize(n),normalize(v))),2.);gl_FragColor=vec4(vec3(.08,.65,1.)*(.2+f),alpha*(.035+.2*f));}`}));cone.position.copy(beamStart).addScaledVector(dir,5);cone.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),dir.clone().negate());scene.add(cone);
const particlePos=[],particleMeta=[];for(let i=0;i<1100;i++){const along=rand(),angle=rand()*Math.PI*2,r=rand();particleMeta.push({along,angle,r});particlePos.push(0,0,0);}
const pg=new T.BufferGeometry();pg.setAttribute('position',new T.Float32BufferAttribute(particlePos,3));
const pmat=new T.PointsMaterial({color:'#80d6ff',size:.045,transparent:true,opacity:.75,depthWrite:false,blending:T.AdditiveBlending});const photons=new T.Points(pg,pmat);scene.add(photons);
const dustPos=[];for(let i=0;i<2000;i++)dustPos.push((rand()-.5)*65,(rand()-.5)*80,(rand()-.5)*65);
const dg=new T.BufferGeometry();dg.setAttribute('position',new T.Float32BufferAttribute(dustPos,3));const dust=new T.Points(dg,new T.PointsMaterial({color:'#88ccdf',size:.025,transparent:true,opacity:.3,depthWrite:false}));scene.add(dust);
function txt(s,x,y,size=44,color='#edf6ff',align='left',family='"Microsoft YaHei"'){g.font=`${size}px ${family}`;g.textAlign=align;g.fillStyle=color;g.fillText(s,x,y);}
function tracked(s,x,y,size=28,spacing=6,color='#9dc7d5'){g.font=`${size}px Bahnschrift`;g.fillStyle=color;for(const c of s){g.fillText(c,x,y);x+=g.measureText(c).width+spacing;}}
function overlay(t){
 const edge=g.createLinearGradient(0,0,0,H);edge.addColorStop(0,'rgba(1,7,14,.9)');edge.addColorStop(.24,'rgba(1,7,14,.4)');edge.addColorStop(.36,'rgba(1,7,14,0)');edge.addColorStop(.66,'rgba(1,7,14,0)');edge.addColorStop(1,'rgba(1,7,14,.9)');g.fillStyle=edge;g.fillRect(0,0,W,H);
 if(t<2.6){tracked('SOUTH POLE  /  ICECUBE',80,185);txt('冰下，',74,350,114);txt('宇宙亮了。',74,490,114);txt('2026 诺贝尔物理学奖',80,1620,44,'#e9d5ad');txt('真实南极历史影像',80,1680,26,'#9eb7c9');txt('Photo: Keith Vanderlinde / NSF',80,1810,24,'#7d9bab');}
 else if(t<6.1){tracked('BELOW THE ICE',80,185);txt('看见几乎',80,320,78);txt('看不见的粒子。',80,420,78);txt('中微子相互作用产生的光',80,1580,43);txt('由冰下光学模块捕捉',80,1650,43);}
 else if(t<11.2){tracked('A TRACE OF THE UNIVERSE',80,185);txt('一次微弱闪光，',80,325,76);txt('留下宇宙的痕迹。',80,425,76);txt('5,160',80,1550,92,'#e9d5ad','left','Bahnschrift');txt('个光学模块 · 捕捉冰中的光',80,1620,37,'#b1d5e2');}
 else {tracked('NOBEL PRIZE IN PHYSICS 2026',80,185,25,4);txt('把一立方公里的冰，',80,325,68);txt('变成宇宙的眼睛。',80,425,76);txt('弗朗西斯·哈尔岑',80,1535,58,'#ecd5ac');txt('Francis Halzen',80,1595,34,'#a4bcc8','left','Bahnschrift');txt('2026.10.06  获奖公布',80,1685,29,'#bdcbd0');}
 if(t>=2.6){txt('探测过程艺术化示意 · 非真实事件重建',80,1795,25,'#7899ab');txt('来源：NobelPrize.org / IceCube',80,1840,24,'#7899ab');}
}
function renderAt(t,type='image/png',quality=.96){
 if(!Number.isFinite(t)||t<0||t>15)throw Error('Invalid time');
 const pull=smooth((t-5.6)/5.6),h=smooth((t-5.6)/2.2);hero.scale.setScalar(mix(1,.055,h));hero.rotation.y=.2+.3*smooth((t-2.6)/3);hero.position.set(0,0,0);
 array.visible=t>=5.6;array.scale.setScalar(1);cable.visible=t>=2.6;cable.material.transparent=true;cable.material.opacity=mix(.9,.18,h);
 camera.position.set(mix(2.25,22,pull),mix(1,10,pull),mix(5.4,35,pull));camera.lookAt(0,-.3,0);warm.intensity=mix(20,1,h);
 bloom.strength=t<6.1?.35:.38;
 const travel=clamp((t-6.9)/1.4);beam.visible=t>=6.9;beam.scale.set(1,12.369*travel,1);beam.position.copy(beamStart).addScaledVector(dir,12.369*travel/2);beamMat.opacity=t<10.5?.9:mix(.9,.25,smooth((t-10.5)/1));
 flash.intensity=t>=6.9?25*Math.exp(-Math.max(0,t-7.1)*1.4):0;
 cone.visible=t>=6.9;cone.scale.setScalar(smooth((t-6.9)/1.6));cone.material.uniforms.alpha.value=1-smooth((t-9.3)/2);
 photons.visible=t>=6.9;const pp=pg.attributes.position.array;for(let i=0;i<particleMeta.length;i++){const m=particleMeta[i],u=Math.min(travel,m.along),age=Math.max(0,t-6.9-m.along*1.4),r=age*2.3*m.r;pp[i*3]=-1+3*u+Math.cos(m.angle)*r;pp[i*3+1]=3-12*u+.3*r;pp[i*3+2]=Math.sin(m.angle)*r;}pg.attributes.position.needsUpdate=true;pmat.opacity=clamp(1-(t-9.2)/4.5)*.65;
 const col=geom.attributes.color.array,power=geom.attributes.power.array;for(let i=0;i<positions.length/3;i++){const x=positions[i*3],y=positions[i*3+1],z=positions[i*3+2],u=clamp((3-y)/12),bx=-1+3*u,dist=Math.sqrt((x-bx)**2+z*z),arrival=6.9+u*1.4+dist/5;const lit=t>=arrival&&t>6.9?Math.exp(-(t-arrival)*.28)*Math.exp(-dist/7):0;col[i*3]=.08+lit*1.1;col[i*3+1]=.32+lit*.8;col[i*3+2]=.65+lit*.7;power[i]=lit*2;}geom.attributes.color.needsUpdate=true;geom.attributes.power.needsUpdate=true;
 dust.rotation.y=t*.006;composer.render();g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;g.drawImage(gl.domElement,0,0);
 if(t<2.85){g.save();g.globalAlpha=1-smooth((t-2.45)/.4);const z=1.03+t*.018,scale=Math.max(W/photo.width,H/photo.height)*z;g.drawImage(photo,(W-photo.width*scale)/2,(H-photo.height*scale)/2,photo.width*scale,photo.height*scale);g.restore();}
 overlay(t);return canvas.toDataURL(type,quality);
}
await document.fonts.ready;window.__film={duration:15,fps:30,width:W,height:H,cuts:[2.6,6.1,11.2]};window.renderAt=renderAt;window.ready=true;renderAt(0);
if(!location.search.includes('render')){const start=performance.now();function play(now){renderAt(((now-start)/1000)%15);requestAnimationFrame(play)}requestAnimationFrame(play);}

