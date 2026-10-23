import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {createRequire} from 'node:module';
const root=path.dirname(fileURLToPath(import.meta.url));
const require=createRequire('D:/ai项目/ai动画/package.json');
const {openBrowser}=require('@remotion/renderer');
const ffmpeg='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe';
const mode=process.argv[2]||'stills';
const out=path.join(root,'out');fs.mkdirSync(out,{recursive:true});
const browser=await openBrowser('chrome',{logLevel:'error'});
try{
 const page=await browser.newPage({context:()=>null,logLevel:'error',indent:false,pageIndex:0,onBrowserLog:null,onLog:()=>{}});
 await page.setViewport({width:1080,height:1920,deviceScaleFactor:1});
 await page.goto({url:pathToFileURL(path.join(root,'film/index.html')).href,timeout:60000});
 const ready=await page.evaluate(()=>({ready:window.__ready,config:window.__config}));
 if(!ready.ready)throw Error('Film did not initialize');
 if(mode==='stills'){
  const samples=await page.evaluate(()=>window.ERAS.map(e=>(e.t0+e.t1)/2));
  const qa=path.join(out,'style-stills');fs.mkdirSync(qa,{recursive:true});
  for(let i=0;i<samples.length;i++){let t=samples[i];const data=await page.evaluate(t=>{window.renderAt(t);return document.getElementById('film').toDataURL('image/png').split(',')[1]},t);fs.writeFileSync(path.join(qa,`${String(i).padStart(2,'0')}-${t.toFixed(2)}.png`),Buffer.from(data,'base64'))}
  console.log(JSON.stringify({stills:samples.length,path:qa}));
 }else if(mode==='check'){
  const evidence=await page.evaluate(()=>{const issues=[];let maxMom=0,maxBaby=0;const near=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);const states=[];for(let f=0;f<990;f++){const t=f/24,s=window.renderAt(t,{noTransition:true});if(s.a.held){maxMom=Math.max(maxMom,near(s.mom.wrist,s.mom.grip));maxBaby=Math.max(maxBaby,near(s.kid.wrist,s.kid.grip));}for(const p of[s.mom.wrist,s.mom.cup.mouth,s.kid.wrist,s.kid.toy])if(!p.every(Number.isFinite)||p[0]<0||p[0]>1080||p[1]<0||p[1]>1920)issues.push({f,p});if(f%100===0)states.push({f,era:s.era,phase:s.a.ph});}const a=JSON.stringify(window.renderAt(2.3));window.renderAt(38.1);const b=JSON.stringify(window.renderAt(2.3));return{frames:990,issues,max_held_mother_error:maxMom,max_held_baby_error:maxBaby,random_access_state_equal:a===b,states};});
  fs.writeFileSync(path.join(out,'mechanical-check.json'),JSON.stringify(evidence,null,2));console.log(JSON.stringify(evidence));
 }else{
  const sample=mode==='sample',start=sample?8.7:0,frames=sample?154:990;
  const file=path.join(out,sample?'action-sample-6.4s.mp4':'mother-baby-35-eras-portrait-v1.mp4');
  const ff=spawn(ffmpeg,['-v','error','-y','-f','image2pipe','-vcodec','mjpeg','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-threads','2',file],{stdio:['pipe','ignore','pipe'],windowsHide:true});let error='';ff.stderr.on('data',d=>error+=d.toString());const closed=once(ff,'close');
  for(let f=0;f<frames;f++){
   const data=await page.evaluate(t=>{window.renderAt(t);return document.getElementById('film').toDataURL('image/jpeg',.97).split(',')[1]},start+f/24);
   if(!ff.stdin.write(Buffer.from(data,'base64')))await once(ff.stdin,'drain');
   if(f%120===0)console.log(JSON.stringify({rendered:f,total:frames}));
  }
  ff.stdin.end();const [code]=await closed;if(code!==0)throw Error(error||`encoder exit ${code}`);
  console.log(JSON.stringify({output:file,frames,duration:frames/24,width:1080,height:1920,audio:false}));
 }
}finally{await browser.close({silent:true})}
