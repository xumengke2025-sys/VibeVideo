import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium} from '../../sand-journey-20261010/node_modules/playwright-core/index.mjs';
import {createServer} from '../server.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),plan=JSON.parse(fs.readFileSync(path.join(root,'plan.json'))),server=createServer();
await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;
try{
 browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--renderer-process-limit=1','--use-angle=d3d11','--enable-gpu','--ignore-gpu-blocklist']});
 const page=await browser.newPage({viewport:{width:1920,height:1080}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(`http://127.0.0.1:${server.address().port}/v14/index.html?render`);await page.waitForFunction(()=>window.__ready);
 const samples=[],issues=[],burdenWindows=[];
 const mandatory=[
  [5,['业务人员的时间，被哪些负担占满？','资料分散','判断费力','专家难找','依据难找','准备重复','记录难接续']],
  [11,['商机查询','治理整改','并购重组','股东减持','风险管理','上市与分拆']],
  [21.8,['把分散线索，变成可跟进的客户机会','客户线索归集']],
  [39.6,['商机从哪里来，为什么值得跟进','融资','并购','股东服务','风险与跨境','融资预案','重组 / 收购公告','减持披露 / 解禁日历','套保 / 境外投资公告']],
  [52.8,['看清客户需求，找到服务切入点','客户需求与服务思路']],
  [67,['复杂业务研判，有专业依据可用','为业务判断补齐依据']],
  [77.4,['少做重复准备，多花精力服务客户','客户跟进准备包']],
  [83.4,['保留经营记录，后续跟进接得上','客户经营记录']],
  [89.5,['FirmBuddy','让商机有线索，研判有依据，跟进有准备','商机判断']]
 ];
 for(const [t,texts]of mandatory){const s=await page.evaluate(t=>window.stateAt(t),t);const chosen=[];
  for(const text of texts){const b=s.bounds.find(b=>b.text===text);if(!b){issues.push({t,text,kind:'missing'});continue;}chosen.push(b);if(b.box[0]<40||b.box[1]<20||b.box[2]>1880||b.box[3]>1070)issues.push({t,text,box:b.box,kind:'out_of_bounds'});}
  for(let i=0;i<chosen.length;i++)for(let j=i+1;j<chosen.length;j++){const a=chosen[i].box,b=chosen[j].box;if(Math.min(a[2],b[2])-Math.max(a[0],b[0])>4&&Math.min(a[3],b[3])-Math.max(a[1],b[1])>4)issues.push({t,kind:'text_overlap',texts:[chosen[i].text,chosen[j].text]});}
  samples.push({t,texts:chosen.length});
 }
 for(const b of plan.burdens){const states=[];for(const t of[b.end-1.3,b.end-.6,b.end+.1])states.push(await page.evaluate(t=>window.stateAt(t),t));if(states[0].burdens.length-states[2].burdens.length!==1)issues.push({burden:b.id,kind:'not_removed_once'});burdenWindows.push({id:b.id,end:b.end,counts:states.map(s=>s.burdens.length),hero:states.map(s=>s.hero)});}
 // Numerically inspect temporal continuity at the new detour and retiming joins.
 const joins=[];for(const t of[14,17,22,26,42,46,54,63,68,78,84,89]){const h=.0001;const poses=await page.evaluate(({t,h})=>[t-h,t,t+h].map(window.cameraAt),{t,h});const delta=Math.hypot(poses[2].x-poses[0].x,poses[2].y-poses[0].y);if(delta>1)issues.push({t,kind:'camera_position_jump',delta});joins.push({t,delta});}
 fs.writeFileSync(path.join(root,'../out/journey-v14-checks.json'),JSON.stringify({scope:'Declared text, each burden count transition and numerical camera continuity; not perceptual full-film review',samples,burdenWindows,joins,errors,issues},null,2));
 console.log(JSON.stringify({samples:samples.length,burdenWindows:burdenWindows.length,errors,issues},null,2));if(issues.length||errors.length)process.exitCode=1;
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
