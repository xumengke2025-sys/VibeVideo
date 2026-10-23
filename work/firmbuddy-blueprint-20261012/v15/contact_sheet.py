from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,sys
R=Path(__file__).resolve().parent;name=sys.argv[1] if len(sys.argv)>1 else 'sample-v15-expert-continuity';O=R.parent/'out'/name
cfg=json.loads((O/'config.json').read_text());start=cfg['start'];fps=cfg['fps'];count=cfg['count']
step=30 if count<1000 else 120
frames=list(range(0,count,step))+[count-1]
cols=4;w=480;h=270;rows=(len(frames)+cols-1)//cols
sheet=Image.new('RGB',(cols*w,rows*(h+30)),'#101e2c');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',21)
for i,f in enumerate(frames):
    im=Image.open(O/'frames'/f'{f:05d}.jpg').convert('RGB');im.thumbnail((w,h));x=i%cols*w;y=i//cols*(h+30);sheet.paste(im,(x,y));d.text((x+10,y+h+3),f'{start+f/fps:.2f}s',font=font,fill='white')
sheet.save(O/'contact.jpg',quality=95)
print(str(O/'contact.jpg'))
