// Portrait adaptation: native Huashu materials + sixteen individually generated animation atlases.
const params=new URLSearchParams(location.search),W=+(params.get('width')||1080),H=W*16/9;
const stage=document.querySelector('#stage');stage.width=W;stage.height=H;
const ctx=stage.getContext('2d'),clamp=x=>Math.max(0,Math.min(1,x)),mix=(a,b,u)=>a+(b-a)*u;
const smooth=x=>{x=clamp(x);return x*x*(3-2*x)},ramp=(x,a,b)=>smooth((x-a)/(b-a));
const make=(w=1080,h=1920)=>{const c=document.createElement('canvas');c.width=w;c.height=h;return c};
const keys=['01_cave','02_egypt','03_greek','04_roman','34_shadowpuppet','05_gothic','06_renaissance','32_rembrandt','17_ink','08_impressionism','09_postimp','11_cubism','33_rubberhose','23_dali','13_pop','14_8bit'];
const labels=['史前 · 约公元前16000年','古埃及 · 约公元前1350年','古希腊 · 约公元前530年','古罗马 · 公元79年','北宋 · 约1050年','中世纪 · 约1290年','文艺复兴 · 1503年','荷兰 · 1642年','清初 · 约1690年','法国 · 1874年','法国 · 1889年','法国 · 1912年','北美 · 1930年','西班牙 · 1931年','北美 · 1962年','日本 · 1985年'];
const dark=[true,false,true,false,false,false,true,true,false,false,true,false,false,false,false,false];
const manifest=await (await fetch('assets/rebuild-v3/atlas-manifest.json')).json();
const assets=await Promise.all(manifest.map(async entry=>{const image=new Image();image.src=entry.src;await image.decode();return {...entry,image}}));
const native=[],background=[];
for(let i=0;i<keys.length;i++){
 const c=make(1920,1080),g=c.getContext('2d');
 SCENES[keys[i]].sourceBackground(g);
 native.push(c);
 const p=make(),z=p.getContext('2d');
 // Uniform scale preserves native motif proportions. Portrait framing centers on the original window/material.
 const cx=[580,580,960,580,960,580,610,580,580,580,580,570,580,1050,580,580][i];
 z.imageSmoothingEnabled=i!==15;z.drawImage(c,cx-303.75,0,607.5,1080,0,0,1080,1920);
 if(i===4){z.strokeStyle='#542817';z.lineWidth=24;z.strokeRect(14,14,1052,1892);z.lineWidth=5;z.strokeRect(40,40,1000,1840)}
 // Reserve the shared action stage. This is the same native material, without source furniture.
 if([1,3,5,6,7,9,10,12,15].includes(i)){
  z.save();const fade=z.createLinearGradient(0,1110,0,1460);fade.addColorStop(0,'rgba(0,0,0,0)');fade.addColorStop(1,'#000');
  const floor=make(),fg=floor.getContext('2d');fg.imageSmoothingEnabled=i!==15;
  const patch=[1,3,5,6,7,9,10,12,15].includes(i)?[100,700,200,180]:[100,100,200,180];
  fg.drawImage(c,...patch,0,1050,1080,870);fg.globalCompositeOperation='destination-in';fg.fillStyle=fade;fg.fillRect(0,1050,1080,870);z.drawImage(floor,0,0);z.restore();
 }
 background.push(p);
}
const sprites=new Map();
function sprite(a,name){const key=a.id+name;if(sprites.has(key))return sprites.get(key);const r=a.parts[name],cv=make(r[2],r[3]),g=cv.getContext('2d');g.drawImage(a.image,...r,0,0,r[2],r[3]);
 if(name==='head'){const px=g.getImageData(0,0,cv.width,cv.height);for(let y=0;y<cv.height;y++)for(let x=0;x<cv.width;x++){const k=(y*cv.width+x)*4;if(px.data[k+3]<24||(x<cv.width*.035&&y>cv.height*.60))px.data[k+3]=0}g.putImageData(px,0,0)}
 // Alpha feathering is part of the animated assembly; original generated PNGs remain untouched.
 if(name==='head'){g.globalCompositeOperation='destination-in';const mask=g.createLinearGradient(0,0,0,cv.height);mask.addColorStop(0,'#000');mask.addColorStop(.76,'#000');mask.addColorStop(.94,'#0000');mask.addColorStop(1,'#0000');g.fillStyle=mask;g.fillRect(0,0,cv.width,cv.height)}
 sprites.set(key,cv);return cv;}
