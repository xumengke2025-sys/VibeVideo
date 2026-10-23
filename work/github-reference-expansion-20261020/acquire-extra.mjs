import fs from'node:fs';import path from'node:path';import crypto from'node:crypto';import{fileURLToPath}from'node:url';import{execFile}from'node:child_process';import{promisify}from'node:util';
const run=promisify(execFile),work=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(work,'../..'),base=path.join(root,'reference-sources/github-expansion-20261020'),slash=p=>p.replaceAll('\\','/'),read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const api=async p=>JSON.parse((await run('gh',['api',p],{timeout:60000,maxBuffer:16e6})).stdout);
const names=['lemomo-ai--lemo-opuscar','holooooo--myriad-worlds','krisuuu2--argon-vs-opus'];
const assets=[];
await Promise.all(names.map(async name=>{
 const j=read(path.join(work,'research',name,'research.json')),git=path.join(work,'git',name),dest=path.join(base,name);fs.mkdirSync(path.dirname(git),{recursive:true});
 if(name.startsWith('holooooo')&&!fs.existsSync(path.join(work,'research',name,'release-research.json'))){j.commit=(await api('repos/'+j.repo+'/commits/v1.0.2')).sha;j.tree=await api('repos/'+j.repo+'/git/trees/'+j.commit+'?recursive=1');fs.writeFileSync(path.join(work,'research',name,'release-research.json'),JSON.stringify(j,null,2));}
 if(!process.argv.includes('--downloads-only')&&!fs.existsSync(path.join(dest,'SOURCE.json'))){
  if(!fs.existsSync(path.join(git,'.git')))await run('git',['clone','--depth','1','--no-checkout',...(name.startsWith('holooooo')?['--branch','v1.0.2']:[]),'https://github.com/'+j.repo+'.git',git],{timeout:480000,maxBuffer:1024*1024});
  for(let n=0;fs.existsSync(path.join(git,'.git/shallow.lock'))&&n<480;n++)await new Promise(r=>setTimeout(r,1000));
  try{await run('git',['-C',git,'cat-file','-e',j.commit],{timeout:30000});}catch{await run('git',['-C',git,'fetch','--depth','1','origin',j.commit],{timeout:480000,maxBuffer:1e6});}
  const tar=path.join(work,name+'.tar');await run('git',['-c','core.autocrlf=false','-C',git,'archive','--format=tar','--output='+tar,j.commit],{timeout:60000});fs.mkdirSync(dest,{recursive:true});
  const blobs=j.tree.tree.filter(x=>x.type==='blob');for(const f of blobs)if(f.mode==='120000'||f.path.split('/').includes('..')||path.isAbsolute(f.path))throw Error('Unsafe path');
  await run('tar',['-xf',tar,'-C',dest],{timeout:120000,maxBuffer:1e6});
  const files=blobs.map(f=>{const b=fs.readFileSync(path.join(dest,f.path)),sha1=crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');if(sha1!==f.sha)throw Error('Blob mismatch '+f.path);return{path:f.path,bytes:b.length,sha256:crypto.createHash('sha256').update(b).digest('hex'),gitBlob:f.sha,url:'https://raw.githubusercontent.com/'+j.repo+'/'+j.commit+'/'+f.path.split('/').map(encodeURIComponent).join('/')};});
  fs.writeFileSync(path.join(dest,'SOURCE.json'),JSON.stringify({repo:j.repo,commit:j.commit,checked:'2026-10-20',scope:'固定提交完整仓库快照；未执行上游代码；Myriad固定影片发布标签v1.0.2',modelEvidence:name.startsWith('lemomo')?'作者README声明Opus 5.5代码制作；未独立证实':name.startsWith('holooooo')?'作者声明Opus 5.5奠基、GLM 5.3F继续开发；混合模型作品':'作者声明Gemini 4 Argon与Claude Opus 5.5同提示词对照',files},null,2)+'\n');console.log(JSON.stringify({archived:j.repo,files:files.length}));
 }
 if(name.startsWith('lemomo')){
  for(const id of ['archive-lighttable','briefing-board','data-physical','lidar-survey','microscope','satellite-briefing','teardown','white-model']){const a=j.releases.find(r=>r.tag_name==='web').assets.find(a=>a.name===id+'.mp4');if(!a)throw Error('Missing '+id);assets.push({...a,repo:j.repo,localPath:slash(path.join(dest,'release-media',a.name))});}
 }else if(name.startsWith('holooooo'))for(const a of j.releases.find(r=>r.tag_name==='v1.0.2').assets)assets.push({...a,repo:j.repo,localPath:slash(path.join(dest,'release-media',a.name))});
}));
fs.writeFileSync(path.join(work,'extra-assets.json'),JSON.stringify(assets,null,2));let cursor=0,done=0;
await Promise.all(Array.from({length:4},async()=>{while(cursor<assets.length){const a=assets[cursor++],dest=a.localPath;fs.mkdirSync(path.dirname(dest),{recursive:true});let valid=false;if(fs.existsSync(dest)){const b=fs.readFileSync(dest);valid=b.length===a.size&&(!a.digest||a.digest==='sha256:'+crypto.createHash('sha256').update(b).digest('hex'));}
 if(!valid){let error;for(const ip of ['185.199.111.133','185.199.109.133']){try{await run('curl.exe',['-fsSL','--resolve','release-assets.githubusercontent.com:443:'+ip,'--connect-timeout','10','--max-time','180',a.browser_download_url,'-o',dest+'.part'],{timeout:190000,maxBuffer:128e3});const b=fs.readFileSync(dest+'.part'),hash=crypto.createHash('sha256').update(b).digest('hex');if(b.length!==a.size||(a.digest&&a.digest!=='sha256:'+hash))throw Error('Release hash mismatch '+a.name+' bytes '+b.length);fs.renameSync(dest+'.part',dest);error=null;break;}catch(e){error=e;}}if(error)throw error;}done++;console.log('Release assets '+done+'/'+assets.length+' '+a.name);
}}));
