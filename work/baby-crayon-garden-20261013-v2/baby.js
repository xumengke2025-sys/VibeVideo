import {line,fill,ellipse,smooth,bez,xf,CAM} from './engine/crayon.js';
import {part,tube,curve} from './engine/rig.js';
import {lerp,clamp,ss,hash} from './engine/lib.js';
import {babyX,floorY} from './timeline.js';
const INK='#3c3447',SKIN='#f2bd95',HAIR='#544130',BLUE='#82b5d3',GREEN='#6b9d6d',YELLOW='#ecc661';
// Every body part has a stable seed and erases the previously drawn parts beneath it.
export function drawBaby(G,S){
 const {x,y,t,crawl:c}=S; const P=pts=>pts.map(([a,b])=>[x+a,y+b]);
 const shape=(pts,col,seed,w=3.4)=>part(G,P(pts),{col,p:.91,gap:3.7,w:5,over:.8,seed,boil:.65},{col:INK,w,seed:seed+1,boil:.55});
 const E=(cx,cy,rx,ry,col,seed,w=3.4)=>shape(ellipse(cx,cy,rx,ry,30),col,seed,w);
 const limb=(pts,col,width,seed)=>shape(tube(curve(pts),width,width*.83),col,seed);
 const gait=(t>5.15&&t<10.2)||(t>17.45&&t<27);
 const start=t<16?5.2:17.5;
 function contact(nom,offset,isHand){
  if(!gait)return[nom,-3];
  const cycle=.58,phase=(t-start)/cycle+offset,k=Math.floor(phase),u=phase-k;
  const td=start+(k-offset)*cycle,next=td+cycle,stance=.68;
  const old=babyX(td)+nom,ne=babyX(next)+nom;
  if(u<stance)return[old-x,-3];
  const q=ss((u-stance)/(1-stance));
  return[lerp(old,ne,q)-x,-3-(isHand?23:15)*Math.sin(Math.PI*q)];
 }
 const hn=contact(99,0,true),hf=contact(72,.5,true),kn=contact(-38,.5,false),kf=contact(-60,0,false);
 const bob=gait?2*Math.sin((t-start)/.78*Math.PI*2):0;
 const shoulder=[lerp(31,41,c),lerp(-124,-91+bob,c)],hip=[lerp(-15,-48,c),lerp(-76,-86+bob,c)];
 // Far legs and arm, then garment, then near limbs, then head.
 limb([[hip[0]-16,hip[1]+7],[lerp(-51,kf[0],c),lerp(-41,kf[1]-10,c)],[lerp(-65,kf[0]-32,c),lerp(-9,kf[1]-5,c)]],BLUE,31,101);
 E(lerp(-71,kf[0]-43,c),lerp(-7,kf[1]+2,c),24,12,'#f7eee0',105,2.8);
 limb([[shoulder[0]-21,shoulder[1]-1],[lerp(-32,57,c),lerp(-90,-53,c)],[lerp(-36,hf[0],c),lerp(-55,hf[1],c)]],SKIN,24,111);
 E(lerp(-36,hf[0]+6,c),lerp(-52,hf[1],c),17,11,SKIN,115,2.6);
 const torso=smooth([[lerp(-45,-74,c),lerp(-139,-112,c)], [lerp(30,10,c),lerp(-152,-120,c)],
 [lerp(49,51,c),lerp(-116,-99,c)], [lerp(45,24,c),lerp(-61,-59,c)],
 [lerp(1,-51,c),lerp(-53,-60,c)],[lerp(-44,-81,c),lerp(-79,-80,c)]]);
 shape(torso,BLUE,130,4);
 // The photo's green/yellow sleeves and pale collar are identity cues, not a pasted photograph.
 E(shoulder[0]-18,shoulder[1]-4,25,23,GREEN,137,2.8);
 E(shoulder[0]+1,shoulder[1]-7,23,23,YELLOW,140,2.8);
 limb([[hip[0]+13,hip[1]+10],[lerp(32,kn[0],c),lerp(-39,kn[1]-10,c)],[lerp(68,kn[0]-30,c),lerp(-7,kn[1]-5,c)]],BLUE,37,151);
 E(lerp(73,kn[0]-42,c),lerp(-5,kn[1]+2,c),25,13,'#f8eedc',155,2.8);
 // Near hand is anchored to support during crawl; otherwise it reaches or waves.
 const q=S.reach,wv=S.wave;
 let hand=[lerp(46,141,q),lerp(-51,-155,q)];
 if(wv>0){const swing=Math.sin(t*8);hand=[lerp(hand[0],81+9*swing,wv),lerp(hand[1],-237+8*swing,wv)];}
 hand=[lerp(hand[0],hn[0],c),lerp(hand[1],hn[1],c)];
 const elbow=[lerp(60,63,c),lerp(lerp(-92,-161,q),-46,c)];
 limb([shoulder,elbow,hand],SKIN,27,162);
 E(hand[0]+6,hand[1],18,12,SKIN,166,2.8);
 for(let i=0;i<3;i++)line(G.l,P([[hand[0]+7+i*3,hand[1]-6],[hand[0]+8+i*3,hand[1]-1]]),{col:'#b48269',w:1.2,seed:170+i,boil:.25});
 // Garment placket and buttons.
 line(G.l,P([[lerp(2,14,c),lerp(-145,-116,c)],[lerp(5,-9,c),lerp(-80,-70,c)]]),{col:'#6596b7',w:2,seed:178});
 for(let i=0;i<2;i++)E(lerp(5,8-i*5,c),lerp(-126+i*22,-101+i*15,c),3,3,'#cee1e9',180+i,1);
 const hx=lerp(0,83,c),hy=lerp(-218,-158+bob,c);
 E(hx+4,hy+58,22,20,SKIN,191,3);
 E(hx-59,hy+6,13,20,SKIN,195,2.4);E(hx+61,hy+8,12,19,SKIN,199,2.4);
 const head=smooth([[hx-47,hy-47],[hx-11,hy-65],[hx+32,hy-59],[hx+61,hy-27],
 [hx+66,hy+17],[hx+49,hy+55],[hx+6,hy+70],[hx-41,hy+55],[hx-65,hy+16],[hx-63,hy-19]]);
 shape(head,SKIN,210,4);
 // Short spiky crown: outer silhouette only; no horizontal headband outline.
 const hair=smooth([[hx-61,hy-23],[hx-63,hy-48],[hx-36,hy-70],[hx-4,hy-77],[hx+32,hy-68],
 [hx+55,hy-51],[hx+62,hy-22],[hx+43,hy-34],[hx+15,hy-45],[hx-16,hy-45],[hx-41,hy-35]],5);
 shape(hair,HAIR,222,2.9);
 for(let i=0;i<19;i++){const a=Math.PI*1.13+i/18*Math.PI*.78; const xx=hx+Math.cos(a)*64,yy=hy+Math.sin(a)*70;
  line(G.l,P([[xx,yy+4],[xx+Math.cos(a)*7,yy-8-hash(i)*5]]),{col:HAIR,w:1.8,seed:250+i,boil:.3});}
 // Eyes are narrow almond shapes, with a lower iris and soft eyelid, matching the references.
 const glance=S.look,blink=Math.pow(Math.max(0,Math.cos(t*1.87+1.2)),28),closed=Math.max(blink,S.sleep*.48,S.yawn*.45);
 const eyeY=hy+5-6*glance;
 function eye(ex,seed){
  const h=6.4*(1-closed)+.8;
  const poly=bez([[ex-16,eyeY],[ex-8,eyeY-h*1.5],[ex+7,eyeY-h*1.5],[ex+17,eyeY+1],
   [ex+7,eyeY+h],[ex-8,eyeY+h],[ex-16,eyeY]],10);
  shape(poly,'#faf5e7',seed,2.5);
  E(ex+3+3*glance,eyeY-h*.07,6.9,Math.max(.5,h*.78),INK,seed+4,1.3);
  if(closed<.5)E(ex+5,eyeY-2,1.9,1.4,'#fffdf2',seed+8,.5);
  line(G.l,P(bez([[ex-16,eyeY],[ex-6,eyeY-h*1.6],[ex+8,eyeY-h*1.5],[ex+17,eyeY+1]],12)),{col:INK,w:2.8,seed:seed+12});
  line(G.l,P(bez([[ex-15,eyeY-17],[ex-5,eyeY-22],[ex+5,eyeY-22],[ex+12,eyeY-18]],10)),{col:'#947153',w:2,seed:seed+14,boil:.25});
 }
 eye(hx-27,280);eye(hx+28,304);
 fill(G.f,P(ellipse(hx-40,hy+31,16,9,24)),{col:'#e79d8e',p:.43,gap:3,w:4,seed:330,boil:.3});
 fill(G.f,P(ellipse(hx+44,hy+32,14,8,24)),{col:'#e79d8e',p:.43,gap:3,w:4,seed:332,boil:.3});
 line(G.l,P(bez([[hx+1,hy+17],[hx-4,hy+26],[hx+6,hy+27],[hx+9,hy+24]],12)),{col:'#bb8d70',w:2.1,seed:340});
 const mouthOpen=Math.max(S.yawn,S.smile*.35*(1-c));
 if(mouthOpen>.07){E(hx+4,hy+46,9+5*mouthOpen,3+12*mouthOpen,'#954f49',350,2.3);E(hx+5,hy+50+5*mouthOpen,6,2.5,'#e29b91',354,1.1);}
 else line(G.l,P(bez([[hx-7,hy+45],[hx+1,hy+51],[hx+10,hy+49],[hx+14,hy+43]],12)),{col:'#9e6058',w:2.5,seed:358});
}

