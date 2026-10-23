"""Cut generated sprite cells and register them using rigid translation/uniform scale only."""
from pathlib import Path
import json,sys
import numpy as np
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent;assets=root/'assets/run-v6';qa=root/'qa/run-v6';qa.mkdir(parents=True,exist_ok=True)
manifest=[]
def isolate_figures(im,pixel=False):
 a=np.array(im);mask=a[:,:,3]>25;parent=[];runs=[];previous=[]
 def find(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for y,row in enumerate(mask):
  edges=np.flatnonzero(np.diff(np.r_[False,row,False].astype(np.int8)));current=[];p=0
  for left,right in zip(edges[::2],edges[1::2]):
   k=len(parent);parent.append(k);runs.append((y,int(left),int(right),k));current.append((left,right,k))
   while p<len(previous) and previous[p][1]<left:p+=1
   q=p
   while q<len(previous) and previous[q][0]<=right:
    parent[find(previous[q][2])]=find(k);q+=1
  previous=current
 groups={}
 for y,l,r,k in runs:
  k=find(k);v=groups.setdefault(k,{'area':0,'box':[l,y,r,y+1],'runs':[]});v['area']+=r-l;v['box']=[min(v['box'][0],l),min(v['box'][1],y),max(v['box'][2],r),max(v['box'][3],y+1)];v['runs'].append((y,l,r))
 major=sorted(groups.values(),key=lambda v:v['area'],reverse=True)[:9]
 if len(major)!=9:raise ValueError('Expected nine disconnected figures')
 major.sort(key=lambda v:(v['box'][1]+v['box'][3])/2)
 ordered=[]
 for row in range(3):ordered.extend(sorted(major[row*3:row*3+3],key=lambda v:(v['box'][0]+v['box'][2])/2))
 # Use original sheet coordinate system within each row/column for stable registration;
 # a 20% overlap captures figures crossing nominal cells, connected masks exclude neighbors.
 out=[];cw=im.width/3;ch=im.height/3
 for k,v in enumerate(ordered):
  l,t,r,b=v['box'];filtered=np.zeros_like(a)
  for yy,ll,rr in v['runs']:filtered[yy,ll:rr]=a[yy,ll:rr]
  # Preserve disconnected fine strokes immediately next to this figure, without neighbors.
  for other in groups.values():
   if other is v or other['area']>v['area']*.08:continue
   ol,ot,orr,ob=other['box']
   if ol>=l-8 and orr<=r+8 and ot>=t-8 and ob<=b+8:
    for yy,ll,rr in other['runs']:filtered[yy,ll:rr]=a[yy,ll:rr]
  # Expanded equal cells retain relative registration without cutting any connected contour.
  x=k%3;y=k//3;box=(round((x-.20)*cw),round((y-.20)*ch),round((x+1.20)*cw),round((y+1.20)*ch))
  out.append(Image.fromarray(filtered).crop(box).resize((384,384),Image.Resampling.NEAREST if pixel else Image.Resampling.LANCZOS))
 return out
for n in range(1,17):
 path=assets/f'owner-{n:02}-sheet.png'
 if not path.exists():continue
 im=Image.open(path).convert('RGBA');w,h=im.size;cells=[];bounds=[]
 for k,c in enumerate(isolate_figures(im,n==16)):
  a=np.array(c);mask=a[:,:,3]>35
  # Remove disconnected micro-specks only; never paint or alter the animal face.
  a[~mask,3]=0;c=Image.fromarray(a);b=c.getbbox()
  if not b:raise ValueError(f'Empty era {n} pose {k}')
  if b[0]<3 or b[1]<3 or b[2]>381 or b[3]>381:print(f'WARN cell edge era={n} pose={k} bounds={b}')
  cells.append(c);bounds.append(b)
 anchors=[]
 for c,b in zip(cells,bounds):
  a=np.array(c)[:,:,3];yy,xx=np.nonzero((a>100)&(np.indices(a.shape)[0]>b[1]+(b[3]-b[1])*.65))
  anchors.append(float(np.median(xx)) if len(xx) else (b[0]+b[2])/2)
 maxw=max(b[2]-b[0] for b in bounds);maxh=max(b[3]-b[1] for b in bounds)
 scale=min(342/maxw,330/maxh,215/max(an-b[0] for an,b in zip(anchors,bounds)),149/max(b[2]-an for an,b in zip(anchors,bounds)),1.12)
 target=assets/f'era-{n:02}';target.mkdir(exist_ok=True);frames=[];outbounds=[]
 for k,(c,b) in enumerate(zip(cells,bounds)):
  anchor=anchors[k]
  resized=c.resize((round(384*scale),round(384*scale)),Image.Resampling.NEAREST if n==16 else Image.Resampling.LANCZOS)
  out=Image.new('RGBA',(384,384));out.alpha_composite(resized,(round(225-anchor*scale),round(350-b[3]*scale)))
  name=f'pose-{k}.png';out.save(target/name);frames.append(name);outbounds.append(out.getbbox())
 b=outbounds[0]
 manifest.append({'era':n,'frames':frames,'anchorX':225,'footY':350,'neutralWidth':b[2]-b[0],'neutralHeight':b[3]-b[1],'sourceSize':[w,h],'sourceCellBounds':bounds,'registeredBounds':outbounds,'uniformScale':scale,'method':'genuine redrawn poses; uniform scale and rigid foot/body registration; no facial deformation'})
(assets/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
for page in range(4):
 subset=[m for m in manifest if page*4<m['era']<=page*4+4]
 if not subset:continue
 sheet=Image.new('RGB',(9*192,4*220),'#66635c');d=ImageDraw.Draw(sheet)
 for row,m in enumerate(subset):
  for k,name in enumerate(m['frames']):
   c=Image.open(assets/f"era-{m['era']:02}"/name).resize((192,192));sheet.paste(c,(k*192,row*220),c);d.text((k*192+4,row*220+198),f"era {m['era']:02} pose {k}",fill='white')
 sheet.save(qa/f'redraws-{page+1}.jpg')
print(json.dumps({'eras':len(manifest),'poses':len(manifest)*9,'qa':str(qa)}))
