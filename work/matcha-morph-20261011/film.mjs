const canvas=document.querySelector('#film'),ctx=canvas.getContext('2d',{willReadFrequently:true});
const W=540,H=960,N=240,TAU=Math.PI*2;
const C={cream:'#F4F0E4',forest:'#153F30',dark:'#0D2D24',green:'#82AE43',light:'#C9D8A4',gold:'#C5AA73',dry:'#5F7939'};
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)),mix=(a,b,t)=>a+(b-a)*t;
const ease=(a,b,t)=>{let u=clamp((t-a)/(b-a));return u*u*u*(10+u*(-15+6*u))};
function rng(seed){return()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296}}
function color(a,b,u){const aa=a.match(/\w\w/g).map(x=>parseInt(x,16)),bb=b.match(/\w\w/g).map(x=>parseInt(x,16));return '#'+aa.map((x,i)=>Math.round(mix(x,bb[i],u)).toString(16).padStart(2,'0')).join('')}
const svgNS='http://www.w3.org/2000/svg';
function sample(d,n=N){const p=document.createElementNS(svgNS,'path');p.setAttribute('d',d);const L=p.getTotalLength();return Array.from({length:n},(_,i)=>{const q=p.getPointAtLength(L*i/n);return[q.x,q.y]})}
const LEAF=sample('M 0 -176 C 64 -134 108 -56 87 28 C 77 93 28 136 0 172 C -50 115 -100 53 -89 -20 C -87 -90 -49 -147 0 -176 Z');
const DRY=LEAF.map(([x,y],i)=>{const k=Math.sin(Math.PI*clamp((y+176)/348));return[x*.9+Math.sin(i*.18)*5*k,y*.91+Math.sin(i*.13)*4*k]});
const rand=rng(631),grain=Array.from({length:1000},()=>[rand()*380-190,rand()*450-225,rand()*1.4+.2,rand()]);
const dots=Array.from({length:260},()=>[rand(),rand(),rand(),rand()]);
let paper,textureReady=false,fontReady=false,playing=false,startClock=0,playStart=0;
const query=new URLSearchParams(location.search),renderMode=query.has('render');
if(renderMode)document.documentElement.classList.add('render');
function poly(P,close=true){ctx.beginPath();P.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));if(close)ctx.closePath()}
function ellipse(x,y,rx,ry,fill){ctx.beginPath();ctx.ellipse(x,y,rx,ry,0,0,TAU);if(fill){ctx.fillStyle=fill;ctx.fill()}}
function curve(P,col,width){ctx.beginPath();P.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.strokeStyle=col;ctx.lineWidth=width;ctx.lineCap='round';ctx.lineJoin='round';ctx.stroke()}
function texture(x,y,w,h,alpha=.17){if(!paper)return;ctx.save();ctx.globalAlpha=alpha;ctx.globalCompositeOperation='multiply';ctx.drawImage(paper,x,y,w,h);ctx.restore()}
function paperBackground(col){ctx.fillStyle=col;ctx.fillRect(0,0,W,H);texture(0,0,W,H,.36)}
function leafPoints(dry){return LEAF.map((p,i)=>[mix(p[0],DRY[i][0],dry),mix(p[1],DRY[i][1],dry)])}
function drawLeaf({x=270,y=440,scale=1,rot=-.3,dry=0,detail=1,stem=true,alpha=1}={}){
 ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(scale,scale);ctx.globalAlpha=alpha;
 const P=leafPoints(dry);poly(P);const g=ctx.createLinearGradient(-90,-140,80,160);g.addColorStop(0,color(C.green,C.dry,dry));g.addColorStop(.5,color('#9CBF50','#82994A',dry));g.addColorStop(1,color('#406D37','#3D5630',dry));ctx.fillStyle=g;ctx.fill();
 ctx.save();ctx.clip();ctx.beginPath();ctx.moveTo(0,-190);ctx.bezierCurveTo(-7,-45,9,78,0,188);ctx.lineTo(-170,190);ctx.lineTo(-170,-190);ctx.closePath();ctx.fillStyle='#153F3020';ctx.fill();texture(-145,-190,290,390,.3*detail);
 for(const [gx,gy,r,a]of grain){ctx.fillStyle=a>.48?'#E8EFAD':'#244825';ctx.globalAlpha=alpha*.12*detail;ctx.beginPath();ctx.arc(gx,gy,r,0,TAU);ctx.fill()}
 ctx.globalAlpha=alpha;ctx.lineWidth=1.4;ctx.strokeStyle='#DEE6A4';ctx.globalAlpha=alpha*.63*detail;ctx.beginPath();ctx.moveTo(0,-160);ctx.bezierCurveTo(-5,-48,10,52,0,166);ctx.stroke();
 for(let j=0;j<9;j++){let yy=-115+j*30,w=72*Math.pow(Math.max(0,1-Math.abs(yy)/170),.7);for(const s of[-1,1]){ctx.beginPath();ctx.moveTo(2,yy+23);ctx.quadraticCurveTo(s*w*.58,yy+4,s*w,yy-26);ctx.stroke();ctx.globalAlpha=alpha*.18*detail;for(let k=1;k<=3;k++){let xx=s*w*k/4;ctx.beginPath();ctx.moveTo(xx,yy+18-45*k/4);ctx.lineTo(xx+s*15,yy-2-45*k/4);ctx.stroke()}ctx.globalAlpha=alpha*.63*detail}}
 ctx.restore();ctx.globalAlpha=alpha;if(stem){ctx.beginPath();ctx.moveTo(0,mix(171,155,dry));ctx.quadraticCurveTo(4,190,0,204);ctx.strokeStyle='#ADBA73';ctx.lineWidth=4;ctx.lineCap='round';ctx.stroke()}
 ctx.restore();return P;
}
function ribbonPoints(j,t){const g=ease(1.45,3.3,t),P=[];for(let k=0;k<82;k++){const u=k/81,phase=t*.65+j*1.5;const ax=144+j*128+Math.sin(u*8+phase)*31,ay=682-u*464;const bx=-60+u*660,by=410+j*88+Math.sin(u*TAU+phase)*23;P.push([mix(ax,bx,g),mix(ay,by,g)])}return P}
function drawRibbon(j,t,foreground=false){const P=ribbonPoints(j,t),g=ease(1.45,3.3,t);const left=[],right=[];for(let i=0;i<P.length;i++){const a=P[Math.max(0,i-1)],b=P[Math.min(P.length-1,i+1)],dx=b[0]-a[0],dy=b[1]-a[1],l=Math.hypot(dx,dy)||1,w=Math.pow(Math.sin(Math.PI*i/(P.length-1)),.8)*mix(14,5,g);left.push([P[i][0]-dy/l*w,P[i][1]+dx/l*w]);right.push([P[i][0]+dy/l*w,P[i][1]-dx/l*w])}ctx.save();ctx.globalAlpha=foreground?.18:.34;poly([...left,...right.reverse()]);ctx.fillStyle=color('#E6EBCF','#718B4B',g);ctx.fill();ctx.restore()}
function trayShape(g,lower=false){const P=[];for(let i=0;i<N;i++){const a=TAU*i/N,ex=Math.cos(a)*200,ey=Math.sin(a)*42,rx=Math.sign(Math.cos(a))*Math.pow(Math.abs(Math.cos(a)),.35)*mix(200,297,g),ry=Math.sign(Math.sin(a))*Math.pow(Math.abs(Math.sin(a)),.5)*18;P.push([mix(ex,rx,g),mix(ey,ry,g)+(lower?mix(50,22,g):0)])}return P}
function drawTray(t){const g=ease(1.65,3.1,t),y=630;ctx.save();ctx.translate(270+100*g,y);
 poly(trayShape(g,true));ctx.fillStyle=color('#927341','#68824E',g);ctx.fill();ctx.fillStyle=color('#B69862','#8A9D66',g);ctx.fillRect(-mix(199,296,g),0,mix(398,592,g),mix(48,22,g));poly(trayShape(g));ctx.fillStyle=color('#E3D3A4','#BCCA9A',g);ctx.fill();
 ctx.save();poly(trayShape(g));ctx.clip();texture(-300,-60,600,145,.25);for(let i=-290;i<=290;i+=12){ctx.strokeStyle=color('#A48B5655','#57754555',g);ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(i,-55);ctx.lineTo(i+mix(25,0,g),70);ctx.stroke()}
 for(let k=0;k<5;k++)drawLeaf({x:-115+k*59,y:4+Math.sin(k)*8,scale:.14,rot:-.85+k*.45,dry:g,detail:.4,stem:false});ctx.restore();
 poly(trayShape(g));ctx.strokeStyle=color('#D2B77D','#68824E',g);ctx.lineWidth=7;ctx.stroke();
 ctx.globalAlpha=1-g;for(let x=-170;x<=170;x+=25){ctx.beginPath();ctx.moveTo(x,18);ctx.lineTo(x+2,48);ctx.strokeStyle='#66563866';ctx.lineWidth=1;ctx.stroke()}ctx.restore();
}
function bgPreview(t){paperBackground(C.forest);ctx.fillStyle='#203F2D';ctx.beginPath();ctx.arc(60,480,325,0,TAU);ctx.fill();texture(0,0,W,H,.24);const g=ease(1.65,3.12,t),y=1100-1250*g;ctx.beginPath();ctx.moveTo(-30,y+80);ctx.bezierCurveTo(160,y-80,355,y+120,580,y-30);ctx.lineTo(580,1000);ctx.lineTo(-30,1000);ctx.closePath();ctx.save();ctx.clip();paperBackground(C.cream);ctx.restore();
 const ring=ease(2.5,4,t);ctx.save();ctx.globalAlpha=ring*.5;ellipse(370,442,238,238,'#DEE5C1');ctx.restore();}
