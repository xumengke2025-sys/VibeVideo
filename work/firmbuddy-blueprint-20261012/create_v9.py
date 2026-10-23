from pathlib import Path
import shutil,json,hashlib
B=Path(__file__).resolve().parent
R=B/'v9'
assert not R.exists(), 'V9 already exists; do not overwrite'
shutil.copytree(B/'v8',R,ignore=shutil.ignore_patterns('__pycache__','premix.wav','revise_content.py'))
s=(R/'scene-body.js').read_text(encoding='utf-8')
changes={
 '减持业务答疑':'业务问题答疑', '客户触达准备':'客户拜访准备',
 '自然语言 · 随时进入':'AI 理解问题 · 调用专业工具',
 '前置信号扫描，识别重点客户':'规则扫描前置信号，AI 解读线索',
 '需求未确认 · 保留来源':'原文依据 · 来源可追溯',
 '需求未确认':'AI 解读：重点客户',
 '数十位 AI 专家 · 按议题协作':'专业化 AI 专家团 · 按议题协作',
 '现在联系，还是先观察？':'AI 汇总多专业研判',
 '示例议题':'规则解读 · 时机研判 · 触达建议',
 '知识库 · 已装配的专业资料':'多源知识库 · 专家专业能力底座',
 "['股东资料','信号规则','减持规范','触达策略','风险合规','案例档案']":"['核心规范','监管规则','产品能力','案例经验','研究资料','补充资料']",
 '预先装配 / 按范围检索':'专业装配 / 按需检索',
 '信号解释卡 · 示例':'AI 检索 · 交叉查证',
 "TX('客户分型',156,-45,43":"TX('AI 辅助客户分型',156,-45,39",
 '示例研判：建议触达':'示例策略：服务回访',
 '前置信号 ≠ 已确认减持需求 · 引用可回查':'规则依据 · 业务经验 · 原文引用',
 '生成触达策略，把线索变成行动':'AI 生成触达策略，把线索变成行动',
 '触达时机待判断':'AI 编排触达方案',
 '何时联系？由谁触达？':'联系时机 · 负责人建议',
 '怎么开场？哪些话不能说？':'开场话术 · 沟通重点',
 '话术速查 · 合规边界 · 跟进建议':'话术速查 · 合规要点 · 跟进节奏',
 '人工确认后，加入商机中心':'人工审核入库，持续经营客户',
 "plaque('人工确认'":"plaque('人工审核'",
 '减持候选 · 待跟进':'减持线索 · 客户经营',
 '需求仍未确认':'触达准备 · 跟进服务',
 '触达记录 → 更新减持商机判断':'触达记录 → AI 辅助复评',
 '需求确认后，再进入正式减持服务':'沟通需求 · 匹配服务 · 推进合作',
 "plaque('专家协作'":"plaque('专业专家团'",
 "plaque('知识库'":"plaque('知识装备库'",
 '更早发现减持线索，更好经营客户':'专业知识驱动，让 AI 贯穿客户经营',
}
for a,b in changes.items():
 assert a in s,a
 s=s.replace(a,b)
s=s.replace("TX('规则解读 · 时机研判 · 触达建议',0,415,26", "TX('规则解读 · 时机研判 · 触达建议',0,415,35")
s=s.replace("mono('DISCUSS / SEGMENT / VERIFY',-1110,610,23,1,{v:.55});", """// Knowledge equipment supplies the specialist seats. Each clutch engages on an existing music beat.
 const foundations=['专业知识装备','业务方法沉淀','培养与试炼'];
 foundations.forEach((label,i)=>{const x=-1045+i*710,u=show(12.1+i*.4,.4);
   plaque(label,x,555,670,44,u);
   const seat=chosen[i],port=[x+335,555],side=i===0?-1170:i===2?1170:380;
   route([port,[port[0],515],[side,515],[side,seat[1]+55],[seat[0],seat[1]+55],[seat[0],seat[1]+31]],12.1+i*.4,12.5+i*.4,2.8,.72);
 });""")
