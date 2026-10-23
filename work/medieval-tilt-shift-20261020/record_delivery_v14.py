"""Record completed delivery only from hash-bound engineering and observations."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
P=Path(__file__).resolve().parent;Q=P/'qa/v14';D=P/'delivery'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
eng=read(D/'engineering-check-v14.json');video=Path(eng['video']);digest=hashlib.sha256(video.read_bytes()).hexdigest()
obs=read(Q/'producer-observations-v14.json');evidence=read(Q/'producer-evidence-v14.json');temporal=read(Q/'encoded-temporal-scan.json')
assert digest==eng['sha256']==obs['video_sha256']==evidence['video_sha256']==temporal['video_sha256']
assert temporal['frames_decoded']==1824 and not temporal['abnormal_green_frames'] and not temporal['isolated_temporal_candidates']
assert obs['actual_viewed_frames'] and obs['observations'] and not obs['audio_perceived'] and not obs['independent_review']
now=datetime.now(timezone.utc).isoformat()
evidence['actual_viewed_frames']=obs['actual_viewed_frames'];evidence['original_resolution_frames']=obs['original_resolution_frames']
for win in evidence['motion_windows']:win['actual_viewed']=win['label'] in obs['actual_viewed_window_labels']
write(Q/'producer-evidence-v14.json',evidence)
cp=read(P/'CHECKPOINT-v14.json');cp.update(status='v14_delivered',updated_at=now,final_candidate=str(video),sha256=digest,next_action='v14已完整交付，等待用户反馈；不自动开启新一轮制作或独立审核。',unresolved=obs['limits'])
cp['completed']+=['All 1824 frames rendered from frozen v14 inputs','Full 76-second audio/video encode and decode passed','Final encoded technical scan and actual producer observations recorded']
cp['verification']+=['delivery/engineering-check-v14.json','qa/v14/encoded-temporal-scan.json','qa/v14/producer-observations-v14.json']
write(P/'CHECKPOINT-v14.json',cp)
main=read(P/'CHECKPOINT.json');main.update(status='v14_delivered',updated_at=now,final_candidate=str(video),final_candidate_sha256=digest,render_session_id=None,next_action=cp['next_action'],delivery_note='v14 76秒竖屏；六项优化已实施。制作角色实际查看范围与剩余限制见qa/v14/producer-observations-v14.json；未实际听音，未新增独立审核。')
main['completed'].append('用户授权的v14六项优化完成；完整1824帧重渲、音频合成、解码和技术扫描完成，实际查看证据已登记。')
main['v14_revision'].update(status='delivered',video=str(video),sha256=digest,evidence='qa/v14/producer-observations-v14.json')
write(P/'CHECKPOINT.json',main)
plan=read(P/'plan.json');plan.update(status='delivered',current_delivery={'video':str(video),'sha256':digest,'engineering':'delivery/engineering-check-v14.json','producer_evidence':'qa/v14/producer-observations-v14.json','independent_review':False,'audio_perceived':False});write(P/'plan.json',plan)
source=read(P/'source-adoption.json');source['verification']['v14']='全部1824帧由v14模型和动态清晰带重渲；扩展水面接触、祭祀交接、屋顶和材质细节及分场景环境音。工程检查与实际查看范围见qa/v14/；未实际听音，未新增独立审核。';write(P/'source-adoption.json',source)
write(D/'delivery-summary-v14.json',{'version':'v14','video':str(video),'sha256':digest,'engineering':eng,'observations':'qa/v14/producer-observations-v14.json','independent_review':False,'audio_perceived':False,'limits':obs['limits']})
shutil.copy2(Q/'encoded-frames/01373.png',D/'preview-v14.png')
(D/'交付说明-v14.txt').write_text('暮河城 · 巴比伦巨城 v14\n\n76秒，1080×1920，24fps，48kHz立体声。v13保持原样。\n\n修订：世界尺度水纹、动态尾流与岸边湿痕；完整供盘交接及落台动作；119名中景居民局部聚集并约束间距；跟随主体的清晰带及逐渐展开的结尾清晰范围；屋顶生活道具、花园细节、建筑色差与神庙木门铜饰；按场景重新制作风、水、脚步及供盘落台声。保留主干道繁荣人流、双列士兵、两岸纤夫及原配乐节选。\n\n完整解码与编码全帧技术检查通过。实际观察与限制见../qa/v14/producer-observations-v14.json。未实际听音，未新增独立审核；技术检查不代表细微闪烁已完全排除。\n',encoding='utf8')
(D/'工程入口-v14.txt').write_text('可编辑模型：../model/babylon-city-v14.blend\n模型修订：../model/revise_city_v14.py\n动作：../v14_motion.py\n渲染：../render_city_v14.py\n完整流水线：../render_pipeline_v14.py full\n镜头：../v14-timeline.json\n交通：../traffic-v14.npz\n音频：../mix_music_v14.py\n冻结输入：../render/frozen-v14-manifest.json\n帧序列：../render/frames-v14/\n\nBlender 4.5.3 / Cycles OptiX / 32采样 / 深度与动态清晰带合成。\n',encoding='utf8')
print(json.dumps({'video':str(video),'sha256':digest,'bytes':video.stat().st_size},ensure_ascii=False))
