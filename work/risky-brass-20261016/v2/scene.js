import * as T from 'three';
import {HDRLoader} from './vendor/HDRLoader.js';
import {RoundedBoxGeometry} from './vendor/RoundedBoxGeometry.js';

await document.fonts.load('400 40px "Microsoft YaHei"');
const Q=new URLSearchParams(location.search),W=+(Q.get('width')||1920),H=Math.round(W*9/16),TAU=2*Math.PI;
const renderer=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true,powerPreference:'high-performance'});
renderer.setSize(W,H);renderer.setPixelRatio(1);renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;
renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.02;
const canvas=document.createElement('canvas');canvas.width=W;canvas.height=H;document.body.appendChild(canvas);const ctx=canvas.getContext('2d');
const scene=new T.Scene();scene.background=new T.Color('#242b2c');scene.fog=new T.FogExp2('#242b2c',.004);
const camera=new T.PerspectiveCamera(37,W/H,.1,250);
const hdr=await new HDRLoader().loadAsync('./assets/brown_photostudio_02_1k.hdr');
const pm=new T.PMREMGenerator(renderer);scene.environment=pm.fromEquirectangular(hdr).texture;hdr.dispose();pm.dispose();scene.environmentIntensity=.72;scene.environmentRotation.y=.7;
scene.add(new T.HemisphereLight(0xc8d4da,0x342317,.8));
const sunlight=new T.DirectionalLight(0xffe5bf,3.6);sunlight.position.set(-12,19,11);sunlight.target.position.set(5,0,-3);sunlight.castShadow=true;sunlight.shadow.mapSize.set(4096,4096);Object.assign(sunlight.shadow.camera,{left:-38,right:38,top:28,bottom:-28,near:1,far:95});sunlight.shadow.normalBias=.012;sunlight.shadow.bias=-.00008;sunlight.shadow.radius=3;scene.add(sunlight,sunlight.target);
const fill=new T.DirectionalLight(0xb4cad8,1.05);fill.position.set(15,10,-15);scene.add(fill);
const rim=new T.DirectionalLight(0xffcf87,.8);rim.position.set(8,5,-9);scene.add(rim);
const loader=new T.TextureLoader();const woodMap=await loader.loadAsync('./assets/dark_wood_diff_1k.jpg');woodMap.colorSpace=T.SRGBColorSpace;woodMap.wrapS=woodMap.wrapT=T.RepeatWrapping;woodMap.repeat.set(1.25,.65);woodMap.anisotropy=16;
const woodNormal=await loader.loadAsync('./assets/dark_wood_nor_gl_1k.jpg');woodNormal.wrapS=woodNormal.wrapT=T.RepeatWrapping;woodNormal.repeat.copy(woodMap.repeat);woodNormal.anisotropy=16;
let seed=171;const rand=()=>{seed=(1664525*seed+1013904223)>>>0;return seed/4294967296;};
function grain(){const c=document.createElement('canvas');c.width=c.height=512;const x=c.getContext('2d');x.fillStyle='#c4c4c4';x.fillRect(0,0,512,512);for(let j=0;j<3000;j++){const v=160+rand()*55;x.strokeStyle=`rgba(${v},${v},${v},.15)`;x.lineWidth=.25+rand()*.4;const y=rand()*512;x.beginPath();x.moveTo(0,y);x.lineTo(512,y+.3*rand());x.stroke();}const t=new T.CanvasTexture(c);t.wrapS=t.wrapT=T.RepeatWrapping;return t;}
const brushed=grain();const standard=(color,metalness,roughness,other={})=>new T.MeshStandardMaterial({color,metalness,roughness,...other});
const M={brass:standard('#b79a60',.91,.29,{bumpMap:brushed,bumpScale:.002}),polish:standard('#d3b77b',.95,.24),satin:standard('#9e8856',.83,.35),dark:standard('#1a2422',.42,.3),ebony:standard('#17211d',.13,.35),wood:standard('#716554',.02,.64,{map:woodMap,normalMap:woodNormal,normalScale:new T.Vector2(.13,.13)}),steel:standard('#8e9799',.96,.23),blue:standard('#172d36',.88,.22),ivory:standard('#e2d8bd',.03,.59),paper:standard('#ded3b5',.02,.72),ink:standard('#342a1e',.1,.52),red:standard('#964b3b',.12,.47),sage:standard('#6c8065',.2,.42),amber:standard('#bc8e36',.42,.36),glass:new T.MeshPhysicalMaterial({color:'#bdd3d0',transmission:.96,thickness:.045,roughness:.08,metalness:0,ior:1.48,transparent:true,opacity:.25,depthWrite:false})};
const cached=new Map();const geom=(key,fn)=>{if(!cached.has(key))cached.set(key,fn());return cached.get(key);};let partCount=0;
function mesh(g,m,p=[0,0,0],parent=scene){const o=new T.Mesh(g,m);o.position.set(...p);o.castShadow=true;o.receiveShadow=true;parent.add(o);partCount++;return o;}
function group(p=[0,0,0],parent=scene){const o=new T.Group();o.position.set(...p);parent.add(o);return o;}
function box(w,h,d,m,p,parent=scene,r=.035){return mesh(geom(`box${w}/${h}/${d}/${r}`,()=>new RoundedBoxGeometry(w,h,d,3,Math.min(r,w/3,h/3,d/3))),m,p,parent);}
function cyl(r,h,m,p,parent=scene,top=r,n=48){return mesh(geom(`c${r}/${h}/${top}/${n}`,()=>new T.CylinderGeometry(top,r,h,n)),m,p,parent);}
function sphere(r,m,p,parent=scene){return mesh(geom(`s${r}`,()=>new T.SphereGeometry(r,24,16)),m,p,parent);}
function bar(a,b,r,m,parent=scene){const A=new T.Vector3(...a),B=new T.Vector3(...b),D=B.clone().sub(A);const o=cyl(r,D.length(),m,A.add(B).multiplyScalar(.5).toArray(),parent);o.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),D.normalize());return o;}
function ring(r,t,m,p,parent=scene,rot=[Math.PI/2,0,0]){const o=mesh(geom(`t${r}/${t}`,()=>new T.TorusGeometry(r,t,8,64)),m,p,parent);o.rotation.set(...rot);return o;}
function tube(points,r,m,parent=scene){const curve=new T.CatmullRomCurve3(points.map(v=>new T.Vector3(...v)),false,'centripetal');return mesh(new T.TubeGeometry(curve,Math.max(24,points.length*10),r,8,false),m,[0,0,0],parent);}
function turned(p,h,r,parent=scene){const profile=[[1,0],[1,.06],[.88,.1],[.65,.18],[.56,.26],[.52,.67],[.57,.76],[.7,.86],[.85,.92],[.85,1]].map(([a,b])=>new T.Vector2(a*r,b*h));const o=mesh(geom(`l${h}/${r}`,()=>new T.LatheGeometry(profile,48)),M.brass,p,parent);return o;}
function screw(x,y,z,parent=scene,s=1){cyl(.057*s,.04*s,M.polish,[x,y,z],parent,.057*s,20);box(.069*s,.005,.009*s,M.ink,[x,y+.021*s,z],parent,.001);}
function frontScrew(x,y,z,parent=scene,s=1){const o=group([x,y,z],parent);o.rotation.x=Math.PI/2;screw(0,0,0,o,s);}
function engravingTexture(lines,width=1024,height=256){const c=document.createElement('canvas');c.width=width;c.height=height;const x=c.getContext('2d');x.clearRect(0,0,width,height);x.strokeStyle='#624a2d';x.lineWidth=2;x.strokeRect(12,12,width-24,height-24);x.strokeRect(19,19,width-38,height-38);x.textAlign='center';x.textBaseline='middle';lines.forEach((s,i)=>{let size=height*(lines.length===1?.57:i?.28:.35);x.font=`${size}px "Microsoft YaHei",Georgia,serif`;size*=Math.min(1,(width-160)/x.measureText(s).width);x.font=`${size}px "Microsoft YaHei",Georgia,serif`;x.fillStyle='#30291e';x.fillText(s,width/2,height*(lines.length===1?.51:.34+i*.36));});const tex=new T.CanvasTexture(c);tex.colorSpace=T.SRGBColorSpace;tex.anisotropy=16;return tex;}
function label(s,w,h,p,parent=scene,material=M.ivory,top=false){const o=group(p,parent);if(top)o.rotation.x=-Math.PI/2;box(w,h,.025,material,[0,0,0],o,.025);const tex=engravingTexture(Array.isArray(s)?s:[s],1024,Math.max(160,Math.round(1024*h/w)));const face=mesh(new T.PlaneGeometry(w*.97,h*.93),new T.MeshStandardMaterial({map:tex,transparent:true,depthWrite:false,roughness:.7,metalness:.02}),[0,0,.016],o);face.castShadow=false;for(const x of [-w/2+.06,w/2-.06])frontScrew(x,0,.028,o,.53);return o;}
function base(w,d,parent){box(w,.18,d,M.wood,[0,.18,0],parent,.11);box(w-.1,.025,d-.1,M.polish,[0,.285,0],parent,.06);box(w-.16,.12,d-.16,M.wood,[0,.36,0],parent,.055);for(const z of [-d/2+.1,d/2-.1])box(w-.22,.012,.014,M.polish,[0,.43,z],parent,.002);for(const x of [-w/2+.25,w/2-.25])for(const z of [-d/2+.25,d/2-.25]){turned([x,-.02,z],.13,.15,parent);screw(x,.44,z,parent,.7);}return .44;}
function gear(r,n,p,parent=scene,depth=.105){const o=group(p,parent),shape=new T.Shape();for(let j=0;j<n*4;j++){const a=j/(n*4)*TAU,R=r*[.91,1,1,.91][j%4],x=R*Math.cos(a),y=R*Math.sin(a);if(j)shape.lineTo(x,y);else shape.moveTo(x,y);}shape.closePath();const center=new T.Path();center.absarc(0,0,r*.12,0,TAU,true);shape.holes.push(center);for(let j=0;j<6;j++){const a=j*TAU/6+.12,b=(j+1)*TAU/6-.12,h=new T.Path();h.absarc(0,0,r*.75,b,a,true);h.lineTo(r*.3*Math.cos(a),r*.3*Math.sin(a));h.absarc(0,0,r*.3,a,b,false);h.closePath();shape.holes.push(h);}mesh(geom(`gear${r}/${n}/${depth}`,()=>new T.ExtrudeGeometry(shape,{depth,steps:1,bevelEnabled:true,bevelThickness:.008,bevelSize:.008,bevelSegments:2})),M.brass,[0,0,-depth/2],o);for(const R of [.80,.85])ring(r*R,.006,M.polish,[0,0,depth/2+.008],o,[0,0,0]);const hub=cyl(r*.19,depth*1.8,M.polish,[0,0,0],o);hub.rotation.x=Math.PI/2;return o;}
function supportedAxle(a,b,r,parent){bar(a,b,r,M.steel,parent);for(const P of [a,b]){const g=group(P,parent);const dir=new T.Vector3(...b).sub(new T.Vector3(...a)).normalize();g.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),dir);cyl(r*2.2,.18,M.brass,[0,0,0],g);ring(r*1.7,.016,M.polish,[0,.1,0],g);}}
const deck=group();box(59,.24,26,M.wood,[-3.5,-.25,-2],deck,.18);box(58.85,.025,25.85,M.polish,[-3.5,-.111,-2],deck,.1);box(58.7,.055,25.7,standard('#27312e',.08,.71),[-3.5,-.07,-2],deck,.1);
const ground=mesh(new T.PlaneGeometry(400,400),standard('#2d3433',.12,.38),[0,-.51,0]);ground.rotation.x=-Math.PI/2;ground.castShadow=false;
// Architectural background: walnut cabinets and sparse scientific instruments, real geometry.
const archive=group([-6,0,-10]);
for(let i=0;i<9;i++){const a=(i-4)*.13,g=group([i*1.25-5,0,.08*(i-4)**2],archive);g.rotation.y=-a;box(1.20,3.8,.7,M.wood,[0,2.1,0],g,.06);box(1.28,.12,.87,M.wood,[0,4.04,0],g,.05);for(let j=0;j<5;j++){box(1.05,.59,.06,M.wood,[0,.7+j*.66,.385],g,.018);label(`${i+1} / ${j+1}`,.39,.13,[0,.7+j*.66,.424],g,M.brass);bar([-.15,.60+j*.66,.47],[.15,.60+j*.66,.47],.018,M.polish,g);}for(const dx of [-.56,.56]){box(.035,3.5,.03,M.polish,[dx,2.1,.39],g,.005);}}
// Main input bridge: guide shafts, saddles, driven screw, attached cross ties.
const inputCurve=new T.LineCurve3(new T.Vector3(-8,1.18,0),new T.Vector3(0,1.18,0));
function rail(curve,width=.74,parent=scene){const edges=[-1,1].map(sign=>{const points=[];for(let i=0;i<=100;i++){const u=i/100,P=curve.getPoint(u),D=curve.getTangent(u),N=new T.Vector3(-D.z,0,D.x).normalize();points.push(P.addScaledVector(N,width*sign));}return points;});for(const q of edges)mesh(new T.TubeGeometry(new T.CatmullRomCurve3(q),150,.06,10,false),M.polish,[0,0,0],parent);for(let u=0;u<=1.001;u+=.13){const P=curve.getPoint(Math.min(1,u)),D=curve.getTangent(Math.min(1,u)),N=new T.Vector3(-D.z,0,D.x).normalize();const a=P.clone().addScaledVector(N,width+.12),b=P.clone().addScaledVector(N,-width-.12);bar(a.toArray(),b.toArray(),.045,M.satin,parent);turned([P.x,.03,P.z],Math.max(.1,P.y-.08),.135,parent);cyl(.18,.05,M.brass,[P.x,.08,P.z],parent);}}

