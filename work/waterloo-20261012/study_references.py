import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
MEDIA = ROOT.parents[1] / 'reference-sources/upstream-videos/lemo-opuscar'
BIN = Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc')
CASES = {
    'shadow-puppet': [1, 5, 12, 20, 25, 26, 27, 37, 43, 49, 52],
    'paper-lantern': [1, 7, 17, 32, 45, 55, 56, 57, 75, 94, 116],
    'stained-glass': [1, 6, 13, 20, 25, 26, 27, 32, 38, 46, 51],
}
evidence = []
for name, times in CASES.items():
    out = ROOT / 'reference-evidence' / name
    out.mkdir(parents=True, exist_ok=True)
    src = MEDIA / (name + '.mp4')
    probe = subprocess.run([str(BIN/'ffprobe.exe'), '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(src)], capture_output=True, text=True, check=True, timeout=30)
    (out/'metadata.json').write_text(probe.stdout, encoding='utf-8')
    sheet = Image.new('RGB', (960, 4*208), '#171717')
    draw = ImageDraw.Draw(sheet)
    for i,t in enumerate(times):
        frame = out / f'{t:06.2f}.jpg'
        subprocess.run([str(BIN/'ffmpeg.exe'), '-hide_banner', '-loglevel', 'error', '-ss', str(t), '-i', str(src), '-frames:v', '1', '-vf', 'scale=640:-1', '-threads', '1', '-y', str(frame)], check=True, timeout=45)
        im = Image.open(frame).convert('RGB'); im.thumbnail((320,180))
        x,y = (i%3)*320,(i//3)*208
        sheet.paste(im,(x,y)); draw.text((x+8,y+182), f'{name} / {t:.2f}s', fill='white')
    sheet.save(out/'sheet.jpg', quality=92)
    evidence.append({'name':name,'source':str(src),'sampled_times':times,'frame_width':640,'method':'sampled frames, no realtime playback or audio review'})
    print(name + ': sampled', flush=True)
(ROOT/'reference-evidence/study-index.json').write_text(json.dumps(evidence, ensure_ascii=False,indent=2),encoding='utf-8')
