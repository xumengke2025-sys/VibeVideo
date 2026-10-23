import fs from 'node:fs';
import path from 'node:path';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const run=promisify(execFile),root=path.dirname(new URL(import.meta.url).pathname.replace(/^\/(\w:)/,'$1'));
const work=decodeURIComponent(root);
const repos=['aadil6971/clawd-video'];
async function api(p){return JSON.parse((await run('gh',['api',p],{timeout:90000,maxBuffer:8*1024*1024})).stdout);}
async function inspect(repo){
 const target=path.join(work,'research',repo.replace('/','--'));fs.mkdirSync(target,{recursive:true});
 const meta=await api('repos/'+repo),commit=(await api('repos/'+repo+'/commits/'+meta.default_branch)).sha;
 const [tree,readme,releases]=await Promise.all([api('repos/'+repo+'/git/trees/'+commit+'?recursive=1'),api('repos/'+repo+'/readme?ref='+commit),api('repos/'+repo+'/releases')]);
 const text=Buffer.from(readme.content,'base64').toString('utf8');fs.writeFileSync(path.join(target,'README.md'),text);
 fs.writeFileSync(path.join(target,'research.json'),JSON.stringify({repo,commit,meta,tree,releases},null,2));
 console.log(JSON.stringify({repo,commit,files:tree.tree.filter(x=>x.type==='blob').length,bytes:tree.tree.reduce((n,x)=>n+(x.size||0),0),readme:text.split('\n').filter(l=>/opus 5\.5|license|hero|clawd-prose/i.test(l)).slice(0,12),releases:releases.slice(0,2).map(r=>({tag:r.tag_name,target:r.target_commitish,assets:r.assets.map(a=>({name:a.name,size:a.size,url:a.browser_download_url}))}))}));
}
for(let i=0;i<repos.length;i+=4)await Promise.all(repos.slice(i,i+4).map(inspect));
