// Code-drawn 15s portrait whale demo. All visuals are Canvas 2D drawing; no images.
import {clamp,ease,lerp,progress,captionAt,validate} from './timeline.mjs';
const plan=await (await fetch('clips/whale.json')).json();
const errors=validate(plan);if(errors.length)throw Error(errors.join('\n'));
const canvas=document.getElementById('film'),g=canvas.getContext('2d');
const W=1080,H=1920;
const FONT='"Microsoft YaHei","Noto Sans CJK SC",sans-serif';
const TECH='"Bahnschrift","Consolas",monospace';
const AMBER='224,161,92',CYAN='159,227,255';
function rng(seed){return ()=>{seed|=0;seed=seed+0x6d2b79f5|0;let a=Math.imul(seed^seed>>>15,1|seed);a^=a+Math.imul(a^a>>>7,61|a);return ((a^a>>>14)>>>0)/4294967296;};}
function line(points,{color='#fff',width=2,alpha=1,dash=[]}={}){g.save();g.globalAlpha*=alpha;g.strokeStyle=color;g.lineWidth=width;g.setLineDash(dash);g.lineCap='round';g.lineJoin='round';g.beginPath();g.moveTo(...points[0]);for(let i=1;i<points.length;i++)g.lineTo(points[i][0],points[i][1]);g.stroke();g.restore();}
function text(s,x,y,size=24,color='#fff',align='left',family=FONT,alpha=1,weight=''){g.save();g.globalAlpha*=alpha;g.fillStyle=color;g.font=`${weight}${size}px ${family}`;g.textAlign=align;g.fillText(s,x,y);g.restore();}
function glow(x,y,r,rgb,a){if(a<=0)return;const rg=g.createRadialGradient(x,y,0,x,y,r);rg.addColorStop(0,`rgba(${rgb},${a})`);rg.addColorStop(1,`rgba(${rgb},0)`);g.save();g.globalCompositeOperation='lighter';g.fillStyle=rg;g.fillRect(x-r,y-r,2*r,2*r);g.restore();}
function smoothPath(pts,close){g.beginPath();const n=pts.length,mid=(a,b)=>[(a[0]+b[0])/2,(a[1]+b[1])/2];
 if(close){const m0=mid(pts[n-1],pts[0]);g.moveTo(...m0);for(let i=0;i<n;i++){const p=pts[i],m=mid(p,pts[(i+1)%n]);g.quadraticCurveTo(p[0],p[1],m[0],m[1]);}}
 else{g.moveTo(...pts[0]);for(let i=1;i<n-1;i++){const m=mid(pts[i],pts[i+1]);g.quadraticCurveTo(pts[i][0],pts[i][1],m[0],m[1]);}g.lineTo(...pts[n-1]);}}

// ---------- shared deterministic particle tables ----------
const snowP=(()=>{const r=rng(plan.seed+11),a=[];for(let i=0;i<120;i++)a.push({x:r(),y:r(),z:.2+r()*.8});return a;})();
const streakP=(()=>{const r=rng(plan.seed+31),a=[];for(let i=0;i<150;i++)a.push({ang:r()*Math.PI*2,rad:.65+r()*.55,sp:.75+r()*.5,st:6.85+r()*.9,sz:1+r()*2});return a;})();
const swirlP=(()=>{const r=rng(plan.seed+41),a=[];for(let i=0;i<70;i++)a.push({an:r()*Math.PI*2,rr:.06+r()*.17,w:(.5+r()*.8)*(r()<.5?-1:1)});return a;})();
const jetP=(()=>{const r=rng(plan.seed+51),a=[];for(let i=0;i<140;i++)a.push({side:r()<.5?-1:1,ox:300+r()*150,oy:-60+r()*150,ela:.55+r()*.55,sp:520+r()*430,st:8.35+r()*.95,life:.7+r()*.55,sz:2.6+r()*3.2});return a;})();
const fleeP=(()=>{const r=rng(99),a=[];for(let i=0;i<44;i++)a.push({an:r()*Math.PI*2,sp:180+r()*420,st:5.4+r()*.9,s:1+r()*2});return a;})();

