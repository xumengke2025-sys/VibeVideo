import * as THREE from '../vendor/three.module.js';
import {FILM,SHOTS,LOOP,P,CHUTES,HERO_CHUTE_INDEX,S_INDUCT,S_GATE,S_HERO_CHUTE,
  pathAt,loopPos,loopOff,heroS,fwd,ease,lerp,shotAt,subtitle,cartChute} from './timeline.js';
const W=FILM.width,H=FILM.height;
const renderWidth=Number(new URLSearchParams(location.search).get('width')||W),renderScale=renderWidth/W;
if(![540,1080].includes(renderWidth))throw Error('Supported render widths: 540,1080');
const canvas=document.querySelector('#scene'),overlay=document.querySelector('#overlay');
overlay.width=renderWidth;overlay.height=H*renderScale;const ctx=overlay.getContext('2d');ctx.setTransform(renderScale,0,0,renderScale,0,0);
const output=document.createElement('canvas');output.width=renderWidth;output.height=H*renderScale;const oc=output.getContext('2d');

const renderer=new THREE.WebGLRenderer({canvas,antialias:true,preserveDrawingBuffer:true});
renderer.setPixelRatio(1);renderer.setSize(renderWidth,H*renderScale,false);
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.12;
const scene=new THREE.Scene();scene.background=new THREE.Color('#eae7db');
scene.add(new THREE.HemisphereLight(0xffffff,0xa39c8c,2.15));
const sun=new THREE.DirectionalLight(0xfff3e0,3.0);sun.position.set(-18,26,14);sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.left=-42;sun.shadow.camera.right=42;sun.shadow.camera.top=42;sun.shadow.camera.bottom=-42;
sun.shadow.camera.far=180;sun.shadow.bias=-.0005;sun.shadow.normalBias=.03;scene.add(sun);
const camera=new THREE.OrthographicCamera(-5,5,9,-9,.1,320);const dir=new THREE.Vector3(1,1,1).normalize();

const mat=(c,r=.7,m=0)=>new THREE.MeshStandardMaterial({color:c,roughness:r,metalness:m});
const M={
  floor:mat('#eae7db',.95),road:mat('#8e9a99',.62,.18),leg:mat('#5d6a6c',.5,.35),
  cart:mat('#42545c',.5,.42),belt:mat('#2c3236',.86,.05),mark:mat('#c98f4a',.6,.12),
  ramp:mat('#bcc4c1',.55,.22),wall:mat('#9aa5a3',.6,.2),bin:mat('#cfc6b0',.82),slat:mat('#8b9794',.62,.18),
  gate:mat('#3d4b52',.45,.5),pal:mat('#c3a878',.85),palDark:mat('#8a7346',.85),rack:mat('#6f7c7d',.5,.3),panel:mat('#7fa8a0',.4,.3),
};
const PARCEL_COLORS=['#d3a670','#c98d5c','#e0b98a','#bfae8e','#d6b184','#c69a6a','#dcc09a','#b99a76',
  '#8fae94','#7fa3ad','#b98a86','#a8a58c'];
const parcMats=PARCEL_COLORS.map(c=>mat(c,.86));
const labelMats=['#f6f1e4','#6f97a3','#8d9a6b','#b0855f','#5f7f8c'].map(c=>mat(c,.9));
const HERO_MAT=mat('#e2704a',.72), HERO_LABEL=mat('#fff3e6',.85);

function box(parent,w,h,d,x,y,z,m,shadow=true){const q=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);q.position.set(x,y,z);q.castShadow=shadow;q.receiveShadow=shadow;parent.add(q);return q}
function cyl(parent,r,h,x,y,z,m,seg=16){const q=new THREE.Mesh(new THREE.CylinderGeometry(r,r,h,seg),m);q.position.set(x,y,z);q.castShadow=true;parent.add(q);return q}

const ground=new THREE.Mesh(new THREE.PlaneGeometry(300,300),M.floor);
ground.rotation.x=-Math.PI/2;ground.position.y=-.02;ground.receiveShadow=true;scene.add(ground);

