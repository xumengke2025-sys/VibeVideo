from pathlib import Path
from datetime import datetime
import json,hashlib
ROOT=Path(__file__).resolve().parent
e=json.loads((ROOT/'delivery/engineering-check-v9.json').read_text(encoding='utf8'))
assert hashlib.sha256(Path(e['video']).read_bytes()).hexdigest()==e['sha256']
frozen=json.loads((ROOT/'render/frozen-v9-manifest.json').read_text(encoding='utf8'))
for key,path in [('model_sha256','model/babylon-city-v9.blend'),('renderer_sha256','render_city_v9.py'),('timeline_sha256','v8-timeline.json'),('mix_sha256','audio/final-mix-v8.wav')]:
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==frozen[key],path+' changed during rendering'
rp=ROOT/'qa/v9/av-review.json';review=json.loads(rp.read_text(encoding='utf8')) if rp.exists() else None
current=bool(review and review.get('video_sha256')==e['sha256'])
findings=review.get('findings',[]) if current else []
remaining=[f for f in findings if f.get('recheck_status') not in ['resolved','fixed','closed']]
remaining_notes=[f"{f.get('id','finding')} ({f.get('severity','unclassified')}): {f.get('observation','')}" for f in remaining]
status={'video':e['video'],'sha256':e['sha256'],'engineering':'passed','specification':{'width':1080,'height':1920,'duration':56,'fps':24,'decoded_frames':1344,'audio':'48kHz stereo'},'review':review.get('verdict','incomplete') if current else 'incomplete','review_scope':'same reviewer, necessary local recheck after the one repair','coverage':review.get('coverage',{}) if current else {},'actual_audio_listening':'unavailable','repair_rounds_used':1,'max_repair_rounds':1,'source_freeze_verified':True,'updated_at':datetime.now().isoformat(timespec='seconds')}
status['remaining_findings']=remaining
(ROOT/'delivery/delivery-status-v9.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf8')
note='''# 暮河城 · 巴比伦巨城 v9

完整影片：暮河城-巴比伦巨城-Dream-of-Babylon-v9.mp4。竖屏1080×1920，56秒，24fps。

保留地平线显城、蓝釉大道、市集驮畜、运河商船、台地花园、神像与巨城全景。用高位俯拍、窄清晰带、前后渐变散焦和8Hz活动更新构成移轴微缩感；相机逐帧连续。本轮把24处石拱桥改为砖墩木梁桥，实体引坡连接两岸街道；4艘遗留三角帆船改为装载绑绳货包、配有艄公的驳船。巴比伦式城邦仍为幻想重构，非考古精确复原。

音乐为用户提供《Dream Of Babylon》29.5–85.5秒连续节选，沿用v8混音。能量起音候选用于编排；没有实际听音，不把技术测量写成高潮或节奏的听感验收。

工程检查通过：1344帧和完整音轨解码无错误，画幅、时长、帧率与48kHz双声道符合计划；冻结模型、摄影、时间表与混音的哈希已核对。沿用同一审片角色，仅复核本轮改动及相邻镜头；实际覆盖见qa/v9/av-review.json。全片独立画面覆盖及实际听音未完成，不能写完整视听审核通过。

工程入口见工程入口-v9.md。v8及更早模型、源码、成片和历史报告保留。
'''
if current:
    ranges=review.get('coverage',{}).get('visual_ranges',[])
    count=sum(r['end_frame']-r['start_frame']+1 for r in ranges)
    note+=f'\n本轮独立局部复核实际查看 {count} 帧；结论：{review.get("verdict","incomplete")}。\n'
if remaining_notes:
    note+='\n残留问题：\n\n'+'\n'.join('- '+n for n in remaining_notes)+'\n'
