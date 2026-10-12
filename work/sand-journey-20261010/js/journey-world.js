import * as THREE from 'three';
import {U,GLSL_COMMON,rng,specks,Pack,solidMaterial} from './core.js';
import {sandHeight,shoreZ} from './site.js';
import {SETTINGS,subjectAt,ease,clamp} from './timeline.js';

const VS=`varying vec3 vW;varying vec3 vN;void main(){vec4 w=modelMatrix*vec4(position,1.);vW=w.xyz;vN=normal;gl_Position=projectionMatrix*viewMatrix*w;}`;
function surfaceGeometry(x0,x1,d0,d1,nx,nd){const pos=[],idx=[];for(let j=0;j<=nd;j++)for(let i=0;i<=nx;i++){const x=x0+(x1-x0)*i/nx,z=shoreZ(x)+d0+(d1-d0)*j/nd;pos.push(x,sandHeight(x,z)-.006,z)}for(let j=0;j<nd;j++)for(let i=0;i<nx;i++){const a=j*(nx+1)+i,b=a+nx+1;idx.push(a,b,a+1,a+1,b,b+1)}const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));geo.setIndex(idx);geo.computeVertexNormals();return geo}

export function createJourneyWorld(scene){
 const groundMat=new THREE.ShaderMaterial({uniforms:{...U},vertexShader:VS,fragmentShader:`${GLSL_COMMON}
 varying vec3 vW;varying vec3 vN;
 float dotAt(vec2 uv,float s,float px,out float shade){vec2 cell=floor(uv/s);vec2 h=vec2(hash21(cell),hash21(cell.yx+17.3));vec2 c=(cell+.20+.60*h)*s;float r=s*(.25+.15*hash21(cell*1.31));shade=.70+.45*hash21(cell*.73);return 1.-smoothstep(r-px,r+px,length(uv-c));}
 void main(){vec3 n=normalize(vN);float d=vW.z-shoreZ(vW.x);float wet=1.-smoothstep(.5,4.,d);vec3 L=lightAt(n,.15);vec3 base=uSand*L*(.20+.12*wet);float px=max(length(fwidth(vW.xz)),.00001);float s=max(px*5.5,.004);float level=floor(log2(s));float sh0,sh1;float dots=mix(dotAt(vW.xz,exp2(level),px,sh0),dotAt(vW.xz,exp2(level+1.),px,sh1),fract(log2(s)));base=mix(base,uSand*L*(.58+.22*sh0),dots*.55);base*=1.-wet*.28;float fog=smoothstep(uFogNear,uFogFar,distance(vW,cameraPosition));base=mix(base,uFogColor,fog*.8);gl_FragColor=vec4(base,1.);}`,side:THREE.DoubleSide});
 const ground=new THREE.Mesh(surfaceGeometry(-160,110,-.8,60,720,310),groundMat);ground.renderOrder=-4;scene.add(ground);
 // Real water surface writes depth. It uses the upstream surf/chop at every vertex.
 const waterGeo=surfaceGeometry(-130,100,-160,.15,320,300);
 const water=new THREE.Mesh(waterGeo,new THREE.ShaderMaterial({uniforms:{...U},vertexShader:`${GLSL_COMMON}
 varying vec3 vW;varying vec3 vN;varying float vFoam;void main(){vec3 p=position;vec2 g;vec3 sf=surf(p.xz,uTime);p.y=sf.x+chop(p.xz,uTime,g)-.027;vN=normalize(vec3(-g.x,1.,-g.y-sf.z));vFoam=sf.y;vW=p;gl_Position=projectionMatrix*viewMatrix*vec4(p,1.);}`,
 fragmentShader:`${GLSL_COMMON}
 varying vec3 vW;varying vec3 vN;varying float vFoam;void main(){vec3 n=normalize(vN);vec3 V=normalize(vW-cameraPosition);vec3 R=reflect(V,n);float fres=.02+.98*pow(1.-max(dot(n,-V),0.),5.);vec3 reflected=mix(uSkyHorizon,uSkyTop,smoothstep(0.,.6,R.y))*uBg;vec3 c=mix(uWaterDeep*.40,reflected*.37,fres);float lace=noise2(vW.xz*1.7+uTime*.16);c=mix(c,uFoam*lightAt(n,.4)*.33,vFoam*(.25+.25*lace));c+=uSunColor*pow(max(dot(R,uSunDir),0.),60.)*.35*uSunVis;gl_FragColor=vec4(c,1.);}`,side:THREE.DoubleSide}));water.renderOrder=-3;scene.add(water);
 // A fixed, irregular grain: twelve asymmetric faceted vertices, a warm quartz face.
 const r=rng(SETTINGS.seed), grainGeo=new THREE.IcosahedronGeometry(SETTINGS.radius,1);
 const gp=grainGeo.attributes.position;for(let i=0;i<gp.count;i++){const v=new THREE.Vector3().fromBufferAttribute(gp,i);const a=.86+.14*Math.sin(v.x*591+v.y*831)+.07*Math.cos(v.z*913);v.set(v.x*a*1.06,v.y*a*.87,v.z*a*.92);gp.setXYZ(i,...v.toArray())}grainGeo.computeVertexNormals();
 const grainMat=new THREE.ShaderMaterial({uniforms:{...U},vertexShader:VS,fragmentShader:`${GLSL_COMMON} varying vec3 vW;varying vec3 vN;varying vec3 vLocal;void main(){vec3 n=normalize(vN);vec3 L=lightAt(n,.18);float q=noise2(vLocal.xz*2300.);vec3 c=uSand*vec3(1.10,.95,.73)*L*(.83+.25*q);vec3 H=normalize(uSunDir+normalize(cameraPosition-vW));c+=uSunColor*pow(max(dot(n,H),0.),42.)*.16;gl_FragColor=vec4(c,1.);}`,side:THREE.DoubleSide});
 // Apply object rotation to the normal, as core's solid shader does.
 grainMat.vertexShader=VS.replace('void main()','varying vec3 vLocal;void main()').replace('vN=normal','vLocal=position;vN=normalize(mat3(modelMatrix)*normal)');
 const grain=new THREE.Mesh(grainGeo,grainMat);grain.name=SETTINGS.subjectId;scene.add(grain);
 // Surface micro-grit shares the same light and the same surface, stays world anchored.
 const gritGeo=grainGeo.clone();const im=new THREE.ShaderMaterial({uniforms:{...U},vertexShader:`varying vec3 vW;varying vec3 vN;varying vec3 vC;void main(){vec4 w=modelMatrix*instanceMatrix*vec4(position,1.);vW=w.xyz;vN=normalize(mat3(modelMatrix*instanceMatrix)*normal);vC=instanceColor;gl_Position=projectionMatrix*viewMatrix*w;}`,fragmentShader:`${GLSL_COMMON} varying vec3 vW;varying vec3 vN;varying vec3 vC;void main(){vec3 c=vC*uSand*lightAt(normalize(vN),.2)*.75;float fog=smoothstep(uFogNear,uFogFar,distance(vW,cameraPosition));gl_FragColor=vec4(mix(c,uFogColor,fog*.8),1.);}`,side:THREE.DoubleSide});
 const grit=new THREE.InstancedMesh(gritGeo,im,22000),dummy=new THREE.Object3D();
 for(let i=0;i<22000;i++){const x=-40+r()*29,z=shoreZ(x)+1+r()*25;const scale=.18+r()*.8;dummy.position.set(x,sandHeight(x,z)+SETTINGS.radius*.72*scale,z);dummy.rotation.set(r()*6,r()*6,r()*6);dummy.scale.setScalar(scale);dummy.updateMatrix();grit.setMatrixAt(i,dummy.matrix);grit.setColorAt(i,new THREE.Color().setRGB(.6+r()*.45,.57+r()*.4,.52+r()*.34))}grit.instanceMatrix.needsUpdate=true;grit.frustumCulled=false;scene.add(grit);
 const pk=new Pack({position:3,aSize:1,aSeed:1,aNormal:3});for(let i=0;i<85;i++){const x=-32+(r()-.5)*2.0,z=shoreZ(x)+22+(r()-.5)*2;pk.push({position:[x,sandHeight(x,z)+.006,z],aSize:.004+r()*.004,aSeed:r(),aNormal:[0,1,0]})}
 const wind=specks({attributes:pk.attributes(),blend:'normal',decl:'attribute vec3 aNormal;',body:`float elapsed=max(0.,uTime-${(SETTINGS.seaStart+1.55).toFixed(2)}-aSeed*.75);float launch=smoothstep(0.,.3,elapsed);pos.x+=elapsed*.50;pos.z-=elapsed*1.05;pos.y+=launch*max(0.,.25*sin(elapsed*.7));col=uSand*lightAt(aNormal,.3)*.7;alpha=(1.-smoothstep(4.,6.,elapsed))*.7;`});scene.add(wind);
 // World-space spray threads ride a passing near-shore crest; no screen-space wipe.
 const sprayPk=new Pack({position:3,aSize:1,aSeed:1});for(let i=0;i<900;i++)sprayPk.push({position:[r(),r(),r()],aSize:.003+r()*.006,aSeed:r()});
 const anchor={value:new THREE.Vector3()};const spray=specks({attributes:sprayPk.attributes(),blend:'normal',uniforms:{uAnchor:anchor,uStory:{value:0}},decl:'uniform vec3 uAnchor;uniform float uStory;',body:`float age=uStory-15.10;float live=smoothstep(0.,.06,age)*(1.-smoothstep(.40,.70,age));pos=uAnchor+vec3((position.x-.5)*.34,position.y*.15+age*.16,(position.z-.5)*.055-age*.12);col=uFoam*lightAt(vec3(0.,1.,0.),.5)*.9;alpha=live*.85;`});spray.renderOrder=3;scene.add(spray);
 return {grain,update(t){grain.position.fromArray(subjectAt(t));const rotate=t<1.4?0:t<2.55?(t-1.4)*13:t<=18.2?14.95+(t-2.55)*3.7:14.95+15.65*3.7+.83*ease((t-18.2)/.45);grain.rotation.set(rotate*.68,rotate*.31,rotate);anchor.value.fromArray(subjectAt(t));anchor.value.z+=.12;anchor.value.y-=.035;spray.material.uniforms.uStory.value=t},ground,water};
}
