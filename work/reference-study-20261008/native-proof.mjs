// Local verification harness for mexicat/pdoom-video, not an original video.
import { createRequire } from 'node:module';
import { spawn, spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const app = process.env.PDOOM_APP ?? 'C:/CodexTemp/pdoom-review-20261008/app';
const { chromium } = createRequire(path.join(app, 'package.json'))('playwright-core');
const out = 'D:/ai项目/ai动画/work/reference-study-20261008';
const ffmpeg = 'D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe';
const qualityOnly = process.argv.includes('--quality-check');
mkdirSync(path.join(out, 'native-frames'), { recursive: true });
mkdirSync(path.join(out, 'native-stills'), { recursive: true });
const server = spawn(process.execPath, [path.join(app, 'node_modules/vite/bin/vite.js'), '--host', '127.0.0.1', '--port', '8913', '--strictPort'], { cwd: app, windowsHide: true, env: {...process.env, PDOOM_NO_HMR:'1'}, stdio: ['ignore', 'pipe', 'pipe'] });
let serverLog = '';
server.stderr.on('data', b => { serverLog += b.toString(); });
let browser;
const errors = [];
const resourceFailures = [];
try {
  let reachable = false;
  for (let i=0; i<80; i++) {
    try { reachable = (await fetch('http://127.0.0.1:8913/')).ok; } catch {}
    if (reachable) break;
    await new Promise(r=>setTimeout(r,250));
  }
  if (!reachable) throw new Error('Private Vite did not start: ' + serverLog);
  browser = await chromium.launch({ executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe', headless:true, args:['--use-angle=d3d11','--enable-gpu-rasterization','--disable-background-timer-throttling'] });
  const page = await browser.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1});
  page.on('pageerror', e => errors.push({text:e.message,url:''}));
  page.on('console', m => { if(m.type()==='error') errors.push({text:m.text(),url:m.location().url}); });
  page.on('response', r => { if(r.status() >= 400) resourceFailures.push({url:r.url(),status:r.status()}); });
  await page.goto('http://127.0.0.1:8913/?export=1&only=loss,shoggoth');
  await page.waitForFunction(()=>window.__pdoom?.ready || window.__pdoom?.error,null,{timeout:60000});
  const status = await page.evaluate(()=>({error:window.__pdoom.error,errors:window.__pdoom.errors,timeline:window.__pdoom.timeline,width:window.__pdoom.width,height:window.__pdoom.height}));
  if(status.error || status.errors.length) throw new Error(JSON.stringify(status));
  if(qualityOnly) {
    mkdirSync(path.join(out,'quality-stills'),{recursive:true});
    const measurements = [];
    for(const samples of [4,36]) {
      const started = performance.now();
      await page.evaluate(samples=>window.__pdoom.still(11,samples,0.2),samples);
      measurements.push({samples,render_call_ms:Math.round(performance.now()-started)});
      await page.screenshot({path:path.join(out,'quality-stills',`source-11s-${samples}samples.png`),clip:{x:0,y:0,width:1920,height:1080}});
    }
    const meaningfulErrors = errors.filter(e=>!e.url.endsWith('/favicon.ico'));
    writeFileSync(path.join(out,'quality-proof.json'),JSON.stringify({source:'mexicat/pdoom-video',commit:'fa164b74fd0b26a99375715b619c55b4a0fb3d05',time:11,shutter:0.2,measurements,resourceFailures,browserErrors:errors,meaningfulErrors,sceneErrors:status.errors},null,2));
    console.log(JSON.stringify({measurements,resourceFailures,browserErrors:errors,meaningfulErrors}));
    if(meaningfulErrors.length) throw new Error(JSON.stringify(meaningfulErrors));
  } else {
  for(const t of [10,11,12,14,32]) {
    await page.evaluate(t=>window.__pdoom.still(t,4,0.2),t);
    await page.screenshot({path:path.join(out,'native-stills',`source-${t.toFixed(2)}s.png`),clip:{x:0,y:0,width:1920,height:1080}});
  }
  console.log('Native representative stills saved; rendering source loss excerpt', JSON.stringify(status));
  for(let n=0;n<120;n++) {
    await page.evaluate(t=>window.__pdoom.still(t,4,0.2),10+n/30);
    await page.screenshot({path:path.join(out,'native-frames',`${String(n).padStart(5,'0')}.png`),clip:{x:0,y:0,width:1920,height:1080}});
    if(n%30===0) console.log('Rendered frame',n);
  }
  const encoded = spawnSync(ffmpeg,['-hide_banner','-loglevel','error','-y','-framerate','30','-i',path.join(out,'native-frames','%05d.png'),'-c:v','libx264','-threads:v','1','-x264-params','threads=1:lookahead_threads=1','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',path.join(out,'pdoom-native-loss-study.mp4')],{encoding:'utf8',windowsHide:true});
  if(encoded.status!==0) throw new Error(encoded.stderr);
  const meaningfulErrors = errors.filter(e=>!e.url.endsWith('/favicon.ico'));
  if(meaningfulErrors.length) throw new Error(JSON.stringify(meaningfulErrors));
  writeFileSync(path.join(out,'native-proof.json'),JSON.stringify({source:'https://github.com/mexicat/pdoom-video',commit:'fa164b74fd0b26a99375715b619c55b4a0fb3d05',kind:'Original source reproduced for analysis; not authored by Codex',original_times_seconds:[10,14],fps:30,frames:120,size:[1920,1080],samples:4,shutter:0.2,audio:false,scene_errors:status.errors,browser_errors:errors,timeline:status.timeline},null,2));
  console.log('Native source excerpt complete');
  }
} finally {
  if(browser) await browser.close();
  server.kill();
}

