from pathlib import Path
import json, shutil
R=Path(__file__).resolve().parent
(R/'vendor').mkdir(exist_ok=True)
for name in ['draw.js','paper.js','LICENSE-Lemo']:
    shutil.copy2(R.parent/'v14/vendor'/name,R/'vendor'/name)
for name in ['index.html','render.mjs','make_audio.py']:
    text=(R.parent/'v14'/name).read_text(encoding='utf-8')
    if name=='render.mjs':text=text.replace('v14-burden-journey','v15-human-mechanism').replace('/v14/index.html','/v15/index.html')
    (R/name).write_text(text,encoding='utf-8')
events=[(6.4,'tick','分散资料翻查'),(10.4,'relay','抽取业务场景卡'),(19.2,'tick','档案入槽'),(20.8,'drop','来源归集'),(24,'relay','取回客户档案'),(35.2,'tick','条件比对'),(38.4,'drop','形成研判要点'),(40.8,'relay','携档案寻找专家'),(51.2,'tick','档案放上会商桌'),(54.4,'drop','专家协作'),(60.8,'travel','知识页沿导轨送达'),(64,'tick','引用接入档案'),(66.4,'relay','依据齐备'),(76,'tick','沟通材料归并'),(79.2,'drop','档案合册'),(81.6,'tick','经营记录回接'),(85.6,'relay','进入客户沟通'),(88,'resolve','客户经营价值')]
shots=[(0,12,'从哪里切入客户需求？','线索散、搜集慢，业务人员反复翻查',''),(12,28,'把分散信息，归到一份客户档案','公告、解禁日历与客户资料形成可用线索','AI 辅助归集与摘要'),(28,44,'有了线索，怎样判断跟进方向？','看阶段、看主体、看窗口，形成业务研判要点','AI 辅助解读与条件整理'),(44,58,'遇到专业问题，找到对口专家','专业知识与业务方法支撑多专业协作','AI 辅助匹配与专家协作'),(58,70,'研判有依据，沟通更有准备','规则、案例与研究资料，回到当前客户问题','AI 辅助检索与引用整理'),(70,84,'材料少重复，经营能接续','沟通要点、问题清单与跟进记录归入同一档案','AI 辅助材料整理与记录梳理'),(84,90,'把时间，留给客户与业务判断','FirmBuddy · 商机查询 / 业务研判 / 客户经营','')]
plan={'version':'v15-human-mechanism','duration':90,'fps':30,'aspect_ratio':'16:9','width':1920,'height':1080,'delivery_mode':'ai_review_once','review_budget':'already_used','burdens':[], 'shots':[{'id':f's{i+1}','start':a,'end':b,'title':c,'result':d,'ai':e,'voiceover':''} for i,(a,b,c,d,e) in enumerate(shots)],'soundtrack':{'sample_rate':48000,'bpm':150,'phrases':[{'start':0,'end':89.6,'beats':224}],'density':[{'start':0,'end':9.6,'gain':.55},{'start':9.6,'end':28,'gain':.95},{'start':28,'end':44,'gain':.8},{'start':44,'end':70,'gain':.6},{'start':70,'end':84,'gain':.95},{'start':84,'end':90,'gain':.65}],'breaks':[[20.55,20.8],[38.15,38.4],[78.95,79.2]],'events':[{'id':f'e{i}','at':a,'sound':s,'action':act,'note':74} for i,(a,s,act) in enumerate(events)]},'reference':{'drawing':'Lemo blueprint draw.js/paper.js, retained license','camera':'original V15 shared-world subject path and camera path; quintic transitions','content':'../v14/opportunity-logic-evidence.json'},'style':'low-contrast abstract silhouette / cyanotype / functional mechanisms / amber dossier'}
(R/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('V15 renderer, paper engine, licence and shared event plan prepared')
