import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const run=promisify(execFile),work=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(work,'../..');
const repos=process.argv.slice(2);
async function api(p){return JSON.parse((await run('gh',['api',p],{timeout:60000,maxBuffer:16*1024*1024})).stdout);}
const catalog=JSON.parse(fs.readFileSync(path.join(root,'work/github-reference-expansion-20261011/catalog.json')));
if(!fs.existsSync(path.join(work,'baseline.json')))fs.writeFileSync(path.join(work,'baseline.json'),JSON.stringify(catalog,null,2));
async function inspect(repo){
 const target=path.join(work,'research',repo.replace('/','--'));fs.mkdirSync(target,{recursive:true});
 try {
 const meta=await api('repos/'+repo),commit=(await api('repos/'+repo+'/commits/'+meta.default_branch)).sha;
 const [tree,readme,releases]=await Promise.all([api('repos/'+repo+'/git/trees/'+commit+'?recursive=1'),api('repos/'+repo+'/readme?ref='+commit).catch(()=>null),api('repos/'+repo+'/releases')]);
 const text=readme?Buffer.from(readme.content,'base64').toString('utf8'):'';fs.writeFileSync(path.join(target,'README.md'),text);
 fs.writeFileSync(path.join(target,'research.json'),JSON.stringify({repo,commit,meta,tree,releases},null,2));
 const blobs=tree.tree.filter(x=>x.type==='blob');
 console.log(JSON.stringify({repo,commit,files:blobs.length,bytes:blobs.reduce((n,x)=>n+(x.size||0),0),license:meta.license?.spdx_id,media:blobs.filter(x=>/\.(mp4|webm|mov|gif)$/i.test(x.path)).map(x=>({path:x.path,size:x.size})).slice(0,45),readme:text.split('\n').filter(l=>/opus|5\.5|mp4|webm|license|preview|demo/i.test(l)).slice(0,18),releases:releases.slice(0,2).map(r=>({tag:r.tag_name,assets:r.assets.map(a=>({name:a.name,size:a.size,url:a.browser_download_url}))}))}));
 } catch(e) {console.log(JSON.stringify({repo,error:e.message}));}
}
for(let i=0;i<repos.length;i+=3)await Promise.all(repos.slice(i,i+3).map(inspect));
