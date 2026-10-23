from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
import build_continuity_v17 as b
R=Path(__file__).resolve().parent;Q=R/'qa/v18';Q.mkdir(exist_ok=True)
board=Image.new('RGB',(1400,1120),'#43284e');d=ImageDraw.Draw(board)
for n,i in enumerate([0,4,8,12,18,19]):
    frames=b.modern_cels() if i==19 else b.stabilize(b.cels(b.EVIDENCE[i]))[0]
    for j,k in enumerate([0,len(frames)//2,len(frames)-1]):
        im=Image.fromarray(b.straight(frames[k]));bg=Image.new('RGBA',im.size,'#b4269a');bg.alpha_composite(im);bg=bg.resize((350,280))
        x=(n%2)*700+(j%2)*350;y=(n//2)*370
        if j==2:continue
        board.paste(bg.convert('RGB'),(x,y+25));d.text((x+5,y+5),f'era {i} raw pose {k}',fill='white')
board.save(Q/'source-alpha.jpg')
keys=b.generated(19)
b.Q=Q;b.TMP=b.TMP.parent/'mother-baby-v18-rife'
frames=b.run(keys,28,'test-dual')
b.contact(frames,'dual-test')
print('v18 source and dual-matte diagnostic ready')
