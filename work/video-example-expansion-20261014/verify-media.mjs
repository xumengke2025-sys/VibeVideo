import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {spawnSync} from 'node:child_process';import {fileURLToPath} from 'node:url';
const work=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(work,'../..'),base=path.join(root,'reference-sources/video-examples-20261014');
const manifest=JSON.parse(fs.readFileSync(path.join(base,'manifest.json'),'utf8'));const bin='D:/Codex/skills/video-shotcraft/workbench/node_modules/@remotion/compositor-win32-x64-msvc/';
const run=(exe,args)=>{const r=spawnSync(bin+exe,args,{encoding:'utf8',windowsHide:true,maxBuffer:2*1024*1024,timeout:180000});if(r.status!==0)throw Error(r.stderr||String(r.error));return r.stdout;};
fs.mkdirSync(path.join(work,'posters'),{recursive:true});const items=[];
for(const m of manifest.media){
 const b=fs.readFileSync(m.path),sha=crypto.createHash('sha256').update(b).digest('hex');if(sha!==m.sha256)throw Error('Hash mismatch '+m.id);if(!fs.existsSync(m.entry))throw Error('Missing entry '+m.id);
 const p=JSON.parse(run('ffprobe.exe',['-v','error','-show_streams','-show_format','-of','json',m.path])),v=p.streams.find(s=>s.codec_type==='video');if(!v||Number(p.format.duration)<=0)throw Error('Invalid video '+m.id);
 run('ffmpeg.exe',['-v','error','-xerror','-threads','1','-filter_threads','1','-i',m.path,'-threads','1','-c:v','rawvideo','-c:a','pcm_s16le','-f','null','-']);
 const poster=path.join(work,'posters',sha.slice(0,20)+'.jpg').replaceAll('\\','/');run('ffmpeg.exe',['-v','error','-threads','1','-ss',String(Math.min(1,Number(p.format.duration)/3)),'-i',m.path,'-vf','scale=640:-2','-frames:v','1','-threads','1','-update','1','-y',poster]);
 items.push({id:m.id,repo:m.repo,path:m.path,sha256:sha,bytes:b.length,decodePassed:true,metadata:{width:v.width,height:v.height,duration:Number(p.format.duration),fps:v.r_frame_rate,codec:v.codec_name,audio:p.streams.filter(s=>s.codec_type==='audio').map(s=>({codec:s.codec_name,sampleRate:s.sample_rate,channels:s.channels}))},poster});
 console.log('Decoded '+m.id+' '+v.width+'x'+v.height+' '+p.format.duration+'s');
}
fs.writeFileSync(path.join(work,'media-verification.json'),JSON.stringify({checked:'2026-10-14',scope:'SHA256、元数据及完整音视频解码；未重渲、未完整动态观看或听音',items},null,2)+'\n');
