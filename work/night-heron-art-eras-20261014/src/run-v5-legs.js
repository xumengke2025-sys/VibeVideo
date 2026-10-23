// Continuous two-link avian limbs. Stance feet follow exact world distance.
export function drawLegs(ctx,cycle,size,bob,era){
 const colors=[['#48301c','#a4844c'],['#473726','#c9a257'],['#15110d','#bd783c'],['#4d452f','#aa935d'],['#50331e','#a57d41'],['#4e4833','#b39b50'],['#54573d','#a2a174'],['#3b3423','#8e8254'],['#3d3d34','#a0a08c'],['#686d52','#bbb77d'],['#375044','#c2a53c'],['#4f4937','#a89562'],['#242421','#d6d2bb'],['#5d563b','#b6a46b'],['#151717','#f5d632'],['#1c2e24','#a1a04d']];
 const [dark,light]=colors[era-1],pixel=era===16,painted=[1,7,8,9,10,11,14].includes(era);
 const snap=v=>pixel?Math.round(v/3)*3:v;
 const path=(points,width,color)=>{ctx.strokeStyle=color;ctx.lineWidth=width;ctx.lineCap=pixel?'square':'round';ctx.lineJoin='round';ctx.beginPath();points.forEach((p,j)=>{const x=snap(p[0]*size),y=snap(p[1]*size-bob);j?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.stroke()};
 for(const [offset,back] of [[.5,true],[0,false]]){
  const p=(cycle+offset)%1,stance=p<.6,f=stance?0:(p-.6)/.4;
  // C1 swing return, including a raised toe arc; stance does not slide.
  const smooth=f*f*(3-2*f),x=stance?.65-(310/size)*p:(.65-(310/size)*.6)+(310/size)*.6*smooth;
  const y=.84-(stance?0:.125*Math.sin(Math.PI*f)**2);
  const hip=[back?.42:.47,.588],foot=[x,y],a=.17,b=.205,dx=x-hip[0],dy=y-hip[1],dist=Math.min(a+b-.001,Math.hypot(dx,dy)),along=(a*a-b*b+dist*dist)/(2*dist),side=Math.sqrt(Math.max(0,a*a-along*along)),ux=dx/(Math.hypot(dx,dy)||1),uy=dy/(Math.hypot(dx,dy)||1),hock=[hip[0]+ux*along-uy*side,hip[1]+uy*along+ux*side];
  ctx.save();ctx.globalAlpha=back?.92:1;
  path([hip,hock,foot],era===3?8:painted?7:10,painted?light:dark);if(!painted)path([hip,hock,foot],era===3?4.5:6.4,light);
  const tuck=stance?0:Math.sin(Math.PI*f)*.026;
  for(const [tx,ty] of [[.067,.011],[.047,.020],[-.037,.012]]){const toe=[x+tx*(1-tuck*10),y+ty-tuck];path([foot,toe],painted?4.5:6.3,painted?light:dark);if(!painted)path([foot,toe],3.5,light)}
  if(era===4){for(let k=1;k<5;k++){const u=k/5;path([[hock[0]*(1-u)+x*u-.007,hock[1]*(1-u)+y*u],[hock[0]*(1-u)+x*u+.007,hock[1]*(1-u)+y*u]],1.1,dark)}}
  if([1,5,7,8,9,10,11,14].includes(era)){path([[hip[0]+.002,hip[1]],[hock[0]+.002,hock[1]],[x+.002,y]],.9,dark)}
  ctx.restore();
 }
}
