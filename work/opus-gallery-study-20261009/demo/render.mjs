import {createServer} from 'node:http';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {createRequire} from 'node:module';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
const root=path.dirname(fileURLToPath(import.meta.url));
const req=createRequire(import.meta.url);
const {chromium}=req(process.env.PLAYWRIGHT_PATH||'C:/CodexTemp/pdoom-review-20261008/app/node_modules/playwright-core');
const ffmpeg=process.env.FFMPEG||path.resolve(root,'../../../node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe');
const out=path.join(root,'out');mkdirSync(out,{recursive:true});
const allowed=new Map([['/',path.join(root,'index.html')],['/continuity.mjs',path.join(root,'continuity.mjs')]]);
const server=createServer((request,response)=>{try{const name=new URL(request.url,'http://localhost').pathname,file=allowed.get(name);if(!file){response.writeHead(404);response.end();return;}response.writeHead(200,{'Content-Type':name.endsWith('.mjs')?'text/javascript':'text/html; charset=utf-8'});response.end(readFileSync(file));}catch(e){response.writeHead(500);response.end(e.message);}});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
let browser,encoder;
try{
 browser=await chromium.launch({executablePath:process.env.CHROME||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(`http://127.0.0.1:${server.address().port}/?export=1`);await page.waitForFunction(()=>window.__film?.ready);await page.evaluate(()=>document.fonts.ready);
 const hashes={};
 for(const t of [0,2.8,4.5,7.95,1.5,4.5,0,8]){
  await page.evaluate(t=>window.seek(t),t);const bytes=await page.screenshot();const hash=createHash('sha256').update(bytes).digest('hex');
  if(hashes[t]&&hashes[t]!==hash)throw new Error(`Nondeterministic screenshot at ${t}`);hashes[t]=hash;
 }
 if(hashes[0]!==hashes[8])throw new Error('Endpoint mismatch');
 for(const t of [.5,1.5,2.8,4.5,6.3,7.7]){await page.evaluate(t=>window.seek(t),t);await page.screenshot({path:path.join(out,`still-${t}.png`)});}
 console.log('Out-of-order seek and loop endpoints passed');
 encoder=spawn(ffmpeg,['-hide_banner','-loglevel','error','-y','-f','image2pipe','-framerate','30','-vcodec','mjpeg','-i','pipe:0','-c:v','libx264','-threads:v','1','-preset','medium','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',path.join(out,'continuity-study.mp4')],{windowsHide:true,stdio:['pipe','ignore','pipe']});
 let log='';encoder.stderr.on('data',data=>log+=data);encoder.stdin.on('error',()=>{});
 const done=new Promise((resolve,reject)=>{encoder.on('error',reject);encoder.on('exit',code=>code===0?resolve():reject(new Error(log)));});
 for(let f=0;f<240;f++){await page.evaluate(t=>window.seek(t),f/30);const jpeg=await page.screenshot({type:'jpeg',quality:96});if(!encoder.stdin.write(jpeg))await new Promise(resolve=>encoder.stdin.once('drain',resolve));if(f%60===0)console.log(`Frame ${f}/240`);}
 encoder.stdin.end();await done;encoder=null;
 if(errors.length)throw new Error(errors.join('\n'));
 writeFileSync(path.join(out,'render-check.json'),JSON.stringify({width:1280,height:720,fps:30,duration:8,frames:240,out_of_order_seek:'passed',same_time_png_hashes:hashes,loop_endpoints:'passed',browser_errors:errors,audio:false,scope:'Original technique study, not original-author source reconstruction or full-showreel parity'},null,2));
 console.log('Rendered continuity-study.mp4');
}finally{if(encoder)encoder.kill();if(browser)await browser.close();server.close();}
