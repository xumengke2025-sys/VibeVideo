// V14: one persistent person, six removable burdens, one new logic station.
let realTime=0;
function legacyTime(t){const k=plan.time_map;let i=1;while(i<k.length-1&&t>k[i][0])i++;const a=k[i-1],b=k[i];return mix(a[1],b[1],p(t,a[0],b[0]));}
const rawPose=t=>cameraAt(Math.max(0,legacyTime(t)-8));
function cameraV14(t){
 let c=rawPose(t);
 const start=cameraAt(8),end=cameraAt(12),logic={x:1650,y:2550,z:.91,r:0};
 const blend=(a,b,u)=>({x:mix(a.x,b.x,u),y:mix(a.y,b.y,u),z:Math.exp(mix(Math.log(a.z),Math.log(b.z),u)),r:mix(a.r,b.r,u)});
 if(t>=22&&t<26)c=blend(start,logic,ease(p(t,22,26)));
 if(t>=26&&t<=42)c={...logic};
 if(t>42&&t<46)c=blend(logic,end,ease(p(t,42,46)));
 const room=ease(p(t,14,17))*(1-ease(p(t,84,89)));c={...c,z:c.z*mix(1,.86,room)};
 c.x-=95*room/c.z;c.y+=36*room/c.z;return c;
}
const logicRows=[
 ['融资','融资预案','筹划阶段 · 募资用途','定增 / 可转债 / 债券'],
 ['并购','重组 / 收购公告','交易阶段 · 对价来源','财顾 / 估值 / 尽调'],
 ['股东服务','减持披露 / 解禁日历','股东身份 · 窗口条件','减持 / 股份管理'],
 ['风险与跨境','套保 / 境外投资公告','真实敞口 · 地区币种','套保 / 跨境协同']
];
const logicIn=bez([2800,1540],[2800,1910],[2440,1900],[2280,2200]);
const logicOut=bez([2480,2550],[3230,2550],[3650,2010],[4590,1570]);
function logicStation(){at(1650,2550,()=>{
 mono('01-B / OPPORTUNITY LOGIC ENGINE',-690,-518,23,1,{v:.6});
 TX('商机从哪里来，为什么值得跟进',-690,-450,51,1);
 TX('公开公告：东方财富 / 巨潮回核 · 解禁日历 · 客户资料',-690,-397,31,1,{v:.75});
 frameBase(-710,-365,1710,690);
 const headings=[['业务场景',-676],['信号来源',-413],['判断要点',16],['服务方向',488]];
 headings.forEach(([s,x])=>TX(s,x,-300,35,1,{v:.8}));
 const active=Math.floor(p(realTime,26.6,39.4)*4);
 logicRows.forEach((row,i)=>{
  const y=-236+i*120,u=ease(p(realTime,26.7+i*3.0,27.4+i*3.0));
  panel(-685,y-37,1655,91,1,.22,12);
  const current=realTime>=26&&realTime<=42&&active===i;
  if(current){R(-693,y-45,1671,107,1,.9,2.5);gear(-745,y+7,16,4,realTime*.9,1,.85,14);}
  TX(row[0],-661,y+23,36,1,{v:.85});
  const v=realTime<26?.45:mix(.38,1,u);
  TX(row[1],-412,y+23,34,1,{v});TX(row[2],16,y+23,34,1,{v});TX(row[3],488,y+23,32,1,{v});
  for(const x of[-3,463]){pointer(x,y+10);}
  if(u>0&&u<1){const xx=mix(-425,940,u);C(xx,y+43,7,1,.95,2);}
 });
 L([[-675,260],[968,260]],1,1.5,.5);
 TX('融资阶段筛选：保留早期筹划，分流审批、发行与存续事项',-672,302,31,1,{v:.86});
 TX('更多场景：回购 · 股权激励 · 现金管理 · ABS / REITs',-687,402,31,1,{v:.78});
 TX('规则筛选线索 · AI 辅助解读依据 · 业务人员研判',-687,458,34,1,{v:.88});
 });at(0,0,()=>{
 rail(logicIn,.43);rail(logicOut,.43);
 if(realTime>=22&&realTime<26)carrier(logicIn,ease(p(realTime,22,26)),'客户线索',210);
 if(realTime>=42&&realTime<46)carrier(logicOut,ease(p(realTime,42,46)),'服务方向',210);
 if(T>44)plaque('商机判断',840,1840,1460,126,show(44,.7));
 });}

