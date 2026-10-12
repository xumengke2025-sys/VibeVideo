import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath, pathToFileURL} from 'node:url';

const require = createRequire(import.meta.url);
const {chromium} = require('C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core');
const out = path.dirname(fileURLToPath(import.meta.url));
const catalog = JSON.parse(fs.readFileSync(path.join(out,'catalog.json'),'utf8'));
const browser = await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
const page = await browser.newPage({viewport:{width:1280,height:900}});
const errors=[];
page.on('pageerror', e => errors.push(e.message));
try {
 await page.goto(pathToFileURL(path.join(out,'index.html')).href);
 const count = await page.locator('.clip').count();
 if (count!==catalog.media.length) throw new Error('Video count mismatch');
 await page.selectOption('#kind','外部原片');
 if (await page.locator('.clip:visible').count()!==8) throw new Error('Original filter failed');
 await page.fill('#search','twoclipping');
 if (await page.locator('.clip:visible').count()!==1) throw new Error('Search failed');
 await page.fill('#search','');
 const metadata = await page.evaluate(async () => {
  const nodes=[...document.querySelectorAll('.clip')].filter(n=>n.dataset.kind==='外部原片');
  const results=[];
  for (const n of nodes) {
   const video=n.querySelector('video');
   results.push(await new Promise(resolve=>{
    const timer=setTimeout(()=>resolve({title:n.querySelector('h3').textContent,error:'Metadata timeout'}),10000);
    video.addEventListener('loadedmetadata',()=>{clearTimeout(timer);resolve({title:n.querySelector('h3').textContent,width:video.videoWidth,height:video.videoHeight,duration:video.duration})},{once:true});
    video.addEventListener('error',()=>{clearTimeout(timer);resolve({title:n.querySelector('h3').textContent,error:video.error?.message || 'Media error'})},{once:true});
    video.preload='metadata';video.load();
   }));
  }
  return results;
 });
 if (metadata.some(m=>m.error)) throw new Error(JSON.stringify(metadata));
 await page.screenshot({path:path.join(out,'desktop.png'),fullPage:false});
 await page.setViewportSize({width:390,height:844});
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
 if (overflow) throw new Error('Mobile horizontal overflow');
 await page.screenshot({path:path.join(out,'mobile.png'),fullPage:false});
 if (errors.length) throw new Error(JSON.stringify(errors));
 const evidence={checked:'2026-10-10',videos:count,originalFilter:8,search:true,mobileOverflow:false,pageErrors:errors,originalMetadata:metadata,visualReviewPerformed:false};
 fs.writeFileSync(path.join(out,'verification.json'),JSON.stringify(evidence,null,2));
 console.log(JSON.stringify(evidence));
} finally {await browser.close()}
