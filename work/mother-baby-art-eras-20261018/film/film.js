/* Portrait family adaptation. See THIRD_PARTY_NOTICES.md for pinned reference.
 * Shared absolute clock and 2-bone IK follow the studied reference mechanism.
 * All paths, portrait layouts, baby rig, costumes and era artwork below are new.
 */
(()=>{
const cv=document.getElementById('film'),ctx=cv.getContext('2d'),W=1080,H=1920;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)),mix=(a,b,t)=>a+(b-a)*t;
const ease=x=>{x=clamp(x);return x*x*(3-2*x)};
const rng=seed=>()=>{seed|=0;seed=(seed+0x6d2b79f5)|0;let z=Math.imul(seed^seed>>>15,1|seed);z^=z+Math.imul(z^z>>>7,61|z);return((z^z>>>14)>>>0)/4294967296};
const pt=(a,b,p)=>[mix(a[0],b[0],p),mix(a[1],b[1],p)];
// Adapted two-bone inverse kinematics; full attribution in notices.
function ik(S,T,a,b,bend=-1){const dx=T[0]-S[0],dy=T[1]-S[1],d=clamp(Math.hypot(dx,dy),Math.abs(a-b)+.001,a+b-.001);const ang=Math.atan2(dy,dx),e=ang+bend*Math.acos(clamp((a*a+d*d-b*b)/(2*a*d),-1,1));return[S[0]+a*Math.cos(e),S[1]+a*Math.sin(e)]}
const paths=new Map();const P=d=>{if(!paths.has(d))paths.set(d,new Path2D(d));return paths.get(d)};
const ellipse=(x,y,rx,ry=rx)=>{let p=new Path2D();p.ellipse(x,y,rx,ry,0,0,Math.PI*2);return p};
const poly=pts=>{let p=new Path2D();pts.forEach((v,i)=>i?p.lineTo(...v):p.moveTo(...v));p.closePath();return p};
const rr=(x,y,w,h,r)=>{let p=new Path2D();p.roundRect(x,y,w,h,r);return p};
function line(c,pts,col,w=3){c.beginPath();pts.forEach((v,i)=>i?c.lineTo(...v):c.moveTo(...v));c.strokeStyle=col;c.lineWidth=w;c.lineCap='round';c.lineJoin='round';c.stroke()}
function limb(c,A,B,w,col,s){const a=Math.atan2(B[1]-A[1],B[0]-A[0]),p=new Path2D();p.moveTo(A[0],A[1]);p.lineTo(B[0],B[1]);c.save();c.lineCap='round';c.strokeStyle=s.outline;c.lineWidth=w+s.lw*2;if(s.lw)c.stroke(p);c.strokeStyle=col;c.lineWidth=w;c.stroke(p);c.restore()}
const textureCache=new Map(),backgroundCache=new Map();
function texture(s){if(textureCache.has(s.mode))return textureCache.get(s.mode);const q=document.createElement('canvas');q.width=q.height=160;const c=q.getContext('2d'),r=rng(s.year+50001);
 const n=['pointill','mosaic','dots','pop','comic'].includes(s.mode)?230:170;
 for(let i=0;i<n;i++){const x=r()*160,y=r()*160; c.fillStyle=i%3?'#fff8e640':s.line+'28';
 if(['impression','postimp','watercolor','blue'].includes(s.mode)){c.save();c.translate(x,y);c.rotate(s.mode==='postimp'?r()*3.14:-.4);c.fillRect(0,0,3+r()*3,7+r()*12);c.restore()}
 else if(s.mode==='ink'){c.fillRect(x,y,.5+r()*1.5,2+r()*5)}
 else if(s.mode==='mosaic'){c.fillStyle=i%2?'#fff5d970':s.line+'55';c.strokeStyle=s.wall;c.lineWidth=1;c.fillRect(Math.floor(x/12)*12,Math.floor(y/12)*12,10,10)}
 else {c.beginPath();c.arc(x,y,s.mode==='pointill'?2.5+r()*2:.6+r(),0,7);c.fill()}}
 if(['pop','comic','dots'].includes(s.mode)){for(let x=5;x<160;x+=11)for(let y=5;y<160;y+=11){c.fillStyle=s.line+'60';c.beginPath();c.arc(x,y,s.mode==='dots'?3:1.7,0,7);c.fill()}}
 if(s.mode==='digital'||s.mode==='vapor'){for(let n=0;n<160;n+=16)line(c,[[n,0],[n,160]],s.line+'55',1);for(let n=0;n<160;n+=16)line(c,[[0,n],[160,n]],s.line+'55',1)}
 const pattern=ctx.createPattern(q,'repeat');textureCache.set(s.mode,pattern);return pattern}
