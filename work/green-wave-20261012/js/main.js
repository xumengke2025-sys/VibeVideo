import * as THREE from '../vendor/three.module.js';
import {FILM,SHOTS,BLOCK,N_INT,zInt,isGreen,zHero,zCar2,zLead,BAND,V_DESIGN,T2_START,T2_STOP,
  clamp,ease,lerp,shotAt,subtitle} from './js/timeline.js';
const W=FILM.width,H=FILM.height;
const renderWidth=Number(new URLSearchParams(location.search).get('width')||W),renderScale=renderWidth/W;
if(![540,1080].includes(renderWidth))throw Error('Supported render widths: 540,1080');
const canvas=document.querySelector('#scene'),overlay=document.querySelector('#overlay');
overlay.width=renderWidth;overlay.height=H*renderScale;const ctx=overlay.getContext('2d');ctx.setTransform(renderScale,0,0,renderScale,0,0);
const output=document.createElement('canvas');output.width=renderWidth;output.height=H*renderScale;const oc=output.getContext('2d');

const renderer=new THREE.WebGLRenderer({canvas,antialias:true,preserveDrawingBuffer:true});
renderer.setPixelRatio(1);renderer.setSize(renderWidth,H*renderScale,false);
renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;
const scene=new THREE.Scene();
const FOG='#2b2c40';scene.fog=new THREE.Fog(FOG,42,240);
const camera=new THREE.PerspectiveCamera(48,W/H,.4,900);

// ---- 生成纹理 ----
function cvs(w,h){const c=document.createElement('canvas');c.width=w;c.height=h;return c}
function skyTexture(){
  const c=cvs(8,512),g=c.getContext('2d'),G=g.createLinearGradient(0,0,0,512);
  G.addColorStop(0,'#03050c');G.addColorStop(.34,'#0b1330');G.addColorStop(.44,'#1d2448');
  G.addColorStop(.485,'#4b4260');G.addColorStop(.505,'#8b6a5a');G.addColorStop(.53,'#3a3346');
  G.addColorStop(.62,'#141828');G.addColorStop(1,'#0a0b12');
  g.fillStyle=G;g.fillRect(0,0,8,512);
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t;
}
function windowTexture(seed){
  const w=64,h=128,c=cvs(w,h),g=c.getContext('2d');let s=seed;
  const rnd=()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296};
  g.fillStyle='#0a0d14';g.fillRect(0,0,w,h);
  const cols=6,rows=22,cw=w/cols,ch=h/rows;
  for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){
    const r=rnd();
    if(r<.30){const k=rnd();g.fillStyle=k<.68?'#ffd091':(k<.9?'#ffe9c8':'#a8dcff');g.globalAlpha=.5+.5*rnd()}
    else if(r<.46){g.fillStyle='#161d2c';g.globalAlpha=1}
    else g.globalAlpha=0;
    g.fillRect(x*cw+cw*.2,y*ch+ch*.24,cw*.62,ch*.5);
  }
  g.globalAlpha=1;
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;
  t.wrapS=t.wrapT=THREE.RepeatWrapping;return t;
}
function roadTexture(){
  const w=128,h=128,c=cvs(w,h),g=c.getContext('2d');
  g.fillStyle='#191b22';g.fillRect(0,0,w,h);
  g.fillStyle='#31343d';
  g.fillRect(4,0,3,h);g.fillRect(w-7,0,3,h);
  g.fillStyle='#d8d2c0';
  for(let y=0;y<h;y+=32)g.fillRect(w/2-1.5,y,3,16);
  g.fillStyle='#7d7a70';
  for(let y=8;y<h;y+=64){g.fillRect(w*.25-1,y,2,20);g.fillRect(w*.75-1,y,2,20)}
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;
  t.wrapS=t.wrapT=THREE.RepeatWrapping;return t;
}
function glowTexture(){
  const S=128,c=cvs(S,S),g=c.getContext('2d');
  const G=g.createRadialGradient(S/2,S/2,0,S/2,S/2,S/2);
  G.addColorStop(0,'rgba(255,255,255,1)');G.addColorStop(.18,'rgba(255,255,255,.62)');
  G.addColorStop(.45,'rgba(255,255,255,.16)');G.addColorStop(1,'rgba(255,255,255,0)');
  g.fillStyle=G;g.fillRect(0,0,S,S);
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t;
}
function bandTexture(){
  const w=8,h=256,c=cvs(w,h),g=c.getContext('2d'),G=g.createLinearGradient(0,h,0,0);
  G.addColorStop(0,'rgba(60,224,138,0)');G.addColorStop(.12,'rgba(60,224,138,.20)');
  G.addColorStop(.55,'rgba(70,235,150,.34)');G.addColorStop(.86,'rgba(140,255,190,.80)');
  G.addColorStop(.95,'rgba(220,255,235,.95)');G.addColorStop(1,'rgba(200,255,225,0)');
  g.fillStyle=G;g.fillRect(0,0,w,h);
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t;
}
const GLOW=glowTexture(),ROADTEX=roadTexture();
const sky=new THREE.Mesh(new THREE.SphereGeometry(600,24,16),new THREE.MeshBasicMaterial({map:skyTexture(),side:THREE.BackSide,fog:false}));
scene.add(sky);

