import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import{fileURLToPath}from'node:url';import{execFile}from'node:child_process';import{promisify}from'node:util';
const work=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(work,'../..'),base=path.join(root,'reference-sources/github-expansion-20261020'),run=promisify(execFile),slash=p=>p.replaceAll('\\','/');fs.mkdirSync(base,{recursive:true});
async function archive(name){
 const j=JSON.parse(fs.readFileSync(path.join(work,'research',name,'research.json'))),dest=path.join(base,name),blobs=j.tree.tree.filter(x=>x.type==='blob');
 for(const f of blobs)if(f.mode==='120000'||path.isAbsolute(f.path)||f.path.split('/').includes('..'))throw Error('Unsafe archive path '+f.path);
 const zip=path.join(work,name+'.zip'),staging=path.join(work,'extract',name);fs.mkdirSync(staging,{recursive:true});
 if(!fs.existsSync(dest)){
  const git=path.join(work,'git',name);
  if(fs.existsSync(path.join(git,'.git'))){
   await run('git',['-C',git,'cat-file','-e',j.commit],{timeout:30000});
   const tar=path.join(work,name+'.tar');await run('git',['-c','core.autocrlf=false','-C',git,'archive','--format=tar','--output='+tar,j.commit],{timeout:60000});
   fs.mkdirSync(dest,{recursive:true});await run('tar',['-xf',tar,'-C',dest],{timeout:120000,maxBuffer:1024*1024});
  }else{
   if(!fs.existsSync(zip)||!fs.statSync(zip).size){await run('curl.exe',['-fL','--retry','2','--connect-timeout','20','--max-time','360','https://codeload.github.com/'+j.repo+'/zip/'+j.commit,'-o',zip+'.part'],{timeout:760000,maxBuffer:1024*1024});fs.renameSync(zip+'.part',zip);}
   await run('tar',['-xf',zip,'-C',staging],{timeout:120000,maxBuffer:1024*1024});
   const top=fs.readdirSync(staging);if(top.length!==1)throw Error('Unexpected archive root');fs.renameSync(path.join(staging,top[0]),dest);
  }
 }
 const files=blobs.map(f=>{const p=path.join(dest,f.path),buf=fs.readFileSync(p),blob=crypto.createHash('sha1').update(Buffer.from('blob '+buf.length+'\0')).update(buf).digest('hex');if(buf.length!==f.size||blob!==f.sha)throw Error('Git blob mismatch '+p);return{path:f.path,bytes:buf.length,sha256:crypto.createHash('sha256').update(buf).digest('hex'),gitBlob:f.sha,url:'https://raw.githubusercontent.com/'+j.repo+'/'+j.commit+'/'+f.path.split('/').map(encodeURIComponent).join('/')};});
 const source={repo:j.repo,repository:'https://github.com/'+j.repo,commit:j.commit,checked:'2026-10-20',scope:'固定提交完整仓库快照，不含Git历史；未安装依赖或执行上游代码',modelEvidence:name.startsWith('lumian')?'README声明复刻热门Claude Opus 5.5影片；复刻源码模型未逐例证实':'README支持Opus 5.5与GPT-6.1 Sol；139个风格样段未逐例公开模型证据，不作为Opus原片',license:name.startsWith('lumian')?'MIT；GSAP、字体及第三方资源另按原许可':'Kiteva Non-Commercial License 1.0；第三方组件另按各自许可',files};
 fs.writeFileSync(path.join(dest,'SOURCE.json'),JSON.stringify(source,null,2)+'\n');console.log(JSON.stringify({archived:j.repo,files:files.length,bytes:files.reduce((n,f)=>n+f.bytes,0)}));
 return {repo:j.repo,path:slash(dest),commit:j.commit,files:files.length,bytes:files.reduce((n,f)=>n+f.bytes,0)};
}
const archives=await Promise.all((process.argv.includes('--templates-only')?['lumian2015--opus-5-5-video-templates']:['lumian2015--opus-5-5-video-templates','delexw--kiteva']).map(archive));fs.writeFileSync(path.join(work,'archives.json'),JSON.stringify(archives,null,2)+'\n');
const readme=fs.readFileSync(path.join(base,'lumian2015--opus-5-5-video-templates','README.md'),'utf8'),urls=[...new Set(readme.match(/https:\/\/cdn\.claudeimagine\.com\/uploads\/opus-5-5-video\/[^)\s]+\.mp4/g))],films=path.join(base,'lumian2015--opus-5-5-video-templates','previews');fs.mkdirSync(films,{recursive:true});
const results=[];let next=0;await Promise.all(Array.from({length:4},async()=>{while(next<urls.length){const url=urls[next++],dest=path.join(films,path.basename(url));try{if(!fs.existsSync(dest))await run('curl.exe',['-fL','--retry','2','--connect-timeout','15','--max-time','120',url,'-o',dest+'.part'],{timeout:270000,maxBuffer:128*1024});if(fs.existsSync(dest+'.part'))fs.renameSync(dest+'.part',dest);const b=fs.readFileSync(dest);results.push({path:slash(dest),url,bytes:b.length,sha256:crypto.createHash('sha256').update(b).digest('hex')});}catch(e){results.push({url,error:e.message.slice(0,250)});}if(results.length%10===0)console.log('Template previews downloaded: '+results.length);}}));
fs.writeFileSync(path.join(work,'downloads.json'),JSON.stringify(results,null,2)+'\n');console.log(JSON.stringify({templateFilms:results.filter(x=>!x.error).length,failures:results.filter(x=>x.error).length}));
