// Sixteen generated historical plates. A bounded pan avoids repeating landmarks.
export async function generatedBackgrounds(make){
 const selected=new URLSearchParams(location.search).get('pilot')?.split(',').map(Number);
 const images=await Promise.all(Array.from({length:16},async(_,i)=>{if(selected&&!selected.includes(i+1))return null;const im=new Image();im.src=`assets/run-v5/background-${String(i+1).padStart(2,'0')}.png`;await im.decode();const c=make(1080,1920),g=c.getContext('2d');g.filter=[0,6,7,8,13].includes(i)?'contrast(0.87) saturate(0.90)':'contrast(0.94)';g.drawImage(im,0,0,1080,1920);g.filter='none';const source=make(1080,1920);source.getContext('2d').drawImage(c,0,0);U.setStage(1080,1920);
 if(i===3)PAINT.mosaic(g,source,{tile:14,grout:'#79735e',seed:79,jitter:.27});
 if(i===9||i===10){PAINT.strokes(g,source,{cell:17,len:i===9?25:36,width:11,angle:(x,y)=>i===9?-.24:Math.sin(x*.004+y*.002)*1.4,seed:19+i,boil:0});g.globalAlpha=.82;g.drawImage(source,0,0);g.globalAlpha=1}
 if(i===14){g.globalAlpha=.35;PAINT.halftone(g,source,{cell:12,paper:'#fce7b6'});g.globalAlpha=1}
 if(i===15)PAINT.pixelate(g,source,{size:10,palette:['#b8e4f0','#2769a8','#398742','#c6ad72','#183c51','#f3e3a1','#8c613b','#6bad67','#faf1d3','#6596b0','#222923','#e1c87b','#335e36','#b75838','#f5f2d1','#80925d']});
 const bank=make(1080,1920),z=bank.getContext('2d');z.drawImage(c,0,0);const lift=i===13?420:i===2?45:0,top=-1920*.12*.65-lift,hh=1920*1.12+lift;
 const mask=z.createLinearGradient(0,0,0,1920);mask.addColorStop(0,'transparent');mask.addColorStop((1200-top)/hh,'transparent');mask.addColorStop((1290-top)/hh,'#fff');mask.addColorStop(1,'#fff');z.globalCompositeOperation='destination-in';z.fillStyle=mask;z.fillRect(0,0,1080,1920);
 return {plate:c,bank}}));
 return {draw(g,i,camera,t,progress,anchorCamera){const pair=images[i];if(!pair)throw Error('Missing background for era '+(i+1));const im=pair.plate,zoom=1.12,w=1080*zoom,h=1920*zoom;
  g.save();g.translate(0,110);g.imageSmoothingEnabled=i!==15;
  const bankLift=[0,0,45,0,0,0,0,0,0,0,0,0,0,420,0,0][i];
  // The distant landscape keeps a restrained pan; the animal's near bank
  // has full camera parallax. Sky landmarks are never reflected or repeated.
  g.drawImage(im,-(w-1080)*(.12+.76*progress),-(h-1920)*.65-bankLift,w,h+bankLift);
  // Scenic plate, bank, fish and planted feet share one camera transform.
  // Reflection extends the original plate seamlessly beyond the finite canvas.
  const shift=-(w-1080)*.5-(camera-anchorCamera),first=Math.floor(-shift/w)-1;
  for(let k=first;k<=first+3;k++){const x=shift+k*w;g.save();if(Math.abs(k)%2){g.translate(x+w,0);g.scale(-1,1);g.drawImage(pair.bank,0,-(h-1920)*.65-bankLift,w,h+bankLift)}else g.drawImage(pair.bank,x,-(h-1920)*.65-bankLift,w,h+bankLift);g.restore()}
  g.restore();return {cameraX:camera,anchorCamera,shift,tileWidth:w};
 }};
}
