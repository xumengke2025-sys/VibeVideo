import {line,fill,ellipse,handCircle,smooth,bez,CAM,W,H,sx,sy} from './engine/crayon.js';
import {clamp,hash,mulberry,lerp,ss} from './engine/lib.js';
import {progress,floorY} from './timeline.js';
const INK='#665d52',GREEN='#739253',DARK='#537e49',BROWN='#9f7851';
let F,L;
const visible=(x,y,r=250)=>sx(x)+r*CAM.s>0&&sx(x)-r*CAM.s<W&&sy(y)+r*CAM.s>0&&sy(y)-r*CAM.s<H;
function shape(poly,col,seed,opts={}){fill(F,poly,{col,p:.88,gap:8,w:10,over:3,boil:0,seed,...opts});line(L,[...poly,poly[0]],{col:INK,w:3,seed:seed+2,boil:.35,...opts.line});}
const rect=(x,y,w,h,col,seed,opts={})=>shape([[x,y],[x+w,y],[x+w,y+h],[x,y+h]],col,seed,opts);
const oval=(x,y,rx,ry,col,seed,opts={})=>shape(ellipse(x,y,rx,ry,30),col,seed,opts);
function pot(x,y,s,seed){
 shape([[x-33*s,y-57*s],[x+34*s,y-57*s],[x+23*s,y],[x-22*s,y]],'#cd9270',seed);
 oval(x,y-56*s,35*s,10*s,'#b58565',seed+1);
 for(let i=0;i<6;i++){
  const xx=x+(hash(seed+i)-.5)*95*s,yy=y-(100+hash(seed+i+4)*75)*s;
  line(L,[[x,y-58*s],[xx,yy]],{col:DARK,w:2.5,seed:seed+10+i});
  oval(xx,yy,15*s,8*s,GREEN,seed+20+i,{line:{w:1.4},ang:.3});
  if(i%3===0)flower(xx,yy-8*s,.33*s,seed+35+i,0);
 }
}
function flower(x,y,s,seed,bend){
 const xx=x+bend*17*s,yy=y-160*s;
 line(L,bez([[x,y],[x-10*s,y-70*s],[xx+5*s,yy+45*s],[xx,yy]],18),{col:DARK,w:3.1,seed,boil:.35});
 oval(x-15*s,y-73*s,24*s,9*s,GREEN,seed+1,{ang:-.4,line:{w:1.5}});
 oval(x+18*s,y-105*s,22*s,9*s,GREEN,seed+2,{ang:.8,line:{w:1.5}});
 for(let j=0;j<6;j++){const a=j/6*Math.PI*2;oval(xx+Math.cos(a)*20*s,yy+Math.sin(a)*20*s,16*s,12*s,'#e5a7a2',seed+10+j,{gap:4,w:5,p:.85,line:{w:1.4}});}
 oval(xx,yy,13*s,12*s,'#eaca71',seed+20,{gap:3,w:4,line:{w:1.2}});
}