// ---------- environment ----------
function bg(){const grad=g.createLinearGradient(0,0,0,H);
 grad.addColorStop(0,'#061c2e');grad.addColorStop(.45,'#04121e');grad.addColorStop(1,'#01050a');
 g.fillStyle=grad;g.fillRect(0,0,W,H);
 const rg=g.createRadialGradient(W/2,-200,60,W/2,600,1400);rg.addColorStop(0,'rgba(120,190,230,.13)');rg.addColorStop(1,'rgba(120,190,230,0)');
 g.save();g.globalCompositeOperation='lighter';g.fillStyle=rg;g.fillRect(0,0,W,H);g.restore();}
function shafts(t,amp){for(let k=0;k<3;k++){
 const a=Math.max(0,amp*(.05+.04*Math.sin(t*.31+k*2.1)+.03*Math.sin(t*.13+k)));
 const x0=W*(.16+.3*k),w=150+70*k;
 g.save();g.globalCompositeOperation='lighter';
 const lg=g.createLinearGradient(0,0,0,H*.8);lg.addColorStop(0,`rgba(150,210,240,${a})`);lg.addColorStop(1,'rgba(150,210,240,0)');
 g.fillStyle=lg;g.beginPath();g.moveTo(x0,0);g.lineTo(x0+w,0);g.lineTo(x0+w+180,H*.8);g.lineTo(x0-140,H*.8);g.closePath();g.fill();g.restore();}}
function snow(t,dx=0,dy=0){for(const p of snowP){
 let y=(p.y - t*(0.008+p.z*0.02))%1;if(y<0)y+=1;const yy=y*H;
 const x=((p.x + 0.012*Math.sin(t*.4+p.z*9))%1+1)%1*W;
 g.globalAlpha=.06+.22*p.z;g.fillStyle='#cfe8f2';
 g.fillRect(x+dx*p.z, yy+dy*p.z, 1+p.z*1.6, 1+p.z*1.6);}
 g.globalAlpha=1;}
function vignette(){const rg=g.createRadialGradient(W/2,H*.46,300,W/2,H*.5,1250);rg.addColorStop(0,'rgba(0,0,0,0)');rg.addColorStop(1,'rgba(0,0,0,.42)');g.fillStyle=rg;g.fillRect(0,0,W,H);}
function grain(t){const r=rng(plan.seed+Math.floor(t*plan.fps));for(let i=0;i<650;i++){g.fillStyle=i%2?'rgba(210,240,255,.028)':'rgba(0,10,20,.05)';g.fillRect(r()*W,r()*H,1.6,1.6);}}

