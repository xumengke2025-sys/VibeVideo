from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import sys
p=Path(sys.argv[1]);files=sorted(p.glob('*.png'),key=lambda x:float(x.stem));w=270;h=480;cols=3;sheet=Image.new('RGB',(cols*w,((len(files)+cols-1)//cols)*(h+28)), '#151c24');d=ImageDraw.Draw(sheet)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGB');im=ImageOps.fit(im,(w,h));x=i%cols*w;y=i//cols*(h+28);sheet.paste(im,(x,y));d.text((x+9,y+h+5),f.stem+' seconds',fill='#e5ddca')
sheet.save(p/'contact.jpg',quality=92);print(p/'contact.jpg')
