import * as T from 'three';
import {HDRLoader} from './vendor/HDRLoader.js';
import {RoundedBoxGeometry} from './vendor/RoundedBoxGeometry.js';

await document.fonts.load('400 40px "Microsoft YaHei"');
const Q=new URLSearchParams(location.search),W=+(Q.get('width')||1920),H=Math.round(W*9/16),TAU=2*Math.PI;
const renderer=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true,powerPreference:'high-performance'});
renderer.setSize(W,H);renderer.setPixelRatio(1);renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;
renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.02;
const canvas=document.createElement('canvas');canvas.width=W;canvas.height=H;document.body.appendChild(canvas);const ctx=canvas.getContext('2d');
const scene=new T.Scene();scene.background=new T.Color('#242b2c');scene.fog=new T.FogExp2('#242b2c',.009);
const camera=new T.PerspectiveCamera(37,W/H,.1,250);
const hdr=await new HDRLoader().loadAsync('./assets/brown_photostudio_02_1k.hdr');
const pm=new T.PMREMGenerator(renderer);scene.environment=pm.fromEquirectangular(hdr).texture;hdr.dispose();pm.dispose();scene.environmentIntensity=.72;scene.environmentRotation.y=.7;
scene.add(new T.HemisphereLight(0xc8d4da,0x342317,.8));
const sunlight=new T.DirectionalLight(0xffe5bf,3.6);sunlight.position.set(-12,19,11);sunlight.target.position.set(5,0,-3);sunlight.castShadow=true;sunlight.shadow.mapSize.set(4096,4096);Object.assign(sunlight.shadow.camera,{left:-24,right:24,top:19,bottom:-19,near:1,far:65});sunlight.shadow.normalBias=.012;sunlight.shadow.bias=-.00008;sunlight.shadow.radius=3;scene.add(sunlight,sunlight.target);
const fill=new T.DirectionalLight(0xb4cad8,1.05);fill.position.set(15,10,-15);scene.add(fill);
const rim=new T.DirectionalLight(0xffcf87,.8);rim.position.set(8,5,-9);scene.add(rim);
const loader=new T.TextureLoader();const woodMap=await loader.loadAsync('./assets/dark_wood_diff_1k.jpg');woodMap.colorSpace=T.SRGBColorSpace;woodMap.wrapS=woodMap.wrapT=T.RepeatWrapping;woodMap.repeat.set(1.25,.65);woodMap.anisotropy=16;
const woodNormal=await loader.loadAsync('./assets/dark_wood_nor_gl_1k.jpg');woodNormal.wrapS=woodNormal.wrapT=T.RepeatWrapping;woodNormal.repeat.copy(woodMap.repeat);woodNormal.anisotropy=16;
let seed=171;const rand=()=>{seed=(1664525*seed+1013904223)>>>0;return seed/4294967296;};
function grain(){const c=document.createElement('canvas');c.width=c.height=512;const x=c.getContext('2d');x.fillStyle='#c4c4c4';x.fillRect(0,0,512,512);for(let j=0;j<3000;j++){const v=160+rand()*55;x.strokeStyle=`rgba(${v},${v},${v},.15)`;x.lineWidth=.25+rand()*.4;const y=rand()*512;x.beginPath();x.moveTo(0,y);x.lineTo(512,y+.3*rand());x.stroke();}const t=new T.CanvasTexture(c);t.wrapS=t.wrapT=T.RepeatWrapping;return t;}
const brushed=grain();const standard=(color,metalness,roughness,other={})=>new T.MeshStandardMaterial({color,metalness,roughness,...other});
const M={brass:standard('#b79a60',.91,.25,{bumpMap:brushed,bumpScale:.002}),polish:standard('#d3b77b',.95,.2),satin:standard('#9e8856',.83,.35),dark:standard('#1a2422',.42,.3),ebony:standard('#17211d',.13,.35),wood:standard('#a47b5b',.04,.35,{map:woodMap,normalMap:woodNormal,normalScale:new T.Vector2(.13,.13)}),steel:standard('#8e9799',.96,.23),blue:standard('#172d36',.88,.22),ivory:standard('#e2d8bd',.03,.39),paper:standard('#ded3b5',.02,.72),ink:standard('#342a1e',.1,.52),red:standard('#78392f',.2,.4),sage:standard('#6c8065',.2,.42),amber:standard('#bc8e36',.42,.36),glass:new T.MeshPhysicalMaterial({color:'#bdd3d0',transmission:.96,thickness:.045,roughness:.08,metalness:0,ior:1.48,transparent:true,opacity:.25,depthWrite:false})};
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
function engravingTexture(lines,width=1024,height=256){const c=document.createElement('canvas');c.width=width;c.height=height;const x=c.getContext('2d');x.clearRect(0,0,width,height);x.strokeStyle='#624a2d';x.lineWidth=1.8;x.strokeRect(16,16,width-32,height-32);x.strokeRect(23,23,width-46,height-46);for(const sx of [-1,1]){x.save();x.translate(width/2,height/2);x.scale(sx,1);x.beginPath();x.moveTo(width*.44,height*.3);x.bezierCurveTo(width*.35,height*.3,width*.33,-height*.22,width*.24,-height*.18);x.bezierCurveTo(width*.16,-height*.12,width*.21,height*.17,width*.26,height*.03);x.stroke();x.restore();}x.textAlign='center';x.textBaseline='middle';lines.forEach((s,i)=>{x.font=`${i?34:48}px Georgia,"Microsoft YaHei",serif`;x.fillStyle='#3f3321';x.fillText(s,width/2,height*(lines.length===1?.5:.40+i*.29));});const tex=new T.CanvasTexture(c);tex.colorSpace=T.SRGBColorSpace;return tex;}
function label(s,w,h,p,parent=scene,material=M.ivory,top=false){const o=group(p,parent);if(top)o.rotation.x=-Math.PI/2;box(w,h,.025,material,[0,0,0],o,.025);const tex=engravingTexture(Array.isArray(s)?s:[s]);const face=mesh(new T.PlaneGeometry(w*.97,h*.93),new T.MeshStandardMaterial({map:tex,transparent:true,depthWrite:false,roughness:.6,metalness:.05}),[0,0,.016],o);face.castShadow=false;for(const x of [-w/2+.06,w/2-.06])frontScrew(x,0,.028,o,.53);return o;}
function base(w,d,parent){box(w,.18,d,M.wood,[0,.18,0],parent,.11);box(w-.1,.025,d-.1,M.polish,[0,.285,0],parent,.06);box(w-.16,.12,d-.16,M.wood,[0,.36,0],parent,.055);for(const z of [-d/2+.1,d/2-.1])box(w-.22,.012,.014,M.polish,[0,.43,z],parent,.002);for(const x of [-w/2+.25,w/2-.25])for(const z of [-d/2+.25,d/2-.25]){turned([x,-.02,z],.13,.15,parent);screw(x,.44,z,parent,.7);}return .44;}
function gear(r,n,p,parent=scene,depth=.105){const o=group(p,parent),shape=new T.Shape();for(let j=0;j<n*4;j++){const a=j/(n*4)*TAU,R=r*[.91,1,1,.91][j%4],x=R*Math.cos(a),y=R*Math.sin(a);if(j)shape.lineTo(x,y);else shape.moveTo(x,y);}shape.closePath();const center=new T.Path();center.absarc(0,0,r*.12,0,TAU,true);shape.holes.push(center);for(let j=0;j<6;j++){const a=j*TAU/6+.12,b=(j+1)*TAU/6-.12,h=new T.Path();h.absarc(0,0,r*.75,b,a,true);h.lineTo(r*.3*Math.cos(a),r*.3*Math.sin(a));h.absarc(0,0,r*.3,a,b,false);h.closePath();shape.holes.push(h);}mesh(geom(`gear${r}/${n}/${depth}`,()=>new T.ExtrudeGeometry(shape,{depth,steps:1,bevelEnabled:true,bevelThickness:.008,bevelSize:.008,bevelSegments:2})),M.brass,[0,0,-depth/2],o);for(const R of [.80,.85])ring(r*R,.006,M.polish,[0,0,depth/2+.008],o,[0,0,0]);const hub=cyl(r*.19,depth*1.8,M.polish,[0,0,0],o);hub.rotation.x=Math.PI/2;return o;}
function supportedAxle(a,b,r,parent){bar(a,b,r,M.steel,parent);for(const P of [a,b]){const g=group(P,parent);const dir=new T.Vector3(...b).sub(new T.Vector3(...a)).normalize();g.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),dir);cyl(r*2.2,.18,M.brass,[0,0,0],g);ring(r*1.7,.016,M.polish,[0,.1,0],g);}}
const deck=group();box(31,.24,22,M.wood,[4,-.25,-2],deck,.18);box(30.85,.025,21.85,M.polish,[4,-.111,-2],deck,.1);box(30.7,.055,21.7,standard('#27312e',.24,.29),[4,-.07,-2],deck,.1);
const ground=mesh(new T.PlaneGeometry(400,400),standard('#2d3433',.12,.38),[0,-.51,0]);ground.rotation.x=-Math.PI/2;ground.castShadow=false;
// Architectural background: walnut cabinets and sparse scientific instruments, real geometry.
const archive=group([-6,0,-10]);
for(let i=0;i<9;i++){const a=(i-4)*.13,g=group([i*1.25-5,0,.08*(i-4)**2],archive);g.rotation.y=-a;box(1.20,3.8,.7,M.wood,[0,2.1,0],g,.06);box(1.28,.12,.87,M.wood,[0,4.04,0],g,.05);for(let j=0;j<5;j++){box(1.05,.59,.06,M.wood,[0,.7+j*.66,.385],g,.018);label(`${i+1} / ${j+1}`,.39,.13,[0,.7+j*.66,.424],g,M.brass);bar([-.15,.60+j*.66,.47],[.15,.60+j*.66,.47],.018,M.polish,g);}for(const dx of [-.56,.56]){box(.035,3.5,.03,M.polish,[dx,2.1,.39],g,.005);}}
// Main input bridge: guide shafts, saddles, driven screw, attached cross ties.
const inputCurve=new T.LineCurve3(new T.Vector3(-8,1.18,0),new T.Vector3(0,1.18,0));
function rail(curve,width=.74,parent=scene){const edges=[-1,1].map(sign=>{const points=[];for(let i=0;i<=100;i++){const u=i/100,P=curve.getPoint(u),D=curve.getTangent(u),N=new T.Vector3(-D.z,0,D.x).normalize();points.push(P.addScaledVector(N,width*sign));}return points;});for(const q of edges)mesh(new T.TubeGeometry(new T.CatmullRomCurve3(q),150,.06,10,false),M.polish,[0,0,0],parent);for(let u=0;u<=1.001;u+=.13){const P=curve.getPoint(Math.min(1,u)),D=curve.getTangent(Math.min(1,u)),N=new T.Vector3(-D.z,0,D.x).normalize();const a=P.clone().addScaledVector(N,width+.12),b=P.clone().addScaledVector(N,-width-.12);bar(a.toArray(),b.toArray(),.045,M.satin,parent);turned([P.x,.03,P.z],Math.max(.1,P.y-.08),.135,parent);cyl(.18,.05,M.brass,[P.x,.08,P.z],parent);}}
rail(inputCurve);
const lead=group([-4,1.05,0]);bar([-4,0,0],[4,0,0],.065,M.blue,lead);const helix=[];for(let i=0;i<=900;i++){const a=i/900*TAU*40;helix.push(new T.Vector3(-4+8*i/900,.091*Math.cos(a),.091*Math.sin(a)));}mesh(new T.TubeGeometry(new T.CatmullRomCurve3(helix),900,.018,5,false),M.steel,[0,0,0],lead);for(const x of [-8,0]){box(.4,.22,.4,M.dark,[x,.96,0]);supportedAxle([x-.12,1.05,0],[x+.12,1.05,0],.075,scene);}
const driveGear=gear(.49,24,[-7.5,1.05,.4]);const pairedGear=gear(.325,16,[-6.712,1.05,.4]);for(const x of [-7.5,-6.712]){bar([x,.08,.08],[x,1.05,.08],.06,M.brass);supportedAxle([x,1.05,.07],[x,1.05,.55],.055,scene);}
// The single case is rigidly attached to a guide carriage; copies retain A17 identity.
function casework(parent=scene,small=1){const o=group([0,0,0],parent);o.scale.setScalar(small);box(1.42,.17,1.26,M.satin,[0,0,0],o,.045);for(const z of [-.74,.74]){const tubeO=cyl(.12,.9,M.brass,[0,-.17,z],o);tubeO.rotation.z=Math.PI/2;ring(.13,.015,M.polish,[-.4,-.17,z],o,[0,Math.PI/2,0]);ring(.13,.015,M.polish,[.4,-.17,z],o,[0,Math.PI/2,0]);}box(1.29,.33,1.03,M.brass,[0,.24,0],o,.07);box(1.22,.07,.96,M.ink,[0,.43,0],o,.04);box(1.16,.10,.9,M.ivory,[0,.50,0],o,.065);label('A17',.72,.36,[0,.559,0],o,M.ivory,true);label('A17',.52,.17,[0,.25,.531],o,M.brass);for(const x of [-.53,.53])for(const z of [-.38,.38])screw(x,.562,z,o,.6);for(const x of [-.65,.65]){const h=group([x,.20,0],o);ring(.14,.023,M.polish,[0,0,0],h,[0,Math.PI/2,0]);}return o;}
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
label(['SNAPSHOT','证据 · 关系 · 假设'],1.6,.43,[0,3.84,1.207],fixture,M.brass);
// Knurled scenario knobs, with true bearing supports and index plates.
const knobs=[];for(let i=0;i<3;i++){const k=group([-.58+i*.58,.91,1.41],fixture);k.rotation.x=.44;const disk=cyl(.17,.16,M.brass,[0,0,0],k);disk.rotation.x=Math.PI/2;for(let j=0;j<30;j++){const a=j*TAU/30;bar([.168*Math.cos(a),.168*Math.sin(a),-.07],[.168*Math.cos(a),.168*Math.sin(a),.07],.007,M.polish,k);}bar([0,0,.09],[0,.12,.09],.012,M.ink,k);knobs.push(k);}
// Frozen snapshot replicas follow three continuous rails; all endpoints meet instrument slots.
const trialXs=[5.2,10.1,15],trialZ=-7.1;
const branchCurves=trialXs.map((x,i)=>new T.CatmullRomCurve3([new T.Vector3(0,1.18,0),new T.Vector3(2.3,1.18,-.12-i*.12),new T.Vector3(x,1.18,-2.2),new T.Vector3(x,1.18,trialZ+1.1)],false,'centripetal'));
branchCurves.forEach(c=>rail(c,.74));
const clones=trialXs.map(()=>casework(scene,.78));
// Mechanical switch tongue at the common branch origin.
const tongue=group([1.15,1.07,0]);bar([0,0,0],[1.4,0,0],.065,M.steel,tongue);cyl(.14,.07,M.brass,[0,0,0],tongue);
// Enamel gauge textures: equal scales, text anchored to the physical face.
function gaugeTexture(title,accent){const c=document.createElement('canvas');c.width=c.height=1024;const x=c.getContext('2d');x.fillStyle='#e4dcc7';x.fillRect(0,0,1024,1024);x.strokeStyle='#6b604e';for(const r of [467,440,320,170]){x.lineWidth=r===467?2:1;x.beginPath();x.arc(512,512,r,0,TAU);x.stroke();}for(let j=0;j<=60;j++){const a=(-.8+j/60*1.6)*Math.PI,R=j%5?421:393;x.lineWidth=j%5?1.5:3;x.beginPath();x.moveTo(512+Math.sin(a)*R,512-Math.cos(a)*R);x.lineTo(512+Math.sin(a)*450,512-Math.cos(a)*450);x.stroke();}x.strokeStyle=accent;x.lineWidth=18;x.beginPath();x.arc(512,512,460,-Math.PI*.42,-Math.PI*.12);x.stroke();x.fillStyle='#423b30';x.textAlign='center';x.font='50px "Microsoft YaHei"';x.fillText(title,512,660);x.font='22px Georgia';x.fillText('CONDITION / A17',512,708);x.font='24px "Microsoft YaHei"';x.fillText('机制示意',512,752);for(let k=0;k<3;k++){const xx=355+k*157;x.lineWidth=2;x.beginPath();x.arc(xx,380,44,0,TAU);x.stroke();x.beginPath();x.moveTo(xx-24,390);x.lineTo(xx,355);x.lineTo(xx+24,390);x.stroke();}const t=new T.CanvasTexture(c);t.colorSpace=T.SRGBColorSpace;t.anisotropy=16;return t;}
function needle(parent,r,z){const o=group([0,0,z],parent),shape=new T.Shape();shape.moveTo(-r*.035,-r*.22);shape.lineTo(-r*.018,r*.82);shape.lineTo(0,r*.92);shape.lineTo(r*.018,r*.82);shape.lineTo(r*.035,-r*.22);shape.closePath();mesh(new T.ExtrudeGeometry(shape,{depth:.016,bevelEnabled:true,bevelThickness:.006,bevelSize:.004,bevelSegments:2}),M.blue,[0,0,0],o);const pin=cyl(r*.065,.07,M.polish,[0,0,.03],parent);pin.rotation.x=Math.PI/2;pin.position.z=z+.02;return o;}
function gauge(r,p,parent,title,accent){const g=group(p,parent);const casing=cyl(r+.10,.22,M.brass,[0,0,0],g);casing.rotation.x=Math.PI/2;ring(r+.07,.027,M.polish,[0,0,.126],g,[0,0,0]);ring(r,.025,M.satin,[0,0,.15],g,[0,0,0]);const face=mesh(new T.CircleGeometry(r-.015,96),new T.MeshStandardMaterial({map:gaugeTexture(title,accent),roughness:.42,metalness:.02}),[0,0,.142],g);face.castShadow=false;const n=needle(g,r,.19);for(let j=0;j<8;j++){const a=j*TAU/8;frontScrew((r+.065)*Math.sin(a),(r+.065)*Math.cos(a),.147,g,.55);}return {g,n};}
const trials=[];
for(let i=0;i<3;i++){
 const title=['基准','不利','缓释'][i],accent=['#a49159','#8b4138','#70856c'][i],g=group([trialXs[i],0,trialZ]);base(4.05,3.7,g);label('05',.53,.26,[0,.24,1.875],g,M.brass);
 for(const x of [-1.55,1.55])for(const z of [-.56,.72]){turned([x,.44,z],.44,.16,g);bar([x,.87,z],[x,5.6,z],.065,M.brass,g);turned([x,5.59,z],.28,.14,g);sphere(.086,M.polish,[x,5.94,z],g);for(const y of [1.1,2.18,4.8,5.52])ring(.093,.015,M.polish,[x,y,z],g);}
 for(const y of [.95,2.15,4.82,5.51]){bar([-1.55,y,.72],[1.55,y,.72],.055,M.brass,g);bar([-1.55,y,-.56],[1.55,y,-.56],.055,M.brass,g);}
 const dial=gauge(1.22,[0,4.1,.70],g,title,accent);
 // Twin physical linear scales. A synchronised pointer travels in its slot.
 const slides=[];
 for(let row=0;row<2;row++){const y=1.85+row*.61;box(2.65,.40,.11,M.ivory,[0,y,.89],g,.12);box(2.35,.038,.04,M.ink,[0,y,.96],g,.012);for(let j=0;j<21;j++)box(.012,j%5===0?.12:.065,.009,M.ink,[-1.08+j*.108,y+.12,.957],g,.002);label(row?'舆情':'业务',.36,.16,[-1.1,y-.085,.974],g,M.ivory);const slider=group([0,y,1.01],g);ring(.082,.018,M.blue,[0,0,0],slider,[0,0,0]);bar([0,-.16,0],[0,.17,0],.013,M.blue,slider);slides.push(slider);}
 // The input slot, guide bushings, supported drive train and open gearwork.
 box(1.85,.13,2.15,M.dark,[0,.93,.45],g,.05);for(const x of [-.75,.75]){bar([x,1.18,-.5],[x,1.18,1.8],.065,M.polish,g);for(const z of [-.4,1.7]){box(.24,.20,.25,M.brass,[x,1.02,z],g,.035);screw(x,1.135,z,g,.6);}}
 const a=gear(.46,24,[-1.10,1.33,-.72],g),b=gear(.305,16,[-.36,1.33,-.72],g);
 for(const x of [-1.1,-.36]){bar([x,.45,-.95],[x,1.33,-.95],.045,M.brass,g);supportedAxle([x,1.33,-1.03],[x,1.33,-.58],.045,g);}
 const driver=group([1.18,1.36,.44],g);const fly=gear(.36,20,[0,0,0],driver);bar([0,0,0],[.30,0,0],.025,M.polish,driver);bar([.3,0,0],[.3,0,.19],.035,M.wood,driver);
 label(['A17 / 同源快照',title+'情景'],2.08,.42,[0,5.45,.79],g,M.brass);
 // Upper/lower mechanism status medallions support each scale without implying real loss data.
 const medallions=[];for(let k=0;k<4;k++){const x=-.96+k*.64;cyl(.10,.12,M.brass,[x,5.78,0],g);sphere(.064,[M.satin,M.red,M.sage][i],[x,5.9,0],g);medallions.push(x);}
 trials.push({g,dial,slides,a,b,driver,medallions});
}
// Shared round/iteration shaft on real saddles spans all three experiment units.
bar([3.65,5.52,trialZ-.56],[16.6,5.52,trialZ-.56],.065,M.steel);for(const x of trialXs){const g=group([x,5.52,trialZ-.56]);g.rotation.z=Math.PI/2;cyl(.15,.16,M.brass,[0,0,0],g);ring(.12,.015,M.polish,[0,.09,0],g);}
const sync=group([10.1,5.52,trialZ-.56]);const syncWheel=gear(.36,20,[0,0,.2],sync);
// Small recording instrument and real return rail establish continuation beyond the sample.
const recorder=group([18.5,0,-.8]);base(3.5,3.4,recorder);for(const x of [-1.14,1.14]){turned([x,.44,0],.4,.16,recorder);bar([x,.8,0],[x,2.4,0],.065,M.brass,recorder);}const drum=cyl(.79,2.1,M.paper,[0,1.75,0],recorder);drum.rotation.z=Math.PI/2;for(const x of [-1.08,1.08]){ring(.8,.034,M.polish,[x,1.75,0],recorder,[0,Math.PI/2,0]);bar([x-.1,1.75,0],[x+.1,1.75,0],.11,M.brass,recorder);}label('06',.60,.28,[0,.23,1.72],recorder,M.brass);
const returning=new T.CatmullRomCurve3([new T.Vector3(18.5,1.18,1.3),new T.Vector3(18,1.18,4.2),new T.Vector3(7,1.18,5),new T.Vector3(-4,1.18,4),new T.Vector3(-6,1.18,-2)],false,'centripetal');rail(returning,.74);
// Sparse turned furnishings in deep background give scale and context, without UI.
for(const x of [-11,-3,5,13]){box(.12,6.5,.12,M.wood,[x,3.0,-13.2]);box(7.6,.09,.12,M.wood,[x+3.8,5.7,-13.2]);}
const clamp=v=>Math.max(0,Math.min(1,v)),ease=v=>{v=clamp(v);return v*v*v*(10+v*(-15+6*v));},p=(t,a,b)=>clamp((t-a)/(b-a)),ramp=(t,a,b)=>ease(p(t,a,b)),mix=(a,b,u)=>a+(b-a)*u;
function quint(a,b,va,vb,h,u){const d=b-a,A=va*h,B=vb*h;return a+A*u+(10*d-6*A-4*B)*u**3+(-15*d+8*A+7*B)*u**4+(6*d-3*A-3*B)*u**5;}
// Shared nonzero endpoint derivatives at travel waypoints; deliberate stop for clamp contact.
const poses=[
 {t:0,P:[-5.5,4.2,7.3],L:[-3.3,1.7,0],v:[1.4,0,0],lv:[1.4,0,0],f:36},
 {t:2.2,P:[-3.1,4.5,7.4],L:[0,1.85,0],v:[0,0,0],lv:[0,0,0],f:36},
 {t:4.2,P:[-2.8,4.7,7.7],L:[.1,1.9,0],v:[.8,.4,.7],lv:[1,0,-.3],f:36},
 {t:6.4,P:[3.4,7.2,12],L:[4.5,2,-2.1],v:[3.5,1,2],lv:[2.8,.1,-1],f:37},
 {t:8.5,P:[11.4,10.8,16.9],L:[9.5,2.7,-5.4],v:[0,0,0],lv:[0,0,0],f:37},
 {t:12,P:[11.0,10.5,16.3],L:[9.5,2.7,-5.4],v:[0,0,0],lv:[0,0,0],f:37}
];
function cameraAt(t){let i=1;while(i<poses.length-1&&t>poses[i].t)i++;const a=poses[i-1],b=poses[i],h=b.t-a.t,u=p(t,a.t,b.t);return {P:a.P.map((v,j)=>quint(v,b.P[j],a.v[j],b.v[j],h,u)),L:a.L.map((v,j)=>quint(v,b.L[j],a.lv[j],b.lv[j],h,u)),f:mix(a.f,b.f,ease(u))};}
function place(o,curve,u,yOffset=.25){const P=curve.getPoint(clamp(u)),D=curve.getTangent(clamp(u));o.position.copy(P);o.position.y+=yOffset;o.rotation.y=Math.atan2(-D.z,D.x);}
function textOverlay(t){const s=W/1920;ctx.save();ctx.scale(s,s);const line=t<2.4?'同一个案件，进入情景试验':t<4.4?'固定证据、关系与假设':t<7.8?'同一快照，生成三组对照':'基准 · 不利 · 缓释：同轮次比较';const alpha=Math.min(ramp(t,0,.5),1-ramp(t,11.6,12));const gr=ctx.createLinearGradient(0,880,0,1080);gr.addColorStop(0,'rgba(8,14,14,0)');gr.addColorStop(1,'rgba(8,14,14,.68)');ctx.fillStyle=gr;ctx.fillRect(0,880,1920,200);ctx.globalAlpha=alpha;ctx.textAlign='center';ctx.fillStyle='#f3ead5';ctx.font='400 34px "Microsoft YaHei"';ctx.fillText(line,960,1002);ctx.fillStyle='#c5bba5';ctx.font='20px "Microsoft YaHei"';ctx.fillText('示例案件 A17 · 机制示意',960,1042);ctx.restore();}
window.renderAt=(seconds,{overview=false}={})=>{
 const t=Math.max(0,Math.min(12,seconds)),travel=ramp(t,.35,2.35),closed=ramp(t,2.6,3.45);
 mainCase.position.set(-4.2+4.2*travel,1.43,0);lead.rotation.x=-travel*TAU*21;driveGear.rotation.z=-travel*TAU*8;pairedGear.rotation.z=travel*TAU*12-Math.PI/16;
 jaws.forEach((o,i)=>o.position.z=(i===0?-1:1)*(1.12-.43*closed));
 clampWheel.rotation.z=-closed*TAU*.7;clampCam.rotation.z=clampWheel.rotation.z;
 seal.position.y=-.24*(ramp(t,3.25,3.65)-ramp(t,4.0,4.35));knobs.forEach((k,i)=>k.rotation.z=(i-1)*.5*ramp(t,3.5,4.3));
 const spread=ramp(t,4.4,7.5);tongue.rotation.y=-.38*ramp(t,4.4,5.3);
 clones.forEach((o,i)=>{const u=ramp(t,4.45+i*.20,7.2+i*.22);o.visible=t>4.45+i*.20;place(o,branchCurves[i],u,.19);o.scale.setScalar(.78*Math.max(.01,ramp(t,4.45+i*.20,4.85+i*.20)));});
 const run=ramp(t,8.0,10.9),round=Math.min(1,p(t,8,11));
 trials.forEach((o,i)=>{const value=[.18,.74,-.25][i]*run;o.dial.n.rotation.z=.5-value*1.8;o.slides.forEach((a,j)=>a.position.x=-.33+value*(j?1.3:1.8));o.a.rotation.z=-round*TAU*1.4;o.b.rotation.z=round*TAU*2.1-Math.PI/16;o.driver.rotation.z=-round*TAU*1.2;});syncWheel.rotation.z=-round*TAU*1.4;
 const pose=cameraAt(t);if(overview){pose.P=[23,18,29];pose.L=[5,2,-3];pose.f=38;}camera.position.fromArray(pose.P);camera.lookAt(new T.Vector3(...pose.L));camera.fov=pose.f;camera.updateProjectionMatrix();renderer.render(scene,camera);ctx.clearRect(0,0,W,H);ctx.drawImage(renderer.domElement,0,0,W,H);if(!overview)textOverlay(t);
 return {t,travel,clamp:closed,spread,round,case:mainCase.position.toArray(),copies:clones.map(o=>({visible:o.visible,p:o.position.toArray()})),camera:pose,parts:partCount,calls:renderer.info.render.calls,triangles:renderer.info.render.triangles};
};
window.capture=(type='image/png',quality=.97)=>canvas.toDataURL(type,quality);
window.sceneInfo={parts:partCount,three:T.REVISION,width:W,height:H,duration:12,style:'eighteenth-century-instrument'};
window.renderAt(0);window.ready=true;
