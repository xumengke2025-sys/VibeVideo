// Original code scenery; techniques informed by the studied art-motion source.
export function scenery(c,e,{path,ell,line,rng}){
 const r=rng(884+e.id),ink=e.ink;
 const ridge=(y,amp,seed,col)=>{let d=`M -60 1450 L -60 ${y}`;for(let x=-60;x<=1140;x+=18){const h=Math.sin(x*.005+seed)*.35+Math.sin(x*.013+seed*3)*.18+Math.cos(x*.023-seed)*.09;d+=` L ${x} ${y-amp*(.5+h)}`}path(c,d+' L 1140 1450 Z',col)};
 const tree=(x,y,s,col)=>{c.save();c.translate(x,y);c.scale(s,s);path(c,'M -23 0 Q 2 -180 -15 -420 L 18 -435 Q 5 -160 31 0 Z',col);for(let j=0;j<18;j++){const yy=-140-j*22,side=j%2?-1:1;line(c,[[0,yy],[side*(75+j*4),yy-70]],col,7);for(let k=0;k<6;k++)ell(c,side*(35+k*16+j*2),yy-30-k*9,35,17,col,null,0,-side*.3)}c.restore()};
 const hills=()=>{ridge(1050,250,1,e.water+'55');ridge(1210,280,3,e.water+'88');ridge(1350,140,4,e.water)};
 if(e.id===0){for(let i=0;i<110;i++){const x=r()*1080,y=300+r()*1200;line(c,[[x,y],[x+70+r()*90,y-20],[x+90,y+50]],'#392a2318',1+r()*3)}c.save();c.translate(480,780);c.scale(1.5,1.5);path(c,'M -130 20 Q -100 -70 -30 -58 Q 20 -72 80 -25 L 133 -18 L 127 14 L 76 31 L 27 48 L -83 43 Z','#61412b40','#57372690',5);for(const x of[-85,-55,40,65])line(c,[[x,37],[x-14,104],[x+5,112]],'#57372690',5);line(c,[[109,-16],[114,-67],[94,-94]],'#57372690',5);c.restore();}
 if(e.id===1){ // Lotus marsh with profile bird frieze, flat mineral pigments.
  for(let j=0;j<9;j++){const x=130+j*105,y=910+(j%3)*30;line(c,[[x,1320],[x+12,y]],'#477e71',5);path(c,`M ${x-43} ${y} q 36 -9 43 -57 q 8 48 43 57 q -42 36 -86 0 Z`,'#447b82','#292f29',2);line(c,[[x-43,y+1],[x+43,y+1]],'#b76a3d',5)}
  for(let j=0;j<5;j++){const x=175+j*180;ell(c,x,680,35,20,e.water,ink,2);path(c,`M ${x+20} 675 q 44 -73 63 -40 l 34 7 l -37 5 q -14 -12 -20 41 Z`,e.water,ink,2);line(c,[[x-8,700],[x-12,738],[x+15,738]],ink,3)}
 }
 if(e.id===2){ // Sgraffito amphora with olive sprays.
  c.fillStyle=e.paper;c.fillRect(130,360,820,600);
  path(c,'M 388 415 L 690 415 L 668 454 Q 642 593 717 756 Q 791 916 540 936 Q 290 916 365 756 Q 440 593 411 454 Z',ink,ink,5);
  line(c,[[401,470],[305,480],[290,650],[376,670]],ink,19);line(c,[[678,470],[774,480],[789,650],[703,670]],ink,19);
  c.save();c.translate(540,780);for(let side of[-1,1]){line(c,[[0,80],[side*80,15],[side*115,-135]],e.paper,4);for(let j=0;j<9;j++)ell(c,side*(25+j*10),45-j*19,8,25,e.paper,null,0,side*.9)}c.restore();
 }
 if(e.id===3||e.id===5||e.id===6){
  c.save();const a=new Path2D(e.id===6?'M 150 1130 L 150 670 Q 540 -110 930 670 L 930 1130 Z':e.id===5?'M 220 1070 L 220 760 Q 540 120 860 760 L 860 1070 Z':'M 100 1250 L 100 420 L 980 420 L 980 1250 Z');c.clip(a);
  const sky=c.createLinearGradient(0,300,0,1250);sky.addColorStop(0,e.id===5?'#476f90':'#9bb7b3');sky.addColorStop(1,'#e6d4a4');c.fillStyle=sky;c.fillRect(0,300,1080,1100);hills();
  for(let j=0;j<15;j++){const x=170+j*57,h=80+r()*110;path(c,`M ${x} 1080 L ${x} ${1080-h} L ${x+13} ${1050-h} L ${x+26} ${1080-h} L ${x+26} 1080 Z`,j%2?'#988d6b':'#6b8777','#54675b',1);}
  path(c,'M 160 1160 Q 440 1030 560 1090 Q 820 1170 1100 1000 L 1100 1250 L 100 1250 Z','#5c837e');tree(225,1190,.9,'#354f43');tree(905,1240,1.3,'#425b44');
  if(e.id===5){ell(c,540,560,85,85,'#d1b260');for(let j=0;j<14;j++){const a=j/14*Math.PI*2;line(c,[[540+Math.cos(a)*100,560+Math.sin(a)*100],[540+Math.cos(a)*130,560+Math.sin(a)*130]],'#d1b260',3)}}c.restore();
  if(e.id===3){for(let j=0;j<22;j++)ell(c,82+j*44,358,10,10,j%2?e.accent:ink)}
  if(e.id===5){for(let y=400;y<1250;y+=95){for(let side of[0,1]){const x=side?972:108;line(c,[[x,y],[x+(side?-28:28),y+35],[x,y+75]],'#a68c48',4);ell(c,x+(side?-20:20),y+30,9,17,'#b65144',ink,1)}}}
 }
 if(e.id===7){ // Single raking light, table and curtain, no unlit flat characters.
  path(c,'M 860 280 Q 710 550 875 840 Q 730 1100 950 1330 L 1100 1360 L 1100 250 Z','#5d3229');for(let j=0;j<9;j++)path(c,`M ${880+j*24} 290 Q ${775+j*30} 760 ${965+j*18} 1280`,null,j%2?'#a7734540':'#160e133f',11);
  const l=c.createLinearGradient(150,600,900,1350);l.addColorStop(0,'#e0bf7928');l.addColorStop(1,'#d9ba7000');path(c,'M 145 575 L 420 575 L 1050 1420 L 0 1420 Z',l);path(c,'M 160 990 L 740 970 L 870 1090 L 130 1100 Z','#4e4031',ink,3);path(c,'M 195 1090 L 210 1360 L 245 1360 L 250 1090 M 730 1080 L 760 1340 L 795 1340 L 780 1080','#332c23');ell(c,440,946,100,30,'#817559',ink,3);path(c,'M 340 946 Q 355 1010 440 1012 Q 525 1010 540 946','#766c4e',ink,3);
 }
 if(e.id===8){ // Broken ink branches and rice-paper washes.
  c.save();c.globalAlpha=.24;for(let j=0;j<5;j++)ridge(1030+j*34,310-j*35,8+j,'#59655b');c.restore();
  for(let j=0;j<5;j++){const x=1030-j*35;line(c,[[x,1190],[x-75,790],[x-150,440],[x-270,300]],'#4e6153',4+j%2*2);for(let k=0;k<12;k++){const y=450+k*52,xx=x-150+(y-440)*.19;for(let s of[-1,1])path(c,`M ${xx} ${y} q ${s*90} -50 ${s*120} -20 q ${s*-60} 36 ${s*-120} 20`,'#30473dd0')}}
  line(c,[[70,1260],[125,1100],[182,1040]],ink,5);for(let j=0;j<12;j++){const x=50+j*17;path(c,`M ${x} 1260 q -34 -65 -12 -130 q 25 65 12 130`,j%2?'#394c42a0':'#394c4260')}
 }
 if([9,10,13,15].includes(e.id)){hills();
  if(e.id===9){tree(90,1360,1.7,'#587b69');for(let j=0;j<140;j++){const x=r()*1080,y=1110+r()*260;ell(c,x,y,4+r()*15,3+r()*7,['#d6c385','#ae8e8e','#748fa6'][j%3],null,0,r()*2)}}
  if(e.id===10){path(c,'M 90 1400 C 190 1200 88 850 142 520 Q 172 670 186 840 Q 224 676 234 612 Q 277 1010 229 1180 L 283 1400 Z','#152f36');for(let j=0;j<35;j++){const y=560+j*22;path(c,`M ${133+Math.sin(j)*15} ${y} q 110 -20 75 100`,null,j%2?'#426557':'#678066',3)}for(let j=0;j<20;j++){const x=420+j*32,y=1220-r()*90;path(c,`M ${x} 1290 v ${y-1290} l 15 -35 l 15 35 v ${1290-y} Z`,'#c2ab72','#203c48',2)}}
  if(e.id===13){path(c,'M 100 1170 L 270 1150 L 800 1350 L 470 1350 Z','#3f5b6050');for(let j=0;j<3;j++){const x=140+j*230;path(c,`M ${x} 1230 L ${x+25} ${900-j*90} L ${x+50} 1230 Z`,'#a48e67','#5b6453',2)}ell(c,850,750,114,33,'#d2ba8e','#5b6453',3);line(c,[[850,750],[900,885]],'#5b6453',4)}
  if(e.id===15){for(let j=0;j<9;j++){const x=90+j*120;c.fillStyle='#305c51';c.fillRect(x,1080,24,210);c.fillRect(x-45,1000,110,110);c.fillStyle='#4b8265';c.fillRect(x-30,975,90,70)}}
 }
 if(e.id===11){for(let j=0;j<12;j++){const x=40+j*90,y=560+r()*360;path(c,`M ${x} 1180 L ${x} ${y} L ${x+110} ${y+40} L ${x+65} 1190 Z`,j%2?'#857b62':'#b49769',ink,2);path(c,`M ${x} ${y} L ${x+70} ${y-60} L ${x+110} ${y+40} Z`,'#4f625b',ink,2)}path(c,'M 70 1250 L 300 1020 L 690 1100 L 900 990 L 1100 1340 Z','#627b70',ink,3)}
 if(e.id===12){ // Drawn river promenade, concentric circles retained as sun.
  path(c,'M 60 1160 Q 440 900 1040 1060 L 1040 1290 Q 500 1130 60 1360 Z','#aab4a6',ink,8);for(let j=0;j<12;j++){const x=70+j*89;line(c,[[x,1080-Math.sin(j*.25)*80],[x,1210-Math.sin(j*.25)*70]],ink,8)}line(c,[[60,1080],[350,985],[740,985],[1040,1060]],ink,9);for(let j=0;j<4;j++){const x=110+j*270;path(c,`M ${x} 1050 L ${x} 700 Q ${x} 660 ${x+30} 660 L ${x+65} 660`,null,ink,8);ell(c,x+70,675,30,40,'#eae7d2',ink,5)}
 }
 if(e.id===14){path(c,'M 80 1020 L 245 865 L 350 970 L 450 720 L 570 920 L 800 790 L 1010 1040 Z','#f0d657',ink,10);for(let j=0;j<8;j++)line(c,[[150+j*110,1080],[110+j*130,1200]],ink,7)}
}
