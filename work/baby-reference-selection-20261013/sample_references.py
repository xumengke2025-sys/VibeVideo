import io, json, subprocess, hashlib, sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
FF = ROOT.parent / 'node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
FP = FF.with_name('ffprobe.exe')
sources = {
 'clawd-goes-to-sea': ROOT / 'reference-sources/github-expansion-20261011/az9713--opus-5.5-builds/builds/02-clawd-goes-to-sea/out/clawd-goes-to-sea.mp4',
 'crayon-book': ROOT / 'reference-sources/upstream-videos/lemo-opuscar/crayon-book.mp4',
 'midcentury-toon': ROOT / 'reference-sources/upstream-videos/lemo-opuscar/midcentury-toon.mp4',
 'watercolor': ROOT / 'reference-sources/upstream-videos/lemo-opuscar/watercolor.mp4',
 'clawd-prose': ROOT / 'reference-sources/github-expansion-20261013/az9713--opus-5.5-musical-cartoon/clawd-prose/out/clawd-prose.mp4',
}
records = json.loads((OUT/'evidence.json').read_text(encoding='utf-8')) if (OUT/'evidence.json').exists() else []
for name, src in sources.items():
 if len(sys.argv) > 1 and name != sys.argv[1]:
  continue
 meta = json.loads(subprocess.check_output([str(FP), '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(src)]))
 dur = float(meta['format']['duration'])
 v = next(x for x in meta['streams'] if x['codec_type'] == 'video')
 times = [round(.5 + (dur-1)*i/11, 3) for i in range(12)]
 sheet = Image.new('RGB', (1440, 880), '#eee9df')
 draw = ImageDraw.Draw(sheet)
 for i, t in enumerate(times):
  data = subprocess.check_output([str(FF), '-v', 'error', '-ss', str(t), '-i', str(src), '-frames:v', '1', '-vf', 'scale=480:-1', '-f', 'image2pipe', '-vcodec', 'png', '-'], timeout=30)
  im = Image.open(io.BytesIO(data)).convert('RGB')
  x, y = (i % 3)*480, (i//3)*220
  im.thumbnail((480, 195))
  sheet.paste(im, (x+(480-im.width)//2, y+22))
  draw.text((x+8,y+5), f'{name}  {t:.3f}s', fill='#222222')
 sheet.save(OUT / f'{name}-overview.jpg', quality=90)
 records = [r for r in records if r['name'] != name]
 records.append({'name':name,'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'duration':dur,'source_size':[v['width'],v['height']],'sample_times':times,'decoded_sample_width':480,'sheet':str(OUT/f'{name}-overview.jpg'),'evidence':'12 sampled stills across source; no realtime playback or audio listening'})
 print(name, dur, flush=True)
(OUT/'evidence.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
