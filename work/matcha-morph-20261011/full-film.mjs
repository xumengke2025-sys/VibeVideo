import {canvas,ctx,W,H,N,TAU,C,clamp,mix,ease,color,sample,LEAF,dots,poly,ellipse,curve,texture,paperBackground,drawLeaf,drawTray,stateAt as previewState,textLine,captionBoxes,cameraLayer,drawPreview,setupScale} from './film.mjs';
const DURATION=35;
const stages=[
 {start:0,end:3,id:'leaf',title:'一片叶',line:'怎样变成一碗抹茶？'},
 {start:3,end:7,id:'shade',title:'遮 阴',line:'采摘前遮阴，再采下嫩叶'},
 {start:7,end:11,id:'steam',title:'蒸 青',line:'蒸青，抑制酶促氧化'},
 {start:11,end:15,id:'dry',title:'干 燥',line:'不揉捻，干燥制成碾茶'},
 {start:15,end:19,id:'refine',title:'精 制',line:'去梗、去叶脉，留下叶肉'},
 {start:19,end:24,id:'mill',title:'细细研磨',line:'叶肉磨成粉，成为抹茶'},
 {start:24,end:29,id:'water',title:'加 水',line:'让茶粉在水中均匀分散'},
 {start:29,end:35,id:'whisk',title:'一碗抹茶',line:'茶筅击拂，从一片叶到这一刻'}
];
const circle=Array.from({length:N},(_,i)=>[Math.sin(TAU*i/N)*85,-Math.cos(TAU*i/N)*85]);
const fragments=Array.from({length:16},(_,i)=>{const row=Math.floor(i/2),side=i%2?1:-1,y=-127+row*35,w=80*Math.sin(Math.PI*(row+.7)/8.8);return {side,y,w,shape:[[side*5,y+1],[side*w*.74,y-12],[side*w,y+6],[side*w*.8,y+25],[side*7,y+29]]}});
function alpha(a,fn){if(a<=0)return;ctx.save();ctx.globalAlpha*=clamp(a);fn();ctx.restore()}
function localPreview(t){return t<=11?(t-7)*.5:2+(t-11)*.75}
function stageAt(t){return stages.find(s=>t>=s.start&&t<s.end)||stages.at(-1)}
function screenBg(t){let col=C.cream;if(t>3&&t<7.7)col=color(C.cream,C.forest,ease(3,4,t));if(t>=7.7&&t<11)col=C.forest;if(t>=11&&t<15)col=color(C.forest,C.cream,ease(11,12.5,t));if(t>=23.3)col=color(C.cream,C.forest,ease(23.3,24.7,t));paperBackground(col);const light=t<3||t>=12.5&&t<23.8;alpha(.4,()=>ellipse(340+Math.sin(t*.17)*32,425,245,245,light?'#DDE6BE':'#25503A'));return col}
function drawOpening(t){
 const u=ease(0,1.15,t),shade=ease(3,4.15,t),exit=ease(6,7,t),c={x:270+25*shade*(1-exit),y:450-15*shade*(1-exit),zoom:.97+.04*ease(0,2,t)-.09*shade+.02*exit};
 cameraLayer(c,.25,()=>{alpha(shade*(1-exit)*.26,()=>{for(let k=0;k<8;k++){ctx.beginPath();ctx.moveTo(30+k*79,205);ctx.lineTo(-120+k*92,700);ctx.strokeStyle='#E8DF9C';ctx.lineWidth=9*(1-shade*.7);ctx.stroke()}})});
 cameraLayer(c,.65,()=>alpha(shade*(1-exit),()=>{for(let k=0;k<7;k++){let x=30+k*85,y=655+Math.sin(k)*25;curve([[x,720],[x+3,y-60]],'#8DA968',4);for(let j=0;j<3;j++)drawLeaf({x:x+(j-1)*27,y:y-j*28,scale:.25,rot:(j-1)*.9,detail:.45})}}));
 cameraLayer(c,1,()=>{
  const px=270+11*exit+30*shade*(1-exit),py=425-10*shade*(1-exit)+exit,rot=.34-.1*shade*(1-exit),sc=mix(.98,1.08,exit);
  if(t<1.25){ctx.save();ctx.translate(px,py);ctx.rotate(rot);ctx.scale(sc,sc);poly(LEAF.map((p,i)=>[mix(circle[i][0]*.12,p[0],u),mix(circle[i][1]*.12,p[1],u)]));ctx.fillStyle=C.green;ctx.fill();ctx.restore();alpha(ease(.55,1.25,t),()=>drawLeaf({x:px,y:py,rot,scale:sc,detail:ease(.65,1.6,t)}))}
  else drawLeaf({x:px,y:py,rot,scale:sc,detail:1});
  alpha(shade*(1-exit),()=>{curve([[px-66,610],[px-75,683],[px-86,735]],'#95AD70',5)});
  alpha(exit,()=>drawTray(0));
 });
 // An overhead woven shade cloth arrives over the crop, then withdraws on picking.
 cameraLayer(c,1.13,()=>alpha(shade*(1-exit),()=>{const yy=mix(80,206,shade);ctx.fillStyle='#0D2D24';ctx.beginPath();ctx.moveTo(-20,yy);ctx.lineTo(560,yy-25);ctx.lineTo(555,yy+55);ctx.lineTo(-25,yy+70);ctx.closePath();ctx.fill();for(let k=0;k<26;k++)curve([[k*24,yy-2],[k*24-8,yy+65]],'#87A07755',1.4);for(let j=0;j<4;j++)curve([[-20,yy+j*17],[560,yy-25+j*17]],'#87A07755',1.2);curve([[25,yy+65],[25,680]],'#56774F',5);curve([[510,yy+42],[510,660]],'#56774F',5)}));
}
function refineCamera(t){let u=ease(15,16,t);return{x:mix(340,270,u),y:mix(480,450,u),zoom:mix(.76,.94,u)}}
function meatPiece(P,fill){poly(P);ctx.fillStyle=fill;ctx.fill();ctx.save();ctx.clip();texture(-100,-180,200,360,.32);ctx.restore();ctx.strokeStyle='#ADC27755';ctx.lineWidth=1;ctx.stroke()}
function drawRefine(t){const u=ease(15.5,17.4,t),ring=ease(17.25,19,t),c=refineCamera(t),ps=previewState(5),m=ease(15,16,t),lx=mix(ps.leaf.x,270,m),ly=mix(ps.leaf.y,425,m),rot=mix(ps.leaf.rot,.12,m),sc=mix(ps.leaf.scale,1,m);
 cameraLayer(c,.4,()=>alpha(.25,()=>ellipse(130,465,220,220,'#D1DDB1')));
 cameraLayer(c,1,()=>{alpha(1-ease(15,15.7,t),()=>drawTray(5));
  alpha(1-ease(15.55,16.35,t),()=>drawLeaf({x:lx,y:ly,rot,scale:sc,dry:1,detail:1}));
  alpha(ease(15.55,16.35,t),()=>{for(let i=0;i<fragments.length;i++){const f=fragments[i],ang=-Math.PI/2+TAU*i/fragments.length;
   ctx.save();ctx.translate(lx,ly);ctx.rotate(rot*(1-ring));ctx.scale(sc,sc);
   const ox=f.side*34*u*(1-ring),oy=(f.y-5)*.1*u*(1-ring);
   const tx=Math.cos(ang)*102,ty=-46+Math.sin(ang)*72,a=ang+.5,cx=f.side*f.w*.5,cy=f.y+10;
   const P=f.shape.map(([x,y])=>{const vx=(x-cx)*.65,vy=(y-cy)*.65;return [mix(x+ox,tx+vx*Math.cos(a)-vy*Math.sin(a),ring),mix(y+oy,ty+vx*Math.sin(a)+vy*Math.cos(a),ring)]});
   meatPiece(P,i%2?'#6E8A41':'#809A4F');ctx.restore();}});
  // Isolated central stem and branching veins leave the leaf meat as one network.
  alpha(ease(15.55,16.35,t)*(1-ease(17,18,t)),()=>{ctx.save();ctx.translate(lx+135*u,ly-30*u);ctx.rotate(rot-.28*u);ctx.scale(sc*(1-.2*u),sc*(1-.2*u));curve([[0,-153],[-3,0],[0,196]],'#C4AD75',4);for(let j=0;j<7;j++){let yy=-110+j*37,w=70*Math.sin(Math.PI*(j+.8)/8.4);for(const side of [-1,1])curve([[0,yy+25],[side*w*.65,yy+3],[side*w,yy-20]],'#C4AD75',3)}ctx.restore()});
 });
}
function millGeometry(x,y,sc,t,assembly=1){ctx.save();ctx.translate(x,y);ctx.scale(sc,sc);
 alpha(assembly,()=>{ellipse(0,174,208,48,'#D8DEBB');ellipse(0,167,181,34,'#8B9B74');ctx.fillStyle='#788570';ctx.beginPath();ctx.moveTo(-150,48);ctx.lineTo(-150,146);ctx.bezierCurveTo(-132,181,135,181,150,146);ctx.lineTo(150,48);ctx.closePath();ctx.fill();ellipse(0,49,150,41,'#B5BEA5');texture(-149,50,298,120,.4);ctx.fillStyle='#92A085';ctx.beginPath();ctx.moveTo(-149,-101);ctx.lineTo(-149,37);ctx.bezierCurveTo(-141,86,138,86,149,37);ctx.lineTo(149,-101);ctx.closePath();ctx.fill();ctx.save();ctx.beginPath();ctx.rect(-147,-100,294,144);ctx.clip();texture(-150,-104,300,200,.45);for(let i=0;i<160;i++){let q=dots[i];ctx.fillStyle=i%2?'#E3E7CF55':'#42543B33';ctx.fillRect(q[0]*290-145,q[1]*145-100,1+q[2]*2,1+q[2]*2)}ctx.restore();});
 alpha(assembly,()=>{ellipse(0,-102,149,43,'#C4CCB2');texture(-140,-126,280,42,.12);
 for(let k=0;k<12;k++){let a=k*TAU/12+t*1.2;curve([[Math.cos(a)*59,-102+Math.sin(a)*17],[Math.cos(a)*133,-102+Math.sin(a)*37]],'#829475',1.4)}
 ellipse(0,-101,38,12,C.dark);ellipse(0,-104,39,12,'#3D5039');});
 const a=t*1.2,hx=Math.cos(a)*110,hy=-102+Math.sin(a)*31;
 alpha(assembly,()=>{ctx.save();ctx.translate(hx,hy);ctx.rotate(.08+Math.sin(a)*.12);ctx.fillStyle='#AA8D56';ctx.beginPath();ctx.roundRect(-8,-115,19,117,4);ctx.fill();ellipse(1,-115,10,4,'#D5C396');for(let k=-4;k<9;k+=4)curve([[k,-105],[k,-4]],'#D7C293',1.4);ctx.restore();ctx.fillStyle='#43583D';ctx.beginPath();ctx.roundRect(-143,99,27,30,8);ctx.fill()});ctx.restore();}
