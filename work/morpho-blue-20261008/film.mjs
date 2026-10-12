import * as THREE from 'three';
const q=new URLSearchParams(location.search),W=Number(q.get('w'))||1920,H=W*9/16;
const canvas=document.getElementById('film');canvas.width=W;canvas.height=H;
const ctx=canvas.getContext('2d'),s=W/1920,clamp=(n,a=0,b=1)=>Math.min(b,Math.max(a,n));
const lerp=(a,b,p)=>a+(b-a)*p,smooth=p=>{p=clamp(p);return p*p*(3-2*p)},seg=(t,a,b)=>smooth((t-a)/(b-a));
const C={bg:'#060c15',white:'#f4f0df',blue:'#4ba9ff',cyan:'#89d8ed',muted:'#839db4',warm:'#e9b887'};
const image=async p=>{const i=new Image();i.src=p;await i.decode();return i};
const [wing,scales]=await Promise.all([image('assets/wing-concept.png'),image('assets/scales-concept.png')]);
// Use an installed Chinese typeface; await explicit load before measuring.
await document.fonts.load('40px "Microsoft YaHei"'); await document.fonts.ready;
const gl=new THREE.WebGLRenderer({antialias:true,alpha:false,preserveDrawingBuffer:true});
gl.setSize(W,H);gl.setPixelRatio(1);gl.outputColorSpace=THREE.SRGBColorSpace;
gl.toneMapping=THREE.ACESFilmicToneMapping;gl.toneMappingExposure=1.3;
const scene=new THREE.Scene();scene.background=new THREE.Color(C.bg);scene.fog=new THREE.Fog(C.bg,22,60);
scene.add(new THREE.HemisphereLight('#b8d6ed','#03101d',1.5));
const key=new THREE.DirectionalLight('#d5f1ff',3.4);key.position.set(-7,11,8);scene.add(key);
const rim=new THREE.DirectionalLight('#146af9',4.4);rim.position.set(5,3,-9);scene.add(rim);
const fill=new THREE.DirectionalLight('#4cbec6',1.3);fill.position.set(-5,1,-4);scene.add(fill);
const camera=new THREE.PerspectiveCamera(37,16/9,.05,100);
const structure=new THREE.Group();scene.add(structure);
const floor=new THREE.Mesh(new THREE.PlaneGeometry(50,26),new THREE.MeshStandardMaterial({color:'#0b1d30',roughness:.82,metalness:.08}));floor.rotation.x=-Math.PI/2;floor.position.y=-.18;scene.add(floor);
// Idealized "Christmas-tree" ridge section, not a dimensional reconstruction.
const lamellaGeometry=[];
for(let j=0;j<8;j++){
 const y=.38+j*.34,half=1.14-j*.09,shape=new THREE.Shape();
 shape.moveTo(-half,y-.035);shape.quadraticCurveTo(-half*.55,y+.025,0,y+.065);shape.quadraticCurveTo(half*.55,y+.025,half,y-.035);
 shape.lineTo(half,y+.04);shape.quadraticCurveTo(half*.55,y+.10,0,y+.14);shape.quadraticCurveTo(-half*.55,y+.10,-half,y+.04);shape.closePath();
 const g=new THREE.ExtrudeGeometry(shape,{depth:11,steps:1,bevelEnabled:true,bevelSegments:2,bevelSize:.018,bevelThickness:.018,curveSegments:8});g.translate(0,0,-5.5);lamellaGeometry.push(g);
}
const ridges=[];
const grainBytes=new Uint8Array(256*256*4);let grainSeed=713;
for(let i=0;i<256*256;i++){grainSeed=(Math.imul(grainSeed,1664525)+1013904223)>>>0;const c=90+(grainSeed>>>24)*.38;grainBytes.set([c,c,c,255],i*4)}
const grain=new THREE.DataTexture(grainBytes,256,256);grain.wrapS=grain.wrapT=THREE.RepeatWrapping;grain.repeat.set(10,26);grain.needsUpdate=true;
for(let i=-5;i<=5;i++){
 const group=new THREE.Group();group.position.set(i*2.8,0,Math.sin(i*1.9)*.15);structure.add(group);
 const mat=new THREE.MeshPhysicalMaterial({color:i===0?'#4386b5':'#276b92',metalness:.12,roughness:.46,bumpMap:grain,bumpScale:.025,clearcoat:.4,clearcoatRoughness:.27,emissive:'#075398',emissiveIntensity:.05});
 const spine=new THREE.Mesh(new THREE.BoxGeometry(.16,2.94,11),mat);spine.position.y=1.38;group.add(spine);
 lamellaGeometry.forEach(g=>group.add(new THREE.Mesh(g,mat)));
 // Thin cross-ribs make scale surfaces belong to a microstructure, not floating bars.
 for(let k=0;k<22;k++){const rib=new THREE.Mesh(new THREE.BoxGeometry(1.7,.025,.026),mat);rib.position.set(0,.19,-5.1+k*.49);group.add(rib)}
 ridges.push({group,mat,x:i*2.8});
}
const waveGeo=new THREE.BufferGeometry();waveGeo.setAttribute('position',new THREE.BufferAttribute(new Float32Array(160*3),3));
const blueField=new THREE.Line(waveGeo,new THREE.LineBasicMaterial({color:'#79caff',transparent:true,opacity:.8}));scene.add(blueField);
const rayFields=[];
for(const r of ridges){const geo=new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(r.x,2.95,0),new THREE.Vector3(r.x+1.6,7.8,0)]);const mat=new THREE.LineBasicMaterial({color:'#6ebbff',transparent:true,opacity:0});const line=new THREE.Line(geo,mat);scene.add(line);rayFields.push({line,mat,x:r.x})}
function type(txt,x,y,size=40,color=C.white,alpha=1,weight=400,align='left'){
 ctx.save();ctx.globalAlpha=clamp(alpha);ctx.font=`${weight} ${size}px "Microsoft YaHei",sans-serif`;ctx.fillStyle=color;ctx.textAlign=align;ctx.textBaseline='middle';ctx.fillText(txt,x,y);ctx.restore();
}
function line(points,color,width=3,alpha=1){ctx.save();ctx.strokeStyle=color;ctx.lineWidth=width;ctx.globalAlpha=clamp(alpha);ctx.lineCap='round';ctx.lineJoin='round';ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(...p):ctx.moveTo(...p));ctx.stroke();ctx.restore()}
function dot(x,y,r,color,alpha=1){ctx.save();ctx.globalAlpha=clamp(alpha);ctx.fillStyle=color;ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();ctx.restore()}
function cover(img,zoom=1,fx=.5,fy=.5,alpha=1){const sh=img.height/zoom,sw=sh*16/9,sx=clamp(img.width*fx-sw/2,0,Math.max(0,img.width-sw)),sy=clamp(img.height*fy-sh/2,0,img.height-sh);ctx.save();ctx.globalAlpha=alpha;ctx.drawImage(img,sx,sy,sw,sh,0,0,1920,1080);ctx.restore()}
function shade(left=.75){const g=ctx.createLinearGradient(0,0,1920,0);g.addColorStop(0,`rgba(4,10,19,${left})`);g.addColorStop(.58,'rgba(4,10,19,.08)');g.addColorStop(1,'rgba(4,10,19,.05)');ctx.fillStyle=g;ctx.fillRect(0,0,1920,1080)}
function textureEnd(){const g=ctx.createRadialGradient(960,470,200,960,470,1140);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,5,13,.36)');ctx.fillStyle=g;ctx.fillRect(0,0,1920,1080)}
function photo(t){
 if(t<7){cover(wing,lerp(1.03,1.16,seg(t,0,7)),.54,.52);shade(.73);
  type('蓝色的建筑',126,338,88,C.white,seg(t,.4,1.4)*(1-seg(t,5.6,6.5)),500);
  type('这片蓝色，藏在哪里？',132,446,37,C.white,seg(t,1.2,2.3)*(1-seg(t,5.6,6.5)));
  type('MORPHO  /  STRUCTURAL COLOUR',136,276,21,C.cyan,seg(t,.4,1.4)*(1-seg(t,5.6,6.5)));
  type('AI 概念图',1780,1008,22,C.white,.65,400,'right');
 }else if(t<14){const p=seg(t,7,14);cover(scales,lerp(1,1.28,p),.55,.54);shade(.30);
  type('鳞片上的细脊',124,151,52,C.white,seg(t,7.2,8)*(1-seg(t,12,13.3)),500);
  type('继续放大，进入一条脊线',126,221,27,C.white,seg(t,8,9)*(1-seg(t,12,13.3)));
  // The fine directional stroke persists across the material-to-geometry cut.
  const a=seg(t,10.1,11)*(1-seg(t,13.6,14));line([[690,680],[1260,353]],C.cyan,2.5,a);dot(980,514,7,C.cyan,a);
  type('AI 概念图',1780,1008,22,C.white,.65,400,'right');
 }else {cover(wing,lerp(1.16,1.03,seg(t,47,51)),.54,.52);shade(.82);
  type('蓝色，主要来自结构。',127,407,67,C.white,seg(t,47.4,48.3),500);
  type('光，在微小的层间合拍。',131,500,36,C.cyan,seg(t,48,49));
  type('多层反射的简化示意',133,901,23,C.white,seg(t,48,49)*.8);
  type('真实蝶翼还涉及衍射、无序、曲率与色素吸收',133,944,23,C.white,seg(t,48.5,49.5)*.8);
  type('AI 概念图',1780,1008,22,C.white,.65,400,'right');
 }
 textureEnd();
}
function project(v){const p=new THREE.Vector3(...v).project(camera);return [(p.x+1)*960,(1-p.y)*540]}
function anchor(txt,v,offset,alpha=1){const p=project(v),e=[p[0]+offset[0],p[1]+offset[1]];dot(...p,4,C.cyan,alpha);line([p,e,[e[0]+80,e[1]]],C.cyan,1.5,alpha*.75);type(txt,e[0]+8,e[1]-26,27,C.white,alpha)}
function structureScene(t){
 const final=t>=41;blueField.visible=final;rayFields.forEach(r=>r.line.visible=final);
 let pos,target,fov;
 if(!final){const p=seg(t,14,18.2),p2=seg(t,18.3,21.6);pos=[lerp(7.3,8.4,p)-p2*1.3,lerp(11.8,3.4,p)-p2*.45,lerp(11,7.4,p)-p2*.65];target=[0,lerp(.7,1.5,p),0];fov=lerp(42,34,p2)}
 else{const p=seg(t,41,46.6);pos=[lerp(6.7,16,p),lerp(3,14,p),lerp(7,24,p)];target=[0,1.5,0];fov=lerp(34,40,p)}
 camera.position.set(...pos);camera.fov=fov;camera.lookAt(...target);camera.updateProjectionMatrix();camera.updateMatrixWorld(true);
 ridges.forEach((r,i)=>{const center=i===5; r.group.visible=true; r.mat.color.set(center?'#4386b5':'#276b92');r.mat.emissiveIntensity=final?.06+.65*Math.exp(-Math.pow((t-42.0-(r.x+14)*.08)/.55,2)):.05;
  if(!final)r.group.scale.y=1; // Static anatomical structure; camera supplies revelation.
 });
 if(final){rayFields.forEach(r=>{r.mat.opacity=.75*seg(t,41.4+(r.x+14)*.055,42.2+(r.x+14)*.055)*(1-seg(t,45.6,47));});
  const b=waveGeo.attributes.position;for(let i=0;i<160;i++){const x=-16+i/159*32;const env=Math.sin(i/159*Math.PI);b.setXYZ(i,x,4.9+Math.sin(x*4-(t-41)*4)*.24*env,0)}b.needsUpdate=true;blueField.material.opacity=.7*seg(t,42,43)*(1-seg(t,46.2,47));
 }
 gl.render(scene,camera);ctx.drawImage(gl.domElement,0,0,1920,1080);
 if(!final){const a=seg(t,16.7,17.4)*(1-seg(t,20.7,21.8));anchor('一层层薄片',[.68,2.42,2],[96,-93],a);anchor('层间空隙',[.82,1.67,2.3],[140,77],a);
  type('脊线的内部',124,142,52,C.white,seg(t,14.3,15)*(1-seg(t,18.7,19.6)),500);
  type('理想化三维结构 · 无真实尺寸',1780,1008,22,C.muted,.8,400,'right');
 }else{type('许多细脊，共同反射蓝光',124,157,49,C.white,seg(t,43,43.7)*(1-seg(t,46,47)),500);}
 textureEnd();
}
const paths={incident:[[360,170],[790,477]],upper:[[790,477],[1337,87]],lower:[[790,477],[970,658],[1150,477],[1650,119]]};
function pathPoint(points,p){const len=points.slice(1).map((v,i)=>Math.hypot(v[0]-points[i][0],v[1]-points[i][1])),total=len.reduce((a,b)=>a+b,0);let d=clamp(p)*total;for(let i=0;i<len.length;i++){if(d<=len[i])return [lerp(points[i][0],points[i+1][0],d/len[i]),lerp(points[i][1],points[i+1][1],d/len[i])];d-=len[i]}return points.at(-1)}
function grow(points,p,color,width=4,alpha=1){const len=points.slice(1).map((v,i)=>Math.hypot(v[0]-points[i][0],v[1]-points[i][1])),total=len.reduce((a,b)=>a+b,0);let d=clamp(p)*total,ps=[points[0]];for(let i=0;i<len.length;i++){if(d>=len[i]){ps.push(points[i+1]);d-=len[i]}else{ps.push([lerp(points[i][0],points[i+1][0],d/len[i]),lerp(points[i][1],points[i+1][1],d/len[i])]);break}}line(ps,color,width,alpha)}
function pulse(points,p,col,amplitude=13){if(p<0||p>1)return;const v=pathPoint(points,p),prev=pathPoint(points,clamp(p-.006)),a=Math.atan2(v[1]-prev[1],v[0]-prev[0]);ctx.save();ctx.translate(...v);ctx.rotate(a);const gradient=ctx.createLinearGradient(-75,0,75,0);gradient.addColorStop(0,'rgba(130,210,255,0)');gradient.addColorStop(.5,col);gradient.addColorStop(1,'rgba(130,210,255,0)');const pts=[];for(let x=-75;x<=75;x+=2)pts.push([x,Math.sin(x*.15)*amplitude*Math.pow(Math.sin((x+75)/150*Math.PI),2)]);line(pts,col,4,.95);dot(0,0,5,col);ctx.restore()}
function section(t){
 const a=seg(t,22,22.6);ctx.fillStyle=C.bg;ctx.fillRect(0,0,1920,1080);
 // The sectional plates inherit real lamella silhouettes; fixed for causal reading.
 for(let j=0;j<4;j++){const y=477+j*181;ctx.save();ctx.globalAlpha=j<2?1:.18;const g=ctx.createLinearGradient(0,y,0,y+60);g.addColorStop(0,'#275776');g.addColorStop(.35,'#122d43');g.addColorStop(1,'#081725');ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(590,y);ctx.lineTo(1540,y);ctx.lineTo(1540,y+43);ctx.quadraticCurveTo(1050,y+57,590,y+43);ctx.closePath();ctx.fill();line([[590,y],[1540,y]],'#538aad',2,.8);ctx.restore()}
 type('同一束光，两段路程',124,142,50,C.white,a,500);type('只跟踪两路反射',126,212,28,C.muted,a);
 const pin=(t-23.0)/1.4,pu=(t-24.4)/2.8,d=t-24.4;
 const lengths=paths.lower.slice(1).map((v,i)=>Math.hypot(v[0]-paths.lower[i][0],v[1]-paths.lower[i][1])),total=lengths.reduce((a,b)=>a+b,0);
 const pl=(d<1.1?d/1.1*lengths[0]:d<2.2?lengths[0]+(d-1.1)/1.1*lengths[1]:lengths[0]+lengths[1]+(d-2.2)/2.56*lengths[2])/total;
 grow(paths.incident,seg(t,22.8,24.4),C.white,3.8,.82);pulse(paths.incident,pin,C.white,11);
 grow(paths.upper,clamp(pu),C.blue,3.2,.72);grow(paths.lower,clamp(pl),C.cyan,3.2,.75);
 pulse(paths.upper,pu,C.blue,12);pulse(paths.lower,pl,C.cyan,12);
 for(const [at,p] of [[24.4,paths.upper[0]],[25.5,paths.lower[1]]]){const k=t-at;if(k>=0&&k<1.4){ctx.save();ctx.strokeStyle=C.white;ctx.globalAlpha=.7*Math.exp(-k*3);ctx.lineWidth=2;ctx.beginPath();ctx.arc(...p,8+k*50,0,Math.PI*2);ctx.stroke();ctx.restore()}}
 type('上层反射',1374,164,29,C.blue,seg(t,26,27),400,'center');
 type('下层反射',1640,206,29,C.cyan,seg(t,27,28),400,'center');
 type('多走的一段路',822,779,36,C.white,seg(t,27.9,28.6)*(1-seg(t,30.7,32)));
 line([[870,574],[923,701],[1050,744]],C.cyan,1.5,seg(t,27.9,28.6)*(1-seg(t,30.7,32)));
 // A train of waves establishes phase; it does not denote a separate photon.
 if(t>28.5){const env=seg(t,28.5,29.2);for(let i=0;i<4;i++){const p=(t*.36+i*.22)%1;pulse(paths.upper,p,C.blue,8*env);pulse(paths.lower,(p-.12+1)%1,C.cyan,8*env)}}
 type('传播速度、角度与间距均为示意',1780,1008,22,C.muted,.8,400,'right');
}
function interferencePanel(t,box,phase,color,title,alpha=1,showSum=true){
 const {x,y,w,h}=box,A=h*.09,k=Math.PI*2*(phase===0?4.3:3.1)/w,omega=(t-32)*2.5;
 const ys=[y+h*.22,y+h*.43,y+h*.78],f=(px,shift)=>Math.sin(px*k-omega+shift);
 ctx.save();ctx.globalAlpha=alpha;
 type(title,x,y,34,color,1,500);
 for(let j=0;j<3;j++){line([[x+172,ys[j]],[x+w,ys[j]]],C.muted,1,.22);type(['上层','下层','叠加'][j],x+3,ys[j],26,C.muted,1);}
 for(let j=0;j<3;j++){if(j===2&&!showSum)continue;const points=[];for(let px=0;px<=w-174;px+=3){const v=j===0?f(px,0):j===1?f(px,phase):f(px,0)+f(px,phase);points.push([x+174+px,ys[j]-v*A])}line(points,j===1?C.cyan:color,j===2?4.5:3.2,j===2?1:.88)}
 if(showSum){type(Math.abs(phase)<.1?'波峰相遇，振幅变大':'相位错开，相互削弱',x+174,y+h+14,26,C.white,1)}ctx.restore();
}
function phaseScene(t){
 ctx.fillStyle=C.bg;ctx.fillRect(0,0,1920,1080);const both=seg(t,36.7,37.7);
 type('路程差，决定怎样合拍',124,139,52,C.white,seg(t,32,32.7),500);
 type('固定结构下，不同波长的相位关系不同',126,211,28,C.muted,seg(t,32.3,33));
 const box={x:lerp(260,132,both),y:330,w:lerp(1380,760,both),h:470};
 interferencePanel(t,box,0,C.blue,'蓝光 · 同相',seg(t,32.4,33),t>=34.3);
 if(t>=34.3){const a=seg(t,34.3,35)*(1-both);type('增强',1570,825,42,C.blue,a,500)}
 if(both>0)interferencePanel(t,{x:1028,y:330,w:760,h:470},Math.PI,C.warm,'另一波长 · 错位',both,t>=38.4);
 type('相位包含传播与界面反射的贡献 · 两路相干波示意',1780,1008,22,C.muted,.8,400,'right');
}
function renderAt(t){t=clamp(t,0,51.9999);ctx.setTransform(s,0,0,s,0,0);ctx.fillStyle=C.bg;ctx.fillRect(0,0,1920,1080);
 if(t<14||t>=47)photo(t);else if(t<22||t>=41)structureScene(t);else if(t<32)section(t);else phaseScene(t);
 if(t<.25){ctx.fillStyle=`rgba(6,12,21,${1-seg(t,0,.25)})`;ctx.fillRect(0,0,1920,1080)}
 document.getElementById('time').textContent=t.toFixed(2);document.getElementById('seek').value=t;
}
window.__film={ready:true,renderAt,duration:52,fps:30,quality:{engine:'Three.js WebGL + Canvas compositing',width:W,height:H,generated_assets:2,science:'idealized multilayer interference illustration',seed:'no runtime randomness',font:'Microsoft YaHei'}};
if(q.has('export'))document.getElementById('controls').style.display='none';
else{let playing=false,now=0,last=0;const audio=new Audio('soundtrack.wav');document.getElementById('play').onclick=()=>{playing=!playing;if(playing){audio.currentTime=now;audio.play()}else audio.pause()};document.getElementById('seek').oninput=e=>{now=Number(e.target.value);audio.currentTime=now;renderAt(now)};
 const tick=time=>{if(playing){now=Math.min(51.999,now+(time-last)/1000);renderAt(now);if(now>=51.999){playing=false;audio.pause()}}last=time;requestAnimationFrame(tick)};requestAnimationFrame(tick)}
renderAt(0);
