import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {fileURLToPath} from 'node:url';import {execFile} from 'node:child_process';import {promisify} from 'node:util';
const run=promisify(execFile);
const work=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(work,'../..'),base=path.join(root,'reference-sources/github-expansion-20261013');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8')),slash=p=>p.replaceAll('\\','/');fs.mkdirSync(base,{recursive:true});
const repos=process.argv.slice(2).length?process.argv.slice(2):['az9713/opus-5.5-musical-cartoon','bilaldemirerr/opus-video-recipes','c5inco/motion-showreel','toankhontech/pelican-test-opus55','JakeB-5/motion-graphic-skill','Vincentwei1021/mg-styles-15','DDChen666/civilization-film'];
const upstream=read(path.join(root,'reference-sources/upstream-videos/manifest.json')).items;
async function download(url,target,expected,blob,digest){
 function valid(){if(!fs.existsSync(target))return false;const data=fs.readFileSync(target);if(expected!=null&&data.length!==expected)return false;if(blob&&crypto.createHash('sha1').update(Buffer.from(`blob ${data.length}\0`)).update(data).digest('hex')!==blob)return false;if(digest&&crypto.createHash('sha256').update(data).digest('hex')!==digest.replace(/^sha256:/,''))return false;return true;}
 if(!valid()){let error;for(let attempt=0;attempt<3;attempt++){try{fs.mkdirSync(path.dirname(target),{recursive:true});await run('curl.exe',['--fail','--location','--silent','--show-error','--connect-timeout','25','--max-time','300','--output',target+'.part',url],{timeout:310000,maxBuffer:512*1024});fs.renameSync(target+'.part',target);if(!valid())throw Error('Hash/size mismatch');error=null;break;}catch(e){error=e;}}if(error)throw error;}
 const data=fs.readFileSync(target);return {bytes:data.length,sha256:crypto.createHash('sha256').update(data).digest('hex')};
}
const manifestPath=path.join(base,'manifest.json');const items=fs.existsSync(manifestPath)?read(manifestPath).items.filter(i=>!repos.includes(i.repo)):[];
for(const repo of repos){
 const id=repo.replace('/','--'),research=read(path.join(work,'research',id,'research.json')),target=path.join(base,id),records=[],tasks=research.tree.tree.filter(f=>f.type==='blob'&& !(repo.startsWith('JakeB')&&(/^samples\/codex-studio\//.test(f.path)||/\/sonnet\//.test(f.path))));
 let cursor=0,done=0;console.log(JSON.stringify({start:repo,files:tasks.length}));
 async function worker(){while(cursor<tasks.length){const f=tasks[cursor++];const full=path.resolve(target,f.path+(f.mode==='120000'?'.symlink.txt':''));if(!full.startsWith(path.resolve(target)+path.sep))throw Error('Unsafe path');
 let reused=null;if(repo==='Vincentwei1021/mg-styles-15'&&f.path.endsWith('.mp4'))reused=upstream.find(m=>m.sourcePath===f.path&&m.packageId==='mg-styles-15'&&m.commit===research.commit&&m.status==='downloaded');
 const local=reused?.path||full,url=`https://raw.githubusercontent.com/${repo}/${research.commit}/${f.path.split('/').map(encodeURIComponent).join('/')}`;
 const check=await download(url,local,f.size,f.sha);records.push({path:f.path,localPath:slash(local),gitBlobSha1:f.sha,url,...check,reusedExistingMedia:!!reused,...(f.mode==='120000'?{storedAs:'symlink target text; no symlink created'}:{})});done++;if(done%40===0)console.log(JSON.stringify({repo,done,total:tasks.length}));}}
 await Promise.all(Array.from({length:8},worker));
 const release=research.releases.find(r=>r.tag_name==='v1.0');
 if(repo==='DDChen666/civilization-film'||repo==='c5inco/motion-showreel'){
  const asset=release.assets.find(a=>repo.startsWith('DDChen')?a.name==='civilization_zh-CN_1080p.mp4':a.name==='showreel.mp4');if(!asset)throw Error('Missing release asset');
  const f='release-media/'+asset.name,full=path.join(target,f),check=await download(asset.browser_download_url,full,asset.size,null,asset.digest);
  records.push({path:f,localPath:slash(full),url:asset.browser_download_url,releaseTag:release.tag_name,releaseAssetId:asset.id,upstreamDigest:asset.digest,role:'author-release-film',...check});
 }
 records.sort((a,b)=>a.path.localeCompare(b.path));const readme=fs.readFileSync(path.join(target,'README.md'),'utf8'),licenseFiles=records.filter(f=>/LICENSE|COPYING|CREDITS|NOTICE/i.test(f.path)).map(f=>f.path);
 const source={repo,repository:'https://github.com/'+repo,commit:research.commit,checked:'2026-10-13',scope:repo.startsWith('JakeB')?'完整仓库文件快照，排除 Codex 与 Sonnet 示例；只收录 Opus 影片':repo.startsWith('Vincent')?'完整仓库文件快照；15个MP4复用已有本地作者影片，不重复下载':'完整仓库文件快照；发布影片另存 release-media',modelEvidence:readme.split('\n').filter(l=>/Opus 5\.5|Claude Opus/i.test(l)).slice(0,12),modelEvidenceStatus:'作者自述；未独立核实模型会话',licenseFiles,files:records,executed:false};
 fs.writeFileSync(path.join(target,'SOURCE.json'),JSON.stringify(source,null,2));
 items.push({repo,id,status:'archived',commit:research.commit,path:slash(target),files:records.length,bytes:records.reduce((n,f)=>n+f.bytes,0),media:records.filter(f=>/\.mp4$/i.test(f.path)),licenseFiles,modelEvidence:source.modelEvidence,scope:source.scope});
 fs.writeFileSync(path.join(base,'manifest.json'),JSON.stringify({checked:'2026-10-13',items},null,2));console.log(JSON.stringify({archived:repo,files:records.length,videos:items.at(-1).media.length}));
}
