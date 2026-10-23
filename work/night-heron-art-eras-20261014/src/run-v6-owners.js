// Real redrawn reaction frames; no mesh deformation, facial warping or pose crossfade.
export async function loadOwnerReactions(){
 const manifest=await(await fetch('assets/run-v6/manifest.json')).json();
 const assets={};
 for(const m of manifest){const frames=await Promise.all(m.frames.map(async name=>{const im=new Image();im.src=`assets/run-v6/era-${String(m.era).padStart(2,'0')}/${name}`;await im.decode();return im}));assets[m.era]={...m,frames};}
 const pilot=new URLSearchParams(location.search).get('pilot');
 if(manifest.length!==16&&!pilot)throw Error('All sixteen redrawn animal reactions are required.');
 return assets;
}
export function drawOwnerReaction(ctx,a,u,x,footY,height,era){
 // Advance through actual drawing keys, then hold the startled result through exit.
 const keys=[0,.055,.14,.245,.36,.49,.62,.74,.86];
 let k=0;while(k<8&&u>=keys[k+1])k++;
 const s=height/a.neutralHeight;
 ctx.save();ctx.imageSmoothingEnabled=era!==16;
 ctx.drawImage(a.frames[k],x-a.anchorX*s,footY-a.footY*s,384*s,384*s);
 ctx.restore();return k;
}
