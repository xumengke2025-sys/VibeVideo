import {clamp,ease,lerp,progress,captionAt} from './timeline.mjs';
// Code-drawn particle-count film. All motion is a pure function of time; the walk uses a fixed seed.
const clip=new URLSearchParams(location.search).get('clip')||'entropy';
if(!/^[a-z0-9-]+$/.test(clip))throw Error('Invalid clip');
const plan=await (await fetch(`clips/${clip}.json`)).json();
const canvas=document.getElementById('film'),g=canvas.getContext('2d');
const W=plan.width||1920,H=plan.height||1080;
const BG='#0B1420',BEIGE='#E9E3D5',FAINT='rgba(233,227,213,.42)',FAINT2='rgba(233,227,213,.22)',CYAN='#5FD6CE',YELLOW='#F0C24B',INK='#08111B';
const font='"Microsoft YaHei","Noto Sans CJK SC",sans-serif',technical='"Bahnschrift","Consolas",monospace',serif='"Cambria Math","Georgia",serif';
const N=plan.model.particles;
let tNow=0;
function rng(seed){return ()=>{seed|=0;seed=seed+0x6d2b79f5|0;let a=Math.imul(seed^seed>>>15,1|seed);a^=a+Math.imul(a^a>>>7,61|a);return ((a^a>>>14)>>>0)/4294967296;};}
function mulberryStream(seed){const r=rng(seed);return ()=>Math.floor(r()*N);}

/* ---- model: counts and arrangements computed, never hardcoded ---- */
const counts=Array.from({length:N+1},(_,k)=>{let r=1;for(let i=0;i<k;i++)r=r*(N-i)/(i+1);return Math.round(r);});
const arrByK=Array.from({length:N+1},(_,k)=>{const out=[];for(let m=0;m<(1<<N);m++){let b=0;for(let j=0;j<N;j++)if(m>>j&1)b++;if(b===k)out.push(m);}return out;});
const maskA=0b00001111,maskB=(1<<0)|(1<<2)|(1<<4)|(1<<6);
const idxA=arrByK[4].indexOf(maskA),idxB=arrByK[4].indexOf(maskB);

/* ---- deterministic crossing schedule from the contract ---- */
function buildSchedule(){
  const s=[];
  const ch=plan.model.choreography||{};
  for(const key of ['s1','s2','seq'])if(ch[key])for(const op of ch[key])for(const mv of op.movers)s.push({kind:'flip',at:op.at,dur:op.duration,i:mv-1,highlight:!!op.highlight});
  const walk=plan.model.walk;
  if(walk){
    for(const run of walk.runs){const stream=mulberryStream(run.seed);
      for(let k=0;k<run.steps;k++)s.push({kind:'flip',at:run.start+(walk.flipDelay||0.05)+k*walk.dt,dur:walk.flipDur||0.26,i:stream(),walk:true,run:run.start});}
    for(const run of walk.runs)s.push({kind:'reset',at:run.start-(walk.resetLead||0.42),dur:(walk.resetDur||0.36)});
  }
  if(plan.model.tail){const stream=mulberryStream(plan.model.tail.seed);
    for(const op of plan.model.tail.ops)s.push({kind:'flip',at:op.at,dur:op.duration,i:stream(),tail:true});}
  s.sort((a,b)=>a.at-b.at);
  const sides=Array.from({length:N},(_,i)=>(plan.model.init||'L'.repeat(N))[i]);
  for(const op of s){if(op.kind==='reset'){for(let i=0;i<N;i++)sides[i]='L';continue;}op.from=sides[op.i];op.to=sides[op.i]==='L'?'R':'L';sides[op.i]=op.to;}
  return s;
}
const schedule=buildSchedule();
const hlWindows=Array.from({length:N},()=>[]);
for(const op of schedule)if(op.kind==='flip'&&op.highlight)hlWindows[op.i].push([op.at-1.0,op.at+op.dur+0.15]);
const walkStates=plan.model.walk?plan.model.walk.runs.map(run=>{
  const flips=schedule.filter(o=>o.walk&&o.run===run.start).sort((a,b)=>a.at-b.at);
  let cnt=N;const arr=[];for(const f of flips){cnt+=f.to==='L'?1:-1;arr.push(cnt);}
  return {run:run.start,counts:arr};
}):null;

