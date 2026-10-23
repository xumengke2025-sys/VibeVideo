from pathlib import Path
import shutil,json,hashlib
B=Path(__file__).resolve().parent
R=B/'v17'
R.mkdir(exist_ok=False)
for f in (B/'v16').iterdir():
    if f.name in ['vendor','assets']:
        shutil.copytree(f,R/f.name)
    elif f.is_file() and f.suffix in ['.js','.mjs','.py','.html']:
        shutil.copy2(f,R/f.name)
shutil.copy2(B/'assets/reference/02-expert-hall.png',R/'assets/expert-hall-reference.png')
for f in R.iterdir():
    if f.is_file() and f.suffix in ['.js','.mjs','.py','.html']:
        s=f.read_text(encoding='utf-8').replace('v16-single-case','v17-blueprint-sources').replace('/v16/','/v17/').replace("Path('v16')","Path('v17')").replace('V16','V17')
        if f.name=='render.mjs':s=s.replace('duration||104','duration||124')
        if f.name=='index.html':s=s.replace('104','124')
        if f.name=='setup.py':s=s.replace('104 seconds','124 seconds')
        f.write_text(s,encoding='utf-8')
p=json.loads((B/'v16/plan.json').read_text(encoding='utf-8'))
p.update(revision='V17 unified blueprint / traceable opportunity sources',duration=124,base='v16',aspect_ratio='16:9',width=1920,height=1080)
old=p['shots'][2:]
for q in old:q['start']+=20;q['end']+=20
p['shots']=[
 {'start':0,'end':18,'id':'pain','name':'业务流程的四个具体阻点','voiceover':'','reads':'0–8秒看线索搜集和切入问题，8–16秒看信息缺口与专业研判；16–18秒合拢到归集机构','action':'分散文档反复往返，时间游标停在多条支路，缺项档案与跨专业请求形成同一业务阻点'},
 {'start':18,'end':28,'id':'origins','name':'商机从公开信息和客户扫描范围中来','voiceover':'','reads':'18–21秒识别公告和解禁日历；21–24秒看到统一规则识别事件并分类；24–28秒读取来源与扫描范围','action':'两个有名称的数据源沿轨道进入规则分拣器，来源凭据保留在输出卡上'},
 {'start':28,'end':38,'id':'cards','name':'按业务分类抽卡，选取同一客户的解禁线索','voiceover':'','reads':'28–32秒读取五类业务及各自信号；32–35秒抽出股东服务；35–38秒A01线索卡沿既有轨道进入资料站','action':'同色蓝图卡片展开，选中卡从卡列抬起并收拢成A01档案'}]+old
for q in p['business_messages']:q['start']+=20;q['end']+=20
for q in p['business_messages']:
    if q['start']==67:q.update(pain='痛点｜行业、合规与客户经营，专业研判如何协同？',result='九大业务领域 · 知识装备、业务方法与培养试炼')
    if q['start']==73:q.update(pain='会商｜围绕同一客户，形成有分工的专业意见',result='股东增减持、解禁预警、拜访策略专家协同研判')
