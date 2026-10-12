import fs from 'node:fs';import path from 'node:path';import{fileURLToPath}from'node:url';import{createRequire}from'node:module';import{createHash}from'node:crypto';import{spawn}from'node:child_process';import{createServer}from'./server.mjs';
import {phaseTimer} from '../../skill/vibe-video/scripts/render_phase_timer.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const args=Object.fromEntries(process.argv.slice(2).map(a=>{let[k,...v]=a.replace(/^--/,'').split('=');return[k,v.join('=')||true]}));
const runtime='C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const req=createRequire(path.join(runtime,'package.json')), {chromium}=req('playwright-core');
const ffmpeg=args.ffmpeg||'D:/ai项目/ai动画/VibeVideo项目/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe';
const probe=ffmpeg.replace('ffmpeg.exe','ffprobe.exe');const out=path.join(root,args.out||'out-preview-r1'),qa=path.join(root,'technical');
fs.mkdirSync(out,{recursive:true});fs.mkdirSync(qa,{recursive:true});
const timer=phaseTimer(out);timer.start('input_check');
const hash=x=>createHash('sha256').update(x).digest('hex');
const source=['film.mjs','index.html','timeline.json','audio.py','render.mjs','server.mjs','assets/paper-generated.png','assets/msyh-local.ttc','audio/preview.wav'].map(f=>({file:f,sha256:hash(fs.readFileSync(path.join(root,f)))}));
const evidence={source,errors:[],externalRequests:[],seek:[],technicalOnly:true,realtimeViewed:false,listened:false};
function run(binary,argv){timer.start(binary===probe?'probe':argv.includes('null')?'decode_validation':'encode');return new Promise((resolve,reject)=>{let so='',se='';const p=spawn(binary,argv,{windowsHide:true});p.stdout.on('data',x=>so+=x);p.stderr.on('data',x=>{se=(se+x).slice(-5000)});p.on('error',reject);p.on('close',code=>code===0?resolve(so):reject(Error(binary+' '+code+' '+se)))})}
const server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;let browser;
async function newPage(){const p=await browser.newPage({viewport:{width:540,height:960},deviceScaleFactor:1});p.on('pageerror',e=>evidence.errors.push(e.message));await p.route('**/*',r=>{if(!r.request().url().startsWith(origin+'/')){evidence.externalRequests.push(r.request().url());return r.abort()}return r.continue()});await p.goto(origin+'/?render');await p.waitForFunction(()=>window.ready,{timeout:30000});return p}
const capture=async(p,t,type='image/png')=>Buffer.from((await p.evaluate(({t,type})=>window.renderAt(t,type,.97,1),{t,type})).split(',')[1],'base64');
try{
 timer.start('browser_setup');
 browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});evidence.browser=browser.version();const p=await newPage();
 if(args.stills){
   timer.start('capture_stills');
   for(const kind of['leaf','mill','bowl']){const b=Buffer.from((await p.evaluate(k=>window.representativeAt(k,2),kind)).split(',')[1],'base64');const file=path.join(root,'representatives',kind+'.png');fs.writeFileSync(file,b);console.log('STILL '+file)}
 }else{
   timer.start('seek_check');
   const times=[0,.7,1.55,2,2.35,3.1,4.5,4.9666666667],forward={};
   for(const t of times)forward[t]=hash(await capture(p,t));for(const t of[...times].reverse())evidence.seek.push({time:t,forward:forward[t],reverse:hash(await capture(p,t))});
   const p2=await newPage();for(const e of evidence.seek)e.fresh=hash(await capture(p2,e.time));await p2.close();if(evidence.seek.some(e=>e.forward!==e.reverse||e.forward!==e.fresh))throw Error('Non-deterministic frame');
   const states=await p.evaluate(ts=>ts.map(t=>{window.renderAt(t);return{state:window.stateAt(t),render:window.inspectState()}}),times);
   for(const s of states){if(!s.render.fontReady||!s.render.textureReady)throw Error('Missing material/font');for(const b of s.render.captionBoxes)if(b.left<40||b.right>500||b.bottom>850||b.top<60)throw Error('Caption safe area exceeded: '+JSON.stringify(b));if(s.state.leafContour.some(p=>p.some(x=>!Number.isFinite(x))))throw Error('Invalid contour')}
   evidence.states=states;if(args.check){evidence.engineeringCheck=true;console.log('CHECK seek, fresh page, fonts and caption bounds passed')}else{const frames=path.join(out,'frames');fs.mkdirSync(frames,{recursive:true});
   const cfg={width:540,height:960,fps:30,frames:150,source};const cf=path.join(out,'inputs.json');if(fs.existsSync(cf)&&JSON.stringify(JSON.parse(fs.readFileSync(cf)))!==JSON.stringify(cfg))throw Error('Inputs changed: choose a new output directory');fs.writeFileSync(cf,JSON.stringify(cfg,null,2));
   timer.start('capture');for(let i=0;i<150;i++){const f=path.join(frames,String(i).padStart(5,'0')+'.jpg');if(!fs.existsSync(f))fs.writeFileSync(f,await capture(p,i/30,'image/jpeg'));if(i%30===0||i===149){timer.progress({frame:i+1,total:150});console.log('FRAME '+(i+1)+'/150');fs.writeFileSync(path.join(out,'progress.json'),JSON.stringify({phase:'capture',frame:i+1,total:150}))}}
   await browser.close();browser=null;
   timer.start('encode');const video=path.join(out,'matcha-steam-dry.mp4');await run(ffmpeg,['-hide_banner','-loglevel','error','-y','-f','image2','-framerate','30','-vcodec','mjpeg','-i',path.join(frames,'%05d.jpg'),'-i',path.join(root,'audio/preview.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p','-threads:v','2','-c:a','aac','-b:a','192k','-ar','48000','-t','5','-movflags','+faststart',video]);
   const info=JSON.parse(await run(probe,['-v','error','-count_frames','-show_streams','-show_format','-of','json',video]));fs.writeFileSync(path.join(out,'media.json'),JSON.stringify(info,null,2));const v=info.streams.find(s=>s.codec_type==='video'),a=info.streams.find(s=>s.codec_type==='audio');if(v.width!==540||v.height!==960||+v.nb_read_frames!==150||!a||Math.abs(+info.format.duration-5)>.05)throw Error('Unexpected media');
   await run(ffmpeg,['-hide_banner','-loglevel','error','-i',video,'-map','0:v:0','-map','0:a:0','-c:v','rawvideo','-threads:v','1','-c:a','pcm_s16le','-f','null','-']);
   evidence.output={path:video,sha256:hash(fs.readFileSync(video)),width:540,height:960,fps:30,decodedFrames:+v.nb_read_frames,duration:+info.format.duration,fullDecode:true,audio:a.codec_name,bytes:fs.statSync(video).size};
   fs.writeFileSync(path.join(out,'progress.json'),JSON.stringify({phase:'complete',frames:150}));console.log('COMPLETE '+JSON.stringify(evidence.output));
   }
 }
 if(evidence.errors.length||evidence.externalRequests.length)throw Error('Browser errors/requests');evidence.status='complete';
}catch(e){evidence.status='failed';evidence.failure=e.stack;throw e}finally{timer.finish(evidence.status==='complete'?'complete':'failed');fs.writeFileSync(path.join(out,args.stills?'still-evidence.json':'render-evidence.json'),JSON.stringify(evidence,null,2));if(browser)await browser.close();await new Promise(r=>server.close(r))}