// The world path is sampled once from planned waypoints, then evaluated independently.
// It remains at the exit when the camera leaves for the final wide reveal.
function laneWaypoint(t){const c=cameraV14(t),x=-685+26*Math.sin(t*.18),y=378;const co=Math.cos(c.r),si=Math.sin(c.r);return[c.x+(co*x+si*y)/c.z,c.y+(-si*x+co*y)/c.z];}
const heroKeys=Array.from({length:141},(_,i)=>{const t=14+i*.5;return[t,...laneWaypoint(t)];});
function heroAt(t){
 if(t>=84){const a=heroKeys.at(-1);const u=ease(p(t,84,89));return[mix(a[1],1820,u),mix(a[2],3980,u)];}
 let i=1;while(i<heroKeys.length-1&&t>heroKeys[i][0])i++;const a=heroKeys[i-1],b=heroKeys[i];
 const before=heroKeys[Math.max(0,i-2)],after=heroKeys[Math.min(heroKeys.length-1,i+1)],h=b[0]-a[0],u=p(t,a[0],b[0]);
 return[1,2].map(j=>quint(a[j],b[j],(b[j]-before[j])/(b[0]-before[0]),(after[j]-a[j])/(after[0]-a[0]),h,u));
}
const gold='#e9c67e',pale='#edf1e7';
function loadBox(ctx,x,y,label,w=172,h=43,alpha=1){
 ctx.save();ctx.globalAlpha*=alpha;ctx.fillStyle='#15354e';pen(ctx,gold,1.8);ctx.fillRect(x,y,w,h);ctx.strokeRect(x,y,w,h);
 ol(ctx,[[x+9,y+6],[x+9,y+h-6]],'#b49355',1);ol(ctx,[[x+w-9,y+6],[x+w-9,y+h-6]],'#b49355',1);
 ot(ctx,label,x+w/2,y+h*.72,24,gold,'center',500);ctx.restore();
}
function person(ctx,t,{opening=false}={}){
 const removed=plan.burdens.reduce((a,b)=>a+ease(p(t,b.end-1.2,b.end)),0);
 const count=6-removed,lean=count/6,walk=(opening?.4:Math.min(1,Math.hypot(...heroAt(Math.min(t+.04,89)).map((v,i)=>v-heroAt(Math.max(14,t-.04))[i]))/25));
 const stride=Math.sin(t*10)*18*walk,bob=Math.abs(Math.sin(t*10))*3*walk,hip=[0,-68-bob],shoulder=[lean*40,-132-bob],head=[lean*51+7,-171-bob];
 // Shoes, trousers, tailored jacket, tie and a small face establish a business person.
 pen(ctx,pale,7);ol(ctx,[[hip[0]-8,hip[1]],[stride-12,-33],[stride-20,0],[stride+2,0]],pale,7);ol(ctx,[[hip[0]+9,hip[1]],[-stride+13,-36],[-stride+23,0],[-stride+42,0]],pale,7);
 ctx.fillStyle='#21445b';ctx.beginPath();ctx.moveTo(hip[0]-19,hip[1]-1);ctx.lineTo(shoulder[0]-19,shoulder[1]-7);ctx.lineTo(shoulder[0]+20,shoulder[1]-8);ctx.lineTo(hip[0]+23,hip[1]);ctx.closePath();ctx.fill();ctx.stroke();
 ring(ctx,head[0],head[1],22,pale,3);ol(ctx,[[head[0]+18,head[1]-3],[head[0]+27,head[1]+1],[head[0]+18,head[1]+5]],pale,2);
 ol(ctx,[[shoulder[0]-10,shoulder[1]-3],[shoulder[0]+2,shoulder[1]+23],[shoulder[0]+13,shoulder[1]-2]],gold,1.6);
 ol(ctx,[[shoulder[0]+3,shoulder[1]+8],[shoulder[0]+3,shoulder[1]+38]],gold,3);
 const hand=[shoulder[0]+37,-83-bob];ol(ctx,[[shoulder[0]+16,shoulder[1]+4],[shoulder[0]+39,-103-bob],hand],pale,5);
 // The straps are anchored to the same shoulder/back pose as the stack.
 const bx=-176+lean*15,by=-119-bob;
 if(count>.01){ol(ctx,[[bx+23,by-12],[shoulder[0]-14,shoulder[1]-6],[shoulder[0]-1,-84]],gold,2.5);}
 plan.burdens.forEach((b,i)=>{
  const u=ease(p(t,b.end-1.2,b.end));if(u>=1)return;
  const initial=opening?ease(p(t,.3+i*.55,1+i*.55)):1;
  const lift=u>0?Math.sin(u*Math.PI)*105:0;
  const x=mix(bx,360,u),y=mix(by-i*48,-57,u)-lift-(1-initial)*85;
  loadBox(ctx,x,y,b.label,172,43,initial*(1-ease(p(u,.90,1))));
  if(u>0){ // hoist head follows the exact load position, with visibly attached hook
   ol(ctx,[[-165,-440],[550,-440],[550,-72]],'#8fa9b8',1.3);
   ol(ctx,[[x+86,-440],[x+86,y-8]],gold,1.4);ol(ctx,[[x+76,y-16],[x+76,y-5],[x+96,y-5],[x+96,y-16]],pale,2.5);
  }
 });
 if(removed>.2){ctx.fillStyle='#15354e';pen(ctx,gold,2);ctx.fillRect(hand[0]-2,hand[1]+12,62,43);ctx.strokeRect(hand[0]-2,hand[1]+12,62,43);ctx.strokeRect(hand[0]+19,hand[1]+5,18,8);ol(ctx,[[hand[0]+12,hand[1]+33],[hand[0]+23,hand[1]+43],[hand[0]+43,hand[1]+24]],gold,2);}
 return{count,removed};
}
function burdenOpening(t){if(t>=14)return;const ctx=ov;ctx.save();ctx.scale(scale,scale);
 const u=ease(p(t,7.2,9));ctx.globalAlpha=1;
 if(t<8.4){ctx.save();ctx.globalAlpha=1-ease(p(t,7.5,8.4));
  pen(ctx,'rgba(184,208,219,.22)',1);ctx.strokeRect(60,52,1800,976);
  ot(ctx,'FIRMBUDDY / BUSINESS OPERATIONS',96,102,18,'#9ab4c5');
  ot(ctx,'业务人员的时间，被哪些负担占满？',960,210,59,pale,'center',600);
  ot(ctx,'找线索、做研判、备材料，每一步都在消耗精力',960,274,30,'#a8c1d2','center');
  const texts=[['线索散落','搜集慢，难以找到切入点'],['判断费力','找专家、查依据，反复确认业务方向'],['准备重复','材料反复整理，经营记录难接续']];
  texts.forEach((q,i)=>{const a=ease(p(t,1+i*1.2,1.6+i*1.2));ctx.save();ctx.globalAlpha*=a;ot(ctx,'0'+(i+1),1080,435+i*160,22,gold);ot(ctx,q[0],1140,435+i*160,43,pale);ot(ctx,q[1],1140,490+i*160,27,'#a8c1d2');ol(ctx,[[1080,524+i*160],[1790,524+i*160]],'rgba(190,201,199,.25)');ctx.restore();});
  ot(ctx,'让机器接住重复工作，让业务人员专注客户',960,980,33,gold,'center');ctx.restore();}
 ctx.translate(mix(650,100,u),mix(895,970,u));ctx.scale(mix(1.35,.48,u),mix(1.35,.48,u));person(ctx,t,{opening:true});ctx.restore();
}
function heroWorld(t){if(t<14)return;const world=heroAt(t),screen=S(...world).map(v=>v/scale),ctx=ov,c=cameraV14(t),arrival=ease(p(t,14,17));
 const pos=[mix(100,screen[0],arrival),mix(970,screen[1],arrival)];
 const z=mix(.48,c.z*1.04,arrival)*mix(1,2.2,ease(p(t,84,89)));
 ctx.save();ctx.scale(scale,scale);ctx.translate(...pos);ctx.rotate(c.r);ctx.scale(z,z);
 // A ground line stays attached to the world subject. Dock is only active during unload.
 ol(ctx,[[-190,18],[550,18]],'#90a8b5',1.2);for(let x=-160;x<520;x+=60)ol(ctx,[[x,19],[x-8,31]],'#78909d',1);
 const active=plan.burdens.find(b=>t>b.end-1.5&&t<b.end+1.0);
 if(active){const dock=ease(p(t,active.end-1.5,active.end-1.2))*(1-ease(p(t,active.end+.5,active.end+1)));ctx.save();ctx.globalAlpha=dock;ol(ctx,[[365,-15],[365,-72],[535,-72],[535,-15]],gold,2);ol(ctx,[[365,-72],[385,-41],[515,-41],[535,-72]],gold,1);ring(ctx,400,-10,12,gold,2);ring(ctx,500,-10,12,gold,2);ctx.restore();}
 person(ctx,t);
 ctx.restore();
 if(active&&t>=active.end){ctx.save();ctx.scale(scale,scale);ctx.globalAlpha=1-ease(p(t,active.end+.6,active.end+1));ot(ctx,active.result,600,951,29,gold,'center');ctx.restore();}
}

