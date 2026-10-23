from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json
R=Path(__file__).resolve().parent;O=R.parent/'out/sample-v16-industry-continuity'
times=[59.6,60.4,61.2,62,62.8,63.6,64.4,65.2,66.4,68,70,72,72.8,73.2,73.6,74,74.4,74.8,75.2,75.6,76,76.8,77.6]
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
for page in range(2):
 ts=times[page*12:(page+1)*12];sheet=Image.new('RGB',(1920,882),'#112338');d=ImageDraw.Draw(sheet)
 for i,t in enumerate(ts):
  index=round((t-58)*30);im=Image.open(O/'frames'/f'{index:05d}.jpg').resize((480,270));x=i%4*480;y=i//4*294;sheet.paste(im,(x,y));d.text((x+8,y+272),f'{t:.2f}s',fill='white',font=font)
 sheet.save(O/f'continuity-{page+1}.jpg',quality=94)
(O/'sample-observation-times.json').write_text(json.dumps(times),encoding='utf-8')
print('Prepared two sample continuity sheets.')
