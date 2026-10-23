import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const root=path.dirname(fileURLToPath(import.meta.url));
const upstream=path.resolve(root,'../../reference-sources/video-films-20261014/alchaincyf--huashu-art-motion');
const vendor=path.join(root,'vendor/huashu'); fs.mkdirSync(vendor,{recursive:true});
const modules=['01_cave','02_egypt','03_greek','04_roman','34_shadowpuppet','05_gothic','06_renaissance','32_rembrandt','17_ink','08_impressionism','09_postimp','11_cubism','33_rubberhose','23_dali','13_pop','14_8bit'];
const sha=s=>createHash('sha256').update(s).digest('hex');
const records=[];
function copy(rel,out,modify=s=>s){const input=fs.readFileSync(path.join(upstream,rel));const output=modify(input.toString('utf8'));fs.writeFileSync(path.join(vendor,out),output);records.push({source:rel,local:'vendor/huashu/'+out,source_sha256:sha(input),local_sha256:sha(output),adapted:input.toString('utf8')!==output});}
copy('LICENSE','LICENSE');
for(const name of ['util','paint','kit','brush','render','rig'])copy('scripts/engine/lib/'+name+'.js',name+'.js');
const exports={
 '01_cave':"c.drawImage(bg(),0,0);",
 '02_egypt':"staticLayer(c);",
 '03_greek':"c.drawImage(bg(),0,0);c.drawImage(topStrip(),0,30);c.drawImage(botStrip(),0,930);rosette(c,960,300,45,0);c.drawImage(vignette(),0,0);",
 '04_roman':"const b=P.canvas(),g=b.getContext('2d');g.fillStyle=C.wall;g.fillRect(0,0,W,H);picture(g);border(g,0);P.mosaic(c,b,{tile:9,grout:'#a3977c',seed:2079,jitter:.22});",
 '34_shadowpuppet':"screen(c,0);",
 '05_gothic':"parchment(c);lattice(c);architecture(c);windowStatic(c);",
 '06_renaissance':"c.drawImage(STATIC(),0,0);c.drawImage(OVER(),0,0);",
 '32_rembrandt':"c.drawImage(stat(),0,0);c.globalAlpha=.3;c.drawImage(beam(),0,0);c.globalAlpha=1;",
 '17_ink':"c.drawImage(paper(),0,0);mountains(c);bamboo(c,0);",
 '08_impressionism':"const b=P.canvas(),g=b.getContext('2d');base(g,0);c.fillStyle='#f2e6ee';c.fillRect(0,0,W,H);P.strokes(c,b,{cell:7,len:16,width:5,angle,seed:12,t:0,boil:0,outline:0,palette:stable(palette)});",
 '09_postimp':"const b=P.canvas(),g=b.getContext('2d');base(g,0);c.drawImage(b,0,0);P.strokes(c,b,{cell:10,len:38,width:7,angle,seed:19,t:0,boil:0,outline:.8,outlineMix:.38,palette});",
 '11_cubism':"c.drawImage(bg(),0,0);",
 '33_rubberhose':"c.drawImage(bg(),0,0);windowAndSky(c,0);",
 '23_dali':"c.drawImage(bg(),0,0);",
 '13_pop':"c.drawImage(bg(),0,0);c.fillStyle=dotPattern(c,'wall',24,5.6,C.blue,C.white);c.fillRect(0,0,1920,700);",
 '14_8bit':"c.save();c.scale(8,8);background(c);c.restore();"
};
for(const name of modules){copy('scripts/engine/scenes/'+name+'.js',name+'.js',s=>{
 // Expose only native material/background entry points; the original narrative draw is never called.
 // Remove original furniture and writing from selected background closures.
 if(name==='01_cave')s=s.replace(/    \/\/ 石凳（少女坐）[\s\S]*?(?=    lg.globalCompositeOperation = 'source-atop')/,'');
 if(name==='02_egypt')s=s.replace(/    GROUPS.forEach[^\n]*g.strokeStyle[^\n]*\n/,'').replace(/    GLYPHS.forEach[^\n]*\n/,'').replace(/    \/\/ —— 左侧尖底陶罐[\s\S]*?(?=    \/\/ —— 地线)/,'');
 if(name==='32_rembrandt')s=s.replace(/    \/\/ 桌毯：单独一层[\s\S]*?(?=  \}\);)/,'');
 if(name==='13_pop')s=s.replace(/    \/\/ MEANWHILE[\s\S]*?(?=    \/\/ 沃霍尔)/,'');
 const at=s.lastIndexOf('  return {'); if(at<0)throw Error(name+' export not found');
 return s.slice(0,at)+'  const sourceBackground = (c) => { c.save(); '+exports[name]+' c.restore(); };\n'+s.slice(at).replace('  return {','  return { sourceBackground,');
 });}
fs.writeFileSync(path.join(vendor,'provenance.json'),JSON.stringify({upstream:'alchaincyf/huashu-art-motion',commit:'64cb27271ee0ad3375298e2890b33cbec36d4051',license:'MIT',note:'Native background/material functions exposed in adapted copies. Original people, dialogue, and scene draw functions are not rendered. Portrait adapter crops materials at uniform scale and recomposes motifs.',records},null,2));
const tags=['util','paint','kit','brush','render','rig',...modules].map(n=>'<script src="vendor/huashu/'+n+'.js"></script>').join('\n');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
fs.writeFileSync(path.join(root,'rebuild-v3.html'),html.replace('<script type="module" src="src/film.js"></script>','<script>window.SCENES={};</script>\n'+tags+'\n<script type="module" src="src/film-v3.js"></script>'));
console.log('Vendored '+records.length+' files with source hashes and MIT notice.');
