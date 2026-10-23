import fs from 'node:fs';import path from 'node:path';import http from 'node:http';import {spawn} from 'node:child_process';import {createRequire} from 'node:module';import {fileURLToPath} from 'node:url';import {once} from 'node:events';import crypto from 'node:crypto';
const here=path.dirname(fileURLToPath(import.meta.url));
const require=createRequire('C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json');const {chromium}=require('playwright');
const args=process.argv.slice(2),option=(k,d)=>args.find(x=>x.startsWith('--'+k+'='))?.split('=').slice(1).join('=')??d;
const width=1080,height=1920,fps=24,range=option('range','0:40').split(':').map(Number),stills=args.includes('--stills');
const out=path.join(here,'out');fs.mkdirSync(out,{recursive:true});
const chrome='D:/ai项目/ai动画/VibeVideo项目/node_modules/.remotion/chrome-headless-shell/win64/chrome-headless-shell-win64/chrome-headless-shell.exe';
const ffmpeg='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe';
const server=http.createServer((req,res)=>{try{const rel=decodeURIComponent(new URL(req.url,'http://localhost').pathname);const file=path.resolve(here,'.'+rel);if(file!==here&&!file.startsWith(here+path.sep)){res.writeHead(403);res.end();return;}const p=rel==='/'?path.join(here,'index.html'):file;res.setHeader('Content-Type',p.endsWith('.js')?'text/javascript':p.endsWith('.html')?'text/html':'application/octet-stream');res.end(fs.readFileSync(p));}catch{res.writeHead(404);res.end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser,encoder;
try{
 browser=await chromium.launch({executablePath:chrome,headless:true,args:['--no-sandbox','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']});
 const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
 const errors=[];page.on('pageerror',e=>{errors.push(String(e));console.error(String(e));});
 await page.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
 await page.goto(`http://127.0.0.1:${server.address().port}/`);await page.waitForFunction(()=>window.READY,{timeout:60000});
 const start=Date.now();
 if(stills){
  const times=option('times','0,2.7,4.5,8.8,12.8,20.8,23,29.9,30.2,36.9,43.5,46,49.5,51.5,55,57.8,58.5,59.5').split(',').map(Number),states=[];
  for(const t of times){const state=await page.evaluate(t=>window.render(t),t);await page.locator('canvas').screenshot({path:path.join(out,`still-${t.toFixed(2)}.png`)});states.push({t,...state});console.log('still '+t);}
  fs.writeFileSync(path.join(out,'stills.json'),JSON.stringify({times,states,errors,elapsedMs:Date.now()-start},null,2));
 }else{
  const name=option('name',range[0]===0&&range[1]===40?'宝宝和太阳的晚安-v2.mp4':'key-sequence.mp4'),target=path.join(out,name);
  const audio=path.join(here,'score.wav'),ffargs=['-y','-hide_banner','-loglevel','warning','-f','image2pipe','-vcodec','mjpeg','-framerate',String(fps),'-i','pipe:0'];
  if(fs.existsSync(audio))ffargs.push('-ss',String(range[0]),'-i',audio);
  ffargs.push('-map','0:v:0');if(fs.existsSync(audio))ffargs.push('-map','1:a:0');
  ffargs.push('-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads:v','2');if(fs.existsSync(audio))ffargs.push('-c:a','aac','-b:a','192k');
  ffargs.push('-t',String(range[1]-range[0]),'-movflags','+faststart',target);
  encoder=spawn(ffmpeg,ffargs,{windowsHide:true,stdio:['pipe','ignore','pipe']});let stderr='';encoder.stderr.on('data',b=>{stderr+=b;});let exitPromise=once(encoder,'exit');
  const count=Math.round((range[1]-range[0])*fps),samples=[];
  for(let i=0;i<count;i++){
   const t=range[0]+i/fps,data=await page.evaluate(t=>{window.render(t);return document.querySelector('canvas').toDataURL('image/jpeg',.94).split(',')[1];},t);
   if(!encoder.stdin.write(Buffer.from(data,'base64')))await once(encoder.stdin,'drain');
   if(i%120===0){const elapsed=(Date.now()-start)/1000;console.log(JSON.stringify({frame:i,total:count,time:+t.toFixed(3),elapsedSeconds:+elapsed.toFixed(1)}));samples.push({frame:i,t,elapsed});}
  }
  encoder.stdin.end();const [code]=await exitPromise;if(code!==0)throw Error('ffmpeg '+code+' '+stderr.slice(-2000));if(errors.length)throw Error(errors.join('\n'));
  const hash=crypto.createHash('sha256').update(fs.readFileSync(target)).digest('hex');
  fs.writeFileSync(path.join(out,name+'.render.json'),JSON.stringify({output:target,sha256:hash,width,height,fps,range,count,errors,elapsedSeconds:(Date.now()-start)/1000,samples},null,2));console.log('complete '+target);
 }
}finally{if(encoder&&!encoder.killed&&encoder.exitCode===null)encoder.kill();if(browser)await browser.close();await new Promise(r=>server.close(r));}
