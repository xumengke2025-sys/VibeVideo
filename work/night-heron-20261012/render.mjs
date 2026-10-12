import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {spawn} from 'node:child_process';import {createHash} from 'node:crypto';
import {chromium} from '../sand-journey-20261010/node_modules/playwright-core/index.mjs';import {createServer} from './server.mjs';
import {phaseTimer} from '../../skill/vibe-video/scripts/render_phase_timer.mjs';
const ROOT=path.dirname(fileURLToPath(import.meta.url));process.chdir(ROOT);
const args=Object.fromEntries(process.argv.slice(2).map(x=>{const[k,...v]=x.replace(/^--/,'').split('=');return [k,v.join('=')||true]}));
const mode=args.mode||'stills',version=args.version||'v1';
const FF='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe',FP=FF.replace('ffmpeg.exe','ffprobe.exe');
const out=path.join(ROOT,'out',mode+'-'+version);fs.mkdirSync(out,{recursive:true});
const timer=phaseTimer(out);const errors=[];
if(!['stills','preview','final'].includes(mode))throw Error('Unknown mode');
const W=1080,H=1920,renderWidth=Number(args.width||(mode==='preview'?540:1080));
if(![540,1080].includes(renderWidth))throw Error('width must be 540 or 1080');
if(mode==='final'&&renderWidth!==1080)throw Error('final requires 1080');
export function run(cmd,argv){if(cmd===FP)timer.start('probe');else if(cmd===FF&&argv.includes('null'))timer.start('decode_validation');return new Promise((res,rej)=>{const p=spawn(cmd,argv,{windowsHide:true,stdio:['ignore','pipe','pipe']});let o='';p.stdout.on('data',x=>o+=x);p.stderr.on('data',x=>o+=x);p.on('error',rej);p.on('exit',c=>c?rej(Error(o.slice(-3000))):res(o))})}
const hash=b=>createHash('sha256').update(b).digest('hex');
timer.start('browser_setup');let completed=false;
const server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;
try{
browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--use-angle=d3d11','--enable-gpu','--ignore-gpu-blocklist','--disable-background-timer-throttling','--disable-renderer-backgrounding']});
const page=await browser.newPage({viewport:{width:renderWidth,height:renderWidth*16/9},deviceScaleFactor:1});
page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:'+server.address().port+'/?w='+renderWidth+(args.query?'&'+args.query:''),{waitUntil:'load'});
await page.waitForFunction(()=>window.READY===true,{timeout:180000});
// 画布原生尺寸必须等于目标渲染宽度（防"假低清"）
const bufs=await page.evaluate(()=>{const c=document.querySelector('#gl');return {gl:[c.width,c.height],dpr:devicePixelRatio}});
if(bufs.gl[0]!==renderWidth||bufs.gl[1]!==renderWidth*16/9)throw Error('native buffer mismatch: '+JSON.stringify(bufs));
async function capture(t,type='image/jpeg',q=.96){
  const d=await page.evaluate(({t,type,q})=>{window.render(t);return document.querySelector('#gl').toDataURL(type,q)},{t,type,q});
  return Buffer.from(d.split(',')[1],'base64');
}
timer.start('capture',{bufs});
if(mode==='stills'){
  const times=args.times?String(args.times).split(',').map(Number):[0,3,6,9,12,16,20,24,28,32,35];
  const samples=[];
  for(const t of times){const b=await capture(t,renderWidth===1080?'image/png':'image/jpeg');fs.writeFileSync(path.join(out,String(t).replace('.','_')+'.png'),b);
    samples.push({t,hash:hash(b)});timer.progress({still:t});console.log('still '+t)}
  timer.start('seek_check');
  const seek=[];for(const t of times.slice(0,3).reverse())seek.push({t,hash:hash(await capture(t,'image/png'))});
  const exact=seek.every(x=>x.hash===samples.find(y=>y.t===x.t).hash);
  fs.writeFileSync(path.join(out,'checks.json'),JSON.stringify({errors,bufs,seek,randomAccessIdentical:exact,samples},null,2));
  if(!exact||errors.length)throw Error('seek or runtime failed: '+errors.join('|'));
}else{
  const dur=Number(args.duration||36),fps=mode==='preview'?12:24,count=Math.round(dur*fps);
  const frames=path.join(out,'frames');fs.mkdirSync(frames,{recursive:true});
  const sigFiles=['index.html','js/main.js','js/timeline.js','js/scene.js','js/heron.js','js/lib.js','engine/carve.js','engine/gl.js'];
  const signature=hash(Buffer.concat(sigFiles.filter(f=>fs.existsSync(f)).map(f=>fs.readFileSync(f))));
  const config={signature,dur,fps,width:renderWidth,count};const cp=path.join(out,'config.json');
  if(fs.existsSync(cp)&&JSON.stringify(JSON.parse(fs.readFileSync(cp)))!==JSON.stringify(config))throw Error('source changed: use a new --version');
  fs.writeFileSync(cp,JSON.stringify(config));
  for(let i=0;i<count;i++){
    const p=path.join(frames,String(i).padStart(5,'0')+'.jpg');
    if(!fs.existsSync(p))fs.writeFileSync(p,await capture(i/fps,'image/jpeg',.97));
    if(i%48===0||i===count-1){timer.progress({frame:i+1,count});fs.writeFileSync(path.join(out,'progress.json'),JSON.stringify({frame:i+1,count}));console.log(`${mode} ${i+1}/${count}`)}
    if(errors.length)throw Error(errors.join('\n'));
  }
  await browser.close();browser=null;timer.start('encode');
  const video=path.join(out,'video.mp4');
  await run(FF,['-hide_banner','-loglevel','error','-y','-framerate',String(fps),'-i',path.join(frames,'%05d.jpg'),
    '-i','audio/mix.wav','-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p',
    '-threads:v','2','-c:a','aac','-b:a','192k','-ar','48000','-t',String(dur),'-movflags','+faststart',video]);
  timer.start('media_validation');
  const probe=JSON.parse(await run(FP,['-v','error','-show_streams','-show_format','-of','json',video]));
  fs.writeFileSync(path.join(out,'ffprobe.json'),JSON.stringify(probe,null,2));
  await run(FF,['-v','error','-i',video,'-map','0:v:0','-map','0:a:0','-c:v','rawvideo','-threads:v','1','-c:a','pcm_s16le','-f','null','-']);
  const v=probe.streams.find(x=>x.codec_type==='video'),a=probe.streams.find(x=>x.codec_type==='audio');
  if(+v.nb_frames!==count||+v.width!==renderWidth||!a)throw Error('media mismatch');
  const ev={...config,video,sha256:hash(fs.readFileSync(video)),decoded:true,errors,frames:+v.nb_frames};
  fs.writeFileSync(path.join(out,'evidence.json'),JSON.stringify(ev,null,2));
  console.log('COMPLETE '+JSON.stringify(ev));
}
completed=true;
}finally{timer.finish(completed?'complete':'failed');if(browser)await browser.close();await new Promise(r=>server.close(r))}
