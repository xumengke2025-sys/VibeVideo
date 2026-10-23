"""Extract bounded producer evidence from the completed, encoded v10 film."""
from pathlib import Path
import hashlib
import json
import math
import subprocess
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
QA = ROOT / 'qa/v10'
FF = Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
engineering = json.loads((ROOT / 'delivery/engineering-check-v10.json').read_text(encoding='utf8'))
video = Path(engineering['video'])
assert hashlib.sha256(video.read_bytes()).hexdigest() == engineering['sha256']
assert engineering['decode_exit'] == 0
frames = [12, 48, 96, 168, 288, 504, 638, 639, 728, 744, 760, 840, 852, 863, 864, 960, 1152, 1296]
(QA / 'encoded-frames').mkdir(parents=True, exist_ok=True)
manifest = []
for frame in frames:
    path = QA / 'encoded-frames' / f'{frame:06d}.png'
    subprocess.run([str(FF), '-y', '-hide_banner', '-loglevel', 'error', '-ss', f'{frame/24:.9f}',
                    '-i', str(video), '-map', '0:v:0', '-frames:v', '1', str(path)], check=True)
    manifest.append({'frame': frame, 'seconds': frame / 24, 'path': str(path),
                     'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})

def sheet(selected, name, columns=3, thumb_width=270):
    thumb_height = round(thumb_width * 16 / 9)
    cell_h = thumb_height + 28
    out = Image.new('RGB', (columns * thumb_width, math.ceil(len(selected) / columns) * cell_h), '#202020')
    draw = ImageDraw.Draw(out)
    for index, item in enumerate(selected):
        with Image.open(item['path']) as image:
            image.thumbnail((thumb_width, thumb_height))
            x, y = (index % columns) * thumb_width, (index // columns) * cell_h
            out.paste(image, (x, y + 28))
            draw.text((x + 6, y + 6), f"f{item['frame']:04d} | {item['seconds']:.3f}s", fill='white')
    path = QA / name
    out.save(path, quality=93)
    return str(path)

by_frame = {item['frame']: item for item in manifest}
sheets = [sheet([by_frame[f] for f in [12, 48, 96, 168, 288, 504]], 'opening-gate-market.jpg'),
          sheet([by_frame[f] for f in [728, 744, 760, 840, 852, 863]], 'boat-correction.jpg'),
          sheet([by_frame[f] for f in [638, 639, 864, 960, 1152, 1296]], 'connections-garden-statue-city.jpg')]
timeline = json.loads((ROOT / 'v8-timeline.json').read_text(encoding='utf8'))['shots']
cameras = []
for index, shot in enumerate(timeline):
    a, b, p0, p1, q0, q1, l0, l1 = shot
    poses = []
    for t, p, q, lens in [(a, p0, q0, l0), (b, p1, q1, l1)]:
        horizontal = math.hypot(q[0] - p[0], q[1] - p[1])
        poses.append({'seconds': t, 'position': p, 'target': q, 'lens_mm': lens,
                      'downward_pitch_degrees': math.degrees(math.atan2(p[2] - q[2], horizontal))})
    cameras.append({'shot': index, 'range_seconds': [a, b], 'poses': poses})

report = {'video': str(video), 'video_sha256': engineering['sha256'],
          'purpose': 'Producer verification only; this does not start or complete another independent review.',
          'extracted_frames': manifest, 'contact_sheets': sheets, 'camera_source': 'v8-timeline.json',
          'camera_geometry': cameras, 'actual_viewed_frames': [],
          'actual_listened_ranges_seconds': [], 'audio_perceived': False,
          'note': 'Extraction and numerical camera evidence do not constitute visual inspection or listening.'}
(QA / 'producer-evidence-v10.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps({'sha256': engineering['sha256'], 'frames': len(frames), 'sheets': sheets}, ensure_ascii=False))
