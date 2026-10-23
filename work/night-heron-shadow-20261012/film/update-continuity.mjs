import fs from 'node:fs';import{fileURLToPath}from'node:url';import path from'node:path';
const root=path.dirname(fileURLToPath(import.meta.url)),file=path.join(root,'film.js');let src=fs.readFileSync(file,'utf8');
fs.writeFileSync(path.join(root,'film-reference-v6.js'),src);
src=src.replace(/function background\(t,shot\)\{[^\n]+\}/,`function background(t,shot){ctx.save();ctx.globalCompositeOperation='source-over';ctx.fillStyle='#fff';ctx.fillRect(0,0,1080,1920);ctx.restore();const zoo=ramp(t,8.8,10.2)*(1-ramp(t,35.8,38)),home=ramp(t,39.4,41.2);ctx.save();ctx.globalAlpha=1-zoo;landscape(ctx,home>.01?8:0,t);ctx.restore();ctx.save();ctx.globalAlpha=zoo;landscape(ctx,2,t);ctx.restore();const gateAlpha=ramp(t,3.8,5.2)*(1-ramp(t,9,10.2));if(gateAlpha>0){ctx.save();ctx.globalAlpha=gateAlpha;ctx.translate(mix(340,-300,ramp(t,4,10)),0);gate();ctx.restore()}if(zoo>0){ctx.save();ctx.globalAlpha=zoo;ctx.fillStyle='#659288';ctx.beginPath();ctx.ellipse(815,1510,260,35,0,0,7);ctx.fill();ctx.strokeStyle='#294f4d';ctx.lineWidth=3;for(let j=0;j<3;j++){ctx.beginPath();ctx.ellipse(815+j*20,1518+j*7,150,8,0,0,Math.PI);ctx.stroke()}ctx.fillStyle='#713c1b';ctx.fillRect(931,1080,5,180);placard(ctx,'企鹅',925,1060,30);ctx.restore()}}`);
const marker='ctx.save();ctx.translate(effectiveX,y);';
src=src.replace(marker,`if(opt.gait){const g=opt.gait,f=stepFeet(Math.max(0,Math.min(t,g.stop)-g.start),g.stride,g.period),b=ramp(t,g.start,g.start+.35)*(1-ramp(t,g.stop,g.stop+.4));legs={a:v(mix(-45,f.a.x-f.rootX,b),mix(235,f.a.y-f.bob,b)),b:v(mix(105,f.b.x-f.rootX,b),mix(235,f.b.y-f.bob,b))};bob=f.bob*b}if(opt.screenX!==undefined)effectiveX=opt.screenX;`+marker);
const begin=src.indexOf('function scene(t,shot)'),end=src.indexOf('function draw(t)',begin);
src=src.slice(0,begin)+`function travel(t,start,stop,stride,period){return(stepFeet(Math.max(0,Math.min(t,stop)-start),stride,period).rootX+50)*.38}
function continuousHero(t){let x=280+travel(t,2.5,9.3,18,.85),gait;
if(t>=2.5&&t<9.7)gait={start:2.5,stop:9.3,stride:18,period:.85};
if(t>=17){x=334.72+travel(t,17,24.35,40.33082706766917,1.05);if(t<24.75)gait={start:17,stop:24.35,stride:40.33082706766917,period:1.05}}
if(t>=35.3){x=442-travel(t,35.3,39.7,59.86842105263158,.55);if(t<40.1)gait={start:35.3,stop:39.7,stride:59.86842105263158,period:.55}}
const upright=ramp(t,15.7,16.5)*(1-ramp(t,26.15,27.2));
const glance=ramp(t,12.1,12.5)*(1-ramp(t,13.2,13.6))+ramp(t,24.7,25.05)*(1-ramp(t,25.65,26));
const flip=glance+ramp(t,34.6,35.15)*(1-ramp(t,40.05,40.65));
let neck=-.1*(1-ramp(t,15.3,16.1));neck+=.82*ramp(t,27.25,28.15)*(1-ramp(t,28.65,30.2));neck-=.15*ramp(t,32,32.9)*(1-ramp(t,40,41.5));
neck+=1.02*ramp(t,42,43.35)*(1-ramp(t,44.05,45.05));
const jaw=.33*ramp(t,27.65,28.05)*(1-ramp(t,28.18,28+8/24))+.32*ramp(t,43.55,43.8)*(1-ramp(t,44.1,44.45));
return{screenX:x,x,y:mix(1370,1340,ramp(t,40.75,41.6)),s:mix(.38,.42,ramp(t,40.75,41.6)),neck,jaw,upright,flip,gait,fish:t>=28+8/24&&t<43+16/24,tilt:Math.sin((t-17)*6)*.025*ramp(t,17,18)*(1-ramp(t,24,24.4))}}
function scene(t,shot){const zoo=ramp(t,8.8,10.2)*(1-ramp(t,35.8,38)),home=ramp(t,39.4,41.2),caught=t>=28+8/24;
ctx.save();ctx.globalAlpha=zoo;penguin(800,1500,.72,Math.max(0,t-32.6));penguin(935,1468,.62,Math.max(0,t-33.35));bucket(640,1250,230);if(!caught)drawFish(710,1311,74,-1.07);ctx.restore();
ctx.save();ctx.globalAlpha=home;nest(425,1170,640);chick(678,1410,.34,t,0);chick(830,1385,.29,t,.25);ctx.restore();
const hero=heron(t,continuousHero(t));
ctx.save();ctx.globalAlpha=zoo;bucket(640,1250,230,true);ctx.restore();
ctx.save();ctx.globalAlpha=home;if(t>=43+16/24&&t<44.2){const p=ramp(t,43+16/24,44.15);drawFish(mix(586,622,p),mix(1308,1382,p),82,-1.07+p*.5)}nest(425,1170,640,true);ctx.restore();return hero;}
`+src.slice(end);
fs.writeFileSync(file,src);
let art=fs.readFileSync(path.join(root,'art.js'),'utf8');
art=art.replace("g.fillText('夜 鹭 小 戏 · 彩 皮 影',540,1810);",'');
art=art.replace('dusk=t>41','dusk=Math.max(0,Math.min(1,(t-40)/6))').replace('dusk?.38:.62','.62-.24*dusk');
fs.writeFileSync(path.join(root,'art.js'),art);
console.log('Continuous actor state and scenery transitions applied; narrative captions removed.');