/* ---- solver: sides + positions at time t ---- */
function geoOf(cx,cy,w,h){return {x:cx-w/2,y:cy-h/2,w,h,midX:cx,cx,cy};}
function geoSlots(geo,side){
  const x0=side==='L'?geo.x:geo.midX,wid=geo.w/2,pts=[];
  const colX=[x0+wid*0.30,x0+wid*0.70],rowY=[geo.y+geo.h*0.20,geo.y+geo.h*0.40,geo.y+geo.h*0.60,geo.y+geo.h*0.80];
  for(const r of [1,2,0,3])for(const c of [0,1])pts.push({x:colX[c],y:rowY[r]});
  return pts;
}
function occupancy(sides,side){const list=[];for(let i=0;i<N;i++)if(sides[i]===side)list.push(i);return list;}
function solve(t,geo){
  const sides=Array.from({length:N},(_,i)=>(plan.model.init||'L'.repeat(N))[i]);
  const active=[];let resetPh=null;
  for(const op of schedule){
    const end=op.at+op.dur;
    if(t>=end){if(op.kind==='reset'){for(let i=0;i<N;i++)sides[i]='L';}else sides[op.i]=op.to;}
    else if(t>=op.at){
      if(op.kind==='reset'){resetPh=(t-op.at)/op.dur;if(resetPh>=0.5)for(let i=0;i<N;i++)sides[i]='L';}
      else{active.push(op);if(t>=op.at+op.dur*0.5)sides[op.i]=op.to;}
    }
  }
  const slotsL=geoSlots(geo,'L'),slotsR=geoSlots(geo,'R'),post=sides.slice(),pos=[];
  for(let i=0;i<N;i++){
    const act=active.find(a=>a.i===i);
    if(act){
      const ph=clamp((t-act.at)/act.dur),e2=ease(ph);
      const preS=sides.slice();preS[i]=act.from;post[i]=act.to;
      const fromList=occupancy(preS,act.from),toList=occupancy(post,act.to);
      const fs=(act.from==='L'?slotsL:slotsR)[fromList.indexOf(i)];
      const ts=(act.to==='L'?slotsL:slotsR)[toList.indexOf(i)];
      const dir=act.to==='R'?1:-1,c1={x:fs.x+dir*40,y:fs.y-56},c2={x:ts.x-dir*40,y:ts.y+56};
      const u=1-e2;
      const bx=u*u*u*fs.x+3*u*u*e2*c1.x+3*u*e2*e2*c2.x+e2*e2*e2*ts.x;
      const by=u*u*u*fs.y+3*u*u*e2*c1.y+3*u*e2*e2*c2.y+e2*e2*e2*ts.y;
      pos.push({x:bx,y:by,i,side:sides[i],tween:{fs,ts,c1,c2,ph}});
    }else{
      const list=occupancy(sides,sides[i]);
      const slot=(sides[i]==='L'?slotsL:slotsR)[list.indexOf(i)];
      pos.push({x:slot.x,y:slot.y,i,side:sides[i]});
    }
  }
  let left=0;for(let i=0;i<N;i++)if(sides[i]==='L')left++;
  return {sides,pos,left,right:N-left,active,resetPh};
}