// ---- 环路轨道与支腿 ----
const TRACK={halfW:.75,top:.50,thick:.09};
const track=new THREE.Group();scene.add(track);
const straight=2*LOOP.L,arc=Math.PI*LOOP.R,arcSeg=36;
function trackRun(s0,s1,steps){
  for(let i=0;i<steps;i++){
    const a=s0+(s1-s0)*i/steps,b=s0+(s1-s0)*(i+1)/steps,sm=(a+b)/2;
    const lp=loopPos(sm);
    const q=new THREE.Mesh(new THREE.BoxGeometry((b-a)*1.06,TRACK.thick,TRACK.halfW*2),M.road);
    q.position.set(lp.x,TRACK.top-TRACK.thick/2,lp.z);q.rotation.y=lp.yaw;
    q.castShadow=true;q.receiveShadow=true;track.add(q);
  }
}
trackRun(0,straight,2);trackRun(straight,straight+arc,arcSeg);
trackRun(straight+arc,2*straight+arc,2);trackRun(2*straight+arc,P,arcSeg);
for(let s=1.2;s<P;s+=3.1){const lp=loopPos(s);box(track,.13,TRACK.top-TRACK.thick,.13,lp.x,(TRACK.top-TRACK.thick)/2,lp.z,M.leg)}

// ---- 小车与包裹 ----
const BELT_TOP=.715, BELT_HALF=.39, CHUTE_Q0=.55, CHUTE_Q1=2.30;
const CHUTE_TOP0=.625, CHUTE_TOP1=.125;
const carts=[];
for(let i=0;i<LOOP.carts;i++){
  const g=new THREE.Group();scene.add(g);
  box(g,1.5,.14,.84,0,.57,0,M.cart);
  box(g,1.2,.075,.78,0,.6775,0,M.belt,false);
  const marks=[];
  for(let k=0;k<5;k++)marks.push(box(g,1.2,.016,.05,0,.720,-.36+k*.18,M.mark,false));
  const hero=i===0;
  const pw=(hero?.50:.40+(i%3)*.035), pd=(hero?.40:.30+(i%4)*.022), ph=(hero?.34:.24+(i%3)*.03);
  const pg=new THREE.Group();scene.add(pg);
  box(pg,pw,ph,pd,0,ph/2,0,hero?HERO_MAT:parcMats[i%parcMats.length]);
  box(pg,pw*.6,.012,pd*.55,0,ph+.006,0,hero?HERO_LABEL:labelMats[i%labelMats.length],false);
  const ch=cartChute(i), outer=ch.side>0;
  carts.push({g,marks,pg,pw,pd,ph,hero,s0:i===0?3.0:((3.0+(P/LOOP.carts)*i)%P+P)%P,
    fd:fwd(S_INDUCT,ch.s),ramp:hero?2.5:.9,slide:hero?.62:.5,chuteS:ch.s,
    side:ch.side,q1:outer?CHUTE_Q1:1.55,y1:outer?CHUTE_TOP1:CHUTE_TOP0-.36,len:(outer?CHUTE_Q1:1.55)-CHUTE_Q0});
}

// ---- 格口斜槽（外圈/内圈两侧出格）----
const chuteAnchors=[];
CHUTES.forEach((c,idx)=>{
  const outer=c.side>0, q1=outer?CHUTE_Q1:1.55, dy=outer?.50:.36;
  const len=q1-CHUTE_Q0, y1=CHUTE_TOP0-dy, sl=Math.hypot(len,dy), ang=Math.atan2(dy,len);
  const lp=loopPos(c.s),g=new THREE.Group();
  g.position.set(lp.x,0,lp.z);g.rotation.y=lp.yaw+(outer?0:Math.PI);scene.add(g);
  const midY=(CHUTE_TOP0+y1)/2-.025;
  const ramp=box(g,.95,.05,sl,0,midY,CHUTE_Q0+len/2,M.ramp);ramp.rotation.x=ang;
  for(const sx of[-1,1]){const w=box(g,.045,.15,sl,sx*.475,midY+.09,CHUTE_Q0+len/2,M.wall);w.rotation.x=ang}
  for(let k=1;k<=6;k++){const u=k/7;const r=box(g,.9,.022,.045,0,CHUTE_TOP0-dy*u+.012,CHUTE_Q0+len*u,M.slat,false);r.rotation.x=ang}
  box(g,1.0,.5,.8,0,.25,q1+.42,M.bin);
  box(g,.86,.06,.66,0,.5,q1+.42,M.palDark,false);
  const anchor=new THREE.Object3D();anchor.position.set(0,.80,q1+.42);g.add(anchor);
  chuteAnchors.push({obj:anchor,city:c.city,hero:idx===HERO_CHUTE_INDEX,s:c.s,side:c.side});
});