const mat=(c,r=.8,m=0,extra={})=>new THREE.MeshStandardMaterial({color:c,roughness:r,metalness:m,...extra});
const M={
  road:new THREE.MeshStandardMaterial({map:ROADTEX,roughness:.42,metalness:.15,color:0xffffff}),
  walk:mat('#2a2d36',.9),kerb:mat('#3a3e48',.85),
  pole:mat('#20242c',.5,.55),head:mat('#181b21',.6,.35),
  glass:mat('#0d1420',.15,.55),tyre:mat('#0b0c10',.95),
};
function box(parent,w,h,d,x,y,z,m,shadow=true){const q=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);q.position.set(x,y,z);q.castShadow=shadow;parent.add(q);return q}
function cyl(parent,r,h,x,y,z,m,seg=12){const q=new THREE.Mesh(new THREE.CylinderGeometry(r,r,h,seg),m);q.position.set(x,y,z);parent.add(q);return q}
function spr(parent,tex,size,color,opacity,x,y,z){
  const m=new THREE.SpriteMaterial({map:tex,color,transparent:true,opacity,blending:THREE.AdditiveBlending,depthWrite:false,fog:true});
  const s=new THREE.Sprite(m);s.scale.set(size,size,1);s.position.set(x,y,z);parent.add(s);return s;
}

// ---- 地面与大道 ----
const ROAD_W=13, WALK_W=3.2, Z_FAR=-360, ROAD_LEN=Math.abs(Z_FAR-60), ROAD_MID=(Z_FAR-60)/2+30;
const ground=new THREE.Mesh(new THREE.PlaneGeometry(800,900),mat('#0c0e15',.95));
ground.rotation.x=-Math.PI/2;ground.position.set(0,-.02,-120);scene.add(ground);
ROADTEX.repeat.set(1,ROAD_LEN/8);
const road=new THREE.Mesh(new THREE.PlaneGeometry(ROAD_W,ROAD_LEN),
  new THREE.MeshStandardMaterial({map:ROADTEX,roughness:.36,metalness:.18}));
road.rotation.x=-Math.PI/2;road.position.set(0,.015,ROAD_MID);scene.add(road);
[1,-1].forEach(sx=>{
  box(scene,1.2,.22,ROAD_LEN,sx*(ROAD_W/2+.6),.11,ROAD_MID,M.kerb,false);
  box(scene,WALK_W,.24,ROAD_LEN,sx*(ROAD_W/2+.6+WALK_W/2),.12,ROAD_MID,M.walk,false);
});
// 横向街道
const crossTex=ROADTEX.clone();crossTex.needsUpdate=true;crossTex.repeat.set(1,9);
for(let i=0;i<N_INT;i++){
  const x=new THREE.Mesh(new THREE.PlaneGeometry(70,11),new THREE.MeshStandardMaterial({map:crossTex,roughness:.4,metalness:.16}));
  x.rotation.x=-Math.PI/2;x.position.set(0,.014,zInt(i));scene.add(x);
}