const lead=group([-4,1.05,0]);bar([-4,0,0],[4,0,0],.065,M.blue,lead);const helix=[];for(let i=0;i<=900;i++){const a=i/900*TAU*40;helix.push(new T.Vector3(-4+8*i/900,.091*Math.cos(a),.091*Math.sin(a)));}mesh(new T.TubeGeometry(new T.CatmullRomCurve3(helix),900,.018,5,false),M.steel,[0,0,0],lead);for(const x of [-8,0]){box(.4,.22,.4,M.dark,[x,.96,0]);supportedAxle([x-.12,1.05,0],[x+.12,1.05,0],.075,scene);}
const driveGear=gear(.49,24,[-7.5,1.05,.4]);const pairedGear=gear(.325,16,[-6.712,1.05,.4]);for(const x of [-7.5,-6.712]){bar([x,.08,.08],[x,1.05,.08],.06,M.brass);supportedAxle([x,1.05,.07],[x,1.05,.55],.055,scene);}
// The single case is rigidly attached to a guide carriage; copies retain A17 identity.
function casework(parent=scene,small=1){const o=group([0,0,0],parent);o.scale.setScalar(small);box(1.42,.17,1.26,M.satin,[0,0,0],o,.045);for(const z of [-.74,.74]){const tubeO=cyl(.12,.9,M.brass,[0,-.17,z],o);tubeO.rotation.z=Math.PI/2;ring(.13,.015,M.polish,[-.4,-.17,z],o,[0,Math.PI/2,0]);ring(.13,.015,M.polish,[.4,-.17,z],o,[0,Math.PI/2,0]);}box(1.29,.33,1.03,M.brass,[0,.24,0],o,.07);const lid=group([0,.43,-.48],o);box(1.22,.07,.96,M.ink,[0,0,.48],lid,.04);box(1.16,.10,.9,M.ivory,[0,.07,.48],lid,.065);label('A17',.72,.36,[0,.129,.48],lid,M.ivory,true);o.userData.lid=lid;label('A17',.52,.17,[0,.25,.531],o,M.brass);for(const x of [-.53,.53])for(const z of [-.38,.38])screw(x,.132,z+.48,lid,.6);for(const x of [-.65,.65]){const h=group([x,.20,0],o);ring(.14,.023,M.polish,[0,0,0],h,[0,Math.PI/2,0]);}return o;}
const mainCase=casework();
// Snapshot apparatus: four slender columns, visible diagonal lead-screw clamp drive.
const fixture=group();base(4.5,3.65,fixture);label('04',.62,.30,[0,.23,1.852],fixture,M.brass);
for(const x of [-1.65,1.65])for(const z of [-1.18,1.18]){turned([x,.45,z],.48,.19,fixture);cyl(.092,2.97,M.brass,[x,2.33,z],fixture);turned([x,3.82,z],.39,.16,fixture);sphere(.105,M.polish,[x,4.26,z],fixture);for(const yy of [.92,3.71,4.05])ring(.112,.019,M.polish,[x,yy,z],fixture);}
for(const z of [-1.18,1.18]){box(3.55,.12,.25,M.brass,[0,3.89,z],fixture,.035);for(const x of [-1.65,1.65])screw(x,3.97,z,fixture,.8);}
for(const x of [-1.65,1.65])bar([x,3.89,-1.18],[x,3.89,1.18],.07,M.brass,fixture);
box(2.8,.2,2.0,M.dark,[0,.65,0],fixture,.08);box(2.65,.06,1.86,M.brass,[0,.78,0],fixture,.04);for(const x of [-1.1,1.1])for(const z of [-.77,.77])screw(x,.82,z,fixture,.7);
// Side glass guards remain outside carriage and jaw envelopes. Front opening is clear.
for(const x of [-1.55,1.55]){const glass=box(.02,2.65,1.85,M.glass,[x,2.26,0],fixture,.01);glass.castShadow=false;for(const z of [-.9,.9])bar([x,.95,z],[x,3.57,z],.017,M.polish,fixture);}
const jaws=[-1,1].map(sign=>{const o=group([0,0,sign*1.12],fixture);box(1.55,.27,.28,M.brass,[0,1.67,0],o,.055);box(1.28,.20,.055,M.ebony,[0,1.63,-sign*.158],o,.025);for(const x of [-.58,.58]){bar([x,.84,0],[x,1.61,0],.05,M.steel,o);cyl(.095,.13,M.polish,[x,1.63,0],o);screw(x,1.82,0,o,.65);}return o;});
const clampWheel=gear(.42,24,[1.11,2.2,1.32],fixture);supportedAxle([1.11,2.2,.95],[1.11,2.2,1.5],.06,fixture);bar([1.11,2.2,.95],[1.11,.83,.95],.055,M.brass,fixture);
const clampCam=group([1.11,2.2,1.53],fixture);bar([0,0,0],[.3,0,0],.03,M.polish,clampCam);bar([.3,0,0],[.3,0,.2],.042,M.wood,clampCam);
const seal=group([0,0,0],fixture);bar([0,2.43,0],[0,3.86,0],.055,M.steel,seal);cyl(.16,.15,M.brass,[0,2.39,0],seal);cyl(.27,.08,M.polish,[0,2.27,0],seal);for(const z of [-.62,.62])bar([0,3.9,z],[0,3.9,0],.035,M.brass,fixture);
label('固定这次资料',2.5,.43,[0,3.58,1.35],fixture,M.ivory);
// Knurled scenario knobs, with true bearing supports and index plates.
const knobs=[];for(let i=0;i<3;i++){const k=group([-.58+i*.58,.91,1.41],fixture);k.rotation.x=.44;const disk=cyl(.17,.16,M.brass,[0,0,0],k);disk.rotation.x=Math.PI/2;for(let j=0;j<30;j++){const a=j*TAU/30;bar([.168*Math.cos(a),.168*Math.sin(a),-.07],[.168*Math.cos(a),.168*Math.sin(a),.07],.007,M.polish,k);}bar([0,0,.09],[0,.12,.09],.012,M.ink,k);knobs.push(k);}
// Frozen snapshot replicas follow three continuous rails; all endpoints meet instrument slots.
const trialXs=[5.2,10.1,15],trialZ=-7.1;
const branchCurves=trialXs.map((x,i)=>new T.CatmullRomCurve3([new T.Vector3(2.65,1.18,0),new T.Vector3(4,1.18,-.35-i*.22),new T.Vector3(x,1.18,-2.5),new T.Vector3(x,1.18,trialZ+1.1)],false,'centripetal'));
branchCurves.forEach(c=>rail(c,.74*.78));
const clones=trialXs.map(()=>casework(scene,.78));
// Mechanical switch tongue at the common branch origin.
const tongue=group([3.7,1.07,0]);bar([0,0,0],[1.1,0,0],.065,M.steel,tongue);cyl(.14,.07,M.brass,[0,0,0],tongue);
// A sheltered outlet dispenses already-sized trial cassettes, one at a time.
const outlet=group([2.55,0,0]);base(2.0,2.0,outlet);box(1.9,.18,1.9,M.brass,[0,2.30,0],outlet,.07);box(1.9,1.4,.12,M.wood,[0,1.5,-.85],outlet);box(.13,1.4,1.7,M.wood,[-.86,1.5,0],outlet);box(.13,.26,1.7,M.brass,[.86,2.05,0],outlet);label('同一份资料',1.64,.33,[0,2.29,.98],outlet);bar([1.58,1.9,-.5],[1.58,1.9,.5],.045,M.brass);
// Enamel gauge textures: equal scales, text anchored to the physical face.
function gaugeTexture(title,accent){const c=document.createElement('canvas');c.width=c.height=1024;const x=c.getContext('2d');x.fillStyle='#e4dcc7';x.fillRect(0,0,1024,1024);x.strokeStyle='#6b604e';for(const r of [467,440,320,170]){x.lineWidth=r===467?2:1;x.beginPath();x.arc(512,512,r,0,TAU);x.stroke();}for(let j=0;j<=60;j++){const a=(-.8+j/60*1.6)*Math.PI,R=j%5?421:393;x.lineWidth=j%5?1.5:3;x.beginPath();x.moveTo(512+Math.sin(a)*R,512-Math.cos(a)*R);x.lineTo(512+Math.sin(a)*450,512-Math.cos(a)*450);x.stroke();}x.strokeStyle=accent;x.lineWidth=18;x.beginPath();x.arc(512,512,460,-Math.PI*.42,-Math.PI*.12);x.stroke();x.fillStyle='#423b30';x.textAlign='center';x.font='50px "Microsoft YaHei"';x.fillText(title,512,660);x.font='22px Georgia';x.fillText('CONDITION / A17',512,708);x.font='24px "Microsoft YaHei"';x.fillText('机制示意',512,752);for(let k=0;k<3;k++){const xx=355+k*157;x.lineWidth=2;x.beginPath();x.arc(xx,380,44,0,TAU);x.stroke();x.beginPath();x.moveTo(xx-24,390);x.lineTo(xx,355);x.lineTo(xx+24,390);x.stroke();}const t=new T.CanvasTexture(c);t.colorSpace=T.SRGBColorSpace;t.anisotropy=16;return t;}
function needle(parent,r,z){const o=group([0,0,z],parent),shape=new T.Shape();shape.moveTo(-r*.035,-r*.22);shape.lineTo(-r*.018,r*.82);shape.lineTo(0,r*.92);shape.lineTo(r*.018,r*.82);shape.lineTo(r*.035,-r*.22);shape.closePath();mesh(new T.ExtrudeGeometry(shape,{depth:.016,bevelEnabled:true,bevelThickness:.006,bevelSize:.004,bevelSegments:2}),M.blue,[0,0,0],o);const pin=cyl(r*.065,.07,M.polish,[0,0,.03],parent);pin.rotation.x=Math.PI/2;pin.position.z=z+.02;return o;}
function gauge(r,p,parent,title,accent){const g=group(p,parent);const casing=cyl(r+.10,.22,M.brass,[0,0,0],g);casing.rotation.x=Math.PI/2;ring(r+.07,.027,M.polish,[0,0,.126],g,[0,0,0]);ring(r,.025,M.satin,[0,0,.15],g,[0,0,0]);const face=mesh(new T.CircleGeometry(r-.015,96),new T.MeshStandardMaterial({map:gaugeTexture(title,accent),roughness:.42,metalness:.02}),[0,0,.142],g);face.castShadow=false;const n=needle(g,r,.19);for(let j=0;j<8;j++){const a=j*TAU/8;frontScrew((r+.065)*Math.sin(a),(r+.065)*Math.cos(a),.147,g,.55);}return {g,n};}
const trials=[];
const nodePositions=[[-.85,2.14,1.05],[.72,3.30,1.05],[-.65,4.55,1.05]];
function enterprise(name,P,g){const o=group(P,g);box(1.35,.64,.18,M.brass,[0,0,0],o,.08);label(name,1.23,.46,[0,.025,.11],o);for(const x of [-.49,.49])bar([x,-.4,-.1],[x,.4,-.1],.035,M.polish,o);box(.21,.94,.08,M.ink,[.79,.15,0],o);const state=group([.79,-.30,.065],o);const flag=box(.15,.94,.04,M.amber.clone(),[0,.47,0],state,.015);return {o,state,flag};}
for(let i=0;i<3;i++){
 const title=['按现有情况','情况变差','采取措施'][i],g=group([trialXs[i],0,trialZ]);base(4.15,3.7,g);
 box(3.4,4.7,.18,M.wood,[0,3.38,.10],g,.13);box(3.20,4.49,.05,M.ebony,[0,3.38,.22],g,.08);
 for(const x of [-1.70,1.70])for(const z of [-.56,.72]){turned([x,.44,z],.44,.16,g);bar([x,.87,z],[x,5.75,z],.06,M.brass,g);turned([x,5.73,z],.28,.14,g);sphere(.086,M.polish,[x,6.08,z],g);for(const y of [1.1,5.52,5.73])ring(.093,.015,M.polish,[x,y,z],g);}
 for(const y of [.95,5.51])for(const z of [-.56,.72])bar([-1.7,y,z],[1.7,y,z],.055,M.brass,g);
 label([title,['已有偿债压力','假设融资更难','假设获得资金支持'][i]],3.08,.81,[0,5.65,.91],g);label('A17 · 同一份资料',2.74,.30,[0,.60,1.88],g,M.brass);
 // Fixed rails are confirmed relationships. Travelling seals indicate the illustrative influence.
 const paths=[[0,1],[1,2]].map(([from,to],j)=>{const a=new T.Vector3(...nodePositions[from]),b=new T.Vector3(...nodePositions[to]),d=b.clone().sub(a).normalize();a.addScaledVector(d,.5);b.addScaledVector(d,-.5);a.z=b.z=.78;const path=new T.LineCurve3(a,b);for(const offset of [-.075,.075]){const N=new T.Vector3(-d.y,d.x,0).multiplyScalar(offset);bar(a.clone().add(N).toArray(),b.clone().add(N).toArray(),.022,M.polish,g);}for(const P of [a,b]){frontScrew(P.x,P.y,.79,g,.7);bar([P.x,P.y,.28],[P.x,P.y,.78],.032,M.brass,g);}const mid=a.clone().add(b).multiplyScalar(.5);label(j?'同属集团':'担保关系',1.07,.28,[mid.x+.68,mid.y-.16,.87],g,M.ivory);const token=group([0,0,0],g);const seal=cyl(.11,.07,M.amber,[0,0,0],token);seal.rotation.x=Math.PI/2;ring(.105,.018,M.polish,[0,0,.05],token,[0,0,0]);return {path,token};});
 const nodes=nodePositions.map((P,j)=>enterprise(['借款公司 A','担保方 B','集团企业 C'][j],P,g));
 // An attached pressure shoe acts on A; mitigation changes this load, never the relationship rods.
 const load=group([-.85,3.03,1.08],g);bar([0,-.31,0],[0,.25,0],.043,M.steel,load);box(.52,.10,.36,M.brass,[0,-.28,0],load,.025);cyl(.18,.16,i===1?M.red:i===2?M.sage:M.satin,[0,.12,0],load);
 const spring=group([-.85,2.46,1.08],g),coil=[];for(let k=0;k<=120;k++){const a=k/120*TAU*4;coil.push(new T.Vector3(.13*Math.cos(a),k/120,.13*Math.sin(a)));}mesh(new T.TubeGeometry(new T.CatmullRomCurve3(coil),120,.016,6,false),M.steel,[0,0,0],spring);spring.scale.y=.24;
 box(1.85,.13,2.15,M.dark,[0,.93,.45],g,.05);for(const x of [-.5772,.5772]){bar([x,1.18,-.5],[x,1.18,1.8],.065,M.polish,g);for(const z of [-.4,1.7]){box(.24,.20,.25,M.brass,[x,1.02,z],g,.035);screw(x,1.135,z,g,.6);}}
 const a=gear(.46,24,[-1.10,.89,-.72],g),b=gear(.305,16,[-.36,.89,-.72],g);for(const x of [-1.1,-.36]){bar([x,.45,-.95],[x,.89,-.95],.045,M.brass,g);supportedAxle([x,.89,-1.03],[x,.89,-.58],.045,g);}
 trials.push({g,nodes,paths,load,spring,a,b});
}
// Shared round/iteration shaft on real saddles spans all three experiment units.
bar([3.65,5.52,trialZ-.56],[16.6,5.52,trialZ-.56],.065,M.steel);for(const x of trialXs){const g=group([x,5.52,trialZ-.56]);g.rotation.z=Math.PI/2;cyl(.15,.16,M.brass,[0,0,0],g);ring(.12,.015,M.polish,[0,.09,0],g);}
const sync=group([10.1,5.52,trialZ-.56]);const syncWheel=gear(.36,20,[0,0,.2],sync);
// Small recording instrument and real return rail establish continuation beyond the sample.
const recorder=group([18.5,0,-.8]);base(3.5,3.4,recorder);for(const x of [-1.14,1.14]){turned([x,.44,0],.4,.16,recorder);bar([x,.8,0],[x,2.4,0],.065,M.brass,recorder);}const drum=cyl(.79,2.1,M.paper,[0,1.75,0],recorder);drum.rotation.z=Math.PI/2;for(const x of [-1.08,1.08]){ring(.8,.034,M.polish,[x,1.75,0],recorder,[0,Math.PI/2,0]);bar([x-.1,1.75,0],[x+.1,1.75,0],.11,M.brass,recorder);}label('06',.60,.28,[0,.23,1.72],recorder,M.brass);
const returning=new T.CatmullRomCurve3([new T.Vector3(18.5,1.18,1.3),new T.Vector3(18,1.18,4.2),new T.Vector3(7,1.18,5),new T.Vector3(-4,1.18,4),new T.Vector3(-6,1.18,-2)],false,'centripetal');rail(returning,.74);

