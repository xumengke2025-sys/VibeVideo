import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import http from 'node:http';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
const root=path.dirname(fileURLToPath(import.meta.url));
const require=createRequire(path.join(root,'package.json'));
const {openBrowser}=require('@remotion/renderer');
const ffmpeg=path.join(path.dirname(require.resolve('@remotion/compositor-win32-x64-msvc/package.json')),'ffmpeg.exe');
const mode=process.argv[2]||'stills';
const out=path.join(root,'out');fs.mkdirSync(out,{recursive:true});
const server=http.createServer((req,res)=>{try{const rel=decodeURIComponent(new URL(req.url,'http://localhost').pathname);const file=path.resolve(root,'.'+rel);if(!file.startsWith(root+path.sep))throw Error('path');const types={'.js':'text/javascript','.html':'text/html','.png':'image/png','.json':'application/json'};res.setHeader('Content-Type',types[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));}catch{res.statusCode=404;res.end();}});server.listen(0,'127.0.0.1');await once(server,'listening');
const browser=await openBrowser('chrome',{logLevel:'error',browserExecutable:process.env.CHROME_EXECUTABLE||null});
try{
 const page=await browser.newPage({context:()=>null,logLevel:'error',indent:false,pageIndex:0,onBrowserLog:null,onLog:()=>{}});
 await page.setViewport({width:1080,height:1920,deviceScaleFactor:1});
 await page.goto({url:`http://127.0.0.1:${server.address().port}/film/index-v20.html${process.env.ONLY_ERAS?"?only="+process.env.ONLY_ERAS:""}`,timeout:60000});
 await page.evaluate(()=>window.__loadPromise);
 const ready=await page.evaluate(()=>({ready:window.__ready,config:window.__config}));
 if(!ready.ready)throw Error('Film did not initialize');
 if(mode==='environmentcheck'){
  const result=await page.evaluate(()=>{const rows=[];let outside=0;for(let i=0;i<20;i++){const e=window.__environmentQA(i,i*2+.5),im=e.source,m=ENV_LIFE_V20.prepare(im,i),mask=m.getContext('2d').getImageData(0,0,1080,1920).data,make=()=>Object.assign(document.createElement('canvas'),{width:1080,height:1920}),a=make(),b=make(),c=make(),t=i*2+.5;STOP_ENV_V15.draw(a.getContext('2d'),im,t,i,40);ENV_LIFE_V20.draw(b.getContext('2d'),im,t,i,40);ENV_LIFE_V20.draw(c.getContext('2d'),im,t+.8,i,40);const aa=a.getContext('2d').getImageData(0,0,1080,1920).data,bb=b.getContext('2d').getImageData(0,0,1080,1920).data,cc=c.getContext('2d').getImageData(0,0,1080,1920).data;let moved=0,unallowed=0;for(let k=0;k<aa.length;k+=4){const delta=Math.max(...[0,1,2].map(n=>Math.abs(aa[k+n]-bb[k+n]))),motion=Math.max(...[0,1,2].map(n=>Math.abs(cc[k+n]-bb[k+n])));if(!mask[k]&&delta>3)unallowed++;if(mask[k]&&motion>3)moved++}rows.push({era:i,registered_regions:ENV_LIFE_V20.regions[i].length,changed_detail_pixels:moved,outside_mask_pixels:unallowed});outside+=unallowed;a.width=b.width=c.width=1;}return{rows,outside_mask_pixels:outside,scope:'Local indoor-motion sampling compared with identical outdoor frame; changes >3 RGB code values outside registered displacement field. Does not rate appearance.'};});
  fs.mkdirSync(path.join(root,'qa/v20'),{recursive:true});fs.writeFileSync(path.join(root,'qa/v20/environment-check.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));if(result.outside_mask_pixels>100)process.exitCode=1;
 }else if(mode==='transitioncheck'){
  const result=await page.evaluate(async()=>{
   const issues=[],endpoints=[],middle=[];
   async function fingerprint(t,opt={}){window.renderAt(t,{...opt,backgroundOnly:true});const c=document.getElementById('film'),pixels=c.getContext('2d').getImageData(0,0,c.width,c.height).data;return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',pixels))).map(n=>n.toString(16).padStart(2,'0')).join('');}
   for(let k=1;k<20;k++){
    const start=k*2-1/3,end=k*2+1/3;
    const a=await fingerprint(start),a0=await fingerprint(start,{era:k-1,noTransition:true});
    const b=await fingerprint(end),b0=await fingerprint(end,{era:k,noTransition:true});
    if(a!==a0||b!==b0)issues.push({cut:k*2,reason:'Transition endpoint pixel mismatch'});
    endpoints.push({cut:k*2,start_matches:a===a0,end_matches:b===b0,family:SCENE_TRANSITIONS_V16.family(k)});
    middle.push(await fingerprint(k*2+.0416666667));
   }
   // Evict and regenerate the small mask cache, seeking in reverse order.
   for(let k=19;k>=1;k--)if(await fingerprint(k*2+.0416666667)!==middle[k-1])issues.push({cut:k*2,reason:'Transition changes under out-of-order seek'});
   return {cuts:19,endpoints,issues,transition_seek_determinism:issues.length===0,scope:'Room-only transition pixel endpoint and random-access checks; actor continuity checked separately; does not rate aesthetics.'};
  });
  const dest=path.join(root,'qa/v20');fs.mkdirSync(dest,{recursive:true});fs.writeFileSync(path.join(dest,'transition-check.json'),JSON.stringify(result,null,2));
  console.log(JSON.stringify({cuts:result.cuts,issues:result.issues.length,transition_seek_determinism:result.transition_seek_determinism}));if(result.issues.length)process.exitCode=1;
 }else if(mode==='stills'){
  const samples=process.env.TIMES?process.env.TIMES.split(',').map(Number):await page.evaluate(()=>window.SEATED_SCENES.map(e=>(e.t0+e.t1)/2));
  const qa=path.join(out,'style-stills-v20');fs.mkdirSync(qa,{recursive:true});
  for(let i=0;i<samples.length;i++){let t=samples[i];const data=await page.evaluate(({t,rig})=>{window.renderAt(t,{});return document.getElementById('film').toDataURL('image/png').split(',')[1]},{t,rig:!!process.env.RIG_SAMPLE});fs.writeFileSync(path.join(qa,`${String(i).padStart(2,'0')}-${t.toFixed(2)}.png`),Buffer.from(data,'base64'))}
  console.log(JSON.stringify({stills:samples.length,path:qa}));
 }else if(mode==='check'||mode==='posecheck'){
  const evidence=await page.evaluate(async()=>({...window.__auditAll(),continuity:await window.__continuityQA(),support:await window.__supportQA()}));if(evidence.continuity.issues.length)evidence.issues.push(...evidence.continuity.issues);if(evidence.support.issues.length)evidence.issues.push(...evidence.support.issues);
  const ids=process.env.ONLY_ERAS?process.env.ONLY_ERAS.split(',').map(Number):Array.from({length:20},(_,i)=>i),sampleAt=ids[Math.floor(ids.length/2)]*2+.345,otherAt=ids[ids.length-1]*2+1;
  const pixels=()=>page.evaluate(t=>{window.renderAt(t);return document.getElementById('film').toDataURL()},sampleAt);
  const a=await pixels();await page.evaluate(t=>window.renderAt(t),otherAt);const b=await pixels();
  await page.goto({url:`http://127.0.0.1:${server.address().port}/film/index-v20.html${process.env.ONLY_ERAS?"?only="+process.env.ONLY_ERAS:""}`,timeout:60000});await page.evaluate(()=>window.__loadPromise);const d=await pixels();
  evidence.pixel_determinism=a===b&&a===d;
  const dest=path.join(root,'qa/v20');fs.mkdirSync(dest,{recursive:true});fs.writeFileSync(path.join(dest,'mechanical-check.json'),JSON.stringify(evidence,null,2));
  console.log(JSON.stringify({frames:evidence.frames,eras:evidence.era_count,issues:evidence.issues.length,max_reach_error:evidence.max_reach_error,pixel_determinism:evidence.pixel_determinism}));
  if(evidence.issues.length||!evidence.pixel_determinism)process.exitCode=1;
 }else{
  const sample=mode==='sample'||mode==='action',start=Number(process.env.START_SECONDS||0),frames=Number(process.env.FRAMES||(sample?144:960));
  const file=path.join(out,process.env.OUTPUT_FILENAME||(mode==='action'?'rig-action-v20.mp4':sample?'generated-action-sample-v20.mp4':'mother-baby-20-eras-portrait-v20-40s.mp4'));
  const videoThreads=process.env.VIDEO_THREADS||'2',temporary=file+'.partial.mp4';
  const ff=spawn(ffmpeg,['-v','error','-y','-f','image2pipe','-vcodec','mjpeg','-threads','1','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-threads:v',videoThreads,...(videoThreads==='1'?['-x264-params','threads=1:lookahead_threads=1']:[]),temporary],{stdio:['pipe','ignore','pipe'],windowsHide:true});let error='',writeError=null;ff.stderr.on('data',d=>{error+=d.toString();process.stderr.write(d)});ff.stdin.on('error',e=>{writeError=e});const closed=once(ff,'close');
  let heldFrame=null,uniqueReadbacks=0;
  for(let f=0;f<frames;f++){
   // Each actor frame contains its own baked motion-compensated inbetween.
   const data=await Promise.race([page.evaluate(({t})=>{const state=window.renderAt(t,{}),key=state.transition?'wipe:'+t:state.actor_key+':'+state.actor_frame+':env'+state.era+':'+state.cel;if(window.__encodedFrameKey===key)return null;window.__encodedFrameKey=key;return document.getElementById('film').toDataURL('image/jpeg',.97).split(',')[1]},{t:start+f/24}),new Promise((_,reject)=>{const timer=setTimeout(()=>reject(Error('frame timeout '+f)),45000);timer.unref()})]);
   if(data!==null){heldFrame=Buffer.from(data,'base64');uniqueReadbacks++}
   if(writeError)throw Error(error||writeError.message);
   if(!heldFrame)throw Error('Missing first encoded frame');
   if(!ff.stdin.write(heldFrame))await once(ff.stdin,'drain');
   if(f%24===0)console.log(JSON.stringify({rendered:f,total:frames}));
  }
  ff.stdin.end();const [code]=await closed;if(code!==0)throw Error(error||`encoder exit ${code}`);fs.renameSync(temporary,file);
  console.log(JSON.stringify({output:file,frames,uniqueReadbacks,duration:frames/24,width:1080,height:1920,audio:false}));
 }
}finally{await browser.close({silent:true});server.close()}
