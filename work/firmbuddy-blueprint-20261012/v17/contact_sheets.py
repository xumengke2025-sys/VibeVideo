from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parent
name=sys.argv[1]
O=R.parent/'out'/name
times=[float(t) for t in sys.argv[2].split(',')]
config=json.loads((O/'config.json').read_text(encoding='utf-8'))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
for page in range((len(times)+11)//12):
    ts=times[page*12:(page+1)*12]
    sheet=Image.new('RGB',(1920,294*((len(ts)+3)//4)),'#112338');d=ImageDraw.Draw(sheet)
    for i,t in enumerate(ts):
        frame=round((t-config['start'])*config['fps'])
        im=Image.open(O/'frames'/f'{frame:05d}.jpg').resize((480,270))
        x=i%4*480;y=i//4*294;sheet.paste(im,(x,y));d.text((x+8,y+272),f'{t:.2f}s',fill='white',font=font)
    sheet.save(O/f'continuity-{page+1}.jpg',quality=94)
(O/'observation-times.json').write_text(json.dumps(dict(prepared=times,actually_viewed=False)),encoding='utf-8')
print(str(O))