export function drawWorld(B,t){
 F=B.f;L=B.l;
 // Ground has its own hatching and path. The geometry remains constant throughout the film.
 fill(F,[[-100,1905],[3300,1960],[3300,2450],[-100,2450]],{col:'#c6c59e',p:.5,gap:15,w:16,over:0,ang:.03,seed:700,boil:0});
 if(visible(420,1520,650)){
  // An open-front home lets the character crawl through a real, separately visible doorway.
  shape([[110,1150],[170,958],[630,960],[800,1140]],'#bf7c62',711,{cross:true,crossP:.4});
  rect(130,1140,515,755,'#dfccab',720,{ang:.12});
  shape([[645,1140],[814,1228],[814,1918],[645,1895]],'#eadac2',723);
  rect(220,1250,195,186,'#b2c0bf',731);
  rect(230,1260,175,166,'#e5d9bb',735);
  line(L,[[318,1260],[318,1426]],{col:'#a38c74',w:4,seed:741});line(L,[[231,1341],[405,1341]],{col:'#a38c74',w:4,seed:742});
  shape([[215,1240],[252,1240],[248,1450],[218,1450]],'#d4b98c',748);
  shape([[375,1240],[418,1240],[420,1450],[386,1450]],'#d4b98c',752);
  rect(651,1420,151,490,'#c4b393',760);
  rect(660,1430,134,480,'#f2e3bf',764);
  line(L,[[661,1909],[815,1918]],{col:'#987e65',w:4.5,seed:766});
  // Front door is folded to the side; the opening is not a painted black rectangle.
  shape([[801,1430],[848,1460],[850,1903],[801,1910]],'#b08b65',772);
  for(let i=0;i<4;i++)line(L,[[809+i*9,1440],[809+i*9,1903]],{col:'#8e6b4d',w:2,seed:777+i});
  oval(838,1700,4,5,'#e5bf62',783);
  shape([[220,1870],[570,1883],[630,1984],[190,1970]],'#a9bfa3',789,{ang:.03,gap:7,w:7});
  for(let i=0;i<6;i++)line(L,[[219+i*60,1875],[204+i*69,1971]],{col:'#87a68c',w:2,seed:798+i});
  for(let i=0;i<3;i++){rect(260+i*48,1815-i*7,33,33,['#d4a070','#b8b799','#96b5ba'][i],808+i*4);}
  shape([[554,1875],[797,1897],[710,2014],[536,1962]],'#ecc96d',831,{p:.43,ang:-.05,line:{col:'#d3b46c',w:1.4}});
 }
 if(visible(1190,1500,650)){
  rect(864,1330,680,483,'#eee9d6',900,{ang:.01,gap:11,w:12,p:.94});
  line(L,[[864,1329],[1544,1329]],{col:'#b9b4a3',w:6,seed:911});
  // Metal rail, with modest blunt decorative points in the child-drawn interpretation.
  for(let i=0;i<13;i++){const xx=885+i*52;line(L,[[xx,1110],[xx,1330]],{col:'#969f99',w:3.2,seed:918+i});shape([[xx-8,1110],[xx,1087],[xx+8,1110]],'#a3aaa2',936+i,{line:{w:1.5}});}
  line(L,[[866,1180],[1544,1180]],{col:'#969f99',w:4,seed:953});
  rect(902,1432,240,129,'#d9dac4',961);
  for(let j=0;j<3;j++){const xx=940+j*68;shape(smooth([[xx-23,1450],[xx-10,1490],[xx-23,1538],[xx+23,1538],[xx+10,1490],[xx+23,1450]]),'#748b68',969+j*5,{line:{w:2}});}
  // Peaked wooden storage cabinet from the courtyard photo, with no writing on it.
  shape([[1264,1530],[1390,1430],[1491,1529],[1481,1832],[1264,1832]],'#a98b64',995,{ang:1.5,gap:8,w:9});
  shape([[1252,1530],[1388,1420],[1501,1530],[1488,1545],[1388,1450],[1265,1545]],'#777b70',1004);
  for(let i=0;i<8;i++)line(L,[[1280+i*26,1550],[1280+i*26,1820]],{col:'#897451',w:2,seed:1010+i});
  line(L,[[1381,1533],[1381,1829]],{col:'#807151',w:3,seed:1021});
  oval(1390,1681,4,4,'#d1b779',1025);
  pot(934,1810,.75,1040);pot(1160,1790,.67,1090);pot(1492,1870,.67,1140);
 }
 // The garden starts on the outside of the courtyard gate.
 if(visible(2100,1600,1100)){
  shape([[1785,1950],[2040,1870],[2380,1880],[2680,1967],[3020,2280],[2620,2315],[2270,2110],[1990,2040]],'#a6b779',1200,{ang:.1,gap:10,w:11,p:.7});
  for(let i=0;i<12;i++){
   const xx=1780+i*104,yy=floorY(xx)+4;
   shape([[xx-43,yy-23],[xx+45,yy-26],[xx+56,yy+29],[xx-50,yy+28]],'#d8d6bf',1210+i*4,{gap:7,w:8,ang:.14,line:{col:'#a6a891',w:2.4}});
   line(L,[[xx-25,yy-10],[xx+22,yy-13]],{col:'#efead6',w:2,seed:1265+i});
  }
  // Bamboo fence is behind the path, and remains a recognizable anchor during the sky reveal.
  for(let i=0;i<15;i++){const xx=1870+i*65,top=1550+Math.sin(i*.9)*30;
   shape([[xx-7,top],[xx+6,top+3],[xx+8,1832],[xx-5,1832]],'#baa779',1300+i*4,{gap:3,w:4,line:{w:1.2}});
   line(L,[[xx-6,top+90],[xx+8,top+91]],{col:'#8d8e61',w:2,seed:1370+i});}
  line(L,[[1850,1635],[2850,1635]],{col:'#aa9c72',w:3,seed:1390});
  line(L,[[1850,1770],[2850,1770]],{col:'#aa9c72',w:3,seed:1391});
  for(let i=0;i<48;i++){
   const xx=1830+hash(i*8.1)*1350,yy=1830+hash(i*9.7)*380;
   if(Math.abs(yy-floorY(xx))<60)continue;
   if(!visible(xx,yy,80))continue;
   const sz=15+hash(i+5)*28;
   oval(xx,yy,sz,sz*.56,i%3===0?DARK:GREEN,1400+i*7,{gap:5,w:6,p:.77,line:{col:'#718653',w:1.5}});
   line(L,[[xx,yy+12],[xx-8,yy-22]],{col:'#557b48',w:1.6,seed:1750+i});
  }
  for(let i=0;i<12;i++){const xx=1900+i*110,yy=2110+Math.sin(i*1.7)*74;if(visible(xx,yy,130))flower(xx,yy,.3+(i%3)*.045,1820+i*30,Math.sin(t*.8+i)*.2);}
 }
 drawSun(t);
 // Tree trunk and canopy occlude the descending sun with the same silhouette at every time.
 if(visible(2730,1490,600)){
  shape(smooth([[2690,1960],[2707,1490],[2679,1260],[2660,1150],[2695,1100],[2741,1360],[2770,1660],[2753,1967]]),'#ad885a',2300,{ang:1.45,gap:8,w:9});
  line(L,bez([[2722,1670],[2713,1450],[2634,1290],[2532,1190]],20),{col:BROWN,w:19,seed:2310});
  line(L,bez([[2744,1550],[2780,1370],[2850,1250],[2910,1180]],20),{col:BROWN,w:15,seed:2311});
  for(let i=0;i<7;i++)line(L,[[2709+i*5,1930],[2710+i*4,1570],[2719+i*3,1430]],{col:'#8f754f',w:2,seed:2320+i});
  for(let i=0;i<19;i++){const a=i*2.3999,rad=55+Math.sqrt(i/19)*245;const xx=2720+Math.cos(a)*rad*1.15,yy=1180+Math.sin(a)*rad*.74;
   oval(xx,yy,110,92,i%3===0?'#9aaf67':'#7e9d58',2350+i*5,{p:.82,cross:i%3===0,crossP:.3,gap:9,w:10,line:{col:'#729250',w:2.4}});}
 }
 // Main flower's response is triggered by the baby's fingertip, after the arm reaches it.
 const u=Math.max(0,t-30.1),bend=t<30.1?0:Math.exp(-u*1.9)*Math.sin(u*9);
 if(visible(2382,1820,210))flower(2382,floorY(2382),1,2490,bend);
 for(const [xx,yy] of [[2030,2004],[2650,2040],[2880,1885]]){
  if(!visible(xx,yy,120))continue;
  line(L,[[xx,yy],[xx,yy-78]],{col:'#747d69',w:8,seed:2600+xx});
  shape([[xx-20,yy-67],[xx+20,yy-67],[xx+22,yy-98],[xx-22,yy-98]],progress(t,48.8,49.5)>0?'#e9c681':'#cbc9ac',2610+xx,{p:.95,gap:3,w:4,line:{w:2}});
  shape([[xx-29,yy-98],[xx,yy-122],[xx+28,yy-98]],'#6b796b',2615+xx);
 }
}