// ---- 信号灯 ----
const LAMP={red:0xff2f24,amber:0xffab1f,green:0x36e58a};
const signals=[];
for(let i=0;i<N_INT;i++){
  const g=new THREE.Group();g.position.set(0,0,zInt(i));scene.add(g);
  cyl(g,.14,7.2,ROAD_W/2+1.4,3.6,0,M.pole);
  box(g,.16,.16,1.9,0,7.0,0,M.pole,false);
  const arm=new THREE.Mesh(new THREE.BoxGeometry(ROAD_W/2+1.5,.16,.16),M.pole);
  arm.position.set(-(ROAD_W/4+.75),7.0,0);g.add(arm);
  cyl(g,.09,1.1,-(ROAD_W/2+1.25),6.6,0,M.pole,8);
  const head=new THREE.Group();head.position.set(-ROAD_W/2-1.0,5.9,-2.6);g.add(head);
  box(head,3.05,.86,.34,0,0,0,M.head);
  box(head,3.15,.12,.42,0,.42,0,M.head,false);
  const lamps=[];
  [['red',-0.98],['amber',0],['green',0.98]].forEach(([k,dx])=>{
    const m=new THREE.MeshStandardMaterial({color:0x0a0a0c,emissive:LAMP[k],emissiveIntensity:.05,roughness:.35});
    const l=new THREE.Mesh(new THREE.CylinderGeometry(.28,.28,.1,20),m);
    l.rotation.x=Math.PI/2;l.position.set(dx,0,.2);head.add(l);
    const gl=spr(head,GLOW,2.4,LAMP[k],0,dx,0,.42);
    lamps.push({k,m,gl});
  });
  signals.push({g,lamps,head});
}

// ---- 沿街建筑 ----
const BUILD_SEEDS=[11,23,37,53,71,89];
for(let blk=0;blk<=N_INT;blk++){
  const zHi=blk===0?14:zInt(blk-1)-7, zLo=zInt(blk)+7;
  if(zHi-zLo<6)continue;
  for(const sx of[1,-1]){
    let z=zHi,n=0;
    while(z>zLo+3){
      const d=4+((blk*7+n*5)%9), w=8+((blk*13+n*11)%7), h=9+((blk*29+n*17)%26);
      const tex=windowTexture(BUILD_SEEDS[(blk+n)%BUILD_SEEDS.length]);
      tex.repeat.set(Math.max(1,Math.round(w/7)),Math.max(1,Math.round(h/7)));
      const b=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),
        new THREE.MeshStandardMaterial({map:tex,emissive:0xffffff,emissiveMap:tex,emissiveIntensity:.9,color:0x39404e,roughness:.92}));
      b.position.set(sx*(ROAD_W/2+WALK_W+1.2+w/2),h/2,z-d/2);scene.add(b);
      z-=d+2+(n%3);n++;
    }
  }
}

// ---- 路灯（含地面光池） ----
for(let z=10;z>Z_FAR;z-=BLOCK){
  for(const sx of[1,-1]){
    const g=new THREE.Group();g.position.set(sx*(ROAD_W/2+1.1),0,z);scene.add(g);
    cyl(g,.1,6.4,0,3.2,0,M.pole,8);
    const arm=new THREE.Mesh(new THREE.BoxGeometry(1.5,.1,.1),M.pole);arm.position.set(-sx*.75,6.35,0);g.add(arm);
    const lm=new THREE.Mesh(new THREE.CylinderGeometry(.16,.24,.3,10),
      new THREE.MeshStandardMaterial({color:0x1a1a1c,emissive:0xffc27a,emissiveIntensity:1.5,roughness:.4}));
    lm.position.set(-sx*1.45,6.2,0);g.add(lm);
    spr(g,GLOW,3.4,0xffc27a,.5,-sx*1.45,6.2,0);
    const pool=new THREE.Mesh(new THREE.PlaneGeometry(6.5,9),new THREE.MeshBasicMaterial({map:GLOW,color:0xffb46a,transparent:true,opacity:.13,blending:THREE.AdditiveBlending,depthWrite:false}));
    pool.rotation.x=-Math.PI/2;pool.position.set(-sx*1.45,.05,z);scene.add(pool);
  }
}