// ---------- krill (stylized code drawing) ----------
function krill(x,y,s,tt){
 g.save();g.translate(x,y);g.rotate(-0.06+0.04*Math.sin(tt*.6));g.scale(s,s);
 glow(0,-90,430,CYAN,.15);
 const N=10,spine=[];for(let i=0;i<=N;i++){const u=i/N;spine.push([-230+u*460, -170*Math.sin(Math.PI*Math.pow(u,.92))-6*u]);}
 const Wd=u=>30+52*Math.pow(1-u,1.15);
 const top=spine.map(([px,py],i)=>[px,py-Wd(i/N)]);
 const bot=spine.map(([px,py],i)=>[px,py+Wd(i/N)]);
 const bg2=g.createLinearGradient(0,-210,0,20);
 bg2.addColorStop(0,'rgba(220,248,255,.55)');bg2.addColorStop(.55,'rgba(165,225,250,.30)');bg2.addColorStop(1,'rgba(115,185,232,.16)');
 smoothPath([...top,...[...bot].reverse()],true);g.fillStyle=bg2;g.fill();
 g.strokeStyle='rgba(228,251,255,.85)';g.lineWidth=3;g.stroke();
 for(let i=1;i<N;i++){const u=i/N;const [px,py]=spine[i];line([[px,py-Wd(u)+4],[px,py+Wd(u)-4]],{color:'rgba(205,242,255,.30)',width:2.2});}
 const [tx,ty]=spine[N];
 for(let k=-2;k<=2;k++){line([[tx,ty],[tx+66,ty-14+k*20]],{color:'rgba(210,244,255,.6)',width:2.6});}
 const [hx,hy]=spine[0];
 g.fillStyle='rgba(208,244,254,.42)';g.strokeStyle='rgba(228,251,255,.9)';g.lineWidth=3;
 g.beginPath();g.ellipse(hx-14,hy+4,60,48,-.28,0,Math.PI*2);g.fill();g.stroke();
 line([[hx-60,hy-26],[hx-122,hy-58]],{color:'rgba(228,251,255,.8)',width:3});
 g.fillStyle='#0a1a24';g.beginPath();g.arc(hx-34,hy-8,14,0,Math.PI*2);g.fill();
 g.fillStyle='rgba(235,252,255,.95)';g.beginPath();g.arc(hx-39,hy-13,5,0,Math.PI*2);g.fill();
 g.beginPath();g.arc(hx-29,hy-2,2.2,0,Math.PI*2);g.fill();
 const sw=Math.sin(tt*2.0)*22;
 line([[hx-52,hy-30],[hx-138,hy-92-sw],[hx-224,hy-100-sw*1.4],[hx-300,hy-132-sw*1.7]],{color:'rgba(208,245,255,.6)',width:2.4});
 line([[hx-46,hy-16],[hx-146,hy-56+sw*.5],[hx-240,hy-70+sw],[hx-320,hy-60+sw*1.3]],{color:'rgba(208,245,255,.5)',width:2.1});
 for(let i=0;i<6;i++){const u=.22+i*.1,idx=Math.round(u*N),[px,py]=spine[idx],kick=Math.sin(tt*3.1+i)*7;
  const lx=px-10,ly=py+Wd(u)-6;
  line([[lx,ly],[lx-12,ly+30+kick]],{color:'rgba(205,242,255,.6)',width:2.2});
  line([[lx-4,ly+12],[lx-19,ly+20+kick*.6]],{color:'rgba(205,242,255,.42)',width:1.6});
  line([[lx-8,ly+22],[lx-23,ly+32+kick*.6]],{color:'rgba(205,242,255,.36)',width:1.6});}
 g.restore();}

