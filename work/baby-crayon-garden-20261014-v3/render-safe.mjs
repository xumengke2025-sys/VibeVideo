import fs from 'node:fs';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const ffmpeg='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe';
const run=(cmd,args)=>new Promise((resolve,reject)=>{
 const child=spawn(cmd,args,{cwd:here,windowsHide:true,stdio:'inherit'});
 child.on('error',reject);child.on('exit',code=>code===0?resolve():reject(Error(`${cmd} exited ${code}`)));
});
fs.mkdirSync(path.join(here,'out'),{recursive:true});
const names=[];
for(let i=0;i<4;i++){
 const name=`part-${i}.mp4`;names.push(name);
 await run(process.execPath,['render.mjs',`--range=${i*10}:${(i+1)*10}`,`--name=${name}`]);
}
fs.writeFileSync(path.join(here,'out/concat.txt'),names.map(n=>`file '${n}'`).join('\n')+'\n');
await run(ffmpeg,['-y','-hide_banner','-loglevel','warning','-f','concat','-safe','0','-i','out/concat.txt','-i','score.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t','40','-movflags','+faststart','out/宝宝和太阳的晚安-v3.mp4']);
console.log('Merged four contiguous 240-frame segments with the original continuous score.');
