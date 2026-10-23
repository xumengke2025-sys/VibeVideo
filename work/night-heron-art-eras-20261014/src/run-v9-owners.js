// Reuse the era-specific neutral, startled and downward-looking drawings.
// No yaw, look-back, thief position, facial mesh, or pose crossfade.
export async function loadOwnerReactions(){
 const manifest=await(await fetch('assets/run-v9/manifest.json')).json(),assets={};
 for(const m of manifest){
  const frames=await Promise.all(m.frames.map(async name=>{
   const im=new Image();im.src=`assets/run-v9/era-${String(m.era).padStart(2,'0')}/${name}`;await im.decode();return im;
  }));assets[m.era]={...m,frames};
 }
 if(manifest.length!==16)throw Error('All sixteen ground-looking reaction sets required');
 return assets;
}
export function drawOwnerReaction(ctx,a,u,x,footY,height,era,target){
 const elapsed=target.sinceGrab;
 // Notice the missing fish, lower the head, then hold the empty ground in view.
 const k=elapsed<.065?0:elapsed<.16?1:elapsed<.30?3:4;
 const s=height/a.neutralHeight;
 ctx.save();ctx.imageSmoothingEnabled=era!==16;
 ctx.drawImage(a.frames[k],x-a.anchorX*s,footY-a.footY*s,384*s,384*s);
 ctx.restore();
 return {pose:k,headFacing:'left',gaze:elapsed>=.16?'empty-fish-ground':'neutral',targetX:target.x,targetY:target.y,sinceGrab:elapsed};
}
