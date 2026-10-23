from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse
p=argparse.ArgumentParser();p.add_argument('folder');p.add_argument('--start',type=float,default=16);p.add_argument('--times',required=True);p.add_argument('--name',default='contact.jpg');p.add_argument('--fps',type=int,default=30);a=p.parse_args()
root=Path(a.folder);times=[float(t) for t in a.times.split(',')];w=480;h=270;cols=3;rows=(len(times)+cols-1)//cols
canvas=Image.new('RGB',(w*cols,(h+30)*rows),'#111e2c');d=ImageDraw.Draw(canvas)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',19)
for i,t in enumerate(times):
    fp=root/'frames'/f'{round((t-a.start)*a.fps):05}.jpg'
    im=Image.open(fp).convert('RGB');im.thumbnail((w,h));x=(i%cols)*w;y=(i//cols)*(h+30);canvas.paste(im,(x,y));d.text((x+10,y+h+4),f'{t:.2f}s',font=font,fill='white')
canvas.save(root/a.name,quality=93);print(root/a.name)
