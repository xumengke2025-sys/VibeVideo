import * as THREE from '../vendor/three.module.js';
import {FILM,SHOTS,SOUNDS,clamp,ease,shotAt,subtitle} from './timeline.js';
const W=FILM.width,H=FILM.height;
const renderWidth=Number(new URLSearchParams(location.search).get('width')||W),renderScale=renderWidth/W;
if(![540,1080].includes(renderWidth))throw Error('Supported render widths: 540,1080');
const canvas=document.querySelector('#scene'),overlay=document.querySelector('#overlay');
overlay.width=renderWidth;overlay.height=H*renderScale;const ctx=overlay.getContext('2d');ctx.setTransform(renderScale,0,0,renderScale,0,0);
const output=document.createElement('canvas');output.width=renderWidth;output.height=H*renderScale;const oc=output.getContext('2d');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(1);renderer.setSize(renderWidth,H*renderScale,false);
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.25;
const scene=new THREE.Scene();scene.background=new THREE.Color('#e9e8df');
scene.add(new THREE.HemisphereLight(0xffffff,0x9fa698,2.3));
const sun=new THREE.DirectionalLight(0xfff4df,3.3);sun.position.set(-16,25,12);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.left=-55;sun.shadow.camera.right=55;sun.shadow.camera.top=55;sun.shadow.camera.bottom=-55;sun.shadow.camera.far=160;sun.shadow.bias=-.0004;sun.shadow.normalBias=.025;scene.add(sun);
const camera=new THREE.OrthographicCamera(-5,5,9,-9,.1,300);const dir=new THREE.Vector3(1,1,1).normalize();
const mat=(color,roughness=.65,metalness=0)=>new THREE.MeshStandardMaterial({color,roughness,metalness});
const M={base:mat('#d2d6cc'),rim:mat('#f8f6ea'),wall:mat('#c8d2c9'),steel:mat('#71837c',.34,.55),dark:mat('#304d4b'),gold:mat('#e9b458',.32,.25),blue:mat('#588f95',.25,.1),pipe:mat('#59968f',.42,.22),mud:mat('#8d7760'),sand:mat('#b69b69'),leaf:mat('#789b7a'),road:mat('#bbc4b8'),white:mat('#ffffff')};
const waterMat=color=>new THREE.MeshStandardMaterial({color,transparent:true,opacity:.67,roughness:.2,metalness:.1,depthWrite:false});
const tankWater=[waterMat('#778b71'),waterMat('#839b81'),waterMat('#689c8d'),waterMat('#639e95'),waterMat('#82b7b1')];
const ground=new THREE.Mesh(new THREE.PlaneGeometry(220,220),mat('#e9e8df'));ground.rotation.x=-Math.PI/2;ground.position.y=-.9;ground.receiveShadow=true;scene.add(ground);
function box(parent,w,h,d,x,y,z,m){const q=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);q.position.set(x,y,z);q.castShadow=true;q.receiveShadow=true;parent.add(q);return q}
function cyl(parent,r,h,x,y,z,m,r2=r,n=40){const q=new THREE.Mesh(new THREE.CylinderGeometry(r,r2,h,n),m);q.position.set(x,y,z);q.castShadow=true;q.receiveShadow=true;parent.add(q);return q}
function ball(parent,r,x,y,z,m){const q=new THREE.Mesh(new THREE.SphereGeometry(r,12,8),m);q.position.set(x,y,z);q.castShadow=true;parent.add(q);return q}
function pipe(parent,points,r,material){const curve=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p)),false,'centripetal');const q=new THREE.Mesh(new THREE.TubeGeometry(curve,72,r,10,false),material);q.castShadow=true;q.receiveShadow=true;parent.add(q);return curve}
function linePipe(parent,a,b,r,m){const v=new THREE.Vector3(...b).sub(new THREE.Vector3(...a));const q=cyl(parent,r,v.length(),...(new THREE.Vector3(...a).addScaledVector(v,.5).toArray()),m);q.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),v.normalize());return q}
function groundPos(sx,sy){return new THREE.Vector3(sx/Math.SQRT2-sy*Math.sqrt(1.5),0,-sx/Math.SQRT2-sy*Math.sqrt(1.5))}
const layout=[[0,-17],[0,-6],[.8,-1],[0,4],[.2,10],[0,15],[0,20]];
const stations=layout.map(([x,y],i)=>{const g=new THREE.Group();g.position.copy(groundPos(x,y));scene.add(g);box(g,7,.48,6,0,-.28,0,M.base);box(g,6.85,.12,5.85,0,0,0,M.rim);return g});
const anchors=[];function anchor(text,g,x,y,z,stages){anchors.push({text,g,p:new THREE.Vector3(x,y,z),stages})}
function rail(g,x1,z1,x2,z2,y=.6){const n=Math.ceil(Math.hypot(x2-x1,z2-z1)/.9);for(let i=0;i<=n;i++){const f=i/n;linePipe(g,[x1+(x2-x1)*f,y-.45,z1+(z2-z1)*f],[x1+(x2-x1)*f,y+.25,z1+(z2-z1)*f],.022,M.steel)}linePipe(g,[x1,y+.25,z1],[x2,y+.25,z2],.028,M.steel)}
function basin(g,w=5,d=3.7,wi=0){box(g,w,.16,d,0,.18,0,M.wall);box(g,w,1.35,.18,0,.89,-d/2,M.wall);box(g,.18,1.35,d,-w/2,.89,0,M.wall);box(g,w,.32,.15,0,.43,d/2,M.rim);box(g,.15,.32,d,w/2,.43,0,M.rim);box(g,w+.22,.12,.38,0,1.62,-d/2,M.rim);box(g,.38,.12,d,-w/2,1.62,0,M.rim);const water=box(g,w-.2,.045,d-.2,0,1.03,0,tankWater[wi]);water.castShadow=false;rail(g,-w/2-.1,-d/2-.1,w/2,-d/2-.1,2);return water}
function tree(g,x,z,s=1){cyl(g,.055,.55,x,.35,z,M.mud);const c=cyl(g,.36*s,.75*s,x,.9*s,z,M.leaf,.1,7);c.rotation.y=.4}
stations.forEach((g,i)=>{for(let j=0;j<3;j++)tree(g,2.9-j*.55,-2.55,.6);box(g,.6,.5,.45,-2.95,.3,2.3,M.steel);box(g,.45,.2,.04,-2.95,.38,2.55,M.gold);});
// 0: small cutaway bathroom and a transparent narrative cross-section of the drain.
const home=stations[0];box(home,3.8,.12,3.5,-.4,.2,-.1,M.white);box(home,3.8,2.7,.13,-.4,1.6,-1.85,M.rim);box(home,.13,2.7,3.5,-2.3,1.6,-.1,M.wall);
for(let i=0;i<7;i++){box(home,.015,.004,3.4,-2.1+i*.53,.265,-.1,M.wall);box(home,3.7,.004,.015,-.4,.265,-1.7+i*.53,M.wall)}
box(home,.9,.85,.4,-.4,1.08,-1.5,M.white);cyl(home,.38,.55,-.4,.62,-.82,M.white,.26);const seat=new THREE.Mesh(new THREE.TorusGeometry(.4,.08,12,36),M.rim);seat.rotation.x=-Math.PI/2;seat.scale.y=1.22;seat.position.set(-.4,.98,-.8);home.add(seat);cyl(home,.29,.04,-.4,.97,-.8,tankWater[4]);box(home,.13,.045,.055,-.05,1.52,-1.25,M.steel);
box(home,.95,.1,.5,-1.77,1.25,.68,M.white);linePipe(home,[-1.76,1.3,.52],[-1.76,1.65,.52],.035,M.steel);
// Simple rounded 2.5D cats; all character geometry is isolated here.
const catFur=mat('#eed4b0',.9),catGrey=mat('#b9ccc2',.9),catPink=mat('#dfaca5',.9),catEye=mat('#34433d',.9),catHat=mat('#efc76b',.85);
const catActors=[];
function catBall(parent,r,x,y,z,m,s=[1,1,1]){const q=new THREE.Mesh(new THREE.SphereGeometry(r,32,24),m);q.position.set(x,y,z);q.scale.set(...s);q.castShadow=true;parent.add(q);return q}
function cat(parent,x,y,z,{worker=false,seated=false,grey=false,scale=1}={}){
const g=new THREE.Group();g.position.set(x,y,z);g.rotation.y=.72;g.scale.setScalar(scale);parent.add(g);const fur=grey?catGrey:catFur;
catBall(g,.25,0,.34,0,fur,[.9,1.12,.72]);
const head=new THREE.Group();head.position.y=.77;head.rotation.x=-.12;g.add(head);catBall(head,.34,0,0,0,fur,[1.1,.93,.72]);
const eyes=[];
for(const side of [-1,1]){
const earShape=new THREE.Shape();earShape.moveTo(-.1,0);earShape.quadraticCurveTo(-.12,.03,-.075,.19);earShape.quadraticCurveTo(-.055,.245,0,.205);earShape.quadraticCurveTo(.1,.11,.11,0);earShape.closePath();
const ear=new THREE.Mesh(new THREE.ExtrudeGeometry(earShape,{depth:.065,bevelEnabled:true,bevelSegments:4,steps:1,bevelSize:.025,bevelThickness:.025,curveSegments:12}),fur);ear.position.set(side*.235,.2,-.055);ear.rotation.z=-side*.2;head.add(ear);
const eye=catBall(head,.032,side*.12,.005,.237,catEye,[.85,1.1,.35]);eyes.push(eye);
catBall(g,.09,side*.12,seated?-.035:.075,seated?.19:.04,fur,[1,.72,1.2]);
}
catBall(head,.021,0,-.064,.248,catPink,[1,.7,.38]);
const smile=new THREE.CatmullRomCurve3([new THREE.Vector3(-.047,-.098,.246),new THREE.Vector3(0,-.114,.251),new THREE.Vector3(.047,-.098,.246)]);head.add(new THREE.Mesh(new THREE.TubeGeometry(smile,16,.006,6,false),catEye));
const left=new THREE.Group();left.position.set(-.2,.45,0);g.add(left);const right=new THREE.Group();right.position.set(.2,.45,0);g.add(right);
for(const [arm,side] of [[left,-1],[right,1]])catBall(arm,.085,side*.035,-.105,.055,fur,[.78,1.55,.8]);
const tail=new THREE.Group();tail.position.set(0,.23,-.12);g.add(tail);pipe(tail,[[0,0,0],[.16,-.03,-.15],[.33,.08,-.18],[.35,.23,-.16]],.057,fur);
if(worker){const cap=new THREE.Mesh(new THREE.SphereGeometry(.285,32,16,0,Math.PI*2,0,Math.PI/2),catHat);cap.scale.set(1,.65,.87);cap.position.set(0,.22,-.015);head.add(cap);const brim=cyl(head,.3,.027,0,.223,-.015,catHat);brim.scale.z=.87;}
if(seated){left.rotation.x=-.4;right.rotation.x=-.4;}
catActors.push({g,head,right,tail,eyes,seated,worker});return g;
}
cat(home,-.4,.99,-.79,{seated:true,scale:1});
// 1: screening channel, steel bars and moving rake.
const screen=stations[1];basin(screen,5.3,3.5,0);
const bars=new THREE.Group();screen.add(bars);bars.position.set(0,0,0);for(let i=0;i<13;i++){linePipe(bars,[-.75,.24,-1.5+i*.25],[.2,2.25,-1.5+i*.25],.035,M.steel)}
box(screen,.4,.23,3.6,.25,2.35,0,M.dark);cyl(screen,.18,3.5,.25,2.5,0,M.steel).rotation.x=Math.PI/2;
const rake=new THREE.Group();screen.add(rake);box(rake,.16,.16,3.2,0,0,0,M.gold);for(let i=0;i<12;i++)box(rake,.3,.08,.045,.08,-.08,-1.4+i*.25,M.steel);
box(screen,1.3,.7,1.25,2,.58,1.55,M.dark);box(screen,1.1,.04,1.05,2,.95,1.55,M.mud);
const trash=[];for(let i=0;i<8;i++){const b=box(screen,.18,.08,.15,0,0,0,i%2?M.rim:M.gold);trash.push(b)}
anchor('格栅',screen,.05,2.3,-.6,['screen','arrival']);anchor('杂物收集',screen,2,1.05,1.5,['screen']);
cat(screen,2.8,.14,-.2,{worker:true,scale:1.15});
// 2: grit chamber with an exposed sloping bed and separate removal pipe.
const grit=stations[2];basin(grit,5.1,3.6,1);const sandBed=box(grit,3.9,.12,2.65,.1,.38,.15,M.sand);sandBed.rotation.z=-.07;
pipe(grit,[[1.5,.3,1],[2.6,.3,1],[3,.1,2.5]],.17,M.mud);const sand=[];for(let i=0;i<70;i++)sand.push(ball(grit,.045+(i%3)*.008,0,0,0,M.sand));anchor('砂粒沉底',grit,.7,.5,.8,['grit']);
cat(grit,2.9,.14,1.7,{worker:true,grey:true,scale:1.15});
// 3: biological reactor with diffuser grid and blower building.
const bio=stations[3];basin(bio,5.25,3.7,2);
for(let j=0;j<4;j++){linePipe(bio,[-2,.38,-1.35+j*.85],[2,.38,-1.35+j*.85],.055,M.steel);for(let i=0;i<6;i++)cyl(bio,.085,.06,-1.8+i*.7,.43,-1.35+j*.85,M.dark)}
box(bio,1,.75,1,-2.7,.53,2,M.dark);for(let i=0;i<5;i++)box(bio,.75,.04,.04,-2.7,.38+i*.11,2.52,M.steel);pipe(bio,[[-2.7,.8,2],[-2.7,1.8,2],[-1.6,1.8,2],[-1.6,.4,1]],.075,M.gold);
const bubbles=[];const bm=new THREE.MeshStandardMaterial({color:'#dfede4',transparent:true,opacity:.72,roughness:.15});for(let i=0;i<100;i++)bubbles.push(ball(bio,.035+(i%5)*.009,0,0,0,bm));
anchor('曝气供氧',bio,-1,1.5,-.5,['bio']);
cat(bio,2.9,.14,1.65,{worker:true,grey:true,scale:1.15});
// 4: circular secondary clarifier, exposed front wall, rotating scraper and weir.
const clar=stations[4];cyl(clar,2.55,.22,0,.2,0,M.wall);cyl(clar,2.32,.08,0,.37,0,M.mud);
const wall=new THREE.Mesh(new THREE.CylinderGeometry(2.51,2.51,1.2,80,1,true,Math.PI*.5,Math.PI),M.wall);wall.position.y=.94;wall.castShadow=true;clar.add(wall);
const ring=new THREE.Mesh(new THREE.TorusGeometry(2.5,.1,8,80),M.rim);ring.rotation.x=-Math.PI/2;ring.position.y=1.56;clar.add(ring);
const cw=cyl(clar,2.36,.025,0,1.13,0,tankWater[3]);cw.castShadow=false;
cyl(clar,.25,1.85,0,1.1,0,M.steel);cyl(clar,.45,.14,0,2.1,0,M.rim);
const bridge=new THREE.Group();clar.add(bridge);box(bridge,4.8,.12,.44,0,1.79,0,M.steel);rail(bridge,-2.35,-.22,2.35,-.22,2.32);
const scraper=new THREE.Group();clar.add(scraper);box(scraper,4.1,.14,.13,0,.5,0,M.dark);linePipe(scraper,[0,.5,0],[0,1.7,0],.06,M.steel);
const sludge=[];for(let i=0;i<85;i++)sludge.push(ball(clar,.06+(i%4)*.018,0,0,0,M.mud));
anchor('上层水流出',clar,2.15,1.3,.2,['settle']);anchor('污泥沉底',clar,.2,.55,1.7,['settle']);
cat(clar,-2.9,.14,1.85,{worker:true,scale:1.15});
// 5: granular filter and baffled chlorine contact tank.
const polish=stations[5];basin(polish,5.2,3.8,4);box(polish,.16,1.3,3.6,-.9,.88,0,M.rim);
for(let i=0;i<4;i++)box(polish,1.5,.13,3.35,-1.8,.4+i*.14,0,i%2?M.sand:M.mud);
for(let i=0;i<3;i++)box(polish,.13,1.03,2.8,-.2+i*.85,.8,i%2?.35:-.35,M.rim);
box(polish,.68,.95,.62,2.8,.6,-2.15,M.dark);cyl(polish,.22,.42,2.8,1.28,-2.15,M.gold);pipe(polish,[[2.8,1.28,-2.15],[2.8,1.5,-1],[2,1.5,-1]],.035,M.steel);
anchor('过滤',polish,-1.8,1.6,0,['polish']);anchor('消毒接触池',polish,1.3,1.6,0,['polish']);
cat(polish,2.9,.14,1.8,{worker:true,grey:true,scale:1.15});
// 6: discharge channel, river and monitoring kiosk.
const outlet=stations[6];box(outlet,6,.12,2.35,0,.18,.6,tankWater[4]);box(outlet,6,.16,.2,0,.23,-.65,M.wall);box(outlet,6,.16,.2,0,.23,1.87,M.wall);box(outlet,1.1,1.35,.8,-1.8,.77,-1.6,M.rim);box(outlet,.75,.38,.035,-1.8,1,-1.18,M.dark);linePipe(outlet,[-.8,.3,-1.6],[-.8,1.2,-1.6],.05,M.steel);anchor('出水监测',outlet,-1.5,1.5,-1.6,['out']);
cat(outlet,2.6,.14,-1.8,{worker:true,scale:1.15});
// Pipes retain physical connectivity, and moving pulses are explicitly flow markers.
const flows=[];for(let i=0;i<6;i++){const a=stations[i].position.clone().add(new THREE.Vector3(-2.3,.55,-1.2)),b=stations[i+1].position.clone().add(new THREE.Vector3(2.3,.55,1.2));const mid=a.clone().lerp(b,.5);let points=[a.toArray(),[a.x,.55,mid.z],[b.x,.55,mid.z],b.toArray()];if(i===0){const h=home.position;points=[[h.x-.4,.55,h.z-.8],[h.x-.4,-.5,h.z-.8],[h.x+1.5,-.5,h.z+2.8],[h.x+4.2,-.5,h.z+2.8],[mid.x+4,-.5,mid.z+4],[b.x,-.5,b.z+1.4],b.toArray()]}
const curve=pipe(scene,points,.16,M.pipe);flows.push({curve,type:'water',start:[1.4,13,17,24,30,40][i],inlet:i===0});}
anchor('地下排水管',scene,...flows[0].curve.getPointAt(.48).toArray(),['arrival']);
const a=clar.position.clone().add(new THREE.Vector3(2.2,.38,1.4)),b=bio.position.clone().add(new THREE.Vector3(2.2,.6,1.4));
const returnCurve=pipe(scene,[a.toArray(),[a.x+4,.38,a.z+1],[b.x+4,.38,b.z+1],b.toArray()],.12,M.mud);flows.push({curve:returnCurve,type:'return',start:31});
const sludgeDest=clar.position.clone().add(new THREE.Vector3(4,.1,4));const wasteGroup=new THREE.Group();wasteGroup.position.copy(sludgeDest);scene.add(wasteGroup);box(wasteGroup,1.8,.25,2.2,0,0,0,M.base);cyl(wasteGroup,.66,1,0,.65,0,M.dark);cyl(wasteGroup,.57,.07,0,1.17,0,M.mud);
const wasteCurve=pipe(scene,[[a.x,.3,a.z],[a.x+1,.3,a.z+.5],[sludgeDest.x,.45,sludgeDest.z]],.1,M.mud);flows.push({curve:wasteCurve,type:'waste',start:34});anchor('污泥处理',wasteGroup,0,1.5,0,['return']);
const pulseMat=new THREE.MeshBasicMaterial({color:'#f1bf58'});const pulses=[];flows.forEach((f,i)=>{for(let k=0;k<5;k++){const p=ball(scene,f.type==='water'?.205:.18,0,0,0,pulseMat);p.castShadow=false;pulses.push({p,f,k})}});
// A handful of patterned particles make treatment processes legible without color magic.
const riverLines=[];for(let i=0;i<12;i++)riverLines.push(box(outlet,.25,.012,.025,0,.27,0,M.rim));
const tmp=new THREE.Vector3();function project(g,p){g.localToWorld(tmp.copy(p));tmp.project(camera);return [(tmp.x+1)*W/2,(1-tmp.y)*H/2]}
function rounded(x,y,w,h,r){ctx.beginPath();ctx.roundRect(x,y,w,h,r)}
function text(s,x,y,size=42,color='#274843',align='left',weight=500){ctx.fillStyle=color;ctx.font=`${weight} ${size}px "Microsoft YaHei", sans-serif`;ctx.textAlign=align;ctx.fillText(s,x,y)}
function micro(t){const a=ease((t-20)/.45)*(1-ease((t-24.1)/.45));if(a<=0)return;ctx.save();ctx.globalAlpha=a;const x=540,y=800,r=288;ctx.fillStyle='#f4f3e9';ctx.strokeStyle='#9caf9e';ctx.lineWidth=3;ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();ctx.stroke();text('微观示意',x,y-r+56,29,'#70847a','center');
for(let i=0;i<7;i++){const ang=i*2.399,rr=65+(i%3)*48;const bx=x+Math.cos(ang)*rr,by=y+Math.sin(ang)*rr+30;ctx.save();ctx.translate(bx,by);ctx.rotate(ang+t*.12);ctx.fillStyle='#739e81';rounded(-32,-14,64,28,14);ctx.fill();for(let k=0;k<3;k++){ctx.fillStyle='#c4d7b8';ctx.beginPath();ctx.arc(-15+k*15,0,3,0,7);ctx.fill()}ctx.restore();
const p=(t*.32+i*.143)%1,px=bx+Math.cos(ang)*110*(1-p),py=by+Math.sin(ang)*110*(1-p);ctx.fillStyle='#b78b57';ctx.globalAlpha=a*(1-ease((p-.7)/.3));ctx.beginPath();ctx.arc(px,py,8,0,7);ctx.fill();ctx.globalAlpha=a;
}
for(let i=0;i<10;i++){const q=(t*.23+i*.1)%1;const bx=x-190+i*42,by=y+180-q*280;ctx.strokeStyle='#85b5b4';ctx.lineWidth=2;ctx.beginPath();ctx.arc(bx,by,7,0,7);ctx.stroke()}
text('微生物',x-180,y+r-58,28,'#567c65');text('有机污染物',x+18,y+r-58,28,'#9e784f');ctx.restore()}
function drawOverlay(t){ctx.clearRect(0,0,W,H);const top=ctx.createLinearGradient(0,220,0,430);top.addColorStop(0,'#e9e8df');top.addColorStop(1,'#e9e8df00');ctx.fillStyle=top;ctx.fillRect(0,0,W,430);const bottom=ctx.createLinearGradient(0,1420,0,1530);bottom.addColorStop(0,'#e9e8df00');bottom.addColorStop(1,'#e9e8df');ctx.fillStyle=bottom;ctx.fillRect(0,1420,W,500);const s=shotAt(t);text('污水处理流程',76,170,43,'#28483f','left',600);text(String(SHOTS.indexOf(s)+1).padStart(2,'0')+' / 09',1004,170,25,'#77867a','right');
ctx.strokeStyle='#cbd1c3';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(76,240);ctx.lineTo(1004,240);ctx.stroke();ctx.strokeStyle='#b08b45';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(76,240);ctx.lineTo(76+928*t/FILM.duration,240);ctx.stroke();
for(const label of anchors){if(!label.stages.includes(s.id)||(label.text==='污泥处理'&&t<34)||(s.id==='bio'&&t>20&&t<24.6))continue;const [x,y]=project(label.g,label.p);if(x<90||x>990||y<340||y>1430)continue;ctx.font='500 31px "Microsoft YaHei", sans-serif';const width=ctx.measureText(label.text).width+36;ctx.fillStyle='#f8f7eeed';rounded(x-width/2,y-38,width,54,8);ctx.fill();text(label.text,x,y,31,'#315348','center')}
if(t>=31&&t<34){const p=returnCurve.getPointAt(.62).project(camera),x=(p.x+1)*W/2,y=(1-p.y)*H/2;ctx.fillStyle='#faf8ee';rounded(x-195,y-44,242,55,9);ctx.fill();text('回流至生物池',x-75,y-7,30,'#876a38','center')}
micro(t);
const lines=subtitle(t);ctx.fillStyle='#e9e8dff2';rounded(55,1515,970,190,20);ctx.fill();lines.forEach((line,i)=>text(line,540,1632+i*80,66,'#26463e','center',600));
text('典型流程示意 · 时间与尺度压缩',540,1810,25,'#738277','center');
if(t>=4&&t<9)text('流向示意',540,1420,29,'#977639','center');
if(t>=41)text('达标排放 ≠ 直接饮用',540,1750,34,'#977639','center');
}
const camKeys=[
[0,0,13],[2.4,0,13],[4,.12,15],[6.1,.48,16],[8.2,.88,17],[9.6,1,14],[13.3,1,14],[14.8,2,14],[17.3,2,14],[18.8,3,14.5],[24.4,3,14.5],[25.8,4,14.5],[30.5,4,14.5],[32.2,3.55,26],[35.5,3.55,26],[36.8,5,14.5],[40.5,5,14.5],[42,6,17],[43.7,3,55],[45,3,55]];
function pose(t){let i=0;while(i<camKeys.length-2&&t>camKeys[i+1][0])i++;const a=camKeys[i],b=camKeys[i+1],u=ease((t-a[0])/(b[0]-a[0]));const index=a[1]+(b[1]-a[1])*u,lo=Math.floor(index),hi=Math.ceil(index);const target=stations[lo].position.clone().lerp(stations[hi].position,index-lo);if(t>=2.5&&t<=9.3){const track=flows[0].curve.getPointAt(clamp((t-1.4)/7.6));const follow=ease((t-2.5)/1)*(1-ease((t-8.6)/.7));target.lerp(track,follow)}target.y=.6;const span=a[2]+(b[2]-a[2])*u;target.addScaledVector(new THREE.Vector3(-1,2,-1).normalize(),-span*.04);return {target,span}}
function update(t){const {target,span}=pose(t);camera.left=-span*W/H/2;camera.right=span*W/H/2;camera.top=span/2;camera.bottom=-span/2;camera.position.copy(target).addScaledVector(dir,90);camera.lookAt(target);camera.updateProjectionMatrix();
stations.forEach((g,i)=>{const reveal=ease((t-(i===0?-1:3+i*.45))/.7);g.scale.y=.02+.98*reveal});
const rp=((Math.max(0,t-9))%2.5)/2.5;rake.position.set(-.65+rp*.9,.4+rp*1.85,0);
trash.forEach((q,i)=>{const f=((Math.max(0,t-9)+i*.03)%2.5)/2.5;q.rotation.y=i+t*.05;const z=-1.25+i*.34;if(f<.22){q.position.set(-2.15+f/.22*1.5,1.06,z)}else if(f<.77){const u=(f-.22)/.55;q.position.set(-.65+u*.9,1.06+u*1.28,z)}else{const u=(f-.77)/.23;q.position.set(.25+u*1.75,2.34-u*u*1.35,z+(1.5-z)*u)}});
sand.forEach((q,i)=>{const p=clamp((t-14)*.24+i*.012);q.position.set(-1.9+(i%10)*.39,.42+(1-p)*.61,-1.45+Math.floor(i/10)*.44)});
bubbles.forEach((q,i)=>{const p=(t*.57+i*.131)%1;q.position.set(-1.95+(i%10)*.43,.42+p*.82,-1.4+Math.floor(i/10)*.3);q.scale.setScalar(.55+p*.65)});
sludge.forEach((q,i)=>{const ang=i*2.399,r=.45+(i%11)*.15;const p=clamp((t-25.5)/4.5+(i%7)*.055);q.position.set(Math.cos(ang)*r,.46+(1-p)*.59,Math.sin(ang)*r)});scraper.rotation.y=t*.1;bridge.rotation.y=t*.055;
pulses.forEach(({p,f,k})=>{p.visible=t>=f.start;let u=((t-f.start)*.28+k*.2)%1;if(f.inlet){p.visible=p.visible&&k===0;u=clamp((t-1.4)/7.6);p.scale.setScalar(1.35)}if(p.visible)p.position.copy(f.curve.getPointAt(u));if(f.type!=='water')p.visible=p.visible&&t<41});
catActors.forEach((actor,i)=>{actor.head.rotation.z=Math.sin(t*1.7+i)*.045;actor.head.rotation.y=Math.sin(t*.8+i)*.065;actor.tail.rotation.y=Math.sin(t*1.5+i)*.14;const blink=((t+i*.71)%4.1);const open=1-.92*Math.max(0,1-Math.abs(blink-3.7)/.12);actor.eyes.forEach(eye=>eye.scale.y=1.1*open);if(actor.worker)actor.right.rotation.z=Math.sin(t*1.2+i)*.13;});
riverLines.forEach((q,i)=>q.position.set(-2.9+((t*.7+i*.48)%5.8),.28,-.4+(i%4)*.58));
scene.updateMatrixWorld(true);renderer.render(scene,camera);drawOverlay(t)}
window.DEMO=FILM;window.__ready=false;
window.__renderBuffers=()=>({logical:[W,H],scene:[canvas.width,canvas.height],overlay:[overlay.width,overlay.height],output:[output.width,output.height]});
window.renderAt=async(t,type='image/png',quality=.97)=>{t=clamp(t,0,FILM.duration-1/300);update(t);oc.drawImage(canvas,0,0);oc.drawImage(overlay,0,0);return output.toDataURL(type,quality)};
window.stateAt=t=>({shot:shotAt(t).id,subtitle:subtitle(t),camera:pose(t).target.toArray(),span:pose(t).span});
await document.fonts.ready;await window.renderAt(0);window.__ready=true;
const renderMode=location.search.includes('render');document.querySelector('#seek').max=FILM.duration-.01;if(renderMode)document.querySelector('#controls').style.display='none';else{let playing=false,last=0,t=0;const audio=new Audio('audio/mix.wav');document.querySelector('#play').onclick=()=>{playing=!playing;if(playing){audio.currentTime=t;audio.play().catch(()=>{});}else audio.pause()};document.querySelector('#seek').oninput=e=>{t=+e.target.value;audio.currentTime=t;update(t)};function tick(now){if(playing){t=Math.min(FILM.duration-.01,t+(now-last)/1000);update(t);document.querySelector('#seek').value=t;document.querySelector('#clock').textContent=t.toFixed(1);if(t>=FILM.duration-.01){playing=false;audio.pause()}}last=now;requestAnimationFrame(tick)}requestAnimationFrame(tick)}
