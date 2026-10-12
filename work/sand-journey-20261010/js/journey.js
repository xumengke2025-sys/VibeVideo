// Complete runtime layers are retained from Particle Beach, fixed upstream in upstream/.
import * as THREE from 'three';
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';
import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';
import {UnrealBloomPass} from 'three/addons/postprocessing/UnrealBloomPass.js';
import {OutputPass} from 'three/addons/postprocessing/OutputPass.js';
import {ShaderPass} from 'three/addons/postprocessing/ShaderPass.js';
import {FXAAShader} from 'three/addons/shaders/FXAAShader.js';
import {U,rng} from './core.js';
import {sunPosition,moonPosition,moonIllumination,localSidereal,atBeachHour,beachHour} from './astro.js';
import {applySky} from './palette.js';
import {createSky} from './sky.js';
import {createSea,setCasters} from './sea.js';
import {createBreakers} from './breakers.js';
import {createDistance} from './distance.js';
import {createShore} from './shore.js';
import {createJourneyWorld} from './journey-world.js';
import {SETTINGS,EVENTS,SHOTS,subjectAt,cameraAt,clamp} from './timeline.js';
import {createPost} from './post.js';
Math.random=rng(SETTINGS.seed);
const record=new URLSearchParams(location.search).has('render');if(record)document.body.classList.add('record');
const W=record?1080:Math.min(1080,Math.round(window.innerHeight*9/16)),H=record?1920:Math.round(W*16/9);
const canvas=document.getElementById('scene');canvas.style.width='min(100vw,56.25vh)';canvas.style.height='min(177.777vw,100vh)';canvas.style.margin='auto';
const renderer=new THREE.WebGLRenderer({canvas,antialias:false,powerPreference:'high-performance',preserveDrawingBuffer:true});
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.04;renderer.setPixelRatio(1);renderer.setSize(W,H,false);
const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(48,9/16,.004,4000);
const sky=createSky(scene),sea=createSea(scene),breakers=createBreakers(scene);
const distance=createDistance(scene),shore=createShore(scene),world=createJourneyWorld(scene);
const composer=new EffectComposer(renderer);composer.addPass(new RenderPass(scene,camera));
const bloom=new UnrealBloomPass(new THREE.Vector2(W,H),.32,.45,.72);composer.addPass(bloom);composer.addPass(new OutputPass());
const fxaa=new ShaderPass(FXAAShader);fxaa.material.uniforms.resolution.value.set(1/W,1/H);composer.addPass(fxaa);composer.setSize(W,H);
const post=createPost(renderer,composer,W,H),frustum=new THREE.Frustum(),vp=new THREE.Matrix4();
const DAY=Date.UTC(2026,8,23,19),ms=atBeachHour(DAY,17.75),sun=sunPosition(ms),moon=moonPosition(ms),illum=moonIllumination(ms),hour=beachHour(ms);
// Reference evening palette; warm side illumination at a stable chosen sunset.
sun.apparent=4.2;sun.alt=4.0;sun.az=276;
const halton=(i,b)=>{let f=1,r=0;for(;i>0;i=Math.floor(i/b)){f/=b;r+=f*(i%b)}return r};
function stateAt(t){t=clamp(t,0,20);return {t,subjectId:SETTINGS.subjectId,subject:subjectAt(t),pose:cameraAt(t),seaTime:SETTINGS.seaStart+t,contact:t>=SETTINGS.contact}}
function draw(t,jx=0,jy=0){const state=stateAt(t),pose=state.pose;U.uTime.value=state.seaTime;U.uPR.value=1;applySky({sun,moon,illum,hour});U.uWaterLit.value.lerp(new THREE.Color(.09,.32,.44),.27);U.uScale.value=H/(2*Math.tan(THREE.MathUtils.degToRad(pose.fov)/2));camera.position.fromArray(pose.position);camera.fov=pose.fov;camera.up.set(0,1,0);camera.lookAt(new THREE.Vector3(...pose.target));camera.updateProjectionMatrix();camera.setViewOffset(W,H,jx,jy,W,H);camera.updateMatrixWorld(true);frustum.setFromProjectionMatrix(vp.multiplyMatrices(camera.projectionMatrix,camera.matrixWorldInverse));sky.update(camera,{lst:localSidereal(ms),illum,moonPos:moon});const ctx={camera,frustum,t:state.seaTime,hour,sun,moon};sea.update(state.seaTime,0,ctx);breakers.update(state.seaTime,0,ctx);world.update(t);setCasters([],camera.position);composer.render(0);camera.clearViewOffset();return state}
window.renderAt=function(t,type='image/jpeg',quality=.97,sub=1){t=clamp(t,0,20);const fi=Math.round(t*30);for(let k=0;k<sub;k++){const st=sub===1?t:Math.min(20,t+(k+.5)/sub*.5/30);const n=fi*sub+k+1;draw(st,sub===1?0:halton(n,2)-.5,sub===1?0:halton(n,3)-.5);post.addSample(k,sub)}post.finish(fi);return canvas.toDataURL(type,quality)};
window.__film={...SETTINGS,width:W,height:H,cuts:[],events:EVENTS,shots:SHOTS,stateAt,diagnostics(){return {state:stateAt(window.__storyTime||0),three:THREE.REVISION,gl:renderer.getContext().getParameter(renderer.getContext().RENDERER),draw:renderer.info.render,fields:sea.fields.map(f=>({name:f.o.name,kept:f.kept(camera),verts:f.verts()})),errors:window.__errors||[]}}};
window.__storyTime=0;window.renderAt(0);window.ready=true;
const audio=new Audio('audio/sand-journey.wav');let anim=0;
function tick(){const t=Math.min(20,audio.currentTime);window.__storyTime=t;window.renderAt(t);if(t<20&&!audio.paused)anim=requestAnimationFrame(tick)}
document.getElementById('play').onclick=async()=>{cancelAnimationFrame(anim);audio.currentTime=0;await audio.play();document.getElementById('play').style.display='none';tick()};audio.onended=()=>{document.getElementById('play').style.display='block'};
