import {backgrounds} from './run-v4-backgrounds.js';
// V4: generated animation drawings, continuous world/camera, absolute-time events.
const plan=await(await fetch('production-plan-run-v4.json')).json(),shots=plan.timeline.shots;
const Q=new URLSearchParams(location.search),W=1080,H=1920,FPS=24,test=Q.has('ink')||Q.has('era');
const canvas=document.querySelector('canvas');canvas.width=+(Q.get('width')||W);canvas.height=canvas.width*16/9;
const g=canvas.getContext('2d'),P=PAINT,{lerp:L,clamp:C,ss:S,rng}=U;
const make=(w=W,h=H)=>Object.assign(document.createElement('canvas'),{width:w,height:h});
const manifest=await(await fetch('assets/run-v4/manifest.json')).json(),assets={};
for(const m of manifest){const arr=await Promise.all(m.cells.map(async v=>{const i=new Image();i.src=`assets/run-v4/era-${String(m.era).padStart(2,'0')}/${v.name}`;await i.decode();return i}));const upper=arr.slice(8,12).map((im,k)=>{const cv=make(384,384),z=cv.getContext('2d');z.drawImage(im,0,0);z.globalCompositeOperation='destination-in';const pts=k===1?[[0,0],[1,0],[1,.98],[.90,.89],[.72,.65],[.62,.60],[.53,.64],[.40,.64],[.27,.61],[.12,.57],[0,.57]]:[[0,0],[1,0],[1,.55],[.75,.55],[.64,.60],[.53,.64],[.40,.64],[.27,.61],[.12,.57],[0,.57]];z.beginPath();pts.forEach((p,i)=>i?z.lineTo(p[0]*384,p[1]*384):z.moveTo(p[0]*384,p[1]*384));z.closePath();z.fill();return cv});assets[m.era]={drawings:arr,upper,meta:m};}
if(!test&&(manifest.length!==16||Array.from({length:16},(_,i)=>i+1).some(i=>!assets[i])))throw Error('All sixteen era atlases are required.');
await document.fonts.ready;
// Coordinates are normalized in the untrimmed generated cells. Hip and ground are stable.
const headInk=[[[.75,.26],[.80,.34],[.98,.38],[.70,.49]],[[.79,.41],[.85,.52],[.97,.71],[.74,.59]],[[.75,.23],[.80,.28],[.96,.20],[.70,.44]],[[.70,.10],[.76,.12],[.86,.005],[.72,.37]]];
const headNew=[[[.75,.26],[.80,.34],[.98,.38],[.70,.49]],[[.80,.52],[.86,.64],[.98,.85],[.74,.62]],[[.75,.21],[.80,.27],[.98,.14],[.70,.44]],[[.70,.08],[.76,.12],[.86,.005],[.72,.37]]];
const targetHead=structuredClone(headInk);targetHead[1]=[[.79,.50],[.85,.61],[.97,.80],[.74,.63]];
const fixed=[[.10,.50],[.25,.37],[.43,.35],[.48,.50],[.25,.59],[.54,.61],[.62,.62],[.1,.64],[.9,.85]];
function field(x,y,src,dst){let sx=0,sy=0,sw=0;for(let i=0;i<src.length;i++){const d=(x-src[i][0])**2+(y-src[i][1])**2,w=1/(d*d+.000002);sx+=(dst[i][0]-src[i][0])*w;sy+=(dst[i][1]-src[i][1])*w;sw+=w}return[x+sx/sw,y+sy/sw]}
function triangle(ctx,img,s,d){const [a,b,c]=s,[u,v,w]=d,den=(b[0]-a[0])*(c[1]-a[1])-(c[0]-a[0])*(b[1]-a[1]);if(Math.abs(den)<1e-5)return;
 const A=((v[0]-u[0])*(c[1]-a[1])-(w[0]-u[0])*(b[1]-a[1]))/den,B=((v[1]-u[1])*(c[1]-a[1])-(w[1]-u[1])*(b[1]-a[1]))/den,
 D=((w[0]-u[0])*(b[0]-a[0])-(v[0]-u[0])*(c[0]-a[0]))/den,E=((w[1]-u[1])*(b[0]-a[0])-(v[1]-u[1])*(c[0]-a[0]))/den;
 ctx.save();ctx.beginPath();const mid=[d.reduce((s,p)=>s+p[0],0)/3,d.reduce((s,p)=>s+p[1],0)/3];d.forEach((p,i)=>{const len=Math.hypot(p[0]-mid[0],p[1]-mid[1])||1,q=[p[0]+.65*(p[0]-mid[0])/len,p[1]+.65*(p[1]-mid[1])/len];i?ctx.lineTo(...q):ctx.moveTo(...q)});ctx.closePath();ctx.clip();ctx.transform(A,B,D,E,u[0]-A*a[0]-D*a[1],u[1]-B*a[0]-E*a[1]);ctx.drawImage(img,0,0,384,384);ctx.restore();}
