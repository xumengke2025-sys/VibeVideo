// Original utility distilled from studying dual camera/target tracks in particle-beach.
import {Vector3,CatmullRomCurve3} from 'three';
export const clamp=x=>Math.max(0,Math.min(1,x));
export const smooth=x=>{x=clamp(x);return x*x*(3-2*x);};
export const smoother=x=>{x=clamp(x);return x*x*x*(x*(x*6-15)+10);};
const v=a=>new Vector3(...a);
export function track(points,{arcLength=true}={}){
  if(points.length===1)return ()=>v(points[0]);
  const c=new CatmullRomCurve3(points.map(v),false,'centripetal');
  return u=>arcLength?c.getPointAt(clamp(u)):c.getPoint(clamp(u));
}
export function cameraTrack({position,target,fov=[40,40],roll=[0,0],ease=smoother,arcLength=true}){
  const p=track(position,{arcLength}),q=track(target,{arcLength});
  return u=>{const k=ease(u);return {position:p(k),target:q(k),fov:fov[0]+(fov[1]-fov[0])*k,roll:roll[0]+(roll[1]-roll[0])*k};};
}
export function applyCamera(camera,pose){
  camera.position.copy(pose.position);camera.up.set(0,1,0);camera.lookAt(pose.target);
  if(pose.roll)camera.rotateZ(pose.roll*Math.PI/180);
  if(camera.fov!==pose.fov){camera.fov=pose.fov;camera.updateProjectionMatrix();}
  camera.updateMatrixWorld(true);
}
// Vertical FOV, sensorHeight in mm. A 36x24 camera uses height=24; do not confuse horizontal FOV.
export const focalLengthToFov=(mm,sensorHeight=24)=>2*Math.atan(sensorHeight/(2*mm))*180/Math.PI;
export const fovToFocalLength=(fov,sensorHeight=24)=>sensorHeight/(2*Math.tan(fov*Math.PI/360));
// Preserve a subject's screen height after moving camera distance (dolly-zoom), not a generic depth effect.
export const matchedFov=(oldFov,oldDistance,newDistance)=>2*Math.atan(oldDistance*Math.tan(oldFov*Math.PI/360)/newDistance)*180/Math.PI;
export function projected(camera,world,width,height){const p=world.clone().project(camera);return {x:(p.x*.5+.5)*width,y:(.5-p.y*.5)*height,visible:p.z>=-1&&p.z<=1};}
