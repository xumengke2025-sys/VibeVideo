from pathlib import Path
import shutil,json,hashlib
B=Path(__file__).resolve().parent; R=B/'v19'; R.mkdir(exist_ok=True)
for f in ['helpers.js','index.html','render.mjs','make_audio.py','source-transfer.json','methodology-evidence.json']:
 shutil.copy2(B/'v18'/f,R/f)
for d in ['vendor','assets']:
 if (B/'v18'/d).exists():shutil.copytree(B/'v18'/d,R/d,dirs_exist_ok=True)
s=(B/'v18/scene-body.js').read_text(encoding='utf-8')
geom=s[s.index('const domains='):s.index('function intro()')]
geom=geom[:geom.index('// Quintic Hermite')]+s[s.index('function quint('):s.index('function intro()')]
# Retain deterministic camera interpolation and source-derived fabrication primitives.
figure=s[s.index('function expertFigure('):s.index('const hallSeatNames=')]
(R/'geometry.js').write_text(geom+'\n'+figure,encoding='utf-8')
r=(R/'render.mjs').read_text(encoding='utf-8').replace('v18-business-story','v19-mechanical-relief').replace('/v18/','/v19/').replace('args.duration||154','args.duration||120')
r=r.replace("'--renderer-process-limit=1'","'--renderer-process-limit=1','--js-flags=--max-old-space-size=2048'")
(R/'render.mjs').write_text(r,encoding='utf-8')
events=[('engage',9.6,'drop','输入齿轮啮合'),('fan',14.4,'tick','业务卡扇形展开'),('select',21.6,'accent','抽出股东服务卡'),('travel1',24,'travel','跟随档案进入归集'),('merge',30.4,'tick','重复纸张进入滚轮'),('file',33.6,'drop','客户档案归集落定'),('judge',37.6,'accent','背景与信号对齐'),('travel2',40,'travel','档案进入专家会场'),('expert1',46.4,'relay','股东专家输出需求'),('expert2',48,'relay','解禁专家输出时机'),('expert3',49.6,'relay','策略专家输出切入'),('consult',52,'drop','会商结果接合'),('travel3',54.4,'travel','会商转产业研究'),('industry',61.6,'accent','客户定位衬底节点'),('evidence',65.6,'tick','研究依据装入档案'),('travel4',67.2,'travel','下降进入知识仓'),('drawer',73.6,'tick','知识抽屉打开'),('retrieve',77.6,'drop','引用证据装入档案'),('travel5',80,'travel','跟随档案进入装配'),('page1',86.4,'tick','关注依据装配'),('page2',88,'tick','沟通重点装配'),('page3',89.6,'tick','跟进安排装配'),('human',92.8,'accent','人工审阅闸门开启'),('travel6',96,'travel','准备包送至跟进'),('record',101.6,'tick','沟通记录归档'),('return',104,'travel','同一档案沿反馈回路返回'),('resolve',114.4,'resolve','全机揭示')]
events=[dict(id=i,at=t,sound=k,action=a,**({'note':n} if k=='relay' else {})) for (i,t,k,a),n in zip(events,[62,65,69]*10)]
shots=[]
for i,(a,b,title,benefit) in enumerate([(0,10,'准备被重复工作占满','搜、筛、抄，挤占研判'),(10,24,'商机查询','从业务场景找到线索'),(24,40,'归集与研判','少搜少抄，先排重点'),(40,54.4,'专业会商','少找专家，共同研判'),(54.4,67.2,'产业研究','补齐背景，沟通更深入'),(67.2,80,'知识查证','少翻资料，依据随用随取'),(80,96,'跟进准备','少拼材料，沟通更有重点'),(96,104,'持续跟进','少重复交接，后续接得上'),(104,113,'记录回流','同一客户，持续经营'),(113,120,'完整机器','AI 辅助准备，业务专注判断')]):
 shots.append(dict(id=f's{i+1}',start=a,end=b,title=title,benefit=benefit,voiceover=False,subjectId='A01',understanding=benefit))