export function drawCat(G,S){
 const {x,y,t,curl}=S,sg=S.flip?-1:1;
 const P=pts=>pts.map(([a,b])=>[x+a*sg,y+b]);
 const sh=(pts,col,seed,w=2.8)=>part(G,P(pts),{col,p:.94,gap:3.5,w:4.6,seed,over:.9,boil:.55},{col:INK,w,seed:seed+1,boil:.4});
 const e=(a,b,rx,ry,col,s)=>sh(ellipse(a,b,rx,ry,30),col,s);
 const orange='#d99a54',cream='#f3dfb3';
 const moving=t>12&&t<13.1||t>14.2&&t<27;
 const phase=t*8;
 if(curl<.99){
  const tail=bez([[-59,-60],[-102,-78],[-103,-122],[-79,-143],[-65,-156],[-59,-131],[-68,-119]],14);
  sh(tube(tail,12,9),orange,500);
  for(const [i,a] of [[0,-40],[1,43]]){
   const d=moving?Math.sin(phase+i*Math.PI)*14:0;
   sh(tube([[a,-45],[a+d,-20],[a+d+7,0]],14,12),orange,510+i*4);
  }
 }
 e(lerp(-7,-5,curl),lerp(-56,-32,curl),lerp(64,68,curl),lerp(34,35,curl),orange,531);
 for(let i=0;i<4;i++)line(G.l,P([[lerp(-45+i*23,-42+i*21,curl),lerp(-78,-54,curl)],[lerp(-39+i*23,-37+i*21,curl),lerp(-62,-38,curl)]]),{col:'#a77748',w:4,seed:540+i});
 const hx=lerp(53,30,curl),hy=lerp(-82,-30,curl);
 sh([[hx-27,hy-15],[hx-31,hy-46],[hx-10,hy-32],[hx+8,hy-32],[hx+27,hy-45],[hx+30,hy-8]],orange,552);
 e(hx,hy,34,30,orange,560);
 e(hx+7,hy+11,17,12,cream,564);
 for(const z of [-10,12]){
  if(curl>.3)line(G.l,P([[hx+z-5,hy],[hx+z,hy+3],[hx+z+5,hy]]),{col:INK,w:2,seed:570+z});
  else {e(hx+z,hy-3,5,6,'#677147',570+z);line(G.l,P([[hx+z,hy-7],[hx+z,hy+1]]),{col:INK,w:2,seed:573+z});}
 }
 sh([[hx+2,hy+6],[hx+11,hy+6],[hx+7,hy+12]],'#b77769',592,1.5);
 for(let k=0;k<2;k++){line(G.l,P([[hx-11,hy+12+k*5],[hx-43,hy+7+k*12]]),{col:'#82704d',w:1.3,seed:601+k});line(G.l,P([[hx+19,hy+12+k*5],[hx+46,hy+5+k*13]]),{col:'#82704d',w:1.3,seed:605+k});}
 if(curl>0)sh(tube(bez([[-49,-36],[-75,-10],[-12,10],[31,-5]],20),13,9),'#c0884c',612);
}
