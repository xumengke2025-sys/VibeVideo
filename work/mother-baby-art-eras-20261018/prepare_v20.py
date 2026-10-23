from pathlib import Path
import json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
Q=R/'qa/v20';Q.mkdir(exist_ok=True)
M=json.loads((R/'assets/motion-v19/manifest.json').read_text())
for b in range(5):
    board=Image.new('RGB',(1400,660),'#bba5ba');d=ImageDraw.Draw(board)
    for k,r in enumerate(M['scenes'][b*4:b*4+4]):
        a=Image.open(R/'assets/motion-v19'/r['file']).convert('RGBA').crop((0,0,700,560))
        im=a.crop((50,400,400,530));base=Image.new('RGBA',im.size,'#bba5ba');base.alpha_composite(im)
        x0=k%2*700;y0=k//2*330+45
        board.paste(base.convert('RGB').resize((700,260)),(x0,y0));d.text((x0+5,y0-35),f"ERA {r['era']} F0 x50-400 y400-530",fill='black')
        for x in range(50,401,25):
            xx=x0+(x-50)*2;d.line((xx,y0,xx,y0+260),fill='#998699',width=1);d.text((xx+1,y0-17),str(x),fill='black')
        for y in range(400,531,20):
            yy=y0+(y-400)*2;d.line((x0,yy,x0+700,yy),fill='#998699',width=1);d.text((x0+1,yy+1),str(y),fill='black')
    board.save(Q/f'reference-grid-{b}.jpg',quality=98)
for b in range(4):
    board=Image.new('RGB',(1400,700),'#d0acbb');d=ImageDraw.Draw(board)
    for k,r in enumerate(M['scenes'][b*5:b*5+5]):
        a=Image.open(R/'assets/motion-v19'/r['file']).convert('RGBA')
        for j,f in enumerate([0,12,24,36,47]):
            im=a.crop((f%6*700,f//6*560,f%6*700+700,f//6*560+560)).crop((50,375,400,535))
            back=Image.new('RGBA',im.size,'#bba5ba');back.alpha_composite(im)
            board.paste(back.convert('RGB').resize((280,128)),(j*280,k*140+12));d.text((j*280+3,k*140),f"{r['era']:02d} F{f}",fill='black')
    board.save(Q/f'cushion-input-{b}.jpg',quality=96)
scenes=json.loads((R/'film/chase-scenes-v9.js').read_text(encoding='utf-8').split('=',1)[1].strip().rstrip(';'))
for b in range(4):
    board=Image.new('RGB',(1350,960),'#eee');d=ImageDraw.Draw(board)
    for k,e in enumerate(scenes[b*5:b*5+5]):
        im=Image.open((R/'film'/e['background']).resolve());board.paste(im.resize((270,960)),(k*270,0));d.rectangle((k*270,0,k*270+50,25),fill='white');d.text((k*270+5,5),str(e['index']),fill='black')
    board.save(Q/f'background-input-{b}.jpg',quality=95)
