import {THREE,C,clamp,progress,mix,vecmix,noise,camera,pose,material,texture,box,rock} from './common.mjs';
// A thick stone, an independent sheet, and contact-anchored image meshes in a real local 3D scene.
export function createRecord3D(lib,plan){
 const scene=new THREE.Scene(),surface=box(5,.12,5,'#c3bdac',texture('wash',99));surface.position.y=-.08;scene.add(surface);scene.fog=new THREE.Fog(C.paper,4,9);
 const origin=[-.34,.17,.18],w=1.08,h=1.27,shape=new THREE.Shape();const outline=[[.02,.9],[.11,.3],[.47,.15],[.7,.05],[.82,.1],[.91,.82],[.82,.98],[.16,.99]];
 outline.forEach(([u,v],i)=>{const x=(u-.5)*w,y=(.5-v)*h;i?shape.lineTo(x,y):shape.moveTo(x,y)});shape.closePath();
 const geo=new THREE.ShapeGeometry(shape);const pp=geo.attributes.position,uv=geo.attributes.uv;for(let i=0;i<pp.count;i++)uv.setXY(i,pp.getX(i)/w+.5,pp.getY(i)/h+.5);uv.needsUpdate=true;
 const slab=new THREE.Group();slab.position.fromArray(origin);slab.rotation.x=Math.PI/2;scene.add(slab);
 const side=new THREE.Mesh(new THREE.ExtrudeGeometry(shape,{depth:.13,bevelEnabled:true,bevelThickness:.012,bevelSize:.012,bevelSegments:2,steps:1}),material('#777a6a',texture('wash',81)));slab.add(side);
 const face=new THREE.Mesh(geo,new THREE.MeshBasicMaterial({map:lib['stone-face'].tx,side:THREE.DoubleSide,transparent:true,alphaTest:.03}));face.position.z=-.016;slab.add(face);
 const dustMaterial=new THREE.ShaderMaterial({transparent:true,depthWrite:false,side:THREE.DoubleSide,uniforms:{clean:{value:0}},vertexShader:'varying vec2 uv0; void main(){uv0=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',fragmentShader:'varying vec2 uv0; uniform float clean; void main(){for(int i=0;i<128;i++){float q=float(i)/127.;if(q<=clean&&clean>0.){vec2 brush=vec2(.5+.35*sin(q*18.849556),1.-q);if(distance(uv0,brush)<.115)discard;}}float n=fract(sin(dot(floor(uv0*500.),vec2(12.9898,78.233)))*43758.5453);gl_FragColor=vec4(vec3(.55,.55,.49),.47+n*.18);}'});
 const dust=new THREE.Mesh(geo.clone(),dustMaterial);dust.position.z=-.020;slab.add(dust);
 const paperCanvas=document.createElement('canvas');paperCanvas.width=512;paperCanvas.height=640;const pg=paperCanvas.getContext('2d'),paperTex=new THREE.CanvasTexture(paperCanvas);paperTex.colorSpace=THREE.SRGBColorSpace;
 const pw=.72,ph=.92,paperGeo=new THREE.PlaneGeometry(pw,ph,20,26),base=paperGeo.attributes.position.array.slice();const paper=new THREE.Mesh(paperGeo,material('#fffdf5',paperTex));paper.rotation.x=Math.PI/2;paper.position.set(.67,.045,-.26);scene.add(paper);
 const marks=[];for(let band=0;band<3;band++)for(let row=0;row<(band===0?4:band===1?5:7);row++)for(let col=0;col<12;col++){const x=col*28+47,y=band*140+row*14+75;marks.push([[x,y],[x+5+noise(col+row)*7,y-3],[x+14,y+3]])}
 function hand(id,size){const asset=lib[id],height=size*asset.im.height/asset.im.width,tip=asset.record.contact_uv;const geo=new THREE.PlaneGeometry(size,height,10,12);geo.translate(size*(.5-tip[0]),height*(tip[1]-.5),0);geo.rotateX(Math.PI/2);const m=new THREE.Mesh(geo,new THREE.MeshBasicMaterial({map:asset.tx,transparent:true,alphaTest:.035,depthWrite:true,side:THREE.DoubleSide}));m.userData.contactUV=tip;scene.add(m);return m}
 const brush=hand('brush-hand',1.08),pen=hand('pen-hand',.79);
 dust.name='stone-dust';face.name='stone-face';side.name='stone-volume';paper.name='record-paper';brush.name='brush-hand';pen.name='pen-hand';
 for(let i=0;i<20;i++)rock(scene,(noise(i+21)-.5)*3,(noise(i+66)-.5)*2.5,.015+noise(i)*.055);
 const cam=camera(scene,[.3,1.4,-1.65],[.05,.07,.05],38),brushAt=plan.events.find(e=>e.id==='stone-brush').at,recordAt=plan.events.find(e=>e.id==='record-contact').at;
 let state={};
 function update(t){
  const clean=progress(t,brushAt,46),write=clamp((t-recordAt)/(48-recordAt)),cursor=write*marks.length,index=Math.min(marks.length-1,Math.floor(cursor)),fraction=write===1?1:cursor-index,stroke=clamp(fraction/.78);dustMaterial.uniforms.clean.value=clean;
  brush.visible=t>=44&&t<46.3;brush.position.set(origin[0]+w*.35*Math.sin(clean*6*Math.PI),origin[1]+.020+mix(.2,0,progress(t,44,brushAt)),origin[2]+h*(.5-clean));
  pg.fillStyle='#e8e2d2';pg.fillRect(0,0,512,640);pg.strokeStyle='#7f85734a';pg.lineWidth=1;pg.strokeRect(18,18,476,604);pg.strokeStyle='#596651';pg.lineWidth=1.65;
  for(let i=0;i<index;i++){pg.beginPath();marks[i].forEach(([x,y],j)=>j?pg.lineTo(x,y):pg.moveTo(x,y));pg.stroke()}
  const m=marks[index],seg=stroke<.5?0:1,q=stroke<.5?stroke*2:(stroke-.5)*2,inkPoint=vecmix(m[seg],m[seg+1],q);if(write>0){pg.beginPath();pg.moveTo(...m[0]);if(seg)pg.lineTo(...m[1]);pg.lineTo(...inkPoint);pg.stroke()}
  paperTex.needsUpdate=true;const a=paperGeo.attributes.position,settle=plan.events.find(e=>e.id==='paper-settle').at,flutter=t<settle?.012*Math.sin((t-settle)*8)*Math.exp(-Math.abs(t-settle)*3):0;
  for(let i=0;i<a.count;i++){const x=base[i*3],y=base[i*3+1];a.setXYZ(i,x,y,flutter*Math.pow(clamp((x/pw+.5)),3))}a.needsUpdate=true;
  const gap=clamp((fraction-.78)/.22),current=fraction<=.78||index===marks.length-1?inkPoint:vecmix(m[2],marks[index+1][0],progress(gap,0,1)),cell=clamp(current[0]/512)*20,column=Math.min(19,Math.floor(cell)),surfaceY=paper.position.y-flutter*mix((column/20)**3,((column+1)/20)**3,cell-column),penTip=[paper.position.x+(current[0]/512-.5)*pw,surfaceY,paper.position.z+(.5-current[1]/640)*ph],contact=write>0&&write<1&&fraction<=.78;
  pen.visible=t>=46.35&&t<48.4;pen.position.fromArray(penTip);pen.position.y+=mix(.17,0,progress(t,46.35,recordAt))+progress(t,48,48.4)*.14+(fraction>.78&&index<marks.length-1?.025*Math.sin(gap*Math.PI):0);
  const back=progress(t,47.8,48.7);pose(cam,vecmix([.1,1.85,-2.4],[.25,2.2,-2.8],back),vecmix([-.24,.08,.2],[.2,.08,-.1],progress(t,46.3,47.5)),38);
  state={camera:cam.position.toArray(),stoneOrigin:origin,stoneThickness:.13,brushTip:brush.position.toArray(),penTip:pen.position.toArray(),paper:paper.position.toArray(),clear:clean,marks:index+(stroke===1?1:0),totalMarks:marks.length,penOnPaper:contact,strokePoint:inkPoint,penGroundError:contact?pen.position.y-penTip[1]:0,brushGroundError:t>=brushAt&&t<=46?brush.position.y-(origin[1]+.020):0};
 }
 return {scene,camera:cam,update,snapshot(t){update(t);return state},engineering(t){update(t);scene.updateMatrixWorld(true);const ray=new THREE.Raycaster(),check=(object,point)=>{ray.set(cam.position,new THREE.Vector3(...point).sub(cam.position).normalize());const hits=ray.intersectObjects(scene.children,true).filter(h=>h.object.visible&&h.object.parent?.visible!==false);const h=hits[0];return {expected:object.name,first:h?.object.name||h?.object.geometry?.type,targetDistance:cam.position.distanceTo(new THREE.Vector3(...point)),firstDistance:h?.distance,blocked:h&&h.object!==object&&!h.object.material.transparent&&h.distance<cam.position.distanceTo(new THREE.Vector3(...point))-.001};};return {stone:check(face,[origin[0],origin[1]+.016,origin[2]]),paper:check(paper,paper.position.toArray()),penContact:t>recordAt&&t<48?check(pen,pen.position.toArray()):null};}};
}
