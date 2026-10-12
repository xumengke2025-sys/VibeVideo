// 《夜鹭的一天》场景部件：岸、水面、树、芦苇。
// 全部按 STYLE.md §2 的刻皮语法：每片一个镂空单元、深色刻线 1.5–2.4、大面积透光只留细皮筋。
import {piece, drawPiece, fill, cut, cutLine, ink, within, scales, scalesOpen, cloud, beads, beadLine,
  plum, waves, meander, lattice, coin, strata, cutTaper, rivet, smooth, poly, DYE} from '../engine/carve.js';
import {rng, clamp} from './lib.js';

export const CLOTH={w:1080,h:1920};
export const BANK_Y=1560;      // 岸线（地条顶缘）
export const WATER_Y=1620;     // 水面线
export const WATER_BOT=1840;

// —— 岸：一条窄地条（回纹带 + 古钱孔 + 联珠）——
export const ground=piece([0,-46,CLOTH.w,86],g=>{
  const r=rng(7),top=[];
  for(let x=0;x<=CLOTH.w;x+=36)top.push([x,-8+Math.sin(x*.011)*5+r()*3]);
  fill(g,DYE.brown,q=>{smooth(q,[[0,-46],...top,[CLOTH.w,-46],CLOTH.w,86,0,86],true)});
  within(g,q=>{smooth(q,[[0,-46],...top,[CLOTH.w,-46],CLOTH.w,86,0,86],true)},()=>{
    meander(g,14,-30,CLOTH.w-14,9,1.8);
    beadLine(g,0,54,CLOTH.w,54,3.1,26);
    for(let x=40;x<CLOTH.w-20;x+=96+((x*7)%40))coin(g,x,12,11);
    strata(g,0,CLOTH.w,x=>-6+Math.sin(x*.011)*5,2,13,2.1);
  });
  ink(g,2.2,q=>{smooth(q,[[0,-46],...top,[CLOTH.w,-46],CLOTH.w,86,0,86],true)});
});

// —— 水面：可单独揭起的一条（长横波纹 + 反光竖条）——
export const water=piece([0,-16,CLOTH.w,WATER_BOT-WATER_Y+16],g=>{
  const r=rng(19),Hh=WATER_BOT-WATER_Y+16;
  fill(g,DYE.teal,q=>{q.rect(0,-16,CLOTH.w,Hh)});
  within(g,q=>{q.rect(0,-16,CLOTH.w,Hh)},()=>{
    for(let y=-4;y<Hh-8;y+=18){
      cutLine(g,3.0+(Math.floor(y/18)%3)*1.4,q=>{
        q.moveTo(-24,y);
        for(let x=0;x<=CLOTH.w+24;x+=36)q.lineTo(x,y+Math.sin(x*.013+y*.085)*5.5);
      });
    }
    for(let k=0;k<20;k++){
      const x=r()*CLOTH.w,y=24+r()*(Hh-70),L=44+r()*140;
      cutTaper(g,[[x,y],[x+(r()-.5)*22,y+L*.5],[x+(r()-.5)*34,y+L]],3.4);
    }
  });
  ink(g,2.2,q=>{q.moveTo(0,-16);q.lineTo(CLOTH.w,-16)});
});

// —— 树：细高树干 + 一整片花边树冠（镂空为主，只留细皮筋）——
export const TREE={trunkH:700,cy:-880,cr:372};
export const trunk=piece([-124,-TREE.trunkH-10,116,34],g=>{
  const body=[[-52,30],[-44,-160],[-50,-330],[-40,-520],[-34,-660],[-30,-702],[-6,-704],[-8,-540],[-2,-350],[6,-170],[22,30]];
  fill(g,DYE.brown,q=>{smooth(q,body,true)});
  // 分枝先画，再和主干一起被裁剪——否则分枝会被裁没
  const BR=[[-8,-560,-128,-636],[-6,-420,-120,-488],[-4,-290,-104,-348]];
  for(const br of BR){
    const sh=[[br[0],br[1]-15],[br[2],br[3]-11],[br[2],br[3]+13],[br[0],br[1]+17]];
    fill(g,DYE.brown,q=>{smooth(q,sh,true)});
  }
  within(g,q=>{smooth(q,body,true)},()=>{
    for(let k=0;k<13;k++){
      const u=k/12,y=24-TREE.trunkH*u,x0=-38+Math.sin(k*1.13)*13;
      cutTaper(g,[[x0,y],[x0+9,y-24],[x0-4+((k%3)-1)*10,y-50]],5.4);
    }
  });
  for(const br of BR){
    const sh=[[br[0],br[1]-16],[br[2],br[3]-12],[br[2],br[3]+14],[br[0],br[1]+20]];
    within(g,q=>{smooth(q,sh,true)},()=>{for(let k=1;k<5;k++){const t=k/5;cutTaper(g,[[br[0]+(br[2]-br[0])*t,br[1]+(br[3]-br[1])*t-10],[br[0]+(br[2]-br[0])*t,br[1]+(br[3]-br[1])*t-24]],3.2)}});
    ink(g,2.2,q=>{smooth(q,sh,true)});
  }
  ink(g,2.6,q=>{smooth(q,body,true)});
});

