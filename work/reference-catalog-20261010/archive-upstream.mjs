import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {fileURLToPath} from 'node:url';

const run=promisify(execFile);
const work=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(work,'../..');
const destination=path.join(root,'reference-sources/upstream-videos');
const discovery=path.join(work,'upstream-discovery');
const probe='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe';
const slash=p=>p.replaceAll('\\','/');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const catalog=read(path.join(work,'catalog.json'));
const packages=new Map(catalog.packages.map(p=>[p.id,p]));
const tasks=[];
const manifestPath=path.join(destination,'manifest.json');
fs.mkdirSync(destination,{recursive:true});

function add(task){task.path=slash(path.join(destination,task.packageId,task.filename));task.status='pending';tasks.push(task)}
function fromTree(packageId,select){const p=packages.get(packageId);const tree=read(path.join(discovery,`${packageId}.json`)).tree;for(const file of tree.filter(select)){
 const styleId=path.basename(file.path,path.extname(file.path));
 const mg=catalog.mg.find(s=>s.id===styleId);
 add({id:`${packageId}/${styleId}`,packageId,styleId,title:mg?`MG / ${mg.title}`:`${p.title} / ${styleId}`,filename:path.basename(file.path),url:`https://raw.githubusercontent.com/${p.repository.replace('https://github.com/','')}/${p.commit}/${file.path}`,repository:p.repository,commit:p.commit,sourcePath:file.path,expectedBytes:file.size,gitBlobSha1:file.sha,entry:mg?.entry||p.entry,representation:path.extname(file.path)==='.gif'?'author-gif':'author-published-video',note:path.extname(file.path)==='.gif'?'作者发布的GIF演示，无声；不是完整MP4影片':'作者仓库发布版本，保持下载文件原样'});
}}
fromTree('mg-styles-15',f=>/^videos\/.*\.mp4$/.test(f.path));
fromTree('songbie',f=>f.path==='media/songbie.mp4');
fromTree('water-opus',f=>f.path==='runs/claude-code-opus-5-5/docs/demo.mp4');
fromTree('work-reel-26',f=>/\.gif$/.test(f.path));
fromTree('three-avbd',f=>f.path==='docs/media/trailer.gif');

const releases=read(path.join(discovery,'lemo-releases.json'));
const films=releases.find(r=>r.tag_name==='films');
for(const asset of films.assets.filter(a=>/\.mp4$/.test(a.name))){const styleId=path.basename(asset.name,'.mp4');const s=catalog.lemo.find(s=>s.id===styleId);add({id:`lemo-opuscar/${styleId}`,packageId:'lemo-opuscar',styleId,title:s?`Lemo / ${s.title}`:'Lemo / OPUSCAR 98',filename:asset.name,url:asset.browser_download_url,repository:'https://github.com/lemomo-ai/lemo-opuscar',releaseTag:'films',releaseId:films.id,assetId:asset.id,assetUpdated:asset.updated_at,expectedBytes:asset.size,expectedSha256:asset.digest?.replace('sha256:',''),entry:s?.entry||null,remoteCode:s?.guide||'https://github.com/lemomo-ai/lemo-opuscar',representation:'author-master',note:'作者films发布的原始高码率版本；发布附件与本地固定源码的逐像素一致性未确认'});}

