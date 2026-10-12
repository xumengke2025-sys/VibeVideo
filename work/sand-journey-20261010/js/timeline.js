import {sandHeight,shoreZ} from './site.js';
import {seaHeight} from './surf.js';
export const SETTINGS={duration:20,fps:30,width:1080,height:1920,subjectId:'sand-0001',radius:.008,seaStart:1023,contact:18.2,seed:20261010};
export const EVENTS=[{time:1.4,type:'wind-rise'},{time:2.55,type:'lift'},{time:9.6,type:'reveal'},{time:15.35,type:'spray-pass'},{time:18.2,type:'sand-contact'},{time:18.65,type:'settle'}];
export const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
export const ease=x=>{x=clamp(x);return x*x*x*(x*(x*6-15)+10)};
const lerp=(a,b,k)=>a+(b-a)*k;
// Hermite keys carry explicit world velocities, independent of render history.
const keys=[
 [0,-32,22,0,0],[1.4,-32,22,0,0],[2.55,-31.90,21.87,.28,-.45],
 [4,-31.1,20.0,.9,-1.5],[7,-28.8,14.2,.9,-2.1],[9,-27.0,9.7,1.0,-2.0],
 [10.6,-25.4,6.7,1.0,-1.4],[12,-24.2,4.2,.7,-1.7],[13,-23.4,1.6,1.0,-2.0],
 [14.5,-21.5,-2.4,1.7,-1.2],[15.7,-19.2,-3.0,1.7,.6],[17,-17.2,-.8,1.1,2.4],
 [18.2,-16.0,3.2,.25,.25],[18.65,-15.91,3.28,0,0],[20,-15.91,3.28,0,0]
];
export const SHOTS=[{start:0,end:4,id:'起风'},{start:4,end:9,id:'随风前进'},{start:9,end:13,id:'看见海'},{start:13,end:17,id:'掠过浪缘'},{start:17,end:20,id:'落回海岸'}];
function hermite(a,b,va,vb,u,dt){return (2*u**3-3*u*u+1)*a+(u**3-2*u*u+u)*dt*va+(-2*u**3+3*u*u)*b+(u**3-u*u)*dt*vb}
export function routeXZ(t){t=clamp(t,0,20);let i=0;while(i<keys.length-2&&keys[i+1][0]<t)i++;const a=keys[i],b=keys[i+1],dt=b[0]-a[0],u=clamp((t-a[0])/dt);return [hermite(a[1],b[1],a[3],b[3],u,dt),hermite(a[2],b[2],a[4],b[4],u,dt)]}
export function subjectAt(t){const [x,d]=routeXZ(t),z=shoreZ(x)+d;const floor=sandHeight(x,z);let lift=ease((t-2.5)/1.2)*(.22+.10*Math.sin((t-3)*1.4))* (1-ease((t-17)/1.2));let y=floor+SETTINGS.radius+lift;if(d<.8){const water=seaHeight(x,z,SETTINGS.seaStart+t);y=Math.max(y,water+.17+.03*Math.sin(t*4.3))}if(t>=18.2)y=floor+SETTINGS.radius;return [x,y,z]}
const offsetKeys=[
 [0,-.10,.090,.19,43,0,0,0],[2.55,-.11,.10,.23,46,0,.01,-.014],
 [4,-.14,.12,.32,49,.015,.014,-.03],[8.6,-.16,.13,.38,49,.025,.02,-.04],
 [10.4,-.38,.65,1.25,55,.10,.15,-.45],[11.8,-.48,.74,1.55,55,.15,.20,-.7],
 [13.2,-.15,.12,.38,48,.018,.01,-.045],[16.8,-.16,.10,.33,48,.016,.0,-.03],
 [18.2,-.10,.075,.22,43,.0,.0,0],[18.65,-.19,.18,.56,48,.01,.04,-.09],
 [20,-4,4.6,11,57,2,.18,-12]
];
export function cameraAt(t){let i=0;while(i<offsetKeys.length-2&&offsetKeys[i+1][0]<t)i++;const a=offsetKeys[i],b=offsetKeys[i+1],k=ease((t-a[0])/(b[0]-a[0]));const values=a.slice(1).map((v,j)=>lerp(v,b[j+1],k));const s=subjectAt(t);return {position:s.map((v,j)=>v+values[j]),target:s.map((v,j)=>v+values[j+4]),fov:values[3]}}
