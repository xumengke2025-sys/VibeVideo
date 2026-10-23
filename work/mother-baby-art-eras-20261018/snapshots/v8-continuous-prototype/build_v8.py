"""Derive a new version from preserved v7. No v7 source or assets are overwritten."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R/'film/rig-v7.js').read_text(encoding='utf-8')
s=s.replace('const ERA_SECONDS=6,DURATION=ERA_SECONDS*35;\nERAS.forEach((e,i)=>{e.t0=i*ERA_SECONDS;e.t1=(i+1)*ERA_SECONDS});','const ERA_SECONDS=40/35,DURATION=40;\nconst props={};')
s=s.replace('window.ACTION_V7.pose(local,t)','window.ACTION_V8.pose(t,t)')
s=s.replace('const requested=[lerp(home[0],grip[0],m.reach),lerp(home[1],grip[1],m.reach)];','const gestureHome=[lerp(home[0],m.target[0],m.gesture),lerp(home[1],m.target[1],m.gesture)];\n const requested=[lerp(gestureHome[0],grip[0],m.reach),lerp(gestureHome[1],grip[1],m.reach)];')
s=s.replace('45,34,cupAngle*m.reach,[.96,.55]','45,34,cupAngle*m.reach+m.hand_angle*m.gesture,[.96,.55]')
s=s.replace('const low=bp.torso([338,1404]);','const low=[338,1440];')
s=s.replace('const left=V(nozzle,R([-12,36],ba)),right=V(nozzle,R([12,36],ba));','const leftGrip=V(nozzle,R([-12,36],ba)),rightGrip=V(nozzle,R([12,36],ba));\n const leftHome=bp.torso([310,1450]),rightHome=bp.torso([394,1457]);\n const toyTouch=ACTION_V8.p(t,22.1,22.4,22.95,23.6),target=[lerp(b.target[0],403,toyTouch),lerp(b.target[1],1450,toyTouch)];\n const freeRight=[lerp(rightHome[0],target[0],Math.max(b.gesture,toyTouch)),lerp(rightHome[1],target[1],Math.max(b.gesture,toyTouch))];\n const left=[lerp(leftHome[0],leftGrip[0],b.hold),lerp(leftHome[1],leftGrip[1],b.hold)],right=[lerp(freeRight[0],rightGrip[0],b.hold),lerp(freeRight[1],rightGrip[1],b.hold)];')
s=s.replace('const result={era:i,available:!!assets[i],actors:state,transition};','const result={era:i,available:!!assets[i],actors:state,transition,shot:ACTION_V8.pose(t,t).shot};')
s=s.replace('Math.min(34,Math.floor(t/ERA_SECONDS))','Math.max(0,ERAS.findIndex(e=>t>=e.t0&&t<e.t1))')
s=s.replace('return {mother:{shoulder,elbow,hand:', 'const state={mother:{shoulder,elbow,hand:')
s=s.replace('body_mesh:false,local_time:local,cycle_seconds:ERA_SECONDS,settled:performance.settled};','body_mesh:false,local_time:t,cycle_seconds:40,settled:performance.settled};\n INTERACTION_V8.interaction(c,t,i,props,state);return state;')
start=s.index('function environment(t,i){');end=s.index('function foreground(t,i){',start)
s=s[:start]+'''function environment(t,i){
 const im=assets[i].background;
 INTERACTION_V8.background(c,im,t,i);
 INTERACTION_V8.ambient(c,t,i,props);
}
'''+s[end:]
s=s.replace('.11*Math.sin(t*1.35)+.035*Math.sin(t*2.1)','.045*Math.sin(t*1.2)+.016*Math.sin(t*1.9)')
s=s.replace('const transitionDuration=24/24','const transitionDuration=16/24')
s=s.replace('const actorAlpha=ease(seg(p,.375,.625))','const actorAlpha=ease(seg(p,.26,.74))')
s=s.replace("route:'phased independent props + head torso follow-through / one complete 6-second performance per era'","route:'native 40s / seven continuous interactions / scene-specific environment motion'").replace('cycle_seconds:ERA_SECONDS,transition_frames:24,actor_blend_frames:6','cycle_seconds:40,transition_frames:16,actor_blend_frames:8')
start=s.index('window.__auditAll=()=>{');end=s.index('window.__loadPromise=',start)
s=s[:start]+'''window.__auditAll=()=>{
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
'''+s[end:]
s=s.replace('await document.fonts.ready;window.renderAt(0);','await Promise.all(INTERACTION_V8.names.map(async name=>{props[name]=await load("../assets/interaction-v8/"+name+".png")}));await document.fonts.ready;window.renderAt(0);')
(R/'film/rig-v8.js').write_text(s,encoding='utf-8')
# Generic renderer retains deterministic canvas capture and bounded output.
r=(R/'render-v7.mjs').read_text(encoding='utf-8').replace('v7','v8').replace('5040','960').replace('sample?288','sample?240').replace('mode===\'action\'?144','mode===\'action\'?240')
r=r.replace('mode===\'action\'?204+t:t','t').replace('action?204+t:t','t').replace('action?{era:34,noTransition:true}:{}','{}')
r=r.replace("sample=mode==='sample'||mode==='action',start=0","sample=mode==='sample'||mode==='action',start=Number(process.env.START_SECONDS||0)")
r=r.replace("'mother-baby-35-eras-portrait-v8.mp4'","'mother-baby-35-eras-portrait-v8-40s.mp4'")
r=r.replace("const samples=process.env.RIG_SAMPLE?", "const samples=process.env.RIG_SAMPLE?")
(R/'render-v8.mjs').write_text(r,encoding='utf-8')
print('v8 source and renderer generated')
