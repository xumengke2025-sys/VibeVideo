import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const work=path.dirname(fileURLToPath(import.meta.url));
const repos=['AbubakrChan/product-launch-motion','tin-computer/tin-film-lab','claude-skills-kit/cosmic-opus','Intentface/intentface-launch','Chaoqi31/opus-paints','Vishnu-tppr/motionloom-studio'];
const gh=(args)=>execFileSync('C:/Program Files/GitHub CLI/gh.exe',args,{encoding:'utf8',maxBuffer:12*1024*1024,timeout:60000});
for(const repo of repos){
 const dir=path.join(work,'discovery',repo.replace('/','--'));fs.mkdirSync(dir,{recursive:true});
 const info=JSON.parse(gh(['api',`repos/${repo}`]));
 const tree=JSON.parse(gh(['api',`repos/${repo}/git/trees/HEAD?recursive=1`]));
 fs.writeFileSync(path.join(dir,'tree.json'),JSON.stringify(tree,null,2));
 fs.writeFileSync(path.join(dir,'repo.json'),JSON.stringify(info,null,2));
 for(const f of tree.tree.filter(f=>f.type==='blob'&&['README.md','LICENSE'].includes(f.path))){
  const raw=gh(['api',`repos/${repo}/contents/${f.path}?ref=${tree.sha}`,'-H','Accept: application/vnd.github.raw+json']);
  fs.writeFileSync(path.join(dir,f.path),raw);
 }
 console.log(JSON.stringify({repo,commit:tree.sha,license:info.license?.spdx_id,files:tree.tree.filter(f=>f.type==='blob').length,MB:Math.round(tree.tree.reduce((n,f)=>n+(f.size||0),0)/1048576)}));
}
const lib=JSON.parse(fs.readFileSync('D:/Codex/skills/vibe-video/references/shotcraft-library.json','utf8'));
fs.writeFileSync(path.join(work,'shotcraft-options.json'),JSON.stringify(lib.cards.filter(c=>['camera','data','transition','outro','interaction','effects'].includes(c.category)),null,2));
