import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium} from '../../sand-journey-20261010/node_modules/playwright-core/index.mjs';
import {createServer} from '../server.mjs';
const ROOT=path.dirname(fileURLToPath(import.meta.url));
const server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;
try{
  browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--use-angle=d3d11','--enable-gpu','--ignore-gpu-blocklist']});
  const page=await browser.newPage({viewport:{width:1920,height:1080}});
  await page.goto(`http://127.0.0.1:${server.address().port}/v4/index.html?render`);await page.waitForFunction(()=>window.__ready);
  const ranges=[[0,5.2],[9,14.3],[17,23.9],[25,35.9],[37,45.5],[48,54.8],[55.7,60.8],[64.5,67.9]];
  const states=[],issues=[];
  for(const [a,b] of ranges)for(let t=a;t<=b;t+=.25){
    const state=await page.evaluate(t=>window.stateAt(t),+t.toFixed(3));
    const visible=state.bounds.filter(({box:[x0,y0,x1,y1]})=>x1>0&&x0<1920&&y1>0&&y0<1080);
    for(const item of visible){
      const [x0,y0,x1,y1]=item.box;
      if(x0<96||y0<64||x1>1824||y1>1016)issues.push({kind:'safe_area',time:state.time,item});
    }
    const sub=visible.find(s=>s.id==='subtitle');
    if(sub)for(const item of visible.filter(s=>s.id!=='subtitle')){
      const a=item.box,b=sub.box;
      if(Math.min(a[2],b[2])>Math.max(a[0],b[0])&&Math.min(a[3],b[3])>Math.max(a[1],b[1]))issues.push({kind:'subtitle_overlap',time:state.time,item});
    }
    states.push({t:state.time,visible:visible.length});
  }
  const result={scope:'Registered fully revealed text >=30 screen px, during listed stationary/read windows. Not all geometry or full-frame visual review.',ranges,samples:states.length,issues};
  fs.writeFileSync(path.resolve(ROOT,'../out/layout-v4.json'),JSON.stringify(result,null,2));
  console.log(JSON.stringify({samples:states.length,issues:issues.length,first:issues.slice(0,8)},null,2));
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