// ---------- whale maw (front view, jaw opens with `open` 0..1) ----------
function maw(open,cx,cy,s,tt,alpha){
 g.save();g.globalAlpha*=alpha;g.translate(cx,cy);g.scale(s,s);
 const MW=460,UHT=570,drop=44+open*190;
 const roofY=x=>{const u=Math.abs(x)/MW;return -(34+118*(1-u*u));};
 const topY=x=>{const u=Math.abs(x)/MW;return -(270+300*(1-u*u));};
 const floorY=x=>{const u=Math.abs(x)/MW;return 30+(drop-30)*(1-u*u);};
 const botY=x=>{const u=Math.abs(x)/MW;return floorY(x)+190+330*(1-u*u);};
 const S=[];for(let x=-MW;x<=MW+1;x+=46)S.push(x);
 const R=S.map(x=>[x,roofY(x)]),T=S.map(x=>[x,topY(x)]),F=S.map(x=>[x,floorY(x)]),B=S.map(x=>[x,botY(x)]);
 // interior darkness
 smoothPath([...R,...[...F].reverse()],true);
 let rg=g.createRadialGradient(0,(roofY(0)+floorY(0))/2,20,0,(roofY(0)+floorY(0))/2,470);
 rg.addColorStop(0,'#1e4668');rg.addColorStop(.6,'#0a1a2b');rg.addColorStop(1,'#000');
 g.fillStyle=rg;g.fill();
 // throat (lower jaw + pleats)
 smoothPath([...F,...[...B].reverse()],true);
 rg=g.createRadialGradient(0,floorY(0)+80,30,0,floorY(0)+140,700);
 rg.addColorStop(0,'#0f2a40');rg.addColorStop(1,'#041018');
 g.fillStyle=rg;g.fill();
 line(F,{color:'rgba(160,215,245,.30)',width:3});
 for(let j=-4;j<=4;j++){const xj=j*88;line([[xj,floorY(xj)+10],[xj*.82,botY(xj*.82)-16]],{color:'rgba(150,192,220,.26)',width:6});}
 line([[0,floorY(0)+12],[0,botY(0)-22]],{color:'rgba(180,220,245,.16)',width:7});
 // upper jaw
 smoothPath([...T,...[...R].reverse()],true);
 rg=g.createLinearGradient(0,-UHT,0,-20);rg.addColorStop(0,'#0e2a3f');rg.addColorStop(1,'#051321');
 g.fillStyle=rg;g.fill();
 // under-roof shadow band + baleen
 line(R,{color:'rgba(0,0,0,.35)',width:56});
 for(let i=0;i<30;i++){const x=-MW+24+i*(MW*2-48)/29;const len=132+36*Math.sin(i*1.7+tt*.4);
  line([[x,roofY(x)+12],[x+6*Math.sin(i*2.3+tt*.6),roofY(x)+12+len]],{color:'rgba(205,220,232,.62)',width:4});}
 line(R,{color:'rgba(150,210,245,.30)',width:3});glow(0,roofY(0)+40,360,CYAN,.18);
 // head rim light + crown
 smoothPath(T,false);
 rg=g.createLinearGradient(0,-UHT-10,0,-140);rg.addColorStop(0,'rgba(190,232,255,.75)');rg.addColorStop(1,'rgba(190,232,255,0)');
 g.strokeStyle=rg;g.lineWidth=3.5;g.stroke();
 glow(0,-520,380,'170,220,250',.16);
 // side edges, corners, eyes, pectoral fins
 for(const sd of [-1,1]){line([[sd*MW,-270],[sd*MW,-34]],{color:'rgba(170,215,245,.40)',width:2});
  glow(sd*MW,0,120,CYAN,.30);
  g.save();g.translate(sd*400,-180);g.rotate(sd*.25);
  g.fillStyle='#020a12';g.beginPath();g.ellipse(0,0,26,16,0,0,Math.PI*2);g.fill();
  g.strokeStyle='rgba(220,245,255,.5)';g.lineWidth=2.4;g.beginPath();g.ellipse(0,-4,22,12,0,Math.PI*1.15,Math.PI*1.85);g.stroke();g.restore();
  glow(sd*400,-180,70,CYAN,.12);
  const fin=[[sd*466,40],[sd*560,170],[sd*648,318],[sd*700,432],[sd*658,392],[sd*548,210],[sd*486,96]];
  smoothPath(fin,true);g.fillStyle='#061527';g.fill();
  g.strokeStyle='rgba(175,222,252,.38)';g.lineWidth=2.5;g.stroke();}
 g.restore();}