function stateAt(local){const t=clamp(local,0,5),g=ease(1.65,3.3,t),dry=ease(2.45,4.55,t);return{localTime:t,globalTime:9+t,stage:t<2?'steam':'dry',morphProgress:g,dry,camera:cameraAt(t),leaf:{x:mix(281,390,g),y:mix(426,490,g)+Math.sin(t*1.4)*4*(1-g),rot:mix(.34,1.21,g)+Math.sin(t*1.7)*.025*(1-g),scale:mix(1.08,.99,dry)},leafContour:leafPoints(dry),ribbonContours:[0,1,2].map(j=>ribbonPoints(j,t)),caption:t<2?'蒸青，抑制酶促氧化':'不揉捻，干燥制成碾茶',material:'paper texture clipped in object coordinates'};}
const captionBoxes=[];
function textLine(txt,x,y,size,col,align='left',weight=400){ctx.font=`${weight} ${size}px Matcha`;ctx.textAlign=align;ctx.textBaseline='alphabetic';ctx.fillStyle=col;ctx.fillText(txt,x,y);const w=ctx.measureText(txt).width;captionBoxes.push({text:txt,left:align==='center'?x-w/2:x,right:align==='center'?x+w/2:x+w,top:y-size,bottom:y+size*.15})}
function captions(t,s){const g=ease(1.9,2.3,t),col=color(C.cream,C.forest,ease(1.65,3.12,t));ctx.save();ctx.globalAlpha=1-ease(1.77,2.05,t);textLine('蒸 青',44,779,47,col);textLine('蒸青，抑制酶促氧化',46,824,24,col);ctx.restore();ctx.save();ctx.globalAlpha=ease(2.05,2.35,t);textLine('干 燥',44,779,47,col);textLine('不揉捻，干燥制成碾茶',46,824,24,col);ctx.restore();ctx.save();ctx.globalAlpha=.5;textLine('一片叶的旅程',46,108,14,col);ctx.restore();}
function moisture(t,s){for(let i=0;i<14;i++){const start=2.25+i*.09,u=clamp((t-start)/1.15);if(u<=0||u>=1)continue;const a=dots[i],x=s.leaf.x+(a[0]-.5)*185+Math.sin(u*2.6+i)*45*u,y=s.leaf.y+(a[1]-.5)*120-u*130;ctx.save();ctx.globalAlpha=Math.sin(Math.PI*u)*.53;ellipse(x,y,2.4*(1-u)+.5,4*(1-u)+.5,'#83956C');ctx.restore()}}
// Absolute-time 2D camera: approach the leaf, follow the air, then reveal the drying bed.
// World layers move at different depths; captions remain in screen coordinates.
function cameraAt(t){const push=ease(0,1.25,t),travel=ease(1.45,4.6,t);return{x:270+70*travel,y:450+30*travel,zoom:.94+.055*push-.235*travel};}
function cameraLayer(c,depth,draw){ctx.save();ctx.translate(270,450);const z=1+(c.zoom-1)*depth;ctx.scale(z,z);ctx.translate(-270-(c.x-270)*depth,-450-(c.y-450)*depth);draw();ctx.restore();}
function drawPreview(t,showCaptions=true){const s=stateAt(t),c=s.camera;bgPreview(t);cameraLayer(c,.28,()=>{ctx.save();ctx.globalAlpha=.12;ellipse(85,380,185,260,t<2?C.light:C.green);ctx.restore()});cameraLayer(c,1,()=>{drawRibbon(0,t);drawRibbon(1,t);drawTray(t);drawLeaf({...s.leaf,dry:s.dry,detail:1-.55*Math.sin(Math.PI*s.morphProgress)});moisture(t,s)});cameraLayer(c,1.12,()=>drawRibbon(2,t,true));if(showCaptions)captions(t,s);return s}
function drawMill(x,y,sc=1,t=0){ctx.save();ctx.translate(x,y);ctx.scale(sc,sc);
 ellipse(0,174,208,48,'#D8DEBB');ellipse(0,167,181,34,'#8B9B74');
 ctx.fillStyle='#788570';ctx.beginPath();ctx.moveTo(-150,48);ctx.lineTo(-150,146);ctx.bezierCurveTo(-132,181,135,181,150,146);ctx.lineTo(150,48);ctx.closePath();ctx.fill();ellipse(0,49,150,41,'#B5BEA5');texture(-149,50,298,120,.4);
 ctx.fillStyle='#92A085';ctx.beginPath();ctx.moveTo(-149,-101);ctx.lineTo(-149,37);ctx.bezierCurveTo(-141,86,138,86,149,37);ctx.lineTo(149,-101);ctx.closePath();ctx.fill();ellipse(0,-102,149,43,'#C4CCB2');
 ctx.save();ctx.beginPath();ctx.rect(-147,-100,294,144);ctx.clip();texture(-150,-104,300,200,.45);for(let i=0;i<200;i++){let q=dots[i];ctx.fillStyle=i%2?'#E3E7CF55':'#42543B33';ctx.fillRect(q[0]*290-145,q[1]*145-100,q[2]*2+1,q[2]*2+1)}ctx.restore();
 ellipse(0,-101,38,12,C.dark);ellipse(0,-104,39,12,'#3D5039');
 ctx.save();ctx.translate(107,-130);ctx.rotate(.05);ctx.fillStyle='#AA8D56';ctx.fillRect(-8,-107,19,126);ellipse(1,-107,10,4,'#D5C396');ctx.strokeStyle='#D7C293';ctx.lineWidth=2;for(let k=-4;k<9;k+=4){ctx.beginPath();ctx.moveTo(k,-98);ctx.lineTo(k,13);ctx.stroke()}ctx.restore();
 ctx.fillStyle='#43583D';ctx.beginPath();ctx.roundRect(-143,99,27,30,8);ctx.fill();
 for(let i=0;i<160;i++){let q=dots[i];ctx.fillStyle=i%3?'#91B13D':'#B7CD65';let xx=-147+q[0]*85,yy=128+q[1]*35+Math.pow((xx+110)/80,2)*10;ellipse(xx,yy,1+q[2]*2,.9+q[2],ctx.fillStyle)}
 for(let k=0;k<4;k++)drawLeaf({x:-5+Math.sin(k*3)*26,y:-168-k*40,scale:.115,rot:k*.8-.4,detail:.4,stem:false,dry:1});ctx.restore();}
