"""Extract encoded-picture evidence after the existing v16 pipeline finishes.

This prepares evidence only; it never grants visual or listening approval.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
QA = ROOT / 'qa/v16/final-encoded'
FF = Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
report = json.loads((ROOT / 'delivery/engineering-check-v16.json').read_text(encoding='utf8'))
video = Path(report['video'])
assert hashlib.sha256(video.read_bytes()).hexdigest() == report['sha256']
assert report['decode_exit'] == 0 and report['frames'] == 2160
QA.mkdir(parents=True, exist_ok=True)
baseline_index = ROOT / 'render/shot-cache-v16.json'
if not baseline_index.exists():
    subprocess.run([sys.executable, str(ROOT / 'shot_cache.py'), 'register',
                    '--report', str(ROOT / 'delivery/engineering-check-v16.json'),
                    '--frames', str(ROOT / 'render/frames-v16'),
                    '--cuts', '8,19,25,31,44,55,64,74,81',
                    '--out', str(baseline_index)], check=True)
else:
    assert json.loads(baseline_index.read_text(encoding='utf8'))['video_sha256'] == report['sha256'], 'Cached baseline belongs to a different encode'
times = [0.5, 4, 7.95, 8.05, 13.5, 18.95, 19.05, 24.95, 25.05,
         27, 28, 30.95, 31.05, 36, 43.95, 44.05, 50.5, 54.95,
         55.05, 63.95, 64.05, 67.8, 70, 73.95, 74.05, 76,
         80.95, 81.05, 86, 88.5, 89.5]
entries = []
for number, second in enumerate(times):
    path = QA / f'{number:02d}-{second:05.2f}s.png'
    subprocess.run([str(FF), '-y', '-hide_banner', '-loglevel', 'error',
                    '-ss', str(second), '-i', str(video), '-frames:v', '1',
                    '-c:v', 'png', str(path)], check=True)
    entries.append({'time': second, 'path': str(path),
                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                    'actually_viewed': False})
sheets = []
for start in range(0, len(entries), 12):
    batch = entries[start:start + 12]
    sheet = Image.new('RGB', (1080, 3 * 510), '#191919')
    draw = ImageDraw.Draw(sheet)
    for i, entry in enumerate(batch):
        with Image.open(entry['path']) as original:
            thumb = original.convert('RGB').resize((270, 480), Image.Resampling.LANCZOS)
        x, y = i % 4 * 270, i // 4 * 510
        sheet.paste(thumb, (x, y))
        draw.text((x + 8, y + 484), f"{entry['time']:.2f}s", fill='white')
    target = QA / f'contact-{start // 12 + 1}.jpg'
    sheet.save(target, quality=94)
    sheets.append(str(target))
evidence = {'video': str(video), 'video_sha256': report['sha256'],
            'frames': entries, 'contact_sheets': sheets,
            'scope': 'Encoded representative frames and both sides of cuts; preparation only.',
            'actually_listened': False, 'independent_review': False}
(QA / 'index.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps({'prepared': len(entries), 'sheets': sheets}, ensure_ascii=False))
