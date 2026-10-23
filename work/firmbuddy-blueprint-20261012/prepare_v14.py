from pathlib import Path
import shutil,json,hashlib
B=Path(__file__).resolve().parent; R=B/'v14'
assert not R.exists(), 'Preserve existing V14; do not rerun initializer'
shutil.copytree(B/'v13',R)
for f in R.glob('*'):
 if f.suffix in ['.js','.mjs','.py','.html','.md','.json']:
  s=f.read_text(encoding='utf-8').replace('v13','v14').replace('V13','V14').replace('business-first','burden-journey')
  f.write_text(s,encoding='utf-8')
for f in ['archive_checks.py','finalize_observations.py','prepare_delivery.py','package_v13.py']:
 p=R/f
 if p.exists(): p.unlink()
plan=json.loads((R/'plan.json').read_text(encoding='utf-8'))
plan.update(duration=90,revision='V14: continuous business-person journey, six burdens relieved, opportunity logic station')
plan['time_map']=[[0,0],[8,4],[14,8],[22,16],[26,16],[42,16],[46,20],[54,24.1],[63,31],[68,33.6],[78,42.7],[84,48.1],[90,60]]
plan['burdens']=[
 {'id':'records','label':'记录难接续','end':83.2,'result':'经营记录接续'},
 {'id':'preparation','label':'准备重复','end':76.8,'result':'跟进材料齐备'},
 {'id':'evidence','label':'依据难找','end':66.4,'result':'研判有据可查'},
 {'id':'expert','label':'专家难找','end':52.4,'result':'多专业协作'},
 {'id':'judgement','label':'判断费力','end':40.8,'result':'判断逻辑清晰'},
 {'id':'collection','label':'资料分散','end':21.2,'result':'客户线索归集'}]
stages=[(0,8,'burden','业务人员背负六项准备负担'),(8,18,'entry','多类业务抽卡进入原机器'),(18,22,'collection','资料归集卸下搜集负担'),(22,46,'logic','新工位展示来源、判断逻辑与业务方向'),(46,54,'experts','专业会商卸下找专家负担'),(54,68,'knowledge','依据检索卸下查资料负担'),(68,78,'preparation','准备包卸下重复准备负担'),(78,84,'records','记录接续卸下经营接续负担'),(84,90,'reveal','轻装前行并揭示完整机器')]
plan['shots']=[dict(start=a,end=b,id=c,reads=d) for a,b,c,d in stages]
plan['business_messages']=[
 dict(start=18,end=22,pain='找线索慢：资料分散，搜集筛选耗时',result='归集客户线索，少做重复搜集'),
 dict(start=26,end=42,pain='判断费力：信号很多，哪些值得业务跟进？',result='看清来源与判断逻辑，再决定业务切入点'),
 dict(start=46,end=54,pain='专业支持难找：客户需求涉及多个业务领域',result='围绕需求、时机与服务思路，获得多专业支持'),
 dict(start=59,end=68,pain='依据难找：规则、案例和研究分散',result='让复杂业务研判有依据，减少反复查找'),
 dict(start=72,end=78,pain='跟进准备重复：材料与沟通重点反复整理',result='形成客户跟进准备包，把精力还给客户沟通'),
 dict(start=80,end=84,pain='经营难接续：沟通过什么，下一步做什么？',result='经营记录接得上，每次跟进都有来由')]
