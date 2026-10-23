"""Crop generated production packs into registered, alpha-clean animation layers.

This performs mechanical atlas extraction and alpha support cleanup only.
Artwork, identities, poses, costumes, furniture and environments come from image_gen.
"""
from pathlib import Path
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import numpy as np
import json,hashlib
ROOT=Path(__file__).resolve().parent
AS=ROOT/'assets/generated-v2'
OUT=AS/'layers';OUT.mkdir(exist_ok=True)
jobs=json.loads((ROOT/'assets/generation-catalog-v3.json').read_text(encoding='utf8'))
jobs.append({'index':34,'mode':'modern','name':'现代扁平插画'})
manifest={};evidence=[]
def connected_support(alpha,min_area=60):
    binary=alpha>100;parent=[];areas=[];allruns=[];previous=[]
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for y,row in enumerate(binary):
        diff=np.diff(np.r_[False,row,False].astype('int8'));starts=np.where(diff==1)[0];ends=np.where(diff==-1)[0]
        current=[];p=0
        for x0,x1 in zip(starts,ends):
            n=len(parent);parent.append(n);areas.append(int(x1-x0));current.append((int(x0),int(x1),n));allruns.append((y,int(x0),int(x1),n))
            while p<len(previous) and previous[p][1]<x0:p+=1
            q=p
            while q<len(previous) and previous[q][0]<=x1:
                a=find(n);b=find(previous[q][2])
                if a!=b:parent[b]=a;areas[a]+=areas[b]
                q+=1
        previous=current
    keep=np.zeros(binary.shape,dtype=bool)
    for y,x0,x1,n in allruns:
        if areas[find(n)]>=min_area:keep[y,x0:x1]=True
    return keep
def clean(im):
    im=im.convert('RGBA');a=np.array(im.getchannel('A'))
    # Low-alpha detached flecks from the generated print texture are not geometry.
    support=Image.fromarray(np.where(a>180,255,0).astype('uint8')).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(5))
    keep=np.asarray(support)>0
    a[~keep]=0
    # Clean the narrow atlas seams; these must not become vertical set artifacts.
    a[:,:3]=0;a[:,-3:]=0;a[:2,:]=0;a[-2:,:]=0
    valid=connected_support(a)
    valid=Image.fromarray((valid*255).astype('uint8')).filter(ImageFilter.MaxFilter(3))
    a[np.asarray(valid)==0]=0
    im.putalpha(Image.fromarray(a))
    return im
for j in jobs:
    i=j['index'];mode=j['mode'];stem=f'{i:02d}-{mode}'
    src=AS/(f'{stem}-v3-pack.png' if i<34 else '34-modern-pack.png')
    if not src.exists():continue
    im=Image.open(src).convert('RGBA');w,h=im.size;a=np.asarray(im.getchannel('A'))
    coverage=(a>200).mean(axis=0)
    # Infer the real generated panel edge instead of assuming a perfect ratio.
    cand=[x for x in range(int(w*.17),int(w*.25)) if coverage[x]<.80]
    edge=cand[0] if cand else round(w*518/2518)
    bw=(w-edge)/4;split=round(h*610/920)
    folder=OUT/stem;folder.mkdir(exist_ok=True)
    bg=im.crop((0,0,edge,h)).convert('RGB').resize((1080,1920),Image.Resampling.LANCZOS)
    bg.save(folder/'background.jpg',quality=96)
    paths={'background':f'../assets/generated-v2/layers/{stem}/background.jpg','mothers':[],'babies':[]}
    al=[]
    for n in range(4):
      x0=round(edge+n*bw);x1=round(edge+(n+1)*bw)
      for key,y0,y1,oh in [('mother',0,split,610),('baby',split,h,310)]:
        bottle=ROOT/'assets/bottle-v3'/f'era-{i:02d}'/f'baby-{n}.png'
        if key=='baby' and bottle.exists():cel=Image.open(bottle).convert('RGBA').resize((500,oh),Image.Resampling.LANCZOS)
        else:cel=im.crop((x0,y0,x1,y1)).resize((500,oh),Image.Resampling.LANCZOS)
        cel=clean(cel);cel.save(folder/f'{key}-{n}.png')
        paths['mothers' if key=='mother' else 'babies'].append(f'../assets/generated-v2/layers/{stem}/{key}-{n}.png')
        al.append({'sprite':f'{key}-{n}','alpha_extrema':cel.getchannel('A').getextrema(),'bbox':cel.getbbox()})
    manifest[mode]=paths
    evidence.append({'index':i,'mode':mode,'source':str(src.relative_to(ROOT)),'source_size':[w,h],'detected_background_edge':edge,'row_split':split,'alpha':al,'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
(ROOT/'film/generated-manifest.js').write_text('window.GENERATED_ASSETS='+json.dumps(manifest,ensure_ascii=False)+';\n',encoding='utf8')
(AS/'layer-extraction.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'era_count':len(manifest),'missing':[j['mode'] for j in jobs if j['mode'] not in manifest]},ensure_ascii=False))
# One full composition contact sheet, preserving the actual portrait layout.
sheet=Image.new('RGB',(350*7,660*5),'#f4ead9');d=ImageDraw.Draw(sheet)
for j in jobs:
 mode=j['mode'];i=j['index']
 if mode not in manifest:continue
 folder=OUT/f'{i:02d}-{mode}'
 bg=Image.open(folder/'background.jpg').convert('RGBA')
 mom=Image.open(folder/'mother-2.png').resize((400,488),Image.Resampling.LANCZOS)
 baby=Image.open(folder/'baby-3.png').resize((360,223),Image.Resampling.LANCZOS)
 bg.alpha_composite(mom,(480,1010));bg.alpha_composite(baby,(160,1280))
 bg=bg.convert('RGB').resize((350,622),Image.Resampling.LANCZOS);x=(i%7)*350;y=(i//7)*660;sheet.paste(bg,(x,y));d.text((x+8,y+628),f'{i:02d} {mode}',fill='#302d25')
sheet.save(AS/'35-era-contact.jpg',quality=94)
