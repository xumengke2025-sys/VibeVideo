"""One-time, non-destructive fork of the approved blueprint engine for the single-case film."""
from pathlib import Path
import shutil, json, hashlib
P=Path(__file__).resolve().parent
R=P/'v16'
R.mkdir(exist_ok=False)
for f in ['vendor','index.html','render.mjs','intro.js','scene-body.js','film.js','professional-ai-content-evidence.json','reduction-content-evidence.json','source-transfer.json']:
    src=P/'v13'/f
    if src.is_dir(): shutil.copytree(src,R/f)
    else: shutil.copy2(src,R/f)
(R/'assets').mkdir()
ref=Path('C:/Users/67236/AppData/Local/Temp/codex-clipboard-f51cb33a-83ad-4993-9056-8139719ce6d2.png')
shutil.copy2(ref,R/'assets/industry-roundtable-reference.png')
film=(R/'film.js').read_text(encoding='utf-8')
(R/'helpers.js').write_text(film[:film.index('// Screen-space drafting table')],encoding='utf-8')
render=(R/'render.mjs').read_text(encoding='utf-8').replace('v13-business-first','v16-single-case').replace('/v13/','/v16/').replace('args.duration||60','args.duration||104')
(R/'render.mjs').write_text(render,encoding='utf-8')
html=(R/'index.html').read_text(encoding='utf-8').replace('max="60"','max="104"').replace(' / 60',' / 104')
(R/'index.html').write_text(html,encoding='utf-8')
intro=(R/'intro.js').read_text(encoding='utf-8').replace('股东服务新需求','股东服务新线索')
intro=intro.replace('B 端商机，为什么总是慢一步？','想拓展客户，先从哪里入手？').replace('时间花在找资料，精力耗在做准备','公告、客户信息、行业资料，分散在不同地方')
intro=intro.replace("['专业支持难找','跨领域问题，需要专业判断']","['信息归集不全','客户背景与产业信息难以拼全']")
intro=intro.replace("['跟进准备重复','拜访材料、沟通重点反复整理']","['专业判断缺支持','找到线索，还要知道如何切入']")
intro=intro.replace('以股东减持为例，进入专业研判','同一个案例：半导体企业的股东服务线索')
(R/'intro.js').write_text(intro,encoding='utf-8')
body=(R/'scene-body.js').read_text(encoding='utf-8')
body=body[:body.index('// Music-only edition')]
body=body.replace('function signals(){','function sourceStation(){')
body=body.replace('filmTime,10.7,11','openingClock(filmTime),10.7,11')
body=body.replace("'找到客户经营的业务切入点'","'找到这家客户的业务切入点'")
body=body.replace("'把分散线索，变成可跟进的客户机会'","'资料归集：先看清同一家客户'")
body=body.replace("'客户资料'","'解禁信息'")
body=body.replace("'减持商机示例'","'A01 · 示例半导体企业'")
body=body.replace("'客户线索归集'","'股东服务线索'")
body=body.replace("'重点客户与业务线索'","'主体 · 事件 · 时间'")
body=body.replace("'看清客户需求，找到服务切入点'","'专业会商：这家客户应该怎样跟进？'")
body=body.replace("'客户需求与服务思路'","'A01 · 股东服务研判'")
body=body.replace("'AI 辅助多专业会商'","'结合客户背景，形成服务思路'")
body=body.replace("'客户需求'","'股份管理需求'").replace("'联系时机'","'联系时机'")
body=body.replace("if(T>=16.3&&T<=20.6)movingRoute(paths.knowledge,16.3,20.6);","/* V16: archive travels through connected industry table. */")
body=body.replace("'复杂业务研判，有专业依据可用'","'回到同一客户：把依据带入服务判断'")
body=body.replace("'为业务判断补齐依据'","'A01 · 研究与规则依据'")
body=body.replace("'存量股东服务回访'","'了解股份管理安排'")
body=body.replace("'客户跟进准备包'","'A01 · 客户沟通准备包'")
body=body.replace("'联系时机 · 服务切入点'","'联系目的：了解股份管理安排'")
body=body.replace("'开场话术 · 沟通重点'","'结合产业背景，准备沟通问题'")
body=body.replace("35,43,show(31.2)","35,36,show(31.2)").replace("116,37,show(31.8)","116,33,show(31.8)")
body=body.replace("'客户经营记录'","'A01 · 沟通记录'").replace("205,-85,45","205,-85,38")
body=body.replace('7970,4570','9570,4570').replace('7900,4500','9500,4500').replace('x<8000','x<9600').replace('x<8050','x<9650')
body=body.replace("plaque('专业研判',5130,325,1240,136,u);","plaque('专业研判',5130,325,1240,136,u);plaque('产业研究',7750,610,1260,136,u);")
body=body.replace('const c={};for(const [j,k]', 'const c={};for(const [j,k]')
# Include the added station in the final wide view. Existing travel/reading keys stay intact.
body=body.replace('[47.5,4140,2480,.22,0],[48.4,4140,2480,.22,0]','[47.5,4900,2480,.18,0],[48.4,4900,2480,.18,0]')
body=body.replace('[50.4,4140,2510,.228,0],[52,4140,2510,.228,0]','[50.4,4900,2510,.185,0],[52,4900,2510,.185,0]')
(R/'scene-body.js').write_text(body,encoding='utf-8')
audio=(P/'v15/make_audio.py').read_text(encoding='utf-8').replace('np.arange(0,88,6.4)','np.arange(0,plan[\'duration\']-2,6.4)').replace('min(6.7,90-at)',"min(6.7,plan['duration']-at)").replace("plan['burdens']","plan.get('burdens',[])")
(R/'make_audio.py').write_text(audio,encoding='utf-8')
shots=[(0,10,'pain','找商机耗时，信息分散'),(10,18,'cards','选择股东服务场景，同一半导体客户'),(18,32,'sources','归集同主体、事件与时间'),(32,46,'judgment','线索怎样成为跟进判断'),(46,60,'experts','专业会商，形成服务思路'),(60,76,'industry','深入理解同一客户的产业位置'),(76,83,'knowledge','研究与规则依据回接客户档案'),(83,96,'preparation','形成沟通材料，经人工审核'),(96,104,'feedback','记录回流，持续客户经营')]
messages=[(18,23,'痛点｜资料分散，搜集耗时','同一家客户：公告、股东资料、解禁信息进入档案'),(23,31.5,'先看清事实，再寻找业务切入点','工具取数与规则筛选 · AI 辅助解读、归纳来源'),(32,37,'痛点｜发现了信号，业务价值仍难判断','以公司解禁信息为线索，梳理主体、时间与服务背景'),(37,45.5,'研判｜为什么关注？联系谁？先谈什么？','AI 辅助梳理条件与依据，形成跟进建议'),(47,53,'痛点｜复杂业务问题，需要专业支持','专业知识装备 + 业务方法 + 培养与试炼'),(53,59.5,'会商｜股东服务判断，还要结合客户背景','AI 专家协作：股份管理需求、联系时机、服务切入点'),(60,65,'继续追问｜这家半导体企业，处在产业链哪里？','同一份 A01 客户档案，进入产业研究台'),(65,71,'产业研判｜先定位环节，再看技术与经营资料','AI 辅助检索年报、专利与产业资料，关联来源'),(71,75.5,'把行业理解，带回这家客户的沟通准备','产业研究提供客户背景，股东服务专家研判服务方向'),(76.5,82.5,'痛点｜建议要有专业依据支撑','规则、案例与研究原文回接同一客户档案'),(84,90,'痛点｜有了判断，怎样与客户展开沟通？','AI 辅助整理：联系目的、客户背景、拜访问题'),(90,95.8,'成果｜带着明确问题与服务思路开展沟通','业务人员审阅材料，安排联系与后续跟进'),(96,100,'把沟通记录留在同一份客户档案里','AI 辅助梳理记录，支持下一次业务研判')]
events=[(10.4,'cards-open','travel'),(13.2,'card-selected','accent'),(17.6,'archive-handoff','tick'),(24,'sources-merge','drop'),(33.2,'judgment-open','tick'),(37.6,'criteria-connect','accent'),(41.6,'judgment-result','drop'),(50.4,'expert-1','tick'),(51.6,'expert-2','tick'),(52.8,'expert-3','accent'),(60.4,'industry-travel','travel'),(64.4,'atlas-open','accent'),(66.4,'company-position','drop'),(68.8,'evidence-connect','tick'),(72.4,'research-result','accent'),(74,'return-evidence','travel'),(79.6,'knowledge-read','accent'),(87.2,'preparation','drop'),(93.2,'human-review','tick'),(96.4,'feedback','travel'),(101.6,'brand','resolve')]
plan={'revision':'V16 single-case blueprint continuation','duration':104,'fps':30,'width':1920,'height':1080,'aspect_ratio':'16:9','world':[9800,4800],'delivery_mode':'ai_review_once','review_budget':'already_used','base':'v13 (V11 blueprint world and cards retained)','case':{'id':'A01','label':'示例客户信息','industry':'半导体衬底企业（流程示意）','opportunity':'股东服务／减持线索','fictional':True},'shots':[{'start':a,'end':b,'id':i,'name':n,'voiceover':'','reads':n} for a,b,i,n in shots],'business_messages':[{'start':a,'end':b,'pain':c,'result':d} for a,b,c,d in messages],'soundtrack':{'sample_rate':48000,'phrases':[{'start':i,'end':min(i+6.4,104),'beats':round((min(i+6.4,104)-i)/.4)} for i in [j*6.4 for j in range(17)] if i<104],'density':[{'start':0,'end':10,'gain':.58},{'start':10,'end':18,'gain':1},{'start':18,'end':46,'gain':.7},{'start':46,'end':60,'gain':.56},{'start':60,'end':65,'gain':.95},{'start':65,'end':74,'gain':.6},{'start':74,'end':84,'gain':.8},{'start':84,'end':96,'gain':.7},{'start':96,'end':101.6,'gain':1},{'start':101.6,'end':104,'gain':.28}],'breaks':[[23.8,24],[66.2,66.4],[87,87.2]],'events':[{'at':a,'id':i,'sound':s} for a,i,s in events]}}
(R/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'original-video-continuity.json').write_text(json.dumps({'base':'v13','protected':['card fanning and extraction','paper compositor','shared machine geometry','nine expert domains','six knowledge slots','quintic camera','feedback loop'],'base_hashes':{f:hashlib.sha256((P/'v13'/f).read_bytes()).hexdigest() for f in ['film.js','scene-body.js','intro.js']},'reference_image_sha256':hashlib.sha256(ref.read_bytes()).hexdigest()},indent=2),encoding='utf-8')
print('Created v16 from preserved original blueprint source.')
