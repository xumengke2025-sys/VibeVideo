from pathlib import Path
from PIL import Image, ImageDraw
import json
root=Path(__file__).parent
out=root/'out/film-v3'
qa=root/'qa/film-v3'
qa.mkdir(parents=True,exist_ok=True)
frames=list(range(0,960,12))
for page in range(2):
    sheet=Image.new('RGB',(1200,2190),'#242a2c'); draw=ImageDraw.Draw(sheet)
    for k,f in enumerate(frames[page*40:(page+1)*40]):
        im=Image.open(out/'frames'/f'{f:05}.jpg').resize((225,400))
        x=12+(k%5)*238;y=12+(k//5)*272
        # Portrait thumbnails at readable ratio, five columns and eight rows.
        im.thumbnail((225,240))
        sheet.paste(im,(x,y));draw.text((x,y+242),f'frame {f} | {f/24:.2f}s',fill='white')
    sheet.save(qa/f'contact-{page+1}.jpg',quality=92)
e=json.loads((out/'evidence.json').read_text(encoding='utf8'))
print(json.dumps({'sha256':e['sha256'],'selectedFrames':frames,'contacts':2}))