// ---- 车辆 ----
function makeCar(body,accent,glowColor){
  const g=new THREE.Group();
  const bm=mat(body,.35,.55), gm=mat(accent,.25,.4);
  box(g,1.92,.58,4.5,0,.66,0,bm);
  box(g,1.78,.34,3.9,0,.34,0,mat('#12141a',.7,.3),false);
  box(g,1.62,.5,2.15,0,1.2,.15,gm);
  for(const sx of[1,-1])for(const sz of[1,-1]){
    const w=new THREE.Mesh(new THREE.CylinderGeometry(.33,.33,.26,14),M.tyre);
    w.rotation.z=Math.PI/2;w.position.set(sx*.98,.34,sz*1.45);g.add(w);
  }
  const hl=[];
  for(const sx of[1,-1]){
    const m=new THREE.MeshStandardMaterial({color:0x20222a,emissive:0xfff3d6,emissiveIntensity:2.6,roughness:.3});
    const l=new THREE.Mesh(new THREE.BoxGeometry(.42,.16,.1),m);l.position.set(sx*.62,.72,-2.26);g.add(l);
    spr(g,GLOW,2.6,0xffeec8,.55,sx*.62,.72,-2.4);hl.push(l);
    const tm=new THREE.MeshStandardMaterial({color:0x1a0b0b,emissive:0xff2a1e,emissiveIntensity:1.5,roughness:.35});
    const tl=new THREE.Mesh(new THREE.BoxGeometry(.4,.14,.1),tm);tl.position.set(sx*.66,.74,2.26);g.add(tl);
  }
  const pool=new THREE.Mesh(new THREE.PlaneGeometry(6.5,13),new THREE.MeshBasicMaterial({map:GLOW,color:glowColor,transparent:true,opacity:.20,blending:THREE.AdditiveBlending,depthWrite:false}));
  pool.rotation.x=-Math.PI/2;pool.position.set(0,.06,-7);g.add(pool);
  scene.add(g);return g;
}
const heroCar=makeCar('#dfe3e8','#9fb4c6',0xffeec8);
const car2=makeCar('#e26a3c','#7a3320',0xffd0a0);
const bgCars=[];
[[-3.4,-16],[3.4,-36],[-3.4,-64],[3.4,-132],[-3.4,-164],[3.4,-214]].forEach(([x,z],i)=>{
  const c=makeCar(i%2?'#49525f':'#5d5249','#2f3740',0xffca8a);
  c.position.set(x,0,z);bgCars.push({obj:c,z0:z,slow:i%3===2});
});

// ---- 绿波窗口光带 ----
const bandMat=new THREE.MeshBasicMaterial({map:bandTexture(),color:0x9dffd0,transparent:true,opacity:.9,blending:THREE.AdditiveBlending,depthWrite:false});
const band=new THREE.Mesh(new THREE.PlaneGeometry(ROAD_W,.1),bandMat);
band.rotation.x=-Math.PI/2;band.position.y=.05;scene.add(band);
const bandEdge=new THREE.Mesh(new THREE.PlaneGeometry(ROAD_W,1.6),
  new THREE.MeshBasicMaterial({map:GLOW,color:0xd6ffe8,transparent:true,opacity:.75,blending:THREE.AdditiveBlending,depthWrite:false}));
bandEdge.rotation.x=-Math.PI/2;bandEdge.position.y=.06;scene.add(bandEdge);

