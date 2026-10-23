from pathlib import Path
from PIL import Image,ImageDraw
import sys,math
folder=Path(sys.argv[1]); out=Path(sys.argv[2]); step=int(sys.argv[3]) if len(sys.argv)>3 else 30
files=sorted(folder.glob('*.jpg'))[::step]; w=480; h=292; cols=4
sheet=Image.new('RGB',(w*cols,h*math.ceil(len(files)/cols)), '#101e29');d=ImageDraw.Draw(sheet)
for i,f in enumerate(files):
 im=Image.open(f);im.thumbnail((w,270));x=i%cols*w;y=i//cols*h;sheet.paste(im,(x,y));d.text((x+8,y+273),f'frame {f.stem}',fill='white')
sheet.save(out)
