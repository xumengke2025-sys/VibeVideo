from pathlib import Path
from PIL import Image,ImageDraw
import sys,json
root=Path(__file__).parent
version=sys.argv[1]
directory=root/'out'/version
frames=sorted((directory/'frames').glob('*.jpg'))
selected=frames[::3]
canvas=Image.new('RGB',(216*9,410*6),'#242424');d=ImageDraw.Draw(canvas)
for i,f in enumerate(selected[:54]):
    im=Image.open(f).convert('RGB');im.thumbnail((216,384))
    x=(i%9)*216;y=(i//9)*410;canvas.paste(im,(x,y));d.text((x+5,y+386),f.stem,fill='#eeeeee')
canvas.save(directory/'contact.jpg',quality=92)
print(directory/'contact.jpg')