/* ---- drawing helpers ---- */
function line(pts,{color=BEIGE,width=2,dash=[],alpha=1,amount=1}={}){
 if(amount<=0)return;g.save();g.globalAlpha*=alpha;g.strokeStyle=color;g.lineWidth=width;g.setLineDash(dash);g.lineCap='round';g.lineJoin='round';
 let length=0;const ls=[];for(let i=1;i<pts.length;i++){const d=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]);ls.push(d);length+=d;}
 let remaining=length*clamp(amount);g.beginPath();g.moveTo(...pts[0]);
 for(let i=1;i<pts.length;i++){const f=Math.min(1,remaining/(ls[i-1]||1));g.lineTo(lerp(pts[i-1][0],pts[i][0],f),lerp(pts[i-1][1],pts[i][1],f));remaining-=ls[i-1];if(remaining<=0)break;}g.stroke();g.restore();
}
function rect(x,y,w,h,o={}){line([[x,y],[x+w,y],[x+w,y+h],[x,y+h],[x,y]],o);}
function rrect(x,y,w,h,r,{fill=null,stroke=null,width=2,alpha=1}={}){g.save();g.globalAlpha*=alpha;g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath();if(fill){g.fillStyle=fill;g.fill();}if(stroke){g.strokeStyle=stroke;g.lineWidth=width;g.stroke();}g.restore();}
function text(s,x,y,size=28,color=BEIGE,align='left',family=font,alpha=1){if(alpha<=0.01)return;g.save();g.globalAlpha*=alpha;g.fillStyle=color;g.font=`${size}px ${family}`;g.textAlign=align;g.fillText(s,x,y);g.textAlign='left';g.restore();}
function dot(x,y,r,color=BEIGE,fill=true,alpha=1){g.save();g.globalAlpha*=alpha;g.beginPath();g.arc(x,y,r,0,Math.PI*2);if(fill){g.fillStyle=color;g.fill();}else{g.strokeStyle=color;g.lineWidth=2;g.stroke();}g.restore();}
function glowDot(x,y,r,alpha=1){g.save();g.globalAlpha*=alpha;const gr=g.createRadialGradient(x,y,r*0.3,x,y,r*2);gr.addColorStop(0,'rgba(95,214,206,.5)');gr.addColorStop(1,'rgba(95,214,206,0)');g.fillStyle=gr;g.beginPath();g.arc(x,y,r*2,0,Math.PI*2);g.fill();g.restore();}

/* ---- particles + badges ---- */
function drawParticles(sol,r=40,alpha=1){
 for(const p of sol.pos){
  const act=sol.active.find(a=>a.i===p.i);
  if(act&&p.tween){for(const back of [0.14,0.28]){const q=clamp(p.tween.ph-back);if(q<=0)continue;
    const e2=ease(q),u=1-e2,{fs,ts,c1,c2}=p.tween;
    const gx=u*u*u*fs.x+3*u*u*e2*c1.x+3*u*e2*e2*c2.x+e2*e2*e2*ts.x;
    const gy=u*u*u*fs.y+3*u*u*e2*c1.y+3*u*e2*e2*c2.y+e2*e2*e2*ts.y;
    dot(gx,gy,r*(1-back*0.5),CYAN,true,alpha*(p.tween.ph-back)*0.30);}}
  glowDot(p.x,p.y,r,alpha*0.8);
  dot(p.x,p.y,r,CYAN,true,alpha);
  text(String(p.i+1),p.x,p.y+r*0.34,r*0.92,INK,'center',technical,alpha);
  if(hlWindows[p.i].some(w=>tNow>=w[0]&&tNow<=w[1])){const pulse=0.6+0.4*Math.sin(tNow*6);
    g.save();g.globalAlpha*=alpha;g.strokeStyle=YELLOW;g.lineWidth=4;g.beginPath();g.arc(p.x,p.y,r+10+pulse*4,0,Math.PI*2);g.stroke();g.restore();}
 }
}
function drawBadges(sol,geo,y){
  const bw=180,bh=74;
  rrect(geo.x,y,bw,bh,12,{fill:'rgba(233,227,213,.06)',stroke:FAINT2,width:1.5});
  rrect(geo.x+geo.w-bw,y,bw,bh,12,{fill:'rgba(233,227,213,.06)',stroke:FAINT2,width:1.5});
  text('左区',geo.x+20,y+30,20,FAINT,'left');text(String(sol.left),geo.x+20,y+62,34,BEIGE,'left',technical);
  text('右区',geo.x+geo.w-bw+20,y+30,20,FAINT,'left');text(String(sol.right),geo.x+geo.w-bw+20,y+62,34,BEIGE,'left',technical);
  text(String(sol.left),geo.midX-64,y+60,40,BEIGE,'center',technical);text(':',geo.midX,y+58,40,FAINT,'center');
  text(String(sol.right),geo.midX+64,y+60,40,BEIGE,'center',technical);
}

