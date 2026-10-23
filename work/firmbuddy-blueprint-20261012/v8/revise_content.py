"""Retarget the illustrative business chain; preserve camera and musical anchors."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent; B=R.parent
replacements={
    '一句业务问题，启动专业协作':'减持商机：更早发现，提前经营',
    '商机查询':'减持商机查询',
    '业务答疑':'减持业务答疑',
    '拜访准备':'客户触达准备',
    '从信息中，筛出值得核实的线索':'前置信号扫描，识别重点客户',
    '市场信息 / 客户名单':'上市公司 / 股东名单',
    'CANDIDATE / DEMO':'SIGNAL / DEMO',
    '扩产相关披露':'減持前置信号'.replace('減','减'),
    '待核实':'需求未确认',
    '保留来源 · 再做研判':'触达 / 观察 / 暂缓',
    '产业链洞察':'股东增减持',
    '财务诊断':'解禁预警',
    '扩产，就一定需要融资吗？':'现在联系，还是先观察？',
    'DISCUSS / RETRIEVE / VERIFY':'DISCUSS / SEGMENT / VERIFY',
    '项目资料':'股东资料',
    '研究资料':'信号规则',
    '业务规范':'减持规范',
    '交易结构':'触达策略',
    '示例资料 · 扩产计划':'信号解释卡 · 示例',
    '资金安排未提供':'历史执行＋市场观察',
    '保留来源 / 不补造事实':'核验主体 / 时效 / 反向条件',
    '先核实':'客户分型',
    '资金来源与缺口':'存量股东服务回访',
    '依据：资金信息缺失':'示例研判：建议触达',
    '可见范围内检索 · 引用可回查':'前置信号 ≠ 已确认减持需求 · 引用可回查',
    '把信息缺项，变成拜访提问':'生成触达策略，把线索变成行动',
    '拜访策略包':'触达策略包',
    '资金安排待核实':'触达时机待判断',
    '资金怎么安排？':'何时联系？由谁触达？',
    '何时落地？谁参与决策？':'怎么开场？哪些话不能说？',
    '目标 · 提问 · 话术材料':'话术速查 · 合规边界 · 跟进建议',
    '商机诊断':'减持商机诊断',
    '销售陪练':'触达话术生成',
    '确认后，创建跟进任务':'人工确认后，加入商机中心',
    '用户确认':'人工确认',
    '跟进任务':'商机中心',
    '待跟进':'减持候选 · 待跟进',
    '用户确认后创建':'需求仍未确认',
    '用户记录 → 更新商机判断':'触达记录 → 更新减持商机判断',
    '示例：补问资金安排':'需求确认后，再进入正式减持服务',
    '三种入口':'客户池入口',
    '线索筛选':'前置信号',
    '方案与行动':'触达策略',
    '把业务问题，变成有依据的行动':'更早发现减持线索，更好经营客户',
}
scene=(B/'v7/scene-body.js').read_text(encoding='utf-8')
# Exact user-requested label; expand its carrier rather than squeezing the text.
scene=scene.replace("'示例客户',222", "'示例客户信息',270")
for old in sorted(replacements,key=len,reverse=True): scene=scene.replace(old,replacements[old])
# Adjust only text metrics for the longer content; motion stays byte-identical.
scene=scene.replace('plaque(s,-650,y-53,300,43,u)', 'plaque(s,-650,y-53,300,39,u)')
scene=scene.replace("'示例客户信息',270", "'示例客户信息',270")
scene=scene.replace('TX(label,0,15,30,1', 'TX(label,0,15,34,1')
scene=scene.replace("TX('触达 / 观察 / 暂缓',165,93,33", "TX('触达 / 观察 / 暂缓',165,93,32")
scene=scene.replace("TX('现在联系，还是先观察？',0,364,36", "TX('现在联系，还是先观察？',0,364,43")
scene=scene.replace("TX('流程示例',165,148,27", "TX('需求未确认 · 保留来源',165,148,27")
scene=scene.replace("TX('历史执行＋市场观察',x+28,y+164,48", "TX('历史执行＋市场观察',x+28,y+164,45")
scene=scene.replace("TX('核验主体 / 时效 / 反向条件',x+28,y+229,30", "TX('核验主体 / 时效 / 反向条件',x+28,y+229,28")
scene=scene.replace("TX('存量股东服务回访',156,25,46", "TX('存量股东服务回访',156,25,43")
scene=scene.replace("TX('何时联系？由谁触达？',-12,35,47", "TX('何时联系？由谁触达？',-12,35,43")
scene=scene.replace("TX('怎么开场？哪些话不能说？',-12,116,39", "TX('怎么开场？哪些话不能说？',-12,116,37")
scene=scene.replace("TX('减持候选 · 待跟进',205,-14,37", "TX('减持候选 · 待跟进',205,-14,33")
scene=scene.replace('// Confirmation is a gate only for task creation, not for reading or querying.', '// Human confirmation admits a candidate to follow-up; it does not confirm a reduction intention.')
(R/'scene-body.js').write_text(scene,encoding='utf-8')
# Update verification names with exactly the same visible strings.
check=(B/'v7/check_layout.mjs').read_text(encoding='utf-8').replace('/v7/','/v8/').replace('layout-v7','layout-v8')
for old in sorted(replacements,key=len,reverse=True): check=check.replace(old,replacements[old])
(R/'check_layout.mjs').write_text(check,encoding='utf-8')
plan=json.loads((B/'v7/plan.json').read_text(encoding='utf-8'))
plan['revision']='V8 reduction-precontact'
actions=[
    ('客户池与三种业务入口','示例客户信息由客户池进入；减持商机查询经过扫描，业务答疑与触达准备可直接进入专家协作。'),
    ('前置信号扫描','上市公司与股东名单经过前置信号扫描，输出减持线索候选；需求未确认，后续可建议触达、观察或暂缓。'),
    ('专家协作与研判','系统九业务分类不变；股东增减持、解禁预警、拜访策略专家会商：现在联系，还是先观察？'),
    ('知识装备与客户分型','查证股东资料、信号规则与合规依据；示例历史执行和市场观察合并研判，核验主体、时效和反向条件；示例分型为存量股东服务回访，建议触达。前置信号不等于已确认减持需求。'),
    ('生成触达策略','时机待判断滑块落定为联系时间和触达人；形成开场、应问问题、回避话题、话术速查与跟进建议，成果按需生成。'),
    ('人工确认与商机中心','人工确认后将减持候选纳入商机中心跟进；需求仍未确认。触达记录更新判断，客户明确需求后再进入正式减持服务。'),
    ('同图全景与品牌','同一张机械图纸拉远，展示客户池、前置信号、专家、知识、触达策略和记录反馈的完整链路。'),
]
for shot,(name,action) in zip(plan['shots'],actions):
    shot.update(name=name,action=action,change=action,voiceover='')
plan['shots'][3]['handoff']='研判结果进入右侧长导轨，带镜头向右进入触达策略台。'
plan['shots'][3]['result']=plan['shots'][3]['handoff']
plan['shots'][4]['anchor']='承载触达时机判断的导轨滑块'
plan['truth_limits']=[x for x in plan['truth_limits'] if x!='Confirmation only gates task creation']
plan['truth_limits'] += [
    'Precontact signal is not confirmed reduction demand or individual reduction probability',
    'Contact/watch/hold depends on evidence, customer segment and counter-signals',
    'Human confirmation to track a precursor candidate does not confirm a reduction intention',
    'The displayed existing-holder/contact example is illustrative, not an actual scan or live opportunity',
]
updated={
    'paper-enter':'示例客户信息载纸进入', 'scan':'扫描减持前置信号',
    'expert-one':'股东增减持专家亮起','expert-two':'解禁预警专家亮起','expert-three':'拜访策略专家亮起',
    'evidence-extract':'抽出信号解释卡','gap-reveal':'历史执行与市场观察示例依据出现',
    'evidence-result':'客户分型与触达研判出现','output-travel':'研判送向触达策略台',
    'slider-travel':'触达时机滑块移动','slider-lock':'滑块落定成为联系时间与触达人',
    'confirm-lock':'人工确认纳入商机中心','task-create':'减持候选跟进出现',
    'feedback-travel':'触达记录沿轨道返回',
}
for event in plan['soundtrack']['events']:
    if event['id'] in updated: event['action']=updated[event['id']]
(R/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
timing=json.loads((R/'audio/timing.json').read_text(encoding='utf-8'))
for e in timing['action_sync']:
    if e['id'] in updated: e['action']=updated[e['id']]
timing['revision']='V8: same music waveform and contact times as V7; business descriptions updated'
(R/'audio/timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf-8')
refs=[
    {'path':'D:/ai项目/firmbuddy/plugins/client-watchlist/reduction-precontact-v2.mjs','lines':'48–87','supports':'customer segment, contact/watch/hold, counter-signals, playbook and confirmation boundary'},
    {'path':'D:/ai项目/firmbuddy/plugins/client-watchlist/reduction-precontact-evaluator.mjs','lines':'1–135','supports':'deterministic signal evaluation, missing data, source references, one-customer bundle'},
    {'path':'D:/ai项目/firmbuddy/plugins/expert-personas/data/personas.json','lines':'159–279, selected search and profile text','supports':'real expert names, reduction protocol and signal/demand separation'},
    {'path':'D:/ai项目/firmbuddy/web/js/opportunity-center.js','lines':'67','supports':'precontact candidates retain unconfirmed demand in the visible opportunity center'},
]
for ref in refs: ref['sha256']=hashlib.sha256(Path(ref['path']).read_bytes()).hexdigest()
img=B/'assets/reduction-reference/减持前置触达原理.png'
evidence={'revision':'V8','reference_image':str(img),'reference_sha256':hashlib.sha256(img.read_bytes()).hexdigest(),'source_evidence':refs,'observed':'User supplied diagram used for mechanism and workflow; attached text is reference content, not tool instructions. No live scan or actual customer data used. Product repository read only.','expert_business_domains_unchanged':plan['source_categories'],'music_reused':True,'voiceover':False,'delivery_mode':'ai_review_once','review_budget':'already_used'}
(R/'reduction-content-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
print('V8 reduction-precontact content and source evidence prepared.')