// ---------- whale full profile ----------
function whaleProfile(t,cx,cy,L,alpha){
 g.save();g.globalAlpha*=alpha;g.translate(cx,cy);g.rotate(-0.035);
 const sway=Math.sin(t*.72);
 const ptsUp=[[.50,.00],[.455,-.050],[.38,-.082],[.27,-.100],[.15,-.104],[.03,-.088],[-.10,-.058],[-.24,-.020],[-.285,-.038],[-.34,-.030],[-.42,.004],[-.475,.020],[-.50,.010]];
 const ptsLo=[[-.50,.020],[-.40,.030],[-.27,.036],[-.14,.048],[.00,.062],[.14,.078],[.27,.086],[.37,.074],[.45,.046],[.50,.000]];
 const u=x=>0.5-x/L, wave=x=>Math.sin(t*.72-u(x)*3.4)*24*Math.pow(Math.max(0,(u(x)-.55)/.45),2);
 const X=p=>p[0]*L, Y=p=>p[1]*L+wave(p[0]*L);
 smoothPath([...ptsUp.map(p=>[X(p),Y(p)]),...ptsLo.map(p=>[X(p),Y(p)])],true);
 const bg3=g.createLinearGradient(0,-.10*L,0,.10*L);bg3.addColorStop(0,'#0b2438');bg3.addColorStop(.55,'#061527');bg3.addColorStop(1,'#030d18');
 g.fillStyle=bg3;g.fill();
 smoothPath(ptsUp.map(p=>[X(p),Y(p)]),false);
 const rg=g.createLinearGradient(0,-.12*L,0,.02*L);rg.addColorStop(0,'rgba(185,228,255,.7)');rg.addColorStop(1,'rgba(185,228,255,0)');
 g.strokeStyle=rg;g.lineWidth=3;g.stroke();
 g.save();g.translate(-.485*L,.012*L);g.rotate(sway*.08);
 g.beginPath();g.moveTo(0,-2);g.quadraticCurveTo(-.06*L,-.06*L,-.145*L,-.085*L);g.quadraticCurveTo(-.095*L,-.03*L,-.02*L,-.006*L);g.closePath();
 g.fillStyle='#061527';g.fill();g.strokeStyle='rgba(175,222,252,.4)';g.lineWidth=2;g.stroke();
 g.beginPath();g.moveTo(0,4);g.quadraticCurveTo(-.06*L,.06*L,-.145*L,.095*L);g.quadraticCurveTo(-.095*L,.035*L,-.02*L,.01*L);g.closePath();
 g.fillStyle='#061527';g.fill();g.strokeStyle='rgba(175,222,252,.32)';g.lineWidth=2;g.stroke();g.restore();
 g.beginPath();g.moveTo(.30*L,.012*L);g.quadraticCurveTo(.19*L,.11*L,.05*L,.155*L);g.quadraticCurveTo(.02*L,.135*L,.13*L,.075*L);g.quadraticCurveTo(.22*L,.03*L,.30*L,.012*L);g.closePath();
 g.fillStyle='#061527';g.fill();g.strokeStyle='rgba(175,222,252,.35)';g.lineWidth=2;g.stroke();
 g.strokeStyle='rgba(160,208,238,.30)';g.lineWidth=2.2;g.beginPath();g.moveTo(.50*L,.004*L);g.quadraticCurveTo(.40*L,.052*L,.34*L,.056*L);g.stroke();
 const belly=g.createRadialGradient(.30*L,.05*L,10,.30*L,.05*L,.30*L);belly.addColorStop(0,'rgba(140,200,240,.10)');belly.addColorStop(1,'rgba(140,200,240,0)');
 g.fillStyle=belly;g.fillRect(0,-.05*L,.6*L,.25*L);
 g.fillStyle='rgba(215,240,252,.75)';g.beginPath();g.arc(.455*L,-.014*L,7,0,Math.PI*2);g.fill();
 g.restore();}

// ---------- flow systems ----------
function streaks(t,cx,cy,rr,alpha){for(const p of streakP){
 const u=(t-p.st)/1.5;if(u<=0||u>=1)continue;
 const r=(1-ease(u))*rr*p.rad+50;
 const x=cx+Math.cos(p.ang)*r, y=cy+Math.sin(p.ang)*r*.78;
 const r2=r-26*u*p.sp-16;
 const x2=cx+Math.cos(p.ang)*r2, y2=cy+Math.sin(p.ang)*r2*.78;
 g.strokeStyle=`rgba(190,235,255,${alpha*(0.9-0.5*u)})`;g.lineWidth=p.sz;
 g.beginPath();g.moveTo(x,y);g.lineTo(x2,y2);g.stroke();}}
function swirl(t,cx,cy,rr,alpha){for(const p of swirlP){
 const an=p.an+t*p.w, r=rr*(0.25+0.85*p.rr/0.23)*0.5;
 const x=cx+Math.cos(an)*r, y=cy+Math.sin(an)*r*.72;
 const a2=an-p.w*.12, x2=cx+Math.cos(a2)*r, y2=cy+Math.sin(a2)*r*.72;
 const a=alpha*(0.3+0.6*p.rr/0.23)*0.9;
 g.strokeStyle=`rgba(185,232,255,${Math.min(a,.5)})`;g.lineWidth=1.7;
 g.beginPath();g.moveTo(x,y);g.lineTo(x2,y2);g.stroke();}}
function jets(t,cx,cy,s,alpha){for(const p of jetP){
 const u=t-p.st;if(u<=0||u>p.life)continue;
 const k=u/p.life, sp=p.sp*(1-k*.3);
 const x0=cx+p.side*p.ox, y0=cy+p.oy;
 const x=x0+p.side*Math.cos(p.ela)*sp*u, y=y0-Math.sin(p.ela)*sp*u+.5*560*u*u;
 if(x<-40||x>W+40||y<-40||y>H+40)continue;
 const a=alpha*(1-k)*(.8+.2*Math.sin(k*6+p.ox));
 g.fillStyle=`rgba(200,238,252,${a})`;g.beginPath();g.arc(x,y,p.sz*(1-k*.35),0,Math.PI*2);g.fill();
 const tx=x-p.side*Math.cos(p.ela)*sp*.05, ty=y+Math.sin(p.ela)*sp*.05;
 g.strokeStyle=`rgba(200,238,252,${a*.6})`;g.lineWidth=p.sz*.8;g.beginPath();g.moveTo(x,y);g.lineTo(tx,ty);g.stroke();}}
