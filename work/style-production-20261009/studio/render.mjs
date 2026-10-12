// Deterministic Canvas capture. No global configuration changes or downloads.
import fs from 'node:fs';import path from 'node:path';import http from 'node:http';
import {fileURLToPath} from 'node:url';import {createRequire} from 'node:module';import {spawn} from 'node:child_process';import {createHash} from 'node:crypto';
import {validate,reviewSchedule} from './timeline.mjs';
const args=Object.fromEntries(process.argv.slice(2).map(s=>{if(!s.startsWith('--'))throw Error('Use --key=value');const i=s.indexOf('=');return [s.slice(2,i<0?undefined:i),i<0?true:s.slice(i+1)];}));
const root=path.dirname(fileURLToPath(import.meta.url)),id=args.clip||'one-way';if(!/^[a-z0-9-]+$/.test(id))throw Error('Invalid clip');
const plan=JSON.parse(fs.readFileSync(path.join(root,'clips',id+'.json'),'utf8'));const errors=validate(plan);if(errors.length)throw Error(errors.join('\n'));
const req=createRequire(path.join(root,'package.json')), {chromium}=req(args.playwright||'playwright-core');
const out=path.resolve(args.out||path.join(root,'out',id));fs.mkdirSync(out,{recursive:true});
const digest=b=>createHash('sha256').update(b).digest('hex');
const sourceFiles=['index.html','film.mjs','timeline.mjs','render.mjs','clips/'+id+'.json'];
const source=sourceFiles.map(f=>({path:f,sha256:digest(fs.readFileSync(path.join(root,f)))}));
const manifest={id,width:1280,height:720,fps:plan.fps,frames:Math.round(plan.duration*plan.fps),source};
const manifestPath=path.join(out,'frame-config.json');if(fs.existsSync(manifestPath)&&JSON.stringify(JSON.parse(fs.readFileSync(manifestPath)))!==JSON.stringify(manifest))throw Error('Source/config changed: choose a new output directory.');
fs.writeFileSync(manifestPath,JSON.stringify(manifest,null,2));
const mime={'.html':'text/html','.mjs':'text/javascript','.json':'application/json'};
const server=http.createServer((request,response)=>{try{
 const url=new URL(request.url,'http://local'),rel=url.pathname==='/'?'index.html':decodeURIComponent(url.pathname.slice(1)),file=path.resolve(root,rel);
 if(!file.startsWith(root+path.sep))throw Error('Outside root');response.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');response.end(fs.readFileSync(file));
}catch{response.writeHead(404);response.end('missing');}});
const evidence={clip:id,errors:[],blocked:[],httpErrors:[],requests:[],source,reviewSchedule:reviewSchedule(plan),listened:false};let browser,encoder;
async function run(binary,argv){return await new Promise((resolve,reject)=>{const child=spawn(binary,argv,{windowsHide:true,stdio:['ignore','ignore','pipe']});encoder=child;let log='';child.stderr.on('data',b=>{log=(log+b).slice(-3000);});child.once('error',reject);child.once('close',code=>code===0?resolve():reject(Error(`${binary} exited ${code}: ${log}`)));});}
try{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin=`http://127.0.0.1:${server.address().port}`;
 browser=await chromium.launch({headless:true,executablePath:args.chrome||process.env.CHROME_PATH||(process.platform==='win32'?'C:/Program Files/Google/Chrome/Application/chrome.exe':undefined)});
 async function page(){const p=await browser.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1});p.on('pageerror',e=>evidence.errors.push(e.message));p.on('response',r=>{if(r.status()>=400)evidence.httpErrors.push({url:r.url(),status:r.status()});});
  await p.route('**/*',async route=>{const u=route.request().url();evidence.requests.push(u);if(!u.startsWith(origin+'/')){evidence.blocked.push(u);return route.abort();}return route.continue();});
  await p.goto(origin+'/?render&clip='+id,{timeout:30000});await p.waitForFunction(()=>window.ready,null,{timeout:30000});return p;
 }
 const p=await page();
 async function capture(pg,t,type='image/png'){return Buffer.from((await pg.evaluate(({t,type})=>window.renderAt(t,type,.95),{t,type})).split(',')[1],'base64');}
 // Three independent evaluation patterns, including a fresh page.
 const times=[.17,.56,.83].map(x=>x*plan.duration),first=[];
 for(const t of times)first.push(digest(await capture(p,t)));
 const rewind=[];for(const t of [...times].reverse())rewind.push({time:t,hash:digest(await capture(p,t))});
 const other=await page(),fresh=[];for(const t of times)fresh.push(digest(await capture(other,t)));await other.close();
 evidence.seek={times,forward:first,reverse:rewind,fresh,identical:first.every((h,i)=>h===fresh[i]&&h===rewind.find(x=>x.time===times[i]).hash)};
 if(!evidence.seek.identical)throw Error('Pixels differ across seek order or fresh page');
 const stillTimes=args.stills?args.stills.split(',').map(Number):[...new Set([...evidence.reviewSchedule.states.map(x=>x.time),...plan.events.map(e=>e.at+e.duration/2)])].sort((a,b)=>a-b);
 for(const t of stillTimes){if(t<0||t>=plan.duration)throw Error('Invalid still time');fs.writeFileSync(path.join(out,`still-${t.toFixed(3)}.png`),await capture(p,t));}
 // Export actual geometry state so tests can check closure and data correspondence.
 evidence.states=await p.evaluate(times=>times.map(t=>({time:t,state:window.stateAt(t)})),[0,...plan.events.flatMap(e=>[e.at,e.at+e.duration]),plan.duration]);
 if(!args['stills-only']){
  const frames=path.join(out,'frames');fs.mkdirSync(frames,{recursive:true});
  for(let i=0;i<manifest.frames;i++){
   const file=path.join(frames,String(i).padStart(5,'0')+'.jpg');if(!fs.existsSync(file))fs.writeFileSync(file,await capture(p,i/plan.fps,'image/jpeg'));
   if(i%48===0){console.log(`${id}: ${i}/${manifest.frames}`);fs.writeFileSync(path.join(out,'progress.json'),JSON.stringify({phase:'capture',frame:i,total:manifest.frames}));}
  }
  const video=path.join(out,id+'-silent.mp4'),tmp=video+'.tmp.mp4';
  await run(args.ffmpeg||process.env.FFMPEG_PATH||'ffmpeg',['-hide_banner','-loglevel','error','-y','-f','image2','-framerate',String(plan.fps),'-vcodec','mjpeg','-i',path.join(frames,'%05d.jpg'),'-an','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-threads:v','2','-movflags','+faststart',tmp]);
  fs.renameSync(tmp,video);evidence.video={file:video,sha256:digest(fs.readFileSync(video)),frames:manifest.frames};
 }
 evidence.requests=[...new Set(evidence.requests)];fs.writeFileSync(path.join(out,'render-evidence.json'),JSON.stringify(evidence,null,2));
 if(evidence.errors.length||evidence.blocked.length||evidence.httpErrors.length)throw Error('See render-evidence.json');
 fs.writeFileSync(path.join(out,'progress.json'),JSON.stringify({phase:args['stills-only']?'stills-complete':'complete'}));console.log(JSON.stringify({clip:id,out,seek:true,errors:0}));
}catch(e){evidence.failure=e.message;fs.writeFileSync(path.join(out,'render-evidence.json'),JSON.stringify(evidence,null,2));throw e;}
finally{if(encoder&&encoder.exitCode===null)encoder.kill();if(browser)await browser.close();server.close();}