/* ---- tank scene: S1, S2, the 5s fragment ---- */
function membersScene(t,{geo,showDivider,showLabels,labelAlpha,badgeY,fragNote}){
  const sol=solve(t,geo);
  rect(geo.x,geo.y,geo.w,geo.h,{color:FAINT,width:2});
  if(showDivider){
    const remove=clamp((t-1.2)/0.6);
    line([[geo.midX,geo.y+12],[geo.midX,geo.y+geo.h-12]],{color:'rgba(240,194,75,.85)',width:4,alpha:1-remove});
    const boundary=clamp((t-2.0)/1.2);
    line([[geo.midX,geo.y+12],[geo.midX,geo.y+geo.h-12]],{color:FAINT,width:2,dash:[16,12],alpha:boundary*0.5});
    if(t<1.7)text('隔板',geo.midX+16,geo.y+46,22,'rgba(240,194,75,.85)',1,font,1-clamp((t-1.0)/0.7));
    if(t>2.3)text('统计边界',geo.midX+16,geo.y+46,22,FAINT,'left',font,clamp((t-2.3)/0.5)*(1-clamp((t-3.8)/0.6)));
  }
  drawParticles(sol);
  drawBadges(sol,geo,badgeY);
  if(showLabels){
    text('微观：具体是谁',geo.x+36,geo.y+geo.h-28,30,BEIGE,'left',font,labelAlpha);
    text('宏观：左右各几个',geo.x+geo.w-36,badgeY-22,30,BEIGE,'right',font,labelAlpha);
  }
  if(fragNote&&t>3.5)text('同为左 4 右 4 · 成员不同',geo.midX,geo.y+geo.h+64,34,YELLOW,'center',font,ease(clamp((t-3.5)/0.7))*(1-clamp((t-4.9)/0.1)));
}

/* ---- S3: combinatorial expansion ---- */
function stripRow(gx,gy,cw,ch,gap,mask,alpha){
  for(let j=0;j<N;j++){const x=gx+j*(cw+gap);
    if(mask>>j&1){g.save();g.globalAlpha*=alpha;g.fillStyle=BEIGE;g.fillRect(x,gy,cw,ch);g.restore();}
    else rect(x,gy,cw,ch,{color:FAINT2,width:1.2,alpha});}
}
function expansion(t){
  const sh=progress(plan,'shrink',t);
  const big=geoOf(960,592,1220,646),small=geoOf(430,646,620,540);
  const geo=geoOf(lerp(big.cx,small.cx,sh),lerp(big.cy,small.cy,sh),lerp(big.w,small.w,sh),lerp(big.h,small.h,sh));
  membersScene(t,{geo,showDivider:false,showLabels:false,labelAlpha:0,badgeY:geo.y-96});
  const one=progress(plan,'oneWay',t);if(one<=0)return;
  text('全部在左（8 : 0）',880,248,32,BEIGE,'left',font,Math.min(1,one*2));
  stripRow(880,292,38,30,6,(1<<N)-1,Math.min(1,one*2));
  rrect(864,276,8*38+7*6+32,62,10,{stroke:'rgba(240,194,75,.55)',width:2,alpha:Math.min(1,one*2)});
  const bigOne=1-clamp((progress(plan,'seventy',t)-0.02)/0.15);
  if(bigOne>0){
    const y=322;
    text('=',1440,y,44,FAINT,'center',font,bigOne*Math.min(1,one*2));
    text('1',1560,y,86,YELLOW,'center',technical,bigOne*Math.min(1,one*2));
    text('种',1632,y,36,YELLOW,'left',font,bigOne*Math.min(1,one*2));
  }
  text('一行 8 格 = 一种左右归属排列（勾选 = 在左区）',880,372,24,FAINT,'left',font,Math.min(1,one*2));
  const numA=progress(plan,'seventy',t);if(numA<=0)return;
  text('左右各 4（4 : 4）',880,500,32,BEIGE,'left',font,Math.min(1,numA*3));
  const gw=17,gh=13,gg=3,dx=142,dy=30,gx0=880,gy0=542;
  const reveal=clamp((numA-0.1)/0.7)*70+0.5;
  for(let i=0;i<70&&i<reveal;i++){const x=gx0+(i%7)*dx,y=gy0+Math.floor(i/7)*dy;stripRow(x,y,gw,gh,gg,arrByK[4][i],1);}
  if(reveal>=70){
    const bracket=(idx,label)=>{const x=gx0+(idx%7)*dx,y=gy0+Math.floor(idx/7)*dy;
      line([[x-5,y-6],[x-5,y-18],[x+8*gw+7*gg+5,y-18],[x+8*gw+7*gg+5,y-6]],{color:YELLOW,width:2.5});
      text(label,x-5,y-24,22,YELLOW,'center',technical);};
    bracket(idxA,'A');bracket(idxB,'B');
    text('A、B = 刚才展示的两种排列',880,462,22,FAINT,'left',font,Math.min(1,(numA-0.9)/0.5));
    text('每行 = 一种归属排列（互不重复，共 70 行）',880,830+62,24,FAINT,'left',font,Math.min(1,(numA-0.9)/0.5));
    const n70=Math.min(1,(numA-0.86)/0.36);
    const y=930;
    text('=',1440,y,44,FAINT,'center',font,n70);
    text('70',1570,y,96,YELLOW,'center',technical,n70);
    text('种',1660,y,36,YELLOW,'left',font,n70);
  }
}