function style(era){const m=era.mode,mono=['cave','greek','puppet','ink','rubber','haring'].includes(m),s={...era};s.outline=era.line;s.lw=['comic','pop'].includes(m)?4:m==='haring'?6:m==='cutout'?0:['egypt','greek','gothic','cubism','rubber'].includes(m)?2.7:1.1;s.hair=['greek','cave','puppet'].includes(m)?era.line:'#49332d';s.skin=['greek','cave'].includes(m)?era.wall:m==='puppet'?era.line:era.skin;s.cream=m==='blue'?'#bdd3d9':m==='ink'?'#f5efde':m==='rubber'?'#ece3d0':'#fff2d7';s.navy=m==='vapor'?'#6a5b9c':m==='blue'?'#38667d':m==='rubber'?'#484940':era.line;if(['greek','cave','puppet'].includes(m)){s.skin=s.line;s.dress=s.line;s.cream=s.line;s.outline=s.wall;s.lw=1.7;}if(['ink','rubber','comic','pop'].includes(m))s.hair=s.line;if(m==='haring'){s.skin=s.wall;s.hair=s.wall;s.cream=s.green;}s.feature=['greek','cave','puppet'].includes(m)?era.wall:m==='rembrandt'?'#48372c':era.line;s.blush=mono?s.skin:'#efab91';s.grain=texture(s);return s}
function fill(c,p,col,s,tex=true){if(!col)return;c.save();c.fillStyle=col;c.fill(p);if(s&&s.lw){c.strokeStyle=s.outline;c.lineWidth=s.lw;c.lineJoin='round';c.stroke(p)}if(s&&tex){c.clip(p);c.globalAlpha=['pointill','mosaic'].includes(s.mode)?.75:.38;c.fillStyle=s.grain;c.fillRect(0,0,W,H)}c.restore()}
function star(c,x,y,r,col,s,rot=0){const p=[];for(let i=0;i<10;i++){const a=-Math.PI/2+i*Math.PI/5+rot,z=i%2?r*.48:r;p.push([x+Math.cos(a)*z,y+Math.sin(a)*z])}fill(c,poly(p),col,s);if(s.mode!=='greek'&&s.mode!=='cave'){fill(c,ellipse(x-r*.17,y,1.6),s.line,null);fill(c,ellipse(x+r*.17,y,1.6),s.line,null);c.beginPath();c.arc(x,y+r*.02,r*.12,.2,Math.PI-.2);c.strokeStyle=s.line;c.lineWidth=1.5;c.stroke()}}
function leaf(c,x,y,sz,a,col,s){c.save();c.translate(x,y);c.rotate(a);fill(c,P(`M0 0 C${-sz} ${-sz*.1} ${-sz*.8} ${-sz*1.3} 0 ${-sz*1.5} C${sz*.8} ${-sz*1.3} ${sz} ${-sz*.1} 0 0Z`),col,s);line(c,[[0,-sz*.1],[0,-sz*1.3]],s?.wall||'#f4e6cc',2);c.restore()}
function plant(c,x,y,h,s,kind=0,t=0){const sw=Math.sin(t*1.1+x)*.055;c.save();c.translate(x,y);c.rotate(sw);for(let i=0;i<7;i++){const a=-.85+i*.27,dy=-h*(.35+i%4*.12);line(c,[[0,-25],[Math.sin(a)*h*.4,dy]],s.green,5);leaf(c,Math.sin(a)*h*.4,dy,h*.16,a,s.green,s)}c.restore();fill(c,poly([[x-57,y-55],[x+57,y-55],[x+44,y+30],[x-42,y+30]]),kind?s.green:s.dress,s);line(c,[[x-49,y-34],[x+49,y-34]],s.cream,9)}
function border(c,s){const m=s.mode;c.save();c.strokeStyle=s.line;c.lineWidth=3;
 if(['egypt','greek','dunhuang','puppet','gothic','nouveau','gold','mosaic'].includes(m)){c.strokeRect(32,32,1016,1856);c.strokeRect(43,43,994,1834);
 for(let i=0;i<24;i++){const x=66+i*41;if(m==='greek'){line(c,[[x,65],[x+27,65],[x+27,87],[x+11,87],[x+11,75]],s.line,4);line(c,[[x,1838],[x+27,1838],[x+27,1816],[x+11,1816]],s.line,4)}else fill(c,ellipse(x,65,3),s.dress,null)}
 if(['nouveau','dunhuang','gothic','gold'].includes(m))for(const x of[61,1019]){for(let y=180;y<1780;y+=85){line(c,[[x,y-35],[x+(x<500?13:-13),y],[x,y+35]],s.green,3);leaf(c,x,y,17,x<500?.7:-.7,s.green,s)}}}
 if(m==='comic'){c.lineWidth=8;c.strokeRect(38,38,1004,1844)}c.restore()}