// ---- 环路中央：低矮线槽盖板与少量控制柜（不遮挡内圈格口）----
for(const s of[6,10,14,18,22]){
  const lp=loopPos(s,-LOOP.R),g=new THREE.Group();
  g.position.set(lp.x,0,lp.z);g.rotation.y=lp.yaw;scene.add(g);
  box(g,4.0,.14,.72,0,.07,0,M.wall,false);
}
for(const s of[8,16,20]){
  const lp=loopPos(s,-LOOP.R),g=new THREE.Group();
  g.position.set(lp.x,0,lp.z);g.rotation.y=lp.yaw;scene.add(g);
  box(g,.62,.78,.58,0,.39,0,M.cart);
  box(g,.5,.44,.035,0,.62,.30,M.panel,false);
}

// ---- 扫码门 ----
const gateG=new THREE.Group();{const lp=loopPos(S_GATE);gateG.position.set(lp.x,0,lp.z);gateG.rotation.y=lp.yaw;scene.add(gateG)}
for(const sz of[-1,1])box(gateG,.10,1.5,.10,0,1.25,sz*1.15,M.gate);
box(gateG,.13,.13,2.44,0,2.0,0,M.gate);
for(const sz of[-1,1])box(gateG,.08,.08,.08,0,1.70,sz*1.15,new THREE.MeshBasicMaterial({color:'#5d7a67'}),false);
const bandMat=new THREE.MeshBasicMaterial({color:'#ffd479',transparent:true,opacity:0,depthWrite:false});
const curtain=box(gateG,.035,1.42,2.3,0,1.24,0,new THREE.MeshBasicMaterial({color:'#cfe6dc',transparent:true,opacity:.12,depthWrite:false}),false);
const scanBand=box(gateG,.05,.085,2.3,0,.62,0,bandMat,false);

// ---- 上线站 ----
const loadG=new THREE.Group();{const lp=loopPos(S_INDUCT);loadG.position.set(lp.x,0,lp.z);loadG.rotation.y=lp.yaw;scene.add(loadG)}
box(loadG,1.4,.06,1.2,0,.95,1.4,M.ramp);cyl(loadG,.07,1.0,0,.55,2.0,M.leg);
for(const sx of[-1,1])box(loadG,.06,.32,1.2,sx*.7,1.10,1.4,M.wall);

// 画面左右边距仅约 100px（外圈斜槽、料箱与去向标签已占满），
// 不再叠加背景道具，避免被画幅裁切的半截物件。

// ---- 相机 ----
const camKeys=[[0,27.5,0],[2.4,26.5,0],[3.2,17,.5],[4.3,11,1],[5.3,9,1],[7.5,6.8,1],
  [11.2,6.2,1],[12.5,7.4,1],[15.9,10.5,1],[16.6,14,.55],[18.4,21,.12],[21.7,29,0]];
const _ca=loopPos(S_HERO_CHUTE,0),_cb=loopPos(S_HERO_CHUTE,1);
const CHUTE_OUT=new THREE.Vector3(_cb.x-_ca.x,0,_cb.z-_ca.z);
function heroWorld(t){const s=heroS(t);const lp=loopPos(s);return new THREE.Vector3(lp.x,BELT_TOP+.22,lp.z)}
function pose(t){
  let i=0;while(i<camKeys.length-2&&t>camKeys[i+1][0])i++;
  const a=camKeys[i],b=camKeys[i+1],u=ease((t-a[0])/(b[0]-a[0]));
  const span=lerp(a[1],b[1],u),follow=lerp(a[2],b[2],u);
  const h=heroWorld(t);
  const ej=t>12.9?Math.min(1,(t-12.9)/1.6):0;
  const target=new THREE.Vector3(h.x*follow+CHUTE_OUT.x*ej*1.15*follow,lerp(.7,h.y,follow),h.z*follow+CHUTE_OUT.z*ej*1.15*follow);
  return{target,span};
}

