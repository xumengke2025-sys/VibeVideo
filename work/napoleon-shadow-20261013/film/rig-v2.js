import {ramp, mix, clamp} from './math.js';

// Native artwork coordinates. Parts retain fixed scale; targets never stretch bones.
const A = {
  head: ['general',[140,5,300,380],[230,286]],
  body: ['general',[570,0,410,430],[730,365]],
  upper: ['general',[212,385,215,184],[352,420]],
  fore: ['general',[568,440,358,180],[612,532]],
  thighL: ['general',[99,641,274,217],[330,677]],
  shinL: ['general',[179,778,163,212],[266,814]],
  footL: ['general',[99,923,274,101],[232,958]],
  thighR: ['general',[680,625,282,220],[722,660]],
  shinR: ['general',[731,781,156,212],[783,804]],
  footR: ['general',[737,928,225,96],[805,973]],
  flag: ['general',[1090,0,446,420],[1130,240]],
  sword: ['general',[1010,450,526,160],[1069,522]],
  sash: ['general',[1080,636,456,388],[1231,711]],
  hat: ['jaffa',[54,35,450,497],[167,427]],
  patient: ['jaffa',[574,0,318,526],[755,500]],
  seated: ['jaffa',[1030,214,486,318],[1290,512]],
  reachUpper: ['jaffa',[0,651,228,156],[40,714]],
  reachFore: ['jaffa',[140,674,428,170],[185,743]],
  helper: ['jaffa',[626,530,321,486],[735,973]],
  bed: ['jaffa',[1030,729,489,274],[1270,973]],
  rider: ['alps',[550,0,430,594],[770,307]],
  cape: ['alps',[978,0,558,594],[1007,461]],
  point: ['alps',[983,589,302,286],[1258,830]],
  emperor: ['coronation',[38,0,510,579],[200,554]],
  josephine: ['coronation',[551,100,556,481],[968,180]],
  pope: ['coronation',[1133,0,403,582],[1390,558]],
  royalUpper: ['coronation',[252,700,200,165],[409,799]],
  royalFore: ['coronation',[45,601,275,211],[282,752]],
  royalUpper2: ['coronation',[250,862,197,162],[391,939]],
  royalFore2: ['coronation',[40,766,280,196],[274,899]],
  crown: ['coronation',[552,641,288,282],[700,910]],
  attendant: ['coronation',[1108,583,187,431],[1200,985]],
  attendant2: ['coronation',[1339,583,197,431],[1450,985]],
  horse: ['horseRig',[0,0,1108,517],[1048,411]],
  tail: ['horseRig',[1107,36,429,489],[1154,109]],
  foreUpper: ['horseRig',[30,524,444,214],[96,567]],
  foreLower: ['horseRig',[595,534,295,206],[636,579]],
  hindUpper: ['horseRig',[1074,515,394,230],[1130,575]],
  hindLower: ['horseRig',[98,774,343,237],[148,814]],
  foreHoof: ['horseRig',[620,777,220,223],[783,825]],
  hindHoof: ['horseRig',[1112,773,266,218],[1290,814]],
};
const masks = {
  upper: [[215,395],[428,388],[423,513],[298,571],[216,567]],
  thighL: [[315,652],[374,652],[374,740],[304,836],[223,836],[217,797],[273,673]],
  shinL: [[185,788],[308,781],[341,852],[294,955],[220,976],[178,936]],
  footL: [[98,936],[281,923],[302,972],[374,1024],[98,1024]],
  thighR: [[679,625],[963,625],[963,767],[849,842],[744,833],[679,737]],
  shinR: [[731,781],[872,781],[886,921],[846,989],[773,988],[731,866]],
  footR: [[738,928],[832,928],[892,971],[963,982],[963,1024],[738,1024]],
  reachUpper: [[0,651],[160,667],[222,706],[222,775],[146,802],[0,802]],
  reachFore: [[139,687],[231,691],[568,674],[568,844],[232,844],[139,784]],
  royalUpper: [[253,699],[452,741],[452,865],[332,833],[253,795]],
  royalFore: [[40,595],[188,629],[319,713],[319,810],[182,777],[40,735]],
  royalUpper2: [[250,863],[445,876],[445,1024],[346,1004],[250,945]],
  royalFore2: [[40,765],[170,809],[319,864],[319,962],[176,922],[40,881]],
};