/* ---- S4: distribution ---- */
function distribution(t){
  const fade=1-clamp((t-43.0)/0.4),grow=progress(plan,'bars',t);
  const ends=progress(plan,'ends',t),center=progress(plan,'center',t),middle=progress(plan,'middle',t);
  const x0=300,x1=1640,base=830,top=250,bw=96,slot=(x1-x0)/9;
  line([[x0,base],[x1,base]],{color:BEIGE,width:2,alpha:0.9*fade});
  line([[x0,top-40],[x0,base]],{color:BEIGE,width:2,alpha:0.9*fade});
  for(const v of [20,40,60]){const y=base-v/70*(base-top);line([[x0,y],[x1,y]],{color:FAINT2,width:1,alpha:0.6*fade});text(String(v),x0-20,y+8,24,FAINT,'right',technical,0.9*fade);}
  text('排列数',x0,top-58,26,FAINT,'left',font,0.9*fade);
  text('左区粒子数',(x0+x1)/2,930,26,FAINT,'center',font,0.9*fade);
  for(let i=0;i<=8;i++){
    const v=counts[i],h=v/70*(base-top),cx=x0+(i+0.5)*slot;
    const arrive=ease(clamp((grow-i*0.08)/0.42));if(arrive<=0)continue;
    const hh=h*arrive,y=base-hh;
    g.save();g.globalAlpha=fade;g.fillStyle=BEIGE;g.fillRect(cx-bw/2,y,bw,hh);g.restore();
    const hlv=(i===0||i===8)?ends:(i===4?center:((i===3||i===5)?middle:0));
    if(hlv>0.02){g.save();g.globalAlpha*=fade*hlv;g.strokeStyle=YELLOW;g.lineWidth=3.5;g.strokeRect(cx-bw/2-6,y-6,bw+12,hh+12);g.restore();}
    if(arrive>0.98)text(String(v),cx,y-16,26,BEIGE,'center',technical,fade);
    text(String(i),cx,base+40,28,BEIGE,'center',technical,0.95*fade);
  }
  if(middle>0.02){
    const cx3=x0+3.5*slot,cx5=x0+5.5*slot;
    rrect(cx3-bw/2-10,top-30,cx5-cx3+bw+20,base-top+30,14,{fill:'rgba(240,194,75,.10)',stroke:'rgba(240,194,75,.7)',width:2,alpha:0.95*fade*Math.min(1,middle*2)});
    text('近均匀三组（k = 3、4、5）：182 / 256 ≈ 71.1%',(cx3+cx5)/2,top-48,34,YELLOW,'center',font,Math.min(1,middle*2)*fade);
  }
  if(ends>0.02){const a=Math.min(1,ends*2)*fade;text('1 种',x0+0.5*slot,base-52,26,YELLOW,'center',technical,a);text('1 种',x0+8.5*slot,base-52,26,YELLOW,'center',technical,a);}
  if(center>0.02){const cx4=x0+4.5*slot,a=Math.min(1,center*2)*fade;
    text('70 / 256 ≈ 27.3%',cx4,base+66,26,'rgba(240,194,75,.85)','center',technical,a);}
}

