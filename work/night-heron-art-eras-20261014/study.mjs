import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
import {chromium} from '../sand-journey-20261010/node_modules/playwright-core/index.mjs';
const root=new URL('.',import.meta.url); const out=new URL('research/',root); fs.mkdirSync(out,{recursive:true});
const ff='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe';
const input='D:/ai项目/ai动画/VibeVideo项目/reference-sources/upstream-videos/huashu-art-motion/art-motion-35-styles.mp4';
const times=Array.from({length:35},(_,i)=>+(i*1.171875+.65).toFixed(3));
const windows=[1.05,1.15,1.25,1.35,1.45,1.55];
let cards=[];
for(const [i,t] of [...times,...windows].entries()){
 const f=new URL(`${i}.jpg`,out);const r=spawnSync(ff,['-v','error','-y','-ss',String(t),'-i',input,'-frames:v','1','-vf','scale=320:180',decodeURIComponent(f.pathname).replace(/^\//,'')],{windowsHide:true});
 if(r.status)throw Error(r.stderr.toString());
 cards.push(`<figure><img src="data:image/jpeg;base64,${fs.readFileSync(f).toString('base64')}"><figcaption>${t}s</figcaption></figure>`);
}
const b=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
const p=await b.newPage({viewport:{width:1360,height:2300}});
await p.setContent(`<style>body{margin:8px;background:#222;color:white;font:16px sans-serif;display:grid;grid-template-columns:repeat(4,320px);gap:12px}figure{margin:0}img{width:320px;height:180px}figcaption{height:22px}</style>${cards.join('')}`);
await p.screenshot({path:decodeURIComponent(new URL('contact.jpg',out).pathname).replace(/^\//,''),fullPage:true});await b.close();
fs.writeFileSync(new URL('coverage.json',out),JSON.stringify({input,times,transitionWindow:windows,sourceSize:[1920,1080],readSize:[320,180],mode:'sampled stills and six-frame transition sequence; no realtime playback or listening',sourceDuration:41.25,fps:24},null,2));
console.log('research/contact.jpg created');
