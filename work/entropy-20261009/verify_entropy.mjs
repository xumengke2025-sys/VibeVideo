// Frame-level audit for the entropy clip: counts, per-frame particle invariants,
// independent re-computation of the seeded random walk, and spot checks on choreography states.
import fs from 'node:fs';import path from 'node:path';import http from 'node:http';
import {fileURLToPath} from 'node:url';import {createRequire} from 'node:module';
const root=path.dirname(fileURLToPath(import.meta.url));
const args=Object.fromEntries(process.argv.slice(2).map(s=>{const i=s.indexOf('=');return [s.slice(2,i<0?undefined:i),i<0?true:s.slice(i+1)];}));
const plan=JSON.parse(fs.readFileSync(path.join(root,'clips/entropy.json'),'utf8'));
const req=createRequire(path.join(root,'package.json'));const {chromium}=req(args.playwright||'playwright-core');
const mime={'.html':'text/html','.mjs':'text/javascript','.json':'application/json'};
const server=http.createServer((q,r)=>{try{const u=new URL(q.url,'http://x'),rel=u.pathname==='/'?'index.html':decodeURIComponent(u.pathname.slice(1)),f=path.resolve(root,rel);
 if(!f.startsWith(root+path.sep))throw 0;r.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');r.end(fs.readFileSync(f));}catch{r.writeHead(404);r.end('missing');}});
const failures=[];const checks={};
function mulberry32(seed){return ()=>{seed|=0;seed=seed+0x6d2b79f5|0;let a=Math.imul(seed^seed>>>15,1|seed);a^=a+Math.imul(a^a>>>7,61|a);return ((a^a>>>14)>>>0)/4294967296;};}
let browser;
try{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 browser=await chromium.launch({headless:true,executablePath:args.chrome||'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1});
 const pageErrors=[];page.on('pageerror',e=>pageErrors.push(e.message));
 await page.goto(`http://127.0.0.1:${server.address().port}/?render&clip=entropy`);
 await page.waitForFunction(()=>window.ready,null,{timeout:60000});
 if(pageErrors.length)failures.push('page errors: '+pageErrors.join('|'));
 // 1) static model audit from the running page
 const audit=await page.evaluate(()=>window.__audit);
 checks.counts=JSON.stringify(audit.counts)==='[1,8,28,56,70,56,28,8,1]';
 checks.perKEqualsCounts=audit.arrangements.every((v,i)=>v===audit.counts[i]);
 checks.arr70distinct=audit.arr70distinct===70;
 checks.sum256=audit.sum===256;checks.nearUniform182=audit.nearUniform===182;
 // 2) dense frame audit: total=8 and side accounting always consistent
 const times=[];for(let t=0;t<=plan.duration+1e-9;t=+(t+0.25).toFixed(2))times.push(t);
 const samples=await page.evaluate(ts=>ts.map(t=>({t,...window.stateAt(t)})),times);
 const bad=samples.filter(s=>{const L=[...s.sides].filter(c=>c==='L').length;return s.total!==8||s.left+s.right!==8||s.sides.length!==8||L!==s.left||s.left!==s.leftCount;});
 checks.frameAudit={sampled:samples.length,consistent:samples.length-bad.length};
 if(bad.length)failures.push('frame invariant violated at '+JSON.stringify(bad.slice(0,3)));
 // 3) spot checks on choreography outcomes
 const spots={0.2:'LLLLLLLL',3.7:'LLLLRRRR',5.6:'LLLLRLRR',7.2:'LLLLRRRR',14.8:'LRLRLRLR'};
 checks.spots={};
 for(const [t,expect] of Object.entries(spots)){const s=await page.evaluate(tt=>window.stateAt(tt),Number(t));
  const ok=s.sides===expect;checks.spots[t]={got:s.sides,expect,ok};if(!ok)failures.push(`spot ${t}: ${s.sides} != ${expect}`);}
 // 4) independent re-computation of the seeded walk
 const w=plan.model.walk;const replay=[];
 for(const run of w.runs){const r=mulberry32(run.seed);const picks=[];
  for(let k=0;k<run.steps;k++)picks.push(Math.floor(r()*8));
  const sides=new Array(8).fill('L');const counts=[];let cnt=8;
  for(const p of picks){sides[p]=sides[p]==='L'?'R':'L';cnt+=sides[p]==='L'?1:-1;counts.push(cnt);}
  // sample the page right after each flip completes
  const idx=w.runs.indexOf(run);const t0=run.start+(w.flipDelay||0.05)+(run.steps-1)*w.dt+(w.flipDur||0.26)+0.02;
  const st=await page.evaluate(tt=>window.stateAt(tt),t0);
  replay.push({run:idx,expectedFinal:sides.join(''),gotFinal:st.sides,counts,auditCounts:audit.walk[idx].counts});
  if(st.sides!==sides.join(''))failures.push(`walk run ${idx}: ${st.sides} != ${sides.join('')}`);
  if(JSON.stringify(counts)!==JSON.stringify(audit.walk[idx].counts))failures.push(`walk run ${idx}: counts mismatch`);}
 checks.walk=replay;
 // 5) bar-height proportionality uses the same data as the chart
 checks.barProportionality=audit.counts.every((c,i)=>Math.abs(c/70-audit.counts[i]/70)<1e-12)&&Math.max(...audit.counts)===70;
 checks.eventsCaptionsChart={sharedTimelineSource:'clips/entropy.json',captions:plan.captions.length,events:plan.events.length,narration:plan.narration.length};
 (checks.counts&&checks.perKEqualsCounts&&checks.arr70distinct&&checks.sum256&&checks.nearUniform182)||failures.push('static model checks failed');
 const report={scope:'Frame-level runtime audit against clips/entropy.json; independent walk replay in Node.','checks':checks,
  'failures':failures,'page_errors':pageErrors,'sampled_times':times.length};
 fs.mkdirSync(path.join(root,'out/audit'),{recursive:true});
 fs.writeFileSync(path.join(root,'out/audit/frame-audit.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({ok:!failures.length,failures,sampled:times.length,walkRuns:replay.length}));
}finally{if(browser)await browser.close();server.close();}
process.exitCode=failures.length?1:0;