// Complete film: one physical case visits evidence, relationships and consultation.
function lectern(p,title,w=5.4,d=3.8){const g=group(p);base(w,d,g);for(const x of [-w/2+.25,w/2-.25]){turned([x,.44,-.7],.45,.16,g);bar([x,.86,-.7],[x,4.9,-.7],.055,M.brass,g);turned([x,4.85,-.7],.32,.15,g);sphere(.085,M.polish,[x,5.2,-.7],g);}bar([-w/2+.25,4.9,-.7],[w/2-.25,4.9,-.7],.06,M.brass,g);label(title,w-.5,.52,[0,4.64,-.45],g);return g;}
function paperCard(lines,w=1.6,h=1.05,parent=scene){const g=group([0,0,0],parent);box(w+.12,h+.12,.07,M.brass,[0,0,0],g,.055);label(lines,w,h,[0,0,.06],g,M.paper);for(const x of [-w*.36,w*.36]){box(.11,.22,.08,M.blue,[x,h/2+.025,.10],g,.02);}return g;}
const intake=lectern([-26,0,0],'先确认公司和事件',5.4);
label('公司',1.8,.38,[-1.2,3.65,-.25],intake);label('事情',1.8,.38,[1.2,3.65,-.25],intake);
for(const x of [-1.2,1.2]){box(1.95,.14,.56,M.dark,[x,2.74,-.27],intake);bar([x-.8,.7,-.56],[x-.8,3.3,-.56],.035,M.brass,intake);}
const identityCards=[paperCard(['借款公司 A','示例公司'],1.85,.77),paperCard(['还款有压力','示例事件'],1.85,.77)];
const sourceStation=lectern([-20,0,0],'先看资料，再作判断',6.1,4);
const evidenceCards=[0,1,2].map(i=>{const pivot=group([-1.85+i*1.85,3.25,-.2],sourceStation);const card=paperCard([['公告原文','出处：示例资料'],['担保文件','出处：示例资料'],['待核验消息','先保留疑问']][i],1.52,1.17,pivot);bar([0,-2.7,-.16],[0,.7,-.16],.035,M.brass,pivot);return pivot;});
const verifiedCards=[paperCard(['已核对','公告原文'],1.3,.65),paperCard(['已核对','担保文件'],1.3,.65)];
const pendingCard=paperCard(['仍待核验','不作为已知事实'],1.55,.75);
box(2,.25,1.2,M.wood,[2.5,.8,1.5],sourceStation);label('待核验',1.5,.32,[2.5,.9,2.13],sourceStation);
const relationStation=lectern([-12.8,0,-.2],'看看还涉及哪些公司',7.5,4.4);
const relFace=group([0,0,0],relationStation);
const relPs=[[-2.1,2.85,-.10],[0,3.85,-.10],[2.1,2.85,-.10]];
const relNodes=relPs.map((P,i)=>{const o=group(P,relFace);box(1.94,.72,.22,M.brass,[0,0,0],o,.07);label(['借款公司 A','担保方 B','集团企业 C'][i],1.81,.51,[0,0,.13],o);bar([0,-2.35,-.18],[0,-.38,-.18],.04,M.brass,o);return o;});
const relLinks=[[0,1],[1,2]].map(([a,b],i)=>{const g=group([0,0,0],relFace);const A=new T.Vector3(...relPs[a]),B=new T.Vector3(...relPs[b]),D=B.clone().sub(A).normalize();A.addScaledVector(D,.65);B.addScaledVector(D,-.65);A.z=B.z=.07;bar(A.toArray(),B.toArray(),.045,M.polish,g);for(const v of [A,B]){sphere(.10,M.polish,v.toArray(),g);}const mid=A.add(B).multiplyScalar(.5);label(i?'同属集团':'担保关系',1.35,.32,[mid.x,2.10,.15],g);return g;});
const backgroundRelation=paperCard(['行业相近','不直接接入试验'],1.95,.77,relationStation);backgroundRelation.position.set(0,1.13,1.5);
// The consultation circle has four real seats; documents travel to and from them.
const council=group([-6,0,-2]);const councilFoot=group([0,0,-.8],council);base(6.4,7.2,councilFoot);
for(const x of [-2.3,2.3]){turned([x,.44,-1.5],1.4,.25,council);bar([x,1.4,-1.5],[x,2.1,-1.5],.07,M.brass,council);}
const table=cyl(2.6,.16,M.wood,[0,1.65,-2.6],council);table.scale.z=.65;const tableRim=ring(2.58,.035,M.polish,[0,1.75,-2.6],council);tableRim.scale.y=.65;
label('带着资料，请专家一起看',5.2,.46,[0,4.75,-2.45],council);
for(const x of [-2.8,2.8]){turned([x,.44,-2.6],.4,.18,council);bar([x,.84,-2.6],[x,4.96,-2.6],.055,M.brass,council);sphere(.10,M.polish,[x,5,-2.6],council);}
const expertNames=['尽调评估专家','产业授信评估专家','合规风险专家','风险监控专家'];
const experts=expertNames.map((name,i)=>{const P=[(i-1.5)*1.52,2.9,-2.1-Math.sin((i+.5)/4*Math.PI)*.65];const g=group(P,council);box(1.36,.95,.43,M.wood,[0,0,0],g,.09);box(1.21,.77,.06,M.ebony,[0,.03,.245],g);label(name,1.27,.38,[0,-.12,.30],g);for(const x of [-.5,.5])turned([x,-1.3,-.03],.85,.13,g);const lamp=ring(.21,.028,M.polish,[0,.68,0],g,[0,0,0]);const pupil=cyl(.15,.07,M.ivory,[0,.68,0],g);pupil.rotation.x=Math.PI/2;return {g,P,parcel:paperCard(['A17','同一份资料'],.90,.52,council)};});
const opinionCards=[paperCard(['先核对','担保责任'],1.36,.75,council),paperCard(['还要查','资金到位时间'],1.65,.75,council)];
const reviewCards=[paperCard(['按现有情况','保留已有压力'],1.6,.76,council),paperCard(['情况变差','相关方影响增大'],1.6,.76,council),paperCard(['假设采取措施','仍需复核'],1.6,.76,council)];
const followup=paperCard(['待查事项','资金何时到位？'],2.0,.85,council);
box(2.3,.24,1.25,M.wood,[2.15,.8,1.5],council);
for(const x of [-1.9,0,1.9])bar([x,1.74,-1.15],[x,2.1,-1.15],.028,M.brass,council);
const earlyNodes=[[-26,1.18,0],[-20,1.18,0],[-12.8,1.18,0],[-6,1.18,-2],[-4.2,1.18,0],[0,1.18,0]];
const earlyPaths=earlyNodes.slice(0,-1).map((a,i)=>{const b=earlyNodes[i+1];return new T.CatmullRomCurve3([new T.Vector3(...a),new T.Vector3((a[0]+b[0])/2,1.18,a[2]),new T.Vector3(...b)],false,'centripetal');});earlyPaths.forEach(c=>rail(c));
const recordPath=new T.CatmullRomCurve3([new T.Vector3(0,1.18,0),new T.Vector3(2,1.18,1.2),new T.Vector3(8,1.18,2),new T.Vector3(15,1.18,2),new T.Vector3(18.5,1.18,1.3)],false,'centripetal');rail(recordPath);
// Two separate paper tracks: company actions and simulated messages, never news claims.
const logRig=group([18.5,0,-.8]);
recorder.visible=false;base(4.8,3.4,logRig);
for(const x of [-2.1,2.1]){turned([x,.44,-.7],.4,.16,logRig);bar([x,.84,-.7],[x,5.4,-.7],.06,M.brass,logRig);sphere(.10,M.polish,[x,5.4,-.7],logRig);}
bar([-2.1,5.15,-.7],[2.1,5.15,-.7],.065,M.brass,logRig);label('每一步，都能回头查',4,.48,[0,5.05,-.4],logRig);
const logs=[];for(let i=0;i<2;i++){const x=i?1.10:-1.10;label(i?'模拟消息':'公司应对',1.9,.40,[x,4.4,.10],logRig);box(1.90,2.6,.12,M.ebony,[x,2.95,-.10],logRig);const roll=cyl(.26,1.95,M.paper,[x,4.0,.06],logRig);roll.rotation.z=Math.PI/2;const roll2=cyl(.26,1.95,M.paper,[x,1.62,.06],logRig);roll2.rotation.z=Math.PI/2;for(const y of [1.62,4])for(const dx of [-1.02,1.02]){bar([x+dx,y,-.5],[x+dx,y,.25],.05,M.brass,logRig);}const lines=(i?['模拟讨论增加','关注担保责任','不是真实新闻']:['与公司沟通核验','假设寻求资金','记录措施与变化']).map((txt,j)=>{const g=paperCard([txt,'示例过程'],1.7,.53,logRig);g.position.set(x,3.56-j*.72,.13);return g;});logs.push({roll,roll2,lines});}
const resultBundle=paperCard(['A17 · 试验记录','条件、过程、待查问题'],2.8,.85);
resultBundle.rotation.order='YXZ';