const morphLayer=make(384,384),morphG=morphLayer.getContext('2d'),partLayer=make(384,384),partG=partLayer.getContext('2d');
function mesh(img,src,dst,n=16){partG.reset();
 for(let y=0;y<n;y++)for(let x=0;x<n;x++){const s=[[x/n,y/n],[(x+1)/n,y/n],[(x+1)/n,(y+1)/n],[x/n,(y+1)/n]],d=s.map(p=>field(...p,src,dst));for(const tr of [[0,1,2],[0,2,3]])triangle(partG,img,tr.map(i=>s[i].map(v=>v*384)),tr.map(i=>d[i].map(v=>v*384)))}
 return partLayer;}
function warp(img,k,target,era){return mesh(img,[...fixed,...(era===9?headInk:headNew)[k]],[...fixed,...target],20)}
function feeding(a,p,local,e){let k=Math.min(2,Math.floor(p)),j=k+1,f=p-k;if(local>e.fishGone){const u=S(e.fishGone,e.neckTucked,local);if(u<.5){k=3;j=2;f=u*2}else{k=2;j=0;f=(u-.5)*2}}const target=targetHead[k].map((v,i)=>v.map((z,h)=>L(z,targetHead[j][i][h],f)));morphG.reset();const chosen=f<.5?k:j;morphG.drawImage(warp(a.upper[chosen],chosen,target,window.__era),0,0);return{image:morphLayer,tip:target[2],eye:target[1]}}
const palettes=[['#a2744c','#302622','#4f5549','#c28e55'],['#ead3a1','#433326','#67735a','#b88e54'],['#b75e2d','#14100d','#29221b','#cc7e47'],['#ddd0ad','#3d5354','#637b61','#c0a16e'],['#f6dca3','#51311e','#a35c38','#b7834b'],['#e8dcc1','#3f5a63','#496448','#cfb56a'],['#8c9b8c','#183b41','#49543c','#96855e'],['#33291d','#161916','#4e4935','#9c7c42'],['#efe6d0','#353a36','#738077','#b7b198'],['#e2e2d1','#6e9eaa','#8fa778','#d1c799'],['#e3bc5b','#244c68','#485d3c','#a48142'],['#d2b68c','#475463','#6f775b','#ad966c'],['#e5e0ce','#3d3c38','#6c6b5d','#b7b19b'],['#edcf8c','#3b7380','#697d53','#bb905c'],['#fae1a7','#194995','#398743','#ead345'],['#b8e4f0','#2769a8','#398742','#c6ad72']];
const sceneDistance=t=>550*t+5*t*t; // continuous art-space path, pace grows throughout the film.
const screenX=t=>375+20*Math.sin(t*.6);const baseY=1450,birdSize=510,scale=birdSize/384;
const scenery=backgrounds(P,U,make,palettes);
const footSource=[[[.13,.85],[.72,.86]],[[.34,.74],[.46,.87]],[[.12,.85],[.77,.83]],[[.08,.77],[.87,.78]],[[.12,.86],[.72,.87]],[[.44,.87],[.60,.73]],[[.12,.85],[.77,.83]],[[.08,.76],[.87,.76]]];
function runFeet(cycle){return[0,.5].map(offset=>{const p=(cycle+offset)%1;if(p<.6)return[.72-(310/birdSize)*p,.855];const f=(p-.6)/.4;return[L(.72-(310/birdSize)*.6,.72,f),.855-.19*Math.sin(Math.PI*f)]}).sort((a,b)=>a[0]-b[0])}
function runningLegs(a,idx,cycle){const feet=runFeet(cycle),src=footSource[idx].slice().sort((a,b)=>a[0]-b[0]),anchors=[[.15,.57],[.3,.58],[.45,.60],[.60,.60],[.75,.57]];
 // Retain authored avian hocks; large generic retargeting folds thin limbs.
 const limited=feet.map((v,i)=>[src[i][0]+C(v[0]-src[i][0],-.12,.12),src[i][1]+C(v[1]-src[i][1],-.07,.07)]);
 return mesh(a.drawings[idx],[...anchors,...src],[...anchors,...limited],16);
}
function phase(local,e){if(local<e.reachStart)return 0;if(local<=e.grab)return S(e.reachStart,e.grab,local);if(local<e.headUp)return 1+2*S(e.grab,e.headUp,local);if(local<=e.fishGone)return 3;if(local<e.neckTucked)return 3*(1-S(e.fishGone,e.neckTucked,local));return 0;}
function bird(ctx,a,t,local,e,x,y){const f=phase(local,e),cycle=((sceneDistance(t)/310)%1),idx=Math.floor(cycle*8),sz=birdSize;const bob=-5*Math.sin(cycle*Math.PI*4);let feed=feeding(a,f,local,e);
 ctx.save();ctx.translate(x-sz*.45,y-sz*.84+bob);ctx.imageSmoothingEnabled=true;
 // Run drawings remain active underneath the feeding upper body. Soft overlap lies in belly plumage.
 const contour=[[0,0],[1,0],[1,.54],[.75,.55],[.64,.60],[.53,.63],[.40,.635],[.27,.61],[.12,.57],[0,.57]];
 const cutPath=()=>{ctx.beginPath();contour.forEach((p,i)=>i?ctx.lineTo(p[0]*sz,p[1]*sz):ctx.moveTo(p[0]*sz,p[1]*sz));ctx.closePath()};
 ctx.save();ctx.beginPath();ctx.rect(0,sz*.57,sz,sz*.43);ctx.clip();ctx.drawImage(runningLegs(a,idx,cycle),0,-bob,sz,sz);ctx.restore();
 ctx.drawImage(feed.image,0,0,sz,sz);ctx.restore();
 const tip={x:x-sz*.45+feed.tip[0]*sz,y:y-sz*.84+bob+feed.tip[1]*sz},eye={x:x-sz*.45+feed.eye[0]*sz,y:y-sz*.84+bob+feed.eye[1]*sz};return{tip,eye,cycle,bob};}