let layer;
function assembly(g, fn) {
  if (!layer || layer.width !== g.canvas.width || layer.height !== g.canvas.height) {
    layer = document.createElement('canvas'); layer.width = g.canvas.width; layer.height = g.canvas.height;
  }
  const c = layer.getContext('2d');
  c.setTransform(1,0,0,1,0,0); c.clearRect(0,0,layer.width,layer.height);
  c.setTransform(g.getTransform()); c.globalAlpha = 1; c.globalCompositeOperation = 'source-over';
  const state = fn(c);
  g.save(); g.setTransform(1,0,0,1,0,0); g.drawImage(layer,0,0); g.restore();
  return state;
}
function draw(g, imgs, key, P, scale=1, angle=0, alpha=1) {
  const [name, r, pin] = A[key];
  g.save(); g.globalAlpha *= alpha; g.translate(...P); g.rotate(angle); g.scale(scale,scale);
  if (masks[key]) {g.beginPath(); masks[key].forEach(([x,y],i)=>i?g.lineTo(x-pin[0],y-pin[1]):g.moveTo(x-pin[0],y-pin[1])); g.closePath(); g.clip();}
  g.drawImage(imgs[name], ...r, r[0]-pin[0],r[1]-pin[1],r[2],r[3]); g.restore();
}
const add=(a,b)=>[a[0]+b[0],a[1]+b[1]];
const sub=(a,b)=>[a[0]-b[0],a[1]-b[1]];
const dist=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
function at(P, scale, angle, native, pin) {
  const x=(native[0]-pin[0])*scale,y=(native[1]-pin[1])*scale;
  return [P[0]+x*Math.cos(angle)-y*Math.sin(angle),P[1]+x*Math.sin(angle)+y*Math.cos(angle)];
}
function bone(g, imgs, key, P, Q, nativeEnd, scale) {
  const v=sub(nativeEnd,A[key][2]);
  draw(g,imgs,key,P,scale,Math.atan2(Q[1]-P[1],Q[0]-P[0])-Math.atan2(v[1],v[0]));
}
function joint(g,P,r=7) {
  g.save();g.fillStyle='#b99755';g.strokeStyle='#77502c';g.lineWidth=1.6;g.beginPath();g.arc(...P,r,0,Math.PI*2);g.fill();g.stroke();g.fillStyle='#715337';g.beginPath();g.arc(...P,r*.32,0,Math.PI*2);g.fill();g.restore();
}
function rod(g,P){g.save();g.globalAlpha=.1;g.strokeStyle='#725943';g.lineWidth=1.3;g.beginPath();g.moveTo(...P);g.lineTo(P[0]+35,1810);g.stroke();g.restore();}

// Return the attainable endpoint as well as the elbow; callers bind props to W.
export function solve(S,T,L1,L2,bend=1) {
  const delta=sub(T,S),wanted=Math.hypot(...delta),d=clamp(wanted,Math.abs(L1-L2)+.01,L1+L2-.01),base=Math.atan2(delta[1],delta[0]);
  const W=[S[0]+Math.cos(base)*d,S[1]+Math.sin(base)*d];
  const angle=base+bend*Math.acos(clamp((L1*L1+d*d-L2*L2)/(2*L1*d),-1,1));
  const E=[S[0]+Math.cos(angle)*L1,S[1]+Math.sin(angle)*L1];
  return {S,E,W,wanted,max:L1+L2,clamped:Math.abs(wanted-d)>.02,error:dist(T,W),boneError:Math.max(Math.abs(dist(S,E)-L1),Math.abs(dist(E,W)-L2))};
}
function arm(g,imgs,S,T,{reach=false,bend=1,royal=0}={}) {
  let k1='upper',end1=[252,536],s1=1,k2='fore',end2=[836,496],s2=.85;
  if(reach){k1='reachUpper';end1=[185,743];s1=1.08;k2='reachFore';end2=[532,714];s2=.66;}
  if(royal===1){k1='royalUpper';end1=[282,752];s1=1.18;k2='royalFore';end2=[127,678];s2=1.18;}
  if(royal===2){k1='royalUpper2';end1=[274,899];s1=1.18;k2='royalFore2';end2=[121,827];s2=1.18;}
  const L1=dist(A[k1][2],end1)*s1,L2=dist(A[k2][2],end2)*s2,z=solve(S,T,L1,L2,bend);
  bone(g,imgs,k1,S,z.E,end1,s1);bone(g,imgs,k2,z.E,z.W,end2,s2);joint(g,z.E,5.5);return z;
}
function leg(g,imgs,hip,sole,left=true) {
  const thigh=left?'thighL':'thighR',shin=left?'shinL':'shinR',foot=left?'footL':'footR';
  const knee=left?[266,814]:[783,804],ankle=left?[232,958]:[805,973],contact=left?[215,1001]:[828,1013],s=1.3;
  const Aft=sub(sole,[(contact[0]-ankle[0])*s,(contact[1]-ankle[1])*s]);
  const z=solve(hip,Aft,dist(A[thigh][2],knee)*s,dist(A[shin][2],ankle)*s,left?1:-1);
  bone(g,imgs,thigh,hip,z.E,knee,s);bone(g,imgs,shin,z.E,z.W,ankle,s);draw(g,imgs,foot,z.W,s);joint(g,z.E,5);return{...z,sole:at(z.W,s,0,contact,ankle)};
}

