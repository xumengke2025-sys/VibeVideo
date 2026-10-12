from pathlib import Path
import json
R=Path(__file__).parent/'source-snapshots/Lugia123'
src=(R/'comic.js').read_text(encoding='utf-8').splitlines()
helpers='\n'.join(src[82:111])+ '\n'+ '\n'.join(src[123:127])
fragment=(R/'p4-action-fragment.txt').read_text(encoding='utf-8')
header='''// Study-only extraction from Lugia123/ai-video MIT source, pinned 1c22f438.
// Author's p4 draw closure preserved. Normalized 0–1.6s timing; no original song/lyrics.
const canvas=document.getElementById('film');canvas.width=960;canvas.height=540;const ctx=canvas.getContext('2d');
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x)),lerp=(a,b,p)=>a+(b-a)*p,smooth=p=>{p=clamp(p);return p*p*(3-2*p)};
const hash=(a,b=0)=>{let h=Math.imul(a|0,374761393)+Math.imul(b|0,668265263);h=Math.imul(h^(h>>>13),1274126177);return((h^(h>>>16))>>>0)/4294967296};
const PAL={ink:'#0A0A10'};const TP={p4:0},C3V={fuse:1.6},K4={src:[.17,.47,.65,.38],top:.4,root:[.71,.86],ropeX:.8,ign:.1};
const im=new Image();im.src='k4.png';await im.decode();const I={k4:im};
const jitter=(c,a,T,s=1)=>c.translate(a*Math.sin(T*91*s),a*Math.cos(T*77*s));
const p4Spark=(T,b)=>{const k=T-TP.p4-K4.ign,u=clamp(k/(C3V.fuse-TP.p4-K4.ign));return k<0?[K4.root[0]*b.w,K4.root[1]*b.h,0]:[lerp(K4.root[0],K4.ropeX,smooth(u*4))*b.w,lerp(K4.root[1],-.12,u*u*.75+u*.25)*b.h,u]};
'''
(R/'fragment.mjs').write_text(header+'const CX={'+helpers+'};\nconst draw='+fragment+''';
function renderAt(t){ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,960,540);draw(ctx,{x:0,y:0,w:960,h:540},t)}
window.__film={ready:true,renderAt};renderAt(0);
''',encoding='utf-8')
(R/'fragment.html').write_text('<!doctype html><meta charset="utf-8"><link rel="icon" href="data:,"><style>body{margin:0;background:#000}canvas{display:block}</style><canvas id="film"></canvas><script type="module" src="fragment.mjs"></script>',encoding='utf-8')
(R/'fragment-version.json').write_text(json.dumps({'source_commit':'1c22f4384f1ed42045666ea47f7b9b0946a9df16','source_lines':'c3-v7.final.js:374–397; comic.js:83–111,124–127','rights':'upstream MIT code; k4 study only, generation origin not independently verified','observed_version':'isolated p4 layer action, 0–1.6 normalized timing','not_original_mv':True,'excluded':['original lyric timing','full comic camera path','3D context','postprocessing','audio']},indent=2),encoding='utf-8')
print('Fragment built')
