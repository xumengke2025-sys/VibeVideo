import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium} from '../../sand-journey-20261010/node_modules/playwright-core/index.mjs';
import {createServer} from '../server.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;
const windows=[
 {range:[1.4,2.8],texts:['减持商机：更早发现，提前经营','减持商机查询','业务问题答疑','客户拜访准备','AI 理解问题 · 调用专业工具']},
 {range:[6.7,8.2],texts:['规则扫描前置信号，AI 解读线索','减持前置信号','AI 解读：重点客户','触达 / 观察 / 暂缓']},
 {range:[14.9,16],texts:['专业培养的 AI 专家团 · 按议题协作','投行业务','机构业务','财富业务','资管业务','国际业务','投资业务','期货与衍生品','行业研究','综合专家','股东增减持','解禁预警','拜访策略','AI 汇总多专业研判','专业知识装备','业务方法沉淀','培养与试炼']},
 {range:[23.9,25.5],texts:['多源知识库 · 专家专业能力底座','核心规范','监管规则','产品能力','案例经验','研究资料','补充资料','AI 检索 · 交叉查证','历史执行＋市场观察','AI 辅助客户分型','存量股东服务回访','规则依据 · 业务经验 · 原文引用']},
 {range:[33.7,34.6],texts:['AI 生成触达策略，把线索变成行动','触达策略包','联系时机 · 负责人建议','开场话术 · 沟通重点','话术速查 · 合规要点 · 跟进节奏','减持商机诊断','触达话术生成','客户经营计划']},
 {range:[39.9,40.05],texts:['人工审核入库，持续经营客户','人工审核','商机中心','减持线索 · 客户经营','触达准备 · 跟进服务','触达记录 → AI 辅助复评']},
 {range:[49.3,51.8],texts:['FirmBuddy','专业知识驱动，让 AI 贯穿客户经营','专业专家团','知识装备库','触达策略','记录反馈']}
];
try{
 browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--renderer-process-limit=1','--use-angle=d3d11','--enable-gpu','--ignore-gpu-blocklist']});
 const page=await browser.newPage({viewport:{width:1920,height:1080}});await page.goto(`http://127.0.0.1:${server.address().port}/v9/index.html?render`);await page.waitForFunction(()=>window.__ready);
 const issues=[],samples=[];
 for(const win of windows)for(let t=win.range[0];t<=win.range[1];t+=.3){
   const state=await page.evaluate(t=>window.stateAt(t),+t.toFixed(3));const sub=state.bounds.find(x=>x.id==='subtitle');
   for(const text of win.texts){const b=state.bounds.find(x=>x.text===text);if(!b){issues.push({t,text,kind:'missing_or_below_30px'});continue;}const [x,y,r,bottom]=b.box;if(x<80||y<48||r>1840||bottom>1020)issues.push({t,text,kind:'safe_area',box:b.box});if(sub){const a=sub.box;if(Math.min(r,a[2])>Math.max(x,a[0])&&Math.min(bottom,a[3])>Math.max(y,a[1]))issues.push({t,text,kind:'subtitle_overlap'});}}
   samples.push({t,subject_count:win.texts.length});
 }
 const result={scope:'Required text at declared reading windows, >=30 projected px; not all incidental technical annotations',windows,samples,issues};fs.writeFileSync(path.join(root,'../out/layout-v9.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({samples:samples.length,issues:issues.length,first:issues.slice(0,12)},null,2));
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
