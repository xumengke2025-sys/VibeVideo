"""Measure existing alpha only. PNGs are never modified; Canvas uses these source rectangles."""
from pathlib import Path
from PIL import Image
import json
root=Path(__file__).parent
rows=[]
for file in sorted((root/'assets/rebuild-v3').glob('era-*.png')):
    im=Image.open(file).convert('RGBA'); w,h=im.size; alpha=im.getchannel('A')
    parts={}
    for col,names in [(0,['body','neck','fish']),(1,['head','owner'])]:
        x0=col*w//2;x1=(col+1)*w//2
        a=alpha.crop((x0,0,x1,h)); data=a.load()
        active=[sum(data[x,y]>100 for x in range(a.width))>5 for y in range(h)]
        bands=[];start=None
        for y,on in enumerate(active+[False]):
            if on and start is None:start=y
            if not on and start is not None:
                if bands and start-bands[-1][1]<12:bands[-1][1]=y
                else:bands.append([start,y])
                start=None
        bands=[b for b in bands if b[1]-b[0]>20]
        if len(bands)!=len(names):raise ValueError(f'{file.name} col{col}: {bands}')
        for name,(y0,y1) in zip(names,bands):
            # A pelican's long bill crosses the nominal atlas column. Keep its whole silhouette.
            part_x0=int(w*.39) if name=='owner' and file.stem=='era-03' else x0
            # Use actual alpha bounds after identifying the major separated bands.
            y0=max(0,y0-12);y1=min(h,y1+12)
            box=alpha.crop((part_x0,y0,x1,y1)).point(lambda v:255 if v>3 else 0).getbbox()
            l,t,r,b=box
            parts[name]=[max(0,part_x0+l-3),max(0,y0+t-3),min(w,r+part_x0+3)-max(0,part_x0+l-3),min(h,y0+b+3)-max(0,y0+t-3)]
    rows.append({'id':file.stem.split('-')[1],'src':'assets/rebuild-v3/'+file.name,'width':w,'height':h,'parts':parts})
(root/'assets/rebuild-v3/atlas-manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print('Measured',len(rows),'era atlases; preserved source alpha and all original PNGs.')
