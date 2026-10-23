import * as THREE from 'three';
import {U,images,sprite,slab,line,infantry,poseInfantry,cavalry,poseCavalry,standard,poseStandard,cannon,regiment,smokeTexture} from './art.js';
import{DURATION,FPS,SHOTS,EVENTS,clamp,mix,smooth,seed,shotAt}from'./timeline.js';
const qs=new URLSearchParams(location.search),W=Number(qs.get('width')||540),H=W*16/9;
const canvas=document.querySelector('#film');const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:false,preserveDrawingBuffer:true});
renderer.setPixelRatio(1);renderer.setSize(W,H,false);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.42;
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
const scene=new THREE.Scene();scene.background=new THREE.Color('#151e2a');
const camera=new THREE.PerspectiveCamera(46,9/16,.1,100);camera.position.set(0,0,18);
scene.add(new THREE.HemisphereLight('#a8bad5','#253046',1.15));
const sun=new THREE.DirectionalLight('#f9dca3',2.5);sun.position.set(-8,10,15);sun.castShadow=true;sun.shadow.mapSize.set(W<1080?1024:2048,W<1080?1024:2048);Object.assign(sun.shadow.camera,{left:-17,right:17,top:16,bottom:-16,near:1,far:60});sun.shadow.bias=-.00035;sun.shadow.normalBias=.015;scene.add(sun);sun.target.position.set(0,0,-4);scene.add(sun.target);
const cool=new THREE.DirectionalLight('#536e99',1.1);cool.position.set(8,0,8);scene.add(cool);
const backgroundTexture=new THREE.Texture(images.battlefield);backgroundTexture.needsUpdate=true;backgroundTexture.colorSpace=THREE.SRGBColorSpace;
const background=slab(18,32,x=>{x.save();x.scale(1,-1);x.drawImage(images.battlefield,-9,-16,18,32);x.restore()},{shadow:false,recv:false,ppm:70,trans:.30});background.position.set(0,2,-9);scene.add(background);
// Eight genuine paper depths, each receives a neighboring cast shadow. No box frame.
const terrain=[];
const colors=['#726757','#665d51','#514c43','#45443d','#383b38','#343431','#282c2c','#20272b'];
for(let j=0;j<8;j++){
 const y=3.1-j*1.42,z=-8.6+j*1.37;
 const land=slab(39,21,x=>{
  x.fillStyle=colors[j];x.beginPath();x.moveTo(-19.5,-10.5);
  for(let k=0;k<=195;k++){const px=-19.5+k*.2,py=10.4+.30*Math.sin(px*.48+j*.8)+.07*Math.sin(px*5.2+j);x.lineTo(px,py)}
  x.lineTo(19.5,-10.5);x.closePath();x.fill();
  x.save();x.globalCompositeOperation='source-atop';x.scale(1,-1);x.globalAlpha=.91;x.drawImage(images.battlefield,-9,y-10.5-18,18,32);x.restore();
  x.strokeStyle='rgba(198,169,105,.17)';x.lineWidth=.018;
  for(let k=0;k<470;k++){
   const px=(seed(k*7+j)-.5)*39,py=8.5-seed(k*7+1+j)*7;
   x.beginPath();x.moveTo(px,py);x.lineTo(px+.08,py+.04);x.lineTo(px+.10,py-.03);x.stroke();
  }
 },{shadow:true,trans:.09});land.position.set(0,y-10.5,z);scene.add(land);terrain.push(land);
}
// A cut-paper farmhouse in the distant ridge, a period landmark rather than a label.
const farm=slab(2.5,1.2,x=>{
 x.fillStyle='#554d3e';x.fillRect(-1.1,-.55,1.2,.60);x.fillRect(.13,-.55,.94,.65);
 x.fillStyle='#272e33';x.beginPath();x.moveTo(-1.23,.05);x.lineTo(-.45,.56);x.lineTo(.20,.05);x.closePath();x.fill();x.beginPath();x.moveTo(.03,.12);x.lineTo(.63,.61);x.lineTo(1.19,.12);x.closePath();x.fill();
 x.fillStyle='#1d262b';for(let k=0;k<6;k++)x.fillRect(-1+k*.35,-.19,.095,.20);
},{trans:.1});farm.position.set(4.1,2.9,-7.2);scene.add(farm);
const groups={};function group(id){const g=new THREE.Group();groups[id]=g;scene.add(g);return g}
const intro=group('standard'),guns=group('guns'),charge=group('charge'),square=group('square'),pressure=group('pressure'),guard=group('guard'),collapse=group('collapse'),aftermath=group('aftermath');
const banks=[];
function ranks(parent,kind,nRows,y0,z0,x0=0,rowsize=28,scale=.8){
 const rows=[];
 for(let i=0;i<nRows;i++){const r=regiment(kind,rowsize,i*.9);r.position.set(x0+(i%2)*.18,y0+i*.49,z0-i*.07);r.scale.setScalar(scale);parent.add(r);rows.push(r)}return rows;
}
function squad(parent,kind,n,x0,y0,z0,spacing=.63,size=1){
 const units=[];for(let i=0;i<n;i++){const row=Math.floor(i/6),col=i%6;const u=infantry(kind,seed(i+1)*Math.PI*2);u.scale.setScalar(size);u.position.set(x0+col*spacing,y0+row*.55,z0-row*.08);parent.add(u);units.push({u,x:u.position.x,y:u.position.y,z:u.position.z,i})}return units;
}
const startRanks=ranks(intro,'guard',7,-4.4,-.1,0,32,.68);
const bearer=infantry('guard',0);bearer.position.set(-1.65,-4.6,1.8);bearer.scale.setScalar(1.16);intro.add(bearer);
const mainStandard=standard();mainStandard.position.set(-1.20,-3.62,1.95);intro.add(mainStandard);
const napoleon=sprite('napoleon',.68,.70,0,-.35,.03);napoleon.position.set(-3.2,-2.0,.45);intro.add(napoleon);
const gunModels=[];for(let i=0;i<3;i++){const c=cannon();c.position.set(-3.3+i*3.4,-3.25+i*.78,1-i*.75);c.userData.baseX=c.position.x;guns.add(c);gunModels.push(c)}
const gunCrew=squad(guns,'guard',6,-4.0,-3.7,1.12,.81,.85);
const gunDefense=ranks(guns,'british',3,1.24,-3.9,.3,37,.44);
const chargeRiders=[];for(let i=0;i<13;i++){
 const h=cavalry(seed(i+22)*7);const row=Math.floor(i/4),s=1.02-row*.105;
 h.scale.setScalar(s);const data={h,x:-7.2+(i%4)*2.7-row*1.2,y:-5.6+row*1.6,z:2-row*.68,phase:seed(i+29)*7};charge.add(h);chargeRiders.push(data);
}
const chargeDefense=ranks(charge,'british',2,2.05,-3.9,.6,36,.47);
// Oblique square has a visible empty center, four stable sides and separate elevated horse assets.
const squareUnits=[];
for(let side=0;side<4;side++)for(let k=0;k<13;k++){
 const p=k/12;let x,y;
 if(side===0){x=mix(-3.15,2.7,p);y=-.5}
 if(side===1){x=mix(-3.15,2.7,p);y=2.2}
 if(side===2){x=-3.15;y=mix(-.5,2.2,p)}
 if(side===3){x=2.7;y=mix(-.5,2.2,p)}
 const u=infantry((k+side)%7===0?'prussian':'british',k*.8);u.scale.setScalar(.54);u.position.set(x,y-.3,-1.4+side*.015);if(side===2)u.scale.x*=-1;square.add(u);squareUnits.push({u,side,k});
}
const squareHorses=[];for(let i=0;i<9;i++){
 const h=sprite('elevated-horse',1.47,1.77,0,-.70,.02);h.position.set(-5+i%3*1.17,-5.8-Math.floor(i/3)*1.05,.25-Math.floor(i/3)*.05);square.add(h);squareHorses.push({h,i,x:h.position.x,y:h.position.y});
}
const squareCenter=slab(5.3,2.8,x=>{x.fillStyle='#5c584a';x.beginPath();x.moveTo(-2.6,-1.4);x.lineTo(2.6,-1.4);x.lineTo(2.6,1.4);x.lineTo(-2.6,1.4);x.closePath();x.fill()},{shadow:false});squareCenter.position.set(-.2,.66,-1.62);square.add(squareCenter);
const pressureRanks=ranks(pressure,'guard',4,-3.9,-.1,-1.3,24,.65);
const flank=ranks(pressure,'prussian',5,.2,-3.25,4.8,22,.50);
const pressureBearer=infantry('guard',.5);pressureBearer.position.set(-2,-4.55,1.4);pressureBearer.scale.setScalar(1.05);pressure.add(pressureBearer);
const pressureStandard=standard();pressureStandard.position.set(-1.62,-3.66,1.55);pressure.add(pressureStandard);
const backRiders=[];for(let i=0;i<5;i++){const h=cavalry(i*1.8);h.scale.set(.75,.75,.75);pressure.add(h);backRiders.push({h,x:-5+i*2.6,y:-2+i%2*.7,z:.5})}
const guardRanks=ranks(guard,'guard',7,-4.8,-.4,.2,30,.7);
const guardSquad=squad(guard,'guard',18,-3.1,-5.7,1.3,.88,1.0);
const guardStandard=standard();guardStandard.scale.setScalar(.95);guard.add(guardStandard);
const guardEnemy=ranks(guard,'british',3,2.1,-2.65,0,34,.55);
const collapseRanks=ranks(collapse,'guard',4,-2.4,.1,0,23,.65);
const collapseSquad=squad(collapse,'guard',24,-3.2,-2.8,1.2,.9,1.0);
const collapseStandard=standard();collapseStandard.scale.setScalar(.95);collapse.add(collapseStandard);
const collapseEnemy=ranks(collapse,'british',2,2.3,-2.65,0,33,.55);
const lastBearer=infantry('guard',.5);lastBearer.position.set(-1.65,-4.6,1.8);lastBearer.scale.setScalar(1.16);aftermath.add(lastBearer);
const finalStandard=standard();finalStandard.position.set(-1.2,-3.62,1.95);aftermath.add(finalStandard);
const retreaters=squad(aftermath,'guard',9,-5.0,-5.2,.3,1.5,.67);
const abandoned=cannon();abandoned.position.set(3.3,-4.3,.2);abandoned.scale.setScalar(.66);aftermath.add(abandoned);
// Background flank column is present before its narrative foreground reveal.
const earlyFlank=ranks(scene,'prussian',3,3.18,-5.8,6.2,22,.27);
const mistMap=smokeTexture(),smokes=[];
for(let i=0;i<28;i++){
 const m=new THREE.Mesh(new THREE.PlaneGeometry(1,1),new THREE.MeshBasicMaterial({map:mistMap,transparent:true,opacity:0,depthWrite:false,color:'#b4b2a3'}));scene.add(m);smokes.push(m);
}
const flashes=[];
for(let i=0;i<5;i++){
 const p=new THREE.PointLight('#ffce87',0,11,2);scene.add(p);flashes.push(p);
}
const flashMap=(()=>{const c=document.createElement('canvas');c.width=c.height=128;const x=c.getContext('2d'),g=x.createRadialGradient(64,64,0,64,64,64);g.addColorStop(0,'rgba(255,225,155,1)');g.addColorStop(.15,'rgba(255,160,55,.8)');g.addColorStop(1,'rgba(255,140,40,0)');x.fillStyle=g;x.fillRect(0,0,128,128);return new THREE.CanvasTexture(c)})();
const burst=new THREE.Mesh(new THREE.PlaneGeometry(1,1),new THREE.MeshBasicMaterial({map:flashMap,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,opacity:0}));scene.add(burst);
// Subtle lens vignette is in the rendered scene, with no typography.
const vignette=(()=>{const c=document.createElement('canvas');c.width=256;c.height=456;const x=c.getContext('2d');const gr=x.createRadialGradient(128,218,80,128,218,270);gr.addColorStop(0,'rgba(8,14,23,0)');gr.addColorStop(.65,'rgba(8,14,23,.03)');gr.addColorStop(1,'rgba(8,14,23,.62)');x.fillStyle=gr;x.fillRect(0,0,256,456);const tx=new THREE.CanvasTexture(c);const s=new THREE.Scene(),c2=new THREE.OrthographicCamera(-1,1,16/9,-16/9,0,2);const m=new THREE.Mesh(new THREE.PlaneGeometry(2,32/9),new THREE.MeshBasicMaterial({map:tx,transparent:true,depthTest:false,depthWrite:false}));s.add(m);return{s,c2}})();
let lastState;
function formation(rows,t,speed=.07){for(let i=0;i<rows.length;i++){const r=rows[i];r.position.y+=0; r.rotation.z=.002*Math.sin(t*2+i);r.position.x=(r.userData.originalX??(r.userData.originalX=r.position.x))+Math.sin(t*.8+i)*.014;}}
export function stateAt(time){
 const t=clamp(time,0,59.999),shot=shotAt(t);return{t,shot:shot.id,camera:camera.position.toArray(),flagLoss:shot.id==='aftermath'?1:shot.id==='collapse'?smooth(t,47,51):0,dimensions:[W,H],paperDepths:terrain.map(m=>m.position.z),text:false,delivery_mode:'user_feedback'};
}
function drawAt(time){
 const t=clamp(time,0,59.999),shot=shotAt(t).id;
 for(const[id,g]of Object.entries(groups))g.visible=id===shot;
 let cx=0,cy=0,cz=18,tx=0,ty=0;
 sun.intensity=1.85;cool.intensity=.85;U.uLit.value=.47;U.uLightCol.value.set('#e8c998');background.material.color.set('#8194aa');
 for(let j=0;j<earlyFlank.length;j++)earlyFlank[j].position.x=6.2-j*.05-smooth(t,0,35)*1.5;
 if(shot==='standard'){
  const p=smooth(t,0,5.5);cx=mix(-.7,-.1,p);cy=mix(2.4,-.1,p);cz=mix(8.7,17.5,p);tx=cx;ty=cy;
  poseStandard(mainStandard,t);poseInfantry(bearer,t,.3,'march',.035);
  napoleon.visible=t>1.8&&t<5.5;formation(startRanks,t);
 }
 if(shot==='guns'){
  const p=smooth(t,6,13.2);cx=mix(-2.5,1.1,p);cy=mix(-1.1,.20,p);cz=mix(11.8,18,p);tx=cx;ty=cy;
  gunModels.forEach((c,i)=>{const d=t-EVENTS[i].t;const recoil=d<0?0:(1-Math.exp(-d*18))*Math.exp(-d*3.6)*.65;c.position.x=c.userData.baseX-recoil;c.userData.wheel.rotation.z=recoil/0.63});
  gunCrew.forEach(({u,i})=>poseInfantry(u,t,.15,i%2?'kneel':'march',.02));
 }
 if(shot==='charge'){
  const q=t-14;cx=mix(-2.2,1.1,smooth(t,14,20));cy=mix(-1.2,.1,smooth(t,14,20));cz=mix(14.0,15.1,smooth(t,14,20));tx=cx;ty=cy;
  chargeRiders.forEach(({h,x,y,z},i)=>{
   const advance=q*.85+.065*q*q;h.position.set(x+advance,y+advance*.24,z);h.position.y+=poseCavalry(h,t,1.12+i*.011);h.scale.x=Math.abs(h.scale.x);
  });
 }
 if(shot==='square'){
  const p=smooth(t,20,22);cx=mix(-1.7,-.1,p);cy=mix(-.7,.2,p);cz=mix(18.6,17.6,p);tx=cx;ty=cy;
  squareUnits.forEach(({u,k})=>poseInfantry(u,t,.02,t>22.55?'aim':'march',0));
  squareHorses.forEach(({h,i,x,y})=>{
   const q=t-20-i*.1,a=clamp(q/2.6),turn=smooth(q,2.05,3.45),run=Math.max(0,q-3.25);
   h.position.set(x+a*2.4+turn*.75+run*(i%2?-.78:1.04),y+a*4.25-run*.82+(i%3)*.03,.12);
   h.rotation.z=-(i%2?1:-1)*turn*.80;h.scale.setScalar(1-.12*turn);h.position.y+=.025*Math.sin(t*12+i);
  });
 }
 if(shot==='pressure'){
  const q=t-26,p=smooth(t,28,34);cx=mix(-1.3,2.1,p);cy=mix(-.5,.1,p);cz=mix(16.4,19.6,p);tx=cx;ty=cy;
  pressureBearer.position.x=-2+q*.13;pressureStandard.position.x=-1.62+q*.13;poseStandard(pressureStandard,t,.13);poseInfantry(pressureBearer,t,.65);
  flank.forEach((r,i)=>{r.position.x=4.8-q*.15+(i%2)*.1;r.position.y=.2+i*.49-q*.035});
  backRiders.forEach(({h,x,y,z},i)=>{h.scale.x=-Math.abs(h.scale.x);h.position.set(x-q*.95,y-q*.1,z);h.position.y+=poseCavalry(h,t,.92)})
 }
 if(shot==='guard'){
  const q=t-35,p=smooth(t,35,44.7);cx=mix(-1.2,.15,p);cy=mix(-.80,.65,p);cz=mix(13.8,17.3,p);tx=cx;ty=cy;
  guardSquad.forEach(({u,x,y,z,i})=>{u.position.set(x+q*.16,y+q*.19,z);u.position.y+=Math.abs(Math.sin(t*7+i))*.025;poseInfantry(u,t,.83)});
  guardRanks.forEach((r,i)=>{r.position.y=-4.8+i*.49+q*.17;r.position.x=.2+q*.12+(i%2)*.18});
  guardStandard.position.set(-1.48+q*.16,-4.75+q*.19,1.42);poseStandard(guardStandard,t);
 }
 if(shot==='collapse'){
  const q=t-46;cx=.35;cy=.73;cz=17.3;tx=cx;ty=cy;
  const loss=smooth(t,47.1,50.6);
  collapseSquad.forEach(({u,x,y,z,i})=>{
   const delay=Math.floor(i/6)*.43+(i%6)*.07,ret=Math.max(0,q-1.95-delay),f=smooth(q,1.85+delay,2.6+delay);
   u.position.set(x-ret*(.55+seed(i+90)*.8)+(seed(i+55)-.5)*f,y-ret*(.36+seed(i+95)*.17),z);
   u.scale.x=(i%7===0?1:1-2*f);if(Math.abs(u.scale.x)<.18)u.scale.x=u.scale.x<0?-.18:.18;
   poseInfantry(u,t,ret?.9:.13,i%9===0&&q>1?'kneel':ret?'retreat':'march',ret?1:.05);
  });
  collapseRanks.forEach((r,i)=>{const ret=Math.max(0,q-2.8-i*.5);r.position.x=ret*(i%2?-.25:.17);r.position.y=-2.4+i*.49-ret*.22;r.rotation.z=ret*(i%2?-.013:.012)});
  collapseStandard.position.set(.25-loss*.45,-2.68-loss*.68,1.42);poseStandard(collapseStandard,t,loss);
 }
 if(shot==='aftermath'){
  const p=smooth(t,54,58.1);cx=mix(-.7,.1,p);cy=mix(2.4,-.1,p);cz=mix(8.7,18.2,p);tx=cx;ty=cy;
  poseStandard(finalStandard,t,.94);poseInfantry(lastBearer,t,.16,'kneel',.012);
  retreaters.forEach(({u,x,y,z,i})=>{const q=Math.min(t-54,3.9);u.position.set(x-q*(.18+seed(i)*.14),y-q*.08,z);u.scale.x=-Math.abs(u.scale.x);poseInfantry(u,t,.7,'retreat',t>58?.05:1)});
  const night=smooth(t,54,60);sun.intensity=mix(1.8,.72,night);cool.intensity=.94;U.uLit.value=mix(.45,.20,night);background.material.color.setRGB(mix(.61,.35,night),mix(.65,.42,night),mix(.69,.50,night));
 }
 camera.position.set(cx,cy,cz);camera.lookAt(tx,ty,0);
 // Smoke begins after recoil/contact and does not erase the action's readable result.
 smokes.forEach(m=>{m.visible=false});flashes.forEach(f=>f.intensity=0);burst.material.opacity=0;
 const relevant=EVENTS.filter(e=>(shot==='guns'&&e.kind==='cannon')||(shot==='square'&&e.id==='square-volley')||(shot==='collapse'&&e.id==='guard-volley'));
 relevant.forEach((e,ei)=>{
  const d=t-e.t;if(d<0||d>5)return;
  const x=e.kind==='cannon'?gunModels[ei].userData.baseX+1.24:0,y=e.kind==='cannon'?gunModels[ei].position.y+1.0:1.75,z=e.kind==='cannon'?1-ei*.75:-.8;
  const flash=Math.exp(-d*38);const fl=flashes[ei];fl.position.set(x,y,z+1);fl.intensity=flash*(e.kind==='cannon'?28:58);
  if(d<.16){burst.position.set(x,y,z+.2);burst.scale.set(e.kind==='cannon'?2.2:8,e.kind==='cannon'?2.2:1.3,1);burst.material.opacity=flash*.8}
  for(let k=0;k<7;k++){
   const m=smokes[ei*7+k],delay=k*.035,s=d-delay;if(s<0)continue;
   m.visible=true;m.position.set(x+(k-3)*(e.kind==='cannon'?.18:.7)+s*.33,y+s*.20+seed(k+ei*9)*.3,z+.3+k*.035);
   m.scale.setScalar((.6+s*.8)*(e.kind==='cannon'?2.0:1.5));m.material.opacity=(1-Math.exp(-s*5))*Math.exp(-s*.77)*.76;
  }
 });
 if(shot==='pressure'||shot==='guard'||shot==='aftermath')for(let k=21;k<28;k++){
  const m=smokes[k];m.visible=true;m.position.set(-5+(k-21)*1.8+Math.sin(t*.14+k)*.3,.4+seed(k)*1.1,-2.8);m.scale.setScalar(4.2);m.material.opacity=.11;
 }
 renderer.autoClear=true;renderer.render(scene,camera);renderer.autoClear=false;renderer.clearDepth();renderer.render(vignette.s,vignette.c2);renderer.autoClear=true;
 lastState=stateAt(t);return lastState;
}
window.renderAt=(t,type='image/png',quality=.95)=>{drawAt(t);return canvas.toDataURL(type,quality)};
window.stateAt=t=>{drawAt(t);return stateAt(t)};window.__ready=true;
drawAt(0);
const audio=document.querySelector('#audio'),seek=document.querySelector('#seek'),clock=document.querySelector('#clock');let playing=false,start=0,current=0;
if(qs.has('render'))document.querySelector('#controls').style.display='none';
document.querySelector('#play').onclick=()=>{playing=!playing;if(playing){start=performance.now()/1000-current;audio.currentTime=current;audio.play()}else audio.pause();document.querySelector('#play').textContent=playing?'Ⅱ':'▶'};
seek.oninput=()=>{current=+seek.value;drawAt(current);audio.currentTime=current;start=performance.now()/1000-current;clock.textContent=current.toFixed(2)};
function tick(){if(playing){current=performance.now()/1000-start;if(current>=60){playing=false;audio.pause();current=59.999}drawAt(current);seek.value=current;clock.textContent=current.toFixed(2)}requestAnimationFrame(tick)};if(!qs.has('render'))tick();