# Tie scanner mechanics to an interpretation result and retain the original scan musical accent.
s=s.replace("TX('原文依据 · 来源可追溯',165,148,27,show(6.4),{v:.7});", "TX('原文依据 · 来源可追溯',165,148,31,show(6.4),{v:.8});route([[-52,52],[55,52],[55,-79],[128,-79]],5.9,6.3,3,.85);")
(R/'scene-body.js').write_text(s,encoding='utf-8')
for f in ['render.mjs','check_layout.mjs','check_motion.mjs','setup.py','collect_delivery.py','package_delivery.py','contact_sheet.py','package.json']:
 p=R/f
 if p.exists():
  t=p.read_text(encoding='utf-8').replace('v8-reduction','v9-expert-ai').replace('v8-content','v9-content').replace('layout-v8','layout-v9').replace('/v8/','/v9/').replace('V8','V9').replace('v8/','v9/').replace('MANIFEST-v8','MANIFEST-v9')
  for a,b in changes.items():t=t.replace(a,b)
  if f=='collect_delivery.py':
   t=t.replace("B/'v7/scene-body.js'", "B/'v8/scene-body.js'").replace("B/'v7/audio/mix.wav'", "B/'v8/audio/mix.wav'").replace('_from_v7','_from_v8')
   t=t.replace("times=[2.6,7.6,15.5,21.5,24.8,31.5,33.8,39.9,42.6,44.6,47.8,50.8]", "times=[2.6,7.6,15.5,21.5,24.8,31.5,33.8,39.9,42.6,44.6,47.8,50.8]")
   t=t.replace("times=[2.6", "assert all(term not in new for term in ['未确认','不能确认','待需求方确认','待判断'])\nassert all(term in new for term in ['专业知识装备','业务方法沉淀','培养与试炼','AI 理解问题','AI 解读','AI 汇总','AI 检索','AI 生成','AI 辅助复评'])\ntimes=[2.6")
  if f=='package_delivery.py':
   t=t.replace("B/'v7/scene-body.js'", "B/'v8/scene-body.js'").replace("B/'v7/audio/mix.wav'", "B/'v8/audio/mix.wav'")
   t=t.replace("'revise_content.py','source-package.json'", "'revise_content.py','source-package.json','reduction-content-evidence.json'")
  p.write_text(t,encoding='utf-8')
p=R/'check_layout.mjs';t=p.read_text(encoding='utf-8')
t=t.replace("'拜访策略']}","'拜访策略','AI 汇总多专业研判','专业知识装备','业务方法沉淀','培养与试炼']}")
t=t.replace("'减持线索 · 客户经营','触达记录", "'减持线索 · 客户经营','触达准备 · 跟进服务','触达记录")
t=t.replace("'减持前置信号','AI 解读：重点客户'", "'减持前置信号','AI 解读：重点客户'")
# Array literal substitution in scene uses single token; check list needs independent names.
t=t.replace("'股东资料','信号规则','减持规范','触达策略','风险合规','案例档案'", "'核心规范','监管规则','产品能力','案例经验','研究资料','补充资料'")
t=t.replace("'客户分型'", "'AI 辅助客户分型'").replace("'人工确认'", "'人工审核'").replace("'专家协作','知识库'", "'专业专家团','知识装备库'")
p.write_text(t,encoding='utf-8')
plan=json.loads((R/'plan.json').read_text(encoding='utf-8'))
actions=[
 'AI 理解自然语言，调用相应专业工具；三入口覆盖减持商机查询、业务问题答疑与客户拜访准备。示例客户信息进入统一流水线。',
 '确定性规则扫描上市公司和股东资料；AI 解读前置信号及原文依据，形成重点客户研判，保留触达、观察、暂缓三类业务动作。',
 '九业务分类的专业化AI专家团；知识装备、业务方法、培养试炼依次接入专家席位；股东增减持、解禁预警、拜访策略专家点亮，AI 汇总多专业研判。',
 '六槽知识装备：核心规范、监管规则、产品能力、案例经验、研究资料、补充资料。AI 按专业范围检索，交叉查证历史执行和市场观察，辅助客户分型，引用可定位原文。',
 'AI 编排触达策略，生成联系时机、负责人建议、开场话术、沟通重点、合规要点和跟进节奏，按需形成可执行成果。',
 '人工审核将减持线索纳入商机中心；触达记录进入反馈回路，AI 辅助复评，业务人员沟通需求、匹配服务并推进合作。',
 '连续拉远揭示专业专家团、知识装备库、工具与业务流程组成的一台整机；专业知识驱动，让AI贯穿客户经营。'
]
for shot,action in zip(plan['shots'],actions):
 shot['action']=shot['change']=action
 shot['understanding']=action
