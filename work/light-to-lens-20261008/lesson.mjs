import * as THREE from 'three';
import {renderAt as drawSpace,quality as spaceQuality} from './film.mjs';

export const DURATION=90,FPS=30;
const W=Number(new URLSearchParams(location.search).get('w'))||1920,H=Math.round(W*9/16);
const canvas=document.getElementById('type');canvas.width=W;canvas.height=H;
const ctx=canvas.getContext('2d');
const C={gold:'#ffc786',white:'#e7eef2',muted:'#92a8b8',blue:'#76cfe7',grid:'#264051',bg:'#03070d'};
const zh='"Microsoft YaHei", "Noto Sans SC", sans-serif',en='Bahnschrift, "Segoe UI", sans-serif';
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)),smooth=x=>{x=clamp(x);return x*x*(3-2*x);};
const ramp=(t,a,b)=>smooth((t-a)/(b-a)),lerp=(a,b,t)=>a+(b-a)*t;
const P=([x,y])=>[960+x*132,510-y*100];
await document.fonts.ready;

function text(str,x,y,size=26,color=C.white,align='left',weight=400,family=zh){ctx.font=`${weight} ${size}px ${family}`;ctx.textAlign=align;ctx.fillStyle=color;ctx.fillText(str,x,y);}
function alpha(a,fn){if(a<=.001)return;ctx.save();ctx.globalAlpha*=a;fn();ctx.restore();}
function line(points,color=C.gold,width=2,dash=[],fraction=1){
 if(fraction<=0||points.length<2)return;
 const n=clamp(fraction)*(points.length-1),whole=Math.floor(n),part=n-whole;
 ctx.save();ctx.strokeStyle=color;ctx.lineWidth=width;ctx.lineJoin='round';ctx.lineCap='round';ctx.setLineDash(dash);ctx.beginPath();ctx.moveTo(...points[0]);
 for(let i=1;i<=whole;i++)ctx.lineTo(...points[i]);
 if(whole<points.length-1)ctx.lineTo(lerp(points[whole][0],points[whole+1][0],part),lerp(points[whole][1],points[whole+1][1],part));
 ctx.stroke();ctx.restore();
}
function glow(x,y,color=C.gold,size=9){ctx.save();const g=ctx.createRadialGradient(x,y,0,x,y,size*4);g.addColorStop(0,color);g.addColorStop(.18,color+'b0');g.addColorStop(1,color+'00');ctx.fillStyle=g;ctx.fillRect(x-size*4,y-size*4,size*8,size*8);ctx.fillStyle='#fff5df';ctx.beginPath();ctx.arc(x,y,size*.25,0,Math.PI*2);ctx.fill();ctx.restore();}
function ring(x,y,r,color=C.blue,dash=[]){ctx.save();ctx.strokeStyle=color;ctx.lineWidth=1.5;ctx.setLineDash(dash);ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.stroke();ctx.restore();}
function arrow(p,q,color=C.gold,size=12){const a=Math.atan2(q[1]-p[1],q[0]-p[0]);line([[q[0]-size*Math.cos(a-.4),q[1]-size*Math.sin(a-.4)],q,[q[0]-size*Math.cos(a+.4),q[1]-size*Math.sin(a+.4)]],color,2);}
function samplePath(points,p){const a=clamp(p)*(points.length-1),i=Math.min(points.length-2,Math.floor(a));return [lerp(points[i][0],points[i+1][0],a-i),lerp(points[i][1],points[i+1][1],a-i)];}
function photon(points,p,a=1){alpha(a,()=>{const xy=samplePath(points,p);glow(...xy,C.gold,10);});}
function grid(t){
 const g=ctx.createRadialGradient(960,460,60,960,460,1080);g.addColorStop(0,'#0b1923');g.addColorStop(.7,'#050d15');g.addColorStop(1,C.bg);ctx.fillStyle=g;ctx.fillRect(0,0,1920,1080);
 ctx.save();ctx.strokeStyle='#31516720';ctx.lineWidth=1;
 for(let x=106;x<1850;x+=88){ctx.beginPath();ctx.moveTo(x,165);ctx.lineTo(x,798);ctx.stroke();}
 for(let y=180;y<800;y+=88){ctx.beginPath();ctx.moveTo(106,y);ctx.lineTo(1814,y);ctx.stroke();}
 ctx.restore();
}
function observer(pos){const [x,y]=P(pos);ctx.save();ctx.strokeStyle=C.blue;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x-28,y);ctx.bezierCurveTo(x-8,y-25,x+20,y-25,x+31,y);ctx.bezierCurveTo(x+20,y+25,x-8,y+25,x-28,y);ctx.stroke();ring(x+1,y,8,C.blue);text('观察者 O',x,y+61,25,C.blue,'center');ctx.restore();}
function source(pos,label='光源 S',offset=42){const xy=P(pos);glow(...xy,C.gold,8);text(label,xy[0],xy[1]+offset,25,C.gold,'center');}
function mass(){const [x,y]=P([0,0]);const g=ctx.createRadialGradient(x,y,0,x,y,56);g.addColorStop(0,'#24445a');g.addColorStop(.7,'#122434');g.addColorStop(1,'#12243400');ctx.fillStyle=g;ctx.fillRect(x-60,y-60,120,120);ring(x,y,23,'#a5bbca');ring(x,y,31,'#829baa33');text('质量 M',x,y+82,24,C.muted,'center');}
function axis(){line([P([-6.1,0]),P([6.1,0])],'#7795aa44',1,[4,10]);}
function ray(points,f=1,color=C.gold){alpha(.1,()=>line(points,color,11,[],f));line(points,color,2.3,[],f);}

