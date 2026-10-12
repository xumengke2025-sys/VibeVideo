import {createRequire} from 'node:module';
import {createServer} from 'node:http';
import {readFileSync,existsSync,mkdirSync,writeFileSync} from 'node:fs';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=path.dirname(fileURLToPath(import.meta.url)),req=createRequire(import.meta.url);
let chromium;try{({chromium}=req('playwright-core'));}catch{({chromium}=req(process.env.PLAYWRIGHT_PATH||'C:/CodexTemp/pdoom-review-20261008/app/node_modules/playwright-core'));}
const threeBuild=path.dirname(req.resolve('three'));
const ffmpeg=process.env.FFMPEG||path.resolve(root,'../../node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe');
const chrome=process.env.CHROME||'C:/Program Files/Google/Chrome/Application/chrome.exe';
const port=Number(process.env.PORT)||8926;
const out=path.join(root,'out');mkdirSync(out,{recursive:true});
const versionArg=process.argv.find(a=>a.startsWith('--version='));const version=versionArg?'-'+versionArg.slice(10).replace(/[^a-z0-9_-]/gi,''):'';
const mime={'.mjs':'text/javascript','.js':'text/javascript','.html':'text/html','.frag':'text/plain','.wav':'audio/wav','.png':'image/png','.mp4':'video/mp4','.json':'application/json','.jpg':'image/jpeg'};
const server=createServer((request,response)=>{
  try{let url=new URL(request.url,'http://localhost');let pathname=decodeURIComponent(url.pathname);let file=pathname.startsWith('/vendor/')?path.join(threeBuild,path.basename(pathname)):path.join(root,pathname==='/'?'index.html':pathname.slice(1));
  if(!file.startsWith(root)&&!file.startsWith(threeBuild)){response.writeHead(403);response.end();return;}
  if(!existsSync(file)){response.writeHead(404);response.end('Not found');return;}
  response.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream','Cache-Control':'no-store'});response.end(readFileSync(file));}catch(e){response.writeHead(500);response.end(e.message);}
});
await new Promise((resolve,reject)=>{server.on('error',reject);server.listen(port,'127.0.0.1',resolve);});
if(process.argv.includes('--serve')){console.log(`Preview http://127.0.0.1:${port}`);process.on('SIGINT',()=>server.close(()=>process.exit(0)));await new Promise(()=>{});}
let browser;const errors=[],resources=[];let encoder;
try{
 browser=await chromium.launch({executablePath:chrome,headless:true,args:['--use-angle=d3d11','--enable-gpu-rasterization','--disable-background-timer-throttling','--disable-dev-shm-usage']});
 const study=process.argv.includes('--study'),stillsOnly=process.argv.includes('--stills');
 const width=study?1280:1920,height=Math.round(width*9/16),page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('response',r=>{if(r.status()>=400)resources.push({url:r.url(),status:r.status()});});
 await page.goto(`http://127.0.0.1:${port}/?export=1&w=${width}`);await page.waitForFunction(()=>window.__film?.ready,null,{timeout:60000});
 const quality=await page.evaluate(()=>window.__film.quality);console.log('Scene ready',JSON.stringify(quality));
 if(stillsOnly){
   mkdirSync(path.join(out,'stills'),{recursive:true});
   for(const t of [0,2,6.5,9.5,11.4,13,15,17.5,23,27.5,31.5]){await page.evaluate(t=>window.__film.renderAt(t),t);await page.screenshot({path:path.join(out,'stills',`${t.toFixed(2).padStart(5,'0')}s.png`)});console.log('Still',t);}
 }else{
  const start=study?8:0,duration=study?9:32,total=Math.round(duration*30),output=path.join(out,study?`key-action-study${version}.mp4`:`around-the-dark${version}.mp4`);
  const args=['-hide_banner','-loglevel','error','-y','-f','image2pipe','-framerate','30','-vcodec','mjpeg','-i','pipe:0'];
  if(existsSync(path.join(root,'soundtrack.wav')))args.push('-ss',String(start),'-i',path.join(root,'soundtrack.wav'));
  args.push('-map','0:v:0');if(existsSync(path.join(root,'soundtrack.wav')))args.push('-map','1:a:0','-c:a','aac','-b:a','256k');
  args.push('-c:v','libx264','-threads:v','2','-preset','medium','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart','-t',String(duration),output);
  encoder=spawn(ffmpeg,args,{windowsHide:true,stdio:['pipe','ignore','pipe']});let encoderLog='';encoder.stderr.on('data',b=>encoderLog+=b.toString());
  const completed=new Promise((resolve,reject)=>{encoder.on('error',reject);encoder.on('exit',code=>code===0?resolve():reject(new Error(encoderLog||`Encoder exit ${code}`)));});
  encoder.stdin.on('error',()=>{});
  const began=performance.now();
  for(let n=0;n<total;n++){
   await page.evaluate(t=>window.__film.renderAt(t),start+n/30);
   const jpeg=await page.screenshot({type:'jpeg',quality:97});
   if(!encoder.stdin.write(jpeg))await new Promise(resolve=>encoder.stdin.once('drain',resolve));
   if(n%30===0)console.log(`FRAME ${n}/${total} elapsed=${Math.round((performance.now()-began)/1000)}s`);
  }
  encoder.stdin.end();await completed;encoder=null;
  console.log('Encoded',output);
 }
 if(errors.length||resources.length)throw new Error(JSON.stringify({errors,resources}));
 writeFileSync(path.join(out,stillsOnly?`stills-render${version}.json`:study?`study-render${version}.json`:`render-manifest${version}.json`),JSON.stringify({created_at:new Date().toISOString(),kind:'Original Codex-authored visualization; no pdoom scene code used',quality,browser_errors:errors,resource_failures:resources,width,height,fps:30,rendering:'Deterministic world geometry and Schwarzschild orbit ray integration, 1.5x spatial supersampling and MSAA for geometry, Chromium JPEG 97 frames encoded with x264 CRF17',audio:existsSync(path.join(root,'soundtrack.wav'))},null,2));
}finally{if(encoder)encoder.kill();if(browser)await browser.close();server.close();}
