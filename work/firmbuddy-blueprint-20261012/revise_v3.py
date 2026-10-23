from pathlib import Path
import json
R=Path(__file__).resolve().parent
f=R/'film.js';s=f.read_text(encoding='utf-8')
s=s.replace("'专业支持，随时进入'","'商机业务，一站协同'")
s=s.replace("'从不同需求，找到专业支持'","'找商机 · 解疑问 · 做方案 · 推跟进'")
a=s.index('function experts()');b=s.index('function knowledge()',a)
s=s[:a]+'''function experts(){at(...centers.experts,()=>{sect('03','多领域专家，协同答疑','EXPERT NETWORK / BUSINESS SUPPORT',17.2);
TX('数十位专家 · 多领域覆盖',0,-276,32,p(T,17.5,18.1),{align:'center',v:.8});
for(let row=0;row<4;row++){const yy=-25+row*62,rx=590-row*43,ry=205-row*14;const a=p(T,17.4+row*.22,18.1+row*.22);L(ell(0,yy,rx,ry,0,100,Math.PI,Math.PI*2),a,2,.75);L(ell(0,yy+22,rx,ry,0,100,Math.PI,Math.PI*2),a,1,.4);for(let j=0;j<14;j++){const angle=Math.PI+.12+(Math.PI-.24)*j/13,x=Math.cos(angle)*rx,y=yy+Math.sin(angle)*ry;R(x-14,y-22,28,20,a,.7,1.4);L([[x-19,y],[x+19,y]],a,1,.45)}}
const labels=['企业画像','行业研究','财务诊断','资本运作','信披合规','客户经营'];labels.forEach((v,i)=>{const x=-430+i%3*430,y=i<3?-126:-24,t=19.8+i*.55,a=p(T,t,t+.5);label(v,x-140,y,280,a,31);route([[x,y+58],[x,106],[0,106],[0,157]],t+.5,t+1.1)});
issue(-120,157,p(T,19,19.7),true);const a=p(T,25.1,25.8);L([[0,267],[0,312],[-440,312]],a,2.2);TX('单专家提问 · 多专家会商',-440,355,28,a);label('依据 [1] [2]',210,287,340,p(T,26,26.5),29);route([[210,316],[-720,316]],27.8,29.3)
})}
''' +s[b:]
a=s.index('function knowledge()');b=s.index('function strategy()',a)
s=s[:a]+'''function knowledge(){at(...centers.knowledge,()=>{sect('04','丰富知识库，按需调用','ARCHIVES / DOCUMENTS / SOURCE CATALOG',29.1);
const kinds=['核心规范','监管规则','产品能力','案例经验','研究资料','补充资料'];kinds.forEach((v,i)=>{const x=-590+i%3*215,y=-252+Math.floor(i/3)*211,a=p(T,29.3+i*.18,30.1+i*.18);for(let k=2;k>=0;k--)R(x+k*5,y-k*6,195,176,a,k?.30:.85,k?1:2);L([[x,y+31],[x+29,y+10],[x+76,y+10],[x+93,y+31],[x+195,y+31]],a,1.5);C(x+97,y+60,8,a);C(x+97,y+105,8,a);L([[x+97,y+52],[x+103,y+100],[x+92,y+113],[x+90,y+62]],a,1.1);TX(v,x+97,y+150,29,p(T,30+i*.18,30.5+i*.18),{align:'center'});mono('V'+(i%2+1),x+145,y+58,15,a,{v:.6})});
R(-387,-258,207,190,p(T,32,32.6),1,2.7);TX('档案库 · 文档资产 · 来源目录',-590,234,28,p(T,31.4,32),{v:.85});L([[-590,263],[45,263]],p(T,32,32.5),1,.4);TX('多类资料沉淀为可检索知识',-590,311,27,p(T,32.2,32.8),{v:.7});
label('检索、引用、追溯',160,-245,420,p(T,33.4,34),33);['查找业务相关资料','定位原文与出处','保留来源和版本'].forEach((v,i)=>{const a=p(T,34+i*.55,34.4+i*.55);C(178,-118+i*95,5,a);TX(v,202,-106+i*95,30,a);L([[202,-87+i*95],[576,-87+i*95]],a,1,.4)});route([[160,156],[105,156],[105,319],[-115,319]],36,37.4);mono('KNOWLEDGE → EXPERTS → ANALYSIS',150,251,18,p(T,36.7,37.2),{v:.7});mono('SOURCE / VERSION / REF.',160,310,20,p(T,37.3,37.8),{v:.7});route([[50,323],[180,323],[180,670]],39,40.5)
})}
''' +s[b:]
a=s.index('function strategy()');b=s.index('function sheet()',a)
s=s[:a]+'''function strategy(){at(...centers.strategy,()=>{sect('05','商机经营，全流程支持','DISCOVER / ANALYZE / PLAN / FOLLOW UP',40.2);const a=p(T,40.2,41.1);R(-590,-240,700,530,a,.85,2.5);TX('多种业务成果，按需生成',-552,-178,37,p(T,40.8,41.4));
const names=['商机研判','企业画像','行业研究','会商纪要','拜访策略包','客户经营计划'];names.forEach((v,i)=>{const x=-554+i%2*327,y=-120+Math.floor(i/2)*119,a=p(T,41.5+i*.4,42+i*.4);for(let k=1;k>=0;k--)R(x+k*5,y+k*5,293,94,a,k?.3:.8,k?1:1.7);TX(v,x+18,y+38,v.length>5?27:30,a);linesOfText(x+18,y+59,247,2,a)});TX('成果可预览、下载，版本化留存',-550,275,23,p(T,44,44.6),{v:.7});
issue(270,-232,p(T,41.5,42.1),true);const u=p(T,47,47.6);label(T<48.2?'确认创建':'',250,-45,310,u,36);if(T>48.2){L([[281,-15],[298,1],[326,-32]],p(T,48.2,48.5),3);TX('确认创建',338,-5,28,p(T,48.3,48.6));}route([[405,13],[405,105]],48.6,49.3);const b=p(T,49.3,49.9);R(224,105,380,181,b);TX('跟进任务',252,157,38,b);TX('待跟进 · 由客户经理确认',252,213,23,p(T,49.8,50.3),{v:.75});mono('NEXT ACTION',253,260,20,b,{v:.5});route([[110,62],[180,62],[180,195],[224,195]],45.5,46.5)
})}
''' +s[b:]
s=s.replace("'拜访 · 答疑 · 商机查询'","'商机经营 · 全流程协同'").replace("'专业支持，贯穿日常业务'","'从发现到行动，一站协同'")
a=s.index('export const captions=');b=s.index('function subtitle()',a)
s=s[:a]+'''export const captions=[
[.2,3.2,'找商机、准备拜访、业务答疑'],[3.2,6.6,'FirmBuddy，一站式专业支持'],
[8.1,11.9,'发现线索、查客户、研判需求'],[12,16.1,'从查询到核实，串联商机流程'],
[18.4,22.7,'数十位专家，覆盖多类业务'],[23,27.8,'行业、财务、资本、合规，协同答疑'],
[30.6,34.3,'规则、案例、研究，多类知识汇聚'],[34.4,39,'检索原文，追溯来源与版本'],
[41.6,47.15,'研判、方案、报告、拜访，按需形成成果'],[47.2,51,'确认后创建任务，推进跟进'],
[52.3,55.8,'商机经营全流程，一站协同支持'],[56,60,'FirmBuddy，从发现到行动，一站协同']];
''' +s[b:]
f.write_text(s,encoding='utf-8')
text=['找商机、准备拜访、业务答疑。','Firm Buddy，一站式专业支持。','发现线索、查客户、研判需求。','从查询到核实，串联商机流程。','数十位专家，覆盖多类业务。','行业、财务、资本、合规，协同答疑。','规则、案例、研究，多类知识汇聚。','检索原文，追溯来源与版本。','研判、方案、报告、拜访，按需形成成果。','确认后创建任务，推进跟进。','商机经营全流程，一站协同支持。','Firm Buddy，从发现到行动，一站协同。']
entries=json.loads((R/'audio/script-v2.json').read_text(encoding='utf-8-sig'))
for e,t in zip(entries,text):e[2]=t
(R/'audio/script-v3.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8-sig')
for name in ['make_audio.py','make_voice.ps1']:
 f=R/name;s=f.read_text(encoding='utf-8-sig').replace('script-v2.json','script-v3.json');f.write_text(s,encoding='utf-8-sig' if name.endswith('ps1') else 'utf-8')
print('V3 expert hall, knowledge collection, complete opportunity workflow updated')