function cropPart(c,a,name,x,y,w,h){if(!a.parts[name])return;c.drawImage(sprite(a,name),x,y,w,h)}
const measured=new Map();
function metrics(a,name){const key=a.id+name;if(measured.has(key))return measured.get(key);const r=a.parts[name],cv=make(r[2],r[3]),g=cv.getContext('2d',{willReadFrequently:true});g.drawImage(a.image,...r,0,0,r[2],r[3]);const d=g.getImageData(0,0,cv.width,cv.height).data;
 const xsAt=(y0,y1,x0=0,x1=cv.width)=>{const points=[];for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++)if(d[(y*cv.width+x)*4+3]>110)points.push([x,y]);return points};
 const avg=p=>p.length?[p.reduce((s,v)=>s+v[0],0)/p.length,p.reduce((s,v)=>s+v[1],0)/p.length]:[cv.width/2,cv.height/2];
 const value={w:cv.width,h:cv.height,top:avg(xsAt(0,Math.ceil(cv.height*.07))),bottom:avg(xsAt(Math.floor(cv.height*.94),cv.height)),tip:avg(xsAt(0,cv.height,Math.floor(cv.width*.97))),throat:avg(xsAt(Math.floor(cv.height*.94),cv.height))};measured.set(key,value);return value;
}
function poseAt(u){const reach=ramp(u,.15,.43)*(1-ramp(u,.52,.71));const lift=ramp(u,.52,.69)*(1-ramp(u,.74,.91));
 return{reach,lift,bob:-3*Math.sin(Math.PI*u)**2,fish:u<.78,ground:u<.44,swallow:ramp(u,.67,.77)};}
function poseTip(p){return{x:680+60*p.reach+32*p.lift,y:1140+445*p.reach-48*p.lift};}
function neckRows(a){const key=a.id+'rows';if(measured.has(key))return measured.get(key);const cv=sprite(a,'neck'),g=cv.getContext('2d',{willReadFrequently:true}),d=g.getImageData(0,0,cv.width,cv.height).data,rows=[];for(let y=0;y<cv.height;y++){let l=cv.width,r=0;for(let x=0;x<cv.width;x++)if(d[(y*cv.width+x)*4+3]>100){l=Math.min(l,x);r=Math.max(r,x)}rows.push([l,r])}measured.set(key,rows);return rows;}
function neckTexture(a){const key=a.id+'texture';if(sprites.has(key))return sprites.get(key);const cv=sprite(a,'neck'),rows=neckRows(a),tx=make(200,400),g=tx.getContext('2d');for(let y=0;y<400;y++){const sy=Math.floor((.18+.65*y/400)*cv.height),[l,r]=rows[sy];if(r>l)g.drawImage(cv,l+3,sy,r-l-6,1,0,y,200,1.5)}sprites.set(key,tx);return tx;}
const neckLayer=make();
function drawNeck(c,a,base,top,p){const cv=neckTexture(a),g=neckLayer.getContext('2d');
 // Four shared joints: tucked S at rest, lengthened forward/down during the reach.
 const j1={x:base.x+mix(3,42,p.reach),y:base.y+mix(-23,40,p.reach)},j2={x:mix(base.x+2,top.x-25,p.reach),y:mix(top.y+16,top.y-48,p.reach)};
 const joints=[base,j1,j2,top],left=Math.min(...joints.map(q=>q.x))-58,up=Math.min(...joints.map(q=>q.y))-58,right=Math.max(...joints.map(q=>q.x))+58,down=Math.max(...joints.map(q=>q.y))+58;
 g.reset();g.lineCap='round';g.lineJoin='round';g.strokeStyle='#fff';const at=u=>{const v=1-u;return{x:v*v*v*base.x+3*v*v*u*j1.x+3*v*u*u*j2.x+u*u*u*top.x,y:v*v*v*base.y+3*v*v*u*j1.y+3*v*u*u*j2.y+u*u*u*top.y}};for(let k=0;k<64;k++){const q=at(k/64),r=at((k+1)/64);g.lineWidth=mix(94,56,k/64);g.beginPath();g.moveTo(q.x,q.y);g.lineTo(r.x,r.y);g.stroke()}
 g.globalCompositeOperation='source-in';g.drawImage(cv,left,up,right-left,down-up);g.globalCompositeOperation='source-over';c.drawImage(neckLayer,0,0);return joints;
}
function actors(c,i,p,t,u){const a=assets[i];if(!a)return;const tip=poseTip(p),m=metrics(a,'head'),headW=365,s=headW/m.w;
 const angle=p.reach*.80-p.lift*.24,ca=Math.cos(angle),sa=Math.sin(angle),joint=[mix(m.throat[0],m.w*.36,p.reach),mix(m.throat[1],m.h*.47,p.reach)],vx=(joint[0]-m.tip[0])*s,vy=(joint[1]-m.tip[1])*s;
 const throat={x:tip.x+ca*vx-sa*vy-6,y:tip.y+sa*vx+ca*vy-18*(1-p.reach)};
 c.save();c.imageSmoothingEnabled=i!==15;
 // Same mild reaction in every era: notice, lean back, then look down at the missing fish.
 const owner=a.parts.owner,ownerW=i===0?415:i===2?360:340,ownerH=ownerW*owner[3]/owner[2];
 const notice=ramp(u,.49,.59)*(1-ramp(u,.68,.80)),look=ramp(u,.69,.81)*(1-ramp(u,.90,1));
 c.save();c.translate(865,1640);c.rotate(.045*notice-.060*look);c.scale(1,1+.018*notice-.025*look);cropPart(c,a,'owner',-ownerW/2,-ownerH,ownerW,ownerH);c.restore();
 const b=a.parts.body,bw=440,bh=bw*b[3]/b[2],bodyTop=1650-bh+p.bob;cropPart(c,a,'body',112,bodyTop,bw,bh);
 const base={x:112+bw*.85,y:bodyTop+bh*.12};
 const joints=drawNeck(c,a,base,throat,p);
 // A small extra overlap hides the atlas shoulder cut while retaining the original painted shape.
 c.save();c.translate(tip.x,tip.y);c.rotate(angle);cropPart(c,a,'head',-m.tip[0]*s,-m.tip[1]*s,m.w*s,m.h*s);c.restore();
 if(p.fish){const ground=p.ground,grab=ramp(t%2.25/2.25,.44,.48);const fx=ground?740:tip.x-60*p.swallow,fy=ground?1600:tip.y+9-20*p.swallow;
  const fish=a.parts.fish,fw=142*(1-p.swallow),fh=fw*fish[3]/fish[2];c.save();c.translate(fx,fy);c.rotate(ground?-.04:-.8*p.lift);cropPart(c,a,'fish',-fw*.55,-fh*.5,fw,fh);c.restore();
 }
 c.restore();return{beak:tip,throat,neckJoints:joints,fishGround:p.ground,ownerFeet:[865,1640],ownerReaction:{notice,look}};
}
const sceneA=make(),sceneB=make();
function drawScene(c,i,p,t,labelAlpha=1){c.reset();c.drawImage(background[i],0,0);const state=actors(c,i,p,t,stateAt(t).u);
 c.save();c.globalAlpha=labelAlpha;c.font='500 34px "Microsoft YaHei",sans-serif';c.textAlign='center';c.textBaseline='middle';
 const tw=c.measureText(labels[i]).width;c.fillStyle='rgba(25,24,19,.66)';c.beginPath();c.roundRect(540-tw/2-23,111,tw+46,60,30);c.fill();c.fillStyle='#fff2d9';c.fillText(labels[i],540,141,960);c.restore();return state;}
