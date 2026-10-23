from pathlib import Path
from PIL import Image, ImageDraw
root = Path(__file__).resolve().parent
out = root / 'out/motion-v2-verification'
out.mkdir(exist_ok=True)
spans = {'flag': [1,2,3,4,5,6,7,8], 'touch': [18,19,20,21,22,23,25,27], 'horse': [35,36,37,38,40,43,45,46], 'crown': [51.5,53,54.5,56,57.5,59,60,61]}
for name, times in spans.items():
    sheet = Image.new('RGB', (1440,1344), '#e7d5b6')
    pen = ImageDraw.Draw(sheet)
    for j,t in enumerate(times):
        p = root / 'out/final-v2/frames' / f'{round(t*24):05d}.jpg'
        if name == 'crown':
            p = root / 'out/sample-human-v2/frames' / f'{round((t-51.4)*24):05d}.jpg'
        x,y = (j%4)*360,(j//4)*672
        sheet.paste(Image.open(p).resize((360,640)), (x,y))
        pen.text((x+10,y+645), f'{t:.2f}s', fill='black')
    sheet.save(out / f'{name}.jpg')
print(out)