// 叶形孔：单片闭合路径（两瓣反向路径在 nonzero 下会绕数相消，故必须画成单环）
function leafHole(g,x,y,s,rot=0){
  const c=Math.cos(rot),si=Math.sin(rot);
  const P=(dx,dy)=>[x+dx*c-dy*si,y+dx*si+dy*c];
  const a=P(-s*1.15,0),b=P(0,-s*.44),cc=P(s*1.15,0),d=P(0,s*.44);
  cut(g,q=>{q.moveTo(a[0],a[1]);q.quadraticCurveTo(b[0],b[1],cc[0],cc[1]);q.quadraticCurveTo(d[0],d[1],a[0],a[1]);q.closePath()},'nonzero');
}
export const canopy=piece([-TREE.cr-40,-TREE.cr-40,TREE.cr+40,TREE.cr+40],g=>{
  const r=rng(53);
  const outline=[];
  for(let i=0;i<=34;i++){const a=i/34*Math.PI*2,rad=TREE.cr*(0.9+Math.sin(a*3.1)*.11+Math.cos(a*5.3)*.07);outline.push([Math.cos(a)*rad,Math.sin(a)*rad*.92])}
  fill(g,DYE.green,q=>{smooth(q,outline,true)});
  within(g,q=>{smooth(q,outline,true)},()=>{
    // 密集叶孔网格 + 抖动：镂空为主，只留细皮筋（STYLE.md §2 "镂空就是密度"）
    const R=33;
    for(let row=0;row*R*.86<TREE.cr*2+R;row++){
      for(let col=0;;col++){
        const x=-TREE.cr-R+col*R*1.72+(row%2)*R*.86;
        if(x>TREE.cr+R)break;
        const y=-TREE.cr*.92+row*R*.86;
        const jx=x+(r()-.5)*13,jy=y+(r()-.5)*13;
        if(Math.hypot(jx,jy*1.09)>TREE.cr-8)continue;
        leafHole(g,jx,jy,9+r()*13,r()*Math.PI*2);
      }
    }
    for(let k=0;k<12;k++){
      const a=k/12*Math.PI*2+.3;
      cloud(g,Math.cos(a)*(TREE.cr-10),Math.sin(a)*(TREE.cr*.92-10),30,r()*6.28,2.8,k%2?1:-1);
    }
    for(let k=0;k<26;k++){
      const a=r()*Math.PI*2,rad=Math.sqrt(r())*(TREE.cr-30);
      cutTaper(g,[[Math.cos(a)*rad,Math.sin(a)*rad*.92],[Math.cos(a)*rad+9,Math.sin(a)*rad*.92-14],[Math.cos(a)*rad+18,Math.sin(a)*rad*.92-30]],2.6);
    }
  });
  ink(g,2.8,q=>{smooth(q,outline,true)});
});

// —— 芦苇：一丛带叶的细杆（穗用锥形裂缝）——
export function buildReeds(seed,n=7){
  const r=rng(seed),out=[];
  for(let i=0;i<n;i++){
    const h=300+r()*320,lean=(r()-.5)*100;
    const p=piece([-90,-h-46,90,30],g=>{
      const stem=q=>{q.moveTo(0,24);q.quadraticCurveTo(lean*.4,-h*.35,lean,-h)};
      for(let k=0;k<5;k++){
        const u=.22+k*.17,px=lean*u*.86,py=24-h*u,side=(k%2?1:-1)*(u<.5?1:-1);
        const len=64+r()*54;
        fill(g,DYE.jade,q=>{smooth(q,[[px,py],[px+side*len*.45,py-len*.30],[px+side*len*.86,py-len*.74],[px+side*len*.5,py-len*.52],[px+side*len*.1,py-len*.12]],true)});
        cutTaper(g,[[px+side*6,py-4],[px+side*len*.45,py-len*.30],[px+side*len*.8,py-len*.7]],2.2);
        ink(g,1.9,q=>{smooth(q,[[px,py],[px+side*len*.45,py-len*.30],[px+side*len*.86,py-len*.74],[px+side*len*.5,py-len*.52],[px+side*len*.1,py-len*.12]],true)});
      }
      for(let k=0;k<7;k++){
        const a=-Math.PI/2+(k-3)*.17;
        cutTaper(g,[[lean,-h],[lean+Math.cos(a)*20,-h+Math.sin(a)*20],[lean+Math.cos(a)*40,-h+Math.sin(a)*40]],2.0);
      }
      ink(g,3.4,stem);
    },{seed:i+3});
    out.push({p,dx:(i-(n-1)/2)*(44+((i*13)%28))});
  }
  return out;
}

// 在幕布坐标里画场景（相机变换由调用方统一施加）
export function drawScenery(g,st={}){
  const {reedLift=0,waterLift=0}=st;
  g.save();g.translate(0,WATER_Y+waterLift);drawPiece(g,water);g.restore();
  g.save();g.translate(0,BANK_Y);drawPiece(g,ground);g.restore();
  if(st.reeds)for(const rd of st.reeds){
    g.save();g.translate(rd.x+rd.dx,BANK_Y+10-reedLift);drawPiece(g,rd.p);g.restore();
  }
}