function veils(t,cx,cy,s,alpha){if(alpha<=0)return;const pulse=.8+.2*Math.sin(t*5.0);
 for(const dir of [[-1,-1],[-1,1],[1,-1],[1,1]]){
  const sx=dir[0],sy=dir[1],a=alpha*.09*pulse;
  const gx0=cx+sx*150, gy0=cy+sy*110, gx1=cx+sx*1020, gy1=cy+sy*640;
  const lg=g.createLinearGradient(gx0,gy0,gx1,gy1);lg.addColorStop(0,`rgba(200,238,252,${a})`);lg.addColorStop(1,'rgba(200,238,252,0)');
  g.fillStyle=lg;g.beginPath();
  g.moveTo(gx0,gy0-40);g.lineTo(cx+sx*900,gy1-150);g.lineTo(cx+sx*980,gy1+120);g.lineTo(gx0,gy0+70);g.closePath();g.fill();}}
function ring(cx,cy,t0,t,a){const rr=ease(clamp((t-t0)/2.6));if(rr<=0)return;
 const r=120+rr*1500,al=a*(1-rr)*1.25;
 g.save();g.strokeStyle=`rgba(180,226,255,${al})`;g.lineWidth=3-1.8*rr;
 g.beginPath();g.ellipse(cx,cy,r,r*.72,0,0,Math.PI*2);g.stroke();g.restore();}

// ---------- scenes ----------
function scene1(t){
 g.fillStyle='rgba(0,0,0,.34)';g.fillRect(0,0,W,H);
 shafts(t,.8);
 const shake=(t>2.6&&t<3.3)?7*Math.exp(-(t-2.6)*5)*Math.sin((t-2.6)*46):0;
 snow(t,0,shake*.5);
 for(const q of [[250,1440,70],[840,420,52],[880,1560,58]]) glow(q[0]+shake,q[1]+shake,q[2],CYAN,.05);
 const push=1+.10*ease(clamp(t/3.4));
 g.save();g.translate(615+shake*1.4,950+shake);g.scale(push,push);krill(0,0,1.0,t);g.restore();
 const eg=t-2.75;
 if(eg>0&&eg<0.62){const k=eg/.62,a=k<.15?k/.15:Math.max(0,1-ease((k-.45)/.55)),sc=k<.15?ease(k/.15):1;
  glow(600+shake*2,700+shake,90,AMBER,.25*a);
  g.save();g.translate(600+shake*2,700+shake);g.rotate(.1);g.scale(sc,sc);g.globalAlpha=a;
  g.fillStyle='rgb(224,161,92)';g.beginPath();g.roundRect(-9,-58,18,40,9);g.fill();
  g.beginPath();g.arc(0,8,10,0,Math.PI*2);g.fill();g.restore();g.globalAlpha=1;}}
function scene2(t){
 const r=progress(plan,'rise',t);
 shafts(t,.85*(1-r*.45));
 snow(t);
 for(const p of fleeP){const u=t-p.st;if(u<0||u>1.1)continue;
  const rad=u*p.sp;const fx=540+Math.cos(p.an)*rad, fy=1150+Math.sin(p.an)*rad*.8;
  g.globalAlpha=(1-u/1.1)*.5;g.fillStyle='#bfe4f4';g.fillRect(fx,fy,p.s,p.s);}
 g.globalAlpha=1;
 const appr=ease(clamp((t-6.2)/.55));
 const sc2=(0.62+0.36*ease(r))*(1+.10*appr), cy2=2250-(2250-1250)*ease(r)+70*appr, open2=.05+.38*r;
 maw(open2,540+18*Math.sin(t*.6),cy2,sc2,t,1);}
