import {line,ellipse,smooth,CAM,sx,sy} from './engine/crayon.js';
import {part,tube,curve} from './engine/rig.js';
import {lerp,clamp,ss} from './engine/lib.js';
const INK='#806451',SKIN='#efbc98',BLUE='#86b9dc',GREEN='#4a9a73',YELLOW='#ecd36d';
const heads={};
export async function loadHeads(){
 await Promise.all(['smile','blink','yawn'].map(async name=>{
  const im=new Image();im.src='./assets/head-'+name+'.png';await im.decode();heads[name]=im;
 }));
}
const mix=(a,b,t)=>a.map((v,i)=>lerp(v,b[i],t));
// Two rigid links. Clamp unreachable targets rather than stretch the child.
export function ik(a,target,l1,l2,bend){
 const dx=target[0]-a[0],dy=target[1]-a[1],raw=Math.hypot(dx,dy)||1;
 const d=Math.max(Math.abs(l1-l2)+.01,Math.min(l1+l2-.01,raw)),ux=dx/raw,uy=dy/raw;
 const along=(l1*l1-l2*l2+d*d)/(2*d),height=Math.sqrt(Math.max(0,l1*l1-along*along));
 return [a,[a[0]+ux*along-uy*height*bend,a[1]+uy*along+ux*height*bend],[a[0]+ux*d,a[1]+uy*d]];
}
export function drawBaby(G,S){
 const {x,y,crawl:c,reach:r,wave:w,t}=S,clock=S.clock??t;
 const distance=x-(t<16?430:1060),active=(t>=5.2&&t<10.2)||(t>=17.5&&t<27);
 const phase=distance/64,bob=active?Math.sin(phase*Math.PI*2)*1.7:0;
 const P=pts=>pts.map(([a,b])=>[x+a,y+b]);
 const sh=(pts,col,seed,width=2.3)=>part(G,P(pts),{col,p:.94,gap:3.5,w:5,over:.5,seed,boil:.38},{col:INK,w:width,seed:seed+1,boil:.3});
 const e=(p,rx,ry,col,s)=>sh(ellipse(...p,rx,ry,28),col,s);
 const seg=(a,b,width,col,s)=>sh(tube([a,b],width,width*.91),col,s);
 function contact(nom,offset,isKnee){
  if(!active)return[nom,isKnee?-11:-6];
  const v=phase+offset,k=Math.floor(v),u=v-k,stance=.72;
  const old=(k-offset)*64+nom+22-distance;
  if(u<stance)return[old,isKnee?-11:-6];
  const q=ss((u-stance)/(1-stance));
  return[old+64*q,(isKnee?-11:-6)-(isKnee?9:19)*Math.sin(Math.PI*q)];
 }
 const hip=mix([-14,-53],[-49,-60+bob],c),shoulder=mix([21,-116],[24,-66+bob],c);
 // Crawl weight passes through palms and knees. Feet follow folded shins.
 function leg(far){
  const h=[hip[0]+(far?-11:11),hip[1]+5],cn=contact(far?-51:-34,far?0:.5,true);
  const knee=mix(far?[-50,-31]:[29,-29],cn,c);
  // Fixed thigh length; knee follows an arc constrained about the hip.
  const dx=knee[0]-h[0],dy=knee[1]-h[1],len=Math.hypot(dx,dy)||1;
  const k=[h[0]+dx/len*50,h[1]+dy/len*50];
  const foot=mix(far?[-74,-9]:[61,-9],[k[0]-34,k[1]-1],c);
  const fd=Math.hypot(foot[0]-k[0],foot[1]-k[1])||1;
  const f=[k[0]+(foot[0]-k[0])/fd*34,k[1]+(foot[1]-k[1])/fd*34];
  sh(tube(curve([h,k,f],10),30,23),SKIN,far?101:151);
  const short=mix(h,k,.56);seg(h,short,34,BLUE,far?105:155);
  e([f[0]+(c>.5?-6:5),f[1]],18,11,'#f8efe1',far?106:156);
  e([f[0]+(c>.5?-16:15),f[1]+1],8,8,YELLOW,far?107:157);
 }
 function arm(far){
  const a=[shoulder[0]+(far?-17:3),shoulder[1]+(far?-4:2)];
  let rest=far?[-32,-61]:[45,-51];
  const goal=[96,-149];
  if(!far)rest=mix(rest,goal,r);
  if(!far&&w>0)rest=mix(rest,[55+5*Math.sin(clock*8),-180+4*Math.sin(clock*8)],w);
  const target=mix(rest,contact(far?48:69,far?.5:0,false),c);
  const links=ik(a,target,43,43,far?1:-1);
  sh(tube(curve(links,10),25,22),SKIN,far?111:162);
  e([links[2][0]+4,links[2][1]],15,10,SKIN,far?114:166);
  if(!far)for(let j=0;j<3;j++)line(G.l,P([[links[2][0]+5+j*3,links[2][1]-4],[links[2][0]+6+j*3,links[2][1]]]),{col:'#bd8c72',w:1,seed:170+j});
  return links;
 }
 leg(true);arm(true);
 const torso=smooth([mix([-43,-131],[-80,-94],c),mix([23,-139],[8,-103],c),mix([44,-106],[47,-84],c),mix([36,-57],[19,-39],c),mix([-5,-44],[-55,-33],c),mix([-43,-66],[-82,-61],c)]);
 sh(torso,BLUE,130,2.9);
 leg(false);arm(false);
 e([shoulder[0]-18,shoulder[1]-3],19,19,GREEN,137);
 e([shoulder[0]+3,shoulder[1]-5],19,19,YELLOW,140);
 line(G.l,P([mix([0,-133],[20,-92],c),mix([2,-76],[-11,-45],c)]),{col:'#609cc2',w:1.8,seed:178});
 for(let j=0;j<2;j++)e(mix([3,-118+j*18],[14-j*8,-81+j*17],c),2.6,2.6,'#d7e5ec',180+j);
 // Pale collar and short neck tie the raster head to the body.
 const hx=lerp(0,66,c),hy=lerp(-204,-130+bob,c);
 e([hx-5,hy+57],15,14,SKIN,191);
 sh(smooth([mix([-26,-142],[10,-106],c),mix([-1,-130],[24,-94],c),mix([24,-143],[43,-109],c),mix([14,-126],[32,-92],c),mix([-10,-121],[17,-88],c)]),'#d9ebeb',193,1.6);
 const blink=clock%3.4,blinkMix=blink>2.72&&blink<2.92?Math.sin((blink-2.72)/.2*Math.PI):0;
 const sleepy=clamp(S.sleep);
 const closed=Math.max(blinkMix,sleepy*.85);
 const angle=(-.055*r-.065*S.look+.03*Math.sin(clock*2)*Math.max(r,w))+.02*active*Math.sin(phase*Math.PI*2);
 // All variants share original canvas coordinates. No face geometry is regenerated.
 const size=174;
 function stamp(L,im,alpha=1,mode='source-over'){
  const g=L.g;g.save();g.globalCompositeOperation=mode;g.globalAlpha=alpha;
  g.translate(sx(x+hx),sy(y+hy));g.rotate(angle);g.drawImage(im,-size*CAM.s/2,-size*CAM.s/2,size*CAM.s,size*CAM.s);g.restore();
 }
 stamp(G.f,heads.smile,1,'destination-out');stamp(G.l,heads.smile,1,'destination-out');stamp(G.k,heads.smile);
 stamp(G.f,heads.smile);if(closed>.001)stamp(G.f,heads.blink,closed);if(S.yawn>.001)stamp(G.f,heads.yawn,S.yawn);
}