/* ---- S5: seeded random walk ---- */
function walk(t){
  const fadeIn=ease(clamp((t-43.4)/0.6));
  const geo=geoOf(520,620,660,560),sol=solve(t,geo);
  const resetting=sol.resetPh!==null;
  rect(geo.x,geo.y,geo.w,geo.h,{color:FAINT,width:2,alpha:fadeIn});
  drawParticles(sol,34,fadeIn*(resetting?0.3:1));
  if(resetting)text('重新开始',geo.midX,geo.y-34,26,FAINT,'center',font,Math.abs(sol.resetPh-0.5)<0.35?1:0);
  drawBadges(sol,geo,geo.y-100);
  const cx0=1080,cx1=1820,cy0=810,cy1=270,X=u=>cx0+u/28*(cx1-cx0),Y=v=>cy0-v/8*(cy0-cy1);
  line([[cx0,cy0],[cx1,cy0]],{color:BEIGE,width:2,alpha:fadeIn});
  line([[cx0,cy0],[cx0,cy1]],{color:BEIGE,width:2,alpha:fadeIn});
  for(const v of [0,2,4,6,8]){line([[cx0,Y(v)],[cx0-10,Y(v)]],{color:BEIGE,width:2,alpha:fadeIn});text(String(v),cx0-20,Y(v)+8,24,FAINT,'right',technical,fadeIn);}
  g.save();g.globalAlpha*=fadeIn;g.translate(1010,(cy0+cy1)/2);g.rotate(-Math.PI/2);g.fillStyle=FAINT;g.font=`24px ${font}`;g.textAlign='center';g.fillText('左区粒子数',0,0);g.restore();
  g.save();g.globalAlpha*=fadeIn;g.fillStyle=FAINT;g.font=`24px ${font}`;g.textAlign='right';g.fillText('步数',cx1,cy0+44);g.restore();
  let ux=0;
  const runs=plan.model.walk.runs;
  for(let ri=0;ri<runs.length;ri++){
    const run=runs[ri],st=walkStates[ri];
    const endT=run.start+plan.model.walk.flipDelay+run.steps*plan.model.walk.dt;
    const pts=[[X(ux),Y(N)]];
    for(let k=0;k<run.steps;k++){const tt=run.start+plan.model.walk.flipDelay+k*plan.model.walk.dt;if(t>=tt)pts.push([X(ux+k+1),Y(st.counts[k])]);else break;}
    if(pts.length>1)line(pts,{color:CYAN,width:2.6,alpha:fadeIn*(ri===runs.length-1||t<run.start?1:0.9)});
    for(const [px,py] of pts.slice(1))dot(px,py,4,CYAN,true,fadeIn*0.9);
    for(let k=0;k<st.counts.length;k++){const c=st.counts[k];if((c<=1||c>=7)&&t>=run.start+plan.model.walk.flipDelay+k*plan.model.walk.dt)dot(X(ux+k+1),Y(c),10,YELLOW,false,fadeIn);}
    if(t>=run.start&&t<endT){
      const k=clamp(Math.floor((t-(run.start+plan.model.walk.flipDelay))/plan.model.walk.dt),0,run.steps-1);
      const val=k===0?N:st.counts[Math.max(0,k-1)];
      dot(X(ux+k+1),Y(val),7,YELLOW,true,fadeIn);
      text('左区：'+String(val),X(ux+k+1)+18,Y(val)-16,26,YELLOW,'left',technical,fadeIn);
    }
    ux+=run.steps+1;
  }
  text('对称随机模型 · 非真实气体轨迹',cx0,cy0+52,24,FAINT,'left',font,fadeIn);
  text('每一步：等概率选一个粒子，翻转它的左右归属',cx0,cy0+86,24,FAINT,'left',font,fadeIn);
}