function powderLocation(t){const rise=ease(23,24.35,t);return{x:mix(146,270,rise),y:mix(650,337,rise),spread:mix(77,95,rise),rise}}
function powderCloud(t){const loc=powderLocation(t),appear=ease(20.3,22.5,t),fall=ease(24.35,25.45,t);
 for(let i=0;i<260;i++){const q=dots[i],radius=Math.sqrt(q[0]),ang=q[1]*TAU+loc.rise*2.5;let px=loc.x+Math.cos(ang)*loc.spread*radius,py=loc.y+Math.sin(ang)*loc.spread*.37*radius;
  const ff=ease(24.35+q[2]*.55,25.25+q[2]*.35,t);px=mix(px,270+(q[0]-.5)*115,ff);py=mix(py,512+(q[1]-.5)*22,ff);
  alpha(appear*(1-ease(25.3,25.7,t)),()=>ellipse(px,py,1.4+q[2]*2.3,1+q[2]*1.3,i%3?'#93B442':'#C4D578'));
 }
}
function drawMillStage(t,showPowder=true){const assembly=ease(19,19.75,t),out=1-ease(23,24.2,t),c={x:270-28*ease(20.5,22.8,t),y:450+22*ease(20.5,22.8,t),zoom:.94+.055*ease(19.6,22.8,t)};
 cameraLayer(c,.32,()=>alpha(out*.3,()=>ellipse(360,410,230,230,'#D0DBB2')));
 cameraLayer(c,1,()=>{alpha(out,()=>{
  millGeometry(270,455,.93,t-19,assembly);
  // The leaf-meat ring settles into the top inlet, keeping the same fragments.
  for(let i=0;i<16;i++){const f=fragments[i],ang=-Math.PI/2+i*TAU/16,u=ease(19+i*.035,20.8+i*.035,t);ctx.save();ctx.translate(mix(270+Math.cos(ang)*96,270+(i%3-1)*12,u),mix(381+Math.sin(ang)*67,352,u));ctx.rotate(ang*.5);ctx.scale(.55*(1-.5*u),.55*(1-.5*u));alpha(1-ease(20.25+i*.035,21.1+i*.035,t),()=>meatPiece(f.shape,i%2?'#6E8A41':'#809A4F'));ctx.restore();}
  // Fresh feed trickles down without implying the mill itself transforms to powder.
  alpha(ease(20.2,20.7,t)*(1-ease(22.6,23,t)),()=>{for(let i=0;i<12;i++){let q=dots[i],u=(t*.72+q[0])%1;ctx.save();ctx.translate(270+(q[1]-.5)*35,246+u*104);ctx.rotate(q[2]*5+t);poly([[-4,-4],[5,-2],[2,6],[-3,3]]);ctx.fillStyle='#789745';ctx.fill();ctx.restore()}});
  alpha(ease(20.4,20.9,t)*(1-ease(22.8,23.2,t)),()=>{for(let i=0;i<60;i++){const q=dots[i],u=(t*1.5+q[0])%1;ellipse(147+(q[1]-.5)*(8+u*36),576+u*70,1+q[2]*1.3,1.3,'#8FAA40')}});
 });});
 if(showPowder)powderCloud(t);
}
function bowlGeometry(t){const appear=ease(23.4,24.4,t),fill=ease(25.45,27.5,t),foam=ease(29.7,32.7,t),x=270,y=521,sc=1.01-.025*ease(32.5,34,t);
 alpha(appear,()=>{ctx.save();ctx.translate(x,y+90*(1-appear));ctx.scale(sc,sc);
  ellipse(0,175,175,28,t<24.5?'#79864C1A':'#081C1B44');ellipse(0,145,73,17,'#B6B99B');ctx.fillStyle='#E6DFC6';ctx.beginPath();ctx.moveTo(-204,-12);ctx.bezierCurveTo(-196,93,-131,155,0,160);ctx.bezierCurveTo(126,155,195,98,204,-12);ctx.closePath();ctx.fill();ctx.save();ctx.clip();texture(-220,-30,440,205,.42);ctx.fillStyle='#CABF9B33';ctx.beginPath();ctx.moveTo(-200,-20);ctx.quadraticCurveTo(-130,112,40,163);ctx.lineTo(-210,175);ctx.closePath();ctx.fill();ctx.restore();
  ellipse(0,-10,204,91,'#F7F2E2');ellipse(0,-7,181,76,color('#DED6BB','#7FA43D',fill));ctx.save();ctx.beginPath();ctx.ellipse(0,-7,178,73,0,0,TAU);ctx.clip();
  alpha(fill,()=>{const grad=ctx.createRadialGradient(-40,-10,15,0,0,190);grad.addColorStop(0,color('#D3E6BB','#B9CF73',fill));grad.addColorStop(1,'#6C912F');ctx.fillStyle=grad;ctx.fillRect(-200,-100,400,200)});
  const deposit=ease(24.9,25.6,t),disp=ease(25.6,28,t);
  for(let i=0;i<230;i++){let q=dots[i],xx=(q[0]-.5)*mix(112,350,disp),yy=(q[1]-.5)*mix(21,145,disp)-7;let a=(t-29)*5*(1-ease(32.5,33.5,t));if(t>29){let X=xx;xx=X*Math.cos(a)-yy*2*Math.sin(a);yy=(X*.35*Math.sin(a)+yy*Math.cos(a))}alpha(deposit*(.55-.26*foam),()=>ellipse(xx,yy,1+q[2]*2,.7+q[2]*1.3,i%2?'#C8DB82':'#4E792D'));}
  alpha(ease(26,27,t),()=>{for(let k=0;k<3;k++){let a=t>29?(t-29)*2:0;ctx.beginPath();ctx.ellipse(Math.sin(a)*8,0,60+k*29,20+k*10,-.14,0,Math.PI*1.3);ctx.strokeStyle='#E4EABB';ctx.globalAlpha=.16+.17*foam;ctx.lineWidth=2;ctx.stroke()}});
  for(let i=0;i<120;i++){let q=dots[i];alpha(foam*.6,()=>{ellipse((q[0]-.5)*330,(q[1]-.5)*125-8,1.4+q[2]*2.5,.8+q[2]*1.5,'#E7ECC0')})}ctx.restore();
  // Tea whisk bristles contact the liquid inside the rim; handle and tines share one pose.
  alpha(ease(28.85,29.55,t),()=>{const act=ease(29.2,29.7,t)*(1-ease(32.6,33.5,t));ctx.save();ctx.translate(105+Math.sin(t*14)*18*act,-101+Math.cos(t*14)*6*act);ctx.rotate(.34+Math.sin(t*14)*.06*act);ctx.fillStyle='#BA995F';ctx.beginPath();ctx.roundRect(-14,-164,28,136,7);ctx.fill();texture(-13,-164,26,130,.3);for(let i=0;i<17;i++){let u=i/16,xx=(u-.5)*95;ctx.beginPath();ctx.moveTo((u-.5)*24,-31);ctx.bezierCurveTo(xx*.7,3,xx*1.15,66,xx,94);ctx.strokeStyle=i%2?'#D6BD85':'#A2864F';ctx.lineWidth=2.3;ctx.stroke()}ctx.fillStyle='#4D5236';ctx.fillRect(-15,-35,30,7);ctx.restore()});ctx.restore();});
}
function pourWater(t){const a=ease(25.4,25.75,t)*(1-ease(27.5,27.95,t));alpha(a,()=>{ctx.save();ctx.translate(388,288);ctx.rotate(-.36);ctx.fillStyle='#E8DFC5';ctx.beginPath();ctx.moveTo(-56,-25);ctx.quadraticCurveTo(-69,34,-22,48);ctx.lineTo(25,46);ctx.lineTo(43,-29);ctx.closePath();ctx.fill();texture(-62,-26,100,80,.2);ctx.beginPath();ctx.moveTo(-53,-12);ctx.lineTo(-86,13);ctx.lineTo(-53,26);ctx.closePath();ctx.fill();ellipse(-3,-26,46,11,'#C7C1AA');ctx.restore();ctx.beginPath();ctx.moveTo(307,313);ctx.bezierCurveTo(288,350,261,390,263,508);ctx.strokeStyle='#DDEBCD';ctx.lineWidth=8;ctx.lineCap='round';ctx.stroke();for(let i=0;i<8;i++){const u=(t*1.3+i/8)%1;ellipse(264+Math.sin(u*5)*6,335+u*172,1.5,4,'#F0F4DE')}alpha(.4,()=>ellipse(264,511,17+Math.sin(t*12)*4,5,'#F5F5DE'));});}
function captionsFull(t){const s=stageAt(t),next=stages[stages.indexOf(s)+1],last=stages[stages.indexOf(s)-1];const after=last?ease(s.start,s.start+.25,t):1,before=next?1-ease(s.end-.25,s.end,t):1;let col=t<7?color(C.forest,C.cream,ease(3,4,t)):t<15?color(C.cream,C.forest,ease(1.65,3.12,localPreview(t))):C.forest;if(t>=23.3)col=color(C.forest,C.cream,ease(23.3,24.7,t));
 alpha(after*before,()=>{textLine(s.title,44,779,s.id==='mill'||s.id==='whisk'?45:47,col);textLine(s.line,46,824,s.id==='whisk'?22:24,col)});
 alpha(.56,()=>textLine(t>=24?'饮用准备':'一片叶的旅程',46,108,14,col));
 if(t>=19&&t<23.4)alpha(ease(19,19.4,t)*(1-ease(23,23.4,t))*.65,()=>textLine('石磨工艺示意',46,145,14,col));
 if(t>=15&&t<18.7)alpha(ease(15.3,15.7,t)*(1-ease(18.3,18.7,t))*.65,()=>textLine('精制过程示意',46,145,14,col));
 if(t>=33.3)alpha(ease(33.3,33.8,t)*.66,()=>textLine('遮阴 · 蒸青 · 干燥 · 精制 · 研磨',46,876,18,col));
}
function fullState(t){const s=stageAt(t),local=clamp(localPreview(t),0,5);return{time:t,stage:s.id,caption:s.line,leafContour:LEAF,camera:t>=7&&t<=15?previewState(local).camera:t>=15&&t<19?refineCamera(t):null,sourcePreviewTime:t>=7&&t<=15?local:null,semantic:'Production schematic; water/whisk stages are drinking preparation',registeredRegions:{captions:[44,732,498,840],mainArt:[35,180,505,724]}}}
function drawFull(t){screenBg(t);if(t<7)drawOpening(t);else if(t<15)drawPreview(localPreview(t),false);else if(t<19)drawRefine(t);else if(t<24)drawMillStage(t);else {if(t<25.7){drawMillStage(t,false);bowlGeometry(t);powderCloud(t)}else bowlGeometry(t);pourWater(t)}captionsFull(t);return fullState(t)}
window.renderAt=(seconds,type='image/png',quality=.96,scale=2)=>{if(seconds<0||seconds>DURATION)throw Error('Full film range 0–35s');setupScale(scale);drawFull(seconds);return canvas.toDataURL(type,quality)};
window.stateAt=fullState;
window.inspectState=()=>({fontReady:document.fonts.check('24px Matcha'),textureReady:true,captionBoxes,width:canvas.width,height:canvas.height});
const audio=new Audio('./audio/full.wav');audio.preload='auto';const seek=document.querySelector('#seek'),button=document.querySelector('#play'),timeEl=document.querySelector('#time');let playing=false;
function paint(t){setupScale(1);drawFull(t);seek.value=t;timeEl.textContent=t.toFixed(2)+' / 35.00'}
function loop(){if(!playing)return;const t=Math.min(DURATION,audio.currentTime);paint(t);if(audio.ended||t>=34.99){playing=false;button.textContent='重新播放';return}requestAnimationFrame(loop)}
button.onclick=async()=>{if(playing){playing=false;audio.pause();button.textContent='继续播放'}else{audio.currentTime=audio.ended||+seek.value>=34.99?0:+seek.value;await audio.play();playing=true;button.textContent='暂停';requestAnimationFrame(loop)}};
seek.oninput=()=>{playing=false;audio.pause();audio.currentTime=+seek.value;button.textContent='播放整片';paint(+seek.value)};
paint(0);window.fullReady=true;
