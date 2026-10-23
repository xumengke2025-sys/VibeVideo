import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {fileURLToPath} from 'node:url';
const run=promisify(execFile),work=path.dirname(fileURLToPath(import.meta.url));
const assets=JSON.parse(fs.readFileSync(path.join(work,'extra-assets.json'),'utf8'));
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const tasks=[],pending=[],block=2*1024*1024;
for(const a of assets){
 if(fs.existsSync(a.localPath)){const b=fs.readFileSync(a.localPath);if(b.length===a.size&&a.digest==='sha256:'+hash(b))continue;}
 const dir=path.join(work,'release-parts',a.repo.replace('/','--'),a.name);
 const chunks=Array.from({length:Math.ceil(a.size/block)},(_,i)=>({i,start:i*block,end:Math.min((i+1)*block,a.size)-1}));
 for(const c of chunks){const file=path.join(dir,c.i+'.bin'),header=file+'.headers',have=fs.existsSync(file)?fs.statSync(file).size:0;
  if(have&&(!fs.existsSync(header)||!fs.readFileSync(header,'utf8').includes(`bytes ${c.start}-${c.end}/${a.size}`)))throw Error('Unverified prefix '+file);
  if(have>c.end-c.start+1)throw Error('Oversize prefix');
  if(have<c.end-c.start+1)tasks.push({a,c,file,header});
 }
 pending.push({a,dir,chunks});
}
let at=0,done=0;const errors=[];
await Promise.all(Array.from({length:4},async()=>{while(at<tasks.length){const {a,c,file,header:originalHeader}=tasks[at++];try{
 const cached=fs.readFileSync(originalHeader,'utf8').match(/^location:\s*(https:\/\/release-assets[^\r\n]+)/im)?.[1];
 const direct=cached&&Date.parse(new URL(cached).searchParams.get('se'))>Date.now()+60000?cached:null;
 for(let attempt=0;fs.statSync(file).size<c.end-c.start+1&&attempt<24;attempt++){
  const have=fs.statSync(file).size,start=c.start+have,end=Math.min(start+512*1024-1,c.end),tail=file+'.tail',header=tail+'.headers';
  let err;try{await run('curl.exe',['-fsSL','--resolve','release-assets.githubusercontent.com:443:'+['185.199.111.133','185.199.109.133'][attempt%2],'--connect-timeout','10','--max-time','45','--range',`${start}-${end}`,'--dump-header',header,'--output',tail,direct||a.browser_download_url+'?resume='+start],{timeout:50000,maxBuffer:128e3});}catch(e){err=e;}
  const bytes=fs.existsSync(tail)?fs.statSync(tail).size:0;
  if(bytes&&bytes<=end-start+1&&fs.existsSync(header)&&fs.readFileSync(header,'utf8').includes(`bytes ${start}-${end}/${a.size}`))fs.appendFileSync(file,fs.readFileSync(tail));
  else if(!err)throw Error('Invalid resumed range');
  if(bytes)console.log(JSON.stringify({video:a.name,chunk:c.i,received:bytes,remaining:c.end-c.start+1-fs.statSync(file).size}));
 }
 if(fs.statSync(file).size!==c.end-c.start+1)throw Error('Incomplete after bounded resumes');
 done++;console.log('Recovered chunks '+done+'/'+tasks.length);
 }catch(e){errors.push({name:a.name,chunk:c.i,error:e.message});}}}));
fs.writeFileSync(path.join(work,'release-resume-errors.json'),JSON.stringify(errors,null,2));
for(const {a,dir,chunks}of pending){
 if(chunks.some(c=>!fs.existsSync(path.join(dir,c.i+'.bin'))||fs.statSync(path.join(dir,c.i+'.bin')).size!==c.end-c.start+1))continue;
 const b=Buffer.concat(chunks.map(c=>fs.readFileSync(path.join(dir,c.i+'.bin'))));
 if(b.length!==a.size||a.digest!=='sha256:'+hash(b))throw Error('Final digest mismatch '+a.name);
 fs.writeFileSync(a.localPath+'.assembled',b);fs.renameSync(a.localPath+'.assembled',a.localPath);
 console.log(JSON.stringify({downloaded:a.name,bytes:b.length,digestMatched:true}));
}
if(errors.length)process.exitCode=1;
