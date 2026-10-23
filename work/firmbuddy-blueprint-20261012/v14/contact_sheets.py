from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;B=R.parent
O=B/'out/stills-v14-checked'
times=[20.3,21,21.7,39.5,40.2,40.9,51.1,51.8,52.5,65.1,65.8,66.5,75.5,76.2,76.9,81.9,82.6,83.3]
sheet=Image.new('RGB',(1920,6*390),'#0b1c2c');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',23)
for i,t in enumerate(times):
 im=Image.open(O/f'{t:g}.png').convert('RGB');im.thumbnail((640,360));x=(i%3)*640;y=(i//3)*390;sheet.paste(im,(x,y));d.text((x+12,y+364),f'{t:.1f}s',font=font,fill='white')
sheet.save(O/'six-unloads.jpg',quality=94)
print(O/'six-unloads.jpg')
