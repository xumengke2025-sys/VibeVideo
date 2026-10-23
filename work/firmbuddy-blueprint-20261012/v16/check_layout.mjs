import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const {chromium}=await import('../../sand-journey-20261010/node_modules/playwright-core/index.mjs').catch(()=>import('playwright-core'));import {createServer} from '../server.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;
const windows=[
{range:[3,8],texts:['商机收集耗时长','不知从何入手','信息归集不全','专业判断缺支持']},
{range:[12,13],texts:['商机查询','治理整改','并购重组','股东减持','风险管理','上市与分拆']},
{range:[29.2,31.2],texts:['资料归集：先看清同一家客户','股东服务线索','主体 · 事件 · 时间','原文依据 · 来源可追溯','AI 辅助解读客户线索']},
{range:[40,45],texts:['业务研判：这条线索，怎样跟进？','公司解禁窗口','公司 · 股东资料','股份管理安排','跟进重点：了解股份事务接口与服务需求']},
{range:[54,58],texts:['专业会商：这家客户应该怎样跟进？','专业培养的 AI 专家团 · 九大业务领域协作','投行业务','机构业务','财富业务','资管业务','国际业务','投资业务','期货与衍生品','行业研究','综合专家','股份管理需求','联系时机','服务切入点','A01 · 股东服务研判','专业知识装备','业务方法沉淀','培养与试炼']},
{range:[69.8,72.4],texts:['产业研判：更懂眼前这家客户','材料耗材','制造装备','晶体生长','衬底','外延','A01 · 本次客户','公司年报','专利原文','财务披露']},
{range:[81,82.4],texts:['回到同一客户：把依据带入服务判断','核心规范','监管规则','产品能力','案例经验','研究资料','补充资料','规则 · 案例 · 研究依据','了解股份管理安排']},
{range:[91.2,91.8],texts:['A01 · 客户沟通准备包','联系目的：了解股份管理安排','结合产业背景，准备沟通问题','AI 辅助整理材料与跟进建议','研判有结论','沟通有重点','跟进有计划']},
{range:[95.8,96],texts:['人工审核','A01 · 沟通记录','沟通需求 · 服务安排','跟进事项 · 经营进展','沟通记录支持持续跟进']},
{range:[101.2,103.6],texts:['FirmBuddy','商机发现有方向 · 业务研判有依据 · 客户跟进有准备']}
];const plan=JSON.parse(fs.readFileSync(path.join(root,'plan.json')));for(const q of plan.business_messages)windows.push({range:[q.start+.5,q.end-.5],texts:[q.pain,q.result]});
try{browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--renderer-process-limit=1','--use-angle=d3d11','--enable-gpu','--ignore-gpu-blocklist']});const page=await browser.newPage({viewport:{width:1920,height:1080}});await page.goto(`http://127.0.0.1:${server.address().port}/v16/index.html?render`);await page.waitForFunction(()=>window.__ready);const issues=[],samples=[];
for(const win of windows)for(let t=win.range[0];t<=win.range[1]+.001;t+=1){const st=await page.evaluate(t=>window.stateAt(t),t),selected=[];for(const text of win.texts){const b=st.bounds.find(x=>x.text===text&&x.box[0]>=0&&x.box[2]<=1920);if(!b){issues.push({t,text,kind:'missing'});continue;}const[x,y,r,bottom]=b.box;if(x<60||y<30||r>1860||bottom>1064)issues.push({t,text,kind:'safe_area',box:b.box});selected.push(b);}for(let i=0;i<selected.length;i++)for(let j=i+1;j<selected.length;j++){const a=selected[i].box,b=selected[j].box;if(Math.min(a[2],b[2])-Math.max(a[0],b[0])>3&&Math.min(a[3],b[3])-Math.max(a[1],b[1])>3)issues.push({t,kind:'text_overlap',texts:[selected[i].text,selected[j].text]});}samples.push(t);}
fs.writeFileSync(path.join(root,'layout-checks.json'),JSON.stringify({scope:'Declared business text in reading windows; excludes decorative text and intermediate transitions',windows,samples,issues},null,2));console.log(JSON.stringify({samples:samples.length,issues:issues.length,first:issues.slice(0,20)},null,2));if(issues.length)process.exitCode=1;
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
