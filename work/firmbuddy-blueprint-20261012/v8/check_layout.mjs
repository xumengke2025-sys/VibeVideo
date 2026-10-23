import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium} from '../../sand-journey-20261010/node_modules/playwright-core/index.mjs';
import {createServer} from '../server.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;
const windows=[
 {range:[1.4,2.8],texts:['减持商机：更早发现，提前经营','减持商机查询','减持业务答疑','客户触达准备','自然语言 · 随时进入']},
 {range:[6.7,8.2],texts:['前置信号扫描，识别重点客户','减持前置信号','需求未确认','触达 / 观察 / 暂缓']},
 {range:[14.9,16],texts:['数十位 AI 专家 · 按议题协作','投行业务','机构业务','财富业务','资管业务','国际业务','投资业务','期货与衍生品','行业研究','综合专家','股东增减持','解禁预警','拜访策略']},
 {range:[23.9,25.5],texts:['知识库 · 已装配的专业资料','股东资料','信号规则','减持规范','触达策略','风险合规','案例档案','信号解释卡 · 示例','历史执行＋市场观察','客户分型','存量股东服务回访','前置信号 ≠ 已确认减持需求 · 引用可回查']},
 {range:[33.7,34.6],texts:['生成触达策略，把线索变成行动','触达策略包','何时联系？由谁触达？','怎么开场？哪些话不能说？','话术速查 · 合规边界 · 跟进建议','减持商机诊断','触达话术生成','客户经营计划']},
 {range:[39.9,40.05],texts:['人工确认后，加入商机中心','人工确认','商机中心','减持候选 · 待跟进','触达记录 → 更新减持商机判断']},
 {range:[49.3,51.8],texts:['FirmBuddy','更早发现减持线索，更好经营客户','专家协作','知识库','触达策略','记录反馈']}
];
try{
 browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--renderer-process-limit=1','--use-angle=d3d11','--enable-gpu','--ignore-gpu-blocklist']});
 const page=await browser.newPage({viewport:{width:1920,height:1080}});await page.goto(`http://127.0.0.1:${server.address().port}/v8/index.html?render`);await page.waitForFunction(()=>window.__ready);
 const issues=[],samples=[];
 for(const win of windows)for(let t=win.range[0];t<=win.range[1];t+=.3){
   const state=await page.evaluate(t=>window.stateAt(t),+t.toFixed(3));const sub=state.bounds.find(x=>x.id==='subtitle');
   for(const text of win.texts){const b=state.bounds.find(x=>x.text===text);if(!b){issues.push({t,text,kind:'missing_or_below_30px'});continue;}const [x,y,r,bottom]=b.box;if(x<80||y<48||r>1840||bottom>1020)issues.push({t,text,kind:'safe_area',box:b.box});if(sub){const a=sub.box;if(Math.min(r,a[2])>Math.max(x,a[0])&&Math.min(bottom,a[3])>Math.max(y,a[1]))issues.push({t,text,kind:'subtitle_overlap'});}}
   samples.push({t,subject_count:win.texts.length});
 }
 const result={scope:'Required text at declared reading windows, >=30 projected px; not all incidental technical annotations',windows,samples,issues};fs.writeFileSync(path.join(root,'../out/layout-v8.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({samples:samples.length,issues:issues.length,first:issues.slice(0,12)},null,2));
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
