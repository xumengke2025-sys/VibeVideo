import {THREE,clamp,billboard,line} from '../scenes/common.mjs';
const rotate=(p,o,a)=>{const x=p[0]-o[0],y=p[1]-o[1];return [o[0]+x*Math.cos(a)-y*Math.sin(a),o[1]+x*Math.sin(a)+y*Math.cos(a),0]};
const distance=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
function component(asset,height){
 const width=height*asset.im.width/asset.im.height,r=asset.record.horse_rig;if(!r)throw Error('Missing calibrated horse rig');
 const local=([u,v])=>[(u-.5)*width,(1-v)*height,0],legs=r.legs.map(c=>c.map(local)),neck=local(r.neck),mouth=local(r.mouth),hand=local(r.hand),saddle=local(r.saddle),landmarks=[...legs.flat(),neck,mouth,hand,saddle];
 const xs=[...new Set([...Array.from({length:25},(_,i)=>-width/2+i*width/24),...landmarks.map(p=>p[0])])].sort((a,b)=>a-b),ys=[...new Set([...Array.from({length:37},(_,i)=>i*height/36),...landmarks.map(p=>p[1])])].sort((a,b)=>a-b),positions=[],uv=[],indices=[];
 ys.forEach((y,j)=>xs.forEach((x,i)=>{positions.push(x,y,0);uv.push(x/width+.5,y/height);if(i<xs.length-1&&j<ys.length-1){const a=j*xs.length+i;indices.push(a,a+1,a+xs.length,a+1,a+xs.length+1,a+xs.length)}}));
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));geo.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));geo.setIndex(indices);geo.computeVertexNormals();
 const mesh=new THREE.Mesh(geo,new THREE.MeshBasicMaterial({map:asset.tx,transparent:true,alphaTest:.035,side:THREE.DoubleSide})),group=new THREE.Group();group.add(mesh);const rein=line([mouth,hand],'#45443e',.55);group.add(rein);
 const toward=Math.sign(mouth[0]-neck[0]),p=geo.attributes.position;
 const bindings=Array.from({length:p.count},(_,i)=>{const x=positions[i*3],y=positions[i*3+1];let best={d:Infinity};legs.forEach((c,leg)=>{for(let bone=0;bone<2;bone++){const a=c[bone],b=c[bone+1],dx=b[0]-a[0],dy=b[1]-a[1],q=clamp(((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)),d=(x-a[0]-q*dx)**2+(y-a[1]-q*dy)**2;if(d<best.d)best={leg,bone,d,fade:clamp((c[0][1]-y)/(height*.075))}}});return best;});
 const vertexAt=v=>ys.indexOf(v[1])*xs.length+xs.indexOf(v[0]);
 const endIndices=[vertexAt(mouth),vertexAt(hand)];
 return {group,mesh,state:null,update(t,rate){
  const phase=t*rate*1.6,bob=Math.sin(phase*2)*.018,neckAngle=Math.sin(phase+.4)*.022,riderAngle=Math.sin(phase+.9)*.016;
  const chains=legs.map((c,i)=>{const ph=phase+[0,Math.PI,Math.PI,.65][i],a=Math.sin(ph)*.16,b=Math.max(0,Math.sin(ph+.7))*.27,knee=rotate(c[1],c[0],a),foot0=rotate(c[2],c[0],a),foot=rotate(foot0,knee,b);return {points:[c[0],knee,foot],a,b,lengthErrors:[Math.abs(distance(c[0],knee)-distance(c[0],c[1])),Math.abs(distance(knee,foot)-distance(c[1],c[2]))]}});
  const targetMouth=rotate(mouth,neck,neckAngle),targetHand=rotate(hand,saddle,riderAngle),reinDx=hand[0]-mouth[0],reinDy=hand[1]-mouth[1];
  function deform(x,y,binding){let v=[x,y,0];const q=clamp(((x-mouth[0])*reinDx+(y-mouth[1])*reinDy)/(reinDx*reinDx+reinDy*reinDy)),reinDistance=Math.hypot(x-mouth[0]-q*reinDx,y-mouth[1]-q*reinDy);
   if(reinDistance<height*.025){v=[x+(targetMouth[0]-mouth[0])*(1-q)+(targetHand[0]-hand[0])*q,y+(targetMouth[1]-mouth[1])*(1-q)+(targetHand[1]-hand[1])*q,0]}
   else if((x-neck[0])*toward>0&&y>neck[1]-height*.13)v=rotate(v,neck,neckAngle);
   else if(y>saddle[1]&&Math.abs(x-saddle[0])<width*.34)v=rotate(v,saddle,riderAngle);
   else if(binding.fade>0){const c=legs[binding.leg],s=chains[binding.leg];let d=rotate(v,c[0],s.a);if(binding.bone===1)d=rotate(d,s.points[1],s.b);v=[x+(d[0]-x)*binding.fade,y+(d[1]-y)*binding.fade,0]}
   v[1]+=bob;return v;
  }
  for(let i=0;i<p.count;i++){const v=deform(positions[i*3],positions[i*3+1],bindings[i]);p.setXYZ(i,...v)}p.needsUpdate=true;
  const endpoints=[targetMouth,targetHand].map(v=>[v[0],v[1]+bob,.002]);const rp=rein.geometry.attributes.position;endpoints.forEach((v,i)=>rp.setXYZ(i,...v));rp.needsUpdate=true;rein.geometry.computeBoundingSphere();geo.computeBoundingSphere();
  const endpointError=Math.max(...endIndices.map((i,k)=>Math.hypot(p.getX(i)-endpoints[k][0],p.getY(i)-endpoints[k][1])));
  this.state={chains:chains.map(c=>({points:c.points,lengthErrors:c.lengthErrors})),neckAngle,riderAngle,reinEndpointError:endpointError};
 }};
}
export function makeHorse(lib,variant=0,height=2.2){
 const left=component(lib['cavalry-'+variant],height),right=component(lib['cavalry-'+(variant+3)],height),group=new THREE.Group();group.add(left.group,right.group);
 return {group,left,right,rigState:null,update(t,c,speed=2.3,away=false){left.group.visible=!away;right.group.visible=away;billboard(group,c);const active=away?right:left;active.update(t,speed);this.rigState=active.state}};
}
