import {layer,clear,fill,line,CAM,W,H,ellipse} from './engine/crayon.js';
import {progress} from './timeline.js';
import {track,hash,clamp,ss,lerp} from './engine/lib.js';
const D=6200, PW=W,PH=H;
const desk={f:layer(),l:layer()},book=layer();
const cam=track([[55,[PW/2,PH/2,0]],[57.8,[0,PH/2,Math.log(.44)]],[60,[0,PH/2,Math.log(.44)]]]);
export function drawBook(comp,t,pages){
 const [cx,cy,lz]=cam(t),z=Math.exp(lz),k=progress(t,55,57);
 CAM.x=cx;CAM.y=cy;CAM.s=z;clear(desk.f);clear(desk.l);clear(book);
 fill(desk.f,[[-2500,-1800],[3500,-1800],[3500,3800],[-2500,3800]],{col:'#c59a63',p:.92,ang:.03,gap:12,w:15,seed:7000,boil:0,over:0});
 for(let i=0;i<38;i++){
  const yy=-1800+i*160,q=[];for(let xx=-2500;xx<3500;xx+=160)q.push([xx,yy+12*Math.sin(xx*.008+i)]);
  line(desk.l,q,{col:i%4===0?'#9e774d':'#b48a56',w:i%4===0?3:1.8,seed:7050+i,boil:0});
 }
 // Wax crayons on the desk, all unlabelled. None occludes the book or takes attention from the turn.
 for(let i=0;i<5;i++){
  const xx=-900+i*380,yy=PH+240+55*Math.sin(i*2),a=.25*Math.sin(i),c=['#7c9f6b','#82b5d3','#e4b962','#c79574','#c2878b'][i];
  const q=[];for(const [u,v] of [[-80,-14],[80,-14],[96,0],[80,14],[-80,14]])q.push([xx+u*Math.cos(a)-v*Math.sin(a),yy+u*Math.sin(a)+v*Math.cos(a)]);
  fill(desk.f,q,{col:c,p:.97,gap:5,w:7,seed:7100+i,boil:0});line(desk.l,[...q,q[0]],{col:'#756653',w:2,seed:7110+i,boil:0});
 }
 const P=(x,y,h=0)=>{const f=D/(D-h);return[(x-cx)*f*z+W/2,(y-cy)*f*z+H/2];};
 const g=book.g;
 if(k>0){
  const [xx,yy]=P(-PW-22,-22),[x2,y2]=P(PW+22,PH+22);
  g.save();g.shadowColor=`rgba(60,42,27,${.28*k})`;g.shadowBlur=24*z;g.shadowOffsetY=35*z;
  g.fillStyle='#68765f';g.fillRect(xx,yy,x2-xx,y2-yy);g.restore();
 }
 function flat(src,side){const N=32;for(let i=0;i<N;i++){
  const u0=PW*i/N,u1=PW*(i+1)/N,lift=k*13*Math.pow(1-Math.min(1,u0/260),2);
  const [xa,ya]=P(side>0?u0:-u1,-lift),[xb,yb]=P(side>0?u1:-u0,PH+lift*.15);
  g.drawImage(src,side>0?u0:PW-u1,0,PW/N,PH,xa,ya,xb-xa+.4,yb-ya);
 }}
 const th=Math.PI*progress(t,58,59.4),turn=th>.00001&&th<Math.PI-.00001,done=th>=Math.PI-.00001;
 flat(done?pages.back:pages.left,-1);flat(turn||done?pages.next:pages.right,1);
 if(turn){
  // Curvature is explicitly per-strip: the outer edge lags behind the spine.
  const N=64;
  const edge=PW*Math.cos(th),[ex,ey]=P(edge,0),[sp,sy]=P(0,0);
  g.save();g.fillStyle=`rgba(46,37,28,${.18*Math.sin(th)})`;const [bottomx,bottomy]=P(edge,PH);g.fillRect(Math.min(ex,sp),Math.min(ey,sy),Math.abs(ex-sp),Math.max(bottomy,ey)-Math.min(ey,sy));g.restore();
  for(let i=0;i<N;i++){
   const u0=PW*i/N,u1=PW*(i+1)/N,ang=u=>th-.5*Math.sin(th)*Math.pow(u/PW,1.6),a0=ang(u0),a1=ang(u1),am=ang((u0+u1)/2);
   const [xa,ya]=P(u0*Math.cos(a0),0,u0*Math.sin(a0)),[,yb]=P(u0*Math.cos(a0),PH,u0*Math.sin(a0));
   const [xc,yc]=P(u1*Math.cos(a1),0,u1*Math.sin(a1));if(Math.abs(xc-xa)<.07)continue;
   const front=Math.cos(am)>0,sw=PW/N,src=front?pages.right:pages.back,col=front?u0:PW-u1;
   g.save();if(front)g.setTransform((xc-xa)/sw,(yc-ya)/sw,0,(yb-ya)/PH,xa,ya);else g.setTransform((xa-xc)/sw,(ya-yc)/sw,0,(yb-ya)/PH,xc,yc);
   g.drawImage(src,col,0,sw,PH,0,0,sw*1.035,PH);g.fillStyle=`rgba(54,41,28,${front?.2*Math.sin(am):.14*Math.abs(Math.cos(am))})`;g.fillRect(0,0,sw*1.035,PH);g.restore();
  }
 }
 const [spine,top]=P(0,0),[,bottom]=P(0,PH),gr=g.createLinearGradient(spine-42*z,0,spine+42*z,0);
 gr.addColorStop(0,'rgba(64,50,31,0)');gr.addColorStop(.5,`rgba(64,50,31,${.27*k})`);gr.addColorStop(1,'rgba(64,50,31,0)');g.fillStyle=gr;g.fillRect(spine-42*z,top,84*z,bottom-top);
 comp.paperCam(cx,cy,z);comp.begin();if(k>0){comp.crayon(desk.f.c);comp.crayon(desk.l.c);}comp.image(book.c);
 comp.finish({vig:.12*k,emb:.15*k,lamp:[.48,.53,.85,.23*k]});
}
