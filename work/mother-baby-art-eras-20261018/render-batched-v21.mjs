import {spawn} from 'node:child_process';
import {once} from 'node:events';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const root=path.dirname(fileURLToPath(import.meta.url)),out=path.join(root,'out');fs.mkdirSync(out,{recursive:true});
async function renderPart(k,j){const start=k*10+j*5,file=`segment-${k}-part-${j}-v21.mp4`,log=fs.createWriteStream(path.join(out,`segment-${k}-part-${j}-v21.log`)),first=Math.max(0,Math.floor((start-1/3)/2)),last=Math.min(19,Math.floor((start+5+1/3)/2)),ids=Array.from({length:last-first+1},(_,n)=>first+n);const p=spawn(process.execPath,['render-v21.mjs','sample'],{cwd:root,env:{...process.env,ONLY_ERAS:ids.join(','),START_SECONDS:String(start),FRAMES:'120',OUTPUT_FILENAME:file,VIDEO_THREADS:'1'},stdio:['ignore','pipe','pipe'],windowsHide:true});
 p.stdout.on('data',d=>{log.write(d);process.stdout.write(`segment ${k}.${j}: `+d)});p.stderr.on('data',d=>{log.write(d);process.stderr.write(d)});const [code]=await once(p,'close');log.end();if(code!==0)throw Error('segment failed '+k+'.'+j+' code '+code);return file;}
const require=createRequire(import.meta.url),ffmpeg=path.join(path.dirname(require.resolve('@remotion/compositor-win32-x64-msvc/package.json')),'ffmpeg.exe');
async function concat(files,name){const list=path.join(out,name+'.txt');fs.writeFileSync(list,files.map(f=>`file '${f}'`).join('\n'));const ff=spawn(ffmpeg,['-v','error','-y','-f','concat','-safe','0','-i',list,'-c','copy','-movflags','+faststart',path.join(out,name)],{stdio:['ignore','ignore','pipe'],windowsHide:true});ff.stderr.on('data',d=>process.stderr.write(d));const[code]=await once(ff,'close');if(code!==0)throw Error('concat failed '+name);}
async function render(k){const files=[];for(let j=0;j<2;j++)files.push(await renderPart(k,j));await concat(files,`segment-${k}-v21.mp4`);}
// Full-resolution canvas readback stalled when two browser renderers shared the
// GPU on this machine. Render one bounded segment at a time.
const selection=process.argv.find(a=>a.startsWith('--segments=')),ids=selection?selection.slice(11).split(',').map(Number):[0,1,2,3];
if(ids.some(k=>!Number.isInteger(k)||k<0||k>3))throw Error('Invalid segment selection');
for(const k of ids)await render(k);
const missing=[0,1,2,3].filter(k=>!fs.existsSync(path.join(out,`segment-${k}-v21.mp4`)));if(missing.length){console.log(JSON.stringify({rendered_segments:ids,pending_segments:missing,concat:false}));process.exit(0)}
const name='mother-baby-20-eras-portrait-v21-40s.mp4';await concat([0,1,2,3].map(k=>`segment-${k}-v21.mp4`),name);console.log(JSON.stringify({output:path.join(out,name),segments:4,frames:960,duration:40}));
// Keep the silent master; copy its picture packets into the scored deliverable.
const music=path.join(root,'assets/audio-v21/warm-family-40s.wav'),scored=path.join(out,'mother-baby-20-eras-portrait-v21-40s-music.mp4');
if(!fs.existsSync(music))throw Error('Missing baked original score: '+music);
const mux=spawn(ffmpeg,['-v','error','-y','-i',path.join(out,name),'-i',music,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t','40','-movflags','+faststart',scored],{stdio:['ignore','ignore','pipe'],windowsHide:true});mux.stderr.on('data',d=>process.stderr.write(d));const[muxCode]=await once(mux,'close');if(muxCode!==0)throw Error('Music mux failed');console.log(JSON.stringify({output:scored,audio:true,duration:40}));