const clamp=v=>Math.max(0,Math.min(1,v)),ease=v=>{v=clamp(v);return v*v*v*(10+v*(-15+6*v));},p=(t,a,b)=>clamp((t-a)/(b-a)),ramp=(t,a,b)=>ease(p(t,a,b)),mix=(a,b,u)=>a+(b-a)*u;
function quint(a,b,va,vb,h,u){const d=b-a,A=va*h,B=vb*h;return a+A*u+(10*d-6*A-4*B)*u**3+(-15*d+8*A+7*B)*u**4+(6*d-3*A-3*B)*u**5;}
// Shared nonzero endpoint derivatives at travel waypoints; deliberate stop for clamp contact.
const poses=[{"t": 0, "P": [-26.5, 5.0, 9], "L": [-26, 2.65, 0], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 39}, {"t": 2, "P": [-26.5, 5, 9], "L": [-26, 2.65, 0], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 39}, {"t": 5.5, "P": [-25.3, 4.5, 8], "L": [-26, 2.1, 0], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 39}, {"t": 8.7, "P": [-20, 5.2, 10], "L": [-20, 2.55, 0], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 39}, {"t": 13, "P": [-19.6, 5.1, 10], "L": [-20, 2.5, 0], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 39}, {"t": 16.5, "P": [-12.8, 6.1, 11], "L": [-12.8, 2.8, 0], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 40}, {"t": 21.5, "P": [-12.6, 5.8, 10.6], "L": [-12.8, 2.9, 0], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 40}, {"t": 25, "P": [-5.7, 6.7, 10], "L": [-6, 2.3, -3], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 40}, {"t": 29, "P": [-5.7, 6.7, 10], "L": [-6, 2.3, -3], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 40}, {"t": 32, "P": [-5.5, 4.2, 7.3], "L": [-3.3, 1.7, 0], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 36}, {"t": 34.2, "P": [-3.1, 4.5, 7.4], "L": [0, 1.85, 0], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 36}, {"t": 36.2, "P": [-2.8, 4.7, 7.7], "L": [0.1, 1.9, 0], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 36}, {"t": 39, "P": [6.4, 7.2, 10], "L": [6, 2, -2.5], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 39}, {"t": 41.4, "P": [11, 9, 13.5], "L": [10.1, 3.1, -6], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 40}, {"t": 43.6, "P": [6, 5.4, 1.4], "L": [5.2, 3.4, -6.15], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 42}, {"t": 45, "P": [6, 5.4, 1.4], "L": [5.2, 3.4, -6.15], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 42}, {"t": 46.4, "P": [10.5, 5.4, 1.4], "L": [10.1, 3.4, -6.15], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 42}, {"t": 49, "P": [10.5, 5.4, 1.4], "L": [10.1, 3.4, -6.15], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 42}, {"t": 50.4, "P": [15.4, 5.4, 1.4], "L": [15, 3.4, -6.15], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 42}, {"t": 53, "P": [15.4, 5.4, 1.4], "L": [15, 3.4, -6.15], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 42}, {"t": 55, "P": [11, 9, 13.5], "L": [10.1, 3.1, -6], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 40}, {"t": 57, "P": [9, 5.4, 10], "L": [8, 1.9, 1.7], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 41}, {"t": 59.5, "P": [18.7, 5.7, 9], "L": [18.5, 2.8, -0.2], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 40}, {"t": 65, "P": [18.7, 5.7, 9], "L": [18.5, 2.8, -0.2], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 40}, {"t": 67, "P": [17, 6.3, 12], "L": [16, 1.9, 3.5], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 41}, {"t": 69, "P": [7, 6.5, 13], "L": [6, 1.9, 4.7], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 41}, {"t": 71, "P": [-3, 6.5, 11], "L": [-4, 1.9, 3], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 41}, {"t": 73, "P": [-5.7, 6.7, 10], "L": [-6, 2.3, -3], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 40}, {"t": 76.7, "P": [-5.7, 6.7, 10], "L": [-6, 2.3, -3], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 40}, {"t": 80, "P": [-3, 30, 51], "L": [-3.5, 1.4, -2], "v": [0, 0, 0], "lv": [0, 0, 0], "f": 43}];
function cameraAt(t){let i=1;while(i<poses.length-1&&t>poses[i].t)i++;const a=poses[i-1],b=poses[i],h=b.t-a.t,u=p(t,a.t,b.t);return {P:a.P.map((v,j)=>quint(v,b.P[j],a.v[j],b.v[j],h,u)),L:a.L.map((v,j)=>quint(v,b.L[j],a.lv[j],b.lv[j],h,u)),f:mix(a.f,b.f,ease(u))};}
function place(o,curve,u,yOffset=.25){const P=curve.getPoint(clamp(u)),D=curve.getTangent(clamp(u));o.position.copy(P);o.position.y+=yOffset;o.rotation.y=Math.atan2(-D.z,D.x);}

