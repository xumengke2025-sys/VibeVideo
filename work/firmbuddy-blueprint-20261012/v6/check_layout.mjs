import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium} from '../../sand-journey-20261010/node_modules/playwright-core/index.mjs';
import {createServer} from '../server.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;
const windows=[
 {range:[1.4,2.8],texts:['一句业务问题，启动专业协作','商机查询','业务答疑','拜访准备','自然语言 · 随时进入']},
 {range:[6.7,8.2],texts:['从信息中，筛出值得核实的线索','扩产相关披露','待核实','保留来源 · 再做研判']},
 {range:[14.9,16],texts:['数十位 AI 专家 · 按议题协作','投行业务','机构业务','财富业务','资管业务','国际业务','投资业务','期货与衍生品','行业研究','综合专家','产业链洞察','财务诊断','拜访策略']},
 {range:[23.9,25.5],texts:['知识库 · 已装配的专业资料','项目资料','研究资料','业务规范','交易结构','风险合规','案例档案','示例资料 · 扩产计划','资金安排未提供','先核实','资金来源与缺口','可见范围内检索 · 引用可回查']},
 {range:[33.7,34.6],texts:['把信息缺项，变成拜访提问','拜访策略包','资金怎么安排？','何时落地？谁参与决策？','目标 · 提问 · 话术材料','商机诊断','销售陪练','客户经营计划']},
 {range:[39.9,40.05],texts:['确认后，创建跟进任务','用户确认','跟进任务','待跟进','用户记录 → 更新商机判断']},
 {range:[49.3,51.8],texts:['FirmBuddy','把业务问题，变成有依据的行动','专家协作','知识库','方案与行动','记录反馈']}
];
try{
 browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--renderer-process-limit=1','--use-angle=d3d11','--enable-gpu','--ignore-gpu-blocklist']});
 const page=await browser.newPage({viewport:{width:1920,height:1080}});await page.goto(`http://127.0.0.1:${server.address().port}/v6/index.html?render`);await page.waitForFunction(()=>window.__ready);
 const issues=[],samples=[];
 for(const win of windows)for(let t=win.range[0];t<=win.range[1];t+=.3){
   const state=await page.evaluate(t=>window.stateAt(t),+t.toFixed(3));const sub=state.bounds.find(x=>x.id==='subtitle');
   for(const text of win.texts){const b=state.bounds.find(x=>x.text===text);if(!b){issues.push({t,text,kind:'missing_or_below_30px'});continue;}const [x,y,r,bottom]=b.box;if(x<80||y<48||r>1840||bottom>1020)issues.push({t,text,kind:'safe_area',box:b.box});if(sub){const a=sub.box;if(Math.min(r,a[2])>Math.max(x,a[0])&&Math.min(bottom,a[3])>Math.max(y,a[1]))issues.push({t,text,kind:'subtitle_overlap'});}}
   samples.push({t,subject_count:win.texts.length});
 }
 const result={scope:'Required text at declared reading windows, >=30 projected px; not all incidental technical annotations',windows,samples,issues};fs.writeFileSync(path.join(root,'../out/layout-v6.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({samples:samples.length,issues:issues.length,first:issues.slice(0,12)},null,2));
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
