import * as THREE from 'three';

export const DURATION=32,FPS=30;
const PI=Math.PI,TAU=PI*2;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const smooth=x=>{x=clamp(x);return x*x*(3-2*x);};
const between=(t,a,b)=>smooth((t-a)/(b-a));
const mix=(a,b,x)=>a+(b-a)*x;
const ease=x=>x*x*x*(x*(6*x-15)+10);
const vec=(x,y,z)=>new THREE.Vector3(x,y,z);
let seed=62136;
const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};
const W=Number(new URLSearchParams(location.search).get('w'))||1920;
const H=Math.round(W*9/16);
const RENDER_SCALE=1.5,RW=Math.round(W*RENDER_SCALE),RH=Math.round(H*RENDER_SCALE);
const exporting=new URLSearchParams(location.search).has('export');
if(exporting)document.body.classList.add('export');

const renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,preserveDrawingBuffer:true,powerPreference:'high-performance'});
renderer.setPixelRatio(1);renderer.setSize(RW,RH,false);renderer.setClearColor(0x03070d);
document.body.prepend(renderer.domElement);
const scene=new THREE.Scene();
const camera=new THREE.PerspectiveCamera(42.6,16/9,.05,250);
const root=new THREE.Group();scene.add(root);
const surface=new THREE.Mesh(new THREE.SphereGeometry(1,96,64),new THREE.MeshBasicMaterial({color:0x020509}));root.add(surface);

