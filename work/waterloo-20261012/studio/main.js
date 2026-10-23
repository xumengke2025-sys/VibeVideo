import * as THREE from 'three';
import {U,slab,infantry,poseInfantry,cavalry,poseCavalry,standard,poseStandard,cannon,regiment} from './art.js';
import {skyPanel,tex} from './vendor/paper.js';
import {SHOTS,EVENTS,clamp,mix,smooth,seed,shotAt} from './timeline.js';
const qs=new URLSearchParams(location.search),W=Number(qs.get('width')||540),H=W*16/9;
const canvas=document.querySelector('#film'),renderer=new THREE.WebGLRenderer({canvas,antialias:true,preserveDrawingBuffer:true});
renderer.setPixelRatio(1);renderer.setSize(W,H,false);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.NoToneMapping;
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
const scene=new THREE.Scene();scene.background=new THREE.Color('#152a36');
const camera=new THREE.PerspectiveCamera(46,9/16,.1,100);
scene.add(new THREE.AmbientLight('#fff1d5',1.15));
const sun=new THREE.DirectionalLight('#ffe1ac',1.4);sun.position.set(-5,9,16);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);Object.assign(sun.shadow.camera,{left:-13,right:13,top:14,bottom:-14,near:.1,far:70});sun.shadow.bias=-.00018;sun.shadow.normalBias=.006;scene.add(sun);sun.target.position.set(0,-2,-4);scene.add(sun.target);
U.uLight.value.set(-1.3,1.5,-9);U.uLightR.value=8;U.uLit.value=1;U.uLightCol.value.set('#ffdca0');
const backdrop=skyPanel({w:24,h:36,z:-10,ppm:75,gain:.94,stops:[[0,'#203f50'],[.25,'#607e82'],[.52,'#ead4a1'],[.74,'#a28860'],[1,'#293e42']],extra:x=>{
 const g=x.createRadialGradient(-1,2,.15,-1,2,8);g.addColorStop(0,'rgba(255,235,170,.72)');g.addColorStop(.3,'rgba(255,222,154,.32)');g.addColorStop(1,'rgba(255,220,150,0)');x.fillStyle=g;x.fillRect(-12,-18,24,36);
}});scene.add(backdrop);
// Five continuous cut contours. Actors share the same terrain function as their layer.
const palette=['#a99b77','#7b897c','#546b66','#344b4c','#1c333d'],tops=[1.0,-.35,-2.15,-4.25,-6.8],zs=[-7.8,-5.3,-2.7,.0,2.8];
const ridge=(x,j)=>tops[j]+.20*Math.sin(x*.53+j*.8)+.065*Math.sin(x*1.65+j);
const terrain=[];
for(let j=0;j<5;j++){
 const land=slab(26,18,x=>{x.fillStyle=palette[j];x.beginPath();x.moveTo(-13,-9);for(let k=0;k<=260;k++){const px=-13+k*.1;x.lineTo(px,ridge(px,j)-tops[j]+8.85)}x.lineTo(13,-9);x.closePath();x.fill();},{ppm:100,trans:[.32,.23,.15,.08,.025][j]});land.position.set(0,tops[j]-8.85,zs[j]);scene.add(land);terrain.push(land);
}
const farm=slab(2.4,1.2,x=>{x.fillStyle='#657365';x.fillRect(-1,-.55,1.0,.58);x.fillRect(.12,-.55,.98,.72);x.beginPath();x.moveTo(-1.17,.03);x.lineTo(-.51,.55);x.lineTo(.17,.03);x.closePath();x.fill();x.beginPath();x.moveTo(-.02,.16);x.lineTo(.63,.65);x.lineTo(1.23,.16);x.closePath();x.fill();x.fillStyle='#a69b75';for(let i=0;i<4;i++)x.fillRect(-.88+i*.48,-.24,.07,.19)},{trans:.18});farm.position.set(-4.4,1.7,-7.5);scene.add(farm);
// Dark outer paper aperture: curved sides, top arch and grass, with real spacing from the stage.
const frame=slab(16,26,x=>{x.fillStyle='#112a36';x.beginPath();x.rect(-8,-13,16,26);x.moveTo(-4.05,-10);x.lineTo(4.05,-10);x.lineTo(4.05,4.8);x.bezierCurveTo(4.0,7.8,-4.0,7.8,-4.05,4.8);x.closePath();x.fill('evenodd');},{trans:.015});frame.position.z=4.5;scene.add(frame);
const grasses=slab(20,7,x=>{x.strokeStyle='#142e38';x.lineCap='round';for(let k=0;k<160;k++){const px=(seed(k+91)-.5)*20,y=-3.5+seed(k+8)*.30;const side=Math.abs(px)>3.7?1.0:.25;x.lineWidth=.025+seed(k+19)*.035;x.beginPath();x.moveTo(px,y);x.quadraticCurveTo(px+.2,y+side*.45,px+(seed(k+81)-.5)*.6,y+side*(.4+seed(k+63)*1.25));x.stroke()}},{trans:.01});grasses.position.set(0,-6.8,4.2);scene.add(grasses);
const groups={};function group(id){const g=new THREE.Group();groups[id]=g;scene.add(g);return g}
function actor(parent,kind,x,j,size=1,z=zs[j]+.16){const u=infantry(kind,seed(x+33)*6);u.scale.setScalar(size);u.position.set(x,ridge(x,j),z);parent.add(u);return u}
function row(parent,kind,x,j,count=12,size=.65,z=zs[j]+.13){const r=regiment(kind,count,seed(x+3)*9);r.scale.setScalar(size);r.position.set(x,ridge(x,j)+.6*size,z);parent.add(r);return r}
function banner(parent,x,y,z,size=.76){const b=standard();b.position.set(x,y,z);b.scale.setScalar(size);parent.add(b);return b}
const intro=group('standard'),guns=group('guns'),charge=group('charge'),square=group('square'),pressure=group('pressure'),guard=group('guard'),collapse=group('collapse'),aftermath=group('aftermath');
const introBearer=actor(intro,'guard',-1.4,3,1.2,.4),introFlag=banner(intro,-1.0,ridge(-1.4,3)+.9,.55,.95);
const introRows=[row(intro,'guard',0,2,15,.7),row(intro,'guard',-1.5,1,17,.53)];
const gun=cannon();gun.position.set(-1.0,ridge(-1,3),.35);gun.scale.setScalar(1.25);guns.add(gun);const crew=actor(guns,'guard',-3,3,1.0,.5);row(guns,'british',1.5,1,15,.5);
const lead=cavalry(.6);charge.add(lead);lead.scale.setScalar(1.08);const second=cavalry(2.4);charge.add(second);second.scale.setScalar(.65);row(charge,'british',1.0,1,17,.48);
const encounter=cavalry(.6);encounter.scale.setScalar(1.03);square.add(encounter);
const defenders=[actor(square,'british',.5,3,.88,.55),actor(square,'british',1.5,3,.88,.55),actor(square,'british',2.5,3,.88,.55)];
const sqA=regiment('british',9,0,.20),sqB=regiment('british',7,2,.85);sqA.scale.setScalar(.54);sqB.scale.setScalar(.45);sqA.position.set(1.0,-1.7,-2.45);sqB.position.set(2.5,-.9,-3.0);square.add(sqA,sqB);
const pressureBearer=actor(pressure,'guard',-1.35,3,1.10,.35),pressureFlag=banner(pressure,-.98,ridge(-1.35,3)+.83,.5,.90);const returnHorse=cavalry(2);returnHorse.scale.setScalar(.75);pressure.add(returnHorse);const flanks=[row(pressure,'prussian',3.2,1,13,.52),row(pressure,'prussian',4.1,0,16,.40)];
const guardMen=[actor(guard,'guard',-1.35,3,1.12,.4),actor(guard,'guard',.0,3,1.04,.35),actor(guard,'guard',1.15,3,.96,.3)];const guardFlag=banner(guard,-.98,ridge(-1.35,3)+.83,.6,.9);const guardRows=[row(guard,'guard',-1.2,2,11,.62),row(guard,'guard',-2.0,1,13,.49)];row(guard,'british',1.5,0,16,.48);
const brokenMen=[actor(collapse,'guard',-1.35,3,1.12,.4),actor(collapse,'guard',0,3,1.04,.35),actor(collapse,'guard',1.15,3,.96,.3)];const brokenFlag=banner(collapse,-.98,ridge(-1.35,3)+.83,.6,.9);const brokenRows=[row(collapse,'guard',-1.2,2,11,.62),row(collapse,'guard',-2,1,13,.49)];row(collapse,'british',1.5,0,16,.48);
const lastBearer=actor(aftermath,'guard',-1.4,3,1.2,.4),lastFlag=banner(aftermath,-1.0,ridge(-1.4,3)+.75,.55,.95);const lost=[actor(aftermath,'guard',2,2,.48,-2.5),actor(aftermath,'guard',3.3,1,.35,-5.1)];const abandoned=cannon();abandoned.position.set(3.3,ridge(3.3,3),.2);abandoned.scale.setScalar(.6);aftermath.add(abandoned);
const earlyFlank=row(scene,'prussian',4.6,0,15,.29,-7.5);
// Keep terrain depth shadows; silhouettes receive light but do not project atlas-sized shadow quads.
scene.traverse(m=>{if(m.isMesh&&!terrain.includes(m))m.castShadow=false});
// Smoke is translucent cut-paper scallops. It shares the stage palette, rather than photographic fog.
function cloud(){return slab(4,2,x=>{x.fillStyle='#b5b08f';x.beginPath();x.moveTo(-2,-.65);x.bezierCurveTo(-2,.0,-1.6,.4,-1.2,.25);x.bezierCurveTo(-1.0,1,-.3,1,-.15,.55);x.bezierCurveTo(.4,1,1.0,.65,1.1,.27);x.bezierCurveTo(1.8,.5,2,.0,1.9,-.5);x.bezierCurveTo(.7,-.9,-.7,-.7,-2,-.65);x.fill()},{shadow:false,recv:false,trans:.32})}
const smoke=[];for(let i=0;i<7;i++){const m=cloud();m.material.transparent=true;m.material.alphaTest=.01;m.material.depthWrite=false;scene.add(m);smoke.push(m)}
const flashes=[];for(let i=0;i<4;i++){const p=new THREE.PointLight('#ffda8d',0,9,2);scene.add(p);flashes.push(p)}
const glowCanvas=document.createElement('canvas');glowCanvas.width=glowCanvas.height=128;const gx=glowCanvas.getContext('2d'),grad=gx.createRadialGradient(64,64,0,64,64,64);grad.addColorStop(0,'rgba(255,234,164,.96)');grad.addColorStop(.1,'rgba(255,213,128,.65)');grad.addColorStop(1,'rgba(255,200,100,0)');gx.fillStyle=grad;gx.fillRect(0,0,128,128);const glow=new THREE.Mesh(new THREE.PlaneGeometry(1,1),new THREE.MeshBasicMaterial({map:tex(glowCanvas),transparent:true,depthWrite:false,blending:THREE.AdditiveBlending}));scene.add(glow);
function moveMarch(u,x,j,z,size,t,amount=1){u.position.set(x,ridge(x,j),z);u.rotation.y=0;u.scale.setScalar(size);poseInfantry(u,t,.63,'march',amount)}
function drawAt(time){
 const t=clamp(time,0,59.999),shot=shotAt(t).id;for(const [id,g] of Object.entries(groups))g.visible=id===shot;
 let cx=0,cy=-.2,cz=22.5;sun.intensity=1.35;U.uLit.value=1.0;backdrop.material.color.setScalar(.94);frame.position.x=0;
 earlyFlank.position.x=4.6-smooth(t,0,35)*.9;
 if(shot==='standard'){const p=smooth(t,0,5.8);cx=mix(-.65,0,p);cy=mix(1.5,-.2,p);cz=mix(13.5,22.5,p);poseStandard(introFlag,t);poseInfantry(introBearer,t,.2,'march',.06)}
 if(shot==='guns'){const p=smooth(t,6,13.9);cx=mix(-.6,.3,p);cy=mix(-1.8,-.5,p);cz=mix(18.0,22,p);let recoil=0;for(const e of EVENTS.filter(e=>e.kind==='cannon')){const d=t-e.t;if(d>=0)recoil+=(1-Math.exp(-d*25))*Math.exp(-d*3.3)*.48}gun.position.x=-1-recoil;gun.userData.wheel.rotation.z=recoil/.63;poseInfantry(crew,t,.1,'kneel',.03)}
 if(shot==='charge'){const q=t-14,p=smooth(t,14,20),x=mix(-3.4,-.7,p);cx=mix(-1.2,.15,p);cy=-1;cz=20.8;lead.position.set(x,ridge(x,3)+poseCavalry(lead,t,1.0),.5);lead.rotation.y=0;second.position.set(x-2.0,ridge(x-2,2)+poseCavalry(second,t,1.06)*.65,-2.45);second.rotation.y=0}
 if(shot==='square'){const a=smooth(t,20,22.1),ret=smooth(t,23.4,26),x=mix(-2.8,-1.3,a)-ret*2.3;cx=.15;cy=-1.2;cz=20.8;encounter.position.set(x,ridge(x,3)+poseCavalry(encounter,t,t<22.1?.85:t<23.4?.05:-.65)*.3,.6);encounter.rotation.y=0;encounter.rotation.z=-Math.sin(smooth(t,22.4,24)*Math.PI)*.08;defenders.forEach(u=>poseInfantry(u,t,.05,'aim',0))}
 if(shot==='pressure'){const p=smooth(t,26,35);cx=mix(-.3,.6,p);cy=-.5;cz=mix(21,23,p);poseStandard(pressureFlag,t,.18);poseInfantry(pressureBearer,t,.1,'march',.05);const x=mix(.6,-5.8,smooth(t,26,30));returnHorse.position.set(x,ridge(x,2)+poseCavalry(returnHorse,t,.8)*.7,-2.4);returnHorse.rotation.y=Math.PI;flanks.forEach((r,i)=>r.position.x=3.2+i*.9-p*1.3)}
 if(shot==='guard'){const p=smooth(t,35,44.6),advance=p*.70;cx=mix(-.45,.25,p);cy=mix(-.8,-.55,p);cz=mix(20.4,22.3,p);guardMen.forEach((u,i)=>moveMarch(u,[-1.35,0,1.15][i]+advance,3,[.4,.35,.3][i],[1.12,1.04,.96][i],t,t>45.55?.02:1));guardFlag.position.set(-.98+advance,ridge(-1.35+advance,3)+.83,.6);poseStandard(guardFlag,t,.04);guardRows.forEach((r,i)=>r.position.x=[-1.2,-2][i]+advance*.7)}
 if(shot==='collapse'){cx=.25;cy=-.55;cz=22.3;brokenMen.forEach((u,i)=>{const r=smooth(t,47.4+i*.43,53),x=[-1.35,0,1.15][i]+.7-r*(2.2+i*.2);u.position.set(x,ridge(x,3),[.4,.35,.3][i]);u.scale.setScalar([1.12,1.04,.96][i]);u.rotation.y=0;poseInfantry(u,t,t<47.4+i*.43?.08:.72,'retreat',t<47.4+i*.43?.03:1)});const r=smooth(t,47.4,53);brokenFlag.position.set(-.28-r*2.2,ridge(-.65-r*2.2,3)+.83-r*.15,.6);poseStandard(brokenFlag,t,smooth(t,47.5,50)*.8);brokenRows.forEach((u,i)=>{const r=smooth(t,48.8+i*.6,54);u.position.x=[-1.2,-2][i]+.49-r*1.9;u.rotation.z=-r*.07})}
 if(shot==='aftermath'){const p=smooth(t,54,59.5);cx=mix(-.55,0,p);cy=mix(.9,-.2,p);cz=mix(16.2,22.5,p);poseInfantry(lastBearer,t,.1,'kneel',.0);poseStandard(lastFlag,t,.95);lost.forEach((u,i)=>{const x=[2,3.3][i]-p*1.6;u.position.set(x,ridge(x,i?1:2),i?-5.1:-2.5);u.rotation.y=Math.PI;poseInfantry(u,t,.5,'retreat',1-p*.8)});sun.intensity=mix(1.35,.65,p);U.uLit.value=mix(1,.42,p);backdrop.material.color.setRGB(mix(.94,.40,p),mix(.94,.54,p),mix(.94,.66,p))}
 if(shot==='square'){cz=17.2;cy=-2.4;cx=.1}
 if(shot==='charge'){cz=18.7;cy=-1.9}
 if(shot==='guns'){cz-=1.2;cy-=.3}
 if(shot==='guard'||shot==='collapse'){cz-=2.3;cy-=.9}
 camera.position.set(cx,cy,cz);camera.lookAt(cx,cy,0);
 smoke.forEach(m=>m.visible=false);flashes.forEach(f=>f.intensity=0);glow.visible=false;
 const relevant=EVENTS.filter(e=>shot==='guns'&&e.kind==='cannon'||shot==='square'&&e.id==='square-volley'||shot==='collapse'&&e.id==='guard-volley');
 relevant.forEach((e,i)=>{const d=t-e.t;if(d<0||d>3.8)return;const isGun=e.kind==='cannon',x=isGun?1.1:shot==='square'?.5:1.0,y=isGun?-3.1:shot==='square'?-3.2:.8,z=isGun?.7:shot==='square'?.7:-6.9;const flash=Math.exp(-d*35);flashes[i].position.set(x,y,z+1);flashes[i].intensity=flash*22;if(d<.15){glow.visible=true;glow.position.set(x,y,z+.2);glow.scale.set(isGun?2.3:5.5,isGun?2.3:.9,1);glow.material.opacity=flash*.8}const m=smoke[i];m.visible=true;m.position.set(x+d*.32,y+d*.42,z+.2);m.scale.setScalar(.25+d*.27);m.material.opacity=(1-Math.exp(-d*7))*Math.exp(-d*1.4)*.43});
 renderer.render(scene,camera);return stateAt(t);
}
function stateAt(t){return{t,shot:shotAt(t).id,camera:camera.position.toArray(),dimensions:[W,H],paperDepths:zs,nearActorLimit:3,text:false,delivery_mode:'user_feedback',style:'layered-paper-lightbox-v3'}}
window.renderAt=(t,type='image/png',quality=.95)=>{drawAt(t);return canvas.toDataURL(type,quality)};window.stateAt=t=>{drawAt(t);return stateAt(t)};window.__ready=true;drawAt(0);
const audio=document.querySelector('#audio'),seek=document.querySelector('#seek'),clock=document.querySelector('#clock');let playing=false,start=0,current=0;
if(qs.has('render'))document.querySelector('#controls').style.display='none';
document.querySelector('#play').onclick=()=>{playing=!playing;if(playing){start=performance.now()/1000-current;audio.currentTime=current;audio.play()}else audio.pause();document.querySelector('#play').textContent=playing?'Ⅱ':'▶'};
seek.oninput=()=>{current=+seek.value;drawAt(current);audio.currentTime=current;start=performance.now()/1000-current;clock.textContent=current.toFixed(2)};
function tick(){if(playing){current=performance.now()/1000-start;if(current>=60){playing=false;audio.pause();current=59.999}drawAt(current);seek.value=current;clock.textContent=current.toFixed(2)}requestAnimationFrame(tick)}if(!qs.has('render'))tick();
