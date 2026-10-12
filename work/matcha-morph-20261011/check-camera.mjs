import fs from 'node:fs';
import {createRequire} from 'node:module';
import {createServer} from './server.mjs';
const require=createRequire('C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/package.json');
const {chromium}=require('playwright-core');
const server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try {
 browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage();await page.goto(`http://127.0.0.1:${server.address().port}/?render`);await page.waitForFunction(()=>window.ready);
 const result=await page.evaluate(()=>{
  const frames=Array.from({length:150},(_,i)=>{const s=window.stateAt(i/30),c=s.camera,l=s.leaf;
   const project=([x,y])=>[270+(x-c.x)*c.zoom,450+(y-c.y)*c.zoom];
   const points=[...s.leafContour,[0,204]].map(([x,y])=>project([l.x+(x*Math.cos(l.rot)-y*Math.sin(l.rot))*l.scale,l.y+(x*Math.sin(l.rot)+y*Math.cos(l.rot))*l.scale]));
   return {frame:i,camera:c,anchor:project([l.x,l.y]),bounds:{left:Math.min(...points.map(p=>p[0])),right:Math.max(...points.map(p=>p[0])),top:Math.min(...points.map(p=>p[1])),bottom:Math.max(...points.map(p=>p[1]))}};
  });
  const violations=frames.filter(f=>Object.values(f.bounds).some(v=>!Number.isFinite(v))||f.bounds.left<40||f.bounds.right>500||f.bounds.top<140||f.bounds.bottom>720);
  const maxAnchorStep=Math.max(...frames.slice(1).map((f,i)=>Math.hypot(f.anchor[0]-frames[i].anchor[0],f.anchor[1]-frames[i].anchor[1])));
  return {framesChecked:150,violations,maxAnchorStep,first:frames[0],last:frames[149],technicalOnly:true};
 });
 fs.mkdirSync('qa/r3',{recursive:true});fs.writeFileSync('qa/r3/camera-check.json',JSON.stringify(result,null,2));
 console.log(JSON.stringify(result));if(result.violations.length||result.maxAnchorStep>8)throw Error('Camera framing discontinuity');
} finally {if(browser)await browser.close();await new Promise(r=>server.close(r));}
