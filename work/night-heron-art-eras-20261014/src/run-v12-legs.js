import {footAt,bodyPoint} from './run-v12-gait.mjs';
// Bold tapered avian shanks, visible hocks and splayed toes. Feet remain world-locked.
export function drawLegs(ctx,cycle,size,bob,era,angle=0){
 const palette=[['#442c1b','#cfad64'],['#3f3023','#e2bf65'],['#120f0c','#d9984d'],['#433b28','#c9b270'],['#432c1c','#d5ac57'],['#3d3c2c','#d3bd62'],['#363c2a','#c9c38b'],['#30291d','#b5a063'],['#292c29','#ccc8b2'],['#424a38','#e1d58c'],['#233c31','#ebc94a'],['#393729','#d2bc7d'],['#20201d','#f0ead3'],['#423e2b','#d9c57b'],['#131715','#ffe443'],['#183125','#c9c058']];
 const [dark,light]=palette[era-1],pixel=era===16,snap=v=>pixel?Math.round(v/3)*3:v;
 const pt=p=>[snap(p[0]*size),snap(p[1]*size-bob)];
 function line(points,width,color){ctx.beginPath();points.forEach((p,j)=>j?ctx.lineTo(...pt(p)):ctx.moveTo(...pt(p)));ctx.lineCap=pixel?'square':'round';ctx.lineJoin='round';ctx.strokeStyle=color;ctx.lineWidth=width;ctx.stroke();}
 function segment(a,b,wa,wb,fill){const dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy),nx=-dy/d,ny=dx/d,points=[[a[0]+nx*wa,a[1]+ny*wa],[b[0]+nx*wb,b[1]+ny*wb],[b[0]-nx*wb,b[1]-ny*wb],[a[0]-nx*wa,a[1]-ny*wa]];ctx.beginPath();points.forEach((p,j)=>j?ctx.lineTo(...pt(p)):ctx.moveTo(...pt(p)));ctx.closePath();ctx.fillStyle=fill;ctx.fill();ctx.strokeStyle=dark;ctx.lineWidth=pixel?3:3.6;ctx.lineJoin='round';ctx.stroke();}
 for(const [offset,back]of[[.5,true],[0,false]]){
  const step=footAt(cycle,offset,size),{x,y,stance}=step,hip=bodyPoint([back?.405:.49,.588],bob,angle,size),foot=[x,y],a=.16,b=.18,dx=x-hip[0],dy=y-hip[1],reach=Math.hypot(dx,dy),d=Math.min(a+b-.001,Math.max(Math.abs(a-b)+.0001,reach)),along=(a*a-b*b+d*d)/(2*d),side=Math.sqrt(Math.max(0,a*a-along*along)),ux=dx/(reach||1),uy=dy/(reach||1),hock=[hip[0]+ux*along-uy*side,hip[1]+uy*along+ux*side];
  ctx.save();ctx.globalAlpha=back?.94:1;
  segment(hip,hock,.010,.008,light);segment(hock,foot,.008,.006,light);
  // An organic ankle bulge merges the tapered bones, without a hinge-like ring.
  const joint=pt(hock);ctx.beginPath();ctx.ellipse(...joint,pixel?3.5:4.2,pixel?3.5:4,0,0,Math.PI*2);ctx.fillStyle=light;ctx.fill();
  if(!pixel){ctx.save();ctx.globalAlpha*=.32;for(let k=1;k<5;k++){const u=k/8,cx=hock[0]+(x-hock[0])*u,cy=hock[1]+(y-hock[1])*u;line([[cx-.006,cy],[cx+.006,cy+.002]],1.3,dark);}ctx.restore();}
  const flex=stance?0:Math.sin(Math.PI*(step.f||0)),tuck=flex*.027;
  for(const[tx,ty]of[[.068,.012],[.049,.025],[-.037,.018]]){
   const end=[x+tx*(1-.36*flex),y+ty-tuck],bend=[x+tx*.53,y+ty*.42-tuck*.65];
   line([foot,bend,end],pixel?7:7.5,dark);line([foot,bend,end],pixel?4.5:4.8,light);
   const claw=[end[0]+(tx>0?.012:-.009),end[1]+.005];line([end,claw],3,dark);
  }
  if(!pixel)line([[hock[0]+.004,hock[1]+.01],[x+.004,y-.016]],1.7,'rgba(255,246,199,.40)');
  ctx.restore();
 }
}
