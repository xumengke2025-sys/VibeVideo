import fs from 'node:fs';
import path from 'node:path';
import cp from 'node:child_process';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const run=(args,cwd=root)=>cp.execFileSync(process.execPath,args,{cwd,encoding:'utf8',timeout:120000});
const git=(args)=>cp.execFileSync('git',args,{cwd:root,maxBuffer:20*1024*1024});
const sandbox=path.join(root,'.codex','publication-smoke-'+Date.now());fs.mkdirSync(sandbox,{recursive:true});
const staged=git(['diff','--cached','--name-only','-z']).toString().split('\0').filter(Boolean);
const provenance=JSON.parse(fs.readFileSync(path.join(root,'work/skill-publication-20261015/provenance-files.json')));
const exportFiles=[...new Set([...staged,...provenance])];
cp.execFileSync('git',['checkout-index','--prefix='+sandbox.replaceAll('\\','/')+'/','-z','--stdin'],{cwd:root,input:exportFiles.join('\0')+'\0',maxBuffer:1024*1024});
const plan=JSON.parse(run(['tools/restore-references.mjs','--dry-run'],sandbox));
if(plan.previewFilms!==319||plan.sourcePackages!==20||plan.files!==6478)throw Error('Wrong plan size');
const search=JSON.parse(run(['skill/vibe-video/scripts/video_examples.mjs','search','--query','纸艺','--limit','1'],sandbox));
if(!search.results[0].path.replaceAll('\\','/').startsWith(sandbox.replaceAll('\\','/')+'/'))throw Error('Video paths were not relocated');
const manifest=JSON.parse(fs.readFileSync(path.join(sandbox,'tools/reference-restore-manifest.json')));
const samples=[
 manifest.files.find(f=>f.relative.endsWith('shotcraft-media/mosaic-reframe.mp4')),
 manifest.files.find(f=>f.relative.endsWith('examples/museum-compound/out/compound.mp4')),
 manifest.files.filter(f=>f.relative.includes('/original-media/')&&f.relative.endsWith('.mp4')).sort((a,b)=>a.bytes-b.bytes)[0],
 manifest.files.find(f=>f.relative.endsWith('video-shotcraft-20261014/gallery/api/library.json'))
];
if(samples.some(x=>!x))throw Error('Missing smoke sample');
const results=[];
for(const sample of samples){const output=run(['tools/restore-references.mjs','--only',sample.relative],sandbox);const verified=run(['tools/restore-references.mjs','--only',sample.relative,'--verify-only'],sandbox);results.push({path:sample.relative,bytes:sample.bytes,restored:true,verified:JSON.parse(verified).failed===0});console.log('Restored and verified '+sample.relative);}
const result={checkedAt:new Date().toISOString(),sandbox,plan,relocationPassed:true,samples:results};
fs.writeFileSync(path.join(root,'work/skill-publication-20261015/smoke-verification.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({relocationPassed:true,samples:results.length,bytes:results.reduce((n,r)=>n+r.bytes,0)}));