plan=dict(version='v19-mechanical-relief',duration=120,fps=30,width=1920,height=1080,aspect_ratio='16:9',delivery_mode='ai_review_once',review_budget='historical_already_used',shots=shots,business_messages=[],burdens=[],soundtrack=dict(sample_rate=48000,events=events,breaks=[[9.25,9.6],[33.25,33.6],[92.45,92.8]],phrases=[dict(start=a,end=b,beats=round((b-a)/.4)) for a,b in [(0,9.6),(9.6,24),(24,40),(40,54.4),(54.4,67.2),(67.2,80),(80,96),(96,104),(104,114.4),(114.4,120)]],density=[dict(start=a,end=b,gain=g) for a,b,g in [(0,9.6,.5),(9.6,24,.9),(24,40,.78),(40,54.4,.55),(54.4,67.2,.6),(67.2,80,.72),(80,96,.78),(96,114.4,.9),(114.4,120,.55)]]))
(R/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'setup.py').write_text("from pathlib import Path\nR=Path(__file__).resolve().parent\n(R/'film.js').write_text('\\n'.join((R/f).read_text(encoding='utf-8') for f in ['helpers.js','geometry.js','mechanisms.js','conductor.js']),encoding='utf-8')\nprint('Built V19 / 120s / 1920x1080')\n",encoding='utf-8')
(R/'v18-preserved.json').write_text(json.dumps({str(f.relative_to(B/'v18')):hashlib.sha256(f.read_bytes()).hexdigest() for f in (B/'v18').rglob('*') if f.is_file()},indent=2),encoding='utf-8')
(R/'brief.md').write_text('''# V19 机械减负工作流

aspect_ratio: 16:9
width: 1920
height: 1080
duration: 120
delivery_mode: ai_review_once
review_budget: historical_already_used

用户要求：更强机械感、巧思、少字、简洁，用动态内容说明各环节业务提升与减负。沿用已获认可蓝图和原始专家会场，无新增审批/审片角色。无试点数据，不使用百分比、计时绩效或虚构成交。

比较三个机制：①仪表盘数值变化（容易虚构绩效且文字多）；②零散独立工具逐项演示（缺连续客户）；③同一客户档案沿装配线加工（选择）。机械只是流程隐喻，不宣称实体设备或自动判定客户减持意图。

保护项：一般入口商机查询、股东服务为示例；示例客户信息/A01半导体衬底企业；九类专家与阶梯座谈厅；产业研究紧接会商；人工审阅/业务人员负责判断；知识装备不等于参数微调；纯音乐/踩点/无配音；保留V18。

减少文字：取消上下双条字幕、长段说明、每张卡的多行解释、会场几十块专家文字牌。每站一个短标题、一句收益，来源/专家分类/关键对象保留。动作链：纸张拥堵→开闸→场景抽卡→滚轮去重归集→对齐背景研判→专家多路会商→产业定位→知识取证→准备包装配→人工审阅→记录回流→全机揭示。

参考：继续使用Lemo固定commit e3cb16f63768c68693ff0e15171d6e755457cc32的纸面引擎、实体消隐、斜投影和齿轮相位；沿用本项目原齿轮/轴承/导轨与确定性五次相机插值。主动作与音效共用plan.soundtrack.events。每站以输入→机构接触→业务成果成立，避免装饰齿轮空转。

概念/动态：用正式代码渲染整体与代表站点，验证滚轮归集、会商接力、知识抽屉及相邻连续运镜，再扩整片。已有方向与连续推进授权，不逐图增加确认。
''',encoding='utf-8')
(R/'CHECKPOINT.md').write_text('# V19 制作中\n\n目标：机械感与动作解释业务减负，减少文字。120秒/1920×1080/纯音乐。delivery_mode=ai_review_once，历史预算已用，零子代理。\n\n已完成：独立工程准备、动作/声音共享事件表、原版保护哈希。下一步：机构制作、正式关键帧与动态样段、成片、工程验证、源码包。\n',encoding='utf-8')
print('Prepared V19 without modifying V18')