export function stateAt(t){t=Math.max(0,Math.min(39.958333,t));const i=Math.max(0,Math.min(15,Math.floor((t-2)/2.25))),u=t<2?0:t>=38?1:((t-2)/2.25-i);return{t,era:i,u,pose:poseAt(u),label:labels[i]};}
export function renderAt(t){const state=stateAt(t),i=state.era,p=state.pose,u=state.u,local=(t-2)-i*2.25;
 const blend=i>0&&t>=2&&local<.5?smooth(local/.5):1;
 const ac=sceneA.getContext('2d'),bc=sceneB.getContext('2d');const geo=drawScene(ac,i,p,t,blend);
 ctx.reset();ctx.scale(W/1080,H/1920);
 if(blend<1){drawScene(bc,i-1,{...p,fish:false},t,1-blend);ctx.drawImage(sceneB,0,0);ctx.globalAlpha=blend;ctx.drawImage(sceneA,0,0);ctx.globalAlpha=1}else ctx.drawImage(sceneA,0,0);
 window.__state={...state,...geo,transition:blend,asset:auditAsset(i)};return window.__state;
}
function auditAsset(i){return assets[i]?.src||'MISSING'}
window.renderAt=renderAt;window.stateAt=stateAt;window.__ready=true;window.__assetsLoaded=assets.length;window.__backgrounds=keys;renderAt(0);
if(!params.has('render')){const btn=document.querySelector('#play'),seek=document.querySelector('#seek'),time=document.querySelector('#time');const audio=new Audio('audio/score.wav');let playing=false,base=0,start=0;
 btn.onclick=()=>{playing=!playing;btn.textContent=playing?'暂停':'播放';if(playing){base=+seek.value;start=performance.now();audio.currentTime=base;audio.play()}else audio.pause()};
 seek.oninput=()=>{base=+seek.value;start=performance.now();audio.currentTime=base;renderAt(base)};
 const loop=now=>{if(playing){const t=base+(now-start)/1000;if(t>=40){playing=false;audio.pause();btn.textContent='播放'}else{seek.value=t;time.textContent=t.toFixed(2);renderAt(t)}}requestAnimationFrame(loop)};requestAnimationFrame(loop);
}else document.body.classList.add('render');
