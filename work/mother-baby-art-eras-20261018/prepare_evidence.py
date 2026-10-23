"""Local contact sheets from actual rendered/decoded frames; no review claims."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,sys,hashlib
root=Path(__file__).resolve().parent
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',20)
def sheet(files,out,cols,per,width,crop=None):
    out.mkdir(parents=True,exist_ok=True)
    records=[]
    for start in range(0,len(files),per):
        subset=files[start:start+per]
        tiles=[]
        for file in subset:
            im=Image.open(file).convert('RGB')
            if crop:
                w,h=im.size;im=im.crop(tuple(round(v*(w if i%2==0 else h)) for i,v in enumerate(crop)))
            im=im.resize((width,round(width*im.height/im.width)))
            tiles.append(im)
        th=tiles[0].height+34
        canvas=Image.new('RGB',(cols*width,((len(tiles)+cols-1)//cols)*th),'#f3eddc')
        draw=ImageDraw.Draw(canvas)
        for i,(im,file) in enumerate(zip(tiles,subset)):
            x=i%cols*width;y=i//cols*th
            canvas.paste(im,(x,y));draw.text((x+8,y+im.height+3),file.stem,fill='#292d39',font=font)
        dest=out/f'page-{start//per:03d}.jpg';canvas.save(dest,quality=94)
        records.append({'start_index':start,'end_index':start+len(subset)-1,'path':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
    (out/'sheets.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'pages':len(records),'folder':str(out)},ensure_ascii=False))
if sys.argv[1]=='styles':
    sheet(sorted((root/'out/style-stills').glob('*.png')),root/'out/style-sheets',5,10,270)
elif sys.argv[1]=='sample':
    sheet(sorted((root/'out/sample-v2/frames').glob('*.jpg'))[::4],root/'out/sample-v2/action-sheets',5,10,300,(.23,.51,.80,.80))
elif sys.argv[1]=='review':
    sheet(sorted((root/'qa/v1/frames/frames').glob('*.jpg')),root/'qa/v1/character-sheets',5,30,300,(.23,.51,.81,.80))