// Thin disk: all particles and line filaments share one world plane.
const diskPositions=[],diskRadii=[],diskPhases=[];
for(let i=0;i<164;i++){
  const r=3.02+i*.0428;
  for(let j=0;j<512;j++){
    for(const a of [j/512*TAU,(j+1)/512*TAU]){
      diskPositions.push(r*Math.sin(a),0,r*Math.cos(a));diskRadii.push(r);diskPhases.push(a);
    }
  }
}
const diskGeometry=new THREE.BufferGeometry();
diskGeometry.setAttribute('position',new THREE.Float32BufferAttribute(diskPositions,3));
diskGeometry.setAttribute('radius',new THREE.Float32BufferAttribute(diskRadii,1));
diskGeometry.setAttribute('phase',new THREE.Float32BufferAttribute(diskPhases,1));
const diskMaterial=new THREE.ShaderMaterial({transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,uniforms:{time:{value:0},alpha:{value:1}},vertexShader:`attribute float radius;attribute float phase;varying float r;varying float a;void main(){r=radius;a=phase;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,fragmentShader:`uniform float time;uniform float alpha;varying float r;varying float a;void main(){float phase=a-time*1.8/pow(r,1.5);float s=.42+.3*sin(phase*13.+r*18.)+.18*sin(phase*29.-r*7.);float b=(.37+.55*s)*pow(3./r,1.3);vec3 c=mix(vec3(.95,.31,.06),vec3(1.,.79,.42),pow(3./r,1.8));gl_FragColor=vec4(c,b*alpha*.76);}`});
const disk=new THREE.LineSegments(diskGeometry,diskMaterial);root.add(disk);
const pp=[],pr=[],pa=[];
for(let i=0;i<4500;i++){let r=3.1+rand()*6.4,a=rand()*TAU;pp.push(r*Math.sin(a),(rand()-.5)*.038,r*Math.cos(a));pr.push(r);pa.push(a);}
const particlesGeo=new THREE.BufferGeometry();particlesGeo.setAttribute('position',new THREE.Float32BufferAttribute(pp,3));particlesGeo.setAttribute('radius',new THREE.Float32BufferAttribute(pr,1));particlesGeo.setAttribute('phase',new THREE.Float32BufferAttribute(pa,1));
const particlesMat=new THREE.ShaderMaterial({transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,uniforms:{time:{value:0},alpha:{value:1},scale:{value:W/1920}},vertexShader:`attribute float radius;attribute float phase;uniform float time;uniform float scale;varying float light;void main(){float a=phase-time*1.8/pow(radius,1.5);vec3 p=vec3(radius*sin(a),position.y,radius*cos(a));vec4 mv=modelViewMatrix*vec4(p,1.);gl_Position=projectionMatrix*mv;gl_PointSize=scale*clamp(27./(-mv.z),.5,2.3);light=.6+.4*sin(phase*18.+radius*3.);}`,fragmentShader:`uniform float alpha;varying float light;void main(){float r=length(gl_PointCoord-.5);float a=exp(-r*r*15.)*alpha*light*.8;gl_FragColor=vec4(1.,.66,.32,a);}`});
root.add(new THREE.Points(particlesGeo,particlesMat));

// The grid is explicitly an explanatory embedding, not an extra physical dimension.
const gridPos=[];
const height=(x,z)=>-.25-2.35/Math.sqrt(Math.sqrt(x*x+z*z)+.18);
for(let i=-16;i<=16;i++)for(let j=0;j<240;j++){
  const a=-18+j*.15,b=a+.15;
  for(const vertical of [true,false]){
    const x1=vertical?i*.85:a,z1=vertical?a:i*.85;
    const x2=vertical?i*.85:b,z2=vertical?b:i*.85;
    if(Math.hypot(x1,z1)<1.18||Math.hypot(x2,z2)<1.18)continue;
    gridPos.push(x1,height(x1,z1),z1,x2,height(x2,z2),z2);
  }
}
const gridGeo=new THREE.BufferGeometry();gridGeo.setAttribute('position',new THREE.Float32BufferAttribute(gridPos,3));
const gridMat=new THREE.ShaderMaterial({transparent:true,depthWrite:false,uniforms:{alpha:{value:1}},vertexShader:`varying vec3 p;void main(){p=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,fragmentShader:`uniform float alpha;varying vec3 p;void main(){float fade=1.-smoothstep(9.,19.,length(p.xz));gl_FragColor=vec4(.22,.48,.64,alpha*fade*.28);}`});
root.add(new THREE.LineSegments(gridGeo,gridMat));

// Stable fixed-seed world stars, deliberately low in visual weight.
const starP=[],starC=[];
for(let i=0;i<2400;i++){
  const y=rand()*2-1,a=rand()*TAU,r=70+rand()*90,s=Math.sqrt(1-y*y);
  starP.push(r*s*Math.cos(a),r*y,r*s*Math.sin(a));
  const b=.16+rand()*.46;starC.push(b*.75,b*.85,b);
}
const starGeo=new THREE.BufferGeometry();starGeo.setAttribute('position',new THREE.Float32BufferAttribute(starP,3));starGeo.setAttribute('color',new THREE.Float32BufferAttribute(starC,3));
const stars=new THREE.Points(starGeo,new THREE.PointsMaterial({vertexColors:true,size:.095,transparent:true,opacity:.75,sizeAttenuation:true,depthWrite:false}));scene.add(stars);

// Integrate the Schwarzschild photon orbit in a plane, in affine parameter.
// r'' vector = -(3/2) rs L² r-vector / r^5, with rs=1. Initial camera mapping is approximate.
function trajectory(eye,dir){
  let p=eye.clone(),v=dir.clone();const angular=p.clone().cross(v).lengthSq(),points=[p.clone()];
  const acceleration=q=>q.clone().multiplyScalar(-1.5*angular/Math.pow(q.length(),5));
  for(let i=0;i<1600;i++){
    const r=p.length();if(r<1.015||r>60)break;
    const dt=clamp(r*.012,.008,.28),a=acceleration(p),n=p.clone().addScaledVector(v,dt).addScaledVector(a,.5*dt*dt),nv=v.clone().addScaledVector(a,dt*.5).addScaledVector(acceleration(n),dt*.5);
    if(p.y*n.y<0){const hit=p.clone().lerp(n,Math.abs(p.y)/(Math.abs(p.y)+Math.abs(n.y)));const hr=Math.hypot(hit.x,hit.z);if(hr>3.05&&hr<9.3){points.push(hit);return {points,hit};}}
    points.push(n.clone());p=n;v=nv;
  }
  return null;
}
const referenceEye=vec(0,4.2,23),referenceLook=vec(0,0,0),forward=referenceLook.clone().sub(referenceEye).normalize(),right=forward.clone().cross(vec(0,1,0)).normalize(),up=right.clone().cross(forward);
const candidates=[];
for(let x=-.22;x<=.221;x+=.025)for(let y=.04;y<=.701;y+=.008){
  const d=forward.clone().addScaledVector(right,.39*x).addScaledVector(up,.39*y).normalize();
  const path=trajectory(referenceEye,d);
  if(path&&path.hit.z<-3&&Math.abs(path.hit.x)<3.8)candidates.push({x,y,...path});
}
if(!candidates.length)throw new Error('No rear-disk photon path found');
candidates.sort((a,b)=>Math.abs(a.hit.z+5.5)+Math.abs(a.hit.x-1.3)-Math.abs(b.hit.z+5.5)-Math.abs(b.hit.x-1.3));
const selected=candidates[0],fullRay=selected.points.slice().reverse();
const receiverIndex=fullRay.findIndex(p=>p.z>12);
const rayPoints=fullRay.slice(0,receiverIndex+1),receiverPosition=rayPoints.at(-1);
const rayCurve=new THREE.CatmullRomCurve3(rayPoints,false,'centripetal');
const sampled=rayCurve.getSpacedPoints(360);
const rayGeo=new THREE.BufferGeometry().setFromPoints(sampled);
const rayMat=new THREE.LineBasicMaterial({color:0xffc279,transparent:true,opacity:1});
const ray=new THREE.Line(rayGeo,rayMat);root.add(ray);
const tubeGeometry=new THREE.TubeGeometry(rayCurve,360,.018,6,false);
const tubeMat=new THREE.MeshBasicMaterial({color:0xffb75e,transparent:true,opacity:.56,depthWrite:false});
const rayTube=new THREE.Mesh(tubeGeometry,tubeMat);root.add(rayTube);
const ghostGroup=new THREE.Group();root.add(ghostGroup);
for(let i=0;i<5;i++){
  const candidate=candidates[Math.floor((i+.5)/5*candidates.length)];
  const g=new THREE.BufferGeometry().setFromPoints(candidate.points);
  ghostGroup.add(new THREE.Line(g,new THREE.LineBasicMaterial({color:0x72b8d9,transparent:true,opacity:.19,depthWrite:false})));
}

const glowCanvas=document.createElement('canvas');glowCanvas.width=glowCanvas.height=128;
const gc=glowCanvas.getContext('2d'),gr=gc.createRadialGradient(64,64,1,64,64,64);gr.addColorStop(0,'#ffffff');gr.addColorStop(.08,'#fff0c1');gr.addColorStop(.19,'#ffc278');gr.addColorStop(.45,'#ff831c44');gr.addColorStop(1,'#ff831c00');gc.fillStyle=gr;gc.fillRect(0,0,128,128);
const glowTexture=new THREE.CanvasTexture(glowCanvas);
const photon=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTexture,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending}));photon.scale.setScalar(.75);root.add(photon);
const source=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTexture,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending}));source.position.copy(selected.hit);source.scale.setScalar(.65);root.add(source);
const receiver=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTexture,color:0x8ed8ff,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending}));receiver.position.copy(receiverPosition);receiver.scale.setScalar(.42);root.add(receiver);

