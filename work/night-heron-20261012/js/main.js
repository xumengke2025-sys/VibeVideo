import {makeGL} from '../engine/gl.js';
import {drawPiece} from '../engine/carve.js';
import * as SC from './scene.js';
import {CLOTH} from './scene.js';
import {drawFrame,drawAudience,drawPlaque,buildStage} from './stage.js';
import {clamp,lerp,ss,ease,rng} from './lib.js';

const W=CLOTH.w,H=CLOTH.h;
const cv=document.querySelector('#gl');
// 渲染宽度：?w=540 时用真实 540×960 像素缓冲（不是缩放）
const RW=Number(new URLSearchParams(location.search).get('w')||W);
if([540,1080].includes(RW)&&RW!==W){cv.width=RW;cv.height=RW*16/9}
const S=cv.width/W;                       // 幕布 → 视口的缩放
const GL=makeGL(cv);
const newC=()=>{const c=document.createElement('canvas');c.width=W;c.height=H;return c};
const trc=newC(),gtr=trc.getContext('2d');
const frc=newC(),gfr=frc.getContext('2d');
gtr.lineJoin='round';gtr.lineCap='round';

const DUR=36;
const REEDS=SC.buildReeds(5,9).map((r,i)=>({...r,x:660+i*44+r.dx*.3}));

// 机位（幕布坐标 + 缩放）。竖版构图：树在上，水在下。
function camAt(t){
  const pts=[[0,540,980,1.0],[5,500,930,1.02],[9,360,760,1.12],[14,470,960,1.06],
             [19,600,1400,1.18],[24,610,1450,1.30],[30,600,1460,1.34],[36,540,980,1.0]];
  let i=0;while(i<pts.length-2&&t>pts[i+1][0])i++;
  const a=pts[i],b=pts[i+1],u=ss(0,1,(t-a[0])/(b[0]-a[0]));
  return {x:lerp(a[1],b[1],u),y:lerp(a[2],b[2],u),z:lerp(a[3],b[3],u)};
}
// 灯：一天里的灯数（白天多、夜里只剩一盏）。STYLE.md §3：亮度来自灯数，不加蓝。
function lampCount(t){
  if(t<5)return 9;
  if(t<10)return lerp(9,4.2,ss(5,10,t));
  if(t<16)return lerp(4.2,1.9,ss(10,16,t));
  if(t<31)return lerp(1.9,1.05,ss(16,31,t));
  return lerp(1.05,9,ss(31,36,t));
}
function lampsAt(t){
  const n=lampCount(t),L=[];
  const base=[[540,700,1.30,1.05],[252,1060,.72,1.15],[840,1010,.68,1.15],
              [540,1330,.58,1.2],[300,1620,.44,1.3],[800,1600,.46,1.3],[540,880,1.0,1.0]];
  for(let i=0;i<base.length;i++){
    const lit=clamp(n-i,0,1);
    if(lit<=0.001)continue;
    L.push([base[i][0],base[i][1],base[i][2]*lit,base[i][3]]);
  }
  return L;
}

function render(t){
  const cam=camAt(t);
  const L=lampsAt(t);
  const sum=L.reduce((a,l)=>a+l[2],0)||1;

  // —— 透射层：皮片用 multiply 画上去，重叠自然变暗 ——
  gtr.setTransform(1,0,0,1,0,0);
  gtr.globalCompositeOperation='source-over';
  gtr.fillStyle='#fff';gtr.fillRect(0,0,W,H);
  gtr.globalCompositeOperation='multiply';
  gtr.save();
  gtr.translate(W/2,H/2);gtr.scale(cam.z,cam.z);gtr.translate(-cam.x,-cam.y);
  SC.drawScenery(gtr,{reeds:REEDS});
  gtr.save();gtr.translate(336,SC.BANK_Y+16);drawPiece(gtr,SC.trunk);gtr.restore();
  gtr.save();gtr.translate(336,SC.BANK_Y+16+SC.TREE.cy);drawPiece(gtr,SC.canopy);gtr.restore();
  gtr.restore();
  gtr.globalCompositeOperation='source-over';

  // —— 前景层（预乘 RGBA）：台口木框、观众、牌匾 ——
  gfr.setTransform(1,0,0,1,0,0);
  gfr.clearRect(0,0,W,H);
  const aud=clamp(1-ss(1.2,3.4,t),0,1)*(1-ss(33,35.4,t));
  gfr.save();gfr.translate(W/2,H/2);gfr.scale(cam.z,cam.z);gfr.translate(-cam.x,-cam.y);
  drawFrame(gfr,1);
  gfr.restore();
  if(aud>.001)drawAudience(gfr,aud,t);
  if(t<3.4){const u=ss(0.2,3.2,t);gfr.save();const bl=(1-u)*16;if(bl>0.4)gfr.filter=`blur(${bl.toFixed(1)}px)`;
    drawPlaque(gfr,STG.title,540,620,lerp(1.32,0.72,ease(u)),clamp((t-0.2)/.6,0,1));gfr.restore()}
  if(t>33.6){const u=ss(33.8,35.8,t);gfr.save();const bl=(1-u)*14;if(bl>0.4)gfr.filter=`blur(${bl.toFixed(1)}px)`;
    drawPlaque(gfr,STG.end,540,640,lerp(1.28,0.74,ease(u)),clamp((t-33.6)/.7,0,1));gfr.restore()}

  GL.render(trc,frc,{
    cam:[cam.x*S,cam.y*S,cam.z],rect:[0,0,cv.width,cv.height],
    lamps:L.map(l=>[l[0]*S,l[1]*S,l[2],l[3]]),
    sigB:700*S,sigC:120*S,amb:.22,expo:1.75/Math.sqrt(sum),
    haze:0,time:t,bloom:.34,thr:.74,vign:.42,sat:1.14,contrast:.16,
    lcol:[1,.77,.46],hotcol:[1,.9,.62],bcol:[1,.82,.6],
  });
}

window.render=render;window.DUR=DUR;window.CLOTH=CLOTH;
await document.fonts.ready;
const STG=buildStage();
render(0);
window.READY=true;

const qs=new URLSearchParams(location.search);
if(qs.has('t'))render(parseFloat(qs.get('t')));
if(!qs.has('t')){
  const seek=document.querySelector('#seek'),clock=document.querySelector('#clock'),play=document.querySelector('#play');
  let playing=false,last=0,t=0;
  play.onclick=()=>{playing=!playing};
  seek.oninput=e=>{t=+e.target.value;render(t)};
  function tick(now){if(playing){t=(t+(now-last)/1000)%DUR;render(t);seek.value=t;clock.textContent=t.toFixed(1)}last=now;requestAnimationFrame(tick)}
  requestAnimationFrame(tick);
}