function patientPose(t) {
  const reaction=ramp(t,21.9,23.1),relax=ramp(t,25,27);
  const P=[857,1508],s=2.06,a=-.012-.019*reaction+.008*relax;
  return {P,s,a,chest:at(P,s,a,[728,204],A.patient[2]),head:at(P,s,a,[777,125],A.patient[2])};
}
export function general(g,imgs,t,{jaffa=false}={}) {
  const prep=jaffa?ramp(t,18,19.25):ramp(t,.8,1.7),act=jaffa?ramp(t,19.1,22.5):ramp(t,1.7,4.6),recover=jaffa?ramp(t,25,27.4):ramp(t,5,6.3);
  const s=1.2,H=[(jaffa?420:480)+(jaffa?18:10)*act-(jaffa?4:5)*recover,1120+5*prep-5*act],a=jaffa?.066*act-.01*recover:-.028*prep+.04*act-.012*recover;
  const P=n=>at(H,s,a,n,A.body[2]);
  return assembly(g,c=>{
    const feet=jaffa?[[295,1540],[571,1540]]:[[343,1540],[648,1540]];
    const legs=[leg(c,imgs,P([629,369]),feet[0],true),leg(c,imgs,P([822,368]),feet[1],false)];
    const backS=P([650,80]),frontS=P([844,80]);
    let flag,contact,sword,zBack,zFront;
    if(jaffa){
      zBack=arm(c,imgs,backS,P([635,283]),{bend:-1});
      const chest=patientPose(t).chest,rest=P([848,292]);
      const T=[mix(rest[0],chest[0],act),mix(rest[1],chest[1],act)];
      draw(c,imgs,'body',H,s,a);
      zFront=arm(c,imgs,frontS,T,{reach:true,bend:1});contact=zFront.W;
    }else{
      const T=[mix(274,280,act),mix(665,536,act)+3*prep];
      zBack=arm(c,imgs,backS,T,{bend:-1});flag=zBack.W;
      draw(c,imgs,'flag',flag,1.23,-.028-.018*prep+.046*(act-recover));
      // Hand covers its own prop attachment; body covers the far shoulder.
      arm(c,imgs,backS,flag,{bend:-1});draw(c,imgs,'body',H,s,a);
      const T2=P([845,315]);zFront=arm(c,imgs,frontS,T2,{bend:1});sword=zFront.W;
      draw(c,imgs,'sword',sword,.61,.87+.07*act);arm(c,imgs,frontS,sword,{bend:1});
    }
    const neck=P([755,14]),headAngle=a+(jaffa?.028*prep+.034*act-.02*recover:-.035*prep+.025*act);
    draw(c,imgs,jaffa?'hat':'head',neck,jaffa?.59:.67,headAngle);
    // Waist sash follows the body once, rather than swinging through its contour.
    draw(c,imgs,'sash',P([822,237]),.30,a+.02*(act-recover));
    rod(c,contact||flag);return{head:neck,hip:H,tilt:a,legs,arms:[zBack,zFront],flag,sword,contact};
  });
}
export function hospital(g,imgs,t) {
  assembly(g,c=>{
    draw(c,imgs,'bed',[934,1517],.82);draw(c,imgs,'seated',[699,1517],.66,-.018*ramp(t,20.5,22));
    const p=patientPose(t);draw(c,imgs,'patient',p.P,p.s,p.a);
    draw(c,imgs,'helper',[153,1519],1.02,.014*ramp(t,19.4,20.8));
  });
  const z=general(g,imgs,t,{jaffa:true});return{...z,patient:patientPose(t),contactError:t>=22.5&&t<25?dist(z.contact,patientPose(t).chest):null};
}

