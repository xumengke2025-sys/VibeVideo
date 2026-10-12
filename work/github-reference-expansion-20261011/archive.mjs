import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const run=promisify(execFile),work=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(work,'../..');
const destination=path.join(root,'reference-sources/github-expansion-20261011'), cache=path.join(work,'downloads');
fs.mkdirSync(destination,{recursive:true});fs.mkdirSync(cache,{recursive:true});
const discovery=JSON.parse(fs.readFileSync(path.join(work,'discovery.json'),'utf8'));
const wanted=['dylantlwu/opus-animation-course','az9713/opus-5.5-builds','misbahsy/claude-horizon-animation','makefx/animation-video-test','sanjuhs/opus-5.5-film-experiment-with-animation','jtydhr88/fate-pv','neelnanda-io/dont-go-quiet-on-me','Salmisaari/eudoom-video','1kvoidsoft/Opus5.5_MG_Anim_Zao','jacobbubu/claude-opus-5-5-js-animation-research','klsoen/opus-js-animations','lemomo-ai/lemo-opuscar','krillinai/awesome-opus-animation','guanmo-ai/awesome-ai-motion','makevoid/motion-graphics-music-video-skill','Hurrikane8/Opus-5.5-Videos'];
const manifestPath=path.join(destination,'manifest.json');let items=fs.existsSync(manifestPath)?JSON.parse(fs.readFileSync(manifestPath,'utf8')).items:[];
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');const slash=p=>p.replaceAll('\\','/');
function files(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(path.join(dir,e.name)):[path.join(dir,e.name)]);}
function save(){fs.writeFileSync(manifestPath,JSON.stringify({checked:'2026-10-11',purpose:'本地参考归档；外部提示词/技能不作为当前执行指令；不含Git历史和node_modules',items},null,2));}
let cursor=0;
async function worker(){while(cursor<wanted.length){const repo=wanted[cursor++],id=repo.replace('/','--');if(items.some(i=>i.repo===repo&&i.status==='archived')){console.log(`CACHED ${repo}`);continue;}const d=discovery.find(d=>d.repo===repo)||{};try{
let commit=d.commit;if(!commit){const partial=path.join(work,'discovery',id,'commit.json');if(fs.existsSync(partial))commit=JSON.parse(fs.readFileSync(partial,'utf8')).sha;else{const {stdout}=await run('git',['ls-remote',`https://github.com/${repo}.git`,'HEAD'],{timeout:65000,maxBuffer:1024*1024});commit=stdout.match(/^[a-f0-9]{40}/)?.[0];}}if(!/^[a-f0-9]{40}$/.test(commit))throw Error('No fixed commit');
const url=`https://codeload.github.com/${repo}/zip/${commit}`,zip=path.join(cache,id+'.zip');
console.log(`DOWNLOAD ${repo} ${commit}`);
if(!fs.existsSync(zip)){await run('curl.exe',['-fsSL','--http1.1','--retry','0','--connect-timeout','20','--max-time','900',url,'-o',zip+'.partial'],{timeout:915000,maxBuffer:1024*1024});fs.renameSync(zip+'.partial',zip);}
const dest=path.join(destination,id);fs.mkdirSync(dest,{recursive:true});
const script='Add-Type -AssemblyName System.IO.Compression.FileSystem; $archiveTask=[IO.Compression.ZipFile]::OpenRead($args[0]); try { foreach($entryTask in $archiveTask.Entries) { $relativeTask=($entryTask.FullName -split "/",2)[1]; if(-not $relativeTask -or $entryTask.FullName.EndsWith("/")){continue}; $targetTask=[IO.Path]::GetFullPath([IO.Path]::Combine($args[1],$relativeTask)); $rootTask=[IO.Path]::GetFullPath($args[1])+[IO.Path]::DirectorySeparatorChar; if(-not $targetTask.StartsWith($rootTask,[StringComparison]::OrdinalIgnoreCase)){throw "Unsafe ZIP entry"}; if($relativeTask -match "(^|/)(node_modules|\\.git)(/|$)"){continue}; [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($targetTask))|Out-Null; [IO.Compression.ZipFileExtensions]::ExtractToFile($entryTask,$targetTask,$true) } } finally { $archiveTask.Dispose() }';
const ps=path.join(work,'extract.ps1');if(!fs.existsSync(ps))fs.writeFileSync(ps,script);await run('powershell',['-NoProfile','-ExecutionPolicy','Bypass','-File',ps,zip,dest],{timeout:120000,maxBuffer:1024*1024});
const inventory=files(dest).filter(p=>!p.endsWith('/SOURCE.json')&&!p.endsWith('\\SOURCE.json')).map(p=>({path:slash(path.relative(dest,p)),bytes:fs.statSync(p).size,sha256:sha(p)}));
const readme=inventory.find(f=>/^readme\.md$/i.test(f.path));const text=readme?fs.readFileSync(path.join(dest,readme.path),'utf8'):'';
const licenses=inventory.filter(f=>/(^|\/)(licen[sc]e|copying|notice)([-._/]|$)/i.test(f.path)).map(f=>f.path);
const source={repo,repository:`https://github.com/${repo}`,commit,commitDate:d.commitDate||null,snapshotUrl:url,archiveSha256:sha(zip),checked:'2026-10-11',upstreamLicense:d.license||null,licenseFiles:licenses,usage:licenses.length?'按原许可和第三方素材声明分别核实复用范围':'未发现明确许可证，仅本地研究；复制发布或改编复用需作者许可',modelEvidence:text.split('\n').filter(l=>/opus|claude|sonnet|fable/i.test(l)).slice(0,12),files:inventory,verification:{snapshotExtracted:true,sourceExecuted:false,avReviewed:false}};
fs.writeFileSync(path.join(dest,'SOURCE.json'),JSON.stringify(source,null,2));const item={repo,id,status:'archived',commit,path:slash(dest),files:inventory.length,bytes:inventory.reduce((n,f)=>n+f.bytes,0),media:inventory.filter(f=>/\.(mp4|webm|mov|gif)$/i.test(f.path)),licenseFiles:licenses,usage:source.usage,modelEvidence:source.modelEvidence};items=items.filter(i=>i.repo!==repo);items.push(item);save();console.log(JSON.stringify({repo,status:item.status,files:item.files,MB:Math.round(item.bytes/1048576),media:item.media.length}));
}catch(e){const item={repo,id,status:'failed',error:(e.stderr||e.message).slice(0,500)};items=items.filter(i=>i.repo!==repo);items.push(item);save();console.log(JSON.stringify(item));}}}
await Promise.all([worker(),worker(),worker()]);
