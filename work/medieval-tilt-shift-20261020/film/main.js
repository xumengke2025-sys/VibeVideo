import * as T from 'three';
import {makePost} from './post.js';
import {buildWorld} from './world.js';
import {makeHero} from './hero.js';
import {V,mix,seg,clamp,worldTime} from './math.js';
const qs=new URLSearchParams(location.search),scale=window.__previewScale||1,W=Math.round(1080*scale),H=Math.round(1920*scale);
const renderer=new T.WebGLRenderer({antialias:false,preserveDrawingBuffer:true,powerPreference:'high-performance'});renderer.setSize(W,H);renderer.setPixelRatio(1);renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.12;renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;document.body.appendChild(renderer.domElement);
const scene=new T.Scene();scene.background=new T.Color('#b4c9cd');scene.fog=new T.FogExp2('#b9beb0',.0018);
const sky=new T.Mesh(new T.SphereGeometry(1800,32,16),new T.ShaderMaterial({side:T.BackSide,depthWrite:false,uniforms:{},vertexShader:'varying vec3 p;void main(){p=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',fragmentShader:'varying vec3 p;void main(){float u=clamp(normalize(p).y*2.3,0.,1.);gl_FragColor=vec4(mix(vec3(.78,.72,.58),vec3(.34,.55,.65),pow(u,.55)),1.);}'}));scene.add(sky);
scene.add(new T.HemisphereLight('#bed5e2','#8f7050',2.3));const sun=new T.DirectionalLight('#ffe3ad',3.5);sun.position.set(-110,100,65);sun.target.position.set(0,0,-30);scene.add(sun,sun.target);sun.castShadow=true;sun.shadow.mapSize.set(4096,4096);Object.assign(sun.shadow.camera,{left:-125,right:125,top:125,bottom:-125,near:1,far:350});sun.shadow.bias=-.00012;sun.shadow.normalBias=.1;sun.shadow.radius=2;
const camera=new T.PerspectiveCamera(30,W/H,.2,2200);const world=buildWorld(scene);const hero=makeHero(scene);const post=makePost(renderer,scene,camera,W,H,{ssaa:qs.has('ssaa1')?1:2,msaa:4,ao:false});post.bloom.strength=.16;post.bloom.radius=.45;post.bloom.threshold=1.5;Object.assign(post.grade.uniforms.sat,{value:1.1});post.grade.uniforms.contrast.value=.08;post.grade.uniforms.amt.value=.14;
// Position and look-at have independent paths. Low ridge -> high oblique -> emissary -> rise.
const opening=new T.CatmullRomCurve3([V(-30,3,290),V(-29,15,265),V(-24,48,222),V(-13,93,156),V(-8,115,89)]);
function pose(t){let p,target,fov=30;
 if(t<12){let u=seg(t,0,12);p=opening.getPoint(u);target=V(mix(0,5,u),mix(16,3,u),mix(-18,-12,u));}
 else if(t<18){let u=seg(t,12,18);p=V(-8,115,89).lerp(V(-3,65,30),u);target=V(5,3,-12).lerp(hero.position(18).add(V(0,1,0)),u);fov=mix(30,29,u)}
 else if(t<26){let u=seg(t,18,26);p=V(-3,65,30).lerp(V(-2,20,-9),u);p.y=10+Math.exp(mix(Math.log(55),Math.log(10),u));target=hero.position(18).add(V(0,1,0)).lerp(V(10,11.5,-27),1-Math.pow(1-u,1.7));fov=mix(29,30,u)}
 else if(t<36){let u=seg(t,26,36);p=V(-2,20,-9).lerp(V(-.5,19,-10.5),u);target=V(10,11.5,-27);fov=30}
 else if(t<48){let u=seg(t,36,48);p=V(-.5,19,-10.5).lerp(V(-36,125,125),u);p.y=10+Math.exp(mix(Math.log(9),Math.log(115),u));target=V(10,11.5,-27).lerp(V(3,5,-20),1-Math.pow(1-u,1.4));fov=mix(30,32,u)}
 else{let u=seg(t,48,52);p=V(-36,125,125).lerp(V(-39,133,133),u);target=V(3,5,-20);fov=32}
 return {position:p,target,fov};}
function render(t,type='image/jpeg',quality=.96){t=clamp(t,0,56);world.update(t,worldTime(t));const h=hero.update(t),p=pose(t);camera.position.copy(p.position);camera.fov=p.fov;camera.near=.2;camera.lookAt(p.target);camera.updateProjectionMatrix();camera.updateMatrixWorld(true);
 let focus=t<12?p.target:t<18?p.target.clone().lerp(h.focus,seg(t,12,16)):t<36?h.focus:p.target;
 // DepthTexture stores forward view depth, NOT radial distance; essential for off-axis focus.
 post.dof.focus=-focus.clone().applyMatrix4(camera.matrixWorldInverse).z;
 const screen=focus.clone().project(camera),openingMix=seg(t,5,11);post.dof.aper=mix(1250,200,seg(t,18,26))*scale;
 post.dof.maxCoc=qs.has('nodof')?0:24*scale;Object.assign(post.dof.band,{y:clamp((screen.y+1)/2,.28,.72),w:t<10?.14:t<24?.10:t<36?.15:.105,amp:32*scale,mix:mix(.12,.55,openingMix),tilt:-.04,pow:1.4});
 post.bloom.enabled=!qs.has('nobloom');post.composer.render();return renderer.domElement.toDataURL(type,quality);}
window.renderAt=render;window.render=render;window.__film={duration:56,fps:24,width:W,height:H,cuts:[12,18,26,36,48,52],continuousCuts:[12,18,26,36,48,52],holdStart:52,stateAt:t=>({pose:pose(t)}),counts:world.counts};render(0);window.ready=true;window.READY=true;
if(!qs.has('render')){let start=performance.now();function loop(){render(((performance.now()-start)/1000)%56);requestAnimationFrame(loop)}requestAnimationFrame(loop)}
