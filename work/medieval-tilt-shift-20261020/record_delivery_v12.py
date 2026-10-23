"""Bind actual producer observations and delivery records to the finished MP4."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

root = Path(__file__).resolve().parent
qa = root / 'qa/v12'
out = root / 'delivery'
def read(p):
    return json.loads(p.read_text(encoding='utf8'))
def write(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf8')
engineering = read(out / 'engineering-check-v12.json')
video = Path(engineering['video'])
digest = hashlib.sha256(video.read_bytes()).hexdigest()
assert digest == engineering['sha256']
evidence = read(qa / 'producer-evidence-v12.json')
assert evidence['video_sha256'] == digest
technical = read(qa / 'encoded-temporal-scan.json')
assert technical['frames_decoded'] == 1824
assert not technical['abnormal_green_frames'] and not technical['isolated_temporal_candidates']
now = datetime.now(timezone.utc).isoformat()
observations = {
    'created_at': now, 'producer': '/root', 'independent_review': False,
    'video': str(video), 'video_sha256': digest,
    'method': 'Actual visual inspection of all seven representative contact sheets and all six consecutive-frame contact sheets; five original-resolution decoded stills. No realtime playback or actual audio listening.',
    'representative_frames': [e['frame'] for e in evidence['frames']],
    'original_resolution_frames': [288, 528, 756, 1176, 1752],
    'consecutive_ranges': [{k:w[k] for k in ['label','start_frame','end_frame','path','sha256']} for w in evidence['motion_windows']],
    'observations': [
        {'frames': [0,12,48,96,168,191], 'observation': 'Intentional opening fade begins at black. Camera rise reveals the gate, temple, connected avenue and canal over the sandy foreground. Later opening views show focused middle distance and increasingly soft foreground/background.'},
        {'range': [12,35], 'observation': 'City progressively emerges with consistent sky and sand colour. The former bad frame 24 has no visible green or bright flash in this inspected continuous sequence.'},
        {'frames': [192,288,383], 'range': [276,299], 'observation': 'White-clad gift bearers, a priest and blue-clad armed guards are distinguishable near the king statue and blue gate. Facing groups suggest reception. Movement in this one-second window is restrained; this is a stylized miniature encounter rather than detailed dramatic acting.'},
        {'frames': [384,396,528,588,611,647], 'range': [516,539], 'observation': 'Armed patrol remains in a purposeful formation amid scattered residents, animals and market activity. Shields, spears, helmets and red backs distinguish soldiers. Camera and crowd state changes remain consistent in the inspected sequence.'},
        {'frames': [648,732,755,756,875], 'range': [732,755], 'observation': 'Blue and green cargo hulls, red canopy, pale tied loads, crew, colourful square-sail craft, quay towmen and connected ropes are visible. Tow groups remain on the raised quay and ropes retain endpoints in the sampled continuous sequence. Near/far boats soften outside the focus band.'},
        {'frames': [876,1067], 'observation': 'Terraced garden retains steps, palms, planting beds and blue trim; the sampled adjoining cuts contain complete images.'},
        {'frames': [1068,1114,1115,1116,1176,1283], 'range': [1103,1126], 'observation': 'Distinct statues face the forecourt, with white-robed priests/acolytes and offering vessels below. No former frame-1115 colour flash is visible in the inspected continuous sequence.'},
        {'frames': [1284,1392,1492,1493,1560,1622], 'observation': 'Courtyard temple and grain exchange retain solid surrounding buildings, courtyard visitors and blue trim. Adjacent sampled cut frames are complete; blur remains localized by depth and the tilted focus band.'},
        {'frames': [1623,1752,1800,1823], 'range': [1740,1763], 'observation': 'Avenue population extends through the focused city into the distance, with people on cross streets and bridge decks. The continuous panorama shows stable architecture and focus while the camera pulls back. Far people become small and blurred; individual action cannot be assessed there. Final black frame belongs to the intentional ending fade.'}
    ],
    'technical': technical,
    'actual_listened_ranges_seconds': [], 'audio_perceived': False,
    'limits': [
        'Producer representative and stated continuous-window checks only; not all 1824 frames visually reviewed.',
        'No new independent review round. Historical review is bound to its own historical video.',
        'Actual audio listening unavailable; subjective music synchronization remains unverified.',
        'Technical scan addresses strong colour faults and isolated jumps; subtle temporal shimmer is not ruled out.',
        'Fantasy interpretation of Babylon; not an archaeological reconstruction.'
    ]
}
write(qa / 'producer-observations-v12.json', observations)
evidence['actual_viewed_frames'] = observations['representative_frames']
evidence['original_resolution_frames'] = observations['original_resolution_frames']
for w in evidence['motion_windows']:
    w['actual_viewed'] = True
    w['method'] = w['method'].replace('visual inspection pending.', 'actually visually inspected by producer.')
write(qa / 'producer-evidence-v12.json', evidence)
checkpoint = read(root / 'CHECKPOINT.json')
checkpoint.update(status='v12_delivered', updated_at=now, final_candidate=str(video), final_candidate_sha256=digest, render_session_id=None)
checkpoint['completed'].append('v12全部1824帧完成；76秒音乐合成、完整解码、源图及编码逐帧技术扫描通过；制作角色查看38张代表帧、6段连续窗及5张原尺寸成片帧。')
checkpoint['verification'].update(render='v12全部1824帧、1080×1920、24fps、76秒；冻结输入核对及完整音视频解码通过。', assets='祭司、军队、埃及使团、全长大道人流、彩绘船、船员及纤夫已在最终成片代表画面核对。', producer_evidence='qa/v12/producer-evidence-v12.json 与 producer-observations-v12.json；绑定当前成片哈希。', temporal='源PNG与编码后1824帧机械扫描均未检出强绿坏帧或阈值内孤立跳帧；不排除细微闪烁。')
checkpoint['next_action'] = 'Current v12 delivered; await user feedback. No new render or independent review scheduled.'
checkpoint['delivery_note'] = '76秒竖屏v12；四项修订已落实。工程与逐帧技术扫描通过，制作角色完成38张代表帧、6段连续窗及5张原尺寸帧检查；未新增独立审核，实际听音未完成。'
r = checkpoint['v12_revision']
r.update(full_render_session=None, active_pipeline_pid=None, next_action=checkpoint['next_action'], final_candidate_sha256=digest, engineering_check='delivery/engineering-check-v12.json', producer_observations='qa/v12/producer-observations-v12.json', encoded_temporal_scan='qa/v12/encoded-temporal-scan.json', completed_at=now)
r['completed'].extend(['1824/1824 formal-size frames rendered and assembled with unchanged music excerpt.', 'Whole source and encoded-frame technical scans found no strong-green or isolated temporal candidates.', 'Producer inspected 38 representative encoded frames, six 24-frame windows and five full-resolution encoded stills.'])
r['verification_limits'] = observations['limits']
r['last_progress_snapshot'] = {'saved_frames':1824,'total_frames':1824,'as_of':now,'stage':'delivered'}
write(root / 'CHECKPOINT.json', checkpoint)
plan = read(root / 'plan.json')
plan['status'] = 'delivered'
plan['current_delivery'] = {'video':str(video),'sha256':digest,'engineering':'delivery/engineering-check-v12.json','producer_evidence':'qa/v12/producer-observations-v12.json','independent_review':False,'audio_perceived':False}
write(root / 'plan.json', plan)
source = read(root / 'source-adoption.json')
source['verification']['v12'] = '1824帧正式Cycles渲染及76秒音乐合成完成；冻结输入、全片解码、源图与编码全帧技术扫描通过。实际制作观察及限制见qa/v12/producer-observations-v12.json，未新增独立全片视听审核。'
write(root / 'source-adoption.json', source)
summary = {'version':'v12','video':str(video),'sha256':digest,'engineering':engineering,'observations':'qa/v12/producer-observations-v12.json','independent_review':False,'audio_perceived':False,'limits':observations['limits']}
write(out / 'delivery-summary-v12.json', summary)
shutil.copy2(qa / 'encoded-frames/00756.png', out / 'preview-v12.png')
(out / '交付说明-v12.txt').write_text('暮河城 · 巴比伦巨城 v12\n\n76秒，1080×1920，24fps，48kHz立体声。\n\n修订：替换不稳定景深合成，修复已定位闪帧；加入祭司、巴比伦巡逻军队、埃及使团；扩充全长大道、横街与桥面人流；细化彩绘船体、帆、货载、船员、岸上纤夫及连接缆绳。\n\n验证：冻结源码、完整音视频解码及源图/编码全帧技术扫描通过。制作角色实际查看38张代表帧、6段各24帧连续窗和5张原尺寸成片帧。未新增独立审核；未实际听音，细微闪烁与主观音画节奏不作通过保证。\n\n当前MP4：'+video.name+'\n证据：../qa/v12/producer-observations-v12.json\n模型：../model/babylon-city-v12.blend\n渲染：../render_city_v12.py\n', encoding='utf8')
(out / '工程入口-v12.txt').write_text('可编辑模型：../model/babylon-city-v12.blend\n模型生成：../model/revise_city_v12.py\n渲染入口：../render_city_v12.py\n完整流水线：../render_pipeline_v12.py full\n镜头：../v12-timeline.json\n交通：../traffic-v12.npz\n冻结输入：../render/frozen-v12-manifest.json\n帧序列：../render/frames-v12/\n音频：../audio/final-mix-v11.wav\n\nBlender 4.5.3，Cycles，OptiX，32采样，GPU多级高斯移轴景深。\n原样例机制迁移说明：../source-adoption.json\n当前编码帧扫描使用本地imageio FFmpeg完整版本；Remotion精简版不支持rawvideo muxer。\n', encoding='utf8')
(root / 'RESUME-v12.md').write_text('v12已完整交付，当前没有活动渲染。\n\n成片：delivery/'+video.name+'\nSHA256：'+digest+'\n技术报告：delivery/engineering-check-v12.json\n制作实际观察：qa/v12/producer-observations-v12.json\n\n1824帧已齐备，76秒1080×1920、24fps、立体声；源图和编码全帧技术扫描未检出强绿异常或孤立跳帧。实际查看38张代表帧、6段连续窗与5张原尺寸帧。未新增独立审核，实际听音未完成。\n\n等待用户反馈；不要自动重开渲染或审核。可编辑模型model/babylon-city-v12.blend，渲染源码render_city_v12.py。\n', encoding='utf8')
print(json.dumps({'video':str(video),'sha256':digest,'actual_representative_frames':len(observations['representative_frames']),'continuous_windows':len(observations['consecutive_ranges']),'bytes':video.stat().st_size},ensure_ascii=False))