// ---- 相机 ----
function camPose(t){
  const pos=new THREE.Vector3(),look=new THREE.Vector3();
  if(t<5){const zh=zHero(t);pos.set(2.1,2.35,zh+13);look.set(0,1.05,zh-34)}
  else if(t<11){const u=ease((t-5)/6),zh=zHero(t);
    pos.set(2.1+6.9*u,2.35+22*u,zh+13+9*u);look.set(0,1.05-.65*u,zh-24-40*u)}
  else if(t<18){const u=ease((t-11)/2),zh=zHero(t);
    pos.set(9+7*u,24.35+18*u,zh+22+6*u);look.set(0,.4,zh-64-14*u)}
  else if(t<22.5){const z2=zCar2(t);pos.set(3.0,2.5,z2+12.5);look.set(0,.95,z2-26)}
  else{const u=ease((t-22.5)/3.5),zh=zHero(t);
    pos.set(3.0+10*u,2.6+30*u,zh+12+16*u);look.set(0,.95-.6*u,zh-26-40*u)}
  return{pos,look};
}

// ---- 每帧 ----
const LAMP_KEYS=['red','amber','green'];
function update(t){
  const {pos,look}=camPose(t);
  camera.position.copy(pos);camera.lookAt(look);
  sky.position.copy(pos);
  // 信号
  for(let i=0;i<N_INT;i++){
    const gr=isGreen(i,t);
    for(const l of signals[i].lamps){
      const on=(l.k==='green'&&gr)||(l.k==='red'&&!gr);
      l.m.emissiveIntensity=on?2.4:.04;
      l.gl.material.opacity=on?.62:0;
      l.gl.scale.setScalar(on?3.4:1);
    }
  }
  // 绿波窗口光带
  const {lead,trail}=bandAt(t);
  const mid=(lead+trail)/2;
  band.scale.y=BAND;band.position.z=mid;
  bandEdge.position.z=lead;
  bandMat.opacity=t<8?.35:.9;
  bandEdge.material.opacity=t<8?.28:.75;
  // 主角车
  heroCar.position.set(0,0,zHero(t));
  car2.position.set(0,0,zCar2(t));
  const bStop=t>=T2_STOP;
  car2.position.x=bStop?3.5:0;
  // 背景车：同向行驶并按路程循环
  for(const b of bgCars){
    let z=b.z0-V_DESIGN*t*(b.slow?.75:1);
    const span=372;
    z=-10-(((-10-z)%span+span)%span);
    b.obj.position.z=z;
    b.obj.visible=z>-330;
  }
  scene.updateMatrixWorld(true);
  renderer.render(scene,camera);drawOverlay(t);
}

