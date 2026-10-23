from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;B=R.parent;O=B/'out/final-v14-burden-journey'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
media=read(O/'evidence.json');checks=read(O/'delivery-checks.json');journey=read(B/'out/journey-v14-checks.json');stills=read(B/'out/stills-v14-checked/checks.json');sample=read(B/'out/sample-v14-unload-transfer/evidence.json');facts=read(R/'opportunity-logic-evidence.json');plan=read(R/'plan.json');audio=read(R/'audio/timing.json')
signature=hashlib.sha256(b''.join((R/f).read_bytes() for f in ['film.js','vendor/draw.js','vendor/paper.js','plan.json','audio/mix.wav'])).hexdigest()
assert signature==media['signature']==sample['signature']
assert checks['duration']==90 and checks['frames']==2700 and checks['decode']
assert not journey['errors'] and not journey['issues']
assert not stills['errors'] and all(s['identical'] for s in stills['seeks'])
assert len(journey['burdenWindows'])==6 and all(w['counts'][0]-w['counts'][-1]==1 for w in journey['burdenWindows'])
assert sorted(w['counts'][-1] for w in journey['burdenWindows'])==list(range(6))
assert all(x['lag_samples']==0 for x in checks['aac_alignment'])
assert not audio['voiceover'] and audio['duration']==90
for src in facts['sources']:assert hashlib.sha256(Path(src['path']).read_bytes()).hexdigest()==src['sha256']
assert hashlib.sha256((B/'out/final-v13-business-first/video.mp4').read_bytes()).hexdigest()=='98285081189f9ba8751fd847e95d585cb12a346549054dbde2c265d05fb1fc8f'
checks['visual_observation']={
 'reviewer':'production agent; no new independent review',
 'final_contact_sheet_actually_viewed':True,
 'final_sample_times':checks['extracted_final_times'],
 'final_full_size_frames_actually_viewed':[5,39.5],
 'source_six_unloads_contact_sheet_actually_viewed':True,
 'formal_sample_contact_sheet_actually_viewed':{'start':19.6,'end':27.5666667,'step':.5,'last_extra':27.5666667},
 'observed':'Six burden boxes visibly leave the same person in sequence; figure straightens and carries a preparation case. New logic station displays four scenario families, sources, judgement factors and service directions. Original machine, cards and auditorium remain.',
 'full_normal_speed_playback':False,
 'complete_actual_listening':False,
}
(O/'delivery-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
requirements=[
 ('约一分半、1920×1080横屏', 'ffprobe.json + evidence.json: 90 seconds, 2700 frames, 30fps, 1920×1080'),
 ('前面用小人背负多项业务负担', 'Final MP4 5-second full-size decoded frame actually viewed; six labeled loads on business figure'),
 ('经过后续每个业务环节逐项减负', 'Final decoded before/mid/after frames of all six unloads actually viewed; journey-v14-checks confirms counts 6→5→4→3→2→1→0'),
 ('新增各种商机判断逻辑与来源环节', 'Final MP4 28/33/39.5s viewed; 39.5s full-size: financing, M&A, shareholder, risk/crossborder source→logic→service mapping'),
 ('基于FirmBuddy项目实际理解', 'opportunity-logic-evidence.json records actual read paths/lines/hash; source hashes rechecked; product rules include phase filtering, identity/windows, consideration, exposure/currency'),
 ('基于原视频保留机械蓝图与专家会场', 'Final contact sheet across complete narrative; V13 MP4 hash unchanged; world geometry and paper engine retained'),
 ('连续运镜与减负动作', '19.6–27.6s formal 1080p sample; actual sequential contact sheet inspection; numerical detour continuity checks'),
 ('纯音乐与动作落点', '90s instrumental generated without speech assets; six cue ledger events and six encoded audio windows show zero-sample lag; not an actual listening claim'),
]
audit=dict(video_sha256=media['sha256'],signature=signature,requirements=[dict(requirement=r,evidence=e,status='verified_with_stated_scope') for r,e in requirements],historical_versions_preserved=True,limitations=['No new independent review; historic budget used','Not full normal-speed playback or full actual listening'],production_complete=True)
(O/'completion-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
with (B/'CHECKPOINT.md').open('a',encoding='utf-8') as f:f.write(f'''
### V14 完成交付 · 2026-10-22
- 成片：out/final-v14-burden-journey/video.mp4；90秒、1920×1080、30fps、2700帧、H264/AAC双声道纯音乐。
- 小人背负六项业务负担进入原机械蓝图；在资料归集、商机判断、专家协作、知识查证、跟进准备、经营记录六个业务环节逐项卸载，身体逐渐站直，最终轻装携带准备包。
- 新增左下商机判断工位：融资、并购、股东服务、风险与跨境的信号来源→判断要点→服务方向；融资阶段过滤、东方财富公告/巨潮回核、解禁日历/客户资料均有项目依据。AI作为辅助说明。
- 原抽卡、世界绘图、专家会场、九业务分类、六知识槽保留；原配乐音色重写为90秒150BPM节奏，六次卸载有共享时间轴声音落点。
- 实际查看：六次卸载前/中/后源码接触表；19.6–27.6秒正式样段每0.5秒连续接触表；最终MP4 24帧接触表及5/39.5秒原尺寸解码帧。
- 工程检查：完整音视频解码、规格通过；9组主要文字读窗与六次负担状态检查无问题；新增相机连接位置连续；3次乱序寻址一致；6处编码音频对齐均0采样偏移。未完整正常速度观看、未完整实际听音，不称独立视听验收。
- 成片SHA256：{media['sha256']}；源签名：{signature}。
- 正式样段：out/sample-v14-unload-transfer/video.mp4；240帧、1080p，整片复用同源帧。效果图：out/stills-v14-checked；事实依据：v14/opportunity-logic-evidence.json；需求核对：out/final-v14-burden-journey/completion-audit.json。
- delivery_mode:ai_review_once；历史预算已用，本次反馈改版无新增角色。V13历史哈希不变，产品工程只读。
- 交付源码包：FirmBuddy-source-v14-burden-journey.zip。下一步：展示成片与源码，由用户反馈。
''')
print(json.dumps({'requirements_verified':len(requirements),'source_signature':signature,'video_sha256':media['sha256']},ensure_ascii=False))