window.renderAt=(t,type='image/png',quality=.95)=>{
 realTime=Math.max(0,Math.min(90,t));filmTime=legacyTime(realTime);T=Math.max(0,filmTime-8);bounds=[];
 const c=cameraV14(realTime);setCam({...c,z:c.z*scale});proj.k=.43;clear();NIBS.length=0;
 if(realTime>=14){chassis();intro();signals();logicStation();experts();knowledge();visit();follow();
  const a=ease(p(realTime,14,16.7));if(a<1){g.setTransform(1,0,0,1,0,0);g.globalCompositeOperation='destination-in';g.fillStyle=`rgba(0,0,0,${a})`;g.fillRect(0,0,W,H);g.globalCompositeOperation='source-over';}}
 if(realTime>=8)opening(filmTime);burdenOpening(realTime);heroWorld(realTime);businessNarrative(realTime);
 compose(inkC,fxC,ovC,{sheet:[8200,4800],cam,seed:19});return type?canvas.toDataURL(type,quality):null;
};
window.cameraAt=cameraV14;
window.stateAt=t=>{window.renderAt(t,null);return{time:t,camera:cameraV14(t),hero:heroAt(Math.max(14,t)),burdens:plan.burdens.filter(b=>t<b.end).map(b=>b.id),buffer:[W,H],duration:90,shot:plan.shots.find(s=>t>=s.start&&t<s.end)?.id,bounds};};
window.__ready=true;window.renderAt(0,null);
const audio=new Audio('./audio/mix.wav'),seek=document.querySelector('#seek'),display=document.querySelector('#time'),button=document.querySelector('#play');let playing=false,started=0,base=0;
seek.oninput=()=>{base=+seek.value;audio.currentTime=base;started=performance.now();window.renderAt(base,null);display.textContent=base.toFixed(2)+' / 90';};
button.onclick=()=>{playing=!playing;button.textContent=playing?'暂停':'播放';if(playing){base=+seek.value;if(base>=90)base=0;started=performance.now();audio.currentTime=base;audio.play().catch(()=>{});}else{base=+seek.value;audio.pause();}};
function tick(){if(playing){const t=Math.min(90,base+(performance.now()-started)/1000);window.renderAt(t,null);seek.value=t;display.textContent=t.toFixed(2)+' / 90';if(t>=90){playing=false;audio.pause();button.textContent='播放';}}requestAnimationFrame(tick);}if(!Q.has('render'))tick();
