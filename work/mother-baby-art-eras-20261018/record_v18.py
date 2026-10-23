from pathlib import Path
import json
R=Path(__file__).resolve().parent;Q=R/'qa/v18'
m=R/'assets/motion-v18/manifest.json';d=json.loads(m.read_text());d['route']='Whole-pair crown-to-seat height registration, anchored seat baseline, dual-matte RGBA reconstruction including enclosed gaps';m.write_text(json.dumps(d,indent=2))
report={'version':18,'delivery_mode':'ai_review_once','independent_review':'Historical one-round budget exhausted; this is targeted production verification following user feedback, not a new independent review','fixes':['Whole-pair crown-to-seat normalization, fixed baseline, no independent limb deformation','Black/white matte interpolation and RGBA reconstruction; enclosed gaps remain transparent'],'viewed':['alpha-before-after.jpg: scene00 F12/F26, bridge19 F12, scene19 F24','scale-board-0..3.jpg: all20 eras at F0/12/24/36/47','bridge-overview-0..3.jpg: all19 connections at five samples each'],'observations':['The inspected enclosed white wedges and exterior white fringe are removed, with white clothing preserved','Overall seated height is stable in sampled drawings; infant lean and source drawing proportions still vary','Cross-style bridge midpoints retain visible soft blending/ghosting of costumes and props'],'limits':['No claim of normal-speed full-film aesthetic review','Crown-height measurement is not anatomical proportion validation','Final encoded evidence pending']}
(Q/'production-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
p=R/'CHECKPOINT.md';s=p.read_text(encoding='utf8');idx=s.index('# 历史 v17')
s='''# v18：尺寸稳定与人物白底修复（2026-10-22）

- aspect_ratio=9:16; width=1080; height=1920; fps=24; duration=40; 20时代；有意无声。
- delivery_mode=ai_review_once；历史一轮已用完，本次定向制作检查，不新增审片角色。
- 20场48帧动作、19连接已全部重建；完整双人按发顶到座位高度校准，固定基线；黑白双底补帧后重建RGBA，修复封闭白块。
- 39图集1291姿态边界/哈希检查0问题；实际烘焙发顶到基线389–391px，相邻最大1px。qa/v18/scale-check.json。
- 已实看20时代各5姿态、19连接各5姿态及白底修复对比。白块消除，坐姿总体尺度稳定；风格连接中间态仍存在服装/道具软化重影，婴儿内部绘画比例会变化。
- 下一步：浏览器动作/背景端点检查、正式渲染、编码后抽帧、打包解包运行；无新一轮独立或正常速度全片审美审核声明。

'''+s[idx:];p.write_text(s,encoding='utf8')
print('Checkpoint and targeted review updated')
