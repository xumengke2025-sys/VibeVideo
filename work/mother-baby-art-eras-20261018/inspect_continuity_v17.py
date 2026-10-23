from pathlib import Path
import json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
Q=R/'qa/v17';Q.mkdir(parents=True,exist_ok=True)
manifest=json.loads((R/'assets/motion-v16/manifest.json').read_text())
for batch in range(4):
    board=Image.new('RGB',(3*350,5*300),'#eee5d8');d=ImageDraw.Draw(board)
    for row,i in enumerate(range(batch*5,batch*5+5)):
        s=manifest['scenes'][i];im=Image.open(R/'assets/motion-v16'/s['file'])
        for col,k in enumerate([0,24,47]):
            w,h=s['width'],s['height'];frame=im.crop((k%6*w,k//6*h,k%6*w+w,k//6*h+h))
            cv=Image.new('RGB',(700,560),'#efe6d5');cv.paste(frame,(s['x']-180,s['y']-980));cv.thumbnail((350,280))
            x=col*350;y=row*300;board.paste(cv,(x,y+20));d.text((x+5,y+4),f'{i:02d} {s["slug"]} F{k:02d}',fill='#342c24')
    board.save(Q/f'endpoints-{batch}.jpg')
print(Q)