function stampDraw(){
 const w=380,h=210;
 g.strokeStyle='rgba(224,161,92,.95)';g.lineWidth=8;g.strokeRect(-w/2,-h/2,w,h);
 g.lineWidth=2.5;g.strokeRect(-w/2+14,-h/2+14,w-28,h-28);
 g.fillStyle='rgba(224,161,92,.98)';g.font=`700 66px ${FONT}`;g.textAlign='center';g.fillText('只留虾',-10,26);
 g.strokeStyle='rgba(224,161,92,.95)';g.lineWidth=9;g.beginPath();g.moveTo(104,-48);g.lineTo(128,-20);g.lineTo(172,-84);g.stroke();g.textAlign='left';
 const r=rng(7);for(let i=0;i<220;i++){g.fillStyle=`rgba(0,0,0,${.05+r()*.06})`;g.fillRect(-w/2+r()*w,-h/2+r()*h,2.5,2.5);}}
function scene3(t){
 const g1=progress(plan,'engulf',t), f=progress(plan,'filter',t);
 const ex=1-ease(clamp((t-10.45)/.25));
 shafts(t,.55);snow(t);
 const open=.95-.45*g1-.10*f, cx=540, cy=1330+g1*36+(1-ex)*300, s=1.85*(0.72+0.28*ex);
 maw(open,cx,cy,s,t,ex);
 const pulse=(t>6.9&&t<8.6)?Math.max(0,Math.sin((t-6.9)/1.7*Math.PI)):0;
 if(pulse>0)glow(cx,cy+150,520,CYAN,.16*pulse*ex);
 streaks(t,cx,cy+120,820,1.0*ex);
 const sa=ease(clamp((t-8.25)/1));
 swirl(t,cx,cy+140*s*.5,860*sa,.62*sa*ex);
 jets(t,cx,cy,s,1.0*f*ex);
 veils(t,cx,cy,s,f*ex);
 if(f>0&&ex>0){line([[cx-460*s,cy-100*s],[cx+460*s,cy-100*s]],{color:`rgba(190,235,255,${.18*f*ex*(0.6+0.4*Math.sin(t*7))})`,width:6,alpha:1});}
 const eg=t-9.75;
 if(eg>0&&eg<0.75){const k=eg/.75,pop=k<.18?ease(k/.18):1,a=k<.14?k/.14:Math.max(0,1-ease((k-.6)/.4));
  g.save();g.translate(540,500);g.rotate(-.12+.02*Math.sin(k*9));g.scale(pop,pop);g.globalAlpha=Math.max(0,a);
  stampDraw();g.restore();g.globalAlpha=1;}}
function scene4(t){
 shafts(t,.45);snow(t);
 const tt=t-10.6;
 const cx=540+(tt-2.2)*14, cy=1180, s=lerp(1.06,1.0,ease(clamp(tt/1.2)));
 g.save();g.globalAlpha=ease(clamp(tt/.9));
 const pa=(t>11.6&&t<12.6)?.32*Math.exp(-(t-11.6)*3.2):0;
 if(pa>0){glow(cx+40,cy+10,420,CYAN,pa);
  g.strokeStyle=`rgba(190,235,255,${pa*.8})`;g.lineWidth=3;
  g.beginPath();g.arc(cx+40,cy+10,90+(t-11.6)*220,0,Math.PI*2);g.stroke();}
 whaleProfile(t,cx,cy,850*s,.98);
 g.restore();
 ring(cx+40,cy+10,12.3,t,.5);ring(cx+40,cy+10,12.85,t,.4);ring(cx+40,cy+10,13.4,t,.32);
 // slow heart monitor
 const ekgA=clamp((t-11.6)/.4)*(1-ease(clamp((t-14.0)/.5))); 
 if(ekgA>0){g.save();g.globalAlpha=ekgA*.85;g.strokeStyle='rgba(190,235,255,.8)';g.lineWidth=2.5;
  g.beginPath();g.moveTo(110,1000);g.lineTo(129,1000);g.lineTo(145,962);g.lineTo(161,1022);g.lineTo(177,1000);g.lineTo(350,1000);g.stroke();
  const fx=110+((t-11.5)/.8)*240;if(fx>=110&&fx<=350){g.fillStyle='rgba(220,245,255,.95)';g.beginPath();g.arc(fx,1000,5,0,Math.PI*2);g.fill();}
  text('2 BPM',110,1046,24,'rgba(210,245,255,.85)','left',TECH);g.restore();}
 // call annotation
 const a2=t>12.9?clamp((t-12.9)/.4,0,1)*(1-ease(clamp((t-14.5)/.45))):0;
 if(a2>0){g.globalAlpha=a2;
  line([[700,556],[560,600]],{color:'rgba(180,225,250,.4)',width:1.5});
  text('歌声，最远 1600 公里',660,540,26,'rgba(210,245,255,.85)','left',TECH);g.globalAlpha=1;}}

