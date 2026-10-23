import fs from 'node:fs';
import {createServer} from '../server.mjs';
import {chromium} from '../../sand-journey-20261010/node_modules/playwright-core/index.mjs';
const server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--renderer-process-limit=1']});
const page=await browser.newPage({viewport:{width:960,height:540}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
try{
 await page.goto(`http://127.0.0.1:${server.address().port}/v19/index.html?render&width=960`);await page.waitForFunction(()=>window.__ready,null,{timeout:60000});
 const data=await page.evaluate(()=>{
  const joins=window.design.cameraKeys.slice(1,-1).map(k=>{const t=k[0],h=.0001,a=window.cameraAt(t-h),b=window.cameraAt(t),c=window.cameraAt(t+h);return{time:t,positionGap:Math.hypot(c.x-a.x,c.y-a.y),velocityGap:Math.hypot((c.x-b.x)/h-(b.x-a.x)/h,(c.y-b.y)/h-(b.y-a.y)/h),zoomGap:Math.abs(c.z-a.z)};});
  const carrier=[];for(let t=20.8;t<113;t+=.2){const a=window.caseAt(t),c=window.cameraAt(t),dx=a.x-c.x,dy=a.y-c.y,x=960+(Math.cos(c.r)*dx-Math.sin(c.r)*dy)*c.z,y=540+(Math.sin(c.r)*dx+Math.cos(c.r)*dy)*c.z;if(x<100||x>1820||y<100||y>965)carrier.push({time:+t.toFixed(2),screen:[x,y]});}
  return{joins,carrier,readWindows:window.design.shots.map(s=>({time:s.start+Math.min(3,(s.end-s.start)/2),benefit:s.benefit})),dur:window.design.duration};
 });
 const report={...data,errors,pass:errors.length===0&&data.carrier.length===0&&data.joins.every(j=>j.positionGap<.5&&j.velocityGap<2&&j.zoomGap<.001)};
 fs.writeFileSync(new URL('./motion-checks.json',import.meta.url),JSON.stringify(report,null,2));console.log(JSON.stringify(report));
}finally{await browser.close();await new Promise(r=>server.close(r));}
