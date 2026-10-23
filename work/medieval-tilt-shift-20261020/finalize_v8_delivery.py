from pathlib import Path
from datetime import datetime
import json
ROOT=Path(__file__).resolve().parent
e=json.loads((ROOT/'delivery/engineering-check-v8.json').read_text(encoding='utf8'))
review_path=ROOT/'qa/v8/av-review.json'
review=json.loads(review_path.read_text(encoding='utf8')) if review_path.exists() else None
current=bool(review and review.get('video_sha256')==e['sha256'])
status={'video':e['video'],'sha256':e['sha256'],'engineering':'passed; 1344 decoded frames, 56s, 1080x1920, 24fps, stereo audio','review':'incomplete','independent_visual_coverage':review.get('coverage',{}) if current else {},'actual_audio_listening':'unavailable','note':'仅采用当前成片哈希绑定的审片记录；未落盘范围不推断为已审。保留同一审片角色的晚到结果。','updated_at':datetime.now().isoformat(timespec='seconds')}
(ROOT/'delivery/delivery-status-v8.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf8')
text='''# 暮河城 · 移轴强化版 v8

完整视频：暮河城-巴比伦巨城-Dream-of-Babylon-v8.mp4。

56秒，1080×1920，24fps。强化高位俯拍、窄清晰带与前后渐变散焦；相机逐帧连续，人畜采用8Hz活动更新。增加蓝釉祭仪长墙、王宫和台地花园、王神雕像、居民、驮畜与商船。保留贯穿街区的大道、运河及桥梁。

音乐采用用户提供的《Dream Of Babylon》29.5–85.5秒连续节选。画面切换参照能量起音候选点编排；未实际听音，不保证听感验收。

工程检查已通过：1344帧和完整音轨解码无错误；尺寸、帧率、时长与48kHz双声道符合计划。视听审核未完成：旧v7结论不适用于本片；新版实际覆盖以qa/v8/中的同一审片角色报告为准。当前工具无法实际听音。依据项目约10分钟无实质审核进展即展示当前版本的规则，交付当前可播放版本并保留晚到报告，不声称完整视听通过。

可编辑模型、源码和核验入口见工程入口-v8.md。旧版成片与历史记录保留。
'''
(ROOT/'delivery/交付说明.md').write_text(text,encoding='utf8')
p=ROOT/'CHECKPOINT.json';d=json.loads(p.read_text(encoding='utf8'))
d['status']='v8_delivery_ready_review_incomplete';d['updated_at']=status['updated_at']
d['delivery_note']='v8完整可播放，工程检查通过；独立审核未完成、实际听音不可用。按本地无实质审核进展软边界交付，保留晚到结果。'
d['verification']['independent_review']='v8未完成，实际覆盖以qa/v8/av-review.json中当前成片哈希记录为准；不沿用v7。'
d['next_action']='向用户展示v8完整影片；保留同一审片者后续记录，后续按用户反馈针对性修改，不重开全面审片。'
d['unresolved']=['新版独立审核未完成，报告只认可实际覆盖','实际听音工具不可用，音乐听感与完整声画节奏未验收']
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'delivery_ready':True,'review_file_present':current,'sha256':e['sha256']}))
