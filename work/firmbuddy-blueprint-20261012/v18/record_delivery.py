"""Run only after the named final images have actually been inspected."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;B=R.parent;O=B/'out/final-v18-business-story'
e=json.loads((O/'evidence.json').read_text(encoding='utf-8'));d=json.loads((O/'delivery-checks.json').read_text(encoding='utf-8'));a=json.loads((R/'audio/timing.json').read_text(encoding='utf-8'));layout=json.loads((R/'layout-checks.json').read_text(encoding='utf-8'));motion=json.loads((R/'motion-checks.json').read_text(encoding='utf-8'))
assert e['decoded'] and not layout['issues'] and motion['pass']
assert e['sha256']==hashlib.sha256((O/'video.mp4').read_bytes()).hexdigest()
observations={'video_sha256':e['sha256'],'role':'Primary maker; not an independent review', 'method':'Full-size stills and sampled consecutive frame sheets; no full normal-speed playback', 'final_decoded_overview_times':d['extracted_final_times'],'final_full_resolution_times':[2,80,141], 'final_frame_sheets':{'opening-sequence.jpg':24,'handoff-sequence.jpg':16,'closing-sequence.jpg':24}, 'production_samples':['sample-v18-outcome','sample-v18-outcome-final','sample-v18-clutch'], 'notes':['Opening establishes a client manager and one A01 preparation task before the detailed business problems.','Source-labelled cards keep shareholder service as a selected example within general opportunity search.','Original stepped expert hall and industry research remain connected to the same client.','One dossier spreads into three outcome pages. Separated gears engage before rotating.','Closing brand appears after the gear text fades, avoiding a simultaneous text/gear crossfade.'], 'full_frame_coverage':False,'complete_actual_listening':False,'independent_review':'Historical review budget already used; no new reviewer', 'pilot_metrics':'None supplied; none invented'}
(O/'observations.json').write_text(json.dumps(observations,ensure_ascii=False,indent=2),encoding='utf-8')
d['visual_observation']='Inspected final decoded 24-frame overview, full-resolution frames at 2/80/141s, and 64 raw-render sequence samples. No full playback or listening claim.'
(O/'delivery-checks.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
text=f'''# V18 已完成 · 2026-10-23

目标：依据用户提供的比赛叙事方法，完整讲清客户经理的业务痛点、代价、单一解决路径和具体成果；保持工程蓝图风格与巧思。

交付：../out/final-v18-business-story/video.mp4
规格：154秒，1920×1080，30fps，4620帧，H264/AAC双声道，纯音乐，无配音。
video_sha256: {e['sha256']}
source_signature: {e['signature']}
aspect_ratio: 16:9
delivery_mode: ai_review_once
review_budget: historical_already_used

已完成：PDF方法全文阅读与关键页面视觉读取；产品资料核对；客户经理开场、两组具体阻点与代价；保留来源抽卡/原图专家会商/产业研判；A01三联成果页与齿轮闭合首尾呼应；154秒配乐。用户明确暂不提供试点数字，片中没有虚构提效、成交或已推广范围。

验证：完整视频与音频解码通过；135个声明文字读窗零问题；相机数值连续性通过；11个AAC片段对齐检查通过；V16/V17原文件哈希未变。最终片实际看24帧解码总览、2/80/141秒原尺寸帧、64帧连续抽样。未逐帧覆盖或完整正常速度观看，未实际完整听音，不声明新增独立审核。

源码包由package_source.py生成到../FirmBuddy-source-v18-business-story.zip，包哈希与完整性结果记录在成片目录source-package.json。活跃入口setup.py；一次性迁移脚本不重跑。

下一步：展示成片与源码，由用户反馈。没有剩余必需绘制工作。
'''
(R/'CHECKPOINT.md').write_text(text,encoding='utf-8')
master=(B/'CHECKPOINT.md').read_text(encoding='utf-8');start=master.index('## V18 ');end=master.index('## V17 ',start)
master=master[:start]+f'''## V18 业务问题与客户行动 · 2026-10-23 完成

- 154秒、1920×1080、30fps、4620帧、纯音乐；out/final-v18-business-story/video.mp4。
- 采用PDF的业务问题叙事，明确客户经理、业务代价、A01单一路径和三联成果；保留来源卡、专家厅与产业研判，新增停转齿轮接合的首尾呼应。用户未提供试点数据，本版不编造效果数字。
- 完整解码、135个文字读窗、相机连续性与11处AAC对齐检查通过，V16/V17原文件未变。已看最终解码总览24帧、原尺寸2/80/141秒与64帧连续抽样。未全片正常速度观看或完整听音；历史审核预算已用，零子代理。
- 视频SHA256：{e['sha256']}；源签名：{e['signature']}。
- 源码包：FirmBuddy-source-v18-business-story.zip；完整性与哈希见out/final-v18-business-story/source-package.json。
- 下一步：交付后由用户反馈，无必需制作工作遗留。

'''+master[end:]
(B/'CHECKPOINT.md').write_text(master,encoding='utf-8');print('Delivery observations and checkpoints recorded.')
