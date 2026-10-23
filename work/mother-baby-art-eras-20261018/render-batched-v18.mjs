import {spawn} from 'node:child_process';
import {once} from 'node:events';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const root=path.dirname(fileURLToPath(import.meta.url)),out=path.join(root,'out');fs.mkdirSync(out,{recursive:true});
async function render(k){const log=fs.createWriteStream(path.join(out,`segment-${k}-v18.log`)),first=Math.max(0,k*5-1),last=Math.min(19,k*5+5),ids=Array.from({length:last-first+1},(_,n)=>first+n);const p=spawn(process.execPath,['render-v18.mjs','sample'],{cwd:root,env:{...process.env,ONLY_ERAS:ids.join(','),START_SECONDS:String(k*10),FRAMES:'240',OUTPUT_FILENAME:`segment-${k}-v18.mp4`},stdio:['ignore','pipe','pipe'],windowsHide:true});
 p.stdout.on('data',d=>{log.write(d);process.stdout.write(`segment ${k}: `+d)});p.stderr.on('data',d=>{log.write(d);process.stderr.write(d)});const [code]=await once(p,'close');log.end();if(code!==0)throw Error('segment failed '+k+' code '+code);}
// Full-resolution canvas readback stalled when two browser renderers shared the
// GPU on this machine. Render one bounded segment at a time.
const selection=process.argv.find(a=>a.startsWith('--segments=')),ids=selection?selection.slice(11).split(',').map(Number):[0,1,2,3];
if(ids.some(k=>!Number.isInteger(k)||k<0||k>3))throw Error('Invalid segment selection');
for(const k of ids)await render(k);
const missing=[0,1,2,3].filter(k=>!fs.existsSync(path.join(out,`segment-${k}-v18.mp4`)));if(missing.length){console.log(JSON.stringify({rendered_segments:ids,pending_segments:missing,concat:false}));process.exit(0)}
const list=path.join(out,'segments-v18.txt');fs.writeFileSync(list,[0,1,2,3].map(k=>`file 'segment-${k}-v18.mp4'`).join('\n'));
const require=createRequire(import.meta.url),ffmpeg=path.join(path.dirname(require.resolve('@remotion/compositor-win32-x64-msvc/package.json')),'ffmpeg.exe');
const result=path.join(out,'mother-baby-20-eras-portrait-v18-40s.mp4');const ff=spawn(ffmpeg,['-v','error','-y','-f','concat','-safe','0','-i',list,'-c','copy','-movflags','+faststart',result],{stdio:['ignore','ignore','pipe'],windowsHide:true});ff.stderr.on('data',d=>process.stderr.write(d));const [code]=await once(ff,'close');if(code!==0)throw Error('concat failed');console.log(JSON.stringify({output:result,segments:4,frames:960,duration:40}));
