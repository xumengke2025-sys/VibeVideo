from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;Q=R/'qa/v20';M=json.loads((R/'assets/motion-v20/manifest.json').read_text());pillows=Image.open(R/'assets/motion-v20/cushions-atlas.png').convert('RGBA')
for b in range(4):
    out=Image.new('RGB',(1500,1000),'#e5d8bf');d=ImageDraw.Draw(out)
    for row,r in enumerate(M['scenes'][b*5:b*5+5]):
        a=Image.open(R/'assets/motion-v20'/r['file']).convert('RGBA');i=r['era'];p=pillows.crop((i%5*300,i//5*90,i%5*300+300,i//5*90+90)).resize((290,87))
        for j,f in enumerate([0,12,24,36,47]):
            im=Image.new('RGBA',(700,560),'#e5d8bf');im.alpha_composite(p,(130,455));im.alpha_composite(a.crop((f%6*700,f//6*560,f%6*700+700,f//6*560+560)))
            out.paste(im.crop((85,300,450,540)).resize((300,180)).convert('RGB'),(j*300,row*200+20));d.text((j*300+5,row*200+4),f'{i:02d} F{f}',fill='black')
    out.save(Q/f'fixed-cushions-{b}.jpg',quality=96)
