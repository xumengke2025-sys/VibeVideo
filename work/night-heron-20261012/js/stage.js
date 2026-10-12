// 竖版（1080×1920）台口：漆木框 + 横楣雕花 + 立柱 + 内沿受光；前排小观众；前景立柱转场；镂空皮影牌。
// 坐标全部在幕布坐标系（1080×1920），调用方负责施加相机变换。
import {piece,drawPiece,fill,cut,cutLine,ink,within,smooth,cloud,beads,coin,meander,DYE} from '../engine/carve.js';
import {clamp,lerp} from './lib.js';

export const FR={top:-430,left:-320,right:1400,bot:2360,w:1080,h:1920};

export function drawFrame(g,spill=1){
  const lac='#2a0d08',lac2='#46140c',gold='#8a6430';
  // 横楣（幕布上方）
  g.fillStyle=lac;g.fillRect(FR.left,FR.top,FR.right-FR.left,-FR.top+20);
  g.fillStyle=lac2;g.fillRect(FR.left+60,FR.top+230,FR.right-FR.left-120,140);
  g.strokeStyle=gold;g.lineWidth=3;
  for(let x=FR.left+90;x<FR.right-120;x+=126){
    g.beginPath();
    for(let i=0;i<=30;i++){const a=i/30*Math.PI*2.1,r=34*(1-i/30*.75),px=x+60+Math.cos(a)*r,py=FR.top+175+Math.sin(a)*r*.7;
      if(i)g.lineTo(px,py);else g.moveTo(px,py)}
    g.stroke();
  }
  g.beginPath();g.moveTo(FR.left+60,FR.top+230);g.lineTo(FR.right-60,FR.top+230);
  g.moveTo(FR.left+60,FR.top+370);g.lineTo(FR.right-60,FR.top+370);g.stroke();
  g.fillStyle='#6a1a10';g.fillRect(FR.left+60,FR.top+370,FR.right-FR.left-120,30);
  // 立柱
  for(const x of[FR.left,1080]){
    const gr=g.createLinearGradient(x,0,x+320,0);
    gr.addColorStop(0,'#1a0806');gr.addColorStop(.5,'#3e110a');gr.addColorStop(1,'#1a0806');
    g.fillStyle=gr;g.fillRect(x,FR.top,320,FR.bot-FR.top);
    g.strokeStyle=gold;g.lineWidth=2.5;g.strokeRect(x+34,60,252,1760);
  }
  // 台口（幕布下方）
  g.fillStyle=lac;g.fillRect(FR.left,1920,FR.right-FR.left,FR.bot-1920);
  g.fillStyle='#5a170d';g.fillRect(FR.left+60,1920,FR.right-FR.left-120,46);
  g.strokeStyle=gold;g.lineWidth=2.5;g.beginPath();g.moveTo(FR.left+60,1966);g.lineTo(FR.right-60,1966);g.stroke();
  // 布透出的暖光打在木框内沿
  g.globalCompositeOperation='lighter';
  const sp=(x0,y0,x1,y1,gx0,gy0,gx1,gy1)=>{
    const gr=g.createLinearGradient(gx0,gy0,gx1,gy1);
    gr.addColorStop(0,`rgba(255,170,90,${.34*spill})`);gr.addColorStop(1,'rgba(255,150,70,0)');
    g.fillStyle=gr;g.fillRect(x0,y0,x1-x0,y1-y0);
  };
  sp(0,-120,1080,0,0,0,0,-120);
  sp(0,1920,1080,2040,0,1920,0,2040);
  sp(-180,0,0,1920,0,0,-180,0);
  sp(1080,0,1260,1920,1080,0,1260,0);
  g.globalCompositeOperation='source-over';
}

// 前排小观众（幕布坐标，坐在台口下方）
export function drawAudience(g,a=1,t=0){
  if(a<=0)return;
  g.save();g.globalAlpha=a;g.fillStyle='#080404';g.filter='blur(4px)';
  const heads=[[170,1620,72,1],[400,1652,86,0],[650,1668,70,1],[900,1644,80,0],[1050,1672,66,1]];
  heads.forEach(([x,y,r,bun],i)=>{
    const bob=Math.sin(t*1.25+i*2.1)*4;
    g.beginPath();g.ellipse(x,y+bob,r*.8,r,0,0,7);g.fill();
    g.beginPath();g.ellipse(x,y+r*1.3+bob,r*1.9,r*.95,0,0,7);g.fill();
    if(bun){g.beginPath();g.arc(x+r*.12,y-r*.96+bob,r*.33,0,7);g.fill()}
  });
  g.restore();
}