function straight(t){
 const s=[-5.2,1.15],o=[5.2,0];const points=Array.from({length:201},(_,i)=>P([lerp(s[0],o[0],i/200),lerp(s[1],o[1],i/200)]));
 axis();source(s);observer(o);
 const p=ramp(t,.4,5.5);ray(points,p);photon(points,p,1-ramp(t,5.6,6.1));
 alpha(ramp(t,6,7),()=>{line([P(o),P(s)],C.blue,1.8,[8,9],ramp(t,6.4,8.8));arrow(P([4,.14]),P([3.4,.2]),C.blue,13);text('沿到达方向，反向延长',1120,665,28,C.blue);});
 alpha(ramp(t,8.9,9.6),()=>{ring(...P(s),17,C.blue);text('真实位置 = 视位置',245,711,34,C.white);});
 text('平直时空',248,232,24,C.muted);text('传播方向',920,352,21,C.gold);arrow(P([-.8,.663]),P([.1,.565]),C.gold);
}

// Finite-start Schwarzschild orbital illustration, not a strong-field thin-lens prediction.
const orbitCache=[];
function orbit(b){
 let x=-18,y=b,vx=1,vy=0,rs=.22,L2=(x*vy-y*vx)**2,raw=[];
 const acc=(xx,yy)=>{const q=-1.5*rs*L2/Math.hypot(xx,yy)**5;return [xx*q,yy*q];};
 for(let i=0;i<5000&&x<7;i++){
  raw.push([x,y]);let [ax,ay]=acc(x,y),dt=.014;
  const nx=x+vx*dt+.5*ax*dt*dt,ny=y+vy*dt+.5*ay*dt*dt,[bx,by]=acc(nx,ny);
  vx+=(ax+bx)*dt*.5;vy+=(ay+by)*dt*.5;x=nx;y=ny;
 }
 let cursor=0;
 return Array.from({length:241},(_,i)=>{const xx=-6.1+i/240*12.2;while(cursor<raw.length-2&&raw[cursor+1][0]<xx)cursor++;const a=raw[cursor],b=raw[cursor+1];return [xx,lerp(a[1],b[1],clamp((xx-a[0])/(b[0]-a[0])))];});
}
for(let i=0;i<=80;i++)orbitCache.push(orbit(1.6+i/80*1.15));
function bent(t){
 const u=t-12;axis();mass();
 const b=lerp(2.75,1.6,ramp(u,3,9)),index=(b-1.6)/1.15*80,i=Math.floor(index),f=index-i;
 const curve=orbitCache[i].map((p,k)=>P([p[0],lerp(p[1],orbitCache[Math.min(80,i+1)][k][1],f)]));
 for(const j of [0,80])alpha(.32,()=>line(orbitCache[j].map(P),C.blue,1.1,[4,9]));
 ray(curve,ramp(u,.1,2.5));photon(curve,clamp((u-.3)/2.6),1-ramp(u,2.8,3.3));
 const xb=-4.25;line([P([xb,0]),P([xb,b])],C.blue,1.5);line([P([xb-.09,0]),P([xb+.09,0])],C.blue);line([P([xb-.09,b]),P([xb+.09,b])],C.blue);
 text('b',P([xb, b/2])[0]-22,P([xb,b/2])[1]+7,32,C.blue,'right',400,en);
 text('远处入射偏移',235,602,23,C.muted);text('固定质量，减小 b',1294,230,27,C.blue);
 text('α ≈ 4GM / (bc²)',252,724,49,C.white,'left',400,en);text('弱场近似：b 越小，偏折角越大',254,767,23,C.muted);
 const gx=1300,gy=736;line([[gx,gy-125],[gx,gy],[gx+286,gy]],'#7995aa77',1);
 const data=Array.from({length:100},(_,k)=>{const q=1.6+k/99*1.15;return [gx+35+k/99*220,gy-(.44/q)*320];});line(data,C.gold,2);glow(gx+35+(b-1.6)/1.15*220,gy-(.44/b)*320,C.gold,6);text('α',gx-18,gy-133,24,C.gold,'left',400,en);text('b',gx+300,gy+7,24,C.blue,'left',400,en);
}

