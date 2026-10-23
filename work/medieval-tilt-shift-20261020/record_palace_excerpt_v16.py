from pathlib import Path
import json,datetime
P=Path(__file__).resolve().parent
cp=P/'CHECKPOINT-v16.json';c=json.loads(cp.read_text(encoding='utf8'))
c['completed']+=['Rendered frozen final-world frames 648–695; encoded playable two-second excerpt with original music','Excerpt ffprobe verified 1080x1920, 24fps, 48 video frames and stereo audio; full decode exited 0','Producer actually viewed all 48 source frames on three ordered contact sheets; no obvious isolated flash or palace clipping seen at thumbnail scale','Fixed preview-only decode invocation for stripped FFmpeg by explicitly selecting rawvideo/pcm_s16le; final-film assembler already uses these codecs','Restarted missing-frame pipeline after excerpt check; existing 48 frames preserved']
c['unresolved']=['Full 2160-frame film render/encode pending','Final encoded picture inspection pending','Actual listening unavailable']
c.update(status='full_render_running_excerpt_ready',excerpt=str(P/'delivery/临河宫殿-v16-实际运镜样段.mp4'),next_action='Continue existing finish_palace_v16.py background process. Read pipeline-status-v16.json and frames-v16/render-progress.json before restarting. On completion inspect engineering-check-v16.json and current final file; do not claim full visual/audio approval from the excerpt.',updated_at=datetime.datetime.now().astimezone().isoformat())
cp.write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf8')
p=P/'qa/v16/producer-observations.json';d=json.loads(p.read_text(encoding='utf8'))
d.update(excerpt_visual_coverage={'frames':[648,695],'mode':'All 48 frames viewed in three ordered 4x4 contact sheets, 225x400 each; full frame 672 viewed separately. Not normal-speed playback or full-film approval.','contact_sheets':[str(P/f'qa/v16/excerpt/continuous-{i}.jpg') for i in range(1,4)],'findings':'Palace remains entirely in shot; camera move progresses smoothly at this scale; no obvious isolated color/geometry flash observed.','limitations':['Fine shimmer not ruled out at contact-sheet scale','Encoded real-time playback not observed','Audio listening unavailable']})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8');print('EXCERPT_RECORDED')
