from pathlib import Path
from PIL import Image, ImageDraw
root = Path(__file__).parent / 'out-r2'
frames = sorted((root/'frames').glob('*.jpg'))
for page in range(4):
    sheet = Image.new('RGB', (1080, 1560), '#071821')
    draw = ImageDraw.Draw(sheet)
    for slot, file in enumerate(frames[page*48:(page+1)*48]):
        im = Image.open(file); im.thumbnail((135, 240))
        x, y = slot % 8 * 135, slot // 8 * 260
        sheet.paste(im, (x,y)); draw.text((x+3,y+241), f'{int(file.stem)/24:.3f}s', fill='white')
    sheet.save(root/f'continuous-{page+1}.jpg', quality=92)
