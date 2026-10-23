import{ramp,mix,sceneAt,transitions}from'./math.js';
export function scenic(g,im,scene,t,cam){
 let r=scene==='arcole'?[0,0,768,512]:scene==='jaffa'?[768,0,768,512]:scene==='alps'?[0,512,768,512]:[768,512,768,512];
 const x=scene==='arcole'?-180:scene==='jaffa'?-370:scene==='alps'?-100:-335,y=scene==='arcole'?550:scene==='jaffa'?340:scene==='alps'?495:340,w=scene==='arcole'?1440:scene==='jaffa'?1800:scene==='alps'?1450:1770,h=w*2/3;
 g.save();g.globalAlpha=.79;g.translate(cam.x*.16-86,cam.y*.03-29);g.drawImage(im,...r,x,y,w,h);g.restore();
 // A narrow carved ground band unifies the theatre without covering the puppet feet.
 g.fillStyle='#ad8552';g.fillRect(-800,1548,2700,27);g.strokeStyle='#ead39a';g.lineWidth=1.6;for(let x=-750;x<2000;x+=50){g.beginPath();g.moveTo(x,1560);g.quadraticCurveTo(x+18,1546,x+33,1560);g.quadraticCurveTo(x+18,1575,x,1560);g.stroke();}
 if(scene==='arcole'){g.save();g.globalAlpha=.2;g.strokeStyle='#658e8b';g.lineWidth=3;for(let j=0;j<6;j++){g.beginPath();for(let x=0;x<1100;x+=20){const y=1500+j*7+Math.sin(x*.012+t*.6+j)*3;x?g.lineTo(x,y):g.moveTo(x,y);}g.stroke();}g.restore();}
}
export function fragments(g,states,t){
 const tr=transitions.find(([a,b])=>t>=a&&t<=b);if(!tr)return;
 const[a,b]=tr,opacity=ramp(t,a,a+.4)*(1-ramp(t,b-1,b));g.save();g.globalAlpha=opacity;
 states.forEach(([x,y,vx,vy],id)=>{g.save();g.translate(x,y);g.rotate(Math.atan2(vy,vx)+id*.37);const l=8+id%7,w=4+id%4;g.fillStyle=id%5===0?'#2d4959':id%3===0?'#b99248':'#a33a21';g.strokeStyle='#66401d';g.lineWidth=1;g.beginPath();g.moveTo(-l,0);g.quadraticCurveTo(-4,-w,l,0);g.quadraticCurveTo(0,w,-l,0);g.fill();g.stroke();g.fillStyle='#f3ddb1';g.beginPath();g.ellipse(0,0,l*.32,1.3,0,0,7);g.fill();g.restore();});g.restore();
}
export function curtain(g,t){
 // Die-cut fabric sweeps are explicit occlusion edits, never character morphs.
 const tr=[[13.4,16.6],[31,34.2],[48,51.2]].find(([a,b])=>t>=a&&t<=b);if(!tr)return;
 const[a,b]=tr,u=(t-a)/(b-a),cx=mix(-1600,2200,u),width=1900;
 g.save();g.globalCompositeOperation='source-over';g.translate(cx,0);g.rotate(-.22);g.fillStyle='#a53820';g.strokeStyle='#b48a42';g.lineWidth=8;g.beginPath();g.moveTo(-width/2,-700);g.bezierCurveTo(-width/2+100,420,-width/2-180,1480,-width/2+40,2400);g.lineTo(width/2,2400);g.bezierCurveTo(width/2-120,1450,width/2+140,700,width/2,-700);g.closePath();g.fill();g.stroke();
 g.strokeStyle='#d0a658';g.lineWidth=3;g.globalAlpha=.8;for(let x=-width/2+60;x<width/2-30;x+=80){g.beginPath();g.moveTo(x,-600);g.bezierCurveTo(x+130,400,x-100,1500,x+50,2300);g.stroke();for(let y=-500;y<2200;y+=105){g.beginPath();g.ellipse(x+20*Math.sin(y*.005),y,13,28,.4,0,7);g.stroke();}}g.restore();
}
export function stage(g){g.save();g.fillStyle='#321b12';g.fillRect(0,0,1080,64);g.fillRect(0,0,31,1920);g.fillRect(1049,0,31,1920);g.fillRect(0,1845,1080,75);g.fillStyle='#67331d';g.fillRect(31,44,1018,15);g.fillRect(31,1844,1018,17);g.strokeStyle='#aa8144';g.lineWidth=2;g.strokeRect(14,14,1052,1892);g.strokeRect(23,24,1034,1872);for(let x=75;x<1040;x+=60){g.beginPath();g.moveTo(x-19,31);g.bezierCurveTo(x-17,9,x+19,10,x+19,31);g.bezierCurveTo(x+14,48,x-9,44,x-6,28);g.stroke();}g.restore();}
export function lamp(t,W,H,cam){const f=1+.008*Math.sin(t*15)+.004*Math.sin(t*30.4);return{cam:[cam.x,cam.y,W/1080*cam.z],rect:[-1800,-1000,3000,3000],lamps:[[cam.x-150,cam.y-220,f,.65],[cam.x+320,cam.y-430,.5,.45]],sigB:1650,sigC:350,amb:.18,expo:1.58,lcol:[1,.86,.68],hotcol:[1,.96,.83],cloth:.78,bloom:.035,thr:.86,vign:.27,sat:1.09,contrast:.075,time:t};}
