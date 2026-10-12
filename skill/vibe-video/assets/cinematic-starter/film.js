// Original code film. No generated raster or video assets. Glass uses Three transmission approximation.
import * as THREE from 'three';
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';
import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';
import {UnrealBloomPass} from 'three/addons/postprocessing/UnrealBloomPass.js';
import {OutputPass} from 'three/addons/postprocessing/OutputPass.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
import {cameraTrack,applyCamera,clamp,smooth,smoother} from './camera-kit.mjs';
const W=1280,H=720,DUR=16,FPS=30;
const canvas=document.getElementById('out');canvas.width=W;canvas.height=H;const ctx=canvas.getContext('2d');
const r=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});r.setSize(W,H);r.setPixelRatio(1);
r.toneMapping=THREE.ACESFilmicToneMapping;r.toneMappingExposure=.78;r.shadowMap.enabled=true;r.shadowMap.type=THREE.PCFSoftShadowMap;
const scene=new THREE.Scene();scene.background=new THREE.Color('#07191f');scene.fog=new THREE.FogExp2('#07191f',.018);
const pmrem=new THREE.PMREMGenerator(r);const env=pmrem.fromScene(new RoomEnvironment(),.04);scene.environment=env.texture;
const camera=new THREE.PerspectiveCamera(40,W/H,.06,160);
const composer=new EffectComposer(r);composer.addPass(new RenderPass(scene,camera));
const bloom=new UnrealBloomPass(new THREE.Vector2(W,H),.38,.45,1.05);composer.addPass(bloom);composer.addPass(new OutputPass());
const brass=new THREE.MeshStandardMaterial({color:'#b6975d',metalness:.84,roughness:.3,envMapIntensity:.7});
const dark=new THREE.MeshStandardMaterial({color:'#143238',metalness:.55,roughness:.42,envMapIntensity:.28});
const edge=new THREE.MeshStandardMaterial({color:'#3a5558',metalness:.68,roughness:.36,envMapIntensity:.3});
const glass=new THREE.MeshPhysicalMaterial({color:'#c6e9e6',metalness:0,roughness:.035,transmission:1,ior:1.46,thickness:.28,attenuationColor:new THREE.Color('#6bada3'),attenuationDistance:3,envMapIntensity:.65});
const glow=(color,intensity=.2)=>new THREE.MeshStandardMaterial({color,emissive:color,emissiveIntensity:intensity,metalness:.28,roughness:.3});
const mesh=(geo,mat,parent=scene)=>{const m=new THREE.Mesh(geo,mat);parent.add(m);m.castShadow=true;m.receiveShadow=true;return m;};
const torus=(rad,tube,mat,parent)=>mesh(new THREE.TorusGeometry(rad,tube,12,128),mat,parent);
const between=(a,b,rad,mat,parent=scene)=>{const d=b.clone().sub(a),m=mesh(new THREE.CylinderGeometry(rad,rad,d.length(),8),mat,parent);m.position.copy(a).add(b).multiplyScalar(.5);m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());return m;};
// A procedural machined floor: grain and engraved grids exist in the world, so dolly motion exposes parallax.
const texCanvas=document.createElement('canvas');texCanvas.width=texCanvas.height=1024;const tg=texCanvas.getContext('2d');
tg.fillStyle='#193338';tg.fillRect(0,0,1024,1024);
for(let i=0;i<1024;i++){tg.fillStyle=`rgba(118,151,140,${.008+(Math.sin(i*7.21)*.5+.5)*.021})`;tg.fillRect(0,i,1024,1);}
tg.strokeStyle='rgba(184,195,164,.12)';tg.lineWidth=1;for(let k=0;k<=1024;k+=128){tg.beginPath();tg.moveTo(k,0);tg.lineTo(k,1024);tg.moveTo(0,k);tg.lineTo(1024,k);tg.stroke();}
for(let x=16;x<1024;x+=128)for(let y=16;y<1024;y+=128){tg.fillStyle='#0b2128';tg.beginPath();tg.arc(x,y,3,0,Math.PI*2);tg.fill();}
const floorTex=new THREE.CanvasTexture(texCanvas);floorTex.wrapS=floorTex.wrapT=THREE.RepeatWrapping;floorTex.repeat.set(8,8);floorTex.colorSpace=THREE.SRGBColorSpace;
const floor=mesh(new THREE.PlaneGeometry(300,300),new THREE.MeshStandardMaterial({color:'#102b2e',map:floorTex,metalness:.08,roughness:.74,envMapIntensity:.05}));floor.rotation.x=-Math.PI/2;floor.position.y=-.06;
for(const radius of [18.2,18.4,20]){const line=torus(radius,.016,brass,scene);line.rotation.x=-Math.PI/2;line.position.set(0,.006,-10);}
const amb=new THREE.HemisphereLight('#b4ddd9','#102026',1.3);scene.add(amb);
const key=new THREE.DirectionalLight('#ffe1ac',4.2);key.position.set(-7,12,10);key.castShadow=true;key.shadow.mapSize.set(2048,2048);key.shadow.camera.left=-24;key.shadow.camera.right=24;key.shadow.camera.top=22;key.shadow.camera.bottom=-24;key.shadow.normalBias=.02;scene.add(key);
const rim=new THREE.DirectionalLight('#7ec4d5',2.1);rim.position.set(8,7,-16);scene.add(rim);
const lamps=[],lenses=[];
function optic(z,index){
 const group=new THREE.Group();group.position.set(0,1.92,z);scene.add(group);
 torus(1.31,.065,brass,group);torus(1.41,.035,dark,group).position.z=-.05;torus(1.23,.015,edge,group).position.z=.08;
 const lens=mesh(new THREE.SphereGeometry(1.19,64,32),glass,group);lens.scale.z=.115;
 const lightMat=glow('#ffb85b',.04);torus(1.28,.013,lightMat,group).position.z=.065;
 let lo=0,hi=1;for(let n=0;n<40;n++){const u=(lo+hi)/2;if(smooth(u)<(8-z)/18)lo=u;else hi=u;}
 lamps.push({mat:lightMat,at:1+7.2*(lo+hi)/2});
 for(let j=0;j<48;j++){const a=j/48*Math.PI*2;const bar=mesh(new THREE.BoxGeometry(.012,j%4===0?.12:.055,.025),brass,group);bar.position.set(Math.sin(a)*1.36,Math.cos(a)*1.36,.06);bar.rotation.z=-a;}
 for(const side of [-1,1]){const a=new THREE.Vector3(side*.85,.91,z),b=new THREE.Vector3(side*.85,.09,z+.12);between(a,b,.055,dark);const foot=mesh(new THREE.BoxGeometry(.55,.12,.75),brass);foot.position.copy(b);}
 const base=mesh(new THREE.BoxGeometry(2.55,.08,.92),dark);base.position.set(0,.015,z);
 lenses.push({group,lens});
}
[6,2,-2,-6,-10].forEach(optic);
// Thin guide rails and precision ribs make foreground occlusion and the glass distortion readable.
for(const x of [-1.68,1.68]){between(new THREE.Vector3(x,.22,8),new THREE.Vector3(x,.22,-12),.035,brass);for(let z=8;z>=-12;z-=.75){const m=mesh(new THREE.BoxGeometry(.08,.025,.018),edge);m.position.set(x,.29,z);}}
const anchor=new THREE.Vector3(0,1.92,-10);
const terminal=mesh(new THREE.IcosahedronGeometry(.42,3),new THREE.MeshPhysicalMaterial({color:'#a4d6cf',transmission:.8,thickness:1,ior:1.5,roughness:.12,metalness:0}));terminal.position.copy(anchor);
const pulseMat=glow('#ffc16c',5),pulse=mesh(new THREE.SphereGeometry(.09,24,16),pulseMat);
const pulseLight=new THREE.PointLight('#ffa83d',3.5,7,2);scene.add(pulseLight);
const mainLine=mesh(new THREE.CylinderGeometry(.009,.009,19,8),dark);mainLine.rotation.x=Math.PI/2;mainLine.position.set(0,1.92,-1.5);
const trail=mesh(new THREE.CylinderGeometry(.012,.012,1.7,8),glow('#ffba67',2.5));trail.rotation.x=Math.PI/2;
const satellites=[],routes=[],routeDots=[];
for(let i=0;i<54;i++){
 const layer=Math.floor(i/18),a=i%18/18*Math.PI*2+layer*.14,rad=5.6+layer*3.8;
 const x=Math.cos(a)*rad,z=-10+Math.sin(a)*rad;
 // Keep a corridor open; all other nodes build concentric depth layers.
 if(Math.abs(x)<2.5&&z>-11)continue;
 const y=.7+layer*.17,grp=new THREE.Group();grp.position.set(x,y,z);scene.add(grp);
 const base=mesh(new THREE.CylinderGeometry(.5,.6,.15,32),dark,grp);base.position.y=-y+.08;
 const stem=mesh(new THREE.CylinderGeometry(.075,.12,y,16),brass,grp);stem.position.y=-y*.5;
 const ring=torus(.42,.025,brass,grp);ring.rotation.y=-a;ring.rotation.x=.25;
 const orbmat=glow('#ffbf73',.01);orbmat.color.set('#10282a');const orb=mesh(new THREE.SphereGeometry(.12,16,12),orbmat,grp);
 const shade=mesh(new THREE.SphereGeometry(.36,24,16),glass,grp);shade.scale.y=.65;
 const route=new THREE.CatmullRomCurve3([anchor.clone(),new THREE.Vector3(x*.32,.45,-10+(z+10)*.35),new THREE.Vector3(x*.72,.16,-10+(z+10)*.7),new THREE.Vector3(x,y,z)]);
 const mat=glow('#eeb977',.01);mat.color.set('#254247');const tube=mesh(new THREE.TubeGeometry(route,64,.025,6,false),mat);
 const dot=mesh(new THREE.SphereGeometry(.045,10,8),glow('#ffd290',4));
 const at=8.2+rad*.095+layer*.12;
 satellites.push({grp,mat:orbmat,at});routes.push({route,mat,at});routeDots.push(dot);
}
// A sparse crown, made of repeated fins rather than unrelated background decorations.
for(let i=0;i<60;i++){
 const a=i/60*Math.PI*2,x=Math.cos(a)*19,z=-10+Math.sin(a)*19;if(z>5)continue;
 const h=1.3+1.5*(Math.cos(a*.5)**2);const fin=mesh(new THREE.BoxGeometry(.035,h,.32),edge);fin.position.set(x,h/2,z);fin.rotation.y=-a;
}
// Quiet deterministic dust, small enough to reveal depth without hiding the subject.
const pp=new Float32Array(540*3);let sd=67;const rnd=()=>{sd=(sd*16807)%2147483647;return sd/2147483647;};
for(let i=0;i<540;i++)pp.set([(rnd()-.5)*44,.35+rnd()*7,(rnd()-.5)*40-6],i*3);
const pg=new THREE.BufferGeometry();pg.setAttribute('position',new THREE.BufferAttribute(pp,3));const dust=new THREE.Points(pg,new THREE.PointsMaterial({color:'#d9be91',size:.025,transparent:true,opacity:.3,depthWrite:false}));scene.add(dust);
const macro=cameraTrack({position:[[2.6,2.38,20],[1.5,2.16,18.8]],target:[[0,1.92,4.8],[0,1.92,3.2]],fov:[18,18]});
const dolly=cameraTrack({position:[[1.35,.82,8.8],[1.25,1.04,3],[1.38,1.36,-2.7]],target:[[0,1.92,0],[0,1.92,-5],[0,1.92,-10]],fov:[43,43]});
const crane=cameraTrack({position:[[1.38,1.36,-2.7],[3.8,4.8,2],[10,13.5,14],[17.5,25,28]],target:[[0,1.92,-10],[0,1,-10],[0,.55,-7],[0,.55,-6]],fov:[43,38]});
function stateAt(t){t=Math.max(0,Math.min(DUR,t));const shot=t<4?'macro':t<9?'dolly':t<14?'crane':'hold';return {shot,pose:t<4?macro(t/4):t<9?dolly((t-4)/5):crane(clamp((t-9)/5)),pulseZ:8-18*smooth(clamp((t-1)/7.2))};}
function draw(t){
 const st=stateAt(t);applyCamera(camera,st.pose);
 pulse.position.set(0,1.92,st.pulseZ);pulseLight.position.copy(pulse.position);pulse.visible=t>=.7&&t<8.5;
 trail.visible=pulse.visible;trail.position.set(0,1.92,st.pulseZ+.85);
 pulse.scale.setScalar(1+.15*Math.sin(t*5));pulseLight.intensity=t<8.5?3.5:1;
 terminal.rotation.set(t*.12,t*.2,.2);terminal.material.emissive.set('#c59b4d');terminal.material.emissiveIntensity=.06+smooth((t-8)/.7)*.55;
 for(const {mat,at} of lamps)mat.emissiveIntensity=.04+.8*smooth((t-at)/.35);
 for(let i=0;i<satellites.length;i++){
   const {mat,at}=satellites[i],k=smooth((t-at)/.65);mat.emissiveIntensity=.01+k*7;
   const rt=routes[i],q=clamp((t-8.2)/(rt.at-8.2));rt.mat.emissiveIntensity=.01+k*.9;routeDots[i].visible=t>=8.2&&q<1;routeDots[i].position.copy(rt.route.getPointAt(q));
 }
 dust.rotation.y=t*.009;bloom.strength=.33;composer.render();
 ctx.clearRect(0,0,W,H);ctx.drawImage(r.domElement,0,0);
 // Restrained letterbox and original text; no permanent HUD or chapter layout.
 ctx.fillStyle='#06141a';ctx.fillRect(0,0,W,40);ctx.fillRect(0,H-40,W,40);
 if(t>13.3){const a=smooth((t-13.3)/.9);ctx.save();ctx.globalAlpha=a;ctx.textAlign='left';ctx.fillStyle='#e2d4b2';ctx.font='500 35px "Microsoft YaHei",sans-serif';ctx.fillText('光庭',72,117);ctx.font='14px Georgia,serif';ctx.fillStyle='#a4b2ad';ctx.fillText('L U M E N  /  A  C O D E  F I L M',74,145);ctx.font='18px "Microsoft YaHei",sans-serif';ctx.fillText('一束光，唤醒整个空间。',74,181);ctx.restore();}
 return st;
}
window.__film={duration:DUR,fps:FPS,width:W,height:H,cuts:[4,9,14],continuousCuts:[9,14],holdStart:14,stateAt,ready:true,seek:draw};
window.renderAt=async(t,type='image/png',quality=.94)=>{draw(t);return canvas.toDataURL(type,quality);};
window.ready=true;window.DUR=DUR;
if(!location.search.includes('render')){let start=null;function live(ms){start??=ms;draw(((ms-start)/1000)%DUR);requestAnimationFrame(live);}requestAnimationFrame(live);}
