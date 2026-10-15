#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const skill=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),args=process.argv.slice(2);
const option=(name,fallback)=>{const i=args.indexOf('--'+name);if(i<0)return fallback;if(!args[i+1]||args[i+1].startsWith('--'))throw Error('Missing --'+name+' value');return args[i+1];};
const index=JSON.parse(fs.readFileSync(path.join(skill,'references/video-examples.json'),'utf8'));
const project=path.resolve(skill,'../..');
const root=path.resolve(option('root',process.env.VIBE_VIDEO_REFERENCE_ROOT||(fs.existsSync(path.join(project,'tools/reference-restore-manifest.json'))?project:index.projectRoot)));
const original=index.projectRoot.replaceAll('\\','/').replace(/\/$/,'');
const relocate=p=>{if(!p)return p;const normalized=p.replaceAll('\\','/');return normalized.startsWith(original+'/')?path.resolve(root,normalized.slice(original.length+1)).replaceAll('\\','/'):p;};
const items=index.items.map(m=>({...m,path:relocate(m.path),entry:relocate(m.entry),researchEntry:relocate(m.researchEntry),card:relocate(m.card),guide:relocate(m.guide),sourceRecord:relocate(m.sourceRecord),poster:relocate(m.poster)}));
const hasSource=m=>Boolean(m.entry&&['影片与源码','镜头样段与源码'].includes(m.kind));
const out=v=>console.log(JSON.stringify(v,null,2)),command=args[0]||'search';
if(command==='search'){
 const query=option('query','').toLowerCase(),words=query.split(/\s+/).filter(Boolean),group=option('group',''),kind=option('kind',''),source=option('source',''),limit=Number(option('limit','6'));if(!Number.isInteger(limit)||limit<1||limit>50)throw Error('limit must be 1..50');if(!['','present','missing'].includes(source))throw Error('source must be present or missing');
 const contains=(value,word)=>String(value||'').toLowerCase().includes(word);
 const result=items.map(m=>({m,score:words.reduce((n,w)=>n+(contains(m.title,w)?6:0)+(contains(m.group,w)?4:0)+(contains(m.tags,w)?1:0)+(contains(m.description,w)?1:0)+(contains(m.author,w)?2:0)+(contains(m.id,w)?1:0),0)})).filter(x=>(!words.length||x.score>0)&&(!group||x.m.group===group)&&(!kind||x.m.kind===kind)&&(!source||hasSource(x.m)===(source==='present'))).sort((a,b)=>b.score-a.score||a.m.id.localeCompare(b.m.id)).slice(0,limit).map(x=>x.m);
 out({checked:index.checked,gallery:path.resolve(root,index.galleryPath).replaceAll('\\','/'),scope:index.scope,results:result});
}else if(command==='card'){
 const found=items.filter(m=>m.id===args[1]||m.id.split('/').at(-1)===args[1]);if(found.length!==1)throw Error('Use one exact example id');out(found[0]);
}else if(command==='verify'){
 const missing=[];for(const m of items){const keys=['path','sourceRecord'];if(['影片与源码','镜头样段与源码'].includes(m.kind))keys.push('entry');for(const key of keys)if(!m[key]||!fs.existsSync(m[key]))missing.push({id:m.id,key,path:m[key]});for(const key of ['entry','researchEntry','card'])if(m[key]&&!keys.includes(key)&&!fs.existsSync(m[key]))missing.push({id:m.id,key,path:m[key]});}out({items:items.length,sourceCount:items.filter(hasSource).length,missing,optionalPostersMissing:items.filter(m=>m.poster&&!fs.existsSync(m.poster)).length});if(missing.length)process.exitCode=1;
}else throw Error('Unknown command '+command);
