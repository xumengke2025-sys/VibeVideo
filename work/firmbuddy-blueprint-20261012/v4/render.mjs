import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
import {createServer} from '../server.mjs';

const ROOT=path.dirname(fileURLToPath(import.meta.url));
const {chromium}=await (process.env.FIRMBUDDY_PLAYWRIGHT
  ? import(pathToFileURL(process.env.FIRMBUDDY_PLAYWRIGHT).href)
  : import('../../sand-journey-20261010/node_modules/playwright-core/index.mjs').catch(()=>import('playwright-core')));
const args=Object.fromEntries(process.argv.slice(2).map(s=>{const [k,...v]=s.replace(/^--/,'').split('=');return[k,v.join('=')||true]}));
const mode=args.mode||'stills',version=args.version||'v4',width=Number(args.width||1920),height=Math.round(width*9/16);
const out=path.resolve(ROOT,'../out',`${mode}-${version}`);fs.mkdirSync(out,{recursive:true});
const FF=process.env.FIRMBUDDY_FFMPEG||path.resolve(ROOT,'../../../node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe');
const FP=process.env.FIRMBUDDY_FFPROBE||FF.replace('ffmpeg.exe','ffprobe.exe');
const hash=b=>createHash('sha256').update(b).digest('hex');
const run=(cmd,argv)=>new Promise((resolve,reject)=>{const child=spawn(cmd,argv,{windowsHide:true});let result='';child.stdout.on('data',s=>result+=s);child.stderr.on('data',s=>result+=s);child.on('error',reject);child.on('exit',c=>c?reject(Error(result.slice(-5000))):resolve(result));});
const server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;const errors=[];
try{
  browser=await chromium.launch({executablePath:process.env.FIRMBUDDY_CHROME||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--use-angle=d3d11','--enable-gpu','--ignore-gpu-blocklist','--disable-background-timer-throttling']});
  const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/v4/index.html?render&width=${width}`);await page.waitForFunction(()=>window.__ready,{timeout:60000});
  const capture=async(t,type='image/jpeg')=>Buffer.from((await page.evaluate(({t,type})=>window.renderAt(t,type,.95),{t,type})).split(',')[1],'base64');
  if(mode==='stills'){
    const times=String(args.times||'2.7,4.5,12.8,16.7,20.5,22.5,25.5,28.5,31,33.8,37.5,39.6,43.5,48.5,50.5,53.5,56.7,59.3,66.5').split(',').map(Number),samples=[];
    for(const t of times){const b=await capture(t,'image/png');fs.writeFileSync(path.join(out,`${t}.png`),b);samples.push({t,hash:hash(b),state:await page.evaluate(t=>window.stateAt(t),t)});console.log(`still ${t}`);}
    const seeks=[];for(const t of times.slice(0,3).reverse())seeks.push({t,identical:hash(await capture(t,'image/png'))===samples.find(s=>s.t===t).hash});
    fs.writeFileSync(path.join(out,'checks.json'),JSON.stringify({errors,samples,seeks},null,2));if(errors.length||seeks.some(s=>!s.identical))throw Error('Runtime or deterministic seek failed');
  }else{
    const start=Number(args.start||0),duration=Number(args.duration||68),fps=Number(args.fps||30),count=Math.round(duration*fps);
    const frames=path.join(out,'frames');fs.mkdirSync(frames,{recursive:true});
    const signature=hash(Buffer.concat(['film.js','vendor/draw.js','vendor/paper.js','plan.json','audio/mix.wav'].map(f=>fs.readFileSync(path.join(ROOT,f)))));
    const config={signature,start,duration,fps,width,height,count},cfg=path.join(out,'config.json');
    if(fs.existsSync(cfg)&&JSON.stringify(JSON.parse(fs.readFileSync(cfg)))!==JSON.stringify(config))throw Error('Source changed: choose another version');
    fs.writeFileSync(cfg,JSON.stringify(config,null,2));const began=Date.now();
    if(args.reuse){
      const reuse=path.resolve(ROOT,args.reuse),rc=JSON.parse(fs.readFileSync(path.join(reuse,'config.json')));
      if(rc.signature!==signature||rc.fps!==fps||rc.width!==width||rc.height!==height)throw Error('Reuse source, fps or dimensions mismatch');
      let reused=0;
      for(let i=0;i<rc.count;i++){
        const destination=Math.round((rc.start+i/rc.fps-start)*fps);
        if(destination<0||destination>=count)continue;
        const src=path.join(reuse,'frames',String(i).padStart(5,'0')+'.jpg'),dst=path.join(frames,String(destination).padStart(5,'0')+'.jpg');
        if(fs.existsSync(src)&&!fs.existsSync(dst)){fs.copyFileSync(src,dst);reused++;}
      }
      console.log(`REUSED ${reused} source-identical frames`);
    }
    for(let i=0;i<count;i++){
      const target=path.join(frames,String(i).padStart(5,'0')+'.jpg');
      if(!fs.existsSync(target))fs.writeFileSync(target,await capture(start+i/fps));
      if(i%60===0||i===count-1){const progress={frame:i+1,count,elapsed_seconds:Math.round((Date.now()-began)/1000)};console.log(JSON.stringify(progress));fs.writeFileSync(path.join(out,'progress.json'),JSON.stringify(progress));}
      if(errors.length)throw Error(errors.join('\n'));
    }
    await browser.close();browser=null;
    const video=path.join(out,'video.mp4');
    await run(FF,['-hide_banner','-loglevel','error','-y','-framerate',String(fps),'-i',path.join(frames,'%05d.jpg'),'-ss',String(start),'-i',path.join(ROOT,'audio/mix.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-threads:v','2','-c:a','aac','-b:a','192k','-t',String(duration),'-movflags','+faststart',video]);
    const probe=JSON.parse(await run(FP,['-v','error','-show_streams','-show_format','-of','json',video]));fs.writeFileSync(path.join(out,'ffprobe.json'),JSON.stringify(probe,null,2));
    await run(FF,['-v','error','-i',video,'-map','0:v:0','-map','0:a:0','-c:v','rawvideo','-threads:v','1','-c:a','pcm_s16le','-f','null','-']);
    const v=probe.streams.find(s=>s.codec_type==='video'),a=probe.streams.find(s=>s.codec_type==='audio');
    if(v.width!==width||v.height!==height||+v.nb_frames!==count||!a||Math.abs(+probe.format.duration-duration)>.1)throw Error('Media specification mismatch');
    const evidence={...config,video,sha256:hash(fs.readFileSync(video)),decoded:true,errors,audio:true,frames:+v.nb_frames};
    fs.writeFileSync(path.join(out,'evidence.json'),JSON.stringify(evidence,null,2));console.log('COMPLETE '+JSON.stringify(evidence));
  }
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
