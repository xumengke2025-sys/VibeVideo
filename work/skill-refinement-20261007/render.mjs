import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {bundle} from '@remotion/bundler';
import {renderMedia,renderStill,selectComposition} from '@remotion/renderer';
const root=path.dirname(fileURLToPath(import.meta.url));
const serveUrl=await bundle({entryPoint:path.join(root,'index.jsx'),publicDir:path.join(root,'public')});
const composition=await selectComposition({serveUrl,id:'OpticalStudy'});
const args=process.argv.slice(2);
if(args[0]==='stills'){
  for(const frame of [0,48,110,145,179,181,220,299]){
    await renderStill({serveUrl,composition,frame,output:path.join(root,'out',`frame-${frame}.png`),imageFormat:'png'});
    console.log(`Still ${frame}`);
  }
}else{
  let progress=-1;
  await renderMedia({serveUrl,composition,outputLocation:path.join(root,'out','optical-study.mp4'),codec:'h264',crf:17,x264Preset:'veryfast',concurrency:1,
    ffmpegOverride:({args})=>{const a=[...args];a.splice(a.length-1,0,'-threads:v','1','-x264-params','threads=1:lookahead_threads=1');return a},
    onProgress:({progress:p})=>{const q=Math.floor(p*100);if(q%20===0&&q!==progress){console.log(`Render ${q}%`);progress=q}}});
  console.log(path.join(root,'out','optical-study.mp4'));
}
