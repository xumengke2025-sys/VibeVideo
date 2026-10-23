"""Mechanical alpha cleanup, crop registration and production-sheet assembly."""
from PIL import Image, ImageFilter
from pathlib import Path
import json, hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent
DIR=ROOT/'assets/generated-v2'
src=Image.open(DIR/'modern-character-atlas.png').convert('RGBA')
# The generated atlas has an intentionally taller mother row than baby row.
mom_offsets=[0,429,847,1276]
baby_offsets=[0,467,882,1310]
def extract(box,anchor,size):
    im=src.crop(box)
    a=im.getchannel('A')
    # Remove isolated low-alpha print flecks; retain antialiasing on connected edges.
    strong=a.point(lambda x:255 if x>=150 else 0)
    support=strong.filter(ImageFilter.MaxFilter(5))
    arr=np.asarray(a).copy();arr[np.asarray(support)==0]=0
    im.putalpha(Image.fromarray(arr))
    out=Image.new('RGBA',size)
    out.alpha_composite(im,(box[0]-anchor,box[1]))
    return out
pack=Image.new('RGBA',(2518,920))
bg=Image.open(DIR/'modern-background.png').convert('RGBA').resize((518,920),Image.Resampling.LANCZOS)
pack.alpha_composite(bg,(0,0))
for n,offset in enumerate(mom_offsets):
    lo=[0,530,946,1370][n]; hi=[530,946,1370,1774][n]
    im=extract((lo,0,hi,590),offset,(500,610))
    im.save(DIR/f'modern-mother-{n}.png')
    pack.alpha_composite(im,(518+n*500,0))
for n,offset in enumerate(baby_offsets):
    lo=[40,530,943,1367][n];hi=[520,916,1323,1774][n]
    im=src.crop((lo,590,hi,887))
    a=np.asarray(im.getchannel('A')).copy();a[a<100]=0;im.putalpha(Image.fromarray(a))
    out=Image.new('RGBA',(500,310));out.alpha_composite(im,(lo-offset,0))
    out.save(DIR/f'modern-baby-{n}.png')
    pack.alpha_composite(out,(518+n*500,610))
pack.save(DIR/'production-template.png')
manifest={p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'size':Image.open(p).size} for p in DIR.glob('*.png')}
(DIR/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'assets':len(manifest),'template':str(DIR/'production-template.png')},ensure_ascii=False))