// ---- 每帧推进 ----
function update(t){
  const{target,span}=pose(t);
  camera.left=-span*W/H/2;camera.right=span*W/H/2;camera.top=span/2;camera.bottom=-span/2;
  camera.position.copy(target).addScaledVector(dir,90);camera.lookAt(target);camera.updateProjectionMatrix();
  for(const c of carts){
    const s=((c.s0+LOOP.v*t)%P+P)%P;
    const lp=loopPos(s);
    c.g.position.set(lp.x,0,lp.z);c.g.rotation.y=lp.yaw;
    const phase=fwd(S_INDUCT,s), d=c.fd-phase;
    const run=Math.max(0,Math.min(c.ramp-d,c.ramp+1.9));
    const runOff=run*.95*c.side;
    for(let k=0;k<5;k++)c.marks[k].position.z=((-.36+k*.18+runOff)%0.72+0.72)%0.72-.36;
    // 包裹：上线 → 载运 → 带面侧行 → 抛出 → 落槽
    let o=0,y=BELT_TOP;
    if(d>c.ramp)o=0;
    else if(d>0)o=.075*ease((c.ramp-d)/c.ramp);
    else{
      const tE=-d;
      if(tE<=c.slide)o=lerp(.075,CHUTE_Q0,tE/c.slide);
      else{const v2=Math.min(1,(tE-c.slide)/1.15);o=lerp(CHUTE_Q0,CHUTE_Q1,1-(1-v2)*(1-v2));}
    }
    if(o>=BELT_HALF&&o<CHUTE_Q0)y=BELT_TOP+Math.sin((o-BELT_HALF)/(CHUTE_Q0-BELT_HALF)*Math.PI)*.05;
    else if(o>=CHUTE_Q0)y=lerp(CHUTE_TOP0,c.y1,(o-CHUTE_Q0)/c.len);
    const sUse=d>0?s:c.chuteS;
    const lp2=loopOff(sUse,c.side,o);
    const sc=Math.min(1,phase/.5)*Math.min(1,Math.max(0,(c.fd+c.slide+1.15-phase)/.4));
    c.pg.position.set(lp2.x,y+.008,lp2.z);
    c.pg.rotation.y=lp2.yaw;
    c.pg.scale.setScalar(sc);
    c.pg.visible=sc>.01;
  }
  const gd=t-5.30;
  const ga=gd>-.7&&gd<.95?Math.max(0,1-Math.abs(gd-.15)/.8):0;
  curtain.material.opacity=.10+ga*.20;
  bandMat.opacity=ga;
  bandMat.color.setHex(gd<.45?0xffd479:0x9ff0c4);
  scanBand.position.y=.62+Math.min(1,Math.max(0,(gd+.35)/.9))*1.22;
  scene.updateMatrixWorld(true);renderer.render(scene,camera);drawOverlay(t);
}