function background(s){if(backgroundCache.has(s.mode))return backgroundCache.get(s.mode);let b=document.createElement('canvas');b.width=W;b.height=H;let c=b.getContext('2d');c.fillStyle=s.wall;c.fillRect(0,0,W,H);const m=s.mode;
 const dark=['rembrandt','blue','digital','vapor'].includes(m);const floor=dark?s.green:s.mode==='ink'?'#ebe5d4':s.mode==='greek'?s.line:'#eaddc3';fill(c,rr(0,1360,W,560,0),floor,null,false);
 // One vertical room, all objects share the same portrait world coordinates.
 if(['modern','pop','dots','bauhaus','haring','cutout','comic','pixel','digital','vapor'].includes(m)){
  fill(c,ellipse(239,740,320,500),m==='modern'?'#f7d5c8':s.dress+'55',null);fill(c,ellipse(837,1130,222,292),m==='modern'?'#dfd8ef':s.green+'55',null);
  if(m==='construct'||m==='comic')fill(c,poly([[0,300],[1080,620],[1080,900],[0,580]]),s.dress,null);
 }
 if(['renaissance','gothic','rembrandt','egypt','dunhuang'].includes(m)){fill(c,rr(108,247,430,740,200),s.green,s);fill(c,rr(127,266,392,703,184),s.cream,s)}
 else if(!['cave','ink','surreal','lilies'].includes(m))fill(c,rr(100,335,430,695,m==='cubism'?0:24),s.cream,s);
 if(!['cave','ink','surreal','lilies'].includes(m)){
  const sky=['greek','puppet'].includes(m)?s.wall:dark?s.green:s.year<1500?s.wall:'#b9dee6';let win=rr(124,359,382,641,['gothic','renaissance'].includes(m)?165:10);fill(c,win,sky,null);c.save();c.clip(win);
  fill(c,ellipse(401,500,53),['greek','puppet'].includes(m)?s.line:'#eeb654',null);
  if(s.year>=1500)for(let i=0;i<5;i++){let x=115+i*84,h=[130,190,150,240,178][i];fill(c,rr(x,1000-h,83,h,i%2?35:0),[s.green,s.dress,s.navy,s.green,s.dress][i],null);for(let j=0;j<3;j++)for(let k=0;k<3;k++)fill(c,rr(x+12+j*22,1020-h+k*40,9,15,0),s.cream,null)}
  if(s.year<1500){for(let i=0;i<4;i++){const x=155+i*100;fill(c,poly([[x-55,960],[x,780-i%2*50],[x+80,960]]),i%2?s.green:s.dress,null);}if(m==='gothic'){for(let i=0;i<4;i++)fill(c,poly([[150+i*85,480],[190+i*85,420],[230+i*85,480],[190+i*85,590]]),i%2?s.green:s.dress,s);}}if(['watercolor','anime','impression','pointill','renaissance','postimp','nouveau','dunhuang','blue'].includes(m)){for(let i=0;i<18;i++){let x=112+i*24;fill(c,ellipse(x,890+Math.sin(i)*17,28,77),s.green,null);fill(c,ellipse(x,825+Math.sin(i)*37,7),s.dress,null)}}
  c.restore();if(s.year>=1500){line(c,[[315,353],[315,1012]],s.cream,16);line(c,[[116,672],[512,672]],s.cream,16)}else if(m==='egypt'||m==='greek'){line(c,[[107,392],[107,1000]],s.green,24);line(c,[[520,392],[520,1000]],s.green,24);line(c,[[92,380],[535,380]],s.green,22)}fill(c,rr(85,1015,462,20,8),s.cream,s)}
 // Historical environments are redrawn, not background filters.
 if(m==='cave'){for(const [x,y,z]of[[238,680,1],[627,360,.65],[853,831,.8]]){c.save();c.translate(x,y);c.scale(z,z);line(c,[[-80,25],[-30,-7],[80,7],[99,32],[63,37],[53,79]],s.line,8);line(c,[[-40,18],[-53,76]],s.line,8);line(c,[[77,3],[89,-36],[103,-11],[127,-29]],s.line,6);c.restore()}for(let i=0;i<19;i++)line(c,[[60+i*53,175],[48+i*53,205]],s.line,3)}
 if(m==='egypt'){for(let i=0;i<6;i++){const x=82+i*89;line(c,[[x,170],[x+20,145],[x+38,170]],s.line,3);fill(c,ellipse(x+20,183,5),s.green,null);line(c,[[x+20,190],[x+20,215],[x+5,228]],s.line,3)}fill(c,poly([[670,910],[825,650],[980,910]]),s.dress+'66',null)}
 if(m==='greek'){for(let i=0;i<3;i++)fill(c,rr(650+i*100,480,32,430,0),s.line,null);line(c,[[619,460],[1004,460]],s.line,18);line(c,[[605,928],[1017,928]],s.line,14)}
 if(m==='dunhuang'){for(let i=0;i<8;i++){let x=700+i*35;line(c,[[x,400],[x+20,442],[x-20,485],[x+15,525]],s.dress,3)}for(let i=0;i<7;i++)leaf(c,780+Math.cos(i)*90,720+Math.sin(i)*60,65,i,s.green,s)}
 if(m==='puppet'){c.strokeStyle=s.dress;c.lineWidth=6;for(let x=70;x<1080;x+=95){c.beginPath();c.moveTo(x,140);c.bezierCurveTo(x+60,250,x-20,280,x+40,320);c.stroke()}fill(c,ellipse(800,610,96),s.dress+'44',null)}
 if(m==='ink'){line(c,[[130,1090],[140,410]],s.green,10);line(c,[[158,1090],[190,490]],s.green,7);for(let y=460;y<1030;y+=90){leaf(c,139,y,40,-.9,s.line,s);leaf(c,180,y+35,40,.7,s.green,s)}for(let i=0;i<3;i++){c.strokeStyle=s.green+'66';c.lineWidth=3;c.beginPath();c.moveTo(540+i*80,1000);c.quadraticCurveTo(660+i*80,610,840+i*50,985);c.stroke()}}
 if(m==='lilies'){fill(c,rr(92,325,890,683,95),s.green,null);for(let i=0;i<28;i++){let r=rng(i+4),x=120+r()*800,y=370+r()*610;fill(c,ellipse(x,y,25+r()*48,12+r()*12),i%3?s.wall:s.dress,null);if(i%5===0)fill(c,ellipse(x,y-4,9,6),s.cream,null)}}
 if(m==='gold'){for(let x=70;x<1020;x+=54)for(let y=330;y<1240;y+=55){fill(c,rr(x,y,15,28,2),(x+y)%3?s.green:s.line,null);fill(c,ellipse(x+25,y+25,4),s.cream,null)}}
 if(m==='cubism'){for(const [d,col]of[['M600 390L1000 540L803 840Z',s.green],['M600 390L803 840L640 1080Z',s.dress],['M803 840L1000 540L1010 1100Z',s.navy]])fill(c,P(d),col+'77',null)}
 if(m==='bauhaus'){fill(c,ellipse(823,620,135),s.dress,null);fill(c,rr(672,800,250,95,0),s.navy,null);fill(c,poly([[721,1040],[934,1040],[934,823]]),'#e9bb48',null)}
 if(m==='construct'){fill(c,poly([[70,400],[1040,220],[1040,530],[70,710]]),s.dress,null);line(c,[[90,940],[1000,720]],s.line,22)}
 if(m==='surreal'){fill(c,poly([[100,1000],[340,720],[535,1000]]),s.green,null);fill(c,ellipse(805,610,85,132),s.cream,s);line(c,[[805,545],[805,624],[851,652]],s.line,5);fill(c,P('M721 640Q805 710 875 675L866 810Q819 851 806 756Q786 734 721 725Z'),s.cream,s)}
 if(m==='hopper'||m==='rembrandt'){fill(c,poly([[0,870],[500,590],[930,1150],[520,1350]]),m==='rembrandt'?'#c2945950':'#f6e6a6',null);line(c,[[700,450],[1000,450],[1000,1100],[700,1100],[700,450]],s.green,13)}
 if(m==='cutout'){for(let i=0;i<8;i++)leaf(c,710+(i%3)*95,470+Math.floor(i/3)*190,80,(i%2?.9:-.9),[s.green,s.dress,s.navy][i%3],null)}
 if(['dots','pop','comic','haring'].includes(m)){for(let x=680;x<1040;x+=43)for(let y=380;y<990;y+=43)fill(c,ellipse(x,y,m==='dots'?10:3),s.line+'55',null)}
 if(m==='haring'){for(let i=0;i<5;i++)line(c,[[700+i*60,500],[680+i*60,540],[710+i*60,580]],s.line,6)}
 if(m==='digital'||m==='vapor'){for(let y=1460;y<1920;y+=55)line(c,[[0,y],[1080,y]],s.line+'55',2);for(let i=-8;i<12;i++)line(c,[[540,1360],[540+i*110,1920]],s.line+'55',2);for(let x=650;x<1000;x+=55)line(c,[[x,400],[x,1000]],s.line+'44',2)}
 if(m==='postimp'||m==='expression'){for(let i=0;i<22;i++){c.strokeStyle=(i%2?s.green:s.line)+'55';c.lineWidth=5;c.beginPath();c.ellipse(760,670,60+i*10,25+i*7,i*.1,0,Math.PI*1.65);c.stroke()}}
 if(m==='nouveau'){for(let i=0;i<9;i++)leaf(c,745+(i%3)*68,450+Math.floor(i/3)*160,60,i*.75,s.green,s)}
 if(m==='rubber'){line(c,[[675,730],[950,730],[950,900],[675,900],[675,730]],s.line,6);for(let i=0;i<7;i++)fill(c,ellipse(710+i*32,810,8),s.line,null)}
 if(['modern','impression','watercolor','anime','pixel'].includes(m)){fill(c,rr(708,525,260,18,4),'#c49259',s);for(let i=0;i<6;i++)fill(c,rr(730+i*33,430-(i%3)*15,27,95+(i%3)*15,2),[s.dress,s.green,s.navy][i%3],s);fill(c,rr(760,295,176,113,0),'#ca9a65',s);fill(c,rr(770,305,156,93,0),s.cream,null);fill(c,ellipse(879,338,22),'#eeb954',null);leaf(c,815,386,40,-.4,s.green,null)}
 // Portrait lamp and small graphic decoration.
 if(!['cave','greek','ink','lilies'].includes(m)){if(s.year<1500){line(c,[[551,0],[551,346],[579,380],[607,346],[607,0]],s.line,3);fill(c,P('M540 375Q579 419 618 375Z'),s.dress,s);fill(c,P('M572 377Q560 349 581 335Q594 359 586 377Z'),'#e5ab43',s)}else{line(c,[[579,0],[579,338]],s.line,4);fill(c,P('M507 402Q509 328 579 328Q650 328 651 402Z'),s.dress,s);fill(c,ellipse(579,403,22,9),'#efc15b',null)}}
 if(!['cave','ink'].includes(m)){for(const [x,y]of[[640,810],[880,345],[735,930]]){line(c,[[x-7,y],[x+7,y]],s.dress,4);line(c,[[x,y-7],[x,y+7]],s.dress,4)}}
 if(s.mode==='comic')fill(c,poly([[660,780],[740,720],[760,780],[820,740],[810,825],[900,830],[850,860],[870,920],[790,900],[750,950],[730,890],[660,910],[690,855]]),s.cream,s);
 c.save();c.globalAlpha=.42;c.fillStyle=s.grain;c.fillRect(0,0,W,H);c.restore();border(c,s);backgroundCache.set(s.mode,b);return b}