// ---------- overlays ----------
function darkLevel(t){
 const seg=(a,b,va,vb)=>va+(vb-va)*ease(clamp((t-a)/(b-a)));
 if(t<3.3)return .30;
 if(t<3.8)return seg(3.3,3.8,.30,.90);
 if(t<4.6)return seg(3.8,4.6,.90,.22);
 if(t<6.25)return .22;
 if(t<6.8)return seg(6.25,6.8,.22,.945);
 if(t<7.15)return seg(6.8,7.15,.945,.42);
 if(t<10.45)return .30+.04*Math.sin(t*2.3);
 if(t<10.95)return seg(10.45,10.95,.30,.22);
 return seg(10.95,12.5,.22,.10);}
function hud(t){
 const dv=t<3.4?lerp(150,170,t/3.4):t<6.8?lerp(170,205,(t-3.4)/3.4):t<10.6?lerp(205,225,(t-6.8)/3.8):lerp(225,240,(t-10.6)/4.4);
 g.globalAlpha=.55;
 text('DEPTH',64,84,20,'rgba(170,215,235,1)','left',TECH);
 text('−'+Math.round(dv)+' m',64,116,24,'rgba(210,245,255,1)','left',TECH);
 line([[64,132],[160,132]],{color:'rgba(170,215,235,.5)',width:1});
 g.globalAlpha=1;}
function captions(t){const cap=captionAt(plan,t);if(!cap)return;
 const a=Math.max(0,Math.min(1,(t-cap.start)/.16,(cap.end-t)/.16));
 g.save();g.globalAlpha=a;g.textAlign='center';
 g.font=`600 46px ${FONT}`;
 g.fillStyle='rgba(2,10,18,.85)';g.fillText(cap.text,542,1714);
 g.fillStyle='rgba(233,245,251,.96)';g.fillText(cap.text,540,1712);
 g.fillStyle='rgba(159,227,255,.7)';g.fillRect(540-26,1742,52,5);
 g.restore();g.textAlign='left';}
function footer(t){const a=clamp((t-13.4)/.6,0,1);if(a<=0)return;
 g.globalAlpha=.5*a;
 text('原创代码演示 · 数据：NOAA / PNAS 2019 / Stanford 2016 / BAS · 深度与速度为示意',64,1852,20,'rgba(200,235,250,1)');
 g.globalAlpha=1;}

function frame(t){
 bg();
 if(t<3.5)scene1(t);
 if(t>=3.4&&t<6.9)scene2(t);
 if(t>=6.8&&t<10.7)scene3(t);
 if(t>=10.6)scene4(t);
 g.fillStyle=`rgba(1,5,10,${darkLevel(t)})`;g.fillRect(0,0,W,H);
 vignette();grain(t);hud(t);captions(t);footer(t);}

window.__film={duration:plan.duration,fps:plan.fps,width:W,height:H,cuts:[],continuousCuts:[3.4,6.8,10.6],holdStart:13.6};
window.__plan=plan;
window.renderAt=(t,type='image/png',quality=.95)=>{
 if(!Number.isFinite(t)||t<0||t>plan.duration)throw Error('Out-of-range time');
 g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;g.setLineDash([]);g.clearRect(0,0,W,H);
 frame(t);return canvas.toDataURL(type,quality);};
await document.fonts.ready;window.ready=true;window.renderAt(0);
// Wall time is used only in the optional preview, never by renderAt.
if(!new URLSearchParams(location.search).has('render')){const start=performance.now();function play(now){window.renderAt(((now-start)/1000)%plan.duration);requestAnimationFrame(play);}requestAnimationFrame(play);}
