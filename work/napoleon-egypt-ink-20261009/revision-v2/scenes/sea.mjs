import {THREE,C,clamp,progress,mix,vecmix,noise,ground,camera,pose,material,texture,rod,line,box,flag,puff,puffTexture} from './common.mjs';
export function makeShip({id='ship',scale=1,masts=3,french=true}={}){
 const group=new THREE.Group(),wood=texture('wood',french?42:55),cloth=texture('sail',12),verts=[],indices=[],uv=[];const sections=24,levels=4;
 // A tapered, curved hull with real cross-section and an open deck.
 for(let j=0;j<levels;j++)for(let i=0;i<=sections;i++)for(let s=0;s<2;s++){
  const z=-5+i*10/sections,breadth=.13+1.2*Math.pow(Math.sin(i/sections*Math.PI),.58),y=[-.2,.2,.75,1.12][j],x=(s?1:-1)*breadth*[.25,.7,1,.93][j];
  verts.push(x,y+.14*Math.pow(Math.abs(z)/5,3),z);uv.push(i/sections,j/3);
 }
 for(let j=0;j<levels-1;j++)for(let i=0;i<sections;i++)for(let s=0;s<2;s++){const a=(j*(sections+1)+i)*2+s,b=a+2,c=a+(sections+1)*2,d=c+2;indices.push(a,b,c,b,d,c)}
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(verts,3));geo.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));geo.setIndex(indices);geo.computeVertexNormals();group.add(new THREE.Mesh(geo,material('#a6a292',wood)));
 const deckVerts=[],deckUV=[],deckIdx=[];for(let i=0;i<=sections;i++){const z=-5+i*10/sections,b=.13+1.2*Math.pow(Math.sin(i/sections*Math.PI),.58);deckVerts.push(-b*.92,1.13,z,b*.92,1.13,z);deckUV.push(0,i/sections,1,i/sections);if(i<sections){const a=i*2;deckIdx.push(a,a+1,a+2,a+1,a+3,a+2)}}const dg=new THREE.BufferGeometry();dg.setAttribute('position',new THREE.Float32BufferAttribute(deckVerts,3));dg.setAttribute('uv',new THREE.Float32BufferAttribute(deckUV,2));dg.setIndex(deckIdx);group.add(new THREE.Mesh(dg,material('#b2ad9c',wood)));
 for(let s of [-1,1])for(let i=0;i<15;i++){const z=-3.8+i*.52,b=.13+1.2*Math.pow(Math.sin((z+5)/10*Math.PI),.58);const win=box(.018,.13,.19,'#383d36');win.position.set(s*b*.995,.7,z);group.add(win);group.add(rod([s*b,.92,z],[s*b,1.5,z],.016,'#656959'))}
 for(let s of [-1,1])for(let level of [.3,.92,1.25]){const pts=[];for(let i=0;i<=24;i++){const z=-5+i*10/24,b=.13+1.2*Math.pow(Math.sin(i/24*Math.PI),.58);pts.push([s*b*(level<.5?.8:.95),level,z])}group.add(line(pts,'#4b5043',.6))}
 const aft=box(1.3,.65,1.3,'#9e9987',wood);aft.position.set(0,1.4,3.4);group.add(aft);const bow=rod([0,1.2,-4.5],[0,2,-7],.035,'#555c4a');group.add(bow);
 const mastGroups=[],sails=[],rigging=[];
 for(let k=0;k<masts;k++){
  const z=masts===3?[-2.7,.3,2.7][k]:[-2,1.7][k],height=k===1?5.8:4.9;
  group.add(rod([0,1.1,z],[0,2.5,z],.065,'#666653'));const hinge=new THREE.Group();hinge.position.set(0,2.5,z);group.add(hinge);hinge.add(rod([0,0,0],[0,height-1.4,0],.05,'#676552'));
  for(let level=0;level<3;level++){
   const y=.1+level*1.12,w=3.1-level*.55;hinge.add(rod([-w/2,y+1.03,0],[w/2,y+1.03,0],.022,'#77735f'));
   const g=new THREE.PlaneGeometry(w,.94,16,12),a=g.attributes.position;g.translate(0,y+.5,.04);const base=a.array.slice();
   for(let i=0;i<a.count;i++){const yy=(base[i*3+1]-y)/.94;a.setX(i,base[i*3]*(.86+.14*yy));}
   const sail=new THREE.Mesh(g,new THREE.MeshBasicMaterial({color:'#c9c8b8',map:cloth,side:THREE.DoubleSide}));hinge.add(sail);sails.push({mesh:sail,base:sail.geometry.attributes.position.array.slice(),main:k===1,level,hinge});
  }
  for(let side of [-1,1])for(let n=0;n<5;n++){
   const bottom=[side*.92,1.22,z-1.3+n*.65],top=[0,height-1.7,0];
   const ln=line([[...bottom],[0,height,z]],'#5b6253',.65);group.add(ln);rigging.push({line:ln,bottom,top,hinge});
   if(n<4)for(let q=1;q<10;q++){const y=1.2+q*.27;const w=side*.92*(1-(y-1.2)/(height-1.2));group.add(line([[w,y,z-1.3+(y-1.2)*.18],[w,y,z-1.3+(y-1.2)*.18+.65]],'#646a5c',.35))}
  }
  mastGroups.push(hinge);
 }
 let standard=null;if(french){standard=flag();standard.group.scale.setScalar(.35);standard.group.position.set(0,3.3,3.3);group.add(standard.group)}else{const pennant=box(.5,.13,.005,'#69685d');pennant.position.set(0,5.6,1.7);group.add(pennant)}
 const anchor=line([[1,1,-3.2],[1.8,.05,-4.8],[2.3,-.07,-6.7]],'#50584b');group.add(anchor);group.scale.setScalar(scale);
 // Prepare damaged materials before the first frame; seeking never creates new render state.
 const damaged=sails.find(s=>s.main&&s.level===1);
 if(damaged){const c=document.createElement('canvas');c.width=c.height=512;const g=c.getContext('2d');g.drawImage(cloth.image,0,0);g.globalCompositeOperation='destination-out';g.beginPath();for(let i=0;i<18;i++){const a=i/18*Math.PI*2,r=45+noise(i+7)*24,x=294+Math.cos(a)*r,y=280+Math.sin(a)*r;if(!i)g.moveTo(x,y);else g.lineTo(x,y)}g.closePath();g.fill();damaged.mesh.userData.tornMap=new THREE.CanvasTexture(c);damaged.mesh.material.transparent=true;damaged.mesh.material.alphaTest=.05;}
 let damage=0,angle=0;
 function update(t,{hit=0,breakage=0,anchored=true}={}){
  damage=hit;group.rotation.z=Math.sin(t*.9)*.009;group.position.y=Math.sin(t*1.3)*.025;const heel=group.rotation.z,water=-.08,contactAngle=heel+Math.acos(clamp((water-group.position.y-2.5*Math.cos(heel))/4.4,-1,1));angle=contactAngle*breakage;
  const main=mastGroups[1];if(main)main.rotation.z=-angle;
  sails.forEach(s=>{const a=s.mesh.geometry.attributes.position;
   for(let i=0;i<a.count;i++){const x=s.base[i*3],y=s.base[i*3+1],wave=Math.sin(t*2.4-x*1.8+y*.9)*.11;const torn=s.main&&s.level===1&&hit>.5&&Math.abs(x-.24)<.42&&Math.abs(y-1.6)<.38;
    a.setXYZ(i,x,y-(s.main?hit*.08:0)*Math.cos(x*6),s.base[i*3+2]+wave*(1-Math.cos(x*2))*.5);
   }a.needsUpdate=true;
  });
  const torn=sails.find(s=>s.main&&s.level===1);if(torn)torn.mesh.material.map=hit>.5?torn.mesh.userData.tornMap:cloth;
  group.updateMatrixWorld(true);
  rigging.forEach((r,i)=>{const top=r.hinge.localToWorld(new THREE.Vector3(...r.top));group.worldToLocal(top);const a=r.line.geometry.attributes.position;a.setXYZ(0,...r.bottom);a.setXYZ(1,top.x,top.y,top.z);a.needsUpdate=true;r.line.visible=!(breakage>.7&&i%3===0)});
  anchor.visible=anchored;standard?.update(t);
 }
 return {id,group,update,get angle(){return angle},get damage(){return damage},mastGroups,engineering(){group.updateMatrixWorld(true);let rigError=0;for(const r of rigging){const p=r.line.geometry.attributes.position,top=r.hinge.localToWorld(new THREE.Vector3(...r.top)),actual=group.localToWorld(new THREE.Vector3(p.getX(1),p.getY(1),p.getZ(1)));rigError=Math.max(rigError,top.distanceTo(actual));}return {mastTip:mastGroups[1]?.localToWorld(new THREE.Vector3(0,4.4,0)).toArray(),rigError,anchored:anchor.visible};}};
}
export function createSea(lib,plan){
 const scene=new THREE.Scene();ground(scene,'sea');scene.fog=new THREE.Fog(C.paper,24,70);const cam=camera(scene,[-7,1.5,-12],[1,3,5],46);
 const main=makeShip({id:'french-line-ship-A'});main.group.position.set(1.5,0,7);scene.add(main.group);
 const others=[];for(let i=0;i<3;i++){const s=makeShip({id:'french-line-ship-'+(i+1),scale:.85+i*.06});s.group.position.set(i%2?2.8:5.8,0,20+i*13);scene.add(s.group);others.push(s)}
 const attacker=makeShip({id:'attacking-ship',scale:.8,masts:2,french:false});scene.add(attacker.group);
 const tx=puffTexture(),smokes=[];for(let i=0;i<25;i++){const p=puff(tx);scene.add(p);smokes.push(p)}
 const flame=new THREE.Mesh(new THREE.PlaneGeometry(.45,.9,4,6),new THREE.MeshBasicMaterial({color:'#80715d',transparent:true,opacity:.6,side:THREE.DoubleSide}));scene.add(flame);
 const event=(id)=>plan.events.find(e=>e.id===id).at,hitTime=event('sail-hit'),breakTime=event('mast-break');
 function update(t){
  const hit=progress(t,hitTime,hitTime+.16),br=progress(t,breakTime,35.5);main.update(t,{hit,breakage:br});others.forEach((s,i)=>s.update(t,{hit:t>34.5+i*.2?1:0,breakage:t>35?br*(.3+i*.1):0}));
  attacker.group.position.set(-4.8,0,mix(-9,15,progress(t,28,32.2)));attacker.update(t,{anchored:false});attacker.group.visible=t<33;
  flame.visible=t>=33.7;flame.position.set(1.4+Math.sin(t*19)*.04,2.4,7.3);flame.scale.set(1+Math.sin(t*18)*.1,1+Math.sin(t*23)*.15,1);flame.rotation.y=Math.atan2(cam.position.x-1.5,cam.position.z-7);
  smokes.forEach((p,i)=>{const start=i<8?hitTime:33.7+(i-8)*.13,age=t-start;p.visible=age>0&&age<5;if(p.visible){p.position.set(1.7+noise(i)*.7+age*.1,2.5+age*.6,7+noise(i+21)*2);p.scale.setScalar(.3+age*.55);p.material.opacity=(i<8?.38:.42)*Math.max(0,1-age/5)}});
  if(t<33){const q=progress(t,28,31.2);pose(cam,vecmix([-8,1.25,-12],[-5.4,1.9,-3.4],q),vecmix([-3,2.1,2],[1.5,3.5,7],progress(t,29.8,31.2)),46)}
  else {const q=progress(t,35.4,36.4),tip=main.mastGroups[1].localToWorld(new THREE.Vector3(0,3.8,0));pose(cam,vecmix([-2.8,4.6,1.2],[-9,7,-13],q),vecmix([1.5,3.3,7],[3,2,17],q),40);if(t<35.4&&t>34.4)cam.lookAt(new THREE.Vector3(mix(1.5,tip.x,progress(t,34.4,35.2)),mix(3.3,tip.y,progress(t,34.4,35.2)),7))}
  flame.rotation.y=Math.atan2(cam.position.x-1.5,cam.position.z-7);cam.updateMatrixWorld(true);
 }
 return {scene,camera:cam,update,snapshot(t){update(t);const mechanism=main.engineering(),ships=[main,...others,attacker],cameraInsideHull=ships.filter(s=>s.group.visible).some(s=>{s.group.updateMatrixWorld(true);const p=s.group.worldToLocal(cam.position.clone()),b=.13+1.2*Math.pow(Math.sin(clamp((p.z+5)/10)*Math.PI),.58);return p.z>-5&&p.z<5&&p.y>-.3&&p.y<1.6&&Math.abs(p.x)<b+.05;});return {camera:cam.position.toArray(),mastAngle:main.angle,hit:main.damage,id:main.id,shipPosition:main.group.position.toArray(),anchor:mechanism.anchored,mastTip:mechanism.mastTip,mastWaterError:t>=35.5?mechanism.mastTip[1]+.08:0,rigError:mechanism.rigError,cameraInsideHull}}};
}
