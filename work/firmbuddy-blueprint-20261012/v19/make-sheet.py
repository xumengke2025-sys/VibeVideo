from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse
p=argparse.ArgumentParser();p.add_argument('--folder',required=True);p.add_argument('--times',required=True);p.add_argument('--start',type=float,default=0);p.add_argument('--fps',type=float,default=30);p.add_argument('--name',default='sequence.jpg');a=p.parse_args()
O=Path(a.folder);times=list(map(float,a.times.split(',')));w,h=480,270;cols=4
im=Image.new('RGB',(w*cols,((len(times)+cols-1)//cols)*(h+24)),'#101e2c');d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
for i,t in enumerate(times):
 f=O/'frames'/f'{round((t-a.start)*a.fps):05d}.jpg';q=Image.open(f).convert('RGB').resize((w,h));x=(i%cols)*w;y=(i//cols)*(h+24);im.paste(q,(x,y));d.text((x+10,y+h+2),f'{t:.2f}s',font=font,fill='white')
im.save(O/a.name,quality=94);print(O/a.name)