plan['revision']='V9 professional-expert-and-AI'
plan['professional_expert_basis']=['专业角色与业务方法','版本化知识装备','材料驱动培养','试炼和人工发布']
plan['ai_workflow']=['理解问题和调用工具','解读扫描结果','专业专家协作研判','检索与交叉查证','辅助客户分型','生成行动成果','记录反馈与辅助复评']
plan['facts']={'training':'知识装备、专业工作协议与培养试炼；不宣称模型参数微调','scan':'确定性规则求值；AI负责解释和策略生成','feedback':'记录辅助复评；不宣称自动改模型或规则','display_policy':'业务状态采用正向动作，人工审核仍保留'}
(R/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
sources=[
 ('D:/ai项目/firmbuddy/README.md',[3,17],'专家体系、工具调用、多专家会商与知识装备'),
 ('D:/ai项目/firmbuddy/项目相关文本与素材/历史规划与设计/docs/PLAN-FIRMBUDDY-V2.md',[174,237],'早期整体需求，结合当前实施文档解读'),
 ('D:/ai项目/firmbuddy/项目相关文本与素材/工程规划与执行/AI-EXECUTION-PLAN.md',[24,24],'客户经营链路整体目标，历史计划不当已实现证据'),
 ('D:/ai项目/firmbuddy/docs/implementation/M12-KNOWLEDGE-EQUIPMENT-2026-09-15.md',[29,85],'六槽专业装备、专家培养/试炼、专业方法和知识检索'),
 ('D:/ai项目/firmbuddy/docs/implementation/KNOWLEDGE-OPTIMIZATION-20260929.md',[24,34],'多源知识目录、中文全文检索与可追溯引用'),
 ('D:/ai项目/firmbuddy/docs/implementation/REDUCTION-PRECONTACT-V2-20260922.md',[3,38],'专业打法、真实知识引用、客户分型与确定性扫描'),
 ('D:/ai项目/firmbuddy/src/experts/training-service.mjs',[195,245],'材料驱动培养建议与受控字段'),
 ('D:/ai项目/firmbuddy/plugins/knowledge-system/plugin.mjs',[42,50],'实际知识检索工具与真实引用约束'),
]
e={'revision':'V9','product_read_only':True,'sources':[{'path':p,'read_lines':r,'purpose':why,'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()} for p,r,why in sources],'wording':plan['facts'],'ai_chain':plan['ai_workflow'],'motion':'V8 camera and paths preserved; knowledge equipment clutches timed to existing expert selection beats at 12.1/12.5/12.9s','delivery_mode':'ai_review_once','review_budget':'already_used; no new roles'}
(R/'professional-ai-content-evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2),encoding='utf-8')
with (B/'CHECKPOINT.md').open('a',encoding='utf-8') as f:
 f.write('\n## V9 专业专家团与AI全过程（制作中）\n- 用户要求：强调知识与培养支撑的专业专家团，讲清AI全过程作用；删除否定式需求状态。\n- 依据：只读核对产品README、整体规划、M12专家培养/知识装备、知识优化、减持V2；事实依据在v9/professional-ai-content-evidence.json。\n- v9独立工程已建立；52秒、1920×1080、30fps、纯音乐。保留相机与机械路线，新增知识装备到专家席位的卡点接合。\n- delivery_mode: ai_review_once，历史预算已用，不增角色；后续由用户反馈。\n- 下一步：重建film，必要文字布局与正式帧检查，完整渲染、解码并打包。\n')
print('V9 prepared',R)