const lensScene=new THREE.Scene(),lensCamera=new THREE.Camera();
const lensFragment=await (await fetch('/lens.frag')).text();
const lensUniforms={resolution:{value:new THREE.Vector2(RW,RH)},eye:{value:vec(0,4.2,23)},look:{value:vec(0,0,0)},time:{value:0},bend:{value:1},imageAlpha:{value:1},diskGain:{value:1}};
const lensMaterial=new THREE.ShaderMaterial({transparent:true,depthTest:false,depthWrite:false,uniforms:lensUniforms,vertexShader:'varying vec2 vUv;void main(){vUv=uv;gl_Position=vec4(position.xy,0.,1.);}',fragmentShader:lensFragment});
lensScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2,2),lensMaterial));

const typeCanvas=document.getElementById('type');typeCanvas.width=W;typeCanvas.height=H;const ctx=typeCanvas.getContext('2d');
const fonts={zh:'"Microsoft YaHei", "Noto Sans SC", sans-serif',en:'Bahnschrift, "Segoe UI", sans-serif'};
await document.fonts.ready;
function text(s,x,y,size,color='#e3e8ee',weight=400,align='left',family=fonts.zh){ctx.font=`${weight} ${size}px ${family}`;ctx.textAlign=align;ctx.fillStyle=color;ctx.fillText(s,x,y);}
function opacity(a,fn){if(a<.002)return;ctx.save();ctx.globalAlpha=a;fn();ctx.restore();}
function block(t,start,end,fn){let a=between(t,start,start+.45)*(1-between(t,end-.45,end));opacity(a,fn);}
function label(position,title,subtitle,dx,dy,a=1){
  let p=position.clone().project(camera);if(p.z>1||p.z<-1)return;
  const x=(p.x*.5+.5)*1920,y=(.5-p.y*.5)*1080;
  const tx=x+dx,ty=y+dy;
  if(tx<80||tx>1800||ty<140||ty>875)return;
  opacity(a,()=>{ctx.strokeStyle='#b9d7e766';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(tx-12,ty-9);ctx.lineTo(tx+156,ty-9);ctx.stroke();ctx.fillStyle='#bddbec';ctx.beginPath();ctx.arc(x,y,2.2,0,TAU);ctx.fill();text(title,tx,ty+25,25,'#d7e6ee',500);if(subtitle)text(subtitle,tx,ty+53,17,'#a0b6c4',400,'left',fonts.en);});
}
function cameraState(t){
  if(t<4){const a=mix(.23,.14,between(t,0,4));return vec(Math.sin(a)*19,3.2+between(t,0,4)*.5,Math.cos(a)*19);}
  if(t<8){const x=ease(clamp((t-4)/4));return vec(mix(2.65,10,x),mix(3.7,16,x),mix(18.8,20,x));}
  if(t<14){const x=ease(clamp((t-8)/6));return vec(mix(10,0,x),mix(16,4.2,x),mix(20,23,x));}
  if(t<20){const x=ease(clamp((t-14)/6));return vec(mix(0,-3.4,x),mix(4.2,4.0,x),mix(23,20.5,x));}
  if(t<26){const x=clamp((t-20)/6);const y=4+Math.sin(PI*x)**2*12;return vec(-3.4+Math.sin(PI*x)*3,y,20.5);}
  const x=between(t,26,30);return vec(mix(-3.4,-2.5,x),mix(4,3.5,x),mix(20.5,18.6,x));
}
function typography(t){
  ctx.clearRect(0,0,W,H);ctx.save();ctx.scale(W/1920,H/1080);
  // Quiet gradients give type stable contrast without panels or floating cards.
  const top=ctx.createLinearGradient(0,0,0,180);top.addColorStop(0,'#02070bb3');top.addColorStop(1,'#02070b00');ctx.fillStyle=top;ctx.fillRect(0,0,1920,180);
  const bottom=ctx.createLinearGradient(0,730,0,1080);bottom.addColorStop(0,'#02070b00');bottom.addColorStop(1,'#02070bcc');ctx.fillStyle=bottom;ctx.fillRect(0,730,1920,350);
  text('光的路径',106,90,25,'#d4dde5',500);text('GRAVITATIONAL LENSING',1814,89,18,'#9bafc0',400,'right',fonts.en);
  ctx.strokeStyle='#8da2b52c';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(106,113);ctx.lineTo(1814,113);ctx.stroke();
  block(t,-.45,4.2,()=>{text('黑洞背后的光，',106,861,60,'#edf0ef',600);text('你也看得见。',106,941,60,'#ffce91',600);});
  block(t,4.4,8.2,()=>{text('发光的是周围的热气体',106,930,48,'#e8edf0',500);text('它们围成一个旋转的吸积盘。',108,990,28,'#aabcc9');});
  block(t,8.3,13.8,()=>{text('跟着这一束光',106,930,50,'#ffce91',600);text('它从背面出发，沿弯曲的路径抵达观察者。',108,990,28,'#bdcbd4');});
  block(t,14.1,20.0,()=>{text('背面的光，出现在上方',106,930,48,'#e8edf0',500);text('引力透镜改变了我们看到的形状。',108,990,28,'#bdcbd4');});
  block(t,13.65,15.9,()=>{text('沿光路，重建视野',108,157,21,'#8ea9bb');});
  block(t,20.1,26.0,()=>{text('换个角度，亮弧也会改变',106,930,48,'#e8edf0',500);text('光源仍是同一个盘；变化的是光抵达眼睛的路径。',108,990,28,'#bdcbd4');});
  opacity(between(t,26.15,26.8),()=>{text('引力改写光的路径',106,875,58,'#edf0ef',600);text('也改写了你看见的宇宙。',108,953,42,'#ffce91',500);});
  text('非旋转黑洞 · 科学示意',1814,1032,19,'#7e94a5',400,'right');
  if(t>5.5&&t<13.5){let a=between(t,5.5,6.3)*(1-between(t,12.7,13.5));label(vec(6.1,0,-2),'吸积盘','ACCRETION DISK',120,-60,a);label(vec(0,0,0),'黑洞','BLACK HOLE',70,75,a);}
  if(t>9&&t<13.3)label(selected.hit,'背面光源','FAR SIDE',-215,-95,between(t,9,9.5)*(1-between(t,12.5,13.3)));
  if(t>9.7&&t<13.3)label(receiverPosition,'观察方向','TO THE OBSERVER',-275,-15,between(t,9.7,10.2)*(1-between(t,12.7,13.3)));
  if(t>15.7&&t<19.7){opacity(between(t,15.7,16.2)*(1-between(t,19.1,19.7)),()=>{ctx.strokeStyle='#ffce9166';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(995,276);ctx.lineTo(1170,260);ctx.lineTo(1450,260);ctx.stroke();text('背面盘面的像',1190,242,27,'#ffce91',500);});}
  ctx.restore();
}
function renderAt(seconds){
  const t=clamp(seconds,0,DURATION-1/FPS);
  const lensAlpha=t<5.55?1-between(t,5.0,5.55):between(t,13.7,14.4);
  const diagramAlpha=1-lensAlpha;
  camera.position.copy(cameraState(t));camera.lookAt(0,0,0);camera.updateMatrixWorld();
  diskMaterial.uniforms.time.value=t;diskMaterial.uniforms.alpha.value=diagramAlpha;
  particlesMat.uniforms.time.value=t;particlesMat.uniforms.alpha.value=diagramAlpha;
  gridMat.uniforms.alpha.value=diagramAlpha*between(t,5,7);
  const rayAlpha=between(t,7.9,8.5)*(1-between(t,13.4,14.7));
  const progress=between(t,8.5,12.7);
  rayMat.opacity=rayAlpha*.8;rayGeo.setDrawRange(0,Math.max(2,Math.round(progress*360)));
  tubeMat.opacity=rayAlpha*.35;rayTube.geometry.setDrawRange(0,Math.max(0,Math.floor(progress*360)*6*6));
  photon.position.copy(rayCurve.getPointAt(clamp(progress,.0001,.9999)));photon.material.opacity=rayAlpha*(1-between(t,12.75,13.3));
  photon.scale.setScalar(.60+.07*Math.sin(t*7));source.material.opacity=rayAlpha*.7;receiver.material.opacity=rayAlpha*(.15+.55*progress);
  ghostGroup.visible=rayAlpha>.001;for(const child of ghostGroup.children)child.material.opacity=rayAlpha*.075;
  root.visible=diagramAlpha>.001;stars.material.opacity=.68*diagramAlpha;
  renderer.autoClear=true;renderer.render(scene,camera);
  lensUniforms.eye.value.copy(camera.position);lensUniforms.look.value.set(0,0,0);lensUniforms.time.value=t;lensUniforms.imageAlpha.value=lensAlpha;
  // Optical reconstruction transition, not a claim that real gravity turns on/off.
  lensUniforms.bend.value=t<5.55?1-between(t,4.0,5.0):between(t,14.4,15.6);
  if(lensAlpha>.001){renderer.autoClear=false;renderer.render(lensScene,lensCamera);renderer.autoClear=true;}
  typography(t);
  document.getElementById('seek').value=t;
  document.getElementById('time').textContent=`00:${String(Math.floor(t)).padStart(2,'0')}`;
  return {t,lensAlpha,diagramAlpha,eye:camera.position.toArray(),photon:photon.position.toArray()};
}
const quality={width:W,height:H,render_size:[RW,RH],supersample_scale:RENDER_SCALE,webgl:renderer.getContext().getParameter(renderer.getContext().RENDERER),photon_source:selected.hit.toArray(),observer_direction_marker:receiverPosition.toArray(),minimum_path_radius:Math.min(...rayPoints.map(p=>p.length())),path_points:rayPoints.length,world_eye:referenceEye.toArray(),fonts:fonts};
window.__film={ready:true,renderAt,duration:DURATION,fps:FPS,quality};
renderAt(0);
let playing=false,epoch=0,offset=0,audio;
function tick(now){if(!playing)return;const t=offset+(now-epoch)/1000;if(t>=DURATION){playing=false;document.getElementById('play').textContent='播放';if(audio)audio.pause();return;}renderAt(t);requestAnimationFrame(tick);}
document.getElementById('play').onclick=()=>{playing=!playing;document.getElementById('play').textContent=playing?'暂停':'播放';if(playing){offset=Number(document.getElementById('seek').value);if(offset>31.8)offset=0;epoch=performance.now();if(!audio)audio=new Audio('/soundtrack.wav');audio.currentTime=offset;audio.play().catch(()=>{});requestAnimationFrame(tick);}else if(audio)audio.pause();};
document.getElementById('seek').oninput=e=>{offset=Number(e.target.value);epoch=performance.now();renderAt(offset);if(audio)audio.currentTime=offset;};