// ---- 画面叠加 ----
const tmp=new THREE.Vector3();
function proj(x,y,z){tmp.set(x,y,z).project(camera);return[(tmp.x+1)*W/2,(1-tmp.y)*H/2]}
function rounded(x,y,w,h,r){ctx.beginPath();ctx.roundRect(x,y,w,h,r)}
function text(s,x,y,size=42,color='#dfe6ea',align='left',weight=500){ctx.fillStyle=color;ctx.font=`${weight} ${size}px "Microsoft YaHei", sans-serif`;ctx.textAlign=align;ctx.fillText(s,x,y)}
function drawOverlay(t){
  ctx.clearRect(0,0,W,H);
  const vg=ctx.createLinearGradient(0,0,0,H);
  vg.addColorStop(0,'rgba(3,5,12,.72)');vg.addColorStop(.28,'rgba(3,5,12,0)');
  vg.addColorStop(.7,'rgba(3,5,12,0)');vg.addColorStop(1,'rgba(3,5,12,.86)');
  ctx.fillStyle=vg;ctx.fillRect(0,0,W,H);
  text('为什么你能一路绿灯',76,168,46,'#eaf2f0','left',600);
  text(String(SHOTS.indexOf(shotAt(t))+1).padStart(2,'0')+' / 0'+SHOTS.length,1004,168,25,'#8f9aa6','right');
  ctx.strokeStyle='rgba(180,200,210,.28)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(76,236);ctx.lineTo(1004,236);ctx.stroke();
  const pg=Math.min(1,t/FILM.duration);
  const pgc=ctx.createLinearGradient(76,0,76+928*pg,0);
  pgc.addColorStop(0,'#2fbf74');pgc.addColorStop(1,'#8dffc4');
  ctx.strokeStyle=pgc;ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(76,236);ctx.lineTo(76+928*pg,236);ctx.stroke();
  // 窗口标注
  if(t>=9.5){
    const {lead,trail}=bandAt(t);
    const [lx,ly]=proj(0,1.2,trail+9);
    if(lx>60&&lx<1020&&ly>260&&ly<1520){
      const cx=clamp(lx,190,890);
      ctx.fillStyle='rgba(20,60,44,.82)';rounded(cx-155,ly-40,310,58,10);ctx.fill();
      ctx.strokeStyle='rgba(120,255,190,.55)';ctx.lineWidth=2;rounded(cx-155,ly-40,310,58,10);ctx.stroke();
      text('绿灯窗口',cx,ly,34,'#a8ffd2','center',600);
      ctx.fillStyle='rgba(20,60,44,.82)';rounded(cx-118,ly+30,236,50,9);ctx.fill();
      text('波速 = 设计车速',cx,ly+64,26,'#8ee8b8','center');
    }
  }
  // 车2 超出窗口的提示
  if(t>=18&&t<23){
    const [x,y]=proj(0,2.0,zCar2(t));
    if(y>280&&y<1480){
      const beyond=t>19.42;
      ctx.fillStyle=beyond?'rgba(90,20,20,.86)':'rgba(20,60,44,.86)';
      rounded(clamp(x,180,900)-150,y-62,300,50,9);ctx.fill();
      text(beyond?'已冲出绿灯窗口':'仍在窗口内',clamp(x,180,900),y-27,28,'#ffd9d0','center',600);
    }
  }
  const lines=subtitle(t);
  ctx.fillStyle='rgba(6,9,16,.72)';rounded(55,1560,970,180,22);ctx.fill();
  ctx.strokeStyle='rgba(150,175,190,.22)';ctx.lineWidth=2;rounded(55,1560,970,180,22);ctx.stroke();
  lines.forEach((l,i)=>text(l,540,1672+i*74,62,'#eef4f6','center',600));
  text('绿波带（信号协调控制）· 简化原理示意，路口间距与配时均为示意值，非真实路口数据',540,1806,22,'#7d8794','center');
}
window.DEMO=FILM;window.__ready=false;
window.__renderBuffers=()=>({logical:[W,H],scene:[canvas.width,canvas.height],overlay:[overlay.width,overlay.height],output:[output.width,output.height]});
window.renderAt=async(t,type='image/png',quality=.97)=>{t=clamp(t,0,FILM.duration-1/300);update(t);oc.drawImage(canvas,0,0);oc.drawImage(overlay,0,0);return output.toDataURL(type,quality)};
window.stateAt=t=>{const b=bandAt(t);return{shot:shotAt(t).id,subtitle:subtitle(t),hero:+zHero(t).toFixed(2),car2:+zCar2(t).toFixed(2),band:[+b.lead.toFixed(2),+b.trail.toFixed(2)]}};
await document.fonts.ready;await window.renderAt(0);window.__ready=true;
const rm=location.search.includes('render');document.querySelector('#seek').max=FILM.duration-.01;
if(rm)document.querySelector('#controls').style.display='none';
else{let playing=false,last=0,t=0;const audio=new Audio('audio/mix.wav');
document.querySelector('#play').onclick=()=>{playing=!playing;if(playing){audio.currentTime=t;audio.play().catch(()=>{})}else audio.pause()};
document.querySelector('#seek').oninput=e=>{t=+e.target.value;audio.currentTime=t;update(t)};
function tick(now){if(playing){t=Math.min(FILM.duration-.01,t+(now-last)/1000);update(t);document.querySelector('#seek').value=t;document.querySelector('#clock').textContent=t.toFixed(1);if(t>=FILM.duration-.01){playing=false;audio.pause()}}last=now;requestAnimationFrame(tick)}requestAnimationFrame(tick)}
