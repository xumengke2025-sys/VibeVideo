// Actual eye centers measured in each 384px era drawing; details rotate with the head.
const eyes=[[308,139,7],[306,148,6],[313,132,8],[329,130,7],[313,139,8],[317,135,7],[317,134,6],[314,125,7],[310,126,6],[314,126,7],[312,144,7],[313,127,8],[315,141,10],[320,137,6],[319,129,7],[303,129,7]];
export function drawIdentity(ctx,era,eye,angle){
 const [ex,ey,r]=eyes[era-1],pixel=era===16;
 ctx.save();ctx.translate(eye[0]*384,eye[1]*384);ctx.rotate(angle);ctx.translate(ex-.80*384,ey-.34*384);
 ctx.lineJoin='round';ctx.lineCap='round';
 // Two separate tapered occipital plumes, rooted in the rear of the black crown.
 for(const [dx,dy,len,drop]of[[-40,-18,92,37],[-34,-20,82,53]]){
  ctx.beginPath();ctx.moveTo(dx,dy);
  if(pixel){ctx.lineTo(dx-24,dy+5);ctx.lineTo(dx-54,dy+18);ctx.lineTo(dx-len,dy+drop);ctx.lineTo(dx-53,dy+14);ctx.lineTo(dx-23,dy+1);}
  else{ctx.bezierCurveTo(dx-24,dy+2,dx-len+24,dy+drop-6,dx-len,dy+drop);ctx.bezierCurveTo(dx-len+23,dy+drop-12,dx-26,dy-3,dx+1,dy-2);}
  ctx.closePath();ctx.strokeStyle='rgba(35,39,39,.72)';ctx.lineWidth=pixel?2:1.6;ctx.stroke();ctx.fillStyle='#fffdf0';ctx.fill();
  if([1,7,8,10,11,14].includes(era)){ctx.beginPath();ctx.moveTo(dx-3,dy);ctx.quadraticCurveTo(dx-40,dy+9,dx-len+5,dy+drop-2);ctx.lineWidth=.7;ctx.strokeStyle='#d5d8d1';ctx.stroke();}
 }
 // Preserve the generated eyelid, replacing only the iris and pupil.
 if(pixel){ctx.fillStyle='#de3028';ctx.fillRect(-r,-r,r*2,r*2);ctx.fillStyle='#171a18';ctx.fillRect(-r*.47,-r*.65,r*.94,r*1.3);ctx.fillStyle='#fff2dc';ctx.fillRect(-r*.18,-r*.58,2,2);}
 else{ctx.beginPath();ctx.ellipse(0,0,r,r*.92,0,0,Math.PI*2);ctx.fillStyle=era===1?'#b92920':'#d92e24';ctx.fill();ctx.strokeStyle='#6b2018';ctx.lineWidth=1;ctx.stroke();ctx.beginPath();ctx.ellipse(.4,.3,r*.46,r*.64,0,0,Math.PI*2);ctx.fillStyle='#151a19';ctx.fill();ctx.beginPath();ctx.arc(-r*.21,-r*.37,Math.max(.8,r*.16),0,Math.PI*2);ctx.fillStyle='#fff6e0';ctx.fill();}
 ctx.restore();
}
