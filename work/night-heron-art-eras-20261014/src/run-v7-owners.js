// Generated, anatomically redrawn left/front/right heads; no facial mesh.
export async function loadOwnerReactions(){
 const manifest=await(await fetch('assets/run-v7/manifest.json')).json(),assets={};
 for(const m of manifest){const frames=await Promise.all(m.frames.map(async name=>{const im=new Image();im.src=`assets/run-v7/era-${String(m.era).padStart(2,'0')}/${name}`;await im.decode();return im}));assets[m.era]={...m,frames};}
 if(manifest.length!==16)throw Error('All sixteen tracking reaction sets required');
 return assets;
}
export function drawOwnerReaction(ctx,a,u,x,footY,height,era,target){
 const s=height/a.neutralHeight;
 // Head direction follows the actual world-relative thief, not elapsed pose time.
 // Measured neutral eye anchors in the registered 384px drawings. Using the
 // feet as a gaze origin makes the large bear turn conspicuously too late.
 const eyeAnchors=[[100,249],[119,145],[162,132],[92,208],[125,117],[156,130],[81,189],[56,183],[136,125],[147,122],[69,207],[109,155],[105,190],[34,219],[136,135],[141,142]];
 const eye=eyeAnchors[era-1],headX=x+(eye[0]-a.anchorX)*s,headY=footY+(eye[1]-a.footY)*s;
 const dx=target.x-headX,span=Math.max(70,height*.34);
 const yaw=Math.max(0,Math.min(1,(dx/span+1)/2));
 const elapsed=target.sinceGrab;
 let k=0;if(elapsed>=.035){k=elapsed<.105?1:(yaw>=.9?7:2+Math.round(yaw*4));if(k>=6&&target.y<headY-height*.15)k=8;}
 ctx.save();ctx.imageSmoothingEnabled=era!==16;
 ctx.drawImage(a.frames[k],x-a.anchorX*s,footY-a.footY*s,384*s,384*s);
 ctx.restore();return {pose:k,yaw,dx,headX,headY,targetX:target.x,targetY:target.y,headFacing:k<4?'left':k===4?'front':k===5?'three-quarter-right':'right'};
}
