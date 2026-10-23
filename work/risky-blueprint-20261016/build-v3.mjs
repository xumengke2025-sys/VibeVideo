import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url)),v=path.join(root,'v3');
const shots=[
 ['signal',0,6,'风险研判，从一个信号开始','指针偏转，采集响应'],
 ['evidence',6,16,'AI 汇集线索，证据定位到原文','来源比对，装入案件匣'],
 ['relations',16,26,'看清关联，识别潜在传导','关系臂展开，证据保留'],
 ['experts',26,40,'专业知识支撑，多专家协同研判','检索档案，激活相关席位，形成条件'],
 ['snapshot',40,46,'固定证据与假设，建立可回放情景','参数旋钮，夹具锁住同源起点'],
 ['compare',46,54,'同一起点，对照三种情景','同源 A-001 分流，标签共同尺度'],
 ['dual',54,59,'业务 × 舆情，逐轮观察','两层沿同一轮次推进'],
 ['result',59,64,'比较路径、范围与恢复过程','模型状态记录形成差异'],
 ['return',64,74,'结果回到专家，研判落到行动','记录与案件一起回程，形成核查事项'],
 ['reveal',74,80,'有据研判 · 情景推演 · 持续跟踪','拉远揭示同一台机器及完整反馈回路']
].map(([id,start,end,caption,action])=>({id,start,end,caption,action,reads:[{at:start+.5,understood:start+2,leave:end-.4,text:caption}],states:{establish:start+.5,action:(start+end)/2,result:end-.7},subjectId:'A-001'}));
const events=[[2.5,'signal','bell'],[8,'source','scan'],[10,'bind','lock'],[20.5,'relation','lock'],[29,'experts','bell'],[34,'knowledge','scan'],[38,'condition','lock'],[44,'freeze','lock'],[48.5,'split','lock'],[51,'trial','bell'],[55,'dual','scan'],[61,'record','lock'],[67,'return','scan'],[73,'review','bell'],[77.5,'reveal','bell']].map(([at,id,sound])=>({at,id,sound}));
const plan={title:'Risky 风险传导与决策试验机',duration:80,fps:30,width:1920,height:1080,aspect_ratio:'16:9',delivery_mode:'ai_review_once',shots,events,soundtrack:{sample_rate:48000,phrases:Array.from({length:10},(_,i)=>({start:i*8,end:(i+1)*8,beats:16})),density:[{start:0,end:6,gain:.32},{start:6,end:26,gain:.58},{start:26,end:40,gain:.50},{start:40,end:46,gain:.68},{start:46,end:64,gain:.95},{start:64,end:74,gain:.62},{start:74,end:80,gain:.32}],breaks:[[43.8,44],[50.8,51],[76.8,77]],events},facts:'Synthetic mechanism demonstration; not engine output, probabilities, ratings or loss estimates.',creative_direction:'风险传导与决策试验机；已由用户指定，无需三选一。',protected:['同一个案件','同源快照','专家半圆会场','三组共同尺度','双轨','返回复核']};
fs.writeFileSync(path.join(v,'plan.json'),JSON.stringify(plan,null,2));
const head=fs.readFileSync(path.join(v,'primitives.js.txt'),'utf8').replace(/^\uFEFF/,'');fs.writeFileSync(path.join(v,'film.js'),head+'\n'+fs.readFileSync(path.join(v,'scene-body.js'),'utf8'));
console.log('Built Risky film and shared timeline');
