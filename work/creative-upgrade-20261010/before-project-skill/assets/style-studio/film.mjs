import {clamp,ease,lerp,progress,captionAt,validate} from './timeline.mjs';
const clip=new URLSearchParams(location.search).get('clip')||'one-way';
if(!/^[a-z0-9-]+$/.test(clip))throw Error('Invalid clip');
const plan=await (await fetch(`clips/${clip}.json`)).json();
const errors=validate(plan);if(errors.length)throw Error(errors.join('\n'));
const canvas=document.getElementById('film'),g=canvas.getContext('2d');
const W=1280,H=720,white='#e5eef2',faint='#94bdd3',blue='#12385f',red='#b24236';
const font='"Microsoft YaHei", "Noto Sans CJK SC", sans-serif';
const technical='"Bahnschrift", "Consolas", monospace';
function rng(seed){return ()=>{seed|=0;seed=seed+0x6d2b79f5|0;let a=Math.imul(seed^seed>>>15,1|seed);a^=a+Math.imul(a^a>>>7,61|a);return ((a^a>>>14)>>>0)/4294967296;};}
const paper=document.createElement('canvas');paper.width=W;paper.height=H;const p=paper.getContext('2d');
const grad=p.createLinearGradient(0,0,W,H);grad.addColorStop(0,'#143a65');grad.addColorStop(.5,'#1b4b77');grad.addColorStop(1,'#102f51');p.fillStyle=grad;p.fillRect(0,0,W,H);
const random=rng(plan.seed);for(let i=0;i<4800;i++){p.fillStyle=i%2?'rgba(190,225,245,.035)':'rgba(4,22,44,.08)';p.fillRect(random()*W,random()*H,random()*1.5+.4,random()*6+.5);}
for(let x=30;x<W;x+=24){p.strokeStyle='rgba(170,210,235,.045)';p.lineWidth=.7;p.beginPath();p.moveTo(x,0);p.lineTo(x,H);p.stroke();}
for(let y=24;y<H;y+=24){p.beginPath();p.moveTo(0,y);p.lineTo(W,y);p.stroke();}
function line(points,{color=white,width=2,dash=[],alpha=1,amount=1}={}){
 if(amount<=0)return;g.save();g.globalAlpha*=alpha;g.strokeStyle=color;g.lineWidth=width;g.setLineDash(dash);g.lineCap='round';g.lineJoin='round';
 let length=0;const ls=[];for(let i=1;i<points.length;i++){const d=Math.hypot(points[i][0]-points[i-1][0],points[i][1]-points[i-1][1]);ls.push(d);length+=d;}
 let remaining=length*clamp(amount);g.beginPath();g.moveTo(...points[0]);
 for(let i=1;i<points.length;i++){const fraction=Math.min(1,remaining/(ls[i-1]||1));g.lineTo(lerp(points[i-1][0],points[i][0],fraction),lerp(points[i-1][1],points[i][1],fraction));remaining-=ls[i-1];if(remaining<=0)break;}g.stroke();g.restore();
}
function rect(x,y,w,h,opt={}){line([[x,y],[x+w,y],[x+w,y+h],[x,y+h],[x,y]],opt);}
function text(s,x,y,size=18,color=white,align='left',family=font){g.fillStyle=color;g.font=`${size}px ${family}`;g.textAlign=align;g.fillText(s,x,y);g.textAlign='left';}
function circle(x,y,r,color=white,fill=false){g.beginPath();g.arc(x,y,r,0,Math.PI*2);g.strokeStyle=color;g.lineWidth=1.5;if(fill){g.fillStyle=color;g.fill();}else g.stroke();}
function arrow(x,y,dx,dy,color=white,scale=1){line([[x,y],[x+dx,y+dy]],{color,width:1.7*scale});const a=Math.atan2(dy,dx),z=7*scale;line([[x+dx-z*Math.cos(a-.5),y+dy-z*Math.sin(a-.5)],[x+dx,y+dy],[x+dx-z*Math.cos(a+.5),y+dy-z*Math.sin(a+.5)]],{color,width:1.7*scale});}
function leader(label,n,x,y,tx,ty){line([[x,y],[x+25,y],[tx,ty]],{color:faint,width:1});circle(x-14,y,11,faint);text(String(n),x-14,y+4,11,faint,'center',technical);text(label,x+4,y-9,16,faint);circle(tx,ty,3,faint,true);}
function hatch(x,y,w,h){g.save();g.beginPath();g.rect(x,y,w,h);g.clip();for(let k=-h;k<w+h;k+=10)line([[x+k,y+h],[x+k+h,y]],{width:.65,color:faint,alpha:.6});g.restore();}
function blueprintState(t){
 const drawn=progress(plan,'draw',t),section=progress(plan,'section',t),ex=progress(plan,'explode',t)*(1-progress(plan,'assemble',t));
 const opened=progress(plan,'open',t)*(1-progress(plan,'close',t)),settle=progress(plan,'settle',t);
 const zoom=1+.14*section-.08*ex+.06*opened-.14*settle;const cx=640+20*opened,cy=370;
 return {drawn,section,ex,opened,settle,zoom,cx,cy,disc:538+82*opened};
}
function blueprint(t){
 const s=blueprintState(t);g.drawImage(paper,0,0);
 // Paper border and title block live in the same world as the machine.
 g.save();g.translate(W/2,H/2);g.scale(s.zoom,s.zoom);g.translate(-s.cx,-s.cy);
 rect(65,55,1150,615,{color:faint,width:1,alpha:.6});line([[85,80],[110,80],[110,62]],{color:faint,width:1});
 text('AXIAL / SPRING CHECK',200,120,15,faint,'left',technical);
 text(plan.title,200,164,32);text('原理示意 · 非工程设计',201,192,13,faint);
 text('FIG. 01',1090,115,18,faint,'right',technical);
 // The centreline anchors the entire film, including the disassembled state.
 line([[230,386],[1080,386]],{color:faint,width:1,dash:[15,6,3,6],alpha:.7,amount:s.drawn});
 const top=282-83*s.ex,bottom=490+60*s.ex;
 if(s.section>0){
  g.save();g.beginPath();g.rect(270,0,810*s.section,H);g.clip();
  // Sectioned shell and wall hatching, not a pretend 3D model.
  g.fillStyle=blue;g.fillRect(300,top,730,38);g.fillRect(300,bottom-38,730,38);
  hatch(300,top,730,38);hatch(300,bottom-38,730,38);
  rect(300,top,730,38,{width:2.3,amount:s.drawn});rect(300,bottom-38,730,38,{width:2.3,amount:s.drawn});
  // Seat leaves one central opening. The closed disc seals exactly that opening.
  g.fillStyle=blue;g.fillRect(524,320,14,24);g.fillRect(524,428,14,24);hatch(524,320,14,24);hatch(524,428,14,24);
  rect(524,320,14,24,{width:2});rect(524,428,14,24,{width:2});
  line([[524,344],[538,344]],{width:2});line([[524,428],[538,428]],{width:2});
  const disc=s.disc;g.fillStyle='#1c507b';g.fillRect(disc,344,13,84);rect(disc,344,13,84,{width:2.8});
  line([[disc+13,386],[934,386]],{width:3});rect(933,367,13,38,{width:2});hatch(933,367,13,38);
  // Spring gets shorter as the valve opens; it stays attached to the moving disc.
  const a=disc+27,b=925;const points=[[disc+13,386],[a,386]];
  for(let i=0;i<=24;i++)points.push([lerp(a,b,i/24),386+(i===0||i===24?0:(i%2?21:-21))]);points.push([933,386]);line(points,{width:2});
  // Particle paths share the disc state: there is no through-flow after reseating.
  const forward=s.opened>.02;
  if(forward){g.save();g.globalAlpha=s.opened*.8;
   for(let lane=-1;lane<=1;lane+=2){line([[310,386],[470,386],[500,386+lane*31],[disc+18,386+lane*48],[700,386+lane*44],[990,386+lane*44]],{color:faint,width:1,alpha:.35});
    for(let j=0;j<7;j++){const u=((t*.26+j/7)%1);const x=310+u*690;let y=386+lane*(x<470?0:x<530?31*(x-470)/60:x<disc+18?lerp(31,48,(x-530)/(disc+18-530)):44);arrow(x,y,13,0,white,.8);}
   }g.restore();
  }else if(s.section>.75&&s.settle<.1){arrow(410,386,80,0,faint);}
  // Live gap measurement uses the same two endpoints as the geometry.
  if(s.opened>.01){line([[538,447],[538,487]],{color:faint,width:.8});line([[disc,440],[disc,487]],{color:faint,width:.8});arrow(538,480,disc-538,0,faint,.7);arrow(disc,480,538-disc,0,faint,.7);text('Δx',lerp(538,disc,.5),504,15,faint,'center',technical);}
  if(s.section>.85){
   leader('阀座',1,370+100*s.ex,247-100*s.ex,529,338);leader('阀瓣',2,615,233-75*s.ex,disc+5,345);leader('弹簧',3,835,244-80*s.ex,lerp(a,b,.65),365);
   g.save();g.globalAlpha*=1-s.ex;text(s.opened>.05?'正向通路打开':'阀瓣贴合阀座',340,534,17,faint);g.restore();
  }
  g.restore();
 }
 // Whole housing masks the section until the physical section sweep arrives.
 if(s.section<1){g.save();g.beginPath();g.rect(270+810*s.section,250,810*(1-s.section),270);g.clip();g.fillStyle='#1a4a73';g.fillRect(300,282,730,208);
  const outline=[[300,328],[343,328],[380,282],[947,282],[989,328],[1030,328],[1030,444],[989,444],[947,490],[380,490],[343,444],[300,444],[300,328]];
  line(outline,{width:2.5,amount:s.drawn});line([[355,306],[960,306]],{width:1,color:faint,amount:s.drawn});line([[355,466],[960,466]],{width:1,color:faint,amount:s.drawn});
  for(const x of [380,947]){line([[x,282],[x,490]],{color:faint,width:1,amount:s.drawn});circle(x,300,5,faint);circle(x,472,5,faint);}g.restore();
 }
 if(s.section>.01&&s.section<.99){const x=270+810*s.section;line([[x,235],[x,512]],{color:white,width:1.1,dash:[4,5]});arrow(x,240,0,25,white);text('A',x+10,246,16,white,'left',technical);}
 const cap=captionAt(plan,t);
 if(cap){const noteX=lerp(365+30*s.ex,720,s.opened);const noteY=lerp(590,577,s.opened);rect(noteX-14,noteY-31,310,47,{color:faint,width:1});text('NOTE',noteX,noteY-9,10,faint,'left',technical);text(cap.text,noteX+45,noteY,18);}
 if(s.settle>.3){g.save();g.globalAlpha=ease((s.settle-.3)/.7);rect(985,562,155,50,{color:red,width:2});text('CLOSED',1062,592,21,'#cf766a','center',technical);g.restore();}
 rect(190,627,910,27,{color:faint,width:.8,alpha:.5});text('VIBE VIDEO   /   原创机制片段',202,645,11,faint,'left',technical);text('SPRING-LOADED  ·  SCHEMATIC ONLY',1088,645,11,faint,'right',technical);
 g.restore();return s;
}
function dataState(t){return {drawn:progress(plan,'draw',t),trace:progress(plan,'trace',t),highlight:progress(plan,'highlight',t),morph:progress(plan,'morph',t),settle:progress(plan,'settle',t)};}
function dataviz(t){
 const s=dataState(t),ink='#24221f',accent='#b93e2f',muted='#807970';g.fillStyle='#f0ece1';g.fillRect(0,0,W,H);
 // Restrained print texture is fixed to paper coordinates, never random per frame.
 const r=rng(plan.seed);for(let i=0;i<1300;i++){g.fillStyle='rgba(75,56,40,.035)';g.fillRect(r()*W,r()*H,.6+r(),.6+r());}
 text('DATA / 001',85,75,14,muted,'left',technical);text('同一组数值',85,141,48,ink);text(plan.data.label,85,178,17,muted);
 const base=590,top=240,x0=205,values=plan.data.values,max=plan.data.maximum,step=868/(values.length-1),maxIndex=values.indexOf(Math.max(...values));
 const coords=values.map((v,i)=>[x0+i*step,base-v/max*(base-top)]);
 for(let tick=0;tick<=4;tick++){const v=max*tick/4,y=base-v/max*(base-top);line([[160,y],[1125,y]],{color:muted,width:.7,alpha:.22});text(String(Number(v.toFixed(2))),143,y+5,14,muted,'right',technical);}
 line([[160,base],[1125,base]],{color:ink,width:1.3});
 for(let i=0;i<values.length;i++){
  const [x,y]=coords[i],arrive=ease((s.drawn-i*(.5/(values.length-1)))/.5),color=i===maxIndex&&s.highlight>.1?accent:ink;
  const yy=lerp(base,y,arrive);const barHeight=(base-yy)*s.morph;
  if(barHeight>0){g.fillStyle=color;g.globalAlpha=.85;g.fillRect(x-18,yy,36,barHeight);g.globalAlpha=1;}
  if(arrive>.05){circle(x,yy,4+3*s.highlight*(i===maxIndex?1:0),color,true);if(arrive>.99)text(String(values[i]),x,yy-18,18,color,'center',technical);}
  text(String(i+1).padStart(2,'0'),x,base+29,15,muted,'center',technical);
 }
 line(coords,{color:ink,width:2.5,amount:s.trace,alpha:1-s.morph});
 if(s.highlight>.1){const [x,y]=coords[maxIndex];g.save();g.globalAlpha=s.highlight;line([[x,y-37],[x,208],[1110,208]],{color:accent,width:1.1});text('MAX / '+values[maxIndex],1110,195,19,accent,'right',technical);g.restore();}
 text((s.morph>.5?'COLUMN':'LINE')+' / '+String(values.length).padStart(2,'0')+' VALUES',1120,76,15,muted,'right',technical);
 if(s.settle>.02){g.save();g.globalAlpha=s.settle;text('换个形状，值不变。',85,666,29,ink);g.restore();}
 return s;
}
window.__film={...plan,width:W,height:H};window.__plan=plan;
window.stateAt=t=>plan.style==='blueprint'?blueprintState(t):dataState(t);
window.renderAt=(t,type='image/png',quality=.95)=>{
 if(!Number.isFinite(t)||t<0||t>plan.duration)throw Error('Out-of-range time');g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;g.clearRect(0,0,W,H);
 if(plan.style==='blueprint')blueprint(t);else dataviz(t);return canvas.toDataURL(type,quality);
};
await document.fonts.ready;window.ready=true;window.renderAt(0);
// Wall time is used only in an optional preview, never by renderAt or stateAt.
if(!new URLSearchParams(location.search).has('render')){const start=performance.now();function play(now){window.renderAt(((now-start)/1000)%plan.duration);requestAnimationFrame(play);}requestAnimationFrame(play);}