function motion(t){const ph=(t%3.2)/3.2,reach=ease(ph/.20);let lift=ph<.28?0:ph<.50?ease((ph-.28)/.22):ph<.67?1:1-ease((ph-.67)/.25);const sip=ph<.52?0:ph<.60?ease((ph-.52)/.08):1-ease((ph-.60)/.07);const held=ph>=.20&&ph<.94;return{ph,reach,lift,sip,held,release:ease((ph-.94)/.06)}}
function headPoint(x,y,a){const ox=779,oy=1152;return[ox+(x-ox)*Math.cos(a)-(y-oy)*Math.sin(a),oy+(x-ox)*Math.sin(a)+(y-oy)*Math.cos(a)]}
function cupPose(a,sip,headAngle){const mouth=headPoint(713,1118,headAngle),tilt=.13*sip;const top=pt([610,1250],[mouth[0]-22*Math.cos(tilt),mouth[1]-22*Math.sin(tilt)],a);return{x:top[0],y:top[1],tilt,w:44,h:37,mouth,grip:[top[0]+35*Math.cos(tilt)-18*Math.sin(tilt),top[1]+35*Math.sin(tilt)+18*Math.cos(tilt)]}}
function cup(c,C,s){c.save();c.translate(C.x,C.y);c.rotate(C.tilt);let p=P('M-22 0L-18 32Q0 40 18 32L22 0Z');fill(c,p,s.cream,s);c.strokeStyle=s.cream;c.lineWidth=7;c.beginPath();c.ellipse(27,15,11,12,0,-1.4,1.4);c.stroke();if(s.lw){c.strokeStyle=s.outline;c.lineWidth=1.5;c.beginPath();c.ellipse(27,15,11,12,0,-1.4,1.4);c.stroke()}fill(c,ellipse(0,0,22,4),s.line,null);line(c,[[-20,0],[20,0]],s.cream,2);c.restore()}
function mother(c,s,a,t){const m=s.mode,old=s.year<1900,ha=-.025*a.sip;const C=cupPose(a.lift,a.sip,ha);let wrist=a.held?C.grip:pt([786,1327],C.grip,a.ph<.20?a.reach:1-a.release);const shoulder=[791,1193],elbow=ik(shoulder,wrist,91,88,-1);
 // Chair, legs, lap and torso are separate explicit drawing parts.
 if(s.year>=1900)fill(c,rr(822,1210,36,208,16),s.green,s);else if(['gothic','renaissance','rembrandt'].includes(m)){fill(c,P('M822 1400L822 1166Q842 1135 861 1166L861 1400Z'),s.green,s);for(let i=0;i<4;i++)line(c,[[828+i*8,1188],[828+i*8,1375]],s.cream,2)}fill(c,rr(734,1381,128,24,old?2:10),s.green,s);line(c,[[752,1401],[741,1507]],s.green,9);line(c,[[851,1400],[866,1503]],s.green,9);
 if(old){fill(c,P('M757 1311Q706 1306 681 1343L666 1490Q708 1515 774 1488L809 1375Z'),s.dress,s);line(c,[[712,1373],[704,1469]],s.line+'77',2)}else{fill(c,P('M780 1327Q733 1315 692 1340Q677 1349 677 1370L690 1489L735 1489L737 1386L806 1387Q831 1367 812 1342Z'),s.navy,s);fill(c,P('M731 1387L745 1487L785 1487L789 1378Z'),s.navy,s)}
 fill(c,P('M686 1479Q665 1480 655 1497Q653 1507 669 1510L734 1510L731 1486Z'),s.cream,s);line(c,[[664,1508],[733,1508]],s.dress,4);fill(c,P('M744 1484Q725 1494 725 1508Q738 1518 791 1511L786 1485Z'),s.cream,s);
 fill(c,P('M752 1157Q722 1165 725 1216L740 1307Q761 1342 823 1338L835 1232Q838 1180 798 1157Z'),s.dress,s);
 if(!old)fill(c,P('M763 1157L783 1154L799 1307L767 1310Z'),s.cream,s);else{line(c,[[752,1169],[777,1213],[799,1172]],s.green,8);line(c,[[777,1213],[786,1307]],s.green,4);}
 // Period costume details are planar, no shaded fabric.
 if(['egypt','greek'].includes(m)){line(c,[[741,1188],[809,1188]],s.green,12);line(c,[[739,1203],[809,1203]],s.cream,5);for(let i=0;i<4;i++)line(c,[[696+i*20,1372],[685+i*23,1485]],s.feature+'80',2)}
 if(m==='cave'){fill(c,P('M741 1174L799 1160L830 1315L808 1342L785 1320L761 1341L739 1307Z'),s.green,s);for(const [x,y] of [[763,1223],[793,1240],[775,1290]])fill(c,ellipse(x,y,5,8),s.line,null)}
 if(m==='renaissance'||m==='rembrandt'){fill(c,P('M739 1169L778 1201L814 1165L808 1189L779 1219L746 1193Z'),s.cream,s);line(c,[[752,1244],[810,1235]],s.green,11)}
 if(['dunhuang','nouveau','gold','gothic'].includes(m)){for(let i=0;i<8;i++)fill(c,ellipse(755+(i%2)*48,1211+Math.floor(i/2)*25,3),s.cream,null);line(c,[[750,1173],[760,1270],[792,1320]],s.green,7)}
 if(m==='cubism'){fill(c,poly([[740,1200],[783,1240],[744,1305]]),s.green,s);fill(c,poly([[792,1176],[830,1247],[792,1279]]),s.navy,s)}
 if(m==='bauhaus'||m==='cutout')fill(c,ellipse(800,1260,16),s.green,null);
 if(m==='comic'||m==='pop'||m==='dots')for(let x=738;x<824;x+=13)for(let y=1210;y<1300;y+=14)fill(c,ellipse(x,y,1.5),s.line+'77',null);
 // Resting far arm and hand on the lap.
 limb(c,[810,1210],[826,1289],29,s.dress,s);limb(c,[826,1289],[774,1320],24,s.dress,s);fill(c,ellipse(771,1320,20,11),s.skin,s);
 c.save();c.translate(779,1152);c.rotate(ha);c.translate(-779,-1152);
 const hairBack=m==='egypt'?'M711 1049L741 1016L795 1017L826 1054L842 1181L785 1181L742 1145Z':m==='cubism'?'M716 1055L737 1012L786 1014L835 1066L842 1174L795 1187L741 1148Z':['greek','dunhuang','ink'].includes(m)?'M715 1055Q712 1018 759 1016Q804 1011 822 1064L825 1149Q807 1170 779 1155L741 1148Z':'M716 1055Q715 1010 763 1014Q821 1012 835 1066L842 1174Q812 1192 779 1176L741 1148Z';
 if(['greek','dunhuang','ink'].includes(m))fill(c,ellipse(810,1025,27,29),s.hair,s);fill(c,P(hairBack),s.hair,s);
 if(m==='egypt')for(let x=787;x<827;x+=9)line(c,[[x,1046],[x+10,1175]],s.green,4);
 if(['gothic','renaissance','rembrandt'].includes(m)){fill(c,P('M712 1055Q725 998 770 1005Q815 1001 836 1060L844 1175L821 1162L812 1063Q769 1027 721 1065Z'),s.cream,s);line(c,[[722,1039],[785,1018],[824,1052]],s.dress,4)}
 fill(c,P(['cubism','egypt'].includes(m)?'M720 1050L764 1032L798 1070L782 1126L746 1156L712 1129L700 1104Z':'M724 1049Q748 1029 774 1044Q801 1060 795 1100Q793 1130 761 1150Q735 1157 720 1133L705 1108L712 1095Q707 1073 724 1049Z'),s.skin,s);
 fill(c,ellipse(794,1106,12,16),s.skin,s);line(c,[[791,1102],[797,1106],[793,1111]],s.blush,2);
 fill(c,P(m==='cubism'?'M716 1057L740 1028L771 1034L803 1097L841 1176L814 1188L798 1160L781 1086L746 1050L716 1071Z':m==='egypt'?'M716 1057L735 1028L772 1032L800 1069L811 1176L790 1169L775 1073L742 1050L716 1071Z':'M716 1057Q736 1012 771 1034Q791 1048 803 1097L813 1138Q835 1173 841 1176Q814 1188 798 1160L781 1086Q767 1061 746 1050Q730 1048 716 1071Z'),s.hair,s);
 if(['dunhuang','ink','nouveau'].includes(m)){line(c,[[796,1047],[827,1020]],s.cream,4);fill(c,ellipse(828,1019,7),s.dress,s)}
 // Glasses and eyes stay recognizable even as the era drawing changes.
 const f=s.feature;for(const [x,y,r]of[[728,1086,17],[767,1084,19]]){c.strokeStyle=f;c.lineWidth=['comic','haring'].includes(m)?3.3:2.3;c.beginPath();c.ellipse(x,y,r,r*.91,0,0,7);c.stroke()}line(c,[[745,1083],[748,1083]],f,2);line(c,[[786,1082],[795,1076]],f,2);
 const blink=(Math.floor(t*2.7)%19===11);if(blink){line(c,[[721,1088],[730,1088]],f,2);line(c,[[758,1087],[768,1087]],f,2)}else{fill(c,ellipse(724,1087,2.8,4.2),f,null);fill(c,ellipse(761,1086,3,4.5),f,null)}
 line(c,[[716,1067],[729,1065]],f,2);line(c,[[756,1063],[771,1064]],f,2);line(c,[[712,1095],[706,1105],[715,1107]],f,1.6);line(c,[[714,1118],[722,1121],[730,1118]],f,1.8);fill(c,ellipse(746,1115,8,5),s.blush,null);
 if(['egypt','greek','gothic','dunhuang'].includes(m)){line(c,[[719,1052],[787,1047]],s.cream,6);fill(c,ellipse(755,1047,4),s.green,null)}
 if(m==='haring')for(let i=0;i<3;i++)line(c,[[704-i*10,1038],[698-i*10,1024]],s.line,3);
 c.restore();
 // Near arm is solved from the same cup target; no floating prop animation.
 limb(c,shoulder,elbow,34,s.dress,s);limb(c,elbow,[wrist[0]+3,wrist[1]+5],27,s.dress,s);fill(c,ellipse(wrist[0]+2,wrist[1]+7,12,13),s.skin,s);
 cup(c,C,s);fill(c,ellipse(wrist[0]-1,wrist[1],5,8),s.skin,s);for(let i=0;i<3;i++)line(c,[[wrist[0]+1,wrist[1]-5+i*4],[wrist[0]+7,wrist[1]-4+i*4]],s.blush,1);
 return{wrist,grip:C.grip,mouth:C.mouth,cup:C};}
 function baby(c,s,a,t){const m=s.mode,ancient=s.year<1500,lean=(1-a.lift)*5;const shoulder=[385+lean,1419],toy=pt([455,1495],[431,1380],a.lift);const grip=[toy[0]-17,toy[1]-6];const wrist=a.held?grip:pt([371,1474],grip,a.ph<.20?a.reach:1-a.release),elbow=ik(shoulder,wrist,54,54,1);
 fill(c,P('M306 1400Q337 1380 367 1401L391 1455Q385 1496 337 1499Q303 1496 289 1473Z'),s.cream,s);
 fill(c,P('M306 1468Q282 1467 273 1484Q270 1507 291 1520L330 1514Q331 1492 306 1468Z'),s.cream,s);fill(c,P('M353 1468Q385 1464 411 1491Q418 1508 395 1515L357 1503Z'),s.cream,s);
 fill(c,ellipse(293,1504,20,15),s.skin,s);fill(c,ellipse(397,1504,18,13),s.skin,s);
 limb(c,[311,1413],[299,1461],22,s.cream,s);fill(c,ellipse(301,1472,14,9),s.skin,s);
 // Simple bib uses the same era pattern as the character, not a separate bitmap.
 fill(c,P(ancient?'M304 1390L334 1406L366 1388L373 1410L343 1432L306 1412Z':'M308 1392Q336 1410 363 1393L374 1420Q340 1450 304 1420Z'),s.green,s);for(let i=0;i<4;i++)fill(c,ellipse(313+i*14,1414+(i%2)*7,2.8),s.cream,null);
 if(ancient){line(c,[[309,1435],[321,1486]],s.green,4);line(c,[[362,1432],[354,1480]],s.green,4);if(m==='egypt')line(c,[[301,1446],[379,1446]],s.dress,6)}else if(s.year>=1950){for(let y=1435;y<1490;y+=12)line(c,[[312,y],[371,y]],s.dress+'88',3)}
 c.save();c.translate(lean,lean*.5);fill(c,['cubism','egypt'].includes(m)?poly([[292,1320],[317,1291],[363,1297],[389,1330],[382,1380],[344,1402],[307,1387]]):ellipse(340,1346,55,57),s.skin,s);
 fill(c,P('M286 1330Q281 1302 308 1285Q341 1269 370 1290Q385 1301 389 1320L378 1313Q347 1287 308 1306Z'),s.hair,s);
 // Few short strokes imply the baby's very short hair, without realistic texture.
 for(let i=0;i<19;i++){let x=290+i*5;line(c,[[x,1313-Math.sin(i/19*Math.PI)*23],[x+1,1306-Math.sin(i/19*Math.PI)*27]],s.hair,1.6)}
 if(['egypt','dunhuang','gothic'].includes(m)){line(c,[[291,1310],[382,1308]],s.green,5);fill(c,ellipse(337,1308,4),s.cream,null)}
 fill(c,ellipse(287,1348,9,13),s.skin,s);fill(c,ellipse(393,1345,8,12),s.skin,s);
 for(const [x,y]of[[317,1346],[366,1343]]){c.beginPath();c.ellipse(x,y+3,8,5,0,Math.PI+.25,Math.PI*2-.25);c.strokeStyle=s.feature;c.lineWidth=2.5;c.stroke()}
 line(c,[[333,1353],[332,1359],[338,1360]],s.feature,1.3);fill(c,P('M325 1370Q340 1376 354 1366Q355 1385 341 1387Q329 1385 325 1370Z'),s.feature,s,false);fill(c,ellipse(340,1382,6,3),s.blush,null);fill(c,ellipse(307,1364,9,5),s.blush,null);fill(c,ellipse(376,1361,8,5),s.blush,null);c.restore();
 limb(c,shoulder,elbow,23,s.cream,s);limb(c,elbow,wrist,21,s.cream,s);fill(c,ellipse(wrist[0],wrist[1],10,11),s.skin,s);
 star(c,toy[0],toy[1],25,s.mode==='ink'?s.dress:'#efbc50',s,-.15+a.lift*.3);fill(c,ellipse(wrist[0]+4,wrist[1]-3,5,6),s.skin,s);
 return{wrist,grip,toy,held:a.held};}