const S=[-5.2,1.1],O=[5.2,0],B=1.36,I=[-5.2,2*B];
const imageRay=Array.from({length:241},(_,i)=>{
 const x=lerp(S[0],O[0],i/240),d=.5,leftSlope=(B-S[1])/5.2,rightSlope=-B/5.2;
 let y;
 if(x<=-d)y=B+leftSlope*x;
 else if(x>=d)y=B+rightSlope*x;
 else{const p=(x+d)/(2*d),ya=B-leftSlope*d,yb=B+rightSlope*d; y=(2*p**3-3*p*p+1)*ya+(p**3-2*p*p+p)*2*d*leftSlope+(-2*p**3+3*p*p)*yb+(p**3-p*p)*2*d*rightSlope;}
 return P([x,y]);
});
function apparent(t){
 const u=t-25;axis();mass();source(S,'真实光源 S',47);observer(O);
 line([P([0,-2.1]),P([0,3.1])],'#617a8d33',1,[3,9]);text('简化透镜平面',984,674,22,C.muted);
 const p=ramp(u,.6,5.2);ray(imageRay,p);photon(imageRay,p,1-ramp(u,5.2,5.8));
 alpha(ramp(u,5.4,6.2),()=>{text('只测到最终的到达方向',1260,619,28,C.blue);line([P(O),P([3.3,(5.2-3.3)*B/5.2])],C.blue,3);});
 const reverse=ramp(u,6.1,10.5);
 alpha(ramp(u,6,6.4),()=>line([P(O),P(I)],C.blue,2,[9,10],reverse));
 alpha(ramp(u,10.5,11.1),()=>{ring(...P(I),13,C.blue);text('视位置 I',P(I)[0],P(I)[1]-35,29,C.blue,'center');line([P(S),P(I)],'#76cfe75c',1,[3,7]);text('真实位置 S',590,745,32,C.gold);text('≠',930,745,44,C.white,'center',400,en);text('视位置 I',1010,745,32,C.blue);});
 alpha(ramp(u,6,6.8),()=>{ctx.save();ctx.strokeStyle=C.blue;ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(...P(O),82,Math.PI,Math.PI+Math.atan(B/5.2));ctx.stroke();ctx.restore();text('θ',P(O)[0]-113,P(O)[1]-18,27,C.blue,'left',400,en);});
 text('真实光路',785,328,24,C.gold);alpha(reverse,()=>text('反向延长线',685,202,24,C.blue));
}

