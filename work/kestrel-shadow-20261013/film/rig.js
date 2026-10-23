import{ramp,clamp}from'./math.js';
const rigs={
 kestrel:{body:[0,110,930,455],bodyRoot:[755,193],wing:[925,0,611,640],wingRoot:[539,552],fold:[35,645,790,330],foldRoot:[715,68],feet:[{box:[1010,650,287,335],root:[48,34]},{box:[1210,670,320,325],root:[38,32]}],scale:.235,headBox:[720,145,205,195],headPivot:[822,287]},
 dove:{body:[0,80,880,410],bodyRoot:[683,173],wing:[900,0,636,610],wingRoot:[589,524],fold:[80,620,650,370],foldRoot:[604,60],feet:[{box:[1000,685,215,303],root:[114,51]},{box:[1190,685,228,303],root:[28,61]}],scale:.153,headBox:[645,94,225,165],headPivot:[744,230]}
};
function slice(g,im,box,root,s){g.drawImage(im,...box,-root[0]*s,-root[1]*s,box[2]*s,box[3]*s);}
function rivet(g,x,y,r){g.fillStyle='#6b461c';g.beginPath();g.arc(x,y,r,0,7);g.fill();g.fillStyle='#ceaa65';g.beginPath();g.arc(x-.5,y-.5,r*.5,0,7);g.fill();}
export function drawBird(g,im,kind,state,t,meta={phase:0,size:1,id:0}){
 const r=rigs[kind],s=r.scale*meta.size,flight=state.flight,face=state.face??(state.vx<0?-1:1),pitch=state.pitch??clamp(Math.atan2(state.vy*face,Math.max(75,Math.abs(state.vx))),-.9,.9)*flight;
 const tremor=Math.sin(t*13.8+meta.phase)*.004,perchNod=Math.sin(t*2.8+meta.phase)*.055*(1-flight);
 g.save();g.translate(state.x,state.y);g.rotate(pitch+tremor+perchNod);g.scale(face,1);
 // Rod is behind leather; stops well short of neighbouring birds.
 g.save();g.globalAlpha=.17;g.strokeStyle='#594832';g.lineWidth=kind==='kestrel'?1.6:.65;g.beginPath();g.moveTo(-15,20);g.lineTo(-35,kind==='kestrel'?340:155);g.stroke();g.restore();
 const phase=t*2*Math.PI*(kind==='kestrel'?3.15:4.05)+meta.phase,flap=Math.sin(phase),spread=.72+.28*Math.abs(flap),down=flap;
 function wing(far){g.save();g.translate(far?-4:0,far?-3:0);g.rotate((far?-.1:.02)+.11*Math.cos(phase));g.scale(spread*(far?.9:1),(far?.77:1)*down);slice(g,im,r.wing,r.wingRoot,s*(far?.92:1));g.restore();}
 if(flight>.005){g.save();g.globalAlpha=.72*flight;wing(true);g.restore();}
 // Main dyed-hide piece; lookout/peck uses the whole-body perch tilt.
 if(flight<.99){slice(g,im,r.body,r.bodyRoot,s);}else{slice(g,im,r.body,r.bodyRoot,s);}
 if(flight<.1){g.save();g.translate(-2,5);slice(g,im,r.fold,r.foldRoot,s*.91);g.restore();}
 if(flight>.005){g.save();g.globalAlpha=flight;wing(false);g.restore();}
 const grab=state.grab||0,tuck=flight*(1-grab),footY=kind==='kestrel'?44:28;
 r.feet.forEach((f,i)=>{g.save();g.translate((kind==='kestrel'?-30:-28)+i*20,footY-7*tuck);g.rotate(tuck*1.08+(i?-.1:.12)-grab*.48);g.scale(1,1-.68*tuck);slice(g,im,f.box,f.root,s*(kind==='kestrel'?.65:.60));g.restore();});
 rivet(g,0,0,kind==='kestrel'?3.1:2.2);g.restore();
 return {x:state.x,y:state.y,length:r.body[2]*s,span:r.wingRoot[1]*s*2,flight};
}
