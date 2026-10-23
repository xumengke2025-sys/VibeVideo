import{makeGL}from'./vendor/gl.js';import{piece,drawPiece,fill,ink,cutLine,cloud,DYE}from'./vendor/carve.js';
export const compositor=makeGL;
const strip=piece([-1000,1640,5000,1860],g=>{const p=q=>q.rect(-1000,1640,6000,220);fill(g,'#bbab81',p);for(let y=1670;y<1840;y+=35)for(let x=-950;x<4950;x+=160){cutLine(g,2,q=>{q.moveTo(x,y);q.quadraticCurveTo(x+70,y-12,x+128,y+4)});if((x+y)%3)cloud(g,x+90,y+15,8,0,1.8,1);}ink(g,2,p,'#765331');},{ss:1,seed:23});
const backdrop=piece([-1000,1430,5000,1900],g=>{fill(g,'#ebe0b9',q=>q.rect(-1000,1430,6000,470));for(let row=0;row<3;row++){let y=1485+row*75;for(let x=-960;x<4950;x+=60){const h=13+Math.sin(x)*5;ink(g,1.6,q=>{q.moveTo(x,y);q.quadraticCurveTo(x+5,y-h,x+12,y-h-3);q.moveTo(x,y);q.quadraticCurveTo(x-8,y-h,x-15,y-h-5)},'#9d9461');}}},{ss:1,seed:74});
function part(g,im,r,x,y,w,h){g.drawImage(im,...r,x,y,w,h);}
export function environment(g,im,t,cam,front=false){
 if(!front){
  // Distant low mountains move by one quarter of the camera travel.
  g.save();g.translate(cam.x*.75-300,cam.y*.12);g.globalAlpha=.23;for(let x=-1000;x<4500;x+=1170)part(g,im,[0,770,780,240],x,1120,1200,350);g.restore();
  g.save();g.globalAlpha=.9;drawPiece(g,backdrop);drawPiece(g,strip);g.restore();
  g.save();g.globalAlpha=.7;for(const[x,y,w,h]of[[-315,-7,900,1660],[1140,195,770,1480],[2280,170,800,1500],[3100,100,780,1540]])part(g,im,[0,0,660,744],x,y,w,h);g.restore();
  // Original branch and perch stay fixed in the same world coordinate system.
  g.strokeStyle='#7f602d';g.lineWidth=9;g.lineCap='round';g.beginPath();g.moveTo(170,681);g.quadraticCurveTo(230,684,300,681);g.stroke();g.strokeStyle='#b69b58';g.lineWidth=2;g.stroke();
 }else{
  g.save();g.globalAlpha=.55;part(g,im,[850,0,686,760],1400,140,700,1500);part(g,im,[850,0,686,760],2500,200,660,1440);g.restore();
 }
}
export function stageFrame(g){g.save();g.fillStyle='#35160e';g.fillRect(0,0,1080,72);g.fillRect(0,0,46,1920);g.fillRect(1034,0,46,1920);g.fillRect(0,1810,1080,110);g.fillStyle='#742c1b';g.fillRect(46,48,988,24);g.fillRect(46,1810,988,20);g.strokeStyle='#b38b44';g.lineWidth=2;g.strokeRect(19,19,1042,1882);g.strokeRect(33,33,1014,1854);for(let x=88;x<1000;x+=50){g.beginPath();for(let k=0;k<30;k++){const a=k/29*6.5,r=16*(1-k/38),xx=x+Math.cos(a)*r,yy=31+Math.sin(a)*r*.6;k?g.lineTo(xx,yy):g.moveTo(xx,yy);}g.stroke();}g.restore();}
export function lampOptions(t,W,H,cam){const f=1+.013*Math.sin(t*17)+.007*Math.sin(t*31.7);return{cam:[cam.x,cam.y,W/1080*cam.zoom],rect:[-2000,-1600,6500,3400],lamps:[[cam.x-160,cam.y-60,f,1],[cam.x+330,cam.y-350,.6,.45]],sigB:1400,sigC:240,amb:.16,expo:1.43,lcol:[1,.85,.65],hotcol:[1,.95,.8],cloth:1.25,bloom:.07,thr:.85,vign:.38,sat:1.05,contrast:.055,time:t};}