const captions=[
 [0,'Risky 风险视角','围绕一件事，把资料和判断连起来'],
 [2.5,'先确认是哪家公司、哪件事','同一案件 A17'],
 [7,'先看资料从哪里来','公告、文件和消息，都要有出处'],
 [10,'核对过的资料，随案保存','还没查清的，单独留下'],
 [15,'看看还涉及哪些公司','担保、集团等关系，要有资料支持'],
 [19,'有关系，也要分清是什么关系','行业相近，不等于一定受到影响'],
 [23,'带着同一份资料，请专家一起看','从业务、行业、合规等角度讨论'],
 [27,'把意见和疑问都留下','还有什么没查清，接着查'],
 [32,'固定这次使用的资料','后面比较时，起点保持一致'],
 [36.4,'选好条件，确认后再试','需要比较时，再分别设置其他条件'],
 [41.4,'A 还款有压力，B 为它担保','黄柱越高，示例中的影响越大'],
 [45.5,'如果融资更难，先看 A 的变化','再沿着关系，看看可能影响谁'],
 [49.9,'假设获得资金支持','压力可能减轻，仍需看后续变化'],
 [54,'把不同条件下的结果放在一起','这些是条件假设，不是事情一定会发生'],
 [57,'结果怎样来的，每一步都留下','公司如何应对，和模拟消息分开看'],
 [61,'模拟消息，不是真实新闻','回看当时的条件、过程和资料'],
 [66,'带着结果和问题，回到同一件事','原来的资料、专家意见都还在'],
 [72,'再请专家复核，留下待查事项','例如：资金支持何时能够到位？'],
 [77,'查资料 · 请专家 · 换条件 · 再复核','Risky 风险视角']
];
function textOverlay(t){const s=W/1920;ctx.save();ctx.scale(s,s);let cap=captions[0];for(const c of captions)if(t>=c[0])cap=c;const a=Math.min(ramp(t,0,.7),1-ramp(t,79.2,80));const gr=ctx.createLinearGradient(0,878,0,1080);gr.addColorStop(0,'rgba(8,14,14,0)');gr.addColorStop(1,'rgba(8,14,14,.84)');ctx.fillStyle=gr;ctx.fillRect(0,878,1920,202);ctx.globalAlpha=a;ctx.textAlign='center';ctx.fillStyle='#f3ead5';ctx.font='400 34px "Microsoft YaHei"';ctx.fillText(cap[1],960,970);ctx.fillStyle='#d4c9b2';ctx.font='25px "Microsoft YaHei"';ctx.fillText(cap[2],960,1013);ctx.fillStyle='#b5ac98';ctx.font='19px "Microsoft YaHei"';ctx.fillText('合成案例 · 机制示意，不是实际预测',960,1053);ctx.restore();}
function interpolatePosition(o,a,b,u){o.position.fromArray(a.map((v,j)=>mix(v,b[j],u)));}
window.renderAt=(seconds,{overview=false}={})=>{
 const full=Math.max(0,Math.min(80,seconds));
 const t=Math.max(0,Math.min(24,seconds-32)),travel=ramp(t,.35,2.35),closed=ramp(t,2.6,3.45);
 lead.rotation.x=-travel*TAU*21;driveGear.rotation.z=-travel*TAU*8;pairedGear.rotation.z=travel*TAU*12-Math.PI/16;
 jaws.forEach((o,i)=>o.position.z=(i===0?-1:1)*(1.12-.43*closed));
 clampWheel.rotation.z=-closed*TAU*.7;clampCam.rotation.z=clampWheel.rotation.z;
 seal.position.y=-.24*(ramp(t,3.25,3.65)-ramp(t,4.0,4.35));knobs.forEach((k,i)=>k.rotation.z=(i-1)*.5*ramp(t,3.5,4.3));
 const spread=ramp(t,4.4,9);tongue.rotation.y=-.12-.22*ramp(t,5.7,7.5);
 clones.forEach((o,i)=>{const u=ramp(t,4.5+i*1.05,6.7+i*1.05);o.visible=t>=4.5+i*1.05;place(o,branchCurves[i],u,.17*.78);o.scale.setScalar(.78);});
 const round=p(t,10,21),stageStarts=[10.2,14.3,18.5];
 const illustrativeStates=trials.map((o,i)=>{
   const start=stageStarts[i],u=ramp(t,start,start+1),values=i===0?[.42-.03*u,.06+.10*ramp(t,start+1,start+1.6),.03+.05*ramp(t,start+1.8,start+2.45)]:i===1?[.42+.42*u,.06+.63*ramp(t,start+1,start+1.7),.03+.49*ramp(t,start+1.8,start+2.5)]:[.42-.22*u,.06+.035*ramp(t,start+1,start+1.7),.03+.015*ramp(t,start+1.8,start+2.5)];
   o.nodes.forEach((n,j)=>{n.state.scale.y=Math.max(.015,values[j]);});
   o.paths.forEach((v,j)=>{const a=start+.15+j*.8,b=a+.85,q=p(t,a,b);v.token.visible=t>=a&&t<=b;v.token.position.copy(v.path.getPoint(q));v.token.position.z+=.10;v.token.scale.setScalar(i===1?1.20:i===2?.62:.82);});
   o.load.position.y=3.03+(i===1?-.08:i===2?.12:0)*u;o.spring.scale.y=o.load.position.y-.33-2.46;o.a.rotation.z=-round*TAU*1.4;o.b.rotation.z=round*TAU*2.1-Math.PI/16;return values;
 });syncWheel.rotation.z=-round*TAU*1.4;

 // Every moving item is a deterministic function of absolute time.
 const earlyTimings=[[6,8.5],[14,16.2],[22,24.5],[30,32],[32,34.35]];
 let which=0,uu=0;for(let i=0;i<earlyTimings.length;i++){if(full>=earlyTimings[i][0]){which=i;uu=ramp(full,...earlyTimings[i]);}}
 place(mainCase,earlyPaths[which],uu,.25);
 if(full>=55)place(mainCase,recordPath,ramp(full,55,59),.25);
 if(full>=66)place(mainCase,returning,ramp(full,66,72),.25);
 const lidOpen=(a,b,c,d)=>ramp(full,a,b)-ramp(full,c,d);mainCase.userData.lid.rotation.x=-1.45*Math.max(lidOpen(1.5,2.3,5.2,5.8),lidOpen(10,10.7,13.2,13.8),lidOpen(26.4,27,29.3,29.8),lidOpen(71.9,72.4,72.9,73.4));
 identityCards.forEach((o,i)=>{const q=ramp(full,2.4+i*1.5,3.5+i*1.5);o.visible=full<3.6+i*1.5;o.scale.setScalar(1-.65*q);interpolatePosition(o,[-27.2+i*2.4,3.15,.25],[-26,1.65,0],q);});
 evidenceCards.forEach((o,i)=>{o.rotation.y=(i-1)*.98*(1-ramp(full,8.7,10.2));});
 verifiedCards.forEach((o,i)=>{const q=ramp(full,10.8+i*.8,12+i*.8);o.visible=full>=10.7+i*.8&&full<13.5;o.scale.setScalar(1-.45*q);interpolatePosition(o,[-21.85+i*1.85,3.25,.12],[-20,1.75,0],q);});
 {const q=ramp(full,11.7,13.1);pendingCard.visible=full>=11.7;interpolatePosition(pendingCard,[-18.15,3.25,.12],[-17.5,1.32,1.5],q);}
 relNodes.forEach((o,i)=>o.rotation.y=(i-1)*1.15*(1-ramp(full,16.4,18)));
 relLinks.forEach((o,i)=>{o.visible=full>=17+i*.6;o.scale.setScalar(Math.max(.001,ramp(full,17+i*.6,18.3+i*.6)));});
 experts.forEach((e,i)=>{const q=ramp(full,24.8+i*.25,26.2+i*.25);e.parcel.visible=full>=24.8+i*.25&&full<30;e.parcel.scale.setScalar(.8);interpolatePosition(e.parcel,[0,2,0],[e.P[0],e.P[1]+.7,e.P[2]+.65],q);});
 opinionCards.forEach((o,i)=>{const q=ramp(full,27+i*.5,28.6+i*.5);o.visible=full>=27+i*.5&&full<30;o.scale.setScalar(1-.45*q);interpolatePosition(o,[-1.5+i*3,3.1,-1.7],[0,1.85,0],q);});
 logs.forEach((log,i)=>{const q=ramp(full,59,65);log.roll.rotation.x=q*TAU*2;log.roll2.rotation.x=q*TAU*2;log.lines.forEach((o,j)=>{const a=59.2+j*1.3+i*.35;o.visible=full>=a;o.position.y=3.56-j*.72-.13*(1-ramp(full,a,a+.5));});});
 drum.rotation.x=ramp(full,59,65)*TAU*2;
 {const q=ramp(full,64.4,65.7);resultBundle.visible=full>=64.4&&full<72;const start=[18.5,3.4,.8],end=[18.5,2.05,1.3];interpolatePosition(resultBundle,start,end,q);if(full>=66){resultBundle.position.copy(mainCase.position);resultBundle.position.y+=.62;resultBundle.rotation.y=mainCase.rotation.y;}else resultBundle.rotation.y=0;resultBundle.rotation.x=-Math.PI/2*q;resultBundle.scale.setScalar(1-.5*q);}
 reviewCards.forEach((o,i)=>{const q=ramp(full,72.2+i*.3,73.5+i*.3);o.visible=full>=72.2+i*.3;interpolatePosition(o,[0,1.95,0],[-1.9+i*1.9,2.48,-1.15],q);});
 {const q=ramp(full,74.1,75.6);followup.visible=full>=74.1;interpolatePosition(followup,[1.55,3.1,-1.5],[2.15,1.45,1.5],q);}
 const pose=cameraAt(full);if(overview){pose.P=[-3,35,56];pose.L=[-3,1.5,-2];pose.f=44;}camera.position.fromArray(pose.P);camera.lookAt(new T.Vector3(...pose.L));camera.fov=pose.f;camera.updateProjectionMatrix();renderer.render(scene,camera);ctx.clearRect(0,0,W,H);ctx.drawImage(renderer.domElement,0,0,W,H);if(!overview)textOverlay(full);if(full>79.2){ctx.fillStyle=`rgba(12,18,17,${ramp(full,79.2,80)})`;ctx.fillRect(0,0,W,H);}
 return {t:full,trialTime:t,travel,clamp:closed,round,illustrativeStates,notEngineResults:true,case:mainCase.position.toArray(),copies:clones.map(o=>({visible:o.visible,p:o.position.toArray()})),camera:pose,parts:partCount,calls:renderer.info.render.calls,triangles:renderer.info.render.triangles};
};
window.capture=(type='image/png',quality=.97)=>canvas.toDataURL(type,quality);
window.sceneInfo={parts:partCount,three:T.REVISION,width:W,height:H,duration:80,style:'eighteenth-century-instrument',purpose:'full-risky-user-explainer',businessMapping:'../BUSINESS-MAPPING.md',notEngineResults:true};
window.renderAt(0);window.ready=true;