function drawBowl(x,y,sc=1,t=0){ctx.save();ctx.translate(x,y);ctx.scale(sc,sc);ellipse(0,175,175,28,'#79864C1A');ellipse(0,145,73,17,'#B6B99B');ctx.fillStyle='#E6DFC6';ctx.beginPath();ctx.moveTo(-204,-12);ctx.bezierCurveTo(-196,93,-131,155,0,160);ctx.bezierCurveTo(126,155,195,98,204,-12);ctx.closePath();ctx.fill();ctx.save();ctx.clip();texture(-220,-30,440,205,.42);ctx.fillStyle='#CABF9B33';ctx.beginPath();ctx.moveTo(-200,-20);ctx.quadraticCurveTo(-130,112,40,163);ctx.lineTo(-210,175);ctx.closePath();ctx.fill();ctx.restore();
 ellipse(0,-10,204,91,'#F7F2E2');ellipse(0,-7,181,76,'#A2BE53');ctx.save();ctx.beginPath();ctx.ellipse(0,-7,178,73,0,0,TAU);ctx.clip();const grad=ctx.createRadialGradient(-40,-10,15,0,0,190);grad.addColorStop(0,'#B9CF73');grad.addColorStop(1,'#6C912F');ctx.fillStyle=grad;ctx.fillRect(-200,-100,400,200);for(let i=0;i<240;i++){let q=dots[i],xx=(q[0]-.5)*360,yy=(q[1]-.5)*148-7;ctx.globalAlpha=.4;ellipse(xx,yy,1+q[2]*2.5,.7+q[2]*1.4,i%2?'#E5EAB2':'#577B2E')}ctx.globalAlpha=.35;for(let k=0;k<3;k++){ctx.beginPath();ctx.ellipse(-8,0,60+k*29,20+k*10,-.14,0,Math.PI*1.3);ctx.strokeStyle='#E4EABB';ctx.lineWidth=2;ctx.stroke()}ctx.restore();
 ctx.save();ctx.translate(155,-104);ctx.rotate(.47);ctx.fillStyle='#BA995F';ctx.beginPath();ctx.roundRect(-14,-164,28,136,7);ctx.fill();for(let i=0;i<17;i++){let u=i/16,xx=(u-.5)*95;ctx.beginPath();ctx.moveTo((u-.5)*24,-31);ctx.bezierCurveTo(xx*.7,3,xx*1.15,66,xx,94);ctx.strokeStyle=i%2?'#D6BD85':'#A2864F';ctx.lineWidth=2.3;ctx.stroke()}ctx.fillStyle='#4D5236';ctx.fillRect(-15,-35,30,7);ctx.restore();ctx.restore();}
