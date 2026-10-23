// Outdoor compositions using the pinned Huashu paint/brush implementation.
// Each layer owns its medium; camera rates express depth, never move the bird.
export function backgrounds(P,U,make,palettes){
 const cache=new Map(),B=1920,{rng}=U,TAU=Math.PI*2;
 const flat=new Set([0,1,2,4,5,11,12,14,15]);
 function path(g,pts,fill,stroke=null,lw=3){g.beginPath();pts.forEach((p,i)=>i?g.lineTo(...p):g.moveTo(...p));g.closePath();if(fill){g.fillStyle=fill;g.fill()}if(stroke){g.strokeStyle=stroke;g.lineWidth=lw;g.stroke()}}
 function ellipse(g,x,y,rx,ry,col){g.fillStyle=col;g.beginPath();g.ellipse(x,y,rx,ry,0,0,TAU);g.fill()}
 function finish(c,i,key){U.setStage(B,B);const out=make(B,B),f=out.getContext('2d');f.drawImage(c,0,0);
  if(i===3)P.mosaic(f,c,{tile:11,grout:'#79735e',seed:79,jitter:.27});
  if(i===9||i===10)P.strokes(f,c,{cell:i===9?9:11,len:i===9?18:31,width:i===9?7:8,angle:(x,y)=>i===9?-.24:Math.sin(x*.004+y*.002)*1.4,seed:19+i,boil:0,outline:i===9?0:.45});
  if(i===11)P.facets(f,c,{nx:18,ny:23,seed:5,shiftAmt:0,edge:'rgba(51,42,28,.2)'});
  if(i===14){f.globalAlpha=.62;P.halftone(f,c,{cell:10,paper:'#fce7b6'});f.globalAlpha=1}
  if(i===15)P.pixelate(f,c,{size:12,palette:['#b8e4f0','#2769a8','#398742','#c6ad72','#183c51','#f3e3a1','#8c613b','#6bad67','#faf1d3','#6596b0']});
  // Restore transparency lost by whole-canvas material processors.
  f.globalCompositeOperation='destination-in';f.drawImage(c,0,0);f.globalCompositeOperation='source-over';
  return out;
 }
 function relief(){const cv=make(480,480),g=cv.getContext('2d'),im=g.createImageData(480,480),h=new Float32Array(481*481);
  for(let y=0;y<=480;y++)for(let x=0;x<=480;x++)h[y*481+x]=P.fbm(x*.0088+3,y*.0088,4)+P.fbm(x*.044,y*.044+7,3)*.16;
  for(let y=0;y<480;y++)for(let x=0;x<480;x++){const j=y*481+x,dx=(h[j+1]-h[j])*52,dy=(h[j+481]-h[j])*52,dot=(dx*.55+dy*.62+.56)/Math.hypot(dx,dy,1),s=U.clamp(.5+(dot-.56)*.9,0,1),k=.72+s*.55,n=P.fbm(x*.0064+11,y*.0064+2,3),a=(y*480+x)*4;const col=P.mix([206,146,90],[110,68,38],U.clamp(.35-n*1.3,0,1));for(let c=0;c<3;c++)im.data[a+c]=col[c]*k;im.data[a+3]=255}g.putImageData(im,0,0);return cv;
 }
 function build(i){if(cache.has(i))return cache.get(i);U.setStage(B,B);const co=palettes[i],r=rng(i+975),far=make(B,B),mid=make(B,B),near=make(B,B),f=far.getContext('2d'),m=mid.getContext('2d'),n=near.getContext('2d');
  f.fillStyle=co[0];f.fillRect(0,0,B,B);
  if(i===0){f.drawImage(relief(),0,0,B,B);f.strokeStyle='rgba(45,24,13,.24)';f.lineWidth=3;for(let k=0;k<13;k++){let x=r()*B,y=r()*B;f.beginPath();f.moveTo(x,y);for(let j=0;j<7;j++){x+=r()*100-30;y+=r()*80;f.lineTo(x,y)}f.stroke()}}
  else if(i===4){const q=f.createRadialGradient(950,800,80,960,900,1400);q.addColorStop(0,'#fff0c9');q.addColorStop(.5,'#e1b572');q.addColorStop(1,'#885127');f.fillStyle=q;f.fillRect(0,0,B,B);f.strokeStyle='rgba(96,59,24,.055)';f.lineWidth=1;for(let k=0;k<B;k+=4){f.beginPath();f.moveTo(k,0);f.lineTo(k,B);f.moveTo(0,k);f.lineTo(B,k);f.stroke()}}
  else if(i===8){f.drawImage(P.texture('v4_xuan','#efe6d0',{scale:.0025,amt:9,grain:7,seed:5}),0,0);f.strokeStyle='rgba(134,116,78,.065)';for(let k=0;k<2600;k++){let x=r()*B,y=r()*B;f.beginPath();f.arc(x,y,3+r()*11,0,r());f.stroke()}}
  else if(!flat.has(i)){const q=f.createLinearGradient(0,0,0,1250);q.addColorStop(0,i===13?'#22407c':i===7?'#30261c':co[0]);q.addColorStop(.55,i===13?'#7898bb':co[0]);q.addColorStop(1,i===13?'#e9dcae':co[1]);f.fillStyle=q;f.fillRect(0,0,B,B)}
  if([1,5,9,10,12,14,15].includes(i)){
   ellipse(f,1420,440,i===14?150:90,i===14?150:90,i===12?'#efe7d2':i===5?'#dbbd6c':i===15?'#f3e3a1':'#f0d387');
   if(i===12){f.strokeStyle='#34332f';f.lineWidth=7;f.stroke()}
  }
  // Closed periodic ridges: matching tile edges prevent camera jumps.
  for(let layer=0;layer<(i===13?0:3);layer++){
   const pts=[[0,B]];for(let x=0;x<=B;x+=i===15?48:16){let y=880+layer*100-(i===8?250:140)*Math.sin(x/B*TAU+layer*.7)-(i===13?45:80)*Math.cos(x/B*TAU*3+layer);if(i===15)y=Math.round(y/24)*24;pts.push([x,y])}pts.push([B,B]);
   f.save();f.globalAlpha=i===8?.10+layer*.08:i===0?.16:.18+layer*.15;path(f,pts,i===2?'#18110c':co[2],i===0?'#42271a':i===5?'#594d36':null);f.restore();
  }
  if(i===13){for(const dx of [-850,100]){f.save();f.translate(dx,0);path(f,[[1170,1130],[1300,890],[1400,850],[1490,740],[1650,720],[1760,780],[1920,750],[1920,1160]],'#d9b271');path(f,[[1460,850],[1530,790],[1650,760],[1760,810]],'#f3d28c');f.strokeStyle='#9c733f';f.lineWidth=3;for(let k=0;k<12;k++){f.beginPath();f.moveTo(1480+k*30,800+r()*80);f.lineTo(1430+k*35,1120);f.stroke()}f.restore()}}
  // Midground water and nearest land share a constant contact line.
  m.fillStyle=i===8?'rgba(101,111,110,.15)':i===2?'#1b140e':co[1];m.fillRect(0,1130,B,300);
  m.save();m.globalAlpha=i===2?.75:.4;m.strokeStyle=i===2?'#cb8247':co[0];m.lineWidth=i===1?4:2;
  for(let k=0;k<80;k++){const x=r()*B,y=1150+r()*180;m.beginPath();if(i===1){for(let j=0;j<9;j++)j?m.lineTo(x+j*12,y+(j%2)*7):m.moveTo(x,y)}else{m.moveTo(x,y);m.lineTo(x+20+r()*160,y)}m.stroke()}m.restore();
  m.fillStyle=i===8?'#d5ccb1':co[3];m.beginPath();m.moveTo(0,1360);m.bezierCurveTo(500,1310,1300,1410,B,1360);m.lineTo(B,B);m.lineTo(0,B);m.closePath();m.fill();
  if(i===5){m.strokeStyle='#bda36b';m.lineWidth=5;m.stroke()}
  if(i===13){m.fillStyle='rgba(49,29,18,.2)';path(m,[[850,1480],[1120,1470],[1720,1790],[1420,1780]],'rgba(49,29,18,.22)')}
  // Separate near-bank scroll supplies ground speed cues at the bird's depth.
  for(let k=0;k<100;k++){const x=r()*B,y=1480+r()*440;n.strokeStyle=i===2?'#20150e':co[2];n.lineWidth=1+r()*3;n.beginPath();n.moveTo(x,y);n.lineTo(x+12+r()*35,y-5-r()*12);n.stroke()}
  const tree=(g,x,y,size)=>{g.save();g.translate(x,y);g.scale(size,size);const col=i===2?'#17110c':co[2];
   g.strokeStyle=col;g.lineWidth=i===12?16:10;g.lineCap='round';g.beginPath();g.moveTo(0,0);g.bezierCurveTo(-40,-160,40,-300,5,-470);g.stroke();
   if(i===8){for(let j=0;j<12;j++){const ax=(j-6)*27;g.strokeStyle='rgba(47,57,46,.6)';g.lineWidth=2;g.beginPath();g.moveTo(4,-450);g.bezierCurveTo(ax,-550,ax-40,-310,ax-45,-190+r()*100);g.stroke();for(let v=0;v<9;v++)P.leaf(g,ax-30,-390+v*20,-.8,25,5,.4)}}
   else if([5,10].includes(i)){for(let j=0;j<12;j++){ellipse(g,0,-100-j*37,55+Math.sin(j)*15,55,col)}}
   else if([3,6,7,9].includes(i)){g.strokeStyle=i===7?'#252419':'#454b34';g.lineWidth=5;
    for(let j=0;j<20;j++){const ax=(r()-.5)*300,ay=-340-r()*230;g.beginPath();g.moveTo(0,-210);g.quadraticCurveTo(ax*.4,ay+90,ax,ay);g.stroke()}
    for(let j=0;j<650;j++){const a=r()*TAU,rad=Math.sqrt(r()),xx=Math.cos(a)*rad*210,yy=-460+Math.sin(a)*rad*160;g.globalAlpha=.4+r()*.55;ellipse(g,xx,yy,5+r()*14,3+r()*8,j%5===0?(i===7?'#a0884d':'#9ba578'):j%3===0?'#5d6d4a':col)}g.globalAlpha=1;
   }else{for(let j=0;j<35;j++)ellipse(g,(r()-.5)*280,-380-r()*200,25+r()*45,30+r()*35,col)}
   if(i===4){g.globalCompositeOperation='destination-out';for(let j=0;j<24;j++)ellipse(g,(r()-.5)*210,-380-r()*160,8,13,'#000')}
   g.restore();};
  if(![0,1,2,13,14,15].includes(i)){tree(f,260,1200,.85);tree(f,1740,1260,1.12)}
  if(i===1){for(let x=160;x<B;x+=440){m.strokeStyle='#3f5d3b';m.lineWidth=8;m.beginPath();m.moveTo(x,1380);m.lineTo(x,850);m.stroke();m.strokeStyle='#32523a';m.lineWidth=3;
   for(let j=-9;j<=9;j++){m.beginPath();m.moveTo(x,860);m.quadraticCurveTo(x+j*9,820-Math.abs(j)*4,x+j*11,787+Math.abs(j)*4);m.stroke()}
   m.strokeStyle='#9a752c';m.lineWidth=4;m.beginPath();m.moveTo(x-105,825);m.quadraticCurveTo(x,740,x+105,825);m.stroke();
  }}
  if(i===5){for(let k=0;k<80;k++){const x=r()*B,y=1450+r()*450;m.strokeStyle='#695b3b';m.lineWidth=2;m.beginPath();m.moveTo(x,y);m.lineTo(x,y-20);m.stroke();for(let j=0;j<5;j++)ellipse(m,x+Math.cos(j*TAU/5)*6,y-23+Math.sin(j*TAU/5)*6,3,4,'#c6a954')}}
  if(i===4){m.strokeStyle='rgba(113,44,19,.5)';m.lineWidth=2;for(let k=0;k<120;k++){let x=r()*B,y=1470+r()*400;m.beginPath();m.arc(x,y,9,0,TAU);m.stroke();m.beginPath();m.arc(x,y,3,0,TAU);m.stroke()}}
  if(i===2){for(let y of [260,1770]){m.strokeStyle='#17110c';m.lineWidth=9;for(let x=0;x<B;x+=96){m.strokeRect(x,y,72,45);m.beginPath();m.moveTo(x+24,y);m.lineTo(x+24,y+23);m.lineTo(x+53,y+23);m.stroke()}}}
  if(i===15){for(let k=0;k<10;k++){const x=k*220;path(f,[[x,610],[x+24,610],[x+24,586],[x+96,586],[x+96,610],[x+144,610],[x+144,634],[x,634]],'#faf1d3')}}
  if(i===12){f.strokeStyle='rgba(45,43,36,.4)';f.lineWidth=5;for(let x=200;x<B;x+=500){f.beginPath();f.arc(x,620,80,Math.PI,0);f.arc(x+100,620,65,Math.PI,0);f.stroke()}}
  if([6,7].includes(i)){for(const layer of [f,m]){layer.globalCompositeOperation='source-atop';layer.globalAlpha=.18;layer.drawImage(P.craquelure('v4_oil_'+i,.3),0,0);layer.globalAlpha=1;layer.globalCompositeOperation='source-over'}}
  // Surface grain sits on painted silhouettes as well as their support.
  if([0,1,2,4,5,12].includes(i)){for(const layer of [f,m,n]){layer.save();layer.globalCompositeOperation='source-atop';layer.drawImage(P.grain('v4_mat_'+i,.12,[45,24,10],i===0?.22:.10),0,0);layer.restore()}}
  const layers=[finish(far,i,'far'),finish(mid,i,'mid'),finish(near,i,'near')];cache.set(i,layers);return layers;
 }
 function draw(g,i,camera,t){const layers=build(i);layers.forEach((cv,k)=>{const rate=[.10,.44,1][k],o=((camera*rate)%B+B)%B;g.drawImage(cv,-o,0);g.drawImage(cv,B-o,0)});
  if(i===12){g.save();g.globalAlpha=.08;g.strokeStyle='#343027';g.lineWidth=1;for(let k=0;k<6;k++){const x=(k*217+Math.floor(t*24)*13)%1080;g.beginPath();g.moveTo(x,0);g.lineTo(x+3,1920);g.stroke()}g.restore()}
 }
 return{draw,build};
}
