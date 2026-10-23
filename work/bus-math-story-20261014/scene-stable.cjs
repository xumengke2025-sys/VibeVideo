// Fixed-size paper actors. The only scene change is an explicit paper wipe into
// a separate distance diagram. Meter positions never change illustration size.
const {bus,kid,titles}=require('./scene.cjs');
const C={ink:'#49392f',cream:'#f5ecd9',paper:'#fffaf0',blue:'#4c849b',coral:'#c87057',gold:'#edba54'};
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const smooth=v=>{v=clamp(v);return v*v*(3-2*v)};
const lerp=(a,b,p)=>a+(b-a)*p;
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;');
const text=(x,y,s,size=34,color=C.ink)=>`<text x="${x}" y="${y}" text-anchor="middle" font-size="${size}" fill="${color}" font-weight="700">${esc(s)}</text>`;
const tag=(x,y,s,w=430,color=C.ink)=>`<rect x="${x-w/2}" y="${y-42}" width="${w}" height="64" rx="24" fill="${C.paper}" stroke="#dbcbb0" stroke-width="3"/>${text(x,y,s,30,color)}`;
const face=kid(0,0,C.blue,1,0,1,false).split('<path d="M-14 103')[1].split('</g>')[0];
const head='<path d="M-14 103'+face;
function ik(hx,hy,fx,fy,a,b,side=1){
 const dx=fx-hx,dy=fy-hy,d=Math.max(.01,Math.hypot(dx,dy)),reach=Math.min(d,a+b-.01);
 const q=(a*a-b*b+reach*reach)/(2*reach),v=Math.sqrt(Math.max(0,a*a-q*q));
 return [hx+dx/d*q+dy/d*v*side,hy+dy/d*q-dx/d*v*side];
}
function foot(phase,run){
 const p=((phase%1)+1)%1;
 let x,y;
 if(p<.6){x=35-70*p/.6;y=300;}
 else{const q=(p-.6)/.4;x=lerp(-35,35,smooth(q));y=300-24*Math.sin(Math.PI*q);}
 return [x*run,300+(y-300)*run];
}
function actor(x,t,color,dir,run=1,raise=0){
 const scale=.84,base=1230-300*scale,phase=t*1.65+(color===C.coral?.37:0),bob=2.5*Math.cos(phase*Math.PI*4)*run;
 const limb=(pts,col,sw)=>`<path d="M${pts.map(p=>p.join(' ')).join(' L')}" fill="none" stroke="${C.paper}" stroke-width="${sw+12}"/><path d="M${pts.map(p=>p.join(' ')).join(' L')}" fill="none" stroke="${col}" stroke-width="${sw}"/>`;
 let legs='',arms='';
 for(let j=0;j<2;j++){
  const [fx,fy]=foot(phase+j*.5,run),hip=[j?18:-18,188+10*run+bob],end=[fx+(j?24:-24),fy];
  const knee=ik(...hip,...end,55,58,1);
  legs+=limb([hip,knee,end],'#374960',25)+`<g transform="translate(${end[0]} ${end[1]})"><path d="M-17 -12 Q-25 -9 -23 0 H22 Q26 -9 7 -13 Z" fill="#f9ecd7" stroke="${C.ink}" stroke-width="4"/></g>`;
  const swing=Math.sin(phase*2*Math.PI+j*Math.PI)*.65*run;
  const sh=[j?35:-35,137+bob];
  let elbow=[sh[0]+Math.sin(swing)*43,sh[1]+Math.cos(swing)*43];
  let hand=[elbow[0]+Math.sin(swing+.8)*38,elbow[1]+Math.cos(swing+.8)*38];
  if(j===1){
   hand=[lerp(hand[0],100,raise),lerp(hand[1],80,raise)];
   elbow=ik(...sh,...hand,44,44,1);
  }
  arms+=limb([sh,elbow,hand],color,22)+`<ellipse cx="${hand[0]}" cy="${hand[1]}" rx="11" ry="13" fill="#f3c7a4" stroke="${C.ink}" stroke-width="4"/>`;
 }
 return `<g data-actor-scale=".84" transform="translate(${x} ${base}) scale(${scale})"><ellipse cx="0" cy="304" rx="65" ry="8" fill="#9b896b" opacity=".18"/><g transform="scale(${dir} 1)">${legs}${arms}<g transform="translate(0 ${bob})" stroke="${C.ink}" stroke-width="4" stroke-linejoin="round"><path d="M-39 117 Q0 104 39 117 L44 205 Q0 219 -44 205 Z" fill="${color}" stroke="${C.paper}" stroke-width="15"/><path d="M-39 117 Q0 104 39 117 L44 205 Q0 219 -44 205 Z" fill="${color}"/>${head}</g></g><rect x="-58" y="149" width="116" height="49" rx="18" fill="${C.paper}" stroke="#dbcbb0" stroke-width="2"/>${text(0,185,color===C.blue?'小甲':'小乙',31,color)}</g>`;
}
function background(cam){
 const o=((cam*2)%300+300)%300,road=((cam*2)%130+130)%130;
 return `<rect x="48" y="326" width="984" height="958" rx="54" fill="#dbe8df"/><circle cx="870" cy="465" r="53" fill="#f4dca0"/><g fill="#f5f1e4"><ellipse cx="206" cy="467" rx="73" ry="17"/><ellipse cx="242" cy="452" rx="40" ry="23"/><ellipse cx="697" cy="550" rx="70" ry="19"/></g><path d="M-90 808 Q160 497 455 756 Q744 470 1160 795 V981 H-90 Z" fill="#abc7ac"/><path d="M-70 900 Q220 650 531 817 Q865 676 1180 918 V981 H-70 Z" fill="#93b592"/>${[-1,0,1,2,3,4].map(i=>`<g transform="translate(${i*300+o-80} 760)"><path d="M0 139 V12" stroke="#647b55" stroke-width="9"/><path d="M-45 109 Q-81 47 -34 21 Q6 -18 30 20 Q88 31 60 89 Q39 131 -45 109 Z" fill="#779d78" stroke="#f5f2e6" stroke-width="8"/></g>`).join('')}<rect x="48" y="944" width="984" height="133" fill="#8f9990"/><path d="M48 957 H1032 M${-200+road} 1017 H1300" stroke="#eee6cf" stroke-width="7" stroke-dasharray="60 70"/><rect x="48" y="1077" width="984" height="207" fill="#e8dcbc"/><path d="M48 1083 H1032" stroke="#fcf2d7" stroke-width="15"/><path d="M48 1212 H1032 ${[-1,0,1,2,3,4].map(i=>`M${i*300+o} 1083 V1212`).join(' ')}" stroke="#d2c6a8" stroke-width="3"/>`;
}
function ruler(a,b,y,label,color,opacity=1){return `<g opacity="${opacity}"><path d="M${a} ${y-13} V${y+13} M${a} ${y} H${b} M${b} ${y-13} V${y+13}" stroke="${color}" stroke-width="4" fill="none"/>${tag((a+b)/2,y-24,label,Math.min(430,Math.max(240,(b-a)*.7)),color)}</g>`;}
function eventState(t){
 let front=412,A=412,B=-180,cam=0,wheel=0,runA=0,runB=0,note='车身15米 · 巴士与甲向西，乙向东';
 if(t>=2&&t<3.6){let p=clamp((t-2)/1.35);front=412-255*p;A=412+255*p;cam=22.5*p;wheel=6*p;runA=smooth((t-2)/.15)*(1-smooth((t-3.3)/.25));note=`同向通过：${(6*p).toFixed(1)}秒`;}
 else if(t>=3.6&&t<4.5){let p=smooth((t-3.6)/.9);front=157+255*p;A=667+213*p;B=lerp(-180,412,p);cam=lerp(22.5,165,p);wheel=6+30*p;runA=smooth((t-3.6)/.16)*(1-smooth((t-4.3)/.2));runB=smooth((t-3.6)/.16);note='再过30秒，车头遇到乙';}
 else if(t>=4.5){let p=clamp((t-4.5)/1.1);front=412-255*p;A=880;B=412+255*p;cam=165+17.5*p;wheel=36+2*p;runA=0;runB=1-smooth((t-5.4)/.25);note=t<6?`迎面通过：${(2*p).toFixed(1)}秒`:'车尾离开乙 · 定格找答案';}
 return {front,A,B,cam,wheel,runA,runB,note};
}
function eventWorld(t){
 const s=eventState(t);
 return background(s.cam)+tag(540,425,s.note,780)+ruler(s.front,s.front+510,710,'整段车身：15米','#a58245')+bus(s.front,818,510,s.wheel)+tag(s.front+30,793,'车头',130)+tag(s.front+480,793,'车尾',130)+actor(s.A,t,C.blue,-1,s.runA)+actor(s.B,t,C.coral,1,s.runB);
}
function elapsedAfterB(t){if(t<23)return 0;if(t<25)return clamp((t-23)/1.4);return 1+15*clamp((t-25)/2.5);}
function diagramWorld(t){
 const u=elapsedAfterB(t),a=600-9.375*u,b=300+9.375*u;
 let run=t<23?0:t<27.15?1:1-smooth((t-27.15)/.35),raise=smooth((t-27.3)/.5);
 let s=background(182.5)+tag(540,425,t<23?'路程图 · 从车尾离甲时算起':u<16?`车尾离乙后，再经过 ${u.toFixed(1)} 秒`:'碰面啦！再过16秒',790);
 s+=`<g opacity="${smooth((t-14.35)/.55)}"><path d="M900 944 V1190" stroke="${C.ink}" stroke-width="6"/><path d="M895 948 H776 L804 980 L776 1010 H895 Z" fill="#dd9062" stroke="${C.ink}" stroke-width="3"/>${text(836,991,'起点',28,C.paper)}${text(900,1268,'0米',28)}</g>`;
 s+=ruler(300,900,635,'车尾走160米','#b78632',smooth((t-16.75)/.35));
 s+=ruler(600,900,730,'小甲走80米',C.blue,smooth((t-18.75)/.35));
 s+=ruler(b,a,835,u===0?'两人相隔80米':`空隙：${Math.max(0,80-5*u).toFixed(u%1===0?0:1)}米`,C.coral,smooth((t-20.75)/.35)*(1-smooth((u-15)/1)));
 s+=actor(a+84,t,C.blue,-1,run,raise)+actor(b-84,t,C.coral,1,run,raise);
 if(t<23)s+=text(300,1268,'乙在160米处',26,C.coral)+text(600,1268,'甲在80米处',26,C.blue);
 if(t>=27.7)s+=`<g opacity="${smooth((t-27.7)/.25)}" stroke="#c78d34" stroke-width="5"><path d="M450 1008 V985 M425 1022 L408 1008 M475 1022 L492 1008"/></g>`;
 const celebration=smooth((t-28)/.65);
 if(celebration>0)s+=`<g opacity="${celebration}"><path d="M60 545 Q540 400 1020 545" stroke="#927657" stroke-width="4" fill="none"/>${Array.from({length:12},(_,i)=>`<path d="M${76+i*79} ${535-Math.sin(i/11*Math.PI)*109} l35 4 -17 28 Z" fill="${[C.gold,C.blue,C.coral][i%3]}"/>`).join('')}</g>`;
 return s;
}
const lessons={
 intro:['巴士生日会 · 先算碰面时间','离开乙后，多久相遇？','车身15米；车速18千米/小时'],
 mystery:['同一辆巴士，速度一直没变','甲6秒 · 乙2秒','离开甲后再过30秒，车头才遇到乙'],
 units:['把巴士速度换成米/秒','18000 ÷ 3600 = 5','18千米＝18000米；1小时＝3600秒'],
 solveA:['同向：巴士速度 − 速度差','5 − 15 ÷ 6 = 2.5','甲速2.5米/秒',C.blue],
 solveB:['迎面：速度和 − 巴士速度','15 ÷ 2 − 5 = 2.5','乙速2.5米/秒',C.coral],
 flag:['车尾离甲时插旗，到离乙共','30 + 2 = 32秒','现在看路程图：起点和时间保持相同'],
 mapbus:['32秒，车尾从起点走了','5 × 32 = 160米','车尾与乙齐平，所以乙在160米处','#b78632'],
 mapA:['同样32秒，小甲从起点走了','2.5 × 32 = 80米','同一个起点，同样的时间',C.blue],
 gap:['甲在80米处，乙在160米处','160 − 80 = 80米','这就是两人之间的剩余距离',C.coral],
 close:['两边一起跑，空隙每秒减少','2.5 + 2.5 = 5','两人的相遇速度：5米/秒',C.coral],
 answer:['剩下距离 ÷ 相遇速度','80 ÷ 5 = 16秒','从车尾离开小乙开始计时',C.coral],
 ending:['谜案破解！一起去生日会','再过16秒相遇！','同向看差，迎面看和',C.coral]
};
function hud(id,line){const [title,formula,detail,color=C.ink]=lessons[id];
 const lines=[...line].length>24?[[...line].slice(0,24).join(''),[...line].slice(24).join('')]:[line];
 return text(540,90,'长长巴士 · 两个跑步伙伴',28,'#8a725d')+text(540,185,titles[id],60)+text(540,258,'30秒精简版 · 动作加速示意',30,'#9a785b')+`<rect x="66" y="1322" width="948" height="333" rx="30" fill="${C.paper}" stroke="#ddceb2" stroke-width="3"/>`+text(540,1391,title,33,color)+text(540,1498,formula,64,color)+text(540,1590,detail,30)+`<rect x="66" y="1700" width="948" height="162" rx="30" fill="${C.paper}" stroke="#ddceb2" stroke-width="3"/>`+lines.map((s,i)=>text(540,lines.length>1?1760+i*51:1790,s,35)).join('');
}
function stateAt(t){return {busWidth:510,actorScale:.84,event:eventState(Math.min(t,14)),elapsed:elapsedAfterB(t),raise:smooth((t-27.3)/.5),paperReveal:smooth((t-14)/.6)};}
function renderAt(t,plan){
 const stage=plan.stages.find(s=>t>=s.start&&t<s.end)||plan.stages.at(-1),index=plan.stages.indexOf(stage),row=plan.captions[index];
 let world;
 if(t<14)world=eventWorld(t);
 else if(t<14.7){const p=smooth((t-14)/.7),x=48+984*(2*p-1);world=(t<14.35?eventWorld(14):diagramWorld(t))+`<g><rect x="${x-9}" y="326" width="1002" height="958" fill="#c8b796" opacity=".2"/><rect x="${x}" y="326" width="984" height="958" fill="#f5ecd9"/><path d="M${x+24} 365 V1245 M${x+960} 365 V1245" stroke="#ddceb2" stroke-width="3"/></g>`;}
 else world=diagramWorld(t);
 // HUD dissolves separately, without changing or duplicating actor geometry.
 const p=smooth((t-stage.start)/.18);let ui=`<g opacity="${index===0?1:p}">${hud(stage.id,row.text)}</g>`;
 if(index>0&&p<1)ui+=`<g opacity="${1-p}">${hud(plan.stages[index-1].id,plan.captions[index-1].text)}</g>`;
 const fade=smooth(t/.25)*smooth((30-t)/.35),edge=48+984*smooth((t-14)/.6);
 return `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920"><defs><clipPath id="world"><rect x="48" y="326" width="984" height="958" rx="54"/></clipPath><clipPath id="paperwipe"><rect x="48" y="326" width="${Math.max(0,edge-48)}" height="958"/></clipPath><pattern id="grain" width="86" height="83" patternUnits="userSpaceOnUse"><circle cx="9" cy="13" r=".7" fill="#886c4b" opacity=".10"/><path d="M27 41 l7 -1 M68 64 l9 1" stroke="#8e7150" stroke-width=".8" opacity=".09"/></pattern></defs><rect width="1080" height="1920" fill="${C.cream}"/><g opacity="${fade}" font-family="Microsoft YaHei, SimHei, sans-serif"><g clip-path="url(#world)">${world}</g>${ui}<path d="M66 1890 H${66+948*t/30}" stroke="${C.coral}" stroke-width="5" stroke-linecap="round"/></g><rect width="1080" height="1920" fill="url(#grain)"/></svg>`;
}
module.exports={renderAt,stateAt,actor,eventState,elapsedAfterB,ik};