function still(kind){paperBackground(C.cream);ctx.fillStyle='#DCE5BD';ellipse(365,393,268,268,ctx.fillStyle);ctx.save();ctx.globalAlpha=.7;texture(0,0,W,H,.3);ctx.restore();
 if(kind==='leaf'){drawLeaf({x:267,y:410,scale:1.25,rot:.31});drawLeaf({x:175,y:603,scale:.45,rot:-.82});ctx.beginPath();ctx.moveTo(190,731);ctx.quadraticCurveTo(227,620,208,619);ctx.strokeStyle='#7E9852';ctx.lineWidth=5;ctx.stroke();textLine('一片叶',44,780,46,C.forest);textLine('旅程，从一抹鲜绿开始',46,828,24,C.forest)}
 if(kind==='mill'){drawMill(270,445,1.04);textLine('细细研磨',44,780,46,C.forest);textLine('叶肉，成为细腻茶粉',46,828,24,C.forest);textLine('石磨示意',44,106,14,'#697B51')}
 if(kind==='bowl'){drawBowl(268,494,1.02);textLine('一碗抹茶',44,780,46,C.forest);textLine('把一片叶，喝进这一刻',46,828,24,C.forest)}
 return {representative:kind,renderedWith:'actual scene geometry and generated paper texture'};
}
function setupScale(scale){canvas.width=Math.round(W*scale);canvas.height=Math.round(H*scale);ctx.setTransform(scale,0,0,scale,0,0);captionBoxes.length=0;ctx.clearRect(0,0,W,H)}
window.renderAt=(seconds,type='image/png',quality=.97,scale=1,subtitles=true)=>{if(seconds<0||seconds>5)throw Error('Only 0–5s preview is implemented; full 35s awaits user feedback.');setupScale(scale);drawPreview(seconds);return canvas.toDataURL(type,quality)};
window.representativeAt=(kind,scale=2)=>{if(!['leaf','mill','bowl'].includes(kind))throw Error('Unknown representative');setupScale(scale);still(kind);return canvas.toDataURL('image/png')};
window.stateAt=stateAt;
window.inspectState=()=>({fontReady,textureReady,captionBoxes,width:canvas.width,height:canvas.height});
const audio=new Audio('./audio/preview.wav');audio.preload='auto';
const seek=document.querySelector('#seek'),button=document.querySelector('#play'),timeEl=document.querySelector('#time');
function paint(t){setupScale(1);drawPreview(t);seek.value=t;timeEl.textContent=t.toFixed(2)+' / 5.00'}
function loop(){if(!playing)return;const t=Math.min(5,audio.currentTime);paint(t);if(t>=4.99||audio.ended){playing=false;button.textContent='重新播放';return}requestAnimationFrame(loop)}
button.onclick=async()=>{if(playing){playing=false;audio.pause();button.textContent='继续播放'}else{if(audio.ended||+seek.value>=4.99)audio.currentTime=0;else audio.currentTime=+seek.value;await audio.play();playing=true;button.textContent='暂停';requestAnimationFrame(loop)}};
seek.oninput=()=>{playing=false;audio.pause();audio.currentTime=+seek.value;button.textContent='播放小样';paint(+seek.value)};
paper=await new Promise((res,rej)=>{const im=new Image();im.onload=()=>res(im);im.onerror=()=>rej(Error('paper missing'));im.src='./assets/paper-generated.png'});textureReady=true;
await document.fonts.load('24px Matcha');await document.fonts.ready;fontReady=document.fonts.check('24px Matcha');if(!fontReady)throw Error('Chinese font not loaded');
paint(0);window.ready=true;
// Shared drawing primitives for the authorized full-film entry; preview remains unchanged.
export {canvas,ctx,W,H,N,TAU,C,clamp,mix,ease,rng,color,sample,LEAF,DRY,dots,poly,ellipse,curve,texture,paperBackground,leafPoints,drawLeaf,drawRibbon,drawTray,stateAt,textLine,captionBoxes,cameraAt,cameraLayer,drawPreview,setupScale};
