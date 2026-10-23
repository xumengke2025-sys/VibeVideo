import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium} from '../../sand-journey-20261010/node_modules/playwright-core/index.mjs';
import {createServer} from '../server.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;
const windows=[
{range:[1.5,3.2],texts:['商机收集耗时长','不知从何入手','专业支持难找','跟进准备重复']},
{range:[4.9,6.3],texts:['商机查询','治理整改','并购重组','股东减持','风险管理','上市与分拆']},
{range:[15.6,16.1],texts:['把分散资料，归集为客户线索','客户线索档案','减持商机示例','AI 解读信号与客户情况','重点客户 · 研判依据']},
{range:[22.5,23.9],texts:['业务研判：需求、时机与服务切入点','专业培养的 AI 专家团 · 九大业务领域协作','投行业务','机构业务','财富业务','资管业务','国际业务','投资业务','期货与衍生品','行业研究','综合专家','客户需求','联系时机','服务切入点','AI 汇总专业判断','专业知识装备','业务方法沉淀','培养与试炼']},
{range:[32,33.4],texts:['专业问题，有知识依据与多专业支持','核心规范','监管规则','产品能力','案例经验','研究资料','补充资料','AI 检索 · 交叉查证','规则 · 案例 · 研究依据','AI 关联客户与服务','存量股东服务回访']},
{range:[41.7,42.5],texts:['减少重复准备，让研判落到客户跟进','客户跟进准备包','联系时机 · 服务切入点','开场话术 · 沟通重点','拜访材料 · 合规要点 · 跟进节奏','研判有结论','沟通有重点','跟进有计划']},
{range:[47.8,48],texts:['保留经营记录，后续跟进接得上','人工审核','客户经营记录','沟通需求 · 服务安排','触达记录 → AI 辅助复评']},
{range:[57.3,59.7],texts:['FirmBuddy','找得到机会，讲得清服务，跟得住客户','专业研判','知识依据','跟进准备','持续经营']}
];
const plan=JSON.parse(fs.readFileSync(path.join(root,'plan.json')));
for(const q of plan.business_messages)windows.push({range:[q.start+.4,q.end-.4],texts:[q.pain,q.result],step:1});
try{
browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--renderer-process-limit=1','--use-angle=d3d11','--enable-gpu','--ignore-gpu-blocklist']});
const page=await browser.newPage({viewport:{width:1920,height:1080}});await page.goto(`http://127.0.0.1:${server.address().port}/v12/index.html?render`);await page.waitForFunction(()=>window.__ready);
const issues=[],samples=[];
for(const win of windows)for(let t=win.range[0];t<=win.range[1];t+=win.step||.4){
 const state=await page.evaluate(t=>window.stateAt(t),+t.toFixed(3));const selected=[];
 for(const text of win.texts){const b=state.bounds.find(x=>x.text===text);if(!b){issues.push({t,text,kind:'missing_or_below_30px'});continue;}const [x,y,r,bottom]=b.box;const footer=plan.business_messages.some(q=>q.result===text);if(x<72||y<32||r>1848||bottom>(footer?1064:1010))issues.push({t,text,kind:'safe_area',box:b.box});selected.push(b);}
 for(let i=0;i<selected.length;i++)for(let j=i+1;j<selected.length;j++){const a=selected[i].box,b=selected[j].box;if(Math.min(a[2],b[2])-Math.max(a[0],b[0])>3&&Math.min(a[3],b[3])-Math.max(a[1],b[1])>3)issues.push({t,kind:'text_overlap',texts:[selected[i].text,selected[j].text]});}
 samples.push({t,texts:win.texts.length});
}
fs.writeFileSync(path.join(root,'../out/layout-v12.json'),JSON.stringify({scope:'Declared business text at reading windows; not all decorative text or every frame',windows,samples,issues},null,2));console.log(JSON.stringify({samples:samples.length,issues:issues.length,first:issues.slice(0,15)},null,2));if(issues.length)process.exitCode=1;
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
