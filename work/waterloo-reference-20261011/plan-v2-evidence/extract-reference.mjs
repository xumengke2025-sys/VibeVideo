import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
const root='D:/ai项目/ai动画/VibeVideo项目';
const dir=path.join(root,'work/waterloo-reference-20261011/plan-v2-evidence');
const source=path.join(root,'reference-sources/upstream-videos/lemo-opuscar/impasto.mp4');
const bin='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc';
fs.mkdirSync(dir,{recursive:true});
function run(exe,args){const r=spawnSync(path.join(bin,exe),args,{encoding:'utf8',timeout:60000,windowsHide:true});if(r.status!==0)throw Error(r.stderr||String(r.error));return r.stdout;}
const meta=JSON.parse(run('ffprobe.exe',['-v','error','-show_entries','format=duration:stream=codec_type,codec_name,width,height,r_frame_rate','-of','json',source]));
const times=[0,5,10,15,20,25,30,39];
for(const t of times){const out=path.join(dir,`impasto-${t}.png`);if(!fs.existsSync(out))run('ffmpeg.exe',['-hide_banner','-loglevel','error','-y','-ss',String(t),'-i',source,'-frames:v','1','-vf','scale=640:-1',out]);}
for(let i=0;i<12;i++)run('ffmpeg.exe',['-hide_banner','-loglevel','error','-y','-ss',String(10+i/6),'-i',source,'-frames:v','1','-vf','scale=640:-1',path.join(dir,`motion-${String(i+1).padStart(2,'0')}.png`)]);
fs.writeFileSync(path.join(dir,'reference-metadata.json'),JSON.stringify({source,sha256:crypto.createHash('sha256').update(fs.readFileSync(source)).digest('hex'),metadata:meta,overviewTimes:times,motionWindow:{start:10,end:12,fps:6,width:640},viewed:false,audioListened:false},null,2));
console.log(JSON.stringify({source,metadata:meta,overviewImages:times.length,motionImages:fs.readdirSync(dir).filter(x=>x.startsWith('motion-')).length}));
