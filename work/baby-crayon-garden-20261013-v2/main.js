import {makeComp} from './engine/gl.js';
import {layer,clear,CAM,BOIL,W,H,fill,line,ellipse} from './engine/crayon.js';
import {group,clearGroup} from './engine/rig.js';
import {camera,babyState,catState,FULL,progress,DUR,EVENTS} from './timeline.js';
import {drawCat} from './baby.js';
import {drawBaby,loadHeads} from './baby-rig.js';
import {storyTime} from './pacing.js';
await loadHeads();
import {drawWorld,drawStars,drawWash,drawMoon,drawGateFront,crescent} from './world.js';
import {drawBook} from './book.js';
const canvas=document.getElementById('gl'),comp=makeComp(canvas,W,H);
const BG={f:layer(),l:layer()},FR={f:layer(),l:layer()},ST=layer(),WS=layer(),MO=layer(),SH=layer(),BABY=group(),CAT=group();
function snapshot(){const c=document.createElement('canvas');c.width=W;c.height=H;c.getContext('2d').drawImage(canvas,0,0);return c;}
function scene(t,cam=camera(t),clock=t){
 [CAM.x,CAM.y,CAM.s]=cam;BOIL.step=Math.floor(clock*12+1e-6);BOIL.amp=t>50?.46:.7;
 for(const q of [BG.f,BG.l,FR.f,FR.l,ST,WS,MO,SH])clear(q);clearGroup(BABY);clearGroup(CAT);
 drawWorld(BG,t);drawStars(ST,t);drawWash(WS,t);drawMoon(MO,t);drawGateFront(FR);
 const b=babyState(t),cat=catState(t);
 // Small grounded shadows precede character knock-out and support the contact phases.
 fill(SH,ellipse(b.x-5,b.y+1,112,12,32),{col:'#8e8f70',p:.36,gap:4,w:6,seed:8500,boil:0});
 fill(SH,ellipse(cat.x,cat.y+4,86,10,32),{col:'#8e8f70',p:.32,gap:4,w:6,seed:8501,boil:0});
 drawBaby(BABY,{...b,clock});drawCat(CAT,cat);
 const dusk=progress(t,38,42),paper=[.957-.013*dusk,.937-.032*dusk,.890-.012*dusk];
 comp.paperCam(CAM.x*.6,CAM.y*.6,CAM.s/.6);comp.begin(paper);comp.crayon(ST.c);
 comp.crayon(BG.f.c);comp.crayon(BG.l.c);if(t>=42)comp.wash(WS.c,{color:[.17,.23,.43],resist:.91,edge:1.2,gran:.5});
 comp.crayon(SH.c);comp.group(CAT);comp.group(BABY);comp.crayon(FR.f.c);comp.crayon(FR.l.c);comp.crayon(MO.c);
 comp.finish({vig:.095*(1-progress(t,53,55)),emb:.5,lift:.7});
 window.state={t,baby:b,cat,camera:cam};
}
let pages=null;
function makePages(){
 scene(55,FULL);const right=snapshot();
 // Illustrations on both pages are code-drawn and contain no textual glyphs.
 const G=group(),L=layer();[CAM.x,CAM.y,CAM.s]=[0,-135,3];clearGroup(G);clear(L);BOIL.step=0;
 drawBaby(G,{...babyState(0),x:0,y:0,reach:.15});
 line(L,[[-150,45],[150,45]],{col:'#91aa82',w:4,seed:9000,boil:0});
 fill(L,ellipse(65,-390,44,44,36),{col:'#ead179',p:.92,gap:5,w:7,seed:9010,boil:0});
 comp.paperCam(780,970,1);comp.begin();comp.crayon(L.c);comp.group(G);comp.finish({vig:0,emb:.5});const left=snapshot();
 clearGroup(G);clear(L);[CAM.x,CAM.y,CAM.s]=[0,-100,4.2];
 drawCat(G,{x:0,y:40,t:60,curl:1,flip:false});
 const moon=crescent(0,-230,51);
 fill(L,moon,{col:'#e4ce82',p:.94,gap:4,w:6,seed:9100,boil:0});
 for(let j=0;j<5;j++){const a=j*1.256;fill(L,ellipse(-55+Math.cos(a)*10,-67+Math.sin(a)*10,9,7,24),{col:'#dca4a0',p:.91,gap:2,w:3,seed:9120+j,boil:0});}
 line(L,[[-55,-56],[-62,-24]],{col:'#729254',w:2,seed:9130,boil:0});
 comp.paperCam(2500,1500,1);comp.begin();comp.crayon(L.c);comp.group(G);comp.finish({vig:0,emb:.5});const next=snapshot();
 const back=document.createElement('canvas');back.width=W;back.height=H;const g=back.getContext('2d');g.fillStyle='#f3eddf';g.fillRect(0,0,W,H);g.globalAlpha=.065;g.translate(W,0);g.scale(-1,1);g.drawImage(right,0,0);
 pages={right,left,next,back};
}
window.DUR=DUR;window.EV=EVENTS;
window.render=clock=>{const t=storyTime(clock);if(t<55)scene(t,camera(t),clock);else{if(!pages)makePages();BOIL.step=Math.floor(t*12);drawBook(comp,t,pages);}return window.state;};
window.render(0);window.READY=true;
// Optional playback is driven by a single absolute clock, while export exclusively calls render(t).
window.play=()=>{const start=performance.now();let raf;const tick=()=>{const t=(performance.now()-start)/1000;window.render(Math.min(t,DUR));if(t<DUR)raf=requestAnimationFrame(tick);};tick();return()=>cancelAnimationFrame(raf);};
