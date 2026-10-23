import * as T from 'three';
import {mergeGeometries} from 'three/addons/utils/BufferGeometryUtils.js';
import {rng,V,seg,mix} from './math.js';
const random=rng(74291);
const R=(a,b)=>mix(a,b,random());
const mats={};
// Repeating baked colour + bump maps, dimensioned in world metres, with stable brick variation.
function masonry(name,base,glaze=false){
 const c=document.createElement('canvas');c.width=c.height=1024;const g=c.getContext('2d');g.fillStyle=glaze?'#273c46':'#8c7658';g.fillRect(0,0,1024,1024);
 const col=new T.Color(base),rows=24,cols=8,h=1024/rows,w=1024/cols;
 for(let j=0;j<rows;j++)for(let i=-1;i<cols+1;i++){const x=i*w+(j%2)*w/2,y=j*h;const n=R(.83,1.13);g.fillStyle='#'+col.clone().multiplyScalar(n).getHexString();g.fillRect(x+2,y+2,w-4,h-4);g.fillStyle='rgba(255,235,190,.15)';g.fillRect(x+3,y+3,w-6,2);g.fillStyle='rgba(20,18,15,.18)';g.fillRect(x+3,y+h-5,w-6,2);}
 for(let i=0;i<45000;i++){g.fillStyle=random()<.5?'rgba(255,245,218,.06)':'rgba(35,25,20,.07)';g.fillRect(R(0,1024),R(0,1024),R(.5,2.5),R(.5,2));}
 const tex=new T.CanvasTexture(c);tex.wrapS=tex.wrapT=T.RepeatWrapping;tex.colorSpace=T.SRGBColorSpace;tex.anisotropy=8;
 const bump=tex.clone();bump.colorSpace=T.NoColorSpace;bump.needsUpdate=true;
 return mats[name]=new T.MeshStandardMaterial({map:tex,bumpMap:bump,bumpScale:glaze?.035:.085,roughness:glaze?.31:.92,metalness:glaze?.13:0});
}
function mat(n,c,r=.8,m=0){return mats[n]=new T.MeshStandardMaterial({color:c,roughness:r,metalness:m})}
export function buildWorld(scene){
 masonry('brick','#c39c6c');masonry('brick2','#b99063');masonry('cream','#d9b986');masonry('blue','#126293',true);masonry('darkblue','#15446e',true);
 mat('gold','#c3a45a',.36,.65);mat('bronze','#657365',.35,.72);mat('wood','#73513a');mat('dark','#392d24');mat('roof','#c7ac85');mat('cloth','#b55f40');mat('cloth2','#d1b98b');mat('leaf','#557447');mat('leaf2','#788858');mat('trunk','#7a6242');mat('terra','#af704e');mat('sand','#b3a080');mat('black','#292c2c');mat('skin','#b18b64');mat('linen','#e6cf9b');
 const bank=new Map();let dynamic=null;
 const add=(geo,m,p=[0,0,0],rot=[0,0,0],sc=[1,1,1])=>{geo.rotateX(rot[0]);geo.rotateY(rot[1]);geo.rotateZ(rot[2]);geo.scale(...sc);geo.translate(...p);if(dynamic){const ob=new T.Mesh(geo,mats[m]||m);ob.castShadow=true;ob.receiveShadow=true;dynamic.add(ob);return ob}if(!bank.has(m))bank.set(m,[]);bank.get(m).push(geo)};
 function box(x,y,z,w,h,d,m){const geo=new T.BoxGeometry(w,h,d);const p=geo.attributes.position,n=geo.attributes.normal,uv=geo.attributes.uv;for(let i=0;i<p.count;i++){const nx=Math.abs(n.getX(i)),ny=Math.abs(n.getY(i));uv.setXY(i,(nx>.5?p.getZ(i):p.getX(i))/4,(ny>.5?p.getZ(i):p.getY(i))/4)}return add(geo,m,[x,y,z]);}
 const ell=(x,y,z,a,b,c,m)=>add(new T.SphereGeometry(1,12,8),m,[x,y,z],[0,0,0],[a,b,c]);
 const cyl=(x,y,z,a,b,h,m,n=12)=>add(new T.CylinderGeometry(a,b,h,n),m,[x,y,z]);
 function tube(points,r,m,segments=20){return add(new T.TubeGeometry(new T.CatmullRomCurve3(points.map(p=>V(...p))),segments,r,6,false),m)}
 function jar(x,y,z,s=1){const pts=[[.15,0],[.22,.06],[.36,.2],[.4,.53],[.31,.78],[.18,.87],[.17,1],[.22,1.03]].map(([r,h])=>new T.Vector2(r*s,h*s));add(new T.LatheGeometry(pts,12),'terra',[x,y,z]);cyl(x,y+1.02*s,z,.17*s,.17*s,.018*s,'dark');}
 function crenel(x,y,z,w,d,m){box(x,y,z,w,.32,d,m);for(let u=-w/2+.45;u<w/2;u+=1.35){box(x+u,y+.55,z-d/2+.22,.6,.85,.5,m);box(x+u,y+.55,z+d/2-.22,.6,.85,.5,m)}for(let u=-d/2+.8;u<d/2;u+=1.35){box(x-w/2+.22,y+.55,z+u,.5,.85,.6,m);box(x+w/2-.22,y+.55,z+u,.5,.85,.6,m)}}
 function palm(x,z,h=7,y=0){
 const lean=R(-.5,.5);tube([[x,y,z],[x+.15,y+h*.4,z],[x+lean,y+h,z]],.19,'trunk',15);
 for(let i=0;i<16;i++){const q=i/16;add(new T.TorusGeometry(.2+q*.012,.032,4,8),'trunk',[x+lean*q,y+h*q,z],[Math.PI/2,0,0])}
 for(let k=0;k<10;k++){const a=k*Math.PI*2/10+R(0,.15),len=R(2,3.6),pts=[];for(let j=0;j<9;j++){const u=j/8;pts.push([x+lean+Math.cos(a)*len*u,y+h+1.7*Math.sin(u*2.6)-u*.9,z+Math.sin(a)*len*u])}tube(pts,.035,'leaf2',10);
 const pp=[],ii=[];for(let j=1;j<9;j++){const u=j/9;const mid=V(x+lean+Math.cos(a)*len*u,y+h+1.7*Math.sin(u*2.6)-u*.9,z+Math.sin(a)*len*u),width=.62*Math.sin(u*Math.PI);for(const s of [-1,1]){const end=mid.clone().add(V(Math.cos(a+s*1.05)*width,-.17,Math.sin(a+s*1.05)*width));const base=mid.clone().add(V(-Math.cos(a)*.13,.02,-Math.sin(a)*.13));let n=pp.length/3;pp.push(...base,...end,...mid.clone().add(V(Math.cos(a)*.18,0,Math.sin(a)*.18)));ii.push(n,n+1,n+2,n+2,n+1,n)}}const gg=new T.BufferGeometry();gg.setAttribute('position',new T.Float32BufferAttribute(pp,3));gg.setIndex(ii);gg.computeVertexNormals();add(gg,k%2?'leaf':'leaf2');}
 }
 // City banks and the long, sunken canal remain the same through every camera move.
 box(0,-2,0,160,2,330,'sand');box(-36,-.35,-27,60,3,182,'brick');box(39,-.35,-27,66,3,182,'brick');
 box(-6.1,.95,-27,.6,.45,183,'cream');box(6.1,.95,-27,.6,.45,183,'cream');
 const waterMat=new T.MeshStandardMaterial({color:'#407d7f',metalness:.45,roughness:.24});
 waterMat.onBeforeCompile=s=>{s.uniforms.uTime={value:0};waterMat.userData.shader=s;s.fragmentShader=s.fragmentShader.replace('#include <common>','#include <common>\nuniform float uTime;').replace('#include <normal_fragment_maps>','#include <normal_fragment_maps>\nnormal = normalize(normal + vec3(sin(vViewPosition.x*1.3+uTime*.8)*.045,cos(vViewPosition.y*2.3-uTime*.6)*.04,0.0));');};
 const water=new T.Mesh(new T.PlaneGeometry(12,310),waterMat);water.rotation.x=-Math.PI/2;water.position.set(0,.4,-22);scene.add(water);
 // A gently irregular sand ridge provides true foreground occlusion at the opening.
 const ridgeG=new T.PlaneGeometry(700,220,100,38);ridgeG.rotateX(-Math.PI/2);const pa=ridgeG.attributes.position;for(let i=0;i<pa.count;i++){let x=pa.getX(i),z=pa.getZ(i)+140;let y=18*Math.exp(-Math.pow((z-145)/24,2))*(.97+.035*Math.sin(x*.035))+.32*Math.sin(x*.12+z*.025);pa.setXYZ(i,x,y-1,z)}ridgeG.computeVertexNormals();add(ridgeG,'sand');
 // Outer walls, repeated buttresses, masonry cornices.
 for(const side of [-1,1]){const x=side<0?-38:39;box(x,4,37,side<0?48:54,6,3,'brick2');for(let u=x-(side<0?24:27);u<x+(side<0?24:27);u+=4){box(u,4,38.9,.8,6.5,1.1,'brick');box(u,7.4,37,1,.9,3,'brick')}box(x,6.6,38.55,side<0?48:54,.25,.2,'cream')}
 for(const x of [-64,70]){box(x,3,-30,2,6,138,'brick2');for(let z=-98;z<40;z+=3)box(x,6.4,z,2,1,1.2,'brick')}
 // Ishtar-inspired gate: two rectangular glazed towers, real opening, glazed relief bands.
 const gx=-14,gz=34;
 for(const x of [gx-6,gx+6]){box(x,7.8,gz,7,14.5,8,'blue');box(x,1.7,gz,7.8,2,8.8,'darkblue');box(x,13.1,gz,7.5,.6,8.5,'gold');box(x,13.6,gz,7.6,.35,8.6,'cream');crenel(x,15.1,gz,7.5,8.5,'blue');
 for(const y of [4,7.8,11.2])for(const xx of [-2,0,2]){ell(x+xx,y,gz+4.04,.44,.21,.085,'gold');ell(x+xx+.33,y+.2,gz+4.06,.15,.2,.1,'gold');for(const dd of [-.25,.25])box(x+xx+dd,y-.29,gz+4.06,.09,.32,.1,'gold');tube([[x+xx-.35,y+.08,gz+4.08],[x+xx-.62,y+.35,gz+4.08],[x+xx-.6,y+.5,gz+4.08]],.035,'gold',5)}
 for(let y=2;y<13;y+=1.15){box(x-3.1,y,gz+4.06,.28,.6,.08,'cream');box(x+3.1,y,gz+4.06,.28,.6,.08,'cream')}
 }
 // Curved arch with voussoirs, rather than a painted dark rectangle.
 for(let i=0;i<22;i++){const a=i/22*Math.PI,b=(i+1)/22*Math.PI;const sh=new T.Shape();sh.moveTo(Math.cos(a)*2.6,Math.sin(a)*2.6);sh.lineTo(Math.cos(b)*2.6,Math.sin(b)*2.6);sh.lineTo(Math.cos(b)*3.6,Math.sin(b)*3.6);sh.lineTo(Math.cos(a)*3.6,Math.sin(a)*3.6);sh.closePath();add(new T.ExtrudeGeometry(sh,{depth:5,bevelEnabled:false}),i%4===0?'gold':'blue',[gx,6,gz-2.5])}box(gx,11.1,gz,6,4,5,'blue');box(gx,13.2,gz,6.4,.4,5.4,'gold');
 // Processional avenue leading inward from the gate, bridged at two points.
 box(-14,1.22,8,8,.18,50,'cream');
 function bridge(z){for(let i=0;i<14;i++){const x=-7+i;const y=1.4+1.6*Math.sin((i+.5)/14*Math.PI);box(x+.5,y,z,1.01,.45,5,'cream');for(const s of [-1,1]){box(x+.5,y+.8,z+s*2.4,1.02,.18,.24,'cream');if(i%2===0)box(x+.5,y+.4,z+s*2.4,.18,.85,.26,'brick')}}for(const x of [-6,6])box(x,1.2,z,1.5,2,5,'brick')}
 bridge(17);bridge(-40);
 function house(x,z,w,d,h,idx){const m=idx%3===0?'brick2':'brick';box(x,1.2+h/2,z,w,h,d,m);box(x,1.22+h,z,w+.3,.3,d+.3,'roof');for(const s of [-1,1]){box(x+s*(w/2-.12),1.6+h,z,.25,.65,d,m);box(x,1.6+h,z+s*(d/2-.12),w,.65,.25,m)}
 for(let xx=x-w/2+1;xx<x+w/2-.3;xx+=1.8){box(xx,2.7,z+d/2+.02,.55,1,.05,'dark');box(xx,3.27,z+d/2+.06,.8,.13,.13,'wood');for(let k=-1;k<=1;k++)box(xx+k*.15,2.7,z+d/2+.07,.05,.95,.1,'wood');if(h>5)box(xx,h-.1,z+d/2+.02,.5,.8,.05,'dark')}
 box(x,2.2,z+d/2+.04,1.1,2,.08,'wood');box(x,3.25,z+d/2+.15,1.35,.2,.35,'cream');
 if(idx%3===0){box(x+.8,1.65+h,z-.6,1.6,.5,2,'cream');box(x+.8,1.92+h,z-.6,1.2,.05,1.6,'dark');}
 for(let k=0;k<(idx%3)+1;k++)jar(x-w*.3+k*.65,1.4+h,z-d*.25,.55);
 if(idx%4===0){const cloth=new T.PlaneGeometry(w*.85,2.8,8,8);const v=cloth.attributes.position;for(let i=0;i<v.count;i++)v.setZ(i,.18*Math.cos(v.getX(i)*3)-.35*Math.cos(v.getY(i)*.8));cloth.computeVertexNormals();add(cloth,idx%8?'cloth':'cloth2',[x,3.7,z+d/2+1.3],[-1.25,0,0]);for(const s of [-1,1])cyl(x+s*w*.4,2.25,z+d/2+2.4,.055,.055,2.3,'wood')}
 }
 let hi=0;for(let z=-94;z<29;z+=13)for(let x=-55;x<64;x+=12){if(Math.abs(x)<10||Math.abs(x+14)<5||((x>1)&&(z<-25&&z>-90)))continue;house(x+R(-1,1),z+R(-1,1),R(6,9.5),R(6,9),R(3.5,7.8),hi++);if(hi%4===0)palm(x+5,z+4,R(6,8))}
 // Ziggurat: seven nested terraces, inset buttresses and blue/gold friezes.
 const tx=26,tz=-58;
 for(let k=0;k<7;k++){const w=51-k*6,d=46-k*5.4,y=1.3+k*4.2;box(tx,y+2.1,tz,w,4.2,d,k%3===1?'brick2':'brick');box(tx,y+4.16,tz,w+.6,.3,d+.6,'cream');box(tx,y+3.5,tz+d/2+.08,w,.38,.2,'blue');for(let x=-w/2+1;x<w/2;x+=3.2){box(tx+x,y+1.9,tz+d/2+.18,.6,3.7,.5,'brick2');box(tx+x,y+3.53,tz+d/2+.23,.25,.23,.2,'gold')}for(let z=-d/2+1;z<d/2;z+=3.2)box(tx-w/2-.18,y+1.9,tz+z,.5,3.7,.6,'brick2');}
 box(tx,33.3,tz,10,5.3,9,'blue');box(tx,36,tz,11,.5,10,'gold');crenel(tx,36.5,tz,11,10,'blue');box(tx,32.2,tz+4.56,2.5,3.9,.08,'dark');for(const x of [-4,4])box(tx+x,33,tz+4.8,.6,5,.65,'gold');
 for(let k=0;k<63;k++){const y=1.3+k*.46,z=-22-k*.51;box(tx,y+.2,z,4.5,.45,.6,'cream');for(const x of [-2.5,2.5])box(tx+x,y+.45,z,.4,.9,.6,'brick')}
 // Foreground temple terrace: beacon and landing plane both at y=9.8.
 box(11,5.2,-30,18,9.2,13,'brick');box(11,9.86,-30,18.6,.28,13.6,'cream');for(const z of [-36.5,-23.5])for(let x=2.5;x<20;x+=2.6){box(x,10.3,z,.45,.65,.5,'cream');box(x,10.7,z,2.6,.16,.4,'cream')}
 for(let x=3;x<20;x+=2){box(x,8.4,-23.42,.45,1.8,.3,'blue');box(x,9.3,-23.4,1.5,.24,.4,'gold')}
 for(const p of [[4,-33],[18,-33]])palm(...p,5.8,10);
 // Inlaid floor radial stonework makes the contact plane legible.
 const beacon=V(10,10,-28);
 for(let i=0;i<48;i++){const a=i*Math.PI/24;box(10+Math.cos(a)*2.1,10.02,-28+Math.sin(a)*2.1,.14,.015,.14,i%2?'gold':'blue')}
 const bowlPoints=[[0,0],[.56,0],[.58,.16],[.31,.28],[.25,1.06],[.42,1.16],[.52,1.24],[1.02,1.6],[1.12,1.86],[1.03,1.91],[.86,1.6],[.32,1.36],[0,1.35]].map(p=>new T.Vector2(...p));add(new T.LatheGeometry(bowlPoints,48),'bronze',beacon.toArray());
 for(let i=0;i<24;i++){const a=i*Math.PI/12;ell(10+Math.cos(a)*1.07,11.84,-28+Math.sin(a)*1.07,.07,.055,.07,'gold')}
 const lamps=[];for(let i=0;i<46;i++){const z=-40+i*1.65;for(const side of [-1,1]){const x=side*7.5;cyl(x,2.1,z,.065,.09,2.1,'bronze');cyl(x,3.1,z,.32,.16,.3,'gold');const m=new T.MeshStandardMaterial({color:'#ca9d55',emissive:'#ff9b31',emissiveIntensity:0,roughness:.4});const globe=new T.Mesh(new T.SphereGeometry(.23,8,6),m);globe.position.set(x,3.35,z);scene.add(globe);lamps.push({m,t:36+i/45*12,position:globe.position})}}
 for(let i=0;i<12;i++)palm(i%2?-8.8:8.8,-30+i*5.3,R(6,8));
 // Dynamic boats, residents and cloth have their own quantized background clock.
 const boats=[];for(let i=0;i<6;i++){dynamic=new T.Group();const hullPts=[[0,0],[.5,.1],[.8,.5],[.72,.65]].map(p=>new T.Vector2(...p));add(new T.LatheGeometry(hullPts,16),'wood',[0,0,0],[Math.PI/2,0,0],[1,3.2,1]);box(0,.1,0,1.2,.18,3.7,'wood');jar(0,.22,0,.55);jar(.3,.22,1,.42);cyl(0,1.2,0,.04,.04,2,'wood');scene.add(dynamic);boats.push({g:dynamic,offset:i*23,x:i%2?2.7:-2.7})}dynamic=null;
 const walkers=[];for(let i=0;i<58;i++){dynamic=new T.Group();cyl(0,.6,0,.15,.23,.8,i%3?'linen':'cloth');ell(0,1.14,0,.14,.17,.14,'skin');ell(0,1.26,0,.16,.09,.16,'linen');box(-.09,.17,0,.1,.3,.12,'dark');box(.09,.17,0,.1,.3,.12,'dark');scene.add(dynamic);walkers.push({g:dynamic,x:i%2?-10:10,z:R(-94,25),v:R(.1,.23)})}dynamic=null;
 // Coalesce static geometry by material: source geo.js batching principle, independent new shapes.
 for(const [key,list]of bank){const clean=list.map(g=>{let u=g.index?g.toNonIndexed():g;if(!u.attributes.uv)u.setAttribute('uv',new T.BufferAttribute(new Float32Array(u.attributes.position.count*2),2));return u});const geo=mergeGeometries(clean,false);const mesh=new T.Mesh(geo,mats[key]);mesh.castShadow=true;mesh.receiveShadow=true;scene.add(mesh);for(const g of clean)if(g!==geo)g.dispose()}
 return {beacon,lamps,update(t,wt){if(waterMat.userData.shader)waterMat.userData.shader.uniforms.uTime.value=t;for(const b of boats){b.g.position.set(b.x,.85,-100+((b.offset+wt*.2)%135));b.g.rotation.z=.015*Math.sin(wt+b.offset)}for(const w of walkers){w.g.position.set(w.x,1.3,-94+((w.z+100+wt*w.v)%126));w.g.rotation.y=w.v>.17?Math.PI:0}for(const l of lamps)l.m.emissiveIntensity=seg(t,l.t,l.t+.45)*4},counts:{buildings:hi,lamps:lamps.length,staticMaterials:bank.size}};
}
