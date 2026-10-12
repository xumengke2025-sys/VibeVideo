import {makeComp,layerSet} from './vendor/claude-ink-comp.mjs';
// Generated complete poses + layered orthographic photography. No skeletal deformation.
const W=1080,H=1920,canvas=document.querySelector('#film');
const renderWidth=Number(new URLSearchParams(location.search).get('width')||W),renderScale=renderWidth/W;
if(![540,1080].includes(renderWidth))throw Error('Supported render widths: 540,1080');
canvas.width=renderWidth;canvas.height=H*renderScale;
const comp=makeComp(canvas,{width:W,height:H}),L=layerSet(W,H,renderScale);
window.__renderBuffers=()=>({logical:[W,H],film:[canvas.width,canvas.height],wet:[L.wet.width,L.wet.height],dry:[L.dry.width,L.dry.height],col:[L.col.width,L.col.height]});
const lib=await (await fetch('./assets/v3/library.json')).json();
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),mix=(a,b,u)=>a+(b-a)*u,smooth=u=>{u=clamp(u);return u*u*(3-2*u)};
const rng=i=>{const q=Math.sin(i*127.1+1798)*43758.5453;return q-Math.floor(q)};
for(const [name,g] of Object.entries(lib))for(const f of g.frames){
 const im=new Image();im.src=f.path;await im.decode();f.image=im;
 // The Claude compositor reads ALPHA as ink density. RGB textures are never fed directly.
 const cv=document.createElement('canvas');cv.width=f.w;cv.height=f.h;const ctx=cv.getContext('2d');ctx.drawImage(im,0,0);
 const raw=ctx.getImageData(0,0,f.w,f.h);f.ink={};
 for(const type of ['wet','dry']){const c=document.createElement('canvas');c.width=f.w;c.height=f.h;const x=c.getContext('2d'),d=x.createImageData(f.w,f.h);
  for(let i=0;i<d.data.length;i+=4){const lum=(raw.data[i]*.2126+raw.data[i+1]*.7152+raw.data[i+2]*.0722)/255;
   const v=clamp((.955-lum)/.9),density=type==='wet'?v*.82:Math.pow(v,1.65)*.58;
   d.data[i+3]=raw.data[i+3]*density;
  }x.putImageData(d,0,0);f.ink[type]=c;
 }
}
let boxes=[];
function draw(name,index,x,y,height,opt={}){
 const g=lib[name],f=g.frames[((Math.floor(index)%g.frames.length)+g.frames.length)%g.frames.length];
 const scale=height/g.nominal; // One uniform scale per sequence; sitting and raised weapons retain their real bounds.
 const px=x-f.root*scale,py=y-f.bottom*scale;
 boxes.push({id:opt.id||name,frame:Math.floor(index),x:px,y:py,w:f.w*scale,h:f.h*scale});
 for(const type of ['wet','dry']){const c=L.ink[type];c.save();c.globalAlpha=opt.alpha??1;
  if(opt.clip){c.beginPath();c.rect(...opt.clip);c.clip()}
  c.translate(x,y);if(opt.angle)c.rotate(opt.angle);c.scale(opt.flip?-scale:scale,scale);
  if(opt.occlude!==false){c.globalCompositeOperation='destination-out';c.drawImage(f.image,-f.root,-f.bottom);c.globalCompositeOperation='source-over'}
  c.drawImage(f.ink[type],-f.root,-f.bottom);c.restore();
 }
 return {f,scale,px,py};
}
function env(name,t,pan=0,alpha=.65){
 const f=lib[name].frames[0];for(const type of ['wet','dry']){const c=L.ink[type];c.save();c.globalAlpha=alpha;
  // Only scenery is projected onto the wider vertical stage; actors retain uniform scale.
  c.drawImage(f.ink[type],-80-pan*.22,-100,1240,2200);c.restore()}
}
function path(points,width=3,alpha=.2,wet=true){const c=wet?L.cw:L.cd;c.save();c.strokeStyle=`rgba(0,0,0,${alpha})`;c.lineWidth=width;c.lineCap='round';c.beginPath();points.forEach(([x,y],i)=>i?c.lineTo(x,y):c.moveTo(x,y));c.stroke();c.restore()}
function wash(x,y,rx,ry,a=.13){const c=L.cw;c.save();const g=c.createRadialGradient(x,y,0,x,y,rx);g.addColorStop(0,`rgba(0,0,0,${a})`);g.addColorStop(1,'rgba(0,0,0,0)');c.translate(x,y);c.scale(1,ry/rx);c.fillStyle=g; c.setTransform(1,0,0,1,0,0);c.restore();c.save();c.translate(x,y);c.scale(rx,ry);const gg=c.createRadialGradient(0,0,0,0,0,1);gg.addColorStop(0,`rgba(0,0,0,${a})`);gg.addColorStop(1,'rgba(0,0,0,0)');c.fillStyle=gg;c.fillRect(-1,-1,2,2);c.restore()}
function sea(t,y=1360,a=.17){for(let j=0;j<9;j++){const p=[];for(let x=-100;x<1200;x+=18)p.push([x,y+j*39+Math.sin(x*.012+t*.8+j)*5]);path(p,2+j*.2,a*(1-j*.08))}}
function footprint(x,y,a=.3){wash(x,y,22,8,a);path([[x-10,y],[x+11,y-1]],6,a,false)}
const cycle=(t,n,period)=>Math.floor(((t%period)+period)%period/period*n);
function walker(name,t,x,y,h,opt={}){return draw(name,cycle(t,lib[name].frames.length,opt.period||1.2),x,y,h,opt)}
function smoke(t,x,y,strength=1){for(let i=0;i<12;i++){const age=clamp(t-i*.035,0,3);if(age<=0)continue;wash(x+Math.sin(i*5)*age*75,y-age*(50+i*5),20+age*(35+i*3),16+age*30,.085*strength*(1-age/3))}}
function ship(x,y,h,t,alpha=1){draw('ship-intact',0,x,y+Math.sin(t)*3,h,{alpha});sea(t,y+7,.07*alpha)}
const cuts=[0,4,9,14,18,24,28,33,38,43,49,55,60];
function scene(t){let s=cuts.findIndex((v,i)=>i<12&&t>=v&&t<cuts[i+1]);if(s<0)s=11;const u=t-cuts[s];
 if(s===0){env('coast',t,0,.48);draw('boat',0,-25,1255,400,{alpha:.55});
  const group=lib.boot2?'boot2':'boot',phase=clamp((u-.5)/2.7),idx=Math.min(11,Math.floor(phase*12));
  draw(group,idx,560,1450,850,{id:'landing-boots'});if(u>1.85){footprint(690,1450,.32);wash(690,1457,75+50*clamp(u-1.85),5,.13)}
  path([[150,1456],[410,1452],[690,1450],[1020,1458]],3,.18);sea(t,1550,.08);
 }else if(s===1){const travel=u*95,cam=u*64;env('coast',t,cam,.58);draw('boat',0,80-cam*.8,1310,200,{alpha:.55});draw('flag',0,140-cam,1530,440,{alpha:.65});
  walker('generalWalk',u,410+travel-cam,1460,650,{period:1.25,id:'general'});
  for(let i=0;i<3;i++)walker('walk2',u+i*.16,90-i*220+travel-cam,1570+i*55,510,{period:1.15,alpha:.8});
 }else if(s===2){const travel=u*150,cam=u*112;env('desert',t,cam,.60);
  for(let row=0;row<2;row++)for(let i=0;i<4;i++)walker('walk2',u+i*.13+row*.22,560+travel-cam-i*250+row*70,1220+row*320,410+row*120,{period:1.15,alpha:row?1:.5,id:`march-${row}-${i}`});
  for(let i=0;i<3;i++)wash(80+i*390-cam*1.3,1720,100,10,.11);
 }else if(s===3){env('desert',t,0,.5);const q=smooth(u/2.7);
  const slots=[[300,1090],[470,1090],[640,1090],[810,1090],[300,1270],[810,1270],[300,1460],[470,1460],[640,1460],[810,1460]];
  slots.forEach(([x,y],i)=>{if(u<2.7)walker('walk2',u+i*.1,mix(x-150,x,q),y,300,{alpha:y<1200?.6:1,period:1.3});else draw('salvo',0,x,y,300,{alpha:y<1200?.6:1})});
 }else if(s===4){env('desert',t,0,.48);
  for(let i=0;i<4;i++)draw('salvo',u<1.8?Math.min(3,Math.floor(u/.45)):u<2.2?4:u<3?5:6,210+i*25,1170+i*180,365,{id:`firing-${i}`,alpha:.7+i*.1});
  for(let i=0;i<3;i++){const q=u-i*.26,x=q<2.3?1100-q*130:801+(q-2.3)*150;draw('horse',cycle(q,12,.95),x,1210+i*220,385,{flip:q>=2.3,alpha:i===1?1:.72,id:`cavalry-${i}`})}
  if(u>1.8)smoke(u-1.8,490,1250,1.3);
 }else if(s===5){env('desert',t,u*14,.54);for(let i=0;i<4;i++)draw('salvo',0,160+i*200,1210,270,{alpha:.5});
  walker('generalWalk',Math.min(u,2.4),430+Math.min(u,2.4)*65,1590,720,{period:1.2,id:'general-result'});
  draw('flag',0,870,1560,580,{alpha:.7});
 }else if(s===6){env('coast',t,u*10,.32);ship(260,940,340,t,.42);ship(850,1120,390,t,.5);ship(530-u*8,1450,620,t,1);if(u>2)smoke(u-2,420,1320,.8);sea(t,1490);
 }else if(s===7){env('coast',t,0,.26);ship(850,970,320,t,.4);draw('ship-hull',0,510,1470,210);
  const q=smooth((u-.9)/2.1);draw('mast',0,535,1320,760,{angle:q*1.24,alpha:u<1.05?1:0,id:'intact-mast'});
  if(u>=1.05)draw('mast-broken',0,535,1320,760,{angle:q*1.24,id:'falling-mast'});
  smoke(u-.55,520,1300,1.4);if(u>2.7){wash(810,1490,210,20,.2);sea(t,1490,.28)}else sea(t,1485,.13);
 }else if(s===8){env('temple',t,0,.35);const q=clamp(u/1.5),x=mix(300,415,q);
  if(u<1.5)walker('surveyor',u,x,1510,650,{period:1.05});else draw('surveyor',Math.min(11,6+Math.floor((u-1.5)/.52)),415,1510,650*lib.surveyor.nominal/482,{id:'surveyor-working'});
  draw('instrument',0,710,1520,585,{id:'telescope'});
 }else if(s===9){if(u<3){env('temple',t,0,.13);draw('stone',0,565,1510,760);const k=cycle(u,6,1.1);draw('hands',k,420+Math.sin(u*5.71)*100,1140,460,{id:'brush-hand'});if(u<2.1)wash(590,1220,160,70,.1*(1-u/2.1));}
  else {draw('book',0,540,1470,780);const v=u-3,k=6+cycle(v,6,1.2);draw('hands',k,665+Math.sin(v*2.4)*35,1260,400,{id:'writing-hand'});
   // A single archaeological contour, never simulated writing or repeated glyphs.
   const outline=[[630,1262],[610,1200],[635,1150],[682,1145],[701,1100],[746,1110],[776,1190],[755,1253],[630,1262]];
   const n=Math.floor(clamp(v/2)*outline.length);if(n>1)path(outline.slice(0,n),2,.45,false);
  }
 }else if(s===10){env('coast',t,0,.4);const idx=Math.min(11,Math.floor(clamp((u-.5)/3.8)*12)),depart=smooth((u-4.6)/1.4),dx=depart*80;
  draw('boat',0,745+dx,1500-depart*35,280,{id:'boarding-boat'});
  // Shore -> step -> bench anchors are keyed to complete generated poses.
  const xs=[285,285,285,285,310,350,390,425,445,455,462,467];
  const ys=[1510,1510,1510,1510,1510,1510,1465,1465,1465,1465,1465,1465];
  draw('boarding',idx,xs[idx]+dx,ys[idx]-depart*35,650,{id:'boarding-general'});
  // Foreground is clipped from the same painted boat; the action stays above the near gunwale.
  if(idx>=6)draw('boat',0,745+dx,1500-depart*35,280,{clip:[350+dx,1400-depart*35,730,300],id:'near-gunwale'});
  sea(t,1540-depart*35,.1);
 }else{env('coast',t,0,.48);ship(785,850,160,t,.28);draw('boat',0,720+u*15,1110-u*16,95-u*3,{alpha:.65});
  const tide=1570-u*105;
  for(let i=0;i<7;i++){const x=365+i*39+(i%2)*55,y=1510-i*66;const fade=clamp((tide-y)/80);footprint(x,y,.32*fade)}
  for(let j=0;j<4;j++){const yy=tide+j*17,p=[];for(let x=0;x<=1080;x+=16)p.push([x,yy+Math.sin(x*.009+u)*13]);path(p,4-j*.7,.22-j*.04)}
  wash(660,tide+55,480,70,.065);draw('flag',0,110,1730,240,{alpha:.0});
 }
 return s;
}
window.stateAt=t=>({time:t,shot:cuts.findIndex((v,i)=>i<12&&t>=v&&t<cuts[i+1])+1,boxes});
window.renderAt=(time,mime)=>{const t=clamp(time,0,59.999);L.clear();boxes=[];const s=scene(t);comp(L,null,{paper:[0,0,1],paperCol:[.955,.955,.94],bleed:3.5,rim:1.15,warm:0,vig:.055});window.__state={time:t,shot:s+1,boxes};return mime?canvas.toDataURL(mime):undefined};
window.__film={version:'v3-generated-poses',duration:60,fps:24,width:W,height:H,generatedVideo:false,compositor:'Claude/Lemo alpha-density wet/dry/paper',scalePolicy:'fixed uniform per sequence'};
window.renderAt(0);window.ready=true;
const seek=document.querySelector('#seek'),button=document.querySelector('#play'),audio=new Audio('out/score.wav');let playing=false,last=0;
if(location.search.includes('render'))document.querySelector('#controls').style.display='none';
seek.oninput=()=>{audio.currentTime=Number(seek.value);window.renderAt(Number(seek.value))};button.onclick=()=>{playing=!playing;if(playing){audio.currentTime=Number(seek.value);audio.play();last=performance.now();requestAnimationFrame(tick)}else audio.pause();button.textContent=playing?'暂停':'播放'};
function tick(now){if(!playing)return;seek.value=Math.min(59.99,Number(seek.value)+(now-last)/1000);last=now;window.renderAt(Number(seek.value));document.querySelector('#time').textContent=Number(seek.value).toFixed(1);if(Number(seek.value)>=59.99){playing=false;audio.pause()}else requestAnimationFrame(tick)}