function drawSun(t){
 if(t>=41.2)return;
 const x=2530,y=lerp(750,1510,progress(t,38.5,41)),r=88;
 if(!visible(x,y,r+30))return;
 shape(handCircle(x,y,r,2710,0,54),'#e9bf55',2710,{gap:7,w:9,p:.96,line:{col:'#a8965d',w:3}});
 const sleepy=progress(t,37,40);
 for(const a of [-27,27]){
  if(sleepy<.6){oval(x+a,y-2,8,9,'#7a7954',2720+a,{gap:2,w:3,line:{w:1}});}
  else line(L,[[x+a-8,y],[x+a,y+4],[x+a+8,y]],{col:'#7a7954',w:2,seed:2720+a});
 }
 line(L,bez([[x-15,y+29],[x,y+36],[x+10,y+35],[x+20,y+25]],12),{col:'#a78558',w:3,seed:2790});
}

const RNG=mulberry(4242),STARS=[];
for(let i=0;i<180;i++){const x=-90+RNG()*3360,y=-2220+RNG()*3970;if(y>950&&x>100&&x<1800)continue;if(y>1050&&x>2450)continue;STARS.push({x,y,r:5+RNG()*7,seed:3000+i});}
export function drawStars(S,t){
 for(const s of STARS){if(!visible(s.x,s.y,s.r+8))continue;const q=[];for(let i=0;i<10;i++){const a=-Math.PI/2+i*Math.PI/5,rr=i%2?s.r*.45:s.r;q.push([s.x+Math.cos(a)*rr,s.y+Math.sin(a)*rr]);}
  fill(S,q,{col:'#fffdf1',p:.98,gap:2,w:3,over:0,seed:s.seed,boil:0});
 }
}
export const BANDS=[{y0:-2500,y1:1030,t0:42,t1:44.1,dir:1,seed:1},{y0:990,y1:1610,t0:44.3,t1:46.4,dir:-1,seed:2},{y0:1565,y1:2400,t0:46.6,t1:48.7,dir:1,seed:3}];
export function drawWash(LW,t){
 const g=LW.g;g.save();g.setTransform(CAM.s,0,0,CAM.s,W/2-CAM.x*CAM.s,H/2-CAM.y*CAM.s);
 for(const b of BANDS){if(t<b.t0)continue;const p=clamp((t-b.t0)/(b.t1-b.t0)),e=.15*p+.85*ss(p),front=lerp(b.dir>0?-230:3330,b.dir>0?3330:-230,e);
  g.save();g.beginPath();const start=b.dir>0?-270:3370;g.moveTo(start,b.y0-40);
  for(let yy=b.y0-40;yy<=b.y1+40;yy+=35)g.lineTo(front+b.dir*30*Math.sin(clamp((yy-b.y0)/(b.y1-b.y0))*Math.PI)+6*Math.sin(yy*.06),yy);
  g.lineTo(start,b.y1+40);g.closePath();g.clip();
  g.beginPath();for(let xx=-260;xx<=3370;xx+=60){const yy=b.y0+6*Math.sin(xx*.019+b.seed);xx===-260?g.moveTo(xx,yy):g.lineTo(xx,yy);}
  for(let xx=3370;xx>=-260;xx-=60)g.lineTo(xx,b.y1+7*Math.sin(xx*.021+b.seed));g.closePath();g.fillStyle='#000';g.globalAlpha=.93;g.fill();g.clip();
  for(let j=0;j<32;j++){const yy=lerp(b.y0,b.y1,hash(j+b.seed*73));g.beginPath();for(let xx=-260;xx<=3370;xx+=70){const y2=yy+6*Math.sin(xx*.009+j);xx===-260?g.moveTo(xx,y2):g.lineTo(xx,y2);}
   g.lineWidth=3+hash(j+5)*8;g.globalAlpha=.035+hash(j+4)*.045;g.globalCompositeOperation=j%3===0?'destination-out':'source-over';g.strokeStyle='#000';g.stroke();}
  g.restore();
 }g.restore();
}
export function crescent(x,y,r){
 const q=[],a=Math.acos(.3),d=r*.6;
 for(let i=0;i<=40;i++){const b=a+(Math.PI*2-2*a)*i/40;q.push([x+Math.cos(b)*r,y+Math.sin(b)*r]);}
 for(let i=0;i<=30;i++){const b=-Math.PI+a-2*a*i/30;q.push([x+d+Math.cos(b)*r,y+Math.sin(b)*r]);}
 return q;
}
export function drawMoon(M,t){
 const p=progress(t,47.7,49.2);if(p===0)return;
 const q=crescent(2200,820,62);
 fill(M,q,{col:'#f6e1a0',p:.88*p,gap:5,w:7,seed:4100,boil:.3,draw:p});line(M,[...q,q[0]],{col:'#d5c28c',w:2,p,seed:4101,draw:p});
}
export function drawGateFront(B){
 F=B.f;L=B.l;
 if(!visible(1650,1510,550))return;
 rect(1560,1170,45,805,'#e3dfca',4400,{gap:8,w:9,line:{col:'#abae96',w:3}});
 rect(1795,1220,45,758,'#e7e1cd',4405,{gap:8,w:9,line:{col:'#abae96',w:3}});
 // Open leaf recedes to the right, so no cut is needed to conceal the crossing.
 shape([[1836,1280],[1923,1320],[1905,1830],[1836,1850]],'#b8c5b2',4410,{p:.36,gap:14,w:7,line:{col:'#8a9d85',w:3}});
 for(let i=0;i<4;i++){const xx=1843+i*21;line(L,[[xx,1290+(xx-1843)*.46],[xx-3,1836-(xx-1843)*.15]],{col:'#8a9d85',w:3,seed:4420+i});}
 line(L,[[1560,1170],[1840,1220]],{col:'#929f81',w:7,seed:4430});
}
