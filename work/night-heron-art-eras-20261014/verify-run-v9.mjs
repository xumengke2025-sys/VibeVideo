import fs from 'node:fs';import path from 'node:path';import http from 'node:http';import{fileURLToPath}from'node:url';import{chromium}from'../sand-journey-20261010/node_modules/playwright-core/index.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),qa=path.join(root,'qa/run-v9-kinematics'),stateOnly=process.argv.includes('--state-only');fs.mkdirSync(qa,{recursive:true});
const plan=JSON.parse(fs.readFileSync(path.join(root,'production-plan-run-v9.json'))),errors=[],records=[];
const server=http.createServer((req,res)=>{try{const file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return}fs.statSync(file);res.setHeader('Content-Type',({'.js':'text/javascript','.html':'text/html','.json':'application/json','.png':'image/png'})[path.extname(file)]||'application/octet-stream');fs.createReadStream(file).pipe(res)}catch{res.writeHead(404).end()}});await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;try{
 browser=await chromium.launch({executablePath:'D:/Migrated/DevCache/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-win64/chrome-headless-shell.exe',headless:true});const page=await browser.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});page.on('pageerror',e=>errors.push(e.message));await page.goto(`http://127.0.0.1:${server.address().port}/run-v9.html?render`);await page.waitForFunction(()=>window.__ready,null,{timeout:120000});
 for(const [idx,sh] of plan.timeline.shots.entries()){
  const samples=[];for(let f=sh.startFrame;f<sh.endFrameExclusive;f+=2){await page.evaluate(t=>window.renderAt(t),f/24);samples.push(await page.evaluate(()=>window.__state));}
  const world=samples.map(s=>s.ownerWorldX),relative=samples.map(s=>s.ownerX-s.bank.shift),range=a=>Math.max(...a)-Math.min(...a);
  const patches=[];
  for(const dt of [-.10,.10,.30,.50,.70]){
   const t=(sh.startFrame+sh.events.grab)/24+dt;await page.evaluate(t=>window.renderAt(t),t);
   const patch=await page.evaluate(()=>{const s=window.__state,c=document.querySelector('canvas'),g=c.getContext('2d'),x=Math.round(s.ownerX-90),y=1425;if(x<0||x+30>1080)return null;return {x,y,pixels:Array.from(g.getImageData(x,y,24,24).data)};});if(patch)patches.push(patch);
   if(!stateOnly){const file=`era-${String(idx+1).padStart(2,'0')}-${dt.toFixed(2)}.png`;fs.writeFileSync(path.join(qa,file),await page.locator('canvas').screenshot());}
  }
  const pixelMAE=patches.slice(1).map(p=>p.pixels.reduce((v,c,k)=>v+Math.abs(c-patches[0].pixels[k]),0)/p.pixels.length);
  if(samples.some(s=>!Number.isFinite(s.ownerX)||!Number.isFinite(s.ownerWorldX)||![0,1,3,4].includes(s.ownerPose)||s.ownerFollow.headFacing!=='left'||Math.abs(s.ownerFollow.targetX-s.groundTarget.x)>1e-6||((s.local-sh.events.grab)/24>=.30&&s.ownerPose!==4)))throw Error('Ground reaction contract failed');
  const rec={era:idx+1,worldAnchorRange:range(world),bankRelativeRange:range(relative),poses:[...new Set(samples.map(s=>s.ownerPose))],groundPatchMAE:pixelMAE,states:samples};records.push(rec);console.log(JSON.stringify({era:rec.era,worldAnchorRange:rec.worldAnchorRange,bankRelativeRange:rec.bankRelativeRange,poses:rec.poses,groundPatchMAE:pixelMAE}));
  if(rec.worldAnchorRange>1e-6||rec.bankRelativeRange>1e-6)throw Error('Owner slipped relative to bank');
 }
 const seeks=[];for(const t of [3.91,12.55,25.73]){await page.evaluate(t=>window.renderAt(t),t);const a=await page.evaluate(()=>document.querySelector('canvas').toDataURL());await page.evaluate(()=>window.renderAt(29.9));await page.evaluate(t=>window.renderAt(t),t);seeks.push({t,identical:a===await page.evaluate(()=>document.querySelector('canvas').toDataURL())});}
 const owners=plan.timeline.shots.map(s=>s.owner);if(new Set(owners).size!==16)throw Error('Repeated owner species');
 const summary={eras:records.length,uniqueSpecies:new Set(owners).size,owners,sampleTimes:records.reduce((n,r)=>n+r.states.length,0),maxBankRelativeRange:Math.max(...records.map(r=>r.bankRelativeRange)),seeks,errors,coverage:'mechanical temporal sampling; selected production images; not independent AV review'};
 fs.writeFileSync(path.join(qa,'summary.json'),JSON.stringify(summary,null,2));
 fs.writeFileSync(path.join(qa,'verification.json'),JSON.stringify({records,...summary},null,2));if(errors.length||seeks.some(s=>!s.identical))throw Error('Runtime/seek check failed');
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
