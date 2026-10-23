import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url)),v=path.join(root,'v4');
const events=[
 ['signal',2,'bell','异常指针到位'],['bind',10,'lock','原文索引进入案件'],['edge',18,'lock','有据关系展开'],['expert',28,'bell','专家席位响应'],['knowledge',32,'scan','检索档案送出'],['conditions',36,'lock','条件记录就位'],['freeze',44,'lock','固定快照S-001'],['split',48,'relay','分发试验副本'],['copies',50,'lock','三个同源副本就位'],['assumptions',52,'drop','三种假设装入'],['run',54,'bell','在假设下启动推演'],['business',56,'relay','业务层示意响应'],['sentiment',58,'relay','舆情层示意响应'],['trace',60,'relay','比较条件下的路径'],['records',62,'lock','形成三份独立记录'],['record0',63.5,'relay','基准记录归入原案件'],['record1',63.75,'relay','不利记录归入原案件'],['collect',64,'lock','三份记录完成归档'],['archive',68,'lock','过程与依据存档'],['review',75,'resolve','带条件返回专家'],['reveal',78,'bell','全局闭环揭示']
].map(([id,at,sound,action],i)=>({id,at,sound,action,note:[62,69,74][i%3]}));
const rows=[
 ['signal',0,8,'发现异常，先找依据','一个信号点亮，采集机构响应'],
 ['evidence',8,16,'AI 整理线索，保留原文索引','来源装入同一个案件匣'],
 ['relations',16,24,'有据连接，保留待核实的关系','关系先核实，潜在路径不等于必然传导'],
 ['experts',24,32,'专业知识与方法，支撑专家会商','知识档案与相关席位响应'],
 ['conditions',32,40,'共同依据、保留分歧、明确假设','检索依据进入会商，假设记录随案件出发'],
 ['snapshot',40,48,'固定同一份证据与初始状态','夹具固定S-001，再解锁分发'],
 ['assumptions',48,54,'同一快照，只改变情景假设','分发试验副本，在52秒装入差异假设'],
 ['simulation',54,62,'在假设下比较可能路径，不是预测','业务与舆情示意分步响应，保留未触达支路'],
 ['records',62,69,'三份情景记录，回到同一个案件','记录归档；不合并为确定性结论'],
 ['review',69,76,'带着条件与疑点，返回专家复核','原案件携带记录，形成核查和监测事项'],
 ['reveal',76,80,'有据研判 · 情景推演 · 持续跟踪','拉远揭示完整闭环']
];
const plan={title:'Risky · 证据不变，假设改变',version:'v4',duration:80,fps:30,width:1920,height:1080,aspect_ratio:'16:9',delivery_mode:'ai_review_once',review_budget_used:true,shots:rows.map(([id,start,end,caption,action])=>({id,start,end,caption,action})),events,soundtrack:{sample_rate:48000,bpm:120,beat:.5,bars_per_phrase:4,phrases:Array.from({length:10},(_,i)=>({start:i*8,end:(i+1)*8,beats:16})),events},disclosure:'合成案例 · 假设推演示意，非预测结果'};
fs.writeFileSync(path.join(v,'plan.json'),JSON.stringify(plan,null,2));
fs.writeFileSync(path.join(v,'film.js'),fs.readFileSync(path.join(v,'primitives.js.txt'),'utf8').replace(/^\uFEFF/,'')+'\n'+fs.readFileSync(path.join(v,'scene-body.js'),'utf8'));
console.log('Built V4 from shared beat/action timeline');
