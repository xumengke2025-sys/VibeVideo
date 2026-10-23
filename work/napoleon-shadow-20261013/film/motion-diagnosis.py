from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent
frames = root / 'out/final-v1/frames'
out = root / 'out/motion-diagnosis'
out.mkdir(exist_ok=True)
spans = {
    'flag': [2, 3, 4, 5, 6, 7, 8, 9],
    'touch': [18, 19, 20, 21, 22, 23, 24, 25],
    'horse': [35, 35.5, 36, 36.5, 37, 37.5, 38, 38.5],
    'crown': [52, 53, 54, 55, 56, 59, 60, 61],
}
for name, times in spans.items():
    sheet = Image.new('RGB', (1440, 1344), '#e7d5b6')
    pen = ImageDraw.Draw(sheet)
    for j, t in enumerate(times):
        x, y = (j % 4) * 360, (j // 4) * 672
        sheet.paste(Image.open(frames / f'{round(t * 24):05d}.jpg').resize((360, 640)), (x, y))
        pen.text((x + 10, y + 645), f'{t:.2f}s', fill='black')
    sheet.save(out / f'{name}.jpg')
print(out)
