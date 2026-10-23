/* Whole actors match on action; environment/actors/foreground blend separately.
   No fragmented anatomy or image mesh morph. See research/transition-study-v5.md. */
(()=>{
const cv=document.querySelector('canvas'),out=cv.getContext('2d'),W=1080,H=1920,TAU=Math.PI*2;
const mk=(w=W,h=H)=>Object.assign(document.createElement('canvas'),{width:w,height:h});
const sceneA=mk(),sceneB=mk(),mix=mk(),mask=mk(270,480);
const actorA=mk(),actorB=mk(),actorMix=mk();let c=out;
const lerp=(a,b,p)=>a+(b-a)*p,clamp=x=>Math.max(0,Math.min(1,x)),seg=(x,a,b)=>clamp((x-a)/(b-a));
const ease=x=>(x=clamp(x),x*x*x*(x*(x*6-15)+10));
const V=(a,b)=>[a[0]+b[0],a[1]+b[1]],R=(v,a)=>[v[0]*Math.cos(a)-v[1]*Math.sin(a),v[0]*Math.sin(a)+v[1]*Math.cos(a)];
const hash=(n,s=0)=>{const a=Math.sin(n*127.1+s*311.7)*43758.5453;return a-Math.floor(a)};
const ERA_SECONDS=40/35,DURATION=40;
const props={};
const assets=[];
const load=src=>new Promise((resolve,reject)=>{let im=new Image();im.onload=()=>resolve(im);im.onerror=()=>reject(Error(src));im.src=src});
function registeredImage(im,x,y,w,h){const b=im.drawClip;if(b)c.drawImage(im,b[0],b[1],b[2]-b[0],b[3]-b[1],x+b[0]/im.width*w,y+b[1]/im.height*h,(b[2]-b[0])/im.width*w,(b[3]-b[1])/im.height*h);else c.drawImage(im,x,y,w,h)}
function sprite(im,x,y,w,h,a=0,p=[0,0]){c.save();c.translate(x,y);c.rotate(a);registeredImage(im,-p[0]*w,-p[1]*h,w,h);c.restore()}
// The requested wrist must be reachable. Never stretch a segment to a clamped IK target.
function ik(s,p,a,b,side){
 const dx=p[0]-s[0],dy=p[1]-s[1],distance=Math.hypot(dx,dy);
 const d=Math.max(Math.abs(a-b)+.01,Math.min(distance,a+b-.01));
 const angle=Math.atan2(dy,dx),o=Math.acos(Math.max(-1,Math.min(1,(a*a+d*d-b*b)/(2*a*d))));
 return {elbow:V(s,[a*Math.cos(angle+side*o),a*Math.sin(angle+side*o)]),
   wrist:V(s,[d*Math.cos(angle),d*Math.sin(angle)]),reach_error:Math.abs(distance-d)};
}
// Each bone has a fixed length. Local points are sprite registration coordinates.
function bone(im,a,b,top=[.5,.10],bottom=[.5,.91],thickness=.8){
 const local=[(bottom[0]-top[0])*im.width,(bottom[1]-top[1])*im.height],d=[b[0]-a[0],b[1]-a[1]],scale=Math.hypot(...d)/Math.hypot(...local);
 c.save();c.translate(...a);c.rotate(Math.atan2(d[1],d[0]));c.scale(scale,scale*thickness);c.rotate(-Math.atan2(local[1],local[0]));registeredImage(im,-top[0]*im.width,-top[1]*im.height,im.width,im.height);c.restore();
}

function actionTime(t,i){return Math.max(0,Math.min(ERA_SECONDS,t-ERAS[i].t0))}
function around(p,pivot,angle,dy=0){const v=R([p[0]-pivot[0],p[1]-pivot[1]],angle);return [pivot[0]+v[0],pivot[1]+v[1]+dy]}
function region(im,x,y,w,h,lo,hi){c.save();c.beginPath();c.rect(x,y+lo*h,w,(hi-lo)*h);c.clip();sprite(im,x,y,w,h);c.restore()}
function bodyPose(im,x,y,w,h,mouthAnchor,motion,type){
 const headCut=mouthAnchor[1]+(type==='mother'?.155:.235),hip=type==='mother'?.685:.87;
 const pivot=[x+w*(type==='mother'?.57:.52),y+h*hip];
 const neck=[x+w*(type==='mother'?.52:.57),y+h*(headCut-.035)];
 const torso=p=>around(p,pivot,motion.torso_angle,motion.torso_y);
 const head=p=>torso(around(p,neck,motion.head_angle,motion.head_y));
 // Overlap is confined to neck/waist joins. No image mesh or limb scaling.
 region(im,x,y,w,h,hip-.014,1);
 c.save();c.translate(pivot[0],pivot[1]+motion.torso_y);c.rotate(motion.torso_angle);c.translate(-pivot[0],-pivot[1]);
 region(im,x,y,w,h,headCut-.012,hip+.014);
 c.translate(neck[0],neck[1]+motion.head_y);c.rotate(motion.head_angle);c.translate(-neck[0],-neck[1]);
 region(im,x,y,w,h,0,headCut+.012);c.restore();
 return {torso,head,mouth:head([x+mouthAnchor[0]*w,y+mouthAnchor[1]*h]),neck:torso(neck)};
}
function emptyHand(im,wrist,cw,ch,angle=0){
 c.save();c.translate(...wrist);c.rotate(angle);c.translate(-.96*cw,-.58*ch);
 c.beginPath();const points=[[.66,.12],[.82,.11],[.98,.25],[1,.5],[.98,.83],[.84,.98],[.68,.92],[.55,.79],[.55,.60],[.57,.39],[.59,.23]];
 points.forEach((p,k)=>k?c.lineTo(p[0]*cw,p[1]*ch):c.moveTo(p[0]*cw,p[1]*ch));c.closePath();c.clip();registeredImage(im,0,0,cw,ch);c.restore();
}
function actors(t,i){
 const s=assets[i],a=window.RIG_ANCHORS[i],local=actionTime(t,i),performance=window.ACTION_V8.pose(t,t),m=performance.mother,b=performance.baby;
 const mw=280,mh=510,mx=715-a.mother[0]*mw,my=1152-a.mother[1]*mh;
 const mp=bodyPose(s.mother,mx,my,mw,mh,a.mother,m,'mother'),mouth=mp.mouth;
 // The near table stands in front of the knees and supports the resting cup.
 const tableBox=window.TABLE_CROPS[i];c.drawImage(s.table,tableBox[0],0,tableBox[1]-tableBox[0],s.table.height,520,1252,180,253);
 const shoulder=mp.torso([mx+.77*mw,my+.43*mh]),cupAngle=m.tilt;
 const rest=window.TABLE_SURFACE[i].cup_contact;
 const contact=[lerp(rest[0],mouth[0],m.lift)-11*Math.sin(m.lift*Math.PI),lerp(rest[1],mouth[1],m.lift)-7*Math.sin(m.lift*Math.PI)];
 const cw=85,ch=60,grip=V(contact,R([(.96-.40)*cw,(.58-.10)*ch],cupAngle));
 // Rest the active hand on the outer thigh, avoiding an elbow raised at the hip.
 const home=mp.torso([mx+.64*mw,my+.69*mh]);
 const gestureHome=[lerp(home[0],m.target[0],m.gesture),lerp(home[1],m.target[1],m.gesture)];
 const requested=[lerp(gestureHome[0],grip[0],m.reach),lerp(gestureHome[1],grip[1],m.reach)];
 const ma=76,mb=88,mik=ik(shoulder,requested,ma,mb,-1),elbow=mik.elbow;
 bone(s['m-upper'],shoulder,elbow);bone(s['m-lower'],elbow,mik.wrist);
 // The cup is always an independent generated prop. It stays at the table after release.
 sprite(s.freecup,contact[0],contact[1],cw*.80,ch,cupAngle,[.50,.10]);
 // Open / closed generated hand poses share one wrist and one anatomical hand.
 c.save();c.globalAlpha=1-m.grip;sprite(s.openhand,mik.wrist[0],mik.wrist[1],45,34,cupAngle*m.reach+m.hand_angle*m.gesture,[.96,.55]);c.restore();
 c.save();c.globalAlpha=m.grip;emptyHand(s.cuphand,mik.wrist,cw,ch,cupAngle*m.reach);c.restore();
 const bw=220,bh=250,bx=345-a.baby[0]*bw,by=1350-a.baby[1]*bh;
 const bp=bodyPose(s.baby,bx,by,bw,bh,a.baby,b,'baby'),bm=bp.mouth;
 const low=[338,1440];
 const ba=b.tilt,nozzle=[lerp(low[0],bm[0],b.lift)+6*Math.sin(b.lift*Math.PI),lerp(low[1],bm[1],b.lift)-4*Math.sin(b.lift*Math.PI)];
 const leftGrip=V(nozzle,R([-12,36],ba)),rightGrip=V(nozzle,R([12,36],ba));
 const leftHome=bp.torso([310,1450]),rightHome=bp.torso([394,1457]);
 const toyTouch=ACTION_V8.p(t,22.1,22.4,22.95,23.6),target=[lerp(b.target[0],403,toyTouch),lerp(b.target[1],1450,toyTouch)];
 const freeRight=[lerp(rightHome[0],target[0],Math.max(b.gesture,toyTouch)),lerp(rightHome[1],target[1],Math.max(b.gesture,toyTouch))];
 const left=[lerp(leftHome[0],leftGrip[0],b.hold),lerp(leftHome[1],leftGrip[1],b.hold)],right=[lerp(freeRight[0],rightGrip[0],b.hold),lerp(freeRight[1],rightGrip[1],b.hold)];
 const ls=bp.torso([bx+.40*bw,by+.60*bh]),rs=bp.torso([bx+.88*bw,by+.66*bh]);
 const la=53,lb=55,ra=50,rb=52,lik=ik(ls,left,la,lb,1),rik=ik(rs,right,ra,rb,-1),le=lik.elbow,re=rik.elbow;
 bone(s['b-upper'],rs,re,[.40,.16],[.67,.86],.78);bone(s['b-lower-right'],re,rik.wrist,[.70,.16],[.24,.74],.78);
 sprite(s.bottle,nozzle[0],nozzle[1],41,67,ba,[.5,.03]);
 bone(s['b-upper'],ls,le,[.40,.16],[.67,.86],.78);bone(s['b-lower-left'],le,lik.wrist,[.26,.17],[.79,.75],.78);
 c.save();c.strokeStyle=i===8?'#e9d7b1':'#fff5df';c.globalAlpha=.30*(1-m.lift);c.lineWidth=2.3;c.lineCap='round';
 for(let k=0;k<2;k++){c.beginPath();for(let j=0;j<=18;j++){const u=j/18,x=contact[0]-12+k*19+Math.sin(u*5-t*2.4+k)*5,y=contact[1]-7-u*49;j?c.lineTo(x,y):c.moveTo(x,y)}c.stroke()}c.restore();
 const state={mother:{shoulder,elbow,hand:mik.wrist,target:requested,grip,contact,rest,mouth,phase:m.lift,reach:m.reach,grip_phase:m.grip,stage:m.stage,active:m.active,lengths:[ma,mb],reach_error:mik.reach_error,head_angle:m.head_angle,torso_angle:m.torso_angle},baby:{ls,le,left:lik.wrist,left_target:left,rs,re,right:rik.wrist,right_target:right,nozzle,mouth:bm,phase:b.lift,stage:b.stage,active:b.active,lengths:[la,lb,ra,rb],reach_error:Math.max(lik.reach_error,rik.reach_error),head_angle:b.head_angle,torso_angle:b.torso_angle},body_mesh:false,local_time:t,cycle_seconds:40,settled:performance.settled};
 INTERACTION_V8.interaction(c,t,i,props,state);return state;
}

function environment(t,i){
 const im=assets[i].background;
 INTERACTION_V8.background(c,im,t,i);
 INTERACTION_V8.ambient(c,t,i,props);
}
function foreground(t,i){
 const s=assets[i],e=ERAS[i];
 sprite(s.branch,1010,110,230,580,.045*Math.sin(t*1.2)+.016*Math.sin(t*1.9),[.08,.02]);
 c.save();c.translate(56,1940);c.rotate(Math.PI+.07*Math.sin(t*1.1+.6));sprite(s.branch,0,0,190,460,0,[.08,.02]);c.restore();
 c.save();c.fillStyle=e.green;c.globalAlpha=.38;
 for(let k=0;k<5;k++){const u=((t*.10+k*.193)%1+1)%1,x=925-u*680+Math.sin(u*7+k)*35,y=280+u*1100;c.save();c.translate(x,y);c.rotate(t*1.2+k);c.beginPath();c.ellipse(0,0,5,12,0,0,TAU);c.fill();c.restore()}c.restore();
}
function layer(t,i,canvas,part){
 c=canvas.getContext('2d');c.resetTransform();c.clearRect(0,0,W,H);c.imageSmoothingEnabled=i!==29;
 // One absolute camera path shared by every era and layer.
 const x=3.2*Math.sin(t*.25),y=2.1*Math.cos(t*.21),z=1.008+.003*Math.sin(t*.18);
 c.translate(540+x,1260+y);c.scale(z,z);c.translate(-540,-1260);
 if(part==='environment')environment(t,i);
 else if(part==='foreground')foreground(t,i);
 else return actors(t,i);
}
const kind=i=>[7,8,10,12,15,16,23,30,31,33,34].includes(i)?'light-dissolve':[5,6,14,21,24,27,28,29].includes(i)?'paper-feather':'pigment-wash';
const fields=new Map();
function field(i){
 if(fields.has(i))return fields.get(i);
 const values=new Float32Array(270*480);let min=Infinity,max=-Infinity;
 for(let y=0;y<480;y++)for(let x=0;x<270;x++){
  const u=x/269,v=y/479,dx=u-.66,dy=v-.59;
  const d=kind(i)==='paper-feather'?.70*u+.30*(1-v)+.03*Math.sin(v*8+i):Math.hypot(dx,dy*.85)+.028*Math.sin(Math.atan2(dy,dx)*5+i);
  values[y*270+x]=d;min=Math.min(min,d);max=Math.max(max,d);
 }
 for(let k=0;k<values.length;k++)values[k]=(values[k]-min)/(max-min);
 fields.set(i,values);return values;
}
function reveal(p,i){
 out.drawImage(sceneA,0,0);const type=kind(i);
 if(type==='light-dissolve'){out.save();out.globalAlpha=ease(p);out.drawImage(sceneB,0,0);out.restore();return type}
 const g=mask.getContext('2d'),im=g.createImageData(270,480),values=field(i),f=.30,front=(1+2*f)*ease(p)-f;
 for(let k=0;k<values.length;k++){const spatial=ease(clamp((front-values[k])/f)),a=.62*ease(p)+.38*spatial;im.data[k*4]=im.data[k*4+1]=im.data[k*4+2]=255;im.data[k*4+3]=Math.round(a*255)}
 g.putImageData(im,0,0);
 const mc=mix.getContext('2d');mc.resetTransform();mc.clearRect(0,0,W,H);mc.globalCompositeOperation='source-over';mc.drawImage(sceneB,0,0);mc.globalCompositeOperation='destination-in';mc.drawImage(mask,0,0,W,H);mc.globalCompositeOperation='source-over';out.drawImage(mix,0,0);return type;
}
function dissolveLayer(t,from,to,part,alpha){
 const oldState=layer(t,from,actorA,part),newState=layer(t,to,actorB,part);
 const mc=actorMix.getContext('2d');mc.resetTransform();mc.clearRect(0,0,W,H);
 // Premultiplied additive blending avoids loss of opacity at cutout edges.
 mc.globalCompositeOperation='source-over';mc.globalAlpha=1-alpha;mc.drawImage(actorA,0,0);
 mc.globalCompositeOperation='lighter';mc.globalAlpha=alpha;mc.drawImage(actorB,0,0);
 mc.globalCompositeOperation='source-over';mc.globalAlpha=1;out.drawImage(actorMix,0,0);
 return alpha<.5?oldState:newState;
}
const transitionDuration=16/24,half=transitionDuration/2;
function transitionAt(t){for(let i=1;i<35;i++){const boundary=ERAS[i].t0;if(t>=boundary-half&&t<boundary+half)return {from:i-1,to:i,p:(t-boundary+half)/transitionDuration,boundary}}return null}
function caption(i,alpha=1){const e=ERAS[i];out.save();out.globalAlpha=alpha;out.fillStyle=e.line;out.font='500 31px "Microsoft YaHei",sans-serif';out.textAlign='center';out.fillText(e.name,540,1688);out.globalAlpha=alpha*.68;out.font='23px Georgia,serif';out.fillText(e.year<0?`${Math.abs(e.year).toLocaleString('en-US')} BCE`:`${e.year}`,540,1731);out.restore()}
window.renderAt=(t,opt={})=>{
 t=Math.max(0,Math.min(DURATION-1/24,t));let i=opt.era??Math.max(0,ERAS.findIndex(e=>t>=e.t0&&t<e.t1));
 out.resetTransform();out.clearRect(0,0,W,H);let state,transition=null;
 const tr=!opt.noTransition&&opt.era===undefined?transitionAt(t):null;
 if(tr){
  const {from,to,p}=tr;
  layer(t,from,sceneA,'environment');layer(t,to,sceneB,'environment');const type=reveal(p,to);
  // Whole figures blend over five frames at the same action instant.
  const actorAlpha=ease(seg(p,.26,.74));
  state=dissolveLayer(t,from,to,'actors',actorAlpha);
  dissolveLayer(t,from,to,'foreground',ease(seg(p,.12,.94)));
  transition={...tr,type,actorAlpha,actor_fragmentation:false};
  if(p<.5)caption(from,1-ease(seg(p,.15,.48)));else caption(to,ease(seg(p,.52,.85)));
 }else {
  layer(t,i,sceneB,'environment');out.drawImage(sceneB,0,0);
  state=layer(t,i,sceneB,'actors');out.drawImage(sceneB,0,0);
  layer(t,i,sceneB,'foreground');out.drawImage(sceneB,0,0);caption(i);
 }
 const result={era:i,available:!!assets[i],actors:state,transition,shot:ACTION_V8.pose(t,t).shot};window.__state=result;return result;
};
window.__config={width:W,height:H,fps:24,duration:DURATION,frames:DURATION*24,silent:true,cycle_seconds:40,transition_frames:16,actor_blend_frames:8,route:'native 40s / seven continuous interactions / scene-specific environment motion'};

window.__auditAll=()=>{
 const previous=c;c=mk(1,1).getContext('2d');const issues=[];let maxReach=0,maxLengthError=0,maxGripError=0,maxMouthError=0,maxStep=0,last=null;const stepRecords=[];const stages=new Set(),eras=new Set();
 const distance=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
 for(let f=0;f<960;f++){
  const t=f/24,i=ERAS.findIndex(e=>t>=e.t0&&t<e.t1),p=actors(t,i),m=p.mother,b=p.baby;eras.add(i);stages.add(ACTION_V8.pose(t,t).shot);
  const lengths=[distance(m.shoulder,m.elbow),distance(m.elbow,m.hand),distance(b.ls,b.le),distance(b.le,b.left),distance(b.rs,b.re),distance(b.re,b.right)];
  const error=Math.max(...lengths.map((v,k)=>Math.abs(v-[...m.lengths,...b.lengths][k])));
  maxLengthError=Math.max(maxLengthError,error);maxReach=Math.max(maxReach,m.reach_error,b.reach_error);
  if(m.reach_error>.01||b.reach_error>.01||error>1e-6)issues.push({f,i,mother:m.reach_error,baby:b.reach_error,error});
  if(m.grip_phase>.999)maxGripError=Math.max(maxGripError,distance(m.hand,m.grip));
  if(m.stage==='drink')maxMouthError=Math.max(maxMouthError,distance(m.contact,m.mouth));
  if(b.stage==='drink')maxMouthError=Math.max(maxMouthError,distance(b.nozzle,b.mouth));
  if(last){const step=Math.max(distance(last.mother.hand,m.hand),distance(last.baby.right,b.right));maxStep=Math.max(maxStep,step);if(step>12)stepRecords.push({f,i,step,mother:m.stage,baby:b.stage});}last=p;
 }
 c=previous;return {frames:960,era_count:eras.size,shots:[...stages],issues,stepRecords,max_reach_error:maxReach,max_bone_length_error:maxLengthError,max_held_grip_error:maxGripError,max_drink_mouth_error:maxMouthError,max_wrist_step_pixels:maxStep,limits:'Mechanical checks only; no claim of naturalness or full visual review.'};
};
window.__loadPromise=(async()=>{const names=['mother','baby','cuphand','m-upper','m-lower','bottle','b-upper','b-lower-left','b-lower-right','branch','table'];await Promise.all(RIGS.map(async r=>{const s={};await Promise.all(names.map(async n=>{s[n]=await load(r.dir+'/'+n+'.png');s[n].drawClip=window.RIG_CLIPS[r.index][n]}));s.background=await load(r.background);s.freecup=await load('../assets/rig-v7/cup-'+String(r.index).padStart(2,'0')+'.png');s.openhand=await load('../assets/rig-v7/open-hand-'+String(r.index).padStart(2,'0')+'.png');assets[r.index]=s}));await Promise.all(INTERACTION_V8.names.map(async name=>{props[name]=await load("../assets/interaction-v8/"+name+".png")}));await document.fonts.ready;window.renderAt(0);window.__ready=true})();
})();
