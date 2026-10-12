import {clamp,ease,lerp,progress,captionAt,validate} from './timeline.mjs';
const plan=await (await fetch('clips/one-way-portrait.json')).json();
const errors=validate(plan);if(errors.length)throw Error(errors.join('\n'));
const W=1080,H=1920,c=document.querySelector('#film'),g=c.getContext('2d');
const white='#e7f1f3',faint='#9abbd1',paperBlue='#174570',cyan='#95e0ee';
const font='"Microsoft YaHei", sans-serif',mono='"Bahnschrift", monospace';
const paper=document.createElement('canvas');paper.width=W;paper.height=H;const p=paper.getContext('2d');
const grad=p.createLinearGradient(0,0,W,H);grad.addColorStop(0,'#163957');grad.addColorStop(.5,'#1a4b76');grad.addColorStop(1,'#0c263e');p.fillStyle=grad;p.fillRect(0,0,W,H);
for(let x=0;x<W;x+=30){p.strokeStyle='rgba(165,205,225,.055)';p.lineWidth=1;p.beginPath();p.moveTo(x,0);p.lineTo(x,H);p.stroke();}for(let y=0;y<H;y+=30){p.beginPath();p.moveTo(0,y);p.lineTo(W,y);p.stroke();}
let seed=1701;for(let i=0;i<5000;i++){seed=(1664525*seed+1013904223)>>>0;let x=seed/4294967296*W;seed=(1664525*seed+1013904223)>>>0;p.fillStyle='rgba(190,220,235,.025)';p.fillRect(x,seed/4294967296*H,1,4);}
function line(points,{color=white,width=3,dash=[],alpha=1,amount=1}={}){if(amount<=0)return;g.save();g.globalAlpha*=alpha;g.strokeStyle=color;g.lineWidth=width;g.setLineDash(dash);g.lineCap='round';g.lineJoin='round';let total=0;const ls=[];for(let i=1;i<points.length;i++){const l=Math.hypot(points[i][0]-points[i-1][0],points[i][1]-points[i-1][1]);ls.push(l);total+=l;}let rem=total*clamp(amount);g.beginPath();g.moveTo(...points[0]);for(let i=1;i<points.length;i++){const f=Math.min(1,rem/(ls[i-1]||1));g.lineTo(lerp(points[i-1][0],points[i][0],f),lerp(points[i-1][1],points[i][1],f));rem-=ls[i-1];if(rem<=0)break;}g.stroke();g.restore();}
function rect(x,y,w,h,o={}){line([[x,y],[x+w,y],[x+w,y+h],[x,y+h],[x,y]],o);}
function text(s,x,y,size=30,color=white,align='left',family=font){g.fillStyle=color;g.textAlign=align;g.font=`${size}px ${family}`;g.fillText(s,x,y);g.textAlign='left';}
function arrow(x,y,dx,dy,color=cyan,width=3){line([[x,y],[x+dx,y+dy]],{color,width});const a=Math.atan2(dy,dx),r=14;line([[x+dx-r*Math.cos(a-.5),y+dy-r*Math.sin(a-.5)],[x+dx,y+dy],[x+dx-r*Math.cos(a+.5),y+dy-r*Math.sin(a+.5)]],{color,width});}
function hatch(x,y,w,h){g.save();g.beginPath();g.rect(x,y,w,h);g.clip();for(let z=-h;z<w+h;z+=14)line([[x+z,y+h],[x+z+h,y]],{color:faint,width:1,alpha:.6});g.restore();}
function block(x,y,w,h){g.fillStyle=paperBlue;g.fillRect(x,y,w,h);hatch(x,y,w,h);rect(x,y,w,h);}
function leader(label,x,y,tx,ty){line([[x-18,y-12],[x-58,y-12],[tx,ty]],{color:faint,width:1.5});g.beginPath();g.arc(tx,ty,4,0,7);g.fillStyle=faint;g.fill();text(label,x,y,30,faint);}
function stateAt(t){return {draw:progress(plan,'draw',t),section:progress(plan,'section',t),ex:progress(plan,'explode',t)*(1-progress(plan,'assemble',t)),opened:progress(plan,'open',t)*(1-progress(plan,'close',t)),settle:progress(plan,'settle',t)};}
function renderAt(t,type='image/png',quality=.96){
 if(!Number.isFinite(t)||t<0||t>15)throw Error('Invalid time');const s=stateAt(t);g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;g.drawImage(paper,0,0);
 rect(55,70,970,1780,{color:faint,width:1,alpha:.5});text('MECHANISM / 01',94,145,28,faint,'left',mono);text('只向一个方向',88,275,76);text('弹簧止回阀',94,340,38,faint);text('轴向剖面 · 原理示意',94,395,25,faint);
 const zoom=1+.035*s.section-.035*s.settle;g.save();g.translate(480,990);g.scale(zoom,zoom);g.translate(-480,-990);
 line([[480,475],[480,1435]],{color:faint,width:1.5,dash:[20,8,4,8],alpha:.55,amount:s.draw});
 const left=300-72*s.ex,right=660+72*s.ex,disc=824+94*s.opened;
 // The reveal travels downward while the centreline and contact remain fixed.
 if(s.section>0){g.save();g.beginPath();g.rect(180,530,720,875*s.section);g.clip();
 block(left,570,40,800);block(right-40,570,40,800);
 // Seat opening 405–555; closed disc touches the seat's lower plane at y=824.
 block(340,800,65,24);block(555,800,65,24);
 g.fillStyle='#225c87';g.fillRect(405,disc,150,18);rect(405,disc,150,18,{width:4});
 line([[480,disc+18],[480,1245]],{width:3});block(440,1245,80,22);
 const a=disc+45,b=1225,sp=[[480,disc+18],[480,a]];for(let i=0;i<=24;i++)sp.push([480+(i===0||i===24?0:(i%2?34:-34)),lerp(a,b,i/24)]);sp.push([480,1245]);line(sp,{width:3});
 if(s.opened>.01){g.save();g.globalAlpha=s.opened;for(const lane of [-1,1]){const path=[[480+lane*30,590],[480+lane*30,770],[480+lane*30,835],[480+lane*95,disc-8],[480+lane*105,disc+40],[480+lane*65,1090],[480+lane*65,1340]];line(path,{color:cyan,width:2,alpha:.25});let lengths=[],length=0;for(let i=1;i<path.length;i++){length+=Math.hypot(path[i][0]-path[i-1][0],path[i][1]-path[i-1][1]);lengths.push(length);}for(let j=0;j<7;j++){let d=((t*.24+j/7)%1)*length;let k=lengths.findIndex(l=>l>=d),before=k?lengths[k-1]:0,u=(d-before)/(lengths[k]-before);const [x,y]=path[k],[xx,yy]=path[k+1],mag=Math.hypot(xx-x,yy-y);arrow(lerp(x,xx,u),lerp(y,yy,u),(xx-x)/mag*22,(yy-y)/mag*22,cyan,2.8);}}g.restore();
 line([[620,824],[695,824],[695,disc],[620,disc]],{color:faint,width:1.5});text('Δx',708,(824+disc)/2+10,28,faint,'left',mono);
 }else if(s.section>.9&&t<6.3){arrow(480,670,0,80,faint,3);}
 if(s.section>.88){leader('阀座',750,755,590,812);leader('阀瓣',750,990,545,disc+8);leader('弹簧',750,1165,510,1150);}
 g.restore();}
 if(s.section<1){g.save();g.beginPath();g.rect(180,530+875*s.section,720,875*(1-s.section));g.clip();g.fillStyle='#19496e';g.fillRect(300,570,360,800);const outline=[[360,570],[600,570],[600,620],[660,680],[660,1260],[600,1320],[600,1370],[360,1370],[360,1320],[300,1260],[300,680],[360,620],[360,570]];line(outline,{width:4,amount:s.draw});for(const y of [680,1260]){line([[300,y],[660,y]],{color:faint,width:2,amount:s.draw});for(const x of [320,640]){g.beginPath();g.arc(x,y+20,8,0,7);g.strokeStyle=faint;g.stroke();}}g.restore();}
 if(s.section>.02&&s.section<.99){const y=530+875*s.section;line([[255,y],[710,y]],{width:2,dash:[8,8]});text('A—A',745,y+8,25,faint,'left',mono);}
 g.restore();
 text('IN',480,510,26,faint,'center',mono);text('OUT',480,1430,26,faint,'center',mono);
 const cap=captionAt(plan,t);rect(94,1500,892,148,{color:faint,width:1,alpha:.6});text('OBSERVATION',122,1540,21,faint,'left',mono);if(cap)text(cap.text,122,1610,48);
 if(s.settle>.2){g.save();g.globalAlpha=ease((s.settle-.2)/.8);rect(700,1690,240,76,{color:'#d38171',width:3});text('CLOSED',820,1741,38,'#dc9b8c','center',mono);g.restore();}
 text('正向压差开启 · 弹簧复位关闭',94,1722,26,faint);text('VIBE VIDEO  /  SCHEMATIC ONLY',94,1810,23,faint,'left',mono);
 return c.toDataURL(type,quality);
}
await document.fonts.ready;window.__film={...plan,width:W,height:H,cuts:plan.connections.map(v=>v.time)};window.stateAt=stateAt;window.renderAt=renderAt;window.ready=true;renderAt(0);
if(!location.search.includes('render')){const start=performance.now();function play(now){renderAt(((now-start)/1000)%15);requestAnimationFrame(play)}requestAnimationFrame(play);}
