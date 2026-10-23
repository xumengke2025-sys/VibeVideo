"""Record resumed production without resetting previous evidence or review budget."""
from pathlib import Path
from datetime import datetime
import json
ROOT=Path(__file__).resolve().parent
p=ROOT/'CHECKPOINT.json';d=json.loads(p.read_text(encoding='utf8'))
s=json.loads((ROOT/'render/pipeline-status-v8.json').read_text(encoding='utf8'))
d['updated_at']=datetime.now().isoformat(timespec='seconds')
d['status']='v8_full_rendering' if s['stage']=='rendering' else s['stage']
d['render_session_id']=43542
d['render_resume']={'source_hashes_verified':True,'existing_valid_frames':680,'current_completed_frames':s['completed_frames'],'total_frames':1344,'fix':'Initialize completed_frames before reporting skipped batches; visual sources unchanged.'}
d['next_action']='补齐v8缺失帧；编码56秒成片、完整解码检查，交同一审片角色续接，保存实际覆盖与听音限制后交付。'
d['verification']['assets']='model/babylon-city-v8.blend：保留10972座远景院落、连贯大道和运河，新增蓝釉长墙、王宫、台地花园、王神雕像、居民、驮畜与商船。'
d['verification']['audio']='v8采用用户原曲29.5–85.5秒，0.15秒渐入、53–56秒渐出，低混环境声；能量/起音仅为候选定位，实际听音未完成。'
d['unresolved']=['v8全片剩余帧与成片编码待完成','新版审核覆盖待记录；原审片角色已确认可续接','无实际音频感知能力，不能声称听音通过']
entry='续接验证680张既有PNG与冻结源码一致，修复断点续渲进度记录初始化错误，恢复剩余帧渲染。'
if entry not in d['completed']:d['completed'].append(entry)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'status':d['status'],'completed':s['completed_frames'],'total':1344}))