/* ---- S6: closing ---- */
function closing(t){
  const a=ease(clamp((t-55.4)/0.7));
  const geo=geoOf(560,620,760,600),sol=solve(t,geo);
  rect(geo.x,geo.y,geo.w,geo.h,{color:FAINT,width:2,alpha:a});
  drawParticles(sol,34,a);drawBadges(sol,geo,geo.y-96);
  const pa=ease(clamp((t-57.6)/0.8));
  const bx0=1140,base=520,bw=52,slot=76;
  for(let i=0;i<=8;i++){const h=counts[i]/70*180,cx=bx0+i*slot;
    g.save();g.globalAlpha*=a*pa;g.fillStyle=i===4?YELLOW:'rgba(233,227,213,.55)';g.fillRect(cx-bw/2,base-h,bw,h);g.restore();
    text(String(i),cx,base+30,22,FAINT,'center',technical,a*pa);}
  text('排列数分布（同前）',bx0+4*slot,base+66,22,FAINT,'center',font,a*pa);
  const fa=ease(clamp((t-60.0)/0.8));
  if(fa>0){g.save();g.globalAlpha*=a*fa;g.fillStyle=BEIGE;g.font=`italic 62px ${serif}`;g.textAlign='left';
    g.fillText('S = k',1140,700);g.font=`italic 38px ${serif}`;g.fillText('B',1250,718);g.font=`italic 62px ${serif}`;g.fillText('ln Ω',1298,700);g.restore();
    text('Ω：该宏观状态对应的微观排列数',1140,756,26,FAINT,'left',font,a*fa);}
  const sa=ease(clamp((t-62.5)/0.8));
  if(sa>0){text('孤立宏观系统的熵增规律具有统计意义；',1140,824,24,FAINT,'left',font,a*sa);
    text('局部熵降低可以伴随环境熵增加。',1140,860,24,FAINT,'left',font,a*sa);}
  const st=ease(clamp((t-64.4)/0.9));
  if(st>0){g.save();g.globalAlpha*=st;g.fillStyle=YELLOW;g.font=`54px ${font}`;g.textAlign='center';
    g.fillText('更容易出现，因为对应的微观排列更多。',960,952);g.restore();}
}