function table(c,s){if(s.year<1500){fill(c,poly([[518,1282],[538,1282],[548,1496],[529,1496]]),s.green,s);fill(c,poly([[657,1282],[676,1282],[663,1496],[644,1496]]),s.green,s);fill(c,rr(504,1271,187,23,2),s.navy,s);line(c,[[535,1444],[657,1444]],s.green,8);if(s.mode==='egypt')for(let i=0;i<9;i++)fill(c,poly([[510+i*20,1280],[519+i*20,1288],[529+i*20,1280]]),s.cream,null)}else{fill(c,rr(589,1281,16,205,7),s.navy,s);fill(c,rr(544,1480,108,17,8),s.navy,s);fill(c,ellipse(596,1282,105,13),s.navy,s)}fill(c,ellipse(610,1280,34,5),s.cream,s);fill(c,rr(542,1249,27,29,6),s.cream,s);for(let i=0;i<3;i++){line(c,[[555,1252],[546+(i*11),1223-i%2*8]],s.green,2);fill(c,ellipse(546+i*11,1223-i%2*8,6),s.mode==='ink'?s.green:'#edc35d',s)}}
function label(c,s,k){c.save();c.fillStyle=s.wall;c.fillRect(670,75,325,181);c.textAlign='right';c.fillStyle=s.line;c.font=`${s.mode==='pixel'?'bold':'600'} 67px "Microsoft YaHei",sans-serif`;const y=s.year<0?`${Math.abs(s.year).toLocaleString('en-US')} BC`:String(s.year);c.fillText(y,967,167);c.font='31px "Microsoft YaHei",sans-serif';c.fillText(s.name,967,217);line(c,[[777,247],[967,247]],s.dress,3);c.restore()}
function scene(c,k,t,{labels=true,debug=false}={}){const s=style(ERAS[k]),a=motion(t);c.save();c.lineCap='round';c.lineJoin='round';c.drawImage(background(s),0,0);fill(c,ellipse(591,1493,358,78),s.mode==='modern'?'#c7e2cf':s.green+'66',null);
 plant(c,130,1420,340,s,0,t);plant(c,997,1430,380,s,1,t);
 table(c,s);const mom=mother(c,s,a,t),kid=baby(c,s,a,t);
 if(labels)label(c,s,k);c.restore();return{a,mom,kid,era:k}}
