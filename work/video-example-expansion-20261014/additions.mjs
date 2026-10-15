import fs from 'node:fs';import path from 'node:path';import {execFileSync} from 'node:child_process';
export function loadAdditions(root,work){
 const read=p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,'')),slash=p=>p.replaceAll('\\','/');
 const manifest=read(path.join(root,'reference-sources/video-examples-20261014/manifest.json'));
 const verificationPath=path.join(root,'work/video-example-expansion-20261014/media-verification.json');
 const verified=new Map(fs.existsSync(verificationPath)?read(verificationPath).items.map(m=>[m.id,m]):[]);
 const packages=manifest.packages.map(p=>{
  const sourceRecord=slash(path.join(p.path,'SOURCE.json')),source=read(sourceRecord);
  const names=source.files?.map(f=>f.path)||execFileSync('git',['-C',p.path,'ls-files'],{encoding:'utf8',windowsHide:true}).trim().split('\n');
  const files=names.filter(f=>fs.existsSync(path.join(p.path,f)));const bytes=files.reduce((n,f)=>n+fs.statSync(path.join(p.path,f)).size,0);
  return{...p,repository:'https://github.com/'+p.repo,sourceRecord,files:files.length,bytes,modelEvidence:source.modelEvidence||[],scope:source.scope||'固定版本源码快照',executed:false,entries:p.entries.map(f=>({relative:f,path:slash(path.join(p.path,f))}))};
 });
 const media=manifest.media.map(m=>{const p=packages.find(p=>p.repo===m.repo);const v=verified.get(m.id);if(!fs.existsSync(m.entry)||!fs.existsSync(m.path))throw Error('Missing entry/media '+m.id);return{...m,packageId:p.id,url:encodeURI(slash(path.relative(work,m.path))),metadata:v?.metadata,decodePassed:v?.decodePassed,poster:v?.poster};});
 return{packages,media,failures:manifest.failures,excluded:manifest.excluded};
}
