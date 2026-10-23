from pathlib import Path
import json
from PIL import Image,ImageDraw
import numpy as np
R=Path(__file__).resolve().parent;Q=R/'qa/v18'
board=Image.new('RGB',(1400,4*305),'#292437');draw=ImageDraw.Draw(board)
for row,(name,f) in enumerate([('scene-00.png',12),('scene-00.png',26),('bridge-19.png',12),('scene-19.png',24)]):
    for col,v in enumerate([17,18]):
        m=json.loads((R/f'assets/motion-v{v}/manifest.json').read_text());r=next(a for a in m['scenes']+m['bridges'] if a['file']==name)
        im=Image.open(R/f'assets/motion-v{v}'/name);x=f%6*700;y=f//6*560;im=im.crop((x,y,x+700,y+560))
        yy,xx=np.mgrid[:560,:700];tile=((xx//20+yy//20)%2);rgb=np.where(tile[:,:,None],np.array([157,72,141]),np.array([59,107,125])).astype(np.uint8)
        bg=Image.fromarray(rgb).convert('RGBA');bg.alpha_composite(im);bg=bg.resize((350,280));x=col*700;py=row*305;board.paste(bg.convert('RGB'),(x,py+25));draw.text((x+5,py+5),f'v{v} {name} F{f}',fill='white')
        # Display gap detail beside full pair.
        detail=Image.fromarray(rgb).convert('RGBA');detail.alpha_composite(im);detail=detail.crop((280,250,530,500)).resize((280,280));board.paste(detail.convert('RGB'),(x+365,py+25))
board.save(Q/'alpha-before-after.jpg')
print('alpha comparison ready')