const small=document.createElement('canvas');small.width=270;small.height=480;const sc=small.getContext('2d');
window.renderAt=(t,opt={})=>{t=clamp(t,0,41.25-1/24);let k=34;for(let i=0;i<ERAS.length;i++)if(t<ERAS[i].t1){k=i;break}const s=ERAS[k],dt=t-s.t0;ctx.resetTransform();ctx.clearRect(0,0,W,H);let state;
 if(s.mode==='pixel'){sc.save();sc.scale(.25,.25);state=scene(sc,k,t,opt);sc.restore();ctx.imageSmoothingEnabled=false;ctx.drawImage(small,0,0,W,H);ctx.imageSmoothingEnabled=true}else state=scene(ctx,k,t,opt);
 // Brief directional wipe; both eras use exactly the same absolute action time.
 if(k>0&&dt<.15&&!opt.noTransition){const p=ease(dt/.15);ctx.save();ctx.beginPath();ctx.rect(W*p,0,W*(1-p),H);ctx.clip();if(ERAS[k-1].mode==='pixel'){sc.save();sc.scale(.25,.25);scene(sc,k-1,t,opt);sc.restore();ctx.imageSmoothingEnabled=false;ctx.drawImage(small,0,0,W,H);ctx.imageSmoothingEnabled=true}else scene(ctx,k-1,t,opt);ctx.restore();}
 window.__state=state;return state;};
window.__config={width:W,height:H,fps:24,duration:41.25,frames:990,silent:true};window.renderAt(40.75);window.__ready=true;
let playing=false,start=0;cv.onclick=()=>{playing=!playing;if(playing){start=performance.now();const tick=now=>{if(!playing)return;renderAt(((now-start)/1000)%41.25);requestAnimationFrame(tick)};requestAnimationFrame(tick)}};
})();


