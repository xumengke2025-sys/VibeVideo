import fs from'node:fs';import path from'node:path';import{fileURLToPath}from'node:url';import{spawn}from'node:child_process';import{createHash}from'node:crypto';
import{chromium}from'../../sand-journey-20261010/node_modules/playwright-core/index.mjs';import{createServer}from'./server.mjs';import{DURATION,FPS}from'./timeline.js';
const root=path.dirname(fileURLToPath(import.meta.url));const args=Object.fromEntries(process.argv.slice(2).map(a=>{const[k,...v]=a.replace(/^--/,'').split('=');return[k,v.join('=')||true]}));
const mode=args.mode||'stills',version=args.version||'v1',width=Number(args.width||(mode==='preview'?540:1080)),height=width*16/9;
const out=path.join(root,'out',`${mode}-${version}`);fs.mkdirSync(out,{recursive:true});
const entry=args.entry||'index.html',audioFile=args.audio||'audio.wav';
const FF='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe',FP=FF.replace('ffmpeg.exe','ffprobe.exe');
const hash=b=>createHash('sha256').update(b).digest('hex');const run=(cmd,argv)=>new Promise((resolve,reject)=>{const p=spawn(cmd,argv,{windowsHide:true});let logs='';p.stdout.on('data',d=>logs+=d);p.stderr.on('data',d=>logs+=d);p.on('error',reject);p.on('exit',n=>n?reject(Error(logs.slice(-3000))):resolve(logs))});
const server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;const errors=[];
try{
 browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--disable-background-timer-throttling','--disable-renderer-backgrounding','--enable-webgl','--ignore-gpu-blocklist']});
 const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('/favicon.ico'))errors.push(r.status()+' '+r.url())});page.on('console',m=>{if(m.type()==='error'&&m.text().includes('THREE.WebGLProgram'))errors.push(m.text().slice(0,2000))});
 const rangeEnd=Number(args.end||(mode==='sample'?Number(args.start||18)+Number(args.duration||8):DURATION));
 await page.goto('http://127.0.0.1:'+server.address().port+'/work/waterloo-20261012/studio/'+entry+'?render&width='+width+'&end='+rangeEnd);await page.waitForFunction(()=>window.__ready,undefined,{timeout:90000}).catch(e=>{throw Error(errors.join('\n')||e.message)});if(errors.length)throw Error(errors.join('\n'));
 const capture=async(t,type='image/jpeg')=>Buffer.from((await page.evaluate(({t,type})=>window.renderAt(t,type,.96),{t,type})).split(',')[1],'base64');
 if(mode==='stills'){
  const times=String(args.times||'1,5,8.15,13,17,21,23.7,25.5,30,38,44,46.3,49,53,55,59').split(',').map(Number),stills=[];
  for(const t of times){const b=await capture(t,'image/png');fs.writeFileSync(path.join(out,`${t}.png`),b);stills.push({t,hash:hash(b),state:await page.evaluate(t=>window.stateAt(t),t)});console.log('still '+t)}
  const seeks=[];for(const t of times.slice(0,3).reverse())seeks.push({t,identical:hash(await capture(t,'image/png'))===stills.find(s=>s.t===t).hash});if(errors.length||seeks.some(x=>!x.identical))throw Error('Runtime or seeking failed');
  fs.writeFileSync(path.join(out,'checks.json'),JSON.stringify({errors,stills,seeks},null,2));
 }else{
  const start=mode==='sample'?Number(args.start||18):0,duration=mode==='sample'?Number(args.duration||8):DURATION,fps=mode==='preview'?12:FPS,count=Math.round(duration*fps),frames=path.join(out,'frames');fs.mkdirSync(frames,{recursive:true});
  const sources=entry==='index-v4.html'?[entry,'main-v4.js','timeline-v4.js',audioFile,...fs.readdirSync(path.join(root,'assets-v4')).sort().map(f=>'assets-v4/'+f)]:['main.js','art.js','timeline.js','vendor/paper.js','vendor/lib.js',audioFile];
  const signature=hash(Buffer.concat(sources.map(f=>fs.readFileSync(path.join(root,f)))));const cfg={signature,entry,audioFile,start,duration,fps,count,width,height};const cp=path.join(out,'config.json');
  if(fs.existsSync(cp)&&JSON.stringify(JSON.parse(fs.readFileSync(cp)))!==JSON.stringify(cfg))throw Error('Changed source; choose a new output version');fs.writeFileSync(cp,JSON.stringify(cfg,null,2));
  for(let i=0;i<count;i++){
   const f=path.join(frames,`${String(i).padStart(5,'0')}.jpg`);if(!fs.existsSync(f))fs.writeFileSync(f,await capture(start+i/fps));
   if(i%48===0||i===count-1){console.log(`captured ${i+1}/${count}`);fs.writeFileSync(path.join(out,'progress.json'),JSON.stringify({frame:i+1,count}))}if(errors.length)throw Error(errors.join('\n'));
  }
  await browser.close();browser=null;
  const video=path.join(out,'video.mp4');await run(FF,['-v','error','-y','-framerate',String(fps),'-i',path.join(frames,'%05d.jpg'),'-ss',String(start),'-i',path.join(root,audioFile),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','17','-preset','fast','-threads:v','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',String(duration),'-movflags','+faststart',video]);
  const probe=JSON.parse(await run(FP,['-v','error','-show_streams','-show_format','-of','json',video]));fs.writeFileSync(path.join(out,'ffprobe.json'),JSON.stringify(probe,null,2));
  await run(FF,['-v','error','-i',video,'-map','0:v:0','-map','0:a:0','-c:v','rawvideo','-threads:v','1','-c:a','pcm_s16le','-f','null','-']);
  const v=probe.streams.find(x=>x.codec_type==='video'),a=probe.streams.find(x=>x.codec_type==='audio');if(v.width!==width||v.height!==height||+v.nb_frames!==count||!a)throw Error('Media mismatch');
  const evidence={...cfg,video,sha256:hash(fs.readFileSync(video)),decoded:true,frames:+v.nb_frames,audio:true,errors};fs.writeFileSync(path.join(out,'evidence.json'),JSON.stringify(evidence,null,2));console.log('COMPLETE '+JSON.stringify(evidence));
 }
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r))}
