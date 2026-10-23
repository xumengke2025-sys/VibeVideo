import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {selectComposition, renderStill} from '@remotion/renderer';

const frames=(process.argv.slice(2).length?process.argv.slice(2):['120','220','300','420','600','760','960','1080','1210','1320']).map(Number);
const serveUrl=await bundle({entryPoint:path.resolve('src/index.jsx'),outDir:path.resolve('out','bundle')});
const composition=await selectComposition({serveUrl,id:'LifeBranches'});
for(const frame of frames){
  const output=path.resolve('out',`still-${String(frame).padStart(4,'0')}-v2.png`);
  await renderStill({composition,serveUrl,output,frame,imageFormat:'png'});
  console.log(frame,output);
}