p['soundtrack']['phrases']=[dict(start=round(i*.4,4),end=round(min(124,(i+16)*.4),4),beats=min(16,310-i)) for i in range(0,310,16)]
p['soundtrack']['density']=[dict(start=0,end=8,gain=.62),dict(start=8,end=18,gain=.64),dict(start=18,end=28,gain=.82),dict(start=28,end=38,gain=1)]+[dict(start=q['start']+20,end=q['end']+20,gain=q['gain']) for q in p['soundtrack']['density'] if q['start']>=18]
p['soundtrack']['breaks']=[[a+20,b+20] for a,b in p['soundtrack']['breaks']]+[[31.8,32.0]]
events=[dict(q,at=q['at']+20) for q in p['soundtrack']['events'] if q['at']>=18]
p['soundtrack']['events']=[dict(at=t,id=i,sound=s) for t,i,s in [(0.4,'problem-establish','accent'),(8.0,'background-problems','tick'),(18.0,'source-bench','travel'),(20.4,'public-source','tick'),(21.2,'unlock-source','tick'),(24.0,'rule-sort','accent'),(28.0,'source-cards','travel'),(32.0,'card-selected','drop'),(37.6,'archive-handoff','tick')]]+events
p['connections']=[dict(time=18,kind='same-world drafting tray',anchor='same workbench frame and document rails',window=[16,20]),dict(time=28,kind='source-bearing cards',anchor='rule output card moves into the fan',window=[26,30]),dict(time=38,kind='continuous geometric handoff',anchor='A01 archive / paths.query',window=[35,40]),dict(time=80,kind='retained industry path',anchor='A01',window=[78,84])]
(R/'plan.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
hist={f:hashlib.sha256((B/'v16'/f).read_bytes()).hexdigest() for f in ['helpers.js','intro.js','scene-body.js','story.js','film.js','plan.json','audio/mix.wav']}
(R/'original-video-continuity.json').write_text(json.dumps(dict(base='v16',base_hashes=hist,protected=['existing post-entry machinery','A01 case','industry atlas','knowledge categories','no voiceover','1920x1080']),indent=2),encoding='utf-8')
(R/'CHECKPOINT.md').write_text('''# V17 制作检查点

- 目标：落实用户反馈，细化业务痛点、说明商机来源，专家座谈贴近原图，全片统一工程蓝图。
- aspect_ratio: 16:9; width: 1920; height: 1080; fps: 30; duration: 124
- delivery_mode: ai_review_once；历史预算已用，本轮零子代理，按用户反馈修改。
- 基线：v16；旧版成片、源文件及 FirmBuddy 产品工程保留。
- 已核对：公开公告/解禁日历、市场/客户/监控扫描、共享业务规则、原始专家会场图。
- 已选方案：同一制图工作台内由四个业务阻点进入来源分拣，再抽出带来源的 A01 卡片；持续载体沿既有机器推进。
- 保护：产业图谱、知识仓、结果与跟进回路、业务优先叙事、纯音乐。
- 下一步：实现蓝图开头与原图式阶梯座谈，渲染设定帧及关键连续样段。
''',encoding='utf-8')
(R/'brief.md').write_text('''# V17 制作说明

1920×1080 / 30fps / 124秒 / 纯音乐。沿用已选 delivery_mode=ai_review_once，审核历史预算已用。

本次只深化已认可的工程蓝图世界：0–18秒以分散文档、岔路时间尺、资料缺口和跨专业请求，具体解释搜集耗时、切入不明、背景不全、研判难协同。18–28秒展示公开公告及结构化解禁日历，在市场扫描、客户定向、监控名单范围内经规则识别分类。28–38秒每张蓝图业务卡保留其公告/日历来源，抽出解禁日历带来的A01公司级线索，进入减持商机研判案例。38秒后沿用原机组与后续故事。

专家区参照 assets/expert-hall-reference.png 的多层弧形长桌、众多有名牌的坐姿专家、后墙品牌屏和前排会商关系。用相同蓝纸白线重建，不贴平面截图。正式九类目录保留；选中专家按系统名称与职责展示。

选择依据：既有视觉方向已获认可，不重开候选。把痛点和来源放进原工作台，能保留同一空间、同一档案和连续交接；独立标题页与米金卡面会重复用户已指出的风格断裂，故移除。

视觉承诺：前面的碎片资料经可见的来源轨道与业务规则成为有出处的卡片；从选中卡跟进同一客户，进入有专业分工的会商。

事实边界：片中企业为流程示意；解禁日历提供公司级线索，后续研判服务条件与沟通路径；不推断具体股东已决定减持。规则识别与AI解读各自标明。专家知识装备与培养不等于模型参数微调。

预定设定帧：5/12/24/30/34/74秒。关键样段：26–42秒（来源卡—抽卡—同一档案入机），66–82秒（阶梯专家会商与原产业图交接）。源码绘制，正式1080p验证，不新增审批节点。
''',encoding='utf-8')
sources=[B/'assets/reference/02-expert-hall.png',Path('D:/ai项目/firmbuddy/docs/opportunity-rules-v2.md'),Path('D:/ai项目/firmbuddy/plugins/_shared/opportunity-rules.mjs'),Path('D:/ai项目/firmbuddy/plugins/expert-personas/data/personas.json')]
(R/'content-evidence.json').write_text(json.dumps(dict(sources=[dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in sources],claims=['Public announcements and structured unlock calendar feed versioned business rules.','Market, customer-specific and monitoring scans share opportunity rules.','Card taxonomy is backed by rule labels; rule output is a candidate lead, not proof of client intention.','Expert names and nine-domain taxonomy follow the product.'],references='Existing Lemo blueprint draw/paper implementation and retained V16 world; no generated imagery.'),ensure_ascii=False,indent=2),encoding='utf-8')
print(R)