// 前景立柱（转场遮挡）：x = 立柱中心（幕布坐标）
export function drawPillar(g,x){
  g.save();g.filter='blur(16px)';
  const w=900,gr=g.createLinearGradient(x-w/2,0,x+w/2,0);
  gr.addColorStop(0,'rgba(12,4,3,0)');gr.addColorStop(.08,'#120604');gr.addColorStop(.45,'#3a1009');
  gr.addColorStop(.55,'#2a0b07');gr.addColorStop(.92,'#0e0503');gr.addColorStop(1,'rgba(12,4,3,0)');
  g.fillStyle=gr;g.fillRect(x-w/2,-60,w,2100);
  g.globalCompositeOperation='lighter';
  const rg=g.createLinearGradient(x-w/2,0,x-w/2+180,0);
  rg.addColorStop(0,'rgba(255,160,80,0)');rg.addColorStop(.6,'rgba(255,160,80,.17)');rg.addColorStop(1,'rgba(255,160,80,0)');
  g.fillStyle=rg;g.fillRect(x-w/2,-60,220,2100);
  g.restore();
}

// 镂空皮影牌（片名 / 片尾）
function plaque(w,h,lines,seal,seed){
  return piece([-w/2-30,-h/2-30,w/2+30,h/2+30],g=>{
    const outer=q=>{const r=26;q.moveTo(-w/2+r,-h/2);q.lineTo(w/2-r,-h/2);q.quadraticCurveTo(w/2+14,-h/2-14,w/2,-h/2+r);
      q.lineTo(w/2,h/2-r);q.quadraticCurveTo(w/2+14,h/2+14,w/2-r,h/2);q.lineTo(-w/2+r,h/2);
      q.quadraticCurveTo(-w/2-14,h/2+14,-w/2,h/2-r);q.lineTo(-w/2,-h/2+r);q.quadraticCurveTo(-w/2-14,-h/2-14,-w/2+r,-h/2);q.closePath()};
    fill(g,'#3a1a10',outer);
    const band=q=>{outer(q);q.rect(-w/2+26,-h/2+26,w-52,h-52)};
    fill(g,DYE.red,band);
    within(g,band,()=>{
      meander(g,-w/2+30,-h/2+20,w/2-30,5,1.6);meander(g,-w/2+30,h/2-7,w/2-30,5,1.6);
      for(let y=-h/2+42;y<h/2-30;y+=22){coin(g,-w/2+13,y,6);coin(g,w/2-13,y,6)}
    });
    for(const[x,y]of[[-w/2+13,-h/2+13],[w/2-13,-h/2+13],[-w/2+13,h/2-13],[w/2-13,h/2-13]]){
      fill(g,DYE.green,q=>q.arc(x,y,20,0,7));cloud(g,x,y,12,0,2,1);ink(g,2,q=>q.arc(x,y,20,0,7));
    }
    ink(g,2.5,outer);ink(g,1.8,q=>q.rect(-w/2+26,-h/2+26,w-52,h-52));
    g.save();g.globalCompositeOperation='destination-out';g.fillStyle='#000';
    g.textAlign='center';g.textBaseline='middle';
    for(const L of lines){g.font=L.font;g.letterSpacing=(L.ls||0)+'px';g.fillText(L.text,L.x||0,L.y)}
    g.restore();
    for(const L of lines)if(L.bars)for(let k=0;k<L.bars;k++){
      const x=-w/2+60+(k+.5)*(w-120)/L.bars;
      ink(g,2.4,q=>{q.moveTo(x,L.y-L.size*.45);q.lineTo(x+6,L.y+L.size*.45)},'#3a1a10');
    }
    if(seal)for(let k=0;k<2;k++){
      const sx=w/2-152,sy=-h/2+52+k*0;
      fill(g,'#b3261b',q=>q.rect(sx,sy,92,92));
      g.save();g.globalCompositeOperation='destination-out';g.fillStyle='#000';
      g.font='400 40px "Ma Shan Zheng"';g.textAlign='center';g.textBaseline='middle';
      g.fillText('夜',sx+46,sy+28);g.fillText('鹭',sx+46,sy+70);g.restore();
      ink(g,2,q=>q.rect(sx,sy,92,92));
    }
  },{ss:2,seed:60+(seed||0)});
}
let P=null;
export function buildStage(){
  if(P)return P;
  P={
    title:plaque(940,420,[
      {text:'夜鹭的一天',font:'700 132px "STXingkai","KaiTi","STKaiti",serif',y:-46,size:132},
      {text:'从黄昏开始',font:'600 66px "KaiTi","STKaiti",serif',y:76,size:66,ls:6}],1,1),
    end:plaque(940,440,[
      {text:'皮影戏',font:'700 104px "STXingkai","KaiTi","STKaiti",serif',y:-70,size:104,ls:14},
      {text:'夜鹭的一天，从黄昏开始',font:'600 54px "KaiTi","STKaiti",serif',y:42,size:54,ls:4}],0,0)
  };
  return P;
}
export function drawPlaque(g,p,x,y,s,a=1){
  g.save();g.globalAlpha=a;g.translate(x,y);g.scale(s,s);drawPiece(g,p);g.restore();
}