(ROOT/'delivery/交付说明-v9.md').write_text(note,encoding='utf8')
cp=json.loads((ROOT/'CHECKPOINT.json').read_text(encoding='utf8'))
cp.update(status='v9_delivery_ready_review_incomplete',final_candidate=e['video'],final_candidate_sha256=e['sha256'],updated_at=status['updated_at'],next_action='展示完整v9影片、一次修复内容与实际复核范围；后续按用户反馈针对性修改。')
cp['verification'].update(render='v9全部1344帧，1080×1920、24fps、56秒，完整音视频解码无错误；冻结源码哈希一致。',assets='model/babylon-city-v9.blend：保留v8城市、蓝釉建筑、街道、人畜、王神雕像；24处砖墩木梁桥与4艘载货驳船已修复。',independent_review='同一审片者本轮局部复核，以qa/v9/av-review.json的当前成片哈希与实际覆盖为准；整片审核和实际听音未完成。')
cp['delivery_note']='完整v9可播放，工程检查通过；本轮一次修复已用。独立审核仅实际局部范围，实际听音不可用，未声称全片视听通过。'
cp['unresolved']=['全片独立画面覆盖未完成；仅本轮修改及相邻镜头局部复核','实际听音能力不可用，高潮听感与完整音画节奏未验收']+remaining_notes
cp['v9_local_recheck']={'report':'qa/v9/av-review.json','verdict':status['review'],'coverage':status['coverage'],'remaining_findings':remaining}
cp['v9_revision']['review']='本轮唯一审片者完成必要局部复核；实际范围及残留缺陷见 qa/v9/av-review.json，未完成全片与听音审核。' if current else '局部复核报告未落盘，不能声称完成。'
(ROOT/'CHECKPOINT.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf8')
adopt=json.loads((ROOT/'source-adoption.json').read_text(encoding='utf8'))
adopt['adoption']['current_blender']='render_city_v9.py沿用v8绝对时间摄影、真实深度+屏幕清晰带Defocus和独立8Hz活动；仅更换v9桥船模型及输出地址。'
adopt['verification']['v9']='1344帧正式Cycles渲染与56秒音画编码完成；整片解码与冻结哈希通过。一次桥船修复后的局部复核见qa/v9/，整片和听音审核未完成。'
(ROOT/'source-adoption.json').write_text(json.dumps(adopt,ensure_ascii=False,indent=2),encoding='utf8')
plan=json.loads((ROOT/'plan.json').read_text(encoding='utf8'))
plan.update(version='v9',status='complete_video_review_incomplete',assets_status='model/babylon-city-v9.blend；保留v8城市细节，24处砖墩木梁桥及4艘货驳完成正式渲染。')
plan['audio'].update(master_clock='用户原曲29.5–85.5秒连续节选；摄影按候选能量起音编排，未实际听音。',meter=None,source_status='用户本地文件已混入v8并沿用至v9；编码AAC与v8逐字节相同。',stems=['user-provided-Dream-Of-Babylon.mp3','ambience.wav'],source_excerpt_seconds=[29.5,85.5],fade_in_seconds=.15,fade_out_seconds=[53,56],notes='旧90BPM原创配器和v7从头节选方案仅为历史；v9沿用v8，实际听音未完成。',cues=[{'start':0,'end':.15,'music':'原曲29.5秒处起，0.15秒渐入'},{'start':.15,'end':53,'music':'电影原曲连续播放，合入低音量合成环境声'},{'start':53,'end':56,'music':'3秒渐出'}])
plan['world']['route']=['城外地平线','蓝釉大道与国王雕像','市集驮畜','运河与码头','王宫台地花园','神像前庭','巨城全景']
plan['world']['street_continuity_evidence']='model/out/model-v9-evidence.json；实体桥头引坡连接原横街，正式画面局部复核见qa/v9/。'
plan['quality_contract']['status']='full_render_decoded_source_freeze_verified_review_incomplete'
plan['evidence'].update(validation_scope='完整v9已输出并全片解码通过；制作角色查看正式帧168、744、1296；独立局部覆盖以qa/v9/av-review.json为准，整片及听音未完成。',engineering_report='delivery/engineering-check-v9.json',frame_audit='qa/v9/recheck-index.json',heard_audio=False)
plan['v9_revision'].update(authoritative_timeline='v8-timeline.json',frozen_manifest='render/frozen-v9-manifest.json',encoded_video='delivery/暮河城-巴比伦巨城-Dream-of-Babylon-v9.mp4',review='qa/v9/av-review.json')
(ROOT/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
md=(ROOT/'视频制作计划.md').read_text(encoding='utf8')
md=md.replace('# 暮河城 · 街巷与运河（移轴强化版 v8）','# 暮河城 · 街巷与运河（移轴城市版 v9）',1)
md=md.replace('当前执行方案为文末“v8 用户反馈改造”七段摄影。1080×1920、56秒、24fps；原曲29.5–85.5秒节选；模型为 `model/babylon-city-v8.blend`，摄影入口为 `render_city_v8.py`。下文六段摄影与原创配乐保留为制作历史，不作为v8执行时间表。','当前交付为v9：沿用文末“v8 用户反馈改造”的七段摄影，并完成“v9 本轮一次针对性修复”。1080×1920、56秒、24fps；原曲29.5–85.5秒节选；模型为 `model/babylon-city-v9.blend`，摄影入口为 `render_city_v9.py`。下文早期六段摄影及原创配乐仅为制作历史。完整音画已输出，审核实际覆盖见 `qa/v9/`，不能视为整片视听审核通过。',1)
(ROOT/'视频制作计划.md').write_text(md,encoding='utf8')
print(json.dumps({'delivery_ready':True,'review_current_hash':current,'review_verdict':status['review'],'video':e['video'],'sha256':e['sha256']},ensure_ascii=False))
