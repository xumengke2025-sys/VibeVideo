import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const run=promisify(execFile), work=path.dirname(fileURLToPath(import.meta.url));
const repos=['jacobbubu/claude-opus-5-5-js-animation-research','dylantlwu/opus-animation-course','az9713/opus-5.5-builds','1kvoidsoft/Opus5.5_MG_Anim_Zao','misbahsy/claude-horizon-animation','makefx/animation-video-test','sanjuhs/opus-5.5-film-experiment-with-animation','neelnanda-io/dont-go-quiet-on-me','Salmisaari/eudoom-video','jtydhr88/fate-pv','meaterick/opusvideo','arimanyus/hophopnopenope','Kianzzz/xilo-opus-video','dshukertjr/opus-animation','Hurrikane8/Opus-5.5-Videos','guanmo-ai/awesome-ai-motion','lemomo-ai/lemo-opuscar','makevoid/motion-graphics-music-video-skill','klsoen/opus-js-animations','krillinai/awesome-opus-animation','athemeroy/awesome-claude-5-5-videos','apimodels/claude-opus-5-5-video-prompts'];
const out=path.join(work,'discovery');fs.mkdirSync(out,{recursive:true});
async function get(url){const {stdout}=await run('curl.exe',['-fsSL','--connect-timeout','15','--max-time','50','-H','Accept: application/vnd.github+json',url],{maxBuffer:20*1024*1024,timeout:55000});return stdout;}
const records=[];let cursor=0;
async function worker(){while(cursor<repos.length){const repo=repos[cursor++],id=repo.replace('/','--'),base=path.join(out,id);fs.mkdirSync(base,{recursive:true});try{
const meta=JSON.parse(await get(`https://api.github.com/repos/${repo}`));fs.writeFileSync(path.join(base,'repository.json'),JSON.stringify(meta,null,2));
const commit=JSON.parse(await get(`https://api.github.com/repos/${repo}/commits/${meta.default_branch}`));fs.writeFileSync(path.join(base,'commit.json'),JSON.stringify(commit,null,2));
const tree=JSON.parse(await get(`https://api.github.com/repos/${repo}/git/trees/${commit.sha}?recursive=1`));fs.writeFileSync(path.join(base,'tree.json'),JSON.stringify(tree,null,2));
const readmeFile=tree.tree.find(f=>/^readme\.md$/i.test(f.path));let readme='';if(readmeFile){readme=await get(`https://raw.githubusercontent.com/${repo}/${commit.sha}/${readmeFile.path}`);fs.writeFileSync(path.join(base,'README.md'),readme);}
let releases=[];try{releases=JSON.parse(await get(`https://api.github.com/repos/${repo}/releases?per_page=10`));fs.writeFileSync(path.join(base,'releases.json'),JSON.stringify(releases,null,2));}catch(e){}
const record={repo,commit:commit.sha,commitDate:commit.commit.committer.date,description:meta.description,license:meta.license?.spdx_id||null,fork:meta.fork,parent:meta.parent?.full_name,size:meta.size,truncated:tree.truncated,files:tree.tree.filter(f=>f.type==='blob').length,media:tree.tree.filter(f=>/\.(mp4|webm|mov|gif)$/i.test(f.path)).map(f=>({path:f.path,size:f.size,sha:f.sha})),releaseMedia:releases.flatMap(r=>r.assets.filter(a=>/\.(mp4|webm|mov|gif)$/i.test(a.name)).map(a=>({name:a.name,url:a.browser_download_url,size:a.size,digest:a.digest,release:r.tag_name}))),urls:[...new Set(readme.match(/https?:\/\/[^\s"'<>`)]+/g)||[])].filter(u=>/attachments|mp4|webm|youtu|github\.com/.test(u)),modelEvidence:readme.split('\n').filter(l=>/opus|claude|sonnet|fable/i.test(l)).slice(0,12),entries:tree.tree.filter(f=>f.type==='blob'&&/\.(html|[cm]?js|tsx?|py)$/i.test(f.path)&&!/(node_modules|package-lock|vendor)/.test(f.path)).slice(0,16).map(f=>f.path)};
records.push(record);fs.writeFileSync(path.join(base,'summary.json'),JSON.stringify(record,null,2));console.log(JSON.stringify({repo,license:record.license,files:record.files,media:record.media.length,releaseMedia:record.releaseMedia.length,entries:record.entries.slice(0,6),model:record.modelEvidence.slice(0,3)}));
}catch(e){records.push({repo,error:(e.stderr||e.message).slice(0,240)});console.log(JSON.stringify(records.at(-1)));}fs.writeFileSync(path.join(work,'discovery.json'),JSON.stringify(records,null,2));}}
await Promise.all([worker(),worker(),worker()]);
