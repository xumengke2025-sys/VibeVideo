import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';

const out=path.join(path.dirname(fileURLToPath(import.meta.url)),'upstream-discovery');
fs.mkdirSync(out,{recursive:true});
const catalog=JSON.parse(fs.readFileSync(path.join(out,'../catalog.json'),'utf8'));
const headers={'User-Agent':'VibeVideo-reference-archive','Accept':'application/vnd.github+json'};
const run=promisify(execFile);
const tasks=catalog.packages.map(p=>({id:p.id,url:p.repository.replace('https://github.com/','https://api.github.com/repos/')+`/git/trees/${p.commit}?recursive=1`,type:'tree'}));
for(const [id,url] of [
 ['mg-site','https://vincentwei1021.github.io/mg-styles-15/'],
 ['lemo-site','https://lemomo-ai.github.io/lemo-opuscar/'],
 ['lemo-releases','https://api.github.com/repos/lemomo-ai/lemo-opuscar/releases'],
 ['paper-readme','https://raw.githubusercontent.com/francozanardi/papermotion/main/README.md'],
 ['songbie-readme','https://raw.githubusercontent.com/JohnnyWang8802/songbie/main/README.md'],
 ['reel-readme','https://raw.githubusercontent.com/tuzhechen2005/opus-video-skills/main/README.md'],
 ['beach-readme','https://raw.githubusercontent.com/ishuagrawal/particle-beach/main/README.md'],
 ['lugia-readme','https://raw.githubusercontent.com/Lugia123/ai-video/main/README.md'],
 ['huashu-readme','https://raw.githubusercontent.com/alchaincyf/huashu-art-motion/main/README.md'],
 ['rigid-readme','https://raw.githubusercontent.com/sbobyn/three-avbd/main/README.md'],
 ['clearwater-readme','https://raw.githubusercontent.com/Aureliengmz/clearwater/main/README.md'],
])tasks.push({id,url,type:'document'});
const results=[];
let cursor=0;
async function worker(){while(cursor<tasks.length){const task=tasks[cursor++];try{let response,body;const saved=path.join(out,`${task.id}.${task.type==='tree'||task.id.includes('releases')?'json':'txt'}`);if(fs.existsSync(saved)){body=fs.readFileSync(saved,'utf8');response={status:200,ok:true}}else if(task.url.includes('raw.githubusercontent.com')){const result=await run('curl.exe',['--silent','--show-error','--fail','--location','--max-time','30',task.url],{maxBuffer:8*1024*1024});body=result.stdout;response={status:200,ok:true}}else{response=await fetch(task.url,{headers,signal:AbortSignal.timeout(30000)});body=await response.text()}fs.writeFileSync(saved,body);const record={...task,status:response.status,bytes:Buffer.byteLength(body)};if(response.ok&&task.type==='tree'){const data=JSON.parse(body);record.videos=(data.tree||[]).filter(x=>/\.(mp4|webm|mov|m4v|gif)$/i.test(x.path)).map(x=>({path:x.path,size:x.size,sha:x.sha}));record.documents=(data.tree||[]).filter(x=>/README|site\/.*\.(js|json)$|catalog|manifest|videos.*json/i.test(x.path)).slice(0,25).map(x=>x.path)}else if(response.ok){record.urls=[...new Set(body.match(/https?:\/\/[^\s"'<>`)]+/g)||[])].filter(u=>/mp4|webm|attachments|youtu|releases|github.io/.test(u)).slice(0,50);record.scriptPaths=[...body.matchAll(/<script[^>]+src=["']([^"']+)/g)].map(x=>x[1])}results.push(record);console.log(JSON.stringify(record));}catch(e){const record={...task,error:e.message};results.push(record);console.log(JSON.stringify(record))}}}
await Promise.all([worker(),worker(),worker(),worker()]);
fs.writeFileSync(path.join(out,'discovery.json'),JSON.stringify(results,null,2));
