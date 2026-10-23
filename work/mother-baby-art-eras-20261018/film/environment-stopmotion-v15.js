/* v15: immutable room painting. Only exterior apertures may change.
   Whole generated birds/butterflies use held cels; no indoor mesh or moving grain. */
(()=>{'use strict';
const W=1080,H=1920,TAU=Math.PI*2,mk=(w=W,h=H)=>Object.assign(document.createElement('canvas'),{width:w,height:h}),clamp=x=>Math.max(0,Math.min(1,x));
const rect=(x,y,w,h)=>[[x,y],[x+w,y],[x+w,y+h],[x,y+h]];
// Each polygon is strictly inside a real opening. Window bars are separate gaps.
const panes=[
 [[[125,305],[360,260],[470,425],[480,690],[100,690],[95,490]]],
 [rect(152,130,455,540)],
 [rect(165,350,535,290)],
 [[[154,310],[177,207],[247,128],[353,96],[434,132],[486,216],[503,310],[503,655],[154,655]]],
 [[[100,255],[172,161],[295,125],[465,135],[584,224],[605,635],[100,635]]],
 [rect(115,310,450,470)],
 [], // Stained glass is a fixed artwork, not an unobstructed sky.
 [[[64,245],[120,145],[218,79],[335,86],[439,171],[488,306],[488,620],[64,620]],rect(660,100,90,490)],
 [[[150,100],[557,100],[659,182],[729,321],[740,650],[654,830],[470,927],[240,940],[110,875]]],
 [[[155,234],[162,170],[220,134],[276,130],[276,334],[155,334]],rect(307,153,170,181),rect(155,365,121,354),rect(307,365,170,354),rect(505,365,115,275)],
 [[[104,318],[128,196],[226,130],[343,136],[444,211],[466,318]],rect(102,341,126,462),rect(253,341,207,462)],
 [[[157,365],[189,289],[273,250],[342,269],[397,345],[397,635],[157,635]]],
 [rect(65,259,189,254),rect(279,259,196,254),rect(65,539,189,285),rect(279,539,196,285)],
 [[[65,286],[86,221],[153,172],[224,155],[224,478],[65,478]],[[247,154],[323,158],[391,208],[435,276],[440,478],[247,478]],[[65,505],[224,505],[224,738],[153,711],[97,656],[65,581]],[[247,505],[442,505],[434,579],[388,658],[326,708],[247,738]]],
 [[[86,322],[101,221],[163,153],[240,132],[240,438],[86,438]],[[265,132],[347,158],[411,223],[429,322],[429,438],[265,438]],rect(86,458,154,234),rect(265,458,164,234)],
 [rect(86,158,168,331),rect(276,158,189,331),rect(86,515,168,283),rect(276,515,189,283)],
 [rect(84,268,195,247),rect(302,268,203,247),rect(84,539,195,319),rect(302,539,203,319)],
 [rect(76,220,196,265),rect(303,220,197,265),rect(76,521,196,270),rect(303,521,197,270)],
 // Watercolor borders have a soft painted lip: inset the effect inside the glass.
 [rect(65,235,180,289),rect(291,235,188,289),rect(65,575,180,269),rect(291,575,188,269)],
 [[[96,298],[251,298],[251,532],[78,532],[78,316],[84,304]],[[276,298],[464,298],[473,307],[474,532],[276,532]],rect(78,556,173,247),rect(276,556,197,247)]
];
// row 0 = swallow, row 1 = butterfly, row 3 = sparrow. Sleeping cat row is unused.
const beats=[
 {row:0,path:[175,600,422,622],size:78,tint:'#6c4935'},
 {row:0,path:[200,420,545,365],size:78,tint:'#7c492d',cloud:[260,555,110]},
 {row:0,path:[208,470,620,430],size:75,tint:'#241b17',cloud:[290,565,100]},
 {row:0,path:[205,365,452,315],size:68,tint:'#776447',cloud:[245,470,100],pixel:3},
 {row:0,path:[171,420,535,365],size:76,tint:'#6e523c',ruyi:true},
 {row:0,path:[180,570,485,555],size:74,tint:'#a24c2c',ruyi:true},
 {},
 {row:0,path:[125,360,415,330],size:68,cloud:[215,455,115]},
 {row:0,path:[315,240,573,270],size:82,tint:'#39443b',cloud:[420,485,125],ink:true},
 {row:1,path:[194,490,430,430],size:63},
 {night:true,cloud:[220,290,100]},
 {row:1,path:[202,485,346,440],size:68,tint:'#816594'},
 {row:0,path:[101,415,439,380],size:66,tint:'#456d7c',cloud:[100,320,90],angular:true},
 {row:3,path:[110,390,388,430],size:65,tint:'#30392e',cloud:[130,310,100],angular:true},
 {row:3,path:[126,540,371,560],size:71,tint:'#3a342c',cloud:[130,350,100],outline:true},
 {row:3,path:[135,445,425,423],size:72,tint:'#a06637',sourceSky:true,sun:[367,300,135]},
 {row:3,path:[128,461,449,440],size:72,tint:'#31342b',cloud:[145,350,102],angular:true},
 {row:3,path:[143,444,445,437],size:72,tint:'#805231',sourceSky:true,sun:[403,328,105],pixel:5},
 {row:3,path:[113,444,440,385],size:75,cloud:[174,330,118]},
 {row:3,path:[136,452,451,468],size:72,tint:'#9d673d',sourceSky:true,sun:[375,405,102]}
];
const prepared=new Map(),cache=new Map(),spriteCache=new Map(),layer=mk(),lg=layer.getContext('2d'),atlas=new Image();
const ready=new Promise((resolve,reject)=>{atlas.onload=resolve;atlas.onerror=()=>reject(Error('Missing animal atlas'));atlas.src='../assets/environment-v15/animals-atlas.png'});
function shape(c,poly){c.beginPath();poly.forEach(([x,y],k)=>k?c.lineTo(x,y):c.moveTo(x,y));c.closePath();c.fill()}
function skyAllowed(r,g,b,i){if(i===0)return r>155&&g>135&&b>110;if(i===2)return r>130&&g>65&&b>25;if(i===5)return r>180&&g>130&&b>65;if(i===8)return r>180&&g>180&&b>168;if(i===14)return r>150&&g>140&&b>120;return (b>r*1.02&&b>g*.89)||(r>201&&g>197&&b>174&&Math.abs(r-g)<28)}
function prepare(im,i){
 if(prepared.has(i))return prepared.get(i);
 const base=mk(),g=base.getContext('2d',{willReadFrequently:true});g.drawImage(im,0,0,W,H);
 const aperture=mk(),a=aperture.getContext('2d',{willReadFrequently:true});a.fillStyle='#fff';panes[i].forEach(p=>shape(a,p));
 const inside=a.getImageData(0,0,W,H).data,p=g.getImageData(0,0,W,H),sky=mk(),s=sky.getContext('2d'),sd=s.createImageData(W,H);
 for(let n=0;n<W*H;n++){const k=n*4;if(inside[k+3]&&skyAllowed(p.data[k],p.data[k+1],p.data[k+2],i))sd.data[k+3]=inside[k+3]}
 s.putImageData(sd,0,0);
 const result={base,aperture,sky,sun:null,clouds:null};
 if(beats[i].sourceSky){
  const sun=mk(),sg=sun.getContext('2d'),sp=sg.createImageData(W,H),clouds=mk(),cg=clouds.getContext('2d'),cp=cg.createImageData(W,H),gold=new Uint8Array(W*H),white=new Uint8Array(W*H),[cx,cy,radius]=beats[i].sun;
  const top=panes[i].slice(0,2),topMask=mk(),tg=topMask.getContext('2d',{willReadFrequently:true});tg.fillStyle='#fff';top.forEach(poly=>shape(tg,poly));const tm=tg.getImageData(0,0,W,H).data;
  let sums=[0,0,0],count=0;
  for(let y=120;y<550;y++)for(let x=50;x<560;x++){const n=y*W+x,k=n*4,r=p.data[k],gg=p.data[k+1],b=p.data[k+2],distance=Math.hypot(x-cx,y-cy);if(!tm[k+3])continue;if(r>165&&gg>104&&r>b*1.5&&gg>b*1.3&&distance<radius)gold[n]=1;else if(distance>radius+6&&Math.min(r,gg,b)>176&&r>b*.93&&gg>b*.91)white[n]=1;else if(b>r+35&&gg>r+18){sums[0]+=r;sums[1]+=gg;sums[2]+=b;count++}}
  const color=sums.map(v=>Math.round(v/Math.max(1,count)));
  // Clear the full conservative sky panes, then restore just the separated
  // painted marks. Never carry dilated blue sky pixels along with the rays.
  // The fixed pane borders stay outside this mask, including the central bar.
  for(let y=120;y<550;y++)for(let x=50;x<560;x++){const n=y*W+x,k=n*4;if(!tm[k+3])continue;const target=gold[n]?sp:white[n]?cp:null;if(target){for(let ch=0;ch<3;ch++)target.data[k+ch]=p.data[k+ch];target.data[k+3]=tm[k+3]}const texture=i===17?0:(((x*13+y*7)%5)-2);for(let ch=0;ch<3;ch++)p.data[k+ch]=Math.max(0,Math.min(255,color[ch]+texture));sd.data[k+3]=inside[k+3]}
  g.putImageData(p,0,0);sg.putImageData(sp,0,0);cg.putImageData(cp,0,0);s.putImageData(sd,0,0);result.sun=sun;
  const left=mk(),right=mk(),split=(panes[i][0][1][0]+panes[i][1][0][0])/2;left.getContext('2d').drawImage(clouds,0,0,split,H,0,0,split,H);right.getContext('2d').drawImage(clouds,split,0,W-split,H,split,0,W-split,H);result.clouds=[left,right];
 }
 prepared.set(i,result);if(prepared.size>3){const key=prepared.keys().next().value,old=prepared.get(key);prepared.delete(key);for(const cv of [old.base,old.aperture,old.sky,old.sun,...(old.clouds||[])])if(cv)cv.width=1}return result;
}
function sprite(row,k,i){const key=[row,k,i].join(':');if(spriteCache.has(key))return spriteCache.get(key);const ranges=[[0,290],[290,550],[550,760],[760,1024]],sy=ranges[row][0],h=ranges[row][1]-sy,cv=mk(384,h),g=cv.getContext('2d');g.drawImage(atlas,k*384,sy,384,h,0,0,384,h);const b=beats[i];if(b.tint){g.globalCompositeOperation='source-in';g.fillStyle=b.tint;g.fillRect(0,0,384,h)}if(b.pixel){const low=mk(Math.round(384/b.pixel),Math.round(h/b.pixel)),l=low.getContext('2d');l.drawImage(cv,0,0,low.width,low.height);g.resetTransform();g.globalCompositeOperation='source-over';g.clearRect(0,0,384,h);g.imageSmoothingEnabled=false;g.drawImage(low,0,0,384,h)}spriteCache.set(key,cv);return cv}
function cloud(c,x,y,size,i){const b=beats[i];c.save();c.translate(x,y);c.scale(size/120,size/120);c.fillStyle=b.ink?'rgba(226,226,209,.42)':i===2?'#e4b780':i===5?'#e9bb72':i===10?'rgba(247,211,135,.24)':'#fff4da';c.globalAlpha=b.angular||b.outline?.88:.62;c.beginPath();if(b.angular){c.moveTo(-58,8);c.lineTo(-58,-5);c.lineTo(-30,-5);c.lineTo(-30,-26);c.lineTo(3,-26);c.lineTo(3,-11);c.lineTo(31,-11);c.lineTo(31,8);c.closePath()}else{c.moveTo(-58,10);c.bezierCurveTo(-74,-10,-43,-28,-26,-15);c.bezierCurveTo(-18,-47,21,-41,29,-15);c.bezierCurveTo(55,-26,72,4,53,12);c.closePath()}c.fill();if(b.outline||b.ruyi){c.strokeStyle=b.outline?'#3d362d':'#b38f56';c.lineWidth=2;c.stroke();if(b.ruyi){c.beginPath();c.moveTo(-30,5);c.bezierCurveTo(-6,-22,19,16,35,-3);c.stroke()}}c.restore()}
function renderLayer(im,t,i,cel){const p=prepare(im,i),b=beats[i],q=Math.max(0,Math.min(2,t-i*2)),cv=mk(),g=cv.getContext('2d');g.imageSmoothingEnabled=i!==17;g.drawImage(p.base,0,0);
 if(!panes[i].length)return cv;
 lg.resetTransform();lg.clearRect(0,0,W,H);lg.globalAlpha=1;lg.globalCompositeOperation='source-over';lg.imageSmoothingEnabled=i!==17;
 if(b.sourceSky){
  // Edge-clipped clouds drift toward their own outer window edge, so their
  // source crop never emerges as a straight vertical edge in the middle of sky.
  lg.drawImage(p.clouds[0],-q*18,0);lg.drawImage(p.clouds[1],q*12,0);
  const[cx,cy]=b.sun;lg.save();lg.translate(cx,cy);const angle=i===17?Math.floor(q*3)*Math.PI/36:q*.30;lg.rotate(angle);lg.drawImage(p.sun,-cx,-cy);lg.restore();
  lg.globalCompositeOperation='destination-in';lg.drawImage(p.aperture,0,0);lg.globalCompositeOperation='source-over';g.drawImage(layer,0,0);lg.clearRect(0,0,W,H);
 }else if(b.cloud){const[x,y,size]=b.cloud;cloud(lg,x+q*26,y,size,i);cloud(lg,x+165+q*19,y+80,size*.62,i)}
 if(b.night){lg.save();lg.fillStyle='#f8dea0';lg.globalAlpha=.35+.25*Math.sin(q*4);for(const[x,y]of[[151,285],[340,254],[296,440]]){lg.beginPath();lg.arc(x,y,3,0,TAU);lg.fill()}lg.restore()}
 // Sky detail stays behind landscape. Animals are complete silhouettes inside
 // the aperture; color-threshold holes must not erase parts of their wings.
 lg.globalCompositeOperation='destination-in';lg.drawImage(p.sky,0,0);lg.globalCompositeOperation='source-over';g.drawImage(layer,0,0);lg.clearRect(0,0,W,H);
 if(b.row!==undefined){const[x0,y0,x1,y1]=b.path,u=q/2,x=x0+(x1-x0)*u,y=y0+(y1-y0)*u+Math.sin(q*3+i)*8,frame=Math.floor(q*6)%4,im=sprite(b.row,frame,i),width=b.size,height=width*im.height/im.width;lg.save();lg.translate(x,y);lg.rotate(Math.atan2(y1-y0,x1-x0)*.45);lg.drawImage(im,-width/2,-height/2,width,height);lg.restore();if(i===8){lg.globalAlpha=.65;lg.drawImage(sprite(0,(frame+1)%4,i),x-55,y+37,width*.7,height*.7);lg.globalAlpha=1}}
 lg.globalCompositeOperation='destination-in';lg.drawImage(i===8?p.sky:p.aperture,0,0);lg.globalCompositeOperation='source-over';g.drawImage(layer,0,0);return cv;
}
function draw(c,im,t,i,cel){const key=i+':'+cel;let cv=cache.get(key);if(!cv){cv=renderLayer(im,t,i,cel);cache.set(key,cv);if(cache.size>4){const key=cache.keys().next().value,old=cache.get(key);cache.delete(key);old.width=1}}c.drawImage(cv,0,0)}
function allowedMask(im,i){return prepare(im,i).aperture}
window.STOP_ENV_V15={draw,ready,panes,beats,allowedMask,description:'fixed interior; held generated animals and clouds only outside real apertures; source-separated sun/cloud movement in three graphic styles'};
})();
