// Local code-film renderer. Needs an installed browser, FFmpeg and the package.json dependencies.
import fs from 'node:fs';import path from 'node:path';import http from 'node:http';import {createRequire} from 'node:module';import {spawn} from 'node:child_process';import {once} from 'node:events';import {createHash} from 'node:crypto';
const args=Object.fromEntries(process.argv.slice(2).map(s=>{const i=s.indexOf('=');return [s.slice(2,i<0?undefined:i),i<0?true:s.slice(i+1)];}));
const root=path.resolve(args.project||'.'),out=path.resolve(args.out||'out'),req=createRequire(path.join(root,'package.json'));
const {chromium}=args.playwright?req(args.playwright):req('playwright-core');
const threeRoot=args.three||path.dirname(req.resolve('three/package.json'));
const chrome=args.chrome||process.env.CHROME_PATH||(process.platform==='win32'?'C:/Program Files/Google/Chrome/Application/chrome.exe':undefined);
const ffmpeg=args.ffmpeg||process.env.FFMPEG_PATH||'ffmpeg';
const mime={'.html':'text/html','.mjs':'text/javascript','.js':'text/javascript','.json':'application/json','.jpg':'image/jpeg','.png':'image/png','.woff2':'font/woff2','.css':'text/css'};
const server=http.createServer((request,response)=>{const u=new URL(request.url,'http://local');const base=u.pathname.startsWith('/node_modules/three/')?threeRoot:root;
 const suffix=u.pathname.startsWith('/node_modules/three/')?u.pathname.slice(20):u.pathname==='/'?'index.html':decodeURIComponent(u.pathname.slice(1));const p=path.resolve(base,suffix);
 if(p!==base&&!p.startsWith(path.resolve(base)+path.sep)){response.writeHead(403);response.end();return;}
 try{response.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');response.end(fs.readFileSync(p));}catch{response.writeHead(404);response.end('missing');}
});
let browser,encoder;const evidence={errors:[],blocked:[],requests:[]};
try {
 fs.mkdirSync(out,{recursive:true});await new Promise(r=>server.listen(0,'127.0.0.1',r));
 browser=await chromium.launch({executablePath:chrome,headless:true,args:process.platform==='win32'?['--use-angle=d3d11']:[]});
 const page=await browser.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});page.on('pageerror',e=>evidence.errors.push(e.message));
 await page.route('**/*',async route=>{const u=route.request().url();evidence.requests.push(u);if(!u.startsWith(`http://127.0.0.1:${server.address().port}/`)){evidence.blocked.push(u);return route.abort();}return route.continue();});
 await page.goto(`http://127.0.0.1:${server.address().port}/?render`);await page.waitForFunction(()=>window.ready&&typeof window.renderAt==='function',null,{timeout:120000});
 const info=await page.evaluate(()=>{const f=window.__film;return {duration:f.duration,fps:f.fps,width:f.width,height:f.height,cuts:f.cuts||[],continuousCuts:f.continuousCuts||[],holdStart:f.holdStart};});evidence.info=info;
 async function capture(t,sub=1,type='image/jpeg'){
  return Buffer.from((await page.evaluate(async({t,sub,type})=>{
    if(sub===1)return window.renderAt(t,type,.96);
    const c=window.__captureCanvas||(window.__captureCanvas=document.createElement('canvas'));c.width=window.__film.width;c.height=window.__film.height;const g=c.getContext('2d');
    const im=window.__captureImage||(window.__captureImage=new Image());
    for(let k=0;k<sub;k++){im.src=await window.renderAt(Math.min(window.__film.duration,t+(k+.5)/sub*.5/window.__film.fps),'image/png');await im.decode();g.globalAlpha=1/(k+1);g.drawImage(im,0,0);}
    return c.toDataURL(type,.96);
  },{t,sub,type})).split(',')[1],'base64');
 }
 const samples=args.stills?args.stills.split(',').map(Number):[.05,.16,.25,.4,.55,.68,.8,.88,.98].map(k=>k*info.duration);
 for(const t of samples){fs.writeFileSync(path.join(out,`still-${t.toFixed(3)}.png`),await capture(t,1,'image/png'));}
 // Test history independence of actual pixels, including a later shot before rewinding.
 const threeTimes=[.15,.55,.77].map(k=>k*info.duration),sequence=[...threeTimes,...threeTimes],hashes=[];
 for(let i=0;i<sequence.length;i++){const buf=await capture(sequence[i],1,'image/png');hashes.push(createHash('sha256').update(buf).digest('hex'));fs.writeFileSync(path.join(out,`seek-${i}.png`),buf);}
 evidence.seek={sequence,hashes,identical:[0,1,2].every(i=>hashes[i]===hashes[i+3])};
 evidence.camera=await page.evaluate(()=>{const f=window.__film;if(!f.stateAt)return null;const cv=p=>({p:p.position.toArray(),target:p.target.toArray(),fov:p.fov});return {boundaries:(f.cuts||[]).map(t=>({t,before:cv(f.stateAt(t-1e-7).pose),at:cv(f.stateAt(t).pose)})),hold:f.holdStart===undefined?null:cv(f.stateAt(f.holdStart+1e-7).pose),end:cv(f.stateAt(f.duration).pose)};});
 if(!args['stills-only']){
  const [start,end]=(args.range||`0:${info.duration}`).split(':').map(Number),fps=Number(args.fps||info.fps),n=Math.round((end-start)*fps),sub=Number(args.sub||1);
  if(!(start>=0&&end<=info.duration&&end>start&&n>0))throw Error('Invalid range');
  const video=path.join(out,args.name||'lumen.mp4'),temporary=video+'.tmp.mp4',frames=path.join(out,'frames');fs.mkdirSync(frames,{recursive:true});
  const sourceHash=createHash('sha256');for(const f of ['index.html','film.js','camera-kit.mjs']){const p=path.join(root,f);if(fs.existsSync(p))sourceHash.update(fs.readFileSync(p));}
  const config={start,end,fps,frames:n,sub,sourceHash:sourceHash.digest('hex')},manifest=path.join(out,'frame-config.json');
  if(fs.existsSync(manifest)&&JSON.stringify(JSON.parse(fs.readFileSync(manifest)))!==JSON.stringify(config))throw Error('Frame configuration changed; use a new output directory');fs.writeFileSync(manifest,JSON.stringify(config));
  for(let i=0;i<n;i++){const file=path.join(frames,String(i).padStart(5,'0')+'.jpg');if(!fs.existsSync(file))fs.writeFileSync(file,await capture(start+i/fps,sub));if(i%30===0){console.log(`capture ${i}/${n}`);fs.writeFileSync(path.join(out,'progress.json'),JSON.stringify({phase:'capture',frame:i,total:n}));}}
  const stderr=[];fs.writeFileSync(path.join(out,'progress.json'),JSON.stringify({phase:'encode',frames:n}));
  encoder=spawn(ffmpeg,['-hide_banner','-loglevel','error','-y','-f','image2','-framerate',String(fps),'-vcodec','mjpeg','-i',path.join(frames,'%05d.jpg'),'-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-threads:v',String(args.threads||2),'-movflags','+faststart',temporary],{windowsHide:true,stdio:['ignore','ignore','pipe']});
  encoder.stderr.on('data',d=>{stderr.push(d.toString());if(stderr.length>50)stderr.shift();});
  const done=new Promise((resolve,reject)=>{encoder.on('error',reject);encoder.on('exit',code=>code===0?resolve():reject(Error('FFmpeg '+code+' '+stderr.join('').slice(-1200))));});done.catch(()=>{});
  await done;fs.renameSync(temporary,video);evidence.render={...config,video,sha256:createHash('sha256').update(fs.readFileSync(video)).digest('hex')};fs.writeFileSync(path.join(out,'progress.json'),JSON.stringify({phase:'complete',frames:n}));
 }
 evidence.requests=[...new Set(evidence.requests)];fs.writeFileSync(path.join(out,'render-evidence.json'),JSON.stringify(evidence,null,2));
 if(!evidence.seek.identical)console.warn('Repeated pixel capture differs; inspect seek images and render-evidence.json');
 if(evidence.errors.length||evidence.blocked.length||(args['strict-pixels']&&!evidence.seek.identical))throw Error('Render evidence needs review');
 console.log(JSON.stringify({out,seek:evidence.seek.identical,errors:evidence.errors}));
}catch(e){fs.writeFileSync(path.join(out,'failure.txt'),e.stack||String(e));throw e;}finally{if(browser)await browser.close();server.close();}

