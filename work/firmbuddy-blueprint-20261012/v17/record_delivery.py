from pathlib import Path
import json
R=Path(__file__).resolve().parent;O=R.parent/'out/final-v17-blueprint-sources'
d=json.loads((O/'delivery-checks.json').read_text(encoding='utf-8'))
d['visual_observation']='Actual inspection: final decoded 24-frame overview and full-resolution frames at 25s and 74s. Earlier source-frame continuity sheets and critical handoff sample are recorded below. No full normal-speed viewing or full actual listening.'
d['actual_final_full_resolution_times']=[25,74]
d['actual_final_overview_viewed']=True
(O/'delivery-checks.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
obs=dict(video_sha256=d['video_sha256'],mode='User-requested revision, historical one-round review budget already used',subagents=0,
 actual_views=[dict(path='out/stills-v17-design-a',times=[5,24,30,37.5,74],status='initial design, subsequently refined'),
 dict(path='out/sample-v17-opening/continuity-1.jpg + continuity-2.jpg',times=[26.4,27.2,28,28.8,30,32,33.2,34.4,35.2,35.6,36,36.4,36.8,37.2,37.6,38,38.4,39.2,40,41.2],status='opening sample; handoff later refined'),
 dict(path='out/sample-v17-experts/continuity-1.jpg',times=[66.4,67.2,68,68.8,69.6,70.4,71.6,72.8,74,75.6,77.2,79.2],full_resolution=[77.2]),
 dict(path='out/sample-v17-handoff/continuity-1.jpg',times=[35.2,35.6,36,36.4,36.8,37.2,37.6,37.8,38,38.2,38.4,39.2],same_render_signature_as_final=True),
 dict(path='out/final-v17-blueprint-sources/continuity-1.jpg',times=[.4,2,6,7.6,8.4,10,12,15.6,16.8,17.6,18.4,20.4],note='source frames from final render'),
 dict(path='out/final-v17-blueprint-sources/final-overview.jpg',times=d['extracted_final_times'],note='MP4 decoded overview'),
 dict(path='out/final-v17-blueprint-sources/decoded-*.jpg',times=[25,74],note='MP4 decoded full-resolution')],
 full_normal_speed_viewing=False,actual_complete_listening=False,
 fixes=['Removed cream/gold card faces; same world-space blueprint paper and ink throughout.','Explained actual public announcement/unlock-calendar sources and scan scopes.','Named each card source; retained company-level nature of unlock lead.','Rebuilt original-reference seating, expert figures, nameplates and formal taxonomy.','Moved industry rails behind the hall file and raised brand backdrop.','Matched carrier time velocity across 38s handoff.'],
 checks=dict(layout_samples=115,layout_issues=0,decode=True,dimensions=[1920,1080],duration=124,frames=3720,aac_sync_windows=9,aac_lag_samples=0))
(O/'observations.json').write_text(json.dumps(obs,ensure_ascii=False,indent=2),encoding='utf-8')
with (R/'CHECKPOINT.md').open('a',encoding='utf-8') as f:f.write('''
- 整片完成：out/final-v17-blueprint-sources/video.mp4，124秒、1920×1080、30fps、3720帧、H264/AAC双声道。SHA256 01d01e76f7f8c94dba578d41dd916552c49420534914f13e8b7877eb0f4d7576。
- 最终验证：全量音视频解码通过，9处AAC对齐均0采样偏移，V16原文件哈希均未变化。已实际看最终解码24帧总览及25/74秒原尺寸帧，另看正式输出前20秒连续抽样表。非独立审核，未全片正常速度观看或完整听音。
- 记录：delivery-checks.json、observations.json；下一步源码打包并打开成片，无制作修改遗留。
''')
print(d['video_sha256'])
