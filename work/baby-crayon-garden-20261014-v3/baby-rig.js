import {line,ellipse,smooth,CAM,sx,sy} from './engine/crayon.js';
import {part,tube,curve} from './engine/rig.js';
import {lerp,clamp,ss} from './engine/lib.js';
const INK='#74503b',SKIN='#f4bb88',BLUE='#86b9dc',GREEN='#4a9a73',YELLOW='#ecd36d';
const heads={};
let headBuffer;
export async function loadHeads(){
 await Promise.all(['front','quarter','profile','yawn'].map(async name=>{
  const im=new Image();im.src='./assets/head-'+name+'.png';await im.decode();heads[name]=im;
 }));
 headBuffer=document.createElement('canvas');headBuffer.width=512;headBuffer.height=512;
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
 const hip=mix([-8,-53],[-49,-60+bob],c);
 // Independent left/right shoulders for seated view; front/back shoulders for crawl.
 const shoulder=far=>mix(far?[-34,-115]:[34,-115],far?[10,-69+bob]:[29,-64+bob],c);
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
  const a=shoulder(far);
  let rest=far?[-47,-43]:[47,-43];
  if(!far)rest=mix(rest,[99,-146],r);
  if(!far&&w>0)rest=mix(rest,[68+4*Math.sin(clock*7),-174+4*Math.sin(clock*7)],w);
  // Hold a supporting hand until the torso has transferred weight into sitting.
  const support=ss(clamp((c-.18)/.68));
  const target=mix(rest,contact(far?49:70,far?.5:0,false),support);
  const links=ik(a,target,40,42,far?1:-1);
  sh(tube(curve(links,10),24,20),SKIN,far?111:162);
  const wrist=links[2],fore=[wrist[0]-links[1][0],wrist[1]-links[1][1]];
  // Fingers follow the forearm; crawling palms rest flat and point along travel.
  let ang=Math.atan2(fore[1],fore[0]);
  ang=lerp(ang,0,support);
  const hand=pts=>pts.map(([u,v])=>[wrist[0]+u*Math.cos(ang)-v*Math.sin(ang),wrist[1]+u*Math.sin(ang)+v*Math.cos(ang)]);
  const palm=smooth([[-5,-8],[6,-9],[13,-6],[17,-2],[17,3],[12,7],[4,8],[-5,6]],5);
  sh(hand(palm),SKIN,far?114:166,1.9);
  // One thumb lobe and two short finger divisions, no cylindrical fist or nails.
  sh(hand(smooth([[-1,-6],[3,-12],[8,-13],[10,-9],[7,-4]],4)),SKIN,far?116:168,1.6);
  if(!far)for(let j=0;j<2;j++)line(G.l,P(hand([[10+j*3,-3],[10+j*3,2]])),{col:'#a57752',w:1.1,seed:170+j,boil:.25});
  return links;
 }
 leg(true);
 const farArm=arm(true);
 const torso=smooth([mix([-39,-134],[-80,-94],c),mix([39,-134],[8,-103],c),mix([44,-102],[47,-84],c),mix([35,-57],[19,-39],c),mix([0,-44],[-55,-33],c),mix([-35,-57],[-82,-61],c)]);
 sh(torso,BLUE,130,2.9);
 // Sleeve capsules emerge from their own shoulders and follow each upper arm.
 seg(farArm[0],mix(farArm[0],farArm[1],.42),29,GREEN,137);
 leg(false);const nearArm=arm(false);
 seg(nearArm[0],mix(nearArm[0],nearArm[1],.42),29,YELLOW,140);
 line(G.l,P([mix([0,-130],[20,-92],c),mix([2,-76],[-11,-45],c)]),{col:'#609cc2',w:1.8,seed:178});
 for(let j=0;j<2;j++)e(mix([3,-118+j*18],[14-j*8,-81+j*17],c),2.6,2.6,'#d7e5ec',180+j);
 // Pale collar and short neck tie the raster head to the body.
 const hx=lerp(0,61,c),hy=lerp(-202,-134+bob,c);
 e([hx-5,hy+57],15,14,SKIN,191);
 sh(smooth([mix([-26,-142],[10,-106],c),mix([-1,-130],[24,-94],c),mix([24,-143],[43,-109],c),mix([14,-126],[32,-92],c),mix([-10,-121],[17,-88],c)]),'#d9ebeb',193,1.6);
 // Turn toward the intended action BEFORE leaving the seated pose. During sit-up
 // retain direction until the shoulders are upright, then return to front.
 const backToFront=ss(clamp((t-49.2)/1.15));
 const turning=Math.max(ss(clamp(c/.38)),r*.62,S.look*.74,w*.62)*(1-backToFront);
 const orient=turning*2;
 const toQuarter=ss(clamp((orient-.72)/.3)),toProfile=ss(clamp((orient-1.72)/.28));
 const weights=[1-toQuarter,toQuarter*(1-toProfile),toProfile];
 const angle=(-.025*r-.19*S.look*(1-backToFront)+.02*Math.sin(clock*2)*w)+.012*active*Math.sin(phase*Math.PI*2)+.055*S.sleep;
 const size=174,HL={g:headBuffer.getContext('2d')};
 HL.g.clearRect(0,0,512,512);
 // Premultiplied additive mixture keeps opacity stable across direction changes.
 HL.g.globalCompositeOperation='lighter';
 ['front','quarter','profile'].forEach((name,i)=>{if(weights[i]>.001){HL.g.globalAlpha=weights[i]*(1-S.yawn);HL.g.drawImage(heads[name],0,0,512,512);}});
 if(S.yawn>.001){HL.g.globalAlpha=S.yawn;HL.g.drawImage(heads.yawn,0,0,512,512);}
 function stamp(L,im,alpha=1,mode='source-over'){
  const g=L.g;g.save();g.globalCompositeOperation=mode;g.globalAlpha=alpha;
  g.translate(sx(x+hx),sy(y+hy));g.rotate(angle);g.drawImage(im,-size*CAM.s/2,-size*CAM.s/2,size*CAM.s,size*CAM.s);g.restore();
 }
 stamp(G.f,HL.g.canvas,1,'destination-out');stamp(G.l,HL.g.canvas,1,'destination-out');stamp(G.k,HL.g.canvas);
 stamp(G.f,HL.g.canvas);
}
