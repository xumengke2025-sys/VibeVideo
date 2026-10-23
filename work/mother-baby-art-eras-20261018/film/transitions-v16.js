/* Era-specific, deterministic matte transitions. The paintings stay rigid;
   only a spatial reveal moves. No camera shake, scene stretching or flash. */
(()=>{'use strict';
const W=1080,H=1920,MW=540,MH=960,TAU=Math.PI*2;
const make=(w,h)=>Object.assign(document.createElement('canvas'),{width:w,height:h});
const mask=make(MW,MH),matte=mask.getContext('2d'),ink=matte.createImageData(MW,MH);
const reveal=make(W,H),r=reveal.getContext('2d'),rim=make(MW,MH),rc=rim.getContext('2d'),edge=rc.createImageData(MW,MH);
const cache=new Map(),clamp=x=>Math.max(0,Math.min(1,x));
const families=['','ribbon','fan','mosaic','ribbon','fan','mosaic','fan','ink','ink','ink','ribbon','fan','mosaic','fan','ribbon','fan','pixel','ink','fan'];
const names={ribbon:'流金丝带',fan:'纸扇旋开',mosaic:'马赛克接力',ink:'颜料晕开',pixel:'像素阶梯'};
function field(to){
 if(cache.has(to))return cache.get(to);
 const type=families[to],v=new Float32Array(MW*MH),phase=to*.731,dir=to%2?1:-1;
 let lo=Infinity,hi=-Infinity;
 for(let y=0;y<MH;y++)for(let x=0;x<MW;x++){
  const X=x*2+1,Y=y*2+1,dx=(X-540)/1080,dy=(Y-1270)/1080;
  const radius=Math.hypot(dx,dy),angle=Math.atan2(dy,dx);let d;
  if(type==='ink'){
   // One coherent pigment front. Fine edge variation never moves the room.
   d=radius*(1+.060*Math.sin(7*angle+phase)+.026*Math.sin(13*angle-phase))
      +.006*Math.sin(X*.052+Math.sin(Y*.031)*2)*Math.sin(Y*.041);
  }else if(type==='fan'){
   // Six interlocking curved lobes open around the shared interaction area.
   d=radius*(1+.23*Math.cos(6*angle+dir*radius*3+phase));
  }else if(type==='ribbon'){
   d=dir*(X-540)/1080+.13*(Y-960)/1920
     +.13*Math.sin(Y/1920*TAU*.8+phase)+.035*Math.sin(Y/1920*TAU*1.7-phase);
  }else{
   const size=type==='pixel'?48:90,cx=Math.floor(X/size),cy=Math.floor(Y/size);
   const nx=Math.ceil(W/size),ny=Math.ceil(H/size),column=dir>0?cx:nx-1-cx;
   const local=Math.max(Math.abs((X%size)/size-.5),Math.abs((Y%size)/size-.5))*2;
   const jitter=type==='pixel'?((cx*7+cy*3+to)%5)/5:((cy%2)*.26);
   d=(column*.70+cy*.30)/(nx*.70+ny*.30)+local*.055+jitter*.022;
  }
  v[y*MW+x]=d;lo=Math.min(lo,d);hi=Math.max(hi,d);
 }
 const range=hi-lo;for(let n=0;n<v.length;n++)v[n]=(v[n]-lo)/range;
 const result={values:v,type};cache.set(to,result);while(cache.size>3)cache.delete(cache.keys().next().value);return result;
}
function rgb(hex){return [1,3,5].map(i=>parseInt(hex.slice(i,i+2),16));}
function draw(c,a,b,p,to,colors={}){
 c.save();c.resetTransform();c.globalCompositeOperation='source-over';c.globalAlpha=1;c.drawImage(a,0,0);
 if(p<=0){c.restore();return}if(p>=1){c.drawImage(b,0,0);c.restore();return}
 const {values,type}=field(to),feather=type==='pixel'?.0018:type==='mosaic'?.0035:.0055;
 // Finite support gives exact endpoints even where the field reaches 0 or 1.
 const progress=p*(1+2*feather)-feather,accent=rgb(colors.green||'#b78850');
 for(let n=0;n<values.length;n++){
  const z=(progress-values[n])/feather,alpha=clamp(z+.5),j=n*4;
  ink.data[j]=ink.data[j+1]=ink.data[j+2]=255;ink.data[j+3]=Math.round(alpha*255);
  const band=clamp(1-Math.abs(z)*.70),fade=Math.sin(Math.PI*p);
  edge.data[j]=accent[0];edge.data[j+1]=accent[1];edge.data[j+2]=accent[2];edge.data[j+3]=Math.round(band*fade*(type==='ink'?55:100));
 }
 matte.putImageData(ink,0,0);rc.putImageData(edge,0,0);
 r.resetTransform();r.globalCompositeOperation='source-over';r.globalAlpha=1;r.clearRect(0,0,W,H);r.drawImage(b,0,0);
 r.globalCompositeOperation='destination-in';r.imageSmoothingEnabled=true;r.drawImage(mask,0,0,W,H);r.globalCompositeOperation='source-over';
 c.imageSmoothingEnabled=true;c.drawImage(reveal,0,0);c.drawImage(rim,0,0,W,H);c.restore();
}
window.SCENE_TRANSITIONS_V16={draw,duration:2/3,family:to=>families[to],name:to=>names[families[to]],
 description:'Era-specific ink blooms, curved paper fans, flowing ribbons, mosaic relays and pixel staircases; rigid paintings and narrow colored matte edges.'};
})();
