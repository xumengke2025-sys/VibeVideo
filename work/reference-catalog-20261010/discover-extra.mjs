import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';

const run=promisify(execFile);
const work=path.dirname(fileURLToPath(import.meta.url));
const out=path.join(work,'upstream-discovery');
const catalog=JSON.parse(fs.readFileSync(path.join(work,'catalog.json'),'utf8'));
const tasks=[
 ['reel-detail','https://raw.githubusercontent.com/tuzhechen2005/opus-video-skills/main/skills/kinetic-reel/README.md'],
 ['painted-detail','https://raw.githubusercontent.com/tuzhechen2005/opus-video-skills/main/skills/painted-animation/README.md'],
 ['lyric-current','https://raw.githubusercontent.com/20q2/i-like-ur-look-lyric-video/main/README.md'],
 ['paper-catalog','https://raw.githubusercontent.com/francozanardi/papermotion/main/examples/catalog.ts'],
 ...['francozanardi/papermotion','tuzhechen2005/opus-video-skills','20q2/i-like-ur-look-lyric-video','Aureliengmz/clearwater','sbobyn/three-avbd','Lugia123/ai-video','alchaincyf/huashu-art-motion','mexicat/pdoom-video'].map(repo=>[repo.split('/')[1]+'-releases',`https://api.github.com/repos/${repo}/releases`]),
 ['lugia-tree','https://api.github.com/repos/Lugia123/ai-video/git/trees/main?recursive=1'],
];
const records=[];
let cursor=0;
async function worker(){while(cursor<tasks.length){const [id,url]=tasks[cursor++];try{const {stdout}=await run('curl.exe',['--silent','--show-error','--fail','--location','--connect-timeout','15','--max-time','35',url],{maxBuffer:10*1024*1024,timeout:40000});fs.writeFileSync(path.join(out,`${id}.txt`),stdout);let summary={id,status:'ok'};if(id.endsWith('-releases')){const r=JSON.parse(stdout);summary.assets=r.flatMap(release=>release.assets).filter(asset=>/\.(mp4|webm|gif|mov)$/i.test(asset.name)).map(asset=>({name:asset.name,url:asset.browser_download_url,size:asset.size,digest:asset.digest}));}else if(id.endsWith('-tree'))summary.media=JSON.parse(stdout).tree?.filter(file=>/\.(mp4|webm|gif|mov)$/i.test(file.path)).map(file=>({path:file.path,size:file.size,sha:file.sha}));else summary.mediaUrls=[...new Set(stdout.match(/https?:\/\/[^\s"'<>`)]+/g)||[])].filter(u=>/attachments|mp4|webm|youtu/.test(u));records.push(summary);console.log(JSON.stringify(summary));}catch(e){records.push({id,error:(e.stderr||e.message).slice(0,400)});console.log(JSON.stringify(records.at(-1)))}}}
await Promise.all([worker(),worker(),worker()]);
fs.writeFileSync(path.join(out,'extra-discovery.json'),JSON.stringify(records,null,2));
const extras=[];
for(const record of records.filter(r=>r.assets?.length))for(const asset of record.assets){const packageId=record.id.replace(/-releases$/,'');const packageInfo=catalog.packages.find(p=>p.id===packageId||p.repository.endsWith('/'+packageId));const repository=packageInfo?.repository||`https://github.com/${packageId==='huashu-art-motion'?'alchaincyf':packageId==='ai-video'?'Lugia123':'mexicat'}/${packageId}`;extras.push({id:`${packageId}/${asset.name}`,packageId:packageInfo?.id||packageId,styleId:path.basename(asset.name,path.extname(asset.name)),filename:asset.name,title:`${packageId} / ${asset.name}`,url:asset.url,expectedBytes:asset.size,expectedSha256:asset.digest?.replace('sha256:',''),repository,entry:packageInfo?.entry||null,representation:'author-release',note:'作者额外发布的媒体附件；保持上游文件原样'})}
fs.writeFileSync(path.join(out,'extra-media.json'),JSON.stringify(extras,null,2));
