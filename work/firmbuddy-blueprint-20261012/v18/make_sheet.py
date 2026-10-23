from pathlib import Path
import sys,json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;O=R.parent/'out'/sys.argv[1]
cfg=json.loads((O/'config.json').read_text());start=cfg['start'];fps=cfg['fps'];count=cfg['count']
step=int(sys.argv[2]) if len(sys.argv)>2 else 18
ids=list(range(0,count,step));w,h=480,270;cols=4
sheet=Image.new('RGB',(w*cols,((len(ids)+cols-1)//cols)*(h+27)),'#101e2c');d=ImageDraw.Draw(sheet);f=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
for j,i in enumerate(ids):
 im=Image.open(O/'frames'/f'{i:05d}.jpg').convert('RGB').resize((w,h));x=j%cols*w;y=j//cols*(h+27);sheet.paste(im,(x,y));d.text((x+8,y+h+2),f'{start+i/fps:.2f}s',font=f,fill='white')
sheet.save(O/'sequence.jpg',quality=94);print(str(O/'sequence.jpg'))
