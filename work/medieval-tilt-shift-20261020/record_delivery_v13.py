"""Publish delivery records only after actual encoded-image observations exist."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
QA = ROOT / 'qa/v13'
OUT = ROOT / 'delivery'

def read(path):
    return json.loads(path.read_text(encoding='utf8'))

def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf8')

engineering = read(OUT / 'engineering-check-v13.json')
video = Path(engineering['video'])
digest = hashlib.sha256(video.read_bytes()).hexdigest()
evidence = read(QA / 'producer-evidence-v13.json')
observations = read(QA / 'producer-observations-v13.json')
technical = read(QA / 'encoded-temporal-scan.json')
assert digest == engineering['sha256'] == evidence['video_sha256'] == observations['video_sha256'] == technical['video_sha256']
assert technical['frames_decoded'] == 1824
assert not technical['abnormal_green_frames'] and not technical['isolated_temporal_candidates']
assert observations['observations'] and observations['actual_viewed_frames']
assert observations['independent_review'] is False and observations['audio_perceived'] is False
now = datetime.now(timezone.utc).isoformat()
evidence['actual_viewed_frames'] = observations['actual_viewed_frames']
evidence['original_resolution_frames'] = observations['original_resolution_frames']
viewed_windows = set(observations['actual_viewed_window_labels'])
for window in evidence['motion_windows']:
    window['actual_viewed'] = window['label'] in viewed_windows
    if window['actual_viewed']:
        window['method'] = window['method'].replace('visual inspection pending.', 'actually visually inspected by producer.')
write(QA / 'producer-evidence-v13.json', evidence)
checkpoint = read(ROOT / 'CHECKPOINT.json')
checkpoint.update(status='v13_delivered', updated_at=now, final_candidate=str(video), final_candidate_sha256=digest, render_session_id=None)
checkpoint['completed'].append('v13完成全部1824帧重渲、76秒音乐合成和完整解码；制作角色实际查看范围见绑定成片哈希的v13观察记录。')
checkpoint['verification'].update(
    render='v13全部1824帧，1080×1920、24fps、76秒；冻结输入及完整音视频解码通过。',
    assets='两岸纤道、拉纤队伍、船只与缆绳，以及双列巡逻和周边行人，按v13实际观察记录核对。',
    producer_evidence='qa/v13/producer-evidence-v13.json 与 producer-observations-v13.json；绑定当前v13成片哈希。',
    review_evidence_consistency='历史独立审核仅对应历史成片；v13仅为制作角色检查，覆盖与限制见v13观察记录。',
    temporal='v13源PNG扫描定位第934帧孤立跳变并重渲；最终编码1824帧扫描未检出强绿坏帧或阈值内孤立跳帧；不排除细微闪烁。')
checkpoint['next_action'] = 'v13已交付，等待用户反馈；不自动重开渲染或独立审核。'
checkpoint['delivery_note'] = '76秒竖屏v13；两岸拉纤、士兵协调及居民避让已修改。实际检查范围见v13制作观察；未实际听音，未新增独立审核。'
checkpoint['v13_revision']['next_action'] = checkpoint['next_action']
checkpoint['v13_revision']['final_candidate_sha256'] = digest
revision = checkpoint['v13_revision_progress']
revision.update(pending=[], active_pipeline_pid=None, pipeline_session_id=None, monitor_cell_id=None,
                completed_at=now, engineering_check='delivery/engineering-check-v13.json',
                producer_observations='qa/v13/producer-observations-v13.json',
                verification_limits=observations['limits'],
                last_progress_snapshot={'saved_frames':1824,'total_frames':1824,'as_of':now,'stage':'delivered'})
revision['completed'].append('All nine shots rendered from the same frozen v13 world; zero v12 frame reuse. Source-frame 934 isolated and rerendered; encoded checks and recorded producer visual inspection completed.')
write(ROOT / 'CHECKPOINT.json', checkpoint)
plan = read(ROOT / 'plan.json')
plan.update(status='delivered', current_delivery={'video':str(video),'sha256':digest,'engineering':'delivery/engineering-check-v13.json','producer_evidence':'qa/v13/producer-observations-v13.json','independent_review':False,'audio_perceived':False})
write(ROOT / 'plan.json', plan)
source = read(ROOT / 'source-adoption.json')
source['verification']['v13'] = '全部1824帧重渲；源图扫描发现第934帧孤立跳变并重渲；76秒音乐合成、完整解码和最终编码全帧技术扫描通过。实际制作检查范围见qa/v13/producer-observations-v13.json；未新增独立审核，未实际听音。'
write(ROOT / 'source-adoption.json', source)
write(OUT / 'delivery-summary-v13.json', {'version':'v13','video':str(video),'sha256':digest,'engineering':engineering,'observations':'qa/v13/producer-observations-v13.json','independent_review':False,'audio_perceived':False,'limits':observations['limits']})
shutil.copy2(QA / 'encoded-frames/00756.png', OUT / 'preview-v13.png')
(OUT / '交付说明-v13.txt').write_text(
    '暮河城 · 巴比伦巨城 v13\n\n76秒，1080×1920，24fps，48kHz立体声。\n\n'
    '修订：两岸各设置实体纤道及四人拉纤队伍；调整东岸视线与货驳位置。士兵采用双列队形、12姿态步态，统一行进速度与脚步，稳定盾矛握持；附近180名居民路径加入巡逻避让。保留蓝釉巨城、繁荣人流、移轴及原音乐节选。\n\n'
    '全9镜头重渲；源图扫描定位并重渲第934帧；完整解码与最终编码全帧技术扫描通过。实际查看范围和限制见制作观察记录。未新增独立审核；未实际听音，细微闪烁及主观音画节奏未获完整验证。\n\n'
    '成片：'+video.name+'\n证据：../qa/v13/producer-observations-v13.json\n', encoding='utf8')
(OUT / '工程入口-v13.txt').write_text(
    '可编辑模型：../model/babylon-city-v13.blend\n模型修订：../model/revise_city_v13.py\n渲染：../render_city_v13.py\n'
    '完整流水线：../render_pipeline_v13.py full\n镜头：../v13-timeline.json\n交通：../traffic-v13.npz\n路径修订：../refine_v13_paths.py\n'
    '冻结输入：../render/frozen-v13-manifest.json\n帧序列：../render/frames-v13/\n音频：../audio/final-mix-v11.wav\n'
    '\nBlender 4.5.3，Cycles OptiX，32采样，GPU多级高斯移轴合成。原样例机制迁移见../source-adoption.json。\n', encoding='utf8')
(ROOT / 'RESUME-v13.md').write_text(
    'v13已完整交付，无活动渲染。\n\n成片：delivery/'+video.name+'\nSHA256：'+digest+
    '\n工程检查：delivery/engineering-check-v13.json\n实际制作观察：qa/v13/producer-observations-v13.json\n\n'
    '全部1824帧，76秒1080×1920、24fps、立体声。仅在记录范围内实际查看；未实际听音，未新增独立审核。等待用户反馈，不自动重启。\n', encoding='utf8')
print(json.dumps({'video':str(video),'sha256':digest,'bytes':video.stat().st_size,'viewed_frames':len(observations['actual_viewed_frames']),'viewed_windows':len(viewed_windows)},ensure_ascii=False))
