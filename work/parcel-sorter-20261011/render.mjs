import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {spawn} from 'node:child_process';import {createHash} from 'node:crypto';
import {chromium} from '../sand-journey-20261010/node_modules/playwright-core/index.mjs';import {createServer} from './server.mjs';
import {phaseTimer} from '../../skill/vibe-video/scripts/render_phase_timer.mjs';
import {FILM} from './js/timeline.js';
const ROOT=path.dirname(fileURLToPath(import.meta.url));process.chdir(ROOT);
const args=Object.fromEntries(process.argv.slice(2).map(x=>{const[k,...v]=x.replace(/^--/,'').split('=');return [k,v.join('=')||true]}));const mode=args.mode||'stills',version=args.version||'v1';
const FF='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe',FP=FF.replace('ffmpeg.exe','ffprobe.exe');
const out=path.join(ROOT,'out',mode+'-'+version);fs.mkdirSync(out,{recursive:true});
const timer=phaseTimer(out);
const errors=[];
if(!['stills','preview','sample','final'].includes(mode))throw Error('Unknown render mode');
const renderWidth=Number(args.width||(mode==='preview'?540:1080));if(![540,1080].includes(renderWidth))throw Error('Supported widths: 540,1080');if(['sample','final'].includes(mode)&&renderWidth!==1080)throw Error('Sample/final require 1080 width');
export function run(cmd,argv){if(cmd===FP)timer.start('probe');else if(cmd===FF&&argv.includes('null'))timer.start('decode_validation');return new Promise((res,rej)=>{const p=spawn(cmd,argv,{windowsHide:true,stdio:['ignore','pipe','pipe']});let out='';p.stdout.on('data',x=>out+=x);p.stderr.on('data',x=>out+=x);p.on('error',rej);p.on('exit',c=>c?rej(Error(out.slice(-3000))):res(out))})}
const hash=b=>createHash('sha256').update(b).digest('hex');
timer.start('browser_setup');let completed=false;
const server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;
try{browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--use-angle=d3d11','--enable-gpu','--ignore-gpu-blocklist','--disable-background-timer-throttling','--disable-renderer-backgrounding']});
const page=await browser.newPage({viewport:{width:renderWidth,height:renderWidth*16/9},deviceScaleFactor:1});page.on('pageerror',e=>errors.push(e.message));await page.goto('http://127.0.0.1:'+server.address().port+'/?render&width='+renderWidth+(args.query?'&'+args.query:''));await page.waitForFunction(()=>window.__ready,{timeout:90000});
const buffers=await page.evaluate(()=>window.__renderBuffers());if(Object.entries(buffers).some(([k,v])=>k!=='logical'&&(v[0]!==renderWidth||v[1]!==renderWidth*16/9)))throw Error('Intrinsic buffer size mismatch');
async function capture(t,w,type='image/jpeg'){if(w!==renderWidth)throw Error('Capture width differs from native buffer');const data=await page.evaluate(({t,type})=>window.renderAt(t,type,.96),{t,type});return Buffer.from(data.split(',')[1],'base64')}
timer.start('capture',{buffers});
if(mode==='stills'){
const times=args.times?String(args.times).split(',').map(Number):[0,1.6,2.8,4.4,5.3,5.9,7.0,8.6,10.0,11.4,12.6,13.8,14.2,14.6,15.6,17.0,18.4,20.0,21.6];const samples=[];
for(const t of times){const b=await capture(t,renderWidth,'image/png');fs.writeFileSync(path.join(out,t+'.png'),b);samples.push({t,hash:hash(b),state:await page.evaluate(t=>window.stateAt(t),t)});timer.progress({still:t});console.log('still '+t)}
timer.start('seek_check');const seeking=[];for(const t of times.slice(0,4).reverse())seeking.push({t,hash:hash(await capture(t,renderWidth,'image/png'))});const exact=seeking.every(x=>x.hash===samples.find(y=>x.t===y.t).hash);fs.writeFileSync(path.join(out,'checks.json'),JSON.stringify({errors,buffers,seeking,randomAccessIdentical:exact,samples},null,2));if(!exact||errors.length)throw Error('Seeking or runtime failed');
}else{
const start=mode==='sample'?Number(args.start||11):0,duration=mode==='sample'?Number(args.duration||6):FILM.duration,fps=mode==='preview'?15:30,width=renderWidth,count=Math.round(duration*fps);
const frames=path.join(out,'frames');fs.mkdirSync(frames,{recursive:true});const signature=hash(Buffer.concat(['js/main.js','js/timeline.js','render.mjs','vendor/three.module.js','audio/mix.wav'].map(f=>fs.readFileSync(f))));const config={signature,start,duration,fps,width,count,renderAlgorithm:'native-buffer-v2'};const configPath=path.join(out,'config.json');if(fs.existsSync(configPath)&&JSON.stringify(JSON.parse(fs.readFileSync(configPath)))!==JSON.stringify(config))throw Error('Changed source: choose a new --version');fs.writeFileSync(configPath,JSON.stringify(config));
for(let i=0;i<count;i++){const p=path.join(frames,String(i).padStart(5,'0')+'.jpg');if(!fs.existsSync(p))fs.writeFileSync(p,await capture(start+i/fps,width));if(i%30===0||i===count-1){timer.progress({frame:i+1,count});fs.writeFileSync(path.join(out,'progress.json'),JSON.stringify({frame:i+1,count}));console.log(`${mode} ${i+1}/${count}`)}if(errors.length)throw Error(errors.join('\n'))}
await browser.close();browser=null;timer.start('encode');const video=path.join(out,'video.mp4');await run(FF,['-hide_banner','-loglevel','error','-y','-framerate',String(fps),'-i',path.join(frames,'%05d.jpg'),'-ss',String(start),'-i','audio/mix.wav','-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-threads:v','2','-c:a','aac','-b:a','192k','-ar','48000','-t',String(duration),'-movflags','+faststart',video]);
timer.start('media_validation');const probe=JSON.parse(await run(FP,['-v','error','-show_streams','-show_format','-of','json',video]));fs.writeFileSync(path.join(out,'ffprobe.json'),JSON.stringify(probe,null,2));await run(FF,['-v','error','-i',video,'-map','0:v:0','-map','0:a:0','-c:v','rawvideo','-threads:v','1','-c:a','pcm_s16le','-f','null','-']);const v=probe.streams.find(x=>x.codec_type==='video'),a=probe.streams.find(x=>x.codec_type==='audio');if(+v.nb_frames!==count||v.width!==width||!a)throw Error('Media mismatch');const evidence={...config,video,sha256:hash(fs.readFileSync(video)),decoded:true,errors,frames:+v.nb_frames};fs.writeFileSync(path.join(out,'evidence.json'),JSON.stringify(evidence,null,2));console.log('COMPLETE '+JSON.stringify(evidence));
}
completed=true;
}finally{timer.finish(completed?'complete':'failed');if(browser)await browser.close();await new Promise(r=>server.close(r))}
