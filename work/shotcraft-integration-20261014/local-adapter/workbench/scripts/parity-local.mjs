#!/usr/bin/env node
// Windows/local adapter: Node + locked Remotion + pngjs, no rsync/Python.
import {bundle} from '@remotion/bundler';
import {openBrowser, renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {PNG} from 'pngjs';
import {syncRenderPublic} from './local-platform.mjs';

const wb = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const opt = (k,d) => {const i=args.indexOf(`--${k}`); return i<0?d:args[i+1];};
const out = path.resolve(opt('out', path.join(wb,'.parity-local')));
const frames = opt('frames','0,30,60').split(',').map(Number);
const tolerance = Number(opt('tolerance','0'));
const maxRatio = Number(opt('max-ratio','0'));
const browserExecutable = opt('browser', process.env.SHOTCRAFT_BROWSER_EXECUTABLE);
const report = {status:'inconclusive',frames:[],tolerance,maxRatio,browserExecutable};
fs.mkdirSync(out,{recursive:true});
let browserInstance;
try {
  if (!frames.length || frames.some(f=>!Number.isInteger(f)||f<0) || !Number.isFinite(tolerance) || tolerance<0 || tolerance>255 || !Number.isFinite(maxRatio) || maxRatio<0 || maxRatio>1) throw Error('Invalid comparison options');
  if (!fs.existsSync(path.join(wb,'proj/workbench.ts'))) throw Error('Link a project with workbench.ts first');
  const serveUrl = await bundle({entryPoint:path.join(wb,'src/remotion/index.ts'),publicDir:syncRenderPublic(wb),webpackOverride:c=>({...c,resolve:{...c.resolve,symlinks:false,alias:{...c.resolve?.alias,'@proj':path.join(wb,'proj'),'@demos':path.join(wb,'demosrc')}}})});
  browserInstance = await openBrowser('chrome',{browserExecutable,chromiumOptions:{gl:'angle'}});
  const base = {serveUrl,browserExecutable,puppeteerInstance:browserInstance,chromiumOptions:{gl:'angle'}};
  const imported = await selectComposition({...base,id:'ProjImported',inputProps:{}});
  const original = await selectComposition({...base,id:'ProjOriginal',inputProps:{}});
  if (imported.width!==original.width || imported.height!==original.height || imported.durationInFrames!==original.durationInFrames || imported.fps!==original.fps) throw Error('Composition metadata differs');
  report.metadata = {width:original.width,height:original.height,fps:original.fps,total:original.durationInFrames};
  const decode = file => {
    const decoded=PNG.sync.read(fs.readFileSync(file));
    if(decoded.width!==original.width || decoded.height!==original.height) throw Error('PNG size mismatch');
    return decoded.data;
  };
  for (const frame of frames) {
    if(frame>=original.durationInFrames) throw Error(`Frame ${frame} outside composition`);
    const files=[];
    for (const composition of [original,imported]) {
      const output=path.join(out,`${composition.id}-f${frame}.png`);
      await renderStill({...base,composition,output,frame,imageFormat:'png'});
      files.push(output);
    }
    const a=decode(files[0]),b=decode(files[1]);
    let bad=0,max=0;
    for(let i=0;i<a.length;i+=4){let d=0;for(let c=0;c<4;c++)d=Math.max(d,Math.abs(a[i+c]-b[i+c]));max=Math.max(max,d);if(d>tolerance)bad++;}
    const pixels=a.length/4;
    const row={frame,badPixels:bad,pixels,ratio:bad/pixels,maxChannelDifference:max,passed:bad/pixels<=maxRatio,files};
    report.frames.push(row);
    console.log(`f${frame}: ${row.passed?'same':'different'}, ${bad}/${pixels} pixels, max ${max}`);
  }
  report.status=report.frames.every(f=>f.passed)?'passed':'different';
  process.exitCode=report.status==='passed'?0:1;
}catch(error){report.error=String(error);process.exitCode=2;console.error(report.error);}
finally{if(browserInstance) await browserInstance.close({silent:true});}
fs.writeFileSync(path.join(out,'comparison.json'),JSON.stringify(report,null,2)+'\n');