// ---- 画面叠加 ----
const tmp=new THREE.Vector3();
function project(obj){obj.getWorldPosition(tmp);tmp.project(camera);return[(tmp.x+1)*W/2,(1-tmp.y)*H/2]}
function rounded(x,y,w,h,r){ctx.beginPath();ctx.roundRect(x,y,w,h,r)}
function text(s,x,y,size=42,color='#26443f',align='left',weight=500){ctx.fillStyle=color;ctx.font=`${weight} ${size}px "Microsoft YaHei", sans-serif`;ctx.textAlign=align;ctx.fillText(s,x,y)}
function drawOverlay(t){
  const{span}=pose(t),pxPerUnit=H/span;
  ctx.clearRect(0,0,W,H);
  const top=ctx.createLinearGradient(0,120,0,340);top.addColorStop(0,'#eae7dbf2');top.addColorStop(1,'#eae7db00');
  ctx.fillStyle=top;ctx.fillRect(0,0,W,340);
  const bot=ctx.createLinearGradient(0,1420,0,1560);bot.addColorStop(0,'#eae7db00');bot.addColorStop(1,'#eae7dbf5');
  ctx.fillStyle=bot;ctx.fillRect(0,1420,W,500);
  text('你的包裹，正在找路',76,168,45,'#26443f','left',600);
  text(String(SHOTS.indexOf(shotAt(t))+1).padStart(2,'0')+' / 0'+SHOTS.length,1004,168,25,'#7c8a80','right');
  ctx.strokeStyle='#ccd1c4';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(76,236);ctx.lineTo(1004,236);ctx.stroke();
  ctx.strokeStyle='#c8843f';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(76,236);ctx.lineTo(76+928*t/FILM.duration,236);ctx.stroke();
  for(const ch of chuteAnchors){
    const isHero=ch.s===S_HERO_CHUTE;
    if(isHero&&t<5.0)continue;
    const[x,y]=project(ch.obj);
    if(x<64||x>1016||y<330||y>1440)continue;
    const show=isHero&&t>=5.0;
    ctx.font='500 30px "Microsoft YaHei", sans-serif';
    const w=ctx.measureText(ch.city).width+(show?76:40);
    ctx.fillStyle=show?'#e2704aef':'#f8f7eecc';rounded(x-w/2,y-36,w,52,8);ctx.fill();
    text(ch.city,x+(show?14:0),y,30,show?'#fff6ee':'#54655c','center');
    if(show){ctx.fillStyle='#fff6ee';ctx.beginPath();ctx.moveTo(x+w/2-48,y-9);ctx.lineTo(x+w/2-33,y+2);ctx.lineTo(x+w/2-48,y+13);ctx.closePath();ctx.fill()}
  }
  if(t>=4.6&&t<=16.4){
    const a=t>=5.4?1:Math.max(0,(t-4.6)/.8);
    tmp.copy(heroWorld(t));tmp.project(camera);
    const px=(tmp.x+1)*W/2,py=(1-tmp.y)*H/2;
    if(px>30&&px<1050&&py>290&&py<1500){
      const r=Math.max(26,Math.min(118,.52*pxPerUnit));
      ctx.save();ctx.globalAlpha=a;ctx.strokeStyle='#e2704a';ctx.lineWidth=Math.max(3,Math.round(r*.09));
      for(const[sx,sy]of[[-1,-1],[1,-1],[-1,1],[1,1]]){
        ctx.beginPath();
        ctx.moveTo(px+sx*r,py+sy*r-sy*r*.45);ctx.lineTo(px+sx*r,py+sy*r);ctx.lineTo(px+sx*r-sx*r*.45,py+sy*r);
        ctx.stroke();
      }
      if(t>=5.4){
        const lw=186,ly=py-r-72;
        ctx.globalAlpha=a*Math.min(1,(t-5.4)/.35);
        ctx.fillStyle='#e2704a';rounded(px-lw/2,ly,lw,50,9);ctx.fill();
        text('去杭州',px,ly+35,29,'#fff6ee','center',600);
        ctx.beginPath();ctx.moveTo(px,ly+50);ctx.lineTo(px,py-r-8);ctx.lineWidth=3;ctx.stroke();
      }
      ctx.restore();
    }
  }
  const lines=subtitle(t);
  ctx.fillStyle='#eae7dbf5';rounded(55,1560,970,180,22);ctx.fill();
  ctx.strokeStyle='#cfd3c6';ctx.lineWidth=2;rounded(55,1560,970,180,22);ctx.stroke();
  lines.forEach((l,i)=>text(l,540,1665+i*74,62,'#26443e','center',600));
  text('交叉带分拣机 · 简化原理示意，非真实分拣计划',540,1806,24,'#7c8a80','center');
  if(t>=16.6)text('每秒，都有包裹在离开这条带子',540,1500,30,'#8a6a33','center');
}
window.DEMO=FILM;window.__ready=false;
window.__renderBuffers=()=>({logical:[W,H],scene:[canvas.width,canvas.height],overlay:[overlay.width,overlay.height],output:[output.width,output.height]});
window.renderAt=async(t,type='image/png',quality=.97)=>{t=Math.max(0,Math.min(FILM.duration-1/300,t));update(t);oc.drawImage(canvas,0,0);oc.drawImage(overlay,0,0);return output.toDataURL(type,quality)};
window.stateAt=t=>({shot:shotAt(t).id,subtitle:subtitle(t),heroArc:+heroS(t).toFixed(3),span:pose(t).span});
await document.fonts.ready;await window.renderAt(0);window.__ready=true;
const rm=location.search.includes('render');document.querySelector('#seek').max=FILM.duration-.01;
if(rm)document.querySelector('#controls').style.display='none';
else{let playing=false,last=0,t=0;const audio=new Audio('audio/mix.wav');
document.querySelector('#play').onclick=()=>{playing=!playing;if(playing){audio.currentTime=t;audio.play().catch(()=>{})}else audio.pause()};
document.querySelector('#seek').oninput=e=>{t=+e.target.value;audio.currentTime=t;update(t)};
function tick(now){if(playing){t=Math.min(FILM.duration-.01,t+(now-last)/1000);update(t);document.querySelector('#seek').value=t;document.querySelector('#clock').textContent=t.toFixed(1);if(t>=FILM.duration-.01){playing=false;audio.pause()}}last=now;requestAnimationFrame(tick)}requestAnimationFrame(tick)}