const mappedCanvas=document.createElement('canvas');mappedCanvas.width=540;mappedCanvas.height=480;const mc=mappedCanvas.getContext('2d');
let lastMapKey=-1;
function mapImage(size){
 const key=Math.round(size*1500);if(key===lastMapKey)return;lastMapKey=key;
 const data=mc.createImageData(540,480),v=data.data;
 for(let y=0;y<480;y++)for(let x=0;x<540;x++){
  const tx=(x-270)/177,ty=(240-y)/177,r2=tx*tx+ty*ty,k=1-.7744/Math.max(r2,.0001),bx=tx*k,by=ty*k;
  const rr=((bx-.31)/size)**2+((by-.16)/(size*.64))**2;
  const intensity=Math.exp(-rr*.5)*(.83+.17*Math.cos(Math.atan2(by-.16,bx-.31)*4+Math.sqrt(rr)*5));
  const i=(y*540+x)*4,l=clamp(intensity);v[i]=255;v[i+1]=Math.round(lerp(136,233,l));v[i+2]=Math.round(lerp(58,189,l));v[i+3]=Math.round(Math.pow(l,.69)*255);
 }
 mc.putImageData(data,0,0);
}
function extended(t){
 const u=t-40,sz=lerp(.036,.19,ramp(u,3,9));
 const lx=530,rx=1385,cy=484;
 text('源平面',lx,238,28,C.white,'center');text('观察者的成像平面',rx,238,28,C.white,'center');
 for(const cx of [lx,rx]){line([[cx-292,cy],[cx+292,cy]],'#7b9caf3d',1,[3,7]);line([[cx,cy-205],[cx,cy+221]],'#7b9caf3d',1,[3,7]);}
 const sx=lx+.31*177,sy=cy-.16*177;
 const g=ctx.createRadialGradient(sx,sy,0,sx,sy,sz*177*3.2);g.addColorStop(0,'#ffe7bd');g.addColorStop(.25,'#ffc786db');g.addColorStop(.7,'#ff9b463f');g.addColorStop(1,'#ff9b4600');
 ctx.save();ctx.translate(sx,sy);ctx.scale(1,.64);ctx.fillStyle=g;ctx.translate(-sx,-sy);ctx.fillRect(sx-sz*177*3.3,sy-sz*177*3.3,sz*177*6.6,sz*177*6.6);ctx.restore();
 ring(rx,cy,177*.88,'#74c7df20',[4,8]);mapImage(sz);ctx.drawImage(mappedCanvas,rx-270,cy-240);
 ring(rx,cy,6,C.muted);text('点质量透镜',rx,cy+241,21,C.muted,'center');text(u<3?'一个点光源':'光源逐渐铺开',lx,730,26,C.gold,'center');
 line([[905,474],[1001,474]],'#9bb1c46e',1.5);arrow([945,474],[1001,474],C.blue,14);text('逐点成像',953,437,22,C.muted,'center');
 text('β = θ − θE² θ / |θ|²',953,794,30,C.muted,'center',400,en);
 alpha(ramp(u,8,9),()=>{text('连续的光源 → 连续的弧形像',960,847,27,C.white,'center');});
}

function spaceTime(t){
 if(t<62)return lerp(6,8,ramp(t,54,62));
 if(t<72)return 8+(t-62)/10*6;
 if(t<80)return 14+(t-72)/8*6;
 if(t<86)return 20+(t-80);
 return 26+(t-86)/4*(6-1/30);
}
const projector=new THREE.PerspectiveCamera(42.6,16/9,.05,250);
function worldLabel(p,title,dx,dy,color=C.gold){
 const q=new THREE.Vector3(...p).project(projector);if(q.z<-1||q.z>1)return;
 const x=(q.x*.5+.5)*1920,y=(.5-q.y*.5)*1080,tx=x+dx,ty=y+dy;
 if(tx<110||tx>1640||ty<200||ty>760)return;
 line([[x,y],[tx-15,ty-10],[tx+150,ty-10]],color+'88',1);ring(x,y,3,color);text(title,tx,ty+20,25,color);
}
function spatial(t,state){
 projector.position.fromArray(state.eye);projector.lookAt(0,0,0);projector.updateMatrixWorld();
 if(t<62){alpha(ramp(t,55,56),()=>worldLabel([6.1,0,-2],'吸积盘：热气体',100,-58));}
 if(t>=62&&t<72){const a=ramp(t,62.5,63.4)*(1-ramp(t,71,71.8));alpha(a,()=>{worldLabel(spaceQuality.photon_source,'同一束背面光',-240,-80);worldLabel(spaceQuality.observer_direction_marker,'观察方向',-285,-15,C.blue);});}
 if(t>=76&&t<80)alpha(ramp(t,76,76.7),()=>{line([[992,280],[1180,246],[1490,246]],C.gold+'88',1);text('背面盘面的像',1210,229,27,C.gold);});
}
const CHAPTERS=['光的方向','引力偏折','像的位置','点到亮弧','进入三维','完整成像'];
function hud(t){
 const stage=t<12?0:t<25?1:t<40?2:t<54?3:t<62?4:5;
 const g=ctx.createLinearGradient(0,0,0,194);g.addColorStop(0,'#02070bdb');g.addColorStop(1,'#02070b00');ctx.fillStyle=g;ctx.fillRect(0,0,1920,194);
 text('从一条直线，到黑洞的亮弧',106,66,30,C.white,'left',500);text('LIGHT · GRAVITY · IMAGE',1814,65,18,C.muted,'right',400,en);
 for(let i=0;i<6;i++){const x=106+i*287;const active=i===stage;
  text(String(i+1).padStart(2,'0'),x,115,18,active?C.gold:'#5a7183','left',400,en);text(CHAPTERS[i],x+36,115,21,active?C.white:'#728899');
  line([[x,138],[x+245,138]],active?C.gold+'aa':'#617c8f33',active?2:1);
 }
 const bottom=ctx.createLinearGradient(0,820,0,1080);bottom.addColorStop(0,'#02070b00');bottom.addColorStop(.42,'#02070bcc');bottom.addColorStop(1,'#02070bee');ctx.fillStyle=bottom;ctx.fillRect(0,820,1920,260);
 let main,sub;
 if(t<12){main='眼睛怎样判断，光来自哪里？';sub='从到达方向反向延长；在平直时空里，这条线指回光源。';}
 else if(t<25){main='掠过得越近，偏折通常越明显';sub='保持其他条件相同；弱场公式解释趋势，不用于预测黑洞附近的强场。';}
 else if(t<40){main=t<31?'光沿弯曲路径，抵达观察者':'眼睛看到的方向，指向偏移后的像';sub=t<31?'先跟着真实光路，从光源走到眼睛。':'虚线只是反向延长；光并没有从视位置出发。';}
 else if(t<54){main='从一个光点，到一条亮弧';sub='让光源有面积：每一点都成像，连在一起就形成弧线。';}
 else if(t<62){main='把二维图解，放回三维空间';sub='光源换成吸积盘；黑洞附近的光路需要强场模型。';}
 else if(t<72){main='这一次，光从黑洞背面出发';sub='同样追踪光源、弯曲路径，以及光抵达观察者的方向。';}
 else if(t<80){main='背面盘面的光，看起来在上方';sub='上方的亮弧是背面光源的像；不是另一层发光盘。';}
 else if(t<86){main='换个角度，同一个盘也会变样';sub='光源与光路共同决定，你最终看见的形状。';}
 else{main='引力改变光路，也改变视野';sub='从一条直线，到你看见的宇宙。';}
 text(main,106,927,47,C.white,'left',500);text(sub,108,984,26,C.muted);
 let note=t<12?'平直时空 · 二维图解':t<25?'非旋转轨道示意 · 公式为弱场近似':t<54?'点质量薄透镜 · 教学近似':'非旋转黑洞 · 科学示意';
 text(note,1814,1038,18,C.muted,'right');text('AI 合成旁白',106,1038,17,'#6c8393');
}

