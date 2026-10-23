from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;out=R/'out/final-v1';qa=R/'qa'
e=json.loads((out/'evidence.json').read_text(encoding='utf-8'))
b=json.loads((R/'brief.json').read_text(encoding='utf-8'));b['review']['current_sha256']=e['sha256'];b['review']['maker_inspection']='15 representative rendered frames and six consecutive transition contact sheets; no actual audio listening or realtime viewing'
(R/'brief.json').write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf-8')
q=json.loads((qa/'maker-inspection-index.json').read_text(encoding='utf-8'));q['actual_viewed']=True;q['video_sha256']=e['sha256'];q['method']='Viewed rendered-source representative PNGs via contact sheet and consecutive JPEG frames for all six cuts; not decoded-video full-frame review';q['finding']='Text-free representative images; diagonal reveal advances continuously, no full-frame blank flash or crossfade ghosting visible in inspected windows.'
(qa/'maker-inspection-index.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'CHECKPOINT.md').write_text(f'''# 宝宝30秒无字版
- delivery_mode: ai_review_once（沿用；一轮预算已在60秒版本用完）
- 用户要求：加快至30秒、画面完全无文字、转场顺畅，已完成。
- 保留认可head-atlas与肤色#f8c28b；移动为爬行。
- 独立变体保留原60秒源码与成片。
- 去除文字绘制API、标题、字母、数字、标签、印章；书页模拟文字改图形。
- outputTime*2；六处0.56秒斜向纸页擦拭；音乐与拟音atempo=2、保持音高。
- 交付out/final-v1/video.mp4：1080×1920、24fps、30.0秒、720帧、AAC音轨；完整音视频解码无错。
- 成片SHA256：{e['sha256']}
- 制作实际查看15幅代表帧及全部六处切口连续接触表；证据qa/maker-inspection-index.json。仅为制作检查，非新增独立审核。
- 正常速度观看/实际听音未完成，不称完整视听通过。
- 当前完成：待用户反馈；不继续自动审美返工。
''',encoding='utf-8')
source=(R/'film.mjs').read_text(encoding='utf-8');assert all(x not in source for x in ['fillText','strokeText','function text(','function tag(','function stamp('])
print(json.dumps({'duration':30,'size':'1080x1920','frames':720,'sha256':e['sha256'],'text_drawing_api_absent':True,'source_frame_windows_viewed':6},ensure_ascii=False))