function tight(ctx,img,x,y,w,h,align='bottom'){const data=assets[window.__era]?.meta;const k=assets[window.__era]?.drawings.indexOf(img),box=data?.cells[k]?.alphaBounds||[0,0,384,384];ctx.drawImage(img,...[box[0],box[1],box[2]-box[0],box[3]-box[1]],x-w/2,align==='bottom'?y-h:y-h/2,w,h)}
function ownerImage(a,u,owner){const neutral=a.meta.cells[12].alphaBounds,down=a.meta.cells[13].alphaBounds;
 // Morph the two generated head drawings toward a shared intermediate, without
 // a transparent double head. Lower torso/feet are fixed mesh constraints.
 const avian=['great_white_pelican','great_cormorant','grey_heron','common_kingfisher','bald_eagle'].includes(owner);
 const toNorm=(p,b)=>[(b[0]+p[0]*(b[2]-b[0]))/384,(b[1]+p[1]*(b[3]-b[1]))/384];
 const h0=avian?[[.27,.10],[.03,.17],[.34,.30]]:[[.22,.12],[.04,.22],[.33,.30]],h1=avian?[[.23,.24],[.20,.50],[.34,.34]]:[[.21,.39],[.13,.59],[.34,.34]];
 const k=u<.5?12:13,b=k===12?neutral:down,ss=(k===12?h0:h1).map(p=>toNorm(p,b));
 const tt=h0.map((p,j)=>toNorm([L(p[0],h1[j][0],u),L(p[1],h1[j][1],u)],b)),fix=[[.47,.5],[.66,.5],[.75,.73],[.3,.85],[.6,.95],[.9,.85]].map(p=>toNorm(p,b));
 return mesh(a.drawings[k],[...fix,...ss],[...fix,...tt],16);
}
function foreground(ctx,frame,i){if(test)return;let s=i,bound=shots[i].endFrameExclusive,start=shots[i].startFrame+shots[i].events.safeCutStart,end=bound+4;
 if(i>0&&frame<shots[i].startFrame+4){s=i-1;bound=shots[s].endFrameExclusive;start=shots[s].startFrame+shots[s].events.safeCutStart;end=bound+4}
 if(s===15||frame<start||frame>=end)return;
 const x=frame<bound?L(1800,540,S(start,bound,frame)):L(540,-850,S(bound,end,frame)),rock=s%3===0;
 ctx.save();ctx.translate(x,0);ctx.fillStyle=rock?'#39332a':'#352e23';ctx.beginPath();ctx.moveTo(-710,0);ctx.bezierCurveTo(-660,450,-800,850,-690,1920);ctx.lineTo(710,1920);ctx.bezierCurveTo(820,1220,650,650,710,0);ctx.closePath();ctx.fill();ctx.clip();
 ctx.strokeStyle=rock?'#5b5143':'#64523c';ctx.lineWidth=8;
 for(let k=0;k<22;k++){const z=-690+k*66;ctx.beginPath();ctx.moveTo(z,0);ctx.bezierCurveTo(z+75,530,z-80,1380,z+20,1920);ctx.stroke()}
 ctx.globalAlpha=.23;ctx.drawImage(assets[s+1].drawings[15],-670,0,1340,1920);ctx.restore();
}
function render(t){t=C(t,0,30.999999);const frame=Math.floor(t*24+.0001);let i=shots.findIndex(s=>frame>=s.startFrame&&frame<s.endFrameExclusive);if(i<0)i=frame<24?0:15;if(test)i=Q.has('era')?Number(Q.get('era'))-1:8;const sh=shots[i],a=assets[i+1];window.__era=i+1;const local=test?(t*24)%sh.frames:frame-sh.startFrame,e=sh.events;
 g.reset();g.scale(canvas.width/W,canvas.height/H);g.fillStyle=palettes[i][3];g.fillRect(0,0,W,H);g.save();g.translate(0,-160);
 const wx=sceneDistance(t),camera=wx-screenX(t);scenery.draw(g,i,camera,t);
 // Owner and fish stay at a fixed world location; the camera overtakes them.
 const grabT=test?(t-local/24+e.grab/24):(sh.startFrame+e.grab)/24;
 const birdX=screenX(t)+(test?0:-750*(1-S(0,.75,t))+1100*S(725/24,741/24,t)),contactX=screenX(grabT)+birdSize*.52;
 const fishX=sceneDistance(grabT)+birdSize*.52-camera;
 const model=plan.fauna.models[sh.owner],pixelsPerMetre=birdSize*.60/.40;
 const mh=model.modelStandingHeightM||model.modelSeatedHeightM||model.modelPerchedHeightM||model.modelShoulderHeightM;
 const oh=mh*pixelsPerMetre,box=a.meta.cells[12].alphaBounds,ow=oh*(box[2]-box[0])/(box[3]-box[1]);const react=S(e.grab+2,e.fishGone+3,local);
 const ownerX=fishX+ow*.40+Math.min(80,oh*.12);
 if(sh.owner==='common_kingfisher'){g.fillStyle='#777666';g.beginPath();g.ellipse(ownerX,baseY-25,60,18,0,0,Math.PI*2);g.fill()}
 // Two generated reaction poses, aligned by feet, preserving animal body scale.
 g.save();const op=react<.5?12:13,ob=a.meta.cells[op].alphaBounds,oi=ownerImage(a,react,sh.owner);g.drawImage(oi,ob[0],ob[1],ob[2]-ob[0],ob[3]-ob[1],ownerX-ow/2,baseY-35-oh,ow,oh);g.restore();
 const bp=bird(g,a,t,local,e,birdX,baseY);
 const fw=birdSize*(sh.fishLengthM/.62),fish=a.drawings[14];let fishState='ground';
 if(local<e.grab){tight(g,fish,fishX,baseY-20,fw,fw*.43,'center')}
 else if(local<e.fishGone){fishState=local<e.swallowStart?'bill':'mouth';const p=S(e.swallowStart,e.fishGone,local),angle=Math.atan2(bp.tip.y-bp.eye.y,bp.tip.x-bp.eye.x);g.save();g.translate(bp.tip.x,bp.tip.y);g.rotate(angle);g.scale(-1,1);
 // Fish head points toward mouth. Mouth clipping consumes head first; tail remains until final frame.
 g.beginPath();g.rect(fw*p-fw*.20,-fw,fw*(1-p)+fw*.20,fw*2);g.clip();tight(g,fish,fw*.4,0,fw,fw*.43,'center');g.restore()}
 else fishState='swallowed';
 // Natural foreground reeds appear only after the complete swallow/retraction window.
 // Generated same-medium bank reeds pass at foreground depth.
 for(let k=0;k<3;k++){const rx=((k*560-camera*1.4)%1680+1680)%1680-350;g.globalAlpha=.95;tight(g,a.drawings[15],rx,2070,360,470);g.globalAlpha=1}
 g.restore();
 // Era/year only, kept off the action stage.
 g.fillStyle=[0,2,7,10].includes(i)?'#f2e0b3':'#393b32';g.font='40px Kai, KaiTi, serif';g.textAlign='left';g.fillText(sh.era+' · '+sh.date,78,160);
 foreground(g,frame,i);
 if(frame>737&&!test){const exit=S(738,744,frame);g.fillStyle=`rgba(20,22,20,${exit})`;g.fillRect(0,0,W,H)}
 window.__state={frame,era:i+1,local,phase:phase(local,e),fishState,worldX:wx,cameraX:camera,screenX:birdX,ownerX,tip:bp.tip,cycle:bp.cycle};
}
window.renderAt=render;render(0);window.__ready=true;
if(!Q.has('render')){const start=performance.now();function loop(now){render(((now-start)/1000)%31);requestAnimationFrame(loop)}requestAnimationFrame(loop)}