/* ---- frame ---- */
window.__audit={counts,arrangements:arrByK.map(a=>a.length),arr70distinct:new Set(arrByK[4]).size,idxA,idxB,sum:counts.reduce((a,b)=>a+b,0),nearUniform:counts[3]+counts[4]+counts[5],walk:walkStates};
function sceneId(t){
  if(plan.id==='members-5s')return 'members';
  if(t<8.5)return 's1';if(t<18.9)return 's2';if(t<31.2)return 's3';if(t<43.4)return 's4';if(t<55.4)return 's5';return 's6';
}
const segTag=['01 提出矛盾','02 两个尺度','03 排列数量','04 概率分布','05 统计含义','06 纠正误解'];
function frame(t){
  tNow=t;
  g.fillStyle=BG;g.fillRect(0,0,W,H);
  const vg=g.createRadialGradient(960,540,200,960,540,1300);vg.addColorStop(0,'rgba(28,44,66,.55)');vg.addColorStop(1,'rgba(4,8,14,.9)');
  g.fillStyle=vg;g.fillRect(0,0,W,H);
  const r=rng(plan.seed);for(let i=0;i<1600;i++){g.fillStyle=i%2?'rgba(233,227,213,.018)':'rgba(95,214,206,.02)';g.fillRect(r()*W,r()*H,1+r(),1+r());}
  if(plan.id==='members-5s'){
    const geo=geoOf(960,560,1220,640);
    membersScene(t,{geo,showDivider:false,showLabels:true,labelAlpha:ease(clamp((t-0.4)/0.8)),badgeY:geo.y-96,fragNote:true});
  }else{
    const id=sceneId(t);
    if(id==='s1'||id==='s2'){
      const geo=geoOf(960,592,1220,646);
      const lab=(id==='s2')?ease(clamp((t-8.9)/1.1))*(1-ease(clamp((t-18.4)/0.5))):0;
      membersScene(t,{geo,showDivider:true,showLabels:lab>0,labelAlpha:lab,badgeY:geo.y-96});
    }
    else if(id==='s3'){
      const a3=1-clamp((t-30.3)/0.9);
      if(a3>0.01){g.save();g.globalAlpha=a3;expansion(t);g.restore();}
      const a4=ease(clamp((t-30.6)/0.6));
      if(a4>0.01){g.save();g.globalAlpha=a4;distribution(t);g.restore();}
    }
    else if(id==='s4')distribution(t);
    else if(id==='s5'){g.save();g.globalAlpha=1-clamp((t-55.0)/0.4);walk(t);g.restore();}
    else closing(t);
    const idx=['s1','s2','s3','s4','s5','s6'].indexOf(id);
    dot(34,44,5,CYAN,true,0.9);
    text('熵增 · 统计计数模型',56,52,24,FAINT,'left');
    text(segTag[idx],W-48,52,24,FAINT2,'right');
  }
  line([[0,6],[W*clamp(t/plan.duration),6]],{color:YELLOW,width:5,alpha:0.5});
  const cap=captionAt(plan,t);
  if(cap){
    g.save();g.font=`42px ${font}`;const full=g.measureText(cap.text).width;g.restore();
    if(full<=1700){
      const bw2=full+96,bx=W/2-bw2/2,by=968;
      rrect(bx,by,bw2,86,18,{fill:'rgba(6,10,16,.82)',stroke:'rgba(233,227,213,.22)',width:1.5});
      text(cap.text,W/2,by+58,42,BEIGE,'center');
    }else{
      const s=cap.text,mid=s.length/2;
      let cut=-1,best=1e9;
      for(let i=1;i<s.length-1;i++)if('，。；：、？！'.includes(s[i])){const d=Math.abs(i+1-mid);if(d<best){best=d;cut=i+1;}}
      if(cut<=0)cut=Math.round(mid);
      const l1=s.slice(0,cut),l2=s.slice(cut);
      g.save();g.font=`42px ${font}`;const w1=g.measureText(l1).width,w2=g.measureText(l2).width;g.restore();
      const bw2=Math.max(w1,w2)+110,bx=W/2-bw2/2,by=946;
      rrect(bx,by,bw2,126,18,{fill:'rgba(6,10,16,.82)',stroke:'rgba(233,227,213,.22)',width:1.5});
      text(l1,W/2,by+52,42,BEIGE,'center');
      text(l2,W/2,by+108,42,BEIGE,'center');
    }
  }
}
window.__film={...plan,width:W,height:H};
window.stateAt=t=>{const s=solve(t,geoOf(960,592,1220,646));
  return {scene:sceneId(t),sides:s.sides.join(''),left:s.left,right:s.right,leftCount:s.left,rightCount:s.right,total:N};};
window.renderAt=(t,type='image/png',quality=.95)=>{
 if(!Number.isFinite(t)||t<0||t>plan.duration)throw Error('Out-of-range time');
 g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;g.clearRect(0,0,W,H);frame(t);return canvas.toDataURL(type,quality);
};
await document.fonts.ready;window.ready=true;window.renderAt(0);
if(!new URLSearchParams(location.search).has('render')){const start=performance.now();function play(now){window.renderAt(((now-start)/1000)%plan.duration);requestAnimationFrame(play);}requestAnimationFrame(play);}