plan['soundtrack'].update(sample_rate=48000,phrases=[dict(start=i,end=min(i+6.4,89.6),beats=round((min(i+6.4,89.6)-i)/.4)) for i in [k*6.4 for k in range(14)]],density=[dict(start=0,end=8,gain=.55),dict(start=8,end=26,gain=.9),dict(start=26,end=42,gain=.55),dict(start=42,end=90,gain=.78)],breaks=[[39.9,40.6],[82.4,83.0]],events=[dict(id=b['id'],at=b['end'],sound='relay',note=74+i*2) for i,b in enumerate(reversed(plan['burdens']))]+[dict(id='cards',at=8,sound='downbeat'),dict(id='entry',at=14,sound='drop'),dict(id='logic',at=26,sound='drop'),dict(id='outro',at=88,sound='resolve')])
(R/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
s=(R/'index.html').read_text(encoding='utf-8').replace('max="60"','max="90"').replace('/ 60','/ 90');(R/'index.html').write_text(s,encoding='utf-8')
s=(R/'render.mjs').read_text(encoding='utf-8').replace('args.duration||60','args.duration||90');(R/'render.mjs').write_text(s,encoding='utf-8')
# New timeline is built on the original geometry, with one inserted station.
s=(R/'scene-body.js').read_text(encoding='utf-8')
s=s[:s.index('window.renderAt=')]
s=s.replace("const a=ease(p(filmTime,10.7,11))", "const a=ease(p(filmTime,10.7,11))")
(R/'scene-body.js').write_text(s,encoding='utf-8')
# Source code facts, not marketing claims.
sources=[('D:/ai项目/firmbuddy/docs/opportunity-rules-v2.md','1-48'),('D:/ai项目/firmbuddy/plugins/_shared/opportunity-rules.mjs','1-53'),('D:/ai项目/firmbuddy/docs/implementation/REDUCTION-PRECONTACT-V2-20260922.md','1-39')]
evidence=dict(sources=[dict(path=p,read_lines=l,sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for p,l in sources],claims=['Public announcements and structured unlock calendar feed deterministic versioned rules.','Financing candidates filter execution/approval/issuance/ongoing stages.','MA assesses stage and consideration; shareholder services assess identity and windows; hedging uses real exposures; crossborder uses geography and currency.','AI supports explanation and expert research; business judgement and human review retained.'],limits=['Title-level signals are leads, not confirmed needs or deal probabilities.','Private needs require authorized client evidence.','Not full-market historical coverage; no guaranteed conversion.'])
(R/'opportunity-logic-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'brief.md').write_text('''# FirmBuddy V14 · 业务减负之旅
- aspect_ratio: 16:9
- width: 1920
- height: 1080
- duration: 90
- fps: 30
- delivery_mode: ai_review_once
- review_budget: already_used；用户反馈修改，不新增角色。

原V13蓝图世界、抽卡、专家座谈、九业务分类、六知识槽与业务叙事保留。采用用户明确的小人减负方向，不重开创意候选。金色线稿业务人员从弯腰负重逐渐站直；六个可拆包裹依次被各工位的吊运机构接走，分别对应归集、判断、专业支持、查证、材料、记录六类负担。人物走独立世界轨迹，相机伴随移行并在卸载处停留，最终留在机器出口，镜头拉远。

新增判断工位位于原世界左下空白区[1650,2550]，使用真实规则展示四类业务的来源→判断要点→服务方向。融资过滤执行阶段，股东服务区分披露/解禁和主体条件，AI是辅助解读而非自动成交。细节依据见opportunity-logic-evidence.json。

制作顺序：正式代码效果图（开场、卸载、判断工位、全景）→首次卸载与新增跨站转场样段→90秒整片。保留原代码绘图与纸纹机制，扩写同风格原创音乐，六次卸载落点与音乐事件共用plan。概念/观察均以实际输出为准。
''',encoding='utf-8')
with (B/'CHECKPOINT.md').open('a',encoding='utf-8') as f:f.write('\n## V14 · 2026-10-22 90秒减负之旅进行中\n- objective: 小人背负多项业务负担，经过各机器环节逐项减负；新增商机判断逻辑与来源工位，基于产品实际规则。\n- aspect_ratio:16:9; width:1920; height:1080; duration:90; delivery_mode:ai_review_once; review_budget:already_used。\n- 已只读核对商机统一规则v4、业务文档和减持V2，保留V13历史。新工位采用来源→阶段/条件判断→服务方向，AI辅助说明和人工审核保留。\n- 下一步：角色世界轨迹、六次卸载、新工位与相机连接代码；实际效果图与样段后导出整片。\n')
print('V14 initialized')