function renderAt(seconds){
 const t=clamp(seconds,0,DURATION-1/FPS);let state=null;
 if(t>=52){
  const u=ramp(t,52,62),eye=t<62?[lerp(0,10,u),lerp(33,16,u),lerp(.01,20,u)]:undefined;
  state=drawSpace(spaceTime(t),{typography:false,eye});
 }
 ctx.clearRect(0,0,W,H);ctx.save();ctx.scale(W/1920,H/1080);
 if(t<54){
  ctx.save();
  if(t>=52){const edge=ramp(t,52,54)*1920;ctx.beginPath();ctx.rect(edge,0,1920-edge,1080);ctx.clip();}
  grid(t);if(t<12)straight(t);else if(t<25)bent(t);else if(t<40)apparent(t);else extended(t);
  ctx.restore();
 }
 if(state)alpha(ramp(t,54,54.6),()=>spatial(t,state));
 hud(t);
 if(t>=52&&t<54){const edge=ramp(t,52,54)*1920;line([[edge,173],[edge,820]],C.blue+'99',1.5);text('模型切换：薄透镜图解 → 黑洞强场示意',106,179,23,C.blue);}
 ctx.restore();
 document.getElementById('seek').value=t;document.getElementById('time').textContent=`${String(Math.floor(t/60)).padStart(2,'0')}:${String(Math.floor(t%60)).padStart(2,'0')}`;
 return {t,chapter:t<12?0:t<25?1:t<40?2:t<54?3:t<62?4:5,space:state};
}
window.__film={ready:true,renderAt,duration:DURATION,fps:FPS,quality:{...spaceQuality,timeline:'90-second six-chapter lesson',new_2d:'Straight propagation, orbital deflection, apparent location and point-mass thin-lens extended-source mapping'}};
renderAt(0);
let playing=false,epoch=0,offset=0,audio;
function tick(now){if(!playing)return;const t=offset+(now-epoch)/1000;if(t>=DURATION){playing=false;document.getElementById('play').textContent='播放';audio?.pause();return;}renderAt(t);requestAnimationFrame(tick);}
document.getElementById('play').onclick=()=>{playing=!playing;document.getElementById('play').textContent=playing?'暂停':'播放';if(playing){offset=Number(document.getElementById('seek').value);if(offset>89.8)offset=0;epoch=performance.now();if(!audio)audio=new Audio('/soundtrack.wav');audio.currentTime=offset;audio.play().catch(()=>{});requestAnimationFrame(tick);}else audio?.pause();};
document.getElementById('seek').oninput=e=>{offset=Number(e.target.value);epoch=performance.now();renderAt(offset);if(audio)audio.currentTime=offset;};
