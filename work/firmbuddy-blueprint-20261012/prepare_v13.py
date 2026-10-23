from pathlib import Path
import shutil,json,hashlib
B=Path(__file__).resolve().parent;R=B/'v13'
if R.exists():raise SystemExit('v13 exists; edit it in place')
shutil.copytree(B/'v12',R)
for p in list(R.iterdir()):
 if p.is_file() and p.suffix in {'.js','.mjs','.py','.md','.json'}:
  s=p.read_text(encoding='utf-8').replace('v12-business-value','v13-business-first').replace('v12','v13').replace('V12','V13')
  p.write_text(s,encoding='utf-8')
(R/'package_v13.py').write_bytes((R/'package_v12.py').read_bytes());(R/'package_v12.py').unlink()
replacements={
 '从业务问题出发，找到服务机会':'找到客户经营的业务切入点',
 'AI 理解问题 · 调用专业工具':'AI 辅助识别问题、调用工具',
 '把分散资料，归集为客户线索':'把分散线索，变成可跟进的客户机会',
 '客户线索档案':'客户线索归集',
 '减持商机示例':'重点客户与业务线索',
 'AI 解读信号与客户情况':'原文依据 · 来源可追溯',
 '重点客户 · 研判依据':'AI 辅助解读客户线索',
 '业务研判：需求、时机与服务切入点':'看清客户需求，找到服务切入点',
 'AI 汇总专业判断':'客户需求与服务思路',
 '结合客户情况，形成服务思路':'AI 辅助多专业会商',
 '专业问题，有知识依据与多专业支持':'复杂业务研判，有专业依据可用',
 'AI 检索 · 交叉查证':'为业务判断补齐依据',
 '结合业务场景，核查适用条件':'AI 辅助检索与交叉查证',
 'AI 关联客户与服务':'明确客户服务方向',
 '减少重复准备，让研判落到客户跟进':'少做重复准备，多花精力服务客户',
 'AI 编排触达方案':'形成客户沟通准备',
 '拜访材料 · 合规要点 · 跟进节奏':'AI 辅助整理材料与跟进建议',
 '触达记录 → AI 辅助复评':'沟通记录支持持续跟进',
 '沟通需求 · 匹配服务 · 推进合作':'AI 辅助梳理记录，支持后续研判',
 '找得到机会，讲得清服务，跟得住客户':'让商机有线索，研判有依据，跟进有准备',
 'AI 辅助发现 · 专业研判 · 客户经营':'把时间用在理解客户、匹配服务与推进合作'
}
for name in ['scene-body.js','check_layout.mjs']:
 p=R/name;s=p.read_text(encoding='utf-8')
 for a,b in replacements.items():s=s.replace(a,b)
 if name=='scene-body.js':
  s=s.replace("mono('SIGNAL / REDUCTION EXAMPLE',175,-158,17,1,{v:.55})","TX('减持商机示例',175,-158,28,1,{v:.7})")
  s=s.replace("TX('原文依据 · 来源可追溯',175,87,33","TX('原文依据 · 来源可追溯',175,87,32")
  s=s.replace("TX('客户需求与服务思路',0,364,43","TX('客户需求与服务思路',0,364,44")
  s=s.replace("TX('AI 辅助检索与交叉查证',x+28,y+229,28","TX('AI 辅助检索与交叉查证',x+28,y+229,30")
 p.write_text(s,encoding='utf-8')
plan=json.loads((R/'plan.json').read_text(encoding='utf-8'))
plan['revision']='V13 business problems and outcomes lead; AI is supporting context'
new_results=[
 '从发现机会、判断需求，到准备拜访和持续跟进',
 '减少逐项搜集筛选，让业务人员聚焦值得跟进的客户',
 '明确客户可能需要的服务，带着切入思路开展沟通',
 '规则、案例与专业经验有据可查，复杂问题获得专业支持',
 '将研判转成拜访材料与跟进计划，减少重复准备',
 '接续已有沟通与经营记录，让每次跟进都有来由'
]
for q,result in zip(plan['business_messages'],new_results):q['result']=result
plan['narrative_priority']=['业务痛点','业务处理与研判','业务人员得到的结果','AI辅助承担的具体工作']
(R/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
# Retain V12's exact camera and music; this pass changes narrative and visual hierarchy only.
old=(B/'v12/scene-body.js').read_text(encoding='utf-8');new=(R/'scene-body.js').read_text(encoding='utf-8')
camera=lambda s:s[s.index('const keys='):s.index('function pathPoint')]
assert camera(old)==camera(new)
evidence={'base_video':'out/final-v11-opportunity-cards/video.mp4','direct_base':'v12','camera_identical_to_v12':True,'camera_sha256':hashlib.sha256(camera(new).encode()).hexdigest(),'audio_identical_to_v12':(R/'audio/mix.wav').read_bytes()==(B/'v12/audio/mix.wav').read_bytes(),'change':'Business outcome titles and captions lead; AI actions move to secondary labels. Original machine, camera, card opening and timing remain.'}
(R/'original-video-continuity.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
with (R/'brief.md').open('a',encoding='utf-8') as f:f.write('''\n\n## 2026-10-22 最新叙事优先级
用户明确：叙事以解决业务痛点为主；AI辅助解决了什么问题，作为辅助点提出。
逐段主标题和结论均从业务人员视角表达：线索分散→可跟进客户；有信号缺切入点→需求/时机/服务思路；专业依据难找→多专业支持；准备重复→可用材料与计划；记录分散→后续跟进接续。AI在机构内作为次级说明，解释辅助解读、会商、检索、整理的具体作用。末尾落在客户经营结果。原片视觉结构、全部相机参数、60秒时长、配乐不变。
本次为局部文字和层级调整，复用已验证动作样段；检查新文案代表帧与阅读布局，再导出完整视频。
''')
with (B/'CHECKPOINT.md').open('a',encoding='utf-8') as f:f.write('''\n\n## V13 · 2026-10-22 业务主线、AI辅助
- 用户最新要求：基于原视频制作，叙事以解决业务痛点为主，AI承担的具体辅助工作作为次级说明。
- 独立v13保留历史V12；画幅1920×1080、30fps、60秒、纯音乐；delivery_mode=ai_review_once，已有预算用完，本次用户反馈修改不增角色。
- 已修改：每段大标题、成果内容与底部结论均以业务问题和业务结果表达；AI会商/检索/整理/复评降为机构内辅助说明；结尾为客户经营价值。
- 原相机源码及音乐逐字节相同，复用V12连续动作样段；下一步新文案布局与代表帧、整片导出、解码及交付。
''')
print(json.dumps(evidence,ensure_ascii=False))