function horseLeg(g,imgs,hip,sole,fore,airAngle=0,far=false) {
  const ku=fore?'foreUpper':'hindUpper',kl=fore?'foreLower':'hindLower',kf=fore?'foreHoof':'hindHoof';
  const endU=fore?[412,698]:[1403,700],endL=fore?[856,702]:[385,948],su=fore?.58:.64,sl=fore?.66:.76,sf=fore?.36:.44;
  const contact=fore?[736,966]:[1257,965],offset=at([0,0],sf,airAngle,contact,A[kf][2]),ankle=sub(sole,offset);
  const z=solve(hip,ankle,dist(A[ku][2],endU)*su,dist(A[kl][2],endL)*sl,fore?1:-1);
  bone(g,imgs,ku,hip,z.E,endU,su);bone(g,imgs,kl,z.E,z.W,endL,sl);draw(g,imgs,kf,z.W,sf,airAngle);
  return{...z,sole:at(z.W,sf,airAngle,contact,A[kf][2]),targetSole:sole,far};
}
export function alpine(g,imgs,t) {
  const prep=ramp(t,34.45,35.35)*(1-ramp(t,35.35,36.1)),rise=ramp(t,35.35,38.1),settle=ramp(t,42.25,46.1),rear=rise*(1-settle),lag=ramp(t,35.6,38.4)*(1-ramp(t,42.55,46.45));
  const H=[925+12*rear,1140+17*prep-15*rear],s=.86,a=.355*rear-.018*prep;
  const P=n=>at(H,s,a,n,A.horse[2]);
  const hoofLift=ramp(t,35.35,37.9)*(1-ramp(t,42.65,45.85));
  const foreNear=[mix(323,262,hoofLift),mix(1540,1201,hoofLift)],foreFar=[mix(369,318,hoofLift),mix(1531,1173,hoofLift)];
  return assembly(g,c=>{
    // Keep the complete horse and seated rider inside the vertical stage.
    c.translate(540,1540);c.scale(.82,.82);c.translate(-540,-1540);
    const hindFar=horseLeg(c,imgs,add(H,[37,-9]),[990,1528],false,0,true);
    const foreHip=P([410,411]);const frontFar=horseLeg(c,imgs,add(foreHip,[32,-6]),foreFar,true,-.23*hoofLift,true);
    const tailP=P([1080,281]);draw(c,imgs,'tail',tailP,.49,a-.08+.14*(rear-lag));
    draw(c,imgs,'horse',H,s,a);
    const hindNear=horseLeg(c,imgs,H,[928,1540],false),frontNear=horseLeg(c,imgs,foreHip,foreNear,true,-.25*hoofLift);
    // Seat is a child of the rigid horse; rider counterbalances, with a delayed cape.
    const saddle=P([720,265]),riderAngle=a*.52-.018*prep;
    const shoulder=at(saddle,1.03,riderAngle,[818,183],A.rider[2]);
    draw(c,imgs,'cape',shoulder,.82,riderAngle-.18+.19*(rear-lag));
    draw(c,imgs,'rider',saddle,1.03,riderAngle);
    draw(c,imgs,'point',shoulder,.61,riderAngle+.62+.025*ramp(t,36.2,37.4));
    rod(c,shoulder);
    return{subject:H,head:P([211,125]),angle:a,saddle,legs:[hindFar,frontFar,hindNear,frontNear],rear,displayScale:.82,displayPivot:[540,1540]};
  });
}

export function coronation(g,imgs,t) {
  const prepare=ramp(t,51.4,52.2),lift=ramp(t,52.2,55.4),offer=ramp(t,55.8,58.1),lower=ramp(t,58.1,60.75);
  const lean=-.056*lift-.020*lower,base=[747-7*offer,1518],s=1.35;
  const P=n=>at(base,s,lean,n,A.emperor[2]);
  const C=[mix(mix(563,435,lift),393,lower),mix(mix(1123,965,lift),1033,lower)];
  const nearS=P([182,138]),farS=add(nearS,[-45,9]);
  return assembly(g,c=>{
    draw(c,imgs,'attendant',[143,1520],.94);draw(c,imgs,'attendant2',[263,1518],.70);
    draw(c,imgs,'pope',[955,1522],1.18);
    const queenAngle=-.003-.008*prepare+.006*lower;
    const back=arm(c,imgs,farS,[C[0]-48,C[1]-5],{royal:2,bend:-1});
    draw(c,imgs,'josephine',[383,1070],1.17,queenAngle);
    draw(c,imgs,'emperor',base,s,lean);
    const front=arm(c,imgs,nearS,[C[0]+48,C[1]-5],{royal:1,bend:-1});
    // Both palms and crown use one pose; trajectories are within both arm reaches.
    draw(c,imgs,'crown',C,.47);
    rod(c,front.W);
    return{crown:C,hands:[back.W,front.W],arms:[back,front],hip:base,tilt:lean,contactError:Math.max(dist(back.W,[C[0]-48,C[1]-5]),dist(front.W,[C[0]+48,C[1]-5]))};
  });
}