const paperText=fs.readFileSync(path.join(discovery,'paper-readme.txt'),'utf8');
for(const block of paperText.split(/^### /m).slice(1)){const heading=block.split('\n')[0];const attachment=block.match(/https:\/\/github.com\/user-attachments\/assets\/[\w-]+/);if(!attachment)continue;const styleId=heading.match(/`([^`]+)`/)?.[1]||attachment[0].split('/').at(-1);const entry=`D:/Codex/skills/vibe-video/assets/code-studies/papermotion/examples/${styleId}/main.ts`;add({id:`papermotion/${styleId}`,packageId:'papermotion',styleId,title:`PaperMotion / ${heading.replace(/\s*\(`[^`]+`\)/,'')}`,filename:`${styleId}.mp4`,url:attachment[0],repository:packages.get('papermotion').repository,sourceDocument:'README.md (downloaded 2026-10-10)',entry:fs.existsSync(entry)?entry:null,representation:'author-attachment',note:'作者README中的公开视频附件；没有把它归为本地重新渲染'});}
const beachText=fs.readFileSync(path.join(discovery,'beach-readme.txt'),'utf8');
for(const [i,url] of [...new Set(beachText.match(/https:\/\/github.com\/user-attachments\/assets\/[\w-]+/g)||[])].entries())add({id:`particle-beach/trailer-${i+1}`,packageId:'particle-beach',styleId:'trailer',title:'粒子海滩 / 作者预告片',filename:`trailer-${i+1}.mp4`,url,repository:packages.get('particle-beach').repository,entry:packages.get('particle-beach').entry,representation:'author-attachment',note:'作者README中的预告附件；保持原文件，不是本地重渲'});

if(fs.existsSync(path.join(discovery,'extra-media.json')))for(const task of read(path.join(discovery,'extra-media.json')))add(task);
const unique=new Map(tasks.map(t=>[t.id,t]));
tasks.splice(0,tasks.length,...unique.values());
const old=fs.existsSync(manifestPath)?read(manifestPath):null;
for(const task of tasks){const existing=old?.items.find(i=>i.id===task.id&&i.url===task.url);if(existing?.status==='downloaded'&&fs.existsSync(existing.path)&&fs.statSync(existing.path).size===existing.bytes)Object.assign(task,existing);else if(existing?.status==='failed'&&existing.error?.includes('404'))Object.assign(task,existing)}

function save(){const payload={checked:'2026-10-10',scope:'上条清单的固定源码工程、MG15种、Lemo43种及其作者附带影片；不自动扩展为513条图库全部视频',items:tasks,summary:{planned:tasks.length,downloaded:tasks.filter(t=>t.status==='downloaded').length,failed:tasks.filter(t=>t.status==='failed').length,bytes:tasks.filter(t=>t.status==='downloaded').reduce((sum,t)=>sum+t.bytes,0)}};const temp=manifestPath+'.tmp';fs.writeFileSync(temp,JSON.stringify(payload,null,2));fs.renameSync(temp,manifestPath)}
async function hashes(filename){const sha256=crypto.createHash('sha256');const git=crypto.createHash('sha1');const size=fs.statSync(filename).size;git.update(`blob ${size}\0`);for await(const chunk of fs.createReadStream(filename)){sha256.update(chunk);git.update(chunk)}return {sha256:sha256.digest('hex'),gitBlobSha1:git.digest('hex')}}
async function inspect(filename){const result=await run(probe,['-v','error','-show_entries','format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate','-of','json',filename],{maxBuffer:1024*1024,timeout:30000});const data=JSON.parse(result.stdout);const video=data.streams?.find(s=>s.codec_type==='video');if(!video||!video.width||!video.height)throw new Error('No readable video stream');return {duration:Number(data.format?.duration)||null,width:video.width,height:video.height,fps:video.r_frame_rate,codec:video.codec_name,audio:data.streams.some(s=>s.codec_type==='audio')}}

let cursor=0;
save();
console.log(JSON.stringify({phase:'plan',count:tasks.length,expectedGB:tasks.reduce((s,t)=>s+(t.expectedBytes||0),0)/1073741824,destination:slash(destination)}));
async function worker(){while(cursor<tasks.length){const task=tasks[cursor++];if(task.status==='downloaded'||(task.status==='failed'&&task.error?.includes('404')))continue;task.status='downloading';save();fs.mkdirSync(path.dirname(task.path),{recursive:true});const partial=task.path+'.part';try{
 const args=['--silent','--show-error','--fail','--location','--retry','2','--retry-all-errors','--retry-delay','3','--connect-timeout','20','--max-time','480','--output',partial];
 if(fs.existsSync(partial)&&fs.statSync(partial).size>0)args.push('--continue-at','-');
 args.push(task.url);
 await run('curl.exe',args,{maxBuffer:1024*1024,timeout:510000,windowsHide:true});
 const bytes=fs.statSync(partial).size;
 if(task.expectedBytes&&bytes!==task.expectedBytes)throw new Error(`Size mismatch ${bytes}/${task.expectedBytes}`);
 const hash=await hashes(partial);
 if(task.expectedSha256&&hash.sha256!==task.expectedSha256)throw new Error('SHA256 mismatch');
 if(task.gitBlobSha1&&hash.gitBlobSha1!==task.gitBlobSha1)throw new Error('Git blob mismatch');
 const metadata=await inspect(partial);
 fs.renameSync(partial,task.path);
 Object.assign(task,{status:'downloaded',bytes,sha256:hash.sha256,verifiedGitBlob:task.gitBlobSha1?hash.gitBlobSha1:null,metadata,downloadedAt:new Date().toISOString()});
 fs.writeFileSync(task.path+'.source.json',JSON.stringify(task,null,2));
 console.log(JSON.stringify({id:task.id,status:task.status,MB:Math.round(bytes/1048576),duration:metadata.duration}));
}catch(e){task.status='failed';task.error=(e.stderr||e.message).slice(0,1500);console.log(JSON.stringify({id:task.id,status:task.status,error:task.error.slice(0,180)}))}save()}}
await Promise.all([worker(),worker()]);
console.log(JSON.stringify({phase:'done',...read(manifestPath).summary}));
