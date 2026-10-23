"""Register new four-pose species sheets; retain nine proven v8 species sets."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent
assets=root/'assets/run-v9';qa=root/'qa/run-v9';qa.mkdir(parents=True,exist_ok=True)
replaced={8,9,10,11,12,14,16}
old=json.loads((root/'assets/run-v8/manifest.json').read_text('utf8'))
plan=json.loads((root/'production-plan-run-v9.json').read_text('utf8'))
manifest=[];provenance=[]
def clean_cell(a):
 mask=a[:,:,3]>35;parents=[];runs=[];prev=[]
 def find(i):
  while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
  return i
 for y,row in enumerate(mask):
  edges=np.flatnonzero(np.diff(np.r_[False,row,False].astype(np.int8)));cur=[];p=0
  for left,right in zip(edges[::2],edges[1::2]):
   k=len(parents);parents.append(k);runs.append((y,int(left),int(right),k));cur.append((left,right,k))
   while p<len(prev) and prev[p][1]<left:p+=1
   q=p
   while q<len(prev) and prev[q][0]<=right:parents[find(prev[q][2])]=find(k);q+=1
  prev=cur
 groups={}
 for y,l,r,k in runs:
  v=groups.setdefault(find(k),{'area':0,'box':[l,y,r,y+1],'runs':[]});v['area']+=r-l;v['box']=[min(v['box'][0],l),min(v['box'][1],y),max(v['box'][2],r),max(v['box'][3],y+1)];v['runs'].append((y,l,r))
 main=max(groups.values(),key=lambda v:v['area']);l,t,r,b=main['box'];out=np.zeros_like(a)
 for v in groups.values():
  vl,vt,vr,vb=v['box']
  if v is main or (vl>=l-5 and vr<=r+5 and vt>=t-5 and vb<=b+5):
   for y,left,right in v['runs']:out[y,left:right]=a[y,left:right]
 return out
for n in range(1,17):
 if n not in replaced:
  m=old[n-1].copy();m['sourceVersion']='run-v8';m['species']=plan['timeline']['shots'][n-1]['owner'];manifest.append(m);continue
 path=assets/f'owner-{n:02}-sheet.png';im=Image.open(path).convert('RGBA');w,h=im.size
 cells=[];bounds=[];anchors=[]
 for k in range(4):
  x=k%2;y=k//2
  c=im.crop((round(x*w/2),round(y*h/2),round((x+1)*w/2),round((y+1)*h/2))).resize((384,384),Image.Resampling.NEAREST if n==16 else Image.Resampling.LANCZOS)
  a=clean_cell(np.array(c));a[a[:,:,3]<35,3]=0;c=Image.fromarray(a);b=c.getbbox()
  if not b:raise ValueError(f'Empty {n} {k}')
  cells.append(c);bounds.append(b)
  yy,xx=np.nonzero((a[:,:,3]>100)&(np.indices(a.shape[:2])[0]>b[3]-(b[3]-b[1])*.10))
  anchors.append(float(np.median(xx)))
 maxw=max(b[2]-b[0] for b in bounds);maxh=max(b[3]-b[1] for b in bounds)
 scale=min(342/maxw,330/maxh,215/max(an-b[0] for an,b in zip(anchors,bounds)),149/max(b[2]-an for an,b in zip(anchors,bounds)),1.12)
 target=assets/f'era-{n:02}';target.mkdir(exist_ok=True);outbounds=[]
 names=['pose-0.png','pose-1.png','pose-3.png','pose-4.png']
 for c,b,anchor,name in zip(cells,bounds,anchors,names):
  resized=c.resize((round(384*scale),round(384*scale)),Image.Resampling.NEAREST if n==16 else Image.Resampling.LANCZOS)
  out=Image.new('RGBA',(384,384));out.alpha_composite(resized,(round(225-anchor*scale),round(350-b[3]*scale)));out.save(target/name);outbounds.append(out.getbbox())
 b=outbounds[0];seam=round(b[1]+(350-b[1])*.91);base=Image.open(target/names[0]).convert('RGBA')
 for name in names[1:]:
  pic=Image.open(target/name).convert('RGBA');pic.paste(base.crop((0,seam,384,384)),(0,seam));pic.save(target/name)
 frames=[names[k] for k in [0,1,1,2,3,3,3,3,3]]
 m={'era':n,'species':plan['timeline']['shots'][n-1]['owner'],'frames':frames,'anchorX':225,'footY':350,'neutralWidth':b[2]-b[0],'neutralHeight':b[3]-b[1],'sourceSize':[w,h],'sourceCellBounds':bounds,'registeredBounds':outbounds,'uniformScale':scale,'staticLowerBodyFromY':seam,'method':'new species, built-in imagegen 2x2 four-pose sheet; rigid registration/uniform scale; static feet; no face mesh, yaw or crossfade'}
 manifest.append(m);provenance.append({'era':n,'file':str(path.relative_to(root)).replace('\\','/'),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'generator':'built-in image_gen','actual_drawings':4,'source_original':next(v['path'] for v in json.loads((assets/'prompts.json').read_text('utf8')) if v['era']==n)})
(assets/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
(assets/'provenance.json').write_text(json.dumps({'newSpecies':provenance,'preservedSpecies':[n for n in range(1,17) if n not in replaced],'preservedSource':'assets/run-v8/manifest.json'},indent=2),encoding='utf8')
board=Image.new('RGB',(4*300,7*330),'#5d5f5b');d=ImageDraw.Draw(board)
for row,n in enumerate(sorted(replaced)):
 m=manifest[n-1]
 for col,k in enumerate([0,1,3,4]):
  c=Image.open(assets/f'era-{n:02}'/m['frames'][k]).resize((300,300));board.paste(c,(col*300,row*330),c);d.text((col*300+5,row*330+305),f'era {n:02} / pose {k}',fill='white')
board.save(qa/'new-species-poses.jpg')
for s in plan['timeline']['shots']:s['assetStatus']='new_species_four_pose_ready' if int(s['id'][-2:]) in replaced else 'preserved_v8_species_pose_ready'
plan['animationImageContract']['status']='implemented; night-heron v4 retained; nine v8 and seven new v9 owner sets ready'
(root/'production-plan-run-v9.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
assert len(set(s['owner'] for s in plan['timeline']['shots']))==16
print(json.dumps({'eras':len(manifest),'unique_species':16,'new_sheets':len(replaced),'new_drawings':len(replaced)*4}))
