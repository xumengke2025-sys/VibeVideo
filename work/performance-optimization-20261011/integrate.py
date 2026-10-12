"""Integrate existing media only; do not resume paused production or encode videos."""
import json
from pathlib import Path
import subprocess
import sys
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
DEST = Path(__file__).resolve().parent
SKILL = ROOT / 'skill/vibe-video'
sys.path.insert(0, str(SKILL / 'scripts'))
from review_batches import prepare, merge, digest

FP = ROOT / 'node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
cases = [
    ('matcha', 'work/matcha-morph-20261011', 'out-preview-r3/matcha-steam-dry.mp4', 'qa/r3/frames/frame-audit.json', 1,
     ['timeline.json', 'SOURCES.md']),
    ('wastewater', 'work/wastewater-isometric-20261011', 'out/preview-v1/video.mp4', 'qa/preview-v1/index.json', 0,
     ['shot-plan.json', 'js/timeline.js']),
]
integrated = []
for name, folder, movie, index, repair_round, brief in cases:
    root = ROOT / folder
    video = root / movie
    media = json.loads(subprocess.run([str(FP), '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', str(video)],
                                     capture_output=True, text=True, check=True, timeout=120).stdout)
    stream = next(s for s in media['streams'] if s['codec_type'] == 'video')
    audio = [s for s in media['streams'] if s['codec_type'] == 'audio']
    origin = float(media.get('format', {}).get('start_time') or 0)
    duration = max(max(0., float(s.get('start_time') or 0) - origin) + float(s['duration'])
                   if s.get('duration') is not None else float(media['format']['duration']) for s in audio or [stream])
    frames = int(stream['nb_read_frames'])
    out = root / 'qa/performance-resume'
    if not (out / 'packet.json').exists():
        packet = prepare(video, root / index, out, frames, duration, bool(audio), 150, repair_round,
                         [root / p for p in brief])
    else:
        packet = json.loads((out / 'packet.json').read_text(encoding='utf-8'))
        assert packet['video_sha256'] == digest(video)
    state = merge(out / 'packet.json', [], out / 'aggregate', paused=True)
    integrated.append({'name': name, 'video': str(video), 'sha256': digest(video), 'frames': frames, 'duration': duration,
                       'size': [stream['width'], stream['height']], 'batches': len(packet['batches']), 'repair_round': repair_round,
                       'packet': str(out / 'packet.json'), 'status': state})

panels = [
    ('wastewater', ROOT / 'work/wastewater-isometric-20261011/out', 'stills-perf-540', 'stills-perf-1080', ['0', '34', '53', '73'], ''),
    ('napoleon', ROOT / 'work/napoleon-egypt-ink-20261009/revision-v3/out', 'perf-540', 'perf-1080', ['14', '17.8', '40.5', '59'], 'still-'),
]
measurements = []
for name, parent, low, high, times, prefix in panels:
    board = Image.new('RGB', (4 * 432, 830), '#202020')
    draw = ImageDraw.Draw(board)
    for i, time in enumerate(times):
        for j, version in enumerate((low, high)):
            with Image.open(parent / version / (prefix + time + '.png')) as picture:
                assert picture.size == ((540, 960) if j == 0 else (1080, 1920))
                board.paste(picture.convert('RGB').resize((216, 384)), (i*432+j*216, 40))
            draw.text((i*432+j*216+4, 15), f'{time}s  {540 if j == 0 else 1080}', fill='white')
    board = board.crop((0, 0, board.width, 430))
    board.save(DEST / (name + '-resolution-comparison.jpg'), quality=95)
    timing = [json.loads((parent / v / 'phase-timings.json').read_text(encoding='utf-8')) for v in (low, high)]
    measurements.append({'name': name, 'low': timing[0], 'high': timing[1], 'scope': 'one still-capture run; not end-to-end film benchmark'})

(DEST / 'integration.json').write_text(json.dumps(integrated, ensure_ascii=False, indent=2), encoding='utf-8')
(DEST / 'render-measurements.json').write_text(json.dumps(measurements, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps([{'project': p['name'], 'frames': p['frames'], 'batches': p['batches'], 'paused': p['status']['paused']} for p in integrated], ensure_ascii=False))
