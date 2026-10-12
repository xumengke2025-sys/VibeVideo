from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageStat
import json
root=Path(__file__).parent
for name in ['beach','reel']:
    out=root/'reference-output'/name
    files=sorted(out.glob('still-*.jpg'))
    w,h=480,270; sheet=Image.new('RGB',(w*3,(h+26)*((len(files)+2)//3)), '#0b161b');d=ImageDraw.Draw(sheet)
    info=json.loads((out/'capture-evidence.json').read_text())
    for i,p in enumerate(files):
        im=Image.open(p);im.thumbnail((w,h));x=i%3*w;y=i//3*(h+26);sheet.paste(im,(x,y));d.text((x+8,y+h+4),f'{name} / {info["times"][i]:.3f}s',fill='white')
    sheet.save(out/'stills-sheet.jpg',quality=93)
    a=Image.open(out/'repeat-a.jpg').convert('RGB');b=Image.open(out/'repeat-b.jpg').convert('RGB');diff=ImageChops.difference(a,b);stat=ImageStat.Stat(diff)
    info['repeat']['meanAbsRGB_0_255']=stat.mean;info['repeat']['differenceBBox']=diff.getbbox()
    (out/'capture-evidence.json').write_text(json.dumps(info,ensure_ascii=False,indent=2))
    print(name, 'repeat MAE', stat.mean)
