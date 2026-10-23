"""Bind current candidate and production records to verified encoded output."""
from pathlib import Path
from datetime import datetime
import json
ROOT=Path(__file__).resolve().parent
report=json.loads((ROOT/'delivery/engineering-check-v8.json').read_text(encoding='utf8'))
p=ROOT/'CHECKPOINT.json';d=json.loads(p.read_text(encoding='utf8'))
d['updated_at']=datetime.now().isoformat(timespec='seconds')
d['status']='v8_candidate_ready_review_in_progress'
d['render_session_id']=None
d['final_candidate']=report['video'];d['final_candidate_sha256']=report['sha256']
d['render_resume']['current_completed_frames']=1344
d['verification']['render']='v8全部1344帧完成；1080×1920、24fps、56秒；完整音视频解码成功，无解码错误。'
d['verification']['independent_review']='同一既有审片角色正在查看v8实际输出；旧v7覆盖不继承。实际听音工具不可用。'
d['v8_visual_validation']['pending']='整片独立画面检查进行中，实际听音不可用'
d['v8_frame_evidence']='qa/v8/full-film/frame-audit.json'
d['unresolved']=['v8独立审核实际覆盖与缺陷待保存','无法实际听音，不能声称完整视听通过']
d['next_action']='同一审片角色完成可做检查；核对当前成片哈希与报告，必要时按证据最多修复一次，交付可播放版本并说明听音限制。'
entry='v8完成全部1344帧、56秒音画编码与完整解码检查；45页连续帧证据已导出，交同一审片角色续接。'
if entry not in d['completed']:d['completed'].append(entry)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
ad=ROOT/'source-adoption.json';a=json.loads(ad.read_text(encoding='utf8'))
a['verification']['v8']='真实完成1344帧1080×1920 Cycles渲染与56秒音画编码，完整解码无错误；已导出45页全帧证据，独立画面检查进行中。实际听音不可用。'
ad.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'candidate_ready':True,'sha256':report['sha256']}))
