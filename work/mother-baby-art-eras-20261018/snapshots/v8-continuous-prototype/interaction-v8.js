/* Scene-specific living environment and visible interaction objects. */
(()=>{
const TAU=2*Math.PI,clamp=x=>Math.max(0,Math.min(1,x)),smooth=x=>(x=clamp(x),x*x*(3-2*x));
const names=['tablet','book','scroll','puppet','flower','blocks','butterfly','card'];
const maps=[
 ['洞穴手印与太阳纹样','抬手指认壁面，宝宝抬头','火光与洞口空气'],
 ['尼罗河帆船与莲花','继续展示窗外，宝宝回应','水波与棕榈叶'],
 ['黑绘陶瓶与海景','沿视线指认陶瓶纹样','海面波纹与橄榄枝'],
 ['马赛克庭院','落手看庭院','窗外云与植物'],
 ['敦煌莲池与飘带','宝宝追看莲池方向','云气、池水与枝叶'],
 ['影戏窗格','观看新增兔形影偶','影偶与灯笼'],
 ['手抄本书房','妈妈拿起装饰图册','书页与窗景'],
 ['文艺复兴凉廊','翻页给宝宝看花鸟图','翻页、庭园云与植物'],
 ['明暗书房','宝宝探头看书，妈妈合拢放回','窗光与书页'],
 ['水墨竹窗','放下图册后指向竹叶','竹叶与远山薄雾'],
 ['印象派花窗','宝宝发现花间蝴蝶','蝴蝶、窗纱和花叶'],
 ['点彩花窗','妈妈伸手拿咖啡杯','窗外云和花叶'],
 ['后印象花房','妈妈举杯，宝宝看花','枝叶与窗外光'],
 ['表现主义室内','妈妈饮用，宝宝准备抱瓶','窗帘与云'],
 ['新艺术花窗','宝宝抬起奶瓶','花藤与蝴蝶'],
 ['睡莲庭园','妈妈放杯，宝宝喝奶','池水与垂柳'],
 ['蓝色室内','宝宝喝奶后回正','窗外云与枝叶'],
 ['金色装饰室内','宝宝放低奶瓶','光斑与花叶'],
 ['立体主义室内','奶瓶放稳，注意几何玩具','几何陈设与植物'],
 ['包豪斯室内','妈妈示意玩具，宝宝伸手','木球滚到宝宝手边'],
 ['构成主义室内','宝宝推球，妈妈回应','木球缓慢滚离'],
 ['橡皮管室内','宝宝收手，两人看窗景','云和吊灯'],
 ['超现实室内','两人看漂浮纸花','纸花、云与窗外景物'],
 ['美式现实室内','纸花落桌，妈妈注意花','窗帘与日光'],
 ['剪纸室内','妈妈拿起纸花给宝宝看','纸花与剪纸枝叶'],
 ['波普室内','宝宝朝纸花伸手回应','花瓣与植物'],
 ['波点室内','继续展示纸花','波点花瓣与窗景'],
 ['漫画室内','妈妈放回纸花，宝宝收手','窗帘和云'],
 ['涂鸦室内','妈妈示意墙上花朵，宝宝追看飞蝶','花朵笔迹与蝴蝶'],
 ['像素室内','视线跟随像素蝴蝶','像素蝶、云和叶片'],
 ['水彩室内','蝴蝶飞向花叶，两人收回视线','水彩枝叶与飞蝶'],
 ['数字室内','妈妈看向宝宝','窗帘和云'],
 ['蒸汽波窗景','妈妈轻挥手，宝宝回应','海面、棕榈与云'],
 ['日系窗景','两人挥手后落手','绿叶和阳光'],
 ['现代扁平室内','相视微笑，动作安定','植物缓动与窗外云']
];
const sky=[null,[.16,.18,.38,.26],[.29,.19,.42,.29],[.18,.12,.44,.35],[.06,.16,.59,.26],[.08,.20,.54,.31],[.21,.12,.35,.30],[.06,.13,.46,.30],[.08,.18,.27,.28],[.27,.18,.37,.28],[.15,.16,.28,.30],[.21,.11,.40,.35],[.18,.12,.26,.29],[.18,.16,.29,.26],[.15,.16,.28,.27],[.22,.14,.48,.24],[.16,.18,.31,.28],[.11,.20,.37,.26],[.15,.23,.38,.22],[.15,.23,.32,.25],[.08,.18,.28,.22],[.14,.17,.35,.27],[.18,.12,.33,.33],[.12,.15,.35,.28],[.11,.14,.36,.27],[.14,.20,.38,.25],[.16,.21,.34,.24],[.14,.13,.36,.28],[.04,.18,.38,.27],[.15,.21,.32,.26],[.13,.17,.30,.27],[.10,.19,.34,.24],[.12,.12,.32,.25],[.08,.13,.40,.28],[.14,.20,.31,.21]];
function prop(c,im,x,y,w,h,a=0,px=.5,py=.5){c.save();c.translate(x,y);c.rotate(a);c.drawImage(im,-px*w,-py*h,w,h);c.restore()}
// Source-aligned deformation: only selected plants/cloth/water move; architecture stays fixed.
const regions=i=>{
 const common=[[.11,.56,.18,.24,9],[.90,.49,.17,.31,11],[.91,.87,.19,.17,9]];
 if(i===0)return [];
 if(i===9)return [[.11,.39,.22,.36,16]];
 if(i===15)return [[.80,.27,.23,.22,16],[.18,.36,.18,.27,10],[.57,.50,.38,.09,5]];
 if([10,13,23,27,31].includes(i))common.push([.60,.29,.18,.29,14]);
 return common;
};
function vertex(x,y,t,i){let dx=0,dy=0;for(const [cx,cy,rx,ry,amp] of regions(i)){const ux=(x/1080-cx)/rx,uy=(y/1920-cy)/ry;const weight=Math.max(0,1-ux*ux)*Math.max(0,1-uy*uy);dx+=weight*weight*amp*Math.sin(t*1.45+y*.003+i*.3);dy+=weight*weight*2*Math.sin(t*1.15+x*.004)}return [x+dx,y+dy]}
function triangle(c,im,s,d){
 const ax=s[1][0]-s[0][0],ay=s[1][1]-s[0][1],bx=s[2][0]-s[0][0],by=s[2][1]-s[0][1],det=ax*by-ay*bx;
 const ux=d[1][0]-d[0][0],uy=d[1][1]-d[0][1],vx=d[2][0]-d[0][0],vy=d[2][1]-d[0][1];
 const a=(ux*by-vx*ay)/det,b=(uy*by-vy*ay)/det,cc=(vx*ax-ux*bx)/det,dd=(vy*ax-uy*bx)/det;
 c.save();c.beginPath();const mx=(d[0][0]+d[1][0]+d[2][0])/3,my=(d[0][1]+d[1][1]+d[2][1])/3;
 d.forEach((q,k)=>{const x=q[0]+Math.sign(q[0]-mx)*.55,y=q[1]+Math.sign(q[1]-my)*.55;k?c.lineTo(x,y):c.moveTo(x,y)});c.closePath();c.clip();
 c.transform(a,b,cc,dd,d[0][0]-a*s[0][0]-cc*s[0][1],d[0][1]-b*s[0][0]-dd*s[0][1]);c.drawImage(im,0,0,1080,1920);c.restore();
}
const skyMasks=new Map(),cloudCanvas=Object.assign(document.createElement('canvas'),{width:1080,height:1920});
function prepareSky(im,i){
 if(skyMasks.has(i)||!sky[i])return;
 const mask=Object.assign(document.createElement('canvas'),{width:270,height:480}),g=mask.getContext('2d',{willReadFrequently:true});g.drawImage(im,0,0,270,480);
 const pixels=g.getImageData(0,0,270,480),[sx,sy,sw,sh]=sky[i];
 for(let y=0;y<480;y++)for(let x=0;x<270;x++){const k=(y*270+x)*4,r=pixels.data[k],gg=pixels.data[k+1],b=pixels.data[k+2],inside=x/270>sx&&x/270<sx+sw&&y/480>sy&&y/480<sy+sh;
 const blue=clamp(Math.min((b-r*.97)/20,(gg-r*.99)/12));pixels.data[k+3]=inside?Math.round(blue*255):0;
 }g.putImageData(pixels,0,0);skyMasks.set(i,mask);
}
function background(c,im,t,i){
 prepareSky(im,i);
 c.drawImage(im,0,0,1080,1920);if(i===0)return;
 const nx=10,ny=18,w=1080/nx,h=1920/ny;
 for(let y=0;y<ny;y++)for(let x=0;x<nx;x++){
  const s=[[x*w,y*h],[(x+1)*w,y*h],[x*w,(y+1)*h],[(x+1)*w,(y+1)*h]],d=s.map(q=>vertex(...q,t,i));
  if(d.every((q,k)=>Math.abs(q[0]-s[k][0])+Math.abs(q[1]-s[k][1])<.05))continue;
  triangle(c,im,[s[0],s[1],s[2]],[d[0],d[1],d[2]]);triangle(c,im,[s[3],s[2],s[1]],[d[3],d[2],d[1]]);
 }
}
function butterfly(c,im,t,i,x,y,size=75){
 c.save();c.translate(x,y);c.rotate(.15*Math.sin(t*2));
 const wing=.45+.55*(.5+.5*Math.sin(t*7));c.scale(wing,1);
 if(i===29){c.imageSmoothingEnabled=false;const small=document.createElement('canvas');small.width=18;small.height=14;small.getContext('2d').drawImage(im,0,0,18,14);c.drawImage(small,-size/2,-size*.4,size,size*.8)}
 else c.drawImage(im,-size/2,-size*.4,size,size*.8);c.restore();
}
function ambient(c,t,i,images){
 const e=ERAS[i],win=sky[i];c.save();
 if(win&&skyMasks.has(i)){const [x,y,w,h]=win.map((v,k)=>v*(k%2===0?1080:1920)),g=cloudCanvas.getContext('2d');g.clearRect(0,0,1080,1920);g.globalCompositeOperation='source-over';g.fillStyle=[2,21].includes(i)?e.wall:'#fff8df';g.globalAlpha=.34;
 for(let k=0;k<2;k++){const u=((t*.045+k*.55)%1),cx=x-90+u*(w+180),cy=y+h*(.20+k*.22);g.beginPath();g.ellipse(cx,cy,40,12,0,0,TAU);g.ellipse(cx+24,cy-8,26,19,0,0,TAU);g.ellipse(cx+48,cy,36,13,0,0,TAU);g.fill()}
 g.globalAlpha=1;g.globalCompositeOperation='destination-in';g.drawImage(skyMasks.get(i),0,0,1080,1920);g.globalCompositeOperation='source-over';c.drawImage(cloudCanvas,0,0);}
 if([1,2,4,15,32].includes(i)){const water=({1:[200,745,370,110],2:[330,790,400,100],4:[200,850,340,120],15:[230,850,600,180],32:[110,880,320,120]})[i];c.save();c.strokeStyle=e.wall;c.globalAlpha=.46;c.lineWidth=2.6;for(let j=0;j<12;j++){const x=water[0]+(j*61+t*14)%water[2],y=water[1]+j%5*water[3]/5;c.beginPath();c.ellipse(x,y,16+10*Math.sin(t+j),2.2,0,0,Math.PI);c.stroke()}c.restore()}
 if(i===0){c.save();const g=c.createRadialGradient(125,1180,20,125,1180,620);g.addColorStop(0,'rgba(255,176,60,'+(.15+.025*Math.sin(t*5)+.015*Math.sin(t*8))+')');g.addColorStop(1,'rgba(255,176,60,0)');c.fillStyle=g;c.fillRect(0,0,1080,1600);c.restore()}
 if(i===5){prop(c,images.puppet,535+12*Math.sin(t*2),850-14*Math.sin(t*2),134,190,.08*Math.sin(t*2));}
 if(i>=9&&i<=17||i>=28&&i<=30){const u=i<18?t-10:t-32;butterfly(c,images.butterfly,t,i,435+100*Math.sin(u*.65),1110+60*Math.sin(u*.8),i===29?70:65)}
 if(i===28){const show=ACTION_V8.s(t,32,32.6);c.save();c.beginPath();c.rect(395,820,120*show,145);c.clip();prop(c,images.card,455,895,105,130);c.restore()}
 c.restore();
}
function interaction(c,t,i,images,state){
 const p=ACTION_V8.pose(t,t),m=state.mother,b=state.baby;
 if(t>=5.5&&t<10.7){const alpha=ACTION_V8.p(t,5.5,6.1,10.1,10.7),held=ACTION_V8.p(t,6.5,6.7,9.65,9.85);c.save();c.globalAlpha=alpha;
 const x=640*(1-held)+(m.hand[0]-73)*held,y=1275*(1-held)+(m.hand[1]-27)*held;prop(c,images.book,x,y,166,113,-.10);
 // A separate cream leaf turns across the open illustration and settles.
 const turn=ACTION_V8.s(t,7.45,8.45);if(turn>0&&turn<1){c.save();c.translate(x,y-8);c.scale(Math.cos(turn*Math.PI),1);c.fillStyle='#f3e7c5';c.strokeStyle='#966344';c.lineWidth=2;c.beginPath();c.moveTo(0,-40);c.quadraticCurveTo(70,-54,72,-36);c.lineTo(70,39);c.quadraticCurveTo(35,34,0,44);c.closePath();c.fill();c.stroke();c.restore()}c.restore();}
 if(t>=20.7&&t<24.45){c.save();c.globalAlpha=ACTION_V8.p(t,20.7,21.1,24,24.45);prop(c,images.blocks,465,1491,130,72,0,.5,1);
 const arrive=ACTION_V8.s(t,21.2,22.4),push=ACTION_V8.s(t,22.95,23.8),x=540-114*arrive+90*push,y=1450;
 c.fillStyle=ERAS[i].dress;c.strokeStyle=ERAS[i].line;c.lineWidth=3;c.beginPath();c.arc(x,y,23,0,TAU);c.fill();c.stroke();c.save();c.translate(x,y);c.rotate((x-540)/23);c.beginPath();c.moveTo(-13,-13);c.lineTo(13,13);c.stroke();c.restore();c.restore();}
 if(t>=25.2&&t<32){const alpha=ACTION_V8.p(t,25.2,25.65,31.6,32),held=ACTION_V8.p(t,27.7,27.8,31.25,31.4);
 const fx=698*(1-held)+(m.hand[0]-7)*held,fy=(1333-100*ACTION_V8.p(t,25.2,25.7,25.95,26.5))*(1-held)+(m.hand[1]+3)*held;
 c.save();c.globalAlpha=alpha;prop(c,images.flower,fx,fy,100,136,-.13+.08*Math.sin(t*1.8),.55,.96);c.restore();}
}
window.INTERACTION_V8={names,maps,sky,background,ambient,interaction};
})();
