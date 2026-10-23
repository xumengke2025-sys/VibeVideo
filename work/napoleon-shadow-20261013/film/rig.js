import{ramp,mix}from'./math.js';
const A={
 head:['general',[140,5,300,380],[260,300]],body:['general',[570,0,410,430],[755,90]],upper:['general',[215,385,210,182],[352,420]],fore:['general',[568,440,358,180],[612,532]],legL:['general',[99,641,274,383],[330,677]],legR:['general',[680,625,282,399],[722,660]],flag:['general',[1095,66,441,364],[1124,240]],sword:['general',[1010,450,526,160],[1069,522]],sash:['general',[1080,636,456,388],[1231,711]],
 hat:['jaffa',[54,35,450,497],[224,427]],patient:['jaffa',[574,0,318,526],[755,500]],seated:['jaffa',[1030,214,486,318],[1290,512]],reach:['jaffa',[0,651,568,201],[43,717]],helper:['jaffa',[626,530,321,486],[735,973]],bed:['jaffa',[1030,729,489,274],[1270,973]],
 horse:['alps',[0,0,560,591],[525,544]],rider:['alps',[550,0,430,594],[770,430]],cape:['alps',[978,0,558,594],[1007,461]],hindL:['alps',[521,592,231,432],[611,630]],hindR:['alps',[756,592,220,432],[856,621]],point:['alps',[983,589,302,286],[1258,830]],tail:['alps',[1285,588,251,436],[1314,618]],
 emperor:['coronation',[38,0,510,579],[182,138]],josephine:['coronation',[551,100,556,481],[968,180]],pope:['coronation',[1133,0,403,582],[1390,558]],royalArm:['coronation',[60,601,380,258],[409,799]],royalArm2:['coronation',[45,766,398,244],[391,939]],crown:['coronation',[552,641,288,282],[700,910]],attendant:['coronation',[1108,583,187,431],[1200,985]],attendant2:['coronation',[1339,583,197,431],[1450,985]],
};
const MASKS={royalArm:[[45,590],[465,725],[465,877],[260,813],[45,746]],royalArm2:[[40,765],[170,832],[450,900],[450,1024],[30,970]]};
export function draw(g,imgs,key,x,y,s=1,a=0,alpha=1){const[name,r,p]=A[key];g.save();g.globalAlpha*=alpha;g.translate(x,y);g.rotate(a);g.scale(s,s);if(MASKS[key]){g.beginPath();MASKS[key].forEach(([xx,yy],i)=>i?g.lineTo(xx-p[0],yy-p[1]):g.moveTo(xx-p[0],yy-p[1]));g.closePath();g.clip();}g.drawImage(imgs[name],...r,r[0]-p[0],r[1]-p[1],r[2],r[3]);g.restore();}
function ik(S,T,L1,L2,bend=1){let dx=T[0]-S[0],dy=T[1]-S[1],d=Math.hypot(dx,dy);d=Math.max(Math.abs(L1-L2)+.001,Math.min(L1+L2-.001,d));const base=Math.atan2(dy,dx),a=Math.acos((L1*L1+d*d-L2*L2)/(2*L1*d))*bend;return[S[0]+Math.cos(base+a)*L1,S[1]+Math.sin(base+a)*L1];}
function rod(g,p){g.save();g.globalAlpha=.2;g.strokeStyle='#6e5437';g.lineWidth=2;g.beginPath();g.moveTo(...p);g.lineTo(p[0]+24,1780);g.stroke();g.restore();}
function arm(g,imgs,S,T,reach=false,bend=1){
 const sc=1.14,L1=Math.hypot(98,115)*sc,L2=reach?Math.hypot(489,13)*.61:Math.hypot(228,-16)*1.08,E=ik(S,T,L1,L2,bend);
 draw(g,imgs,'upper',...S,sc,Math.atan2(E[1]-S[1],E[0]-S[0])-Math.atan2(115,-98));
 draw(g,imgs,reach?'reach':'fore',...E,reach?.61:1.08,Math.atan2(T[1]-E[1],T[0]-E[0])-Math.atan2(reach?13:-16,reach?489:228));rod(g,T);return E;
}
export function general(g,imgs,t,{jaffa=false,bridge=false}={}){
 const X=jaffa?385:470,Y=jaffa?730:750,s=1.28,nod=.035*Math.sin(t*2.4),flagHand=[295,600-34*ramp(t,2,5)];
 if(!jaffa){draw(g,imgs,'flag',...flagHand,1.43,-.07+.028*Math.sin(t*2.7));}
 const hipL=[X+(638-755)*s,Y+(369-90)*s],hipR=[X+(825-755)*s,Y+(368-90)*s];
 draw(g,imgs,'legL',...hipL,s,-.13);draw(g,imgs,'legR',...hipR,s,.03);
 draw(g,imgs,'body',X,Y,s);draw(g,imgs,'sash',X+105,Y+205,.45,.09*Math.sin(t*1.5));
 const S=[X+(649-755)*s,Y+(80-90)*s];
 if(!jaffa){arm(g,imgs,S,flagHand,false,1);const T=[325,1145+5*Math.sin(t*2)];arm(g,imgs,[X+110,Y],T,false,-1);draw(g,imgs,'sword',...T,.71,Math.PI+.07);}
 else{
  const u=ramp(t,19,23),pt=patientChest(t);const T=[mix(655,pt[0],u),mix(1155,pt[1],u)];arm(g,imgs,[X+100,Y],T,true,-1);
  arm(g,imgs,S,[X-135,Y+240],false,1);
 }
 draw(g,imgs,jaffa?'hat':'head',X-8,Y-(jaffa?72:110),jaffa?.6:.77,nod*(jaffa?.5:1));rod(g,[X-20,Y-38]);
 if(bridge){draw(g,imgs,'flag',930,700,.65,-.14,.35);}
 return{head:[X,Y-200],shoulder:[X+100,Y],contact:jaffa?patientChest(t):flagHand};
}
function patientChest(t){const a=.006*Math.sin(t*1.3),dx=(732-755)*1.65,dy=(205-500)*1.65;return[830+dx*Math.cos(a)-dy*Math.sin(a),1460+dx*Math.sin(a)+dy*Math.cos(a)];}
export function hospital(g,imgs,t){
 draw(g,imgs,'helper',174,1415,.91,.015*Math.sin(t));draw(g,imgs,'bed',924,1510,.88);draw(g,imgs,'seated',670,1502,.8,.01*Math.sin(t*1.7));
 draw(g,imgs,'patient',830,1460,1.65,.006*Math.sin(t*1.3));return general(g,imgs,t,{jaffa:true,bridge:t>28});
}
export function alpine(g,imgs,t){
 const u=ramp(t,34.5,42),moving=(1-ramp(t,42,45)),phase=(t-35)*5.5,bob=Math.sin(phase)*7*moving,X=845-155*u,Y=1210-82*u+bob,s=1.48;
 draw(g,imgs,'tail',X+2,Y-26,.76,-.43+.04*Math.sin(t*2.6));
 draw(g,imgs,'hindR',X-18,Y-27,1.02,-.06+.08*Math.sin(phase+Math.PI)*moving);
 draw(g,imgs,'hindL',X-7,Y-19,1.03,.11+.085*Math.sin(phase)*moving);
 draw(g,imgs,'horse',X,Y,s,-.065-.025*ramp(t,36,40));
 const saddle=[X-105,Y-145];draw(g,imgs,'cape',saddle[0]+57,saddle[1]-228,1.10,-.26+.10*Math.sin(t*2.1)*moving);
 const shoulder=[saddle[0]+62,saddle[1]-307];draw(g,imgs,'point',...shoulder,.73,.64+.09*ramp(t,36,39));draw(g,imgs,'rider',...saddle,1.25,-.02);rod(g,shoulder);
 return{subject:[X,Y],head:[saddle[0]-20,saddle[1]-420]};
}
function upperRoyal(g,S,E){const dx=E[0]-S[0],dy=E[1]-S[1],l=Math.hypot(dx,dy);g.save();g.translate(...S);g.rotate(Math.atan2(dy,dx));g.fillStyle='#d4ad70';g.strokeStyle='#704923';g.lineWidth=3;g.beginPath();g.roundRect(-22,-31,l+48,62,27);g.fill();g.stroke();g.strokeStyle='#99712c';g.lineWidth=2;for(let x=10;x<l;x+=21){g.beginPath();g.moveTo(x,-19);g.lineTo(x+8,0);g.lineTo(x,19);g.stroke();}g.fillStyle='#5c351c';g.beginPath();g.arc(0,0,9,0,7);g.fill();g.restore();}
function royalArm(g,imgs,S,T,back=false){const L1=145,L2=218,E=ik(S,T,L1,L2,-1);upperRoyal(g,S,E);const k=back?'royalArm2':'royalArm',vec=back?[-301,-136]:[-302,-150],s=L2/Math.hypot(...vec);draw(g,imgs,k,...E,s,Math.atan2(T[1]-E[1],T[0]-E[0])-Math.atan2(vec[1],vec[0]));rod(g,T);}
export function coronation(g,imgs,t){
 draw(g,imgs,'attendant',132,1485,.95);draw(g,imgs,'attendant2',255,1500,.72);draw(g,imgs,'pope',943,1500,1.20);
 draw(g,imgs,'josephine',383,1070,1.20,.005*Math.sin(t));
 const u=ramp(t,51.7,55.8),v=ramp(t,59,61),C=[mix(mix(535,418,u),393,v),mix(mix(1150,941,u),1028,v)];
 royalArm(g,imgs,[642,827],[C[0]+51,C[1]-15],true);
 draw(g,imgs,'emperor',693,809,1.35);
 royalArm(g,imgs,[697,827],[C[0]-51,C[1]-15]);
 draw(g,imgs,'crown',...C,.47);return{crown:C,hands:[[C[0]+51,C[1]-15],[C[0]-51,C[1]-15]],head:[383,1070]};
}
