"""Only extracts generated cells, computes sprite anchors and records provenance.
Visible illustration is never replaced by procedural geometry.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import json,shutil,hashlib,statistics
import numpy as np
R=Path(__file__).resolve().parent
inputs=json.loads((R/'assets/generated-inputs.json').read_text(encoding='utf8'))
dest=R/'assets/v3';originals=dest/'originals';frames=dest/'frames'
originals.mkdir(parents=True,exist_ok=True);frames.mkdir(exist_ok=True)
lib={};metadata=[]
if frames.exists() and not (dest/'frames-grid-history').exists():
 shutil.copytree(frames,dest/'frames-grid-history')
def gutter_boxes(im,cols,rows):
 # Find the actual empty gutters, not the nominal grid. Generated sheets are uneven.
 a=np.array(im.convert('RGBA'))[:,:,3]>35
 def cut(proj,guess,radius):
  lo=max(1,int(guess-radius));hi=min(len(proj)-1,int(guess+radius))
  p=proj[lo:hi];minimum=p.min();ids=np.where(p<=minimum+1)[0]+lo
  # Centre of the contiguous minimum nearest the nominal boundary.
  runs=np.split(ids,np.where(np.diff(ids)>1)[0]+1)
  run=min(runs,key=lambda v:abs(float(v.mean())-guess))
  return int(round(float(run.mean())))
 ys=[0]+[cut(a.sum(1),r*im.height/rows,im.height/rows*.22) for r in range(1,rows)]+[im.height]
 boxes=[]
 for y0,y1 in zip(ys,ys[1:]):
  p=a[y0:y1].sum(0)
  xs=[0]+[cut(p,c*im.width/cols,im.width/cols*.22) for c in range(1,cols)]+[im.width]
  boxes.extend((x0,y0,x1,y1) for x0,x1 in zip(xs,xs[1:]))
 return boxes
def extract(group,im,boxes,actor=False,top=False):
 arr=[]
 for i,box in enumerate(boxes):
  if group in ['boot','surveyor','generalWalk']:
   # Hand-traced empty boundaries around overlapping grid extents, no image warping.
   box=(0,box[1],im.width,box[3])
  cell=im.crop(tuple(map(round,box))).convert('RGBA');a=np.array(cell)
  if group in ['boot','surveyor','generalWalk']:
   mask=Image.fromarray(np.uint8(a[:,:,3]>70)*255).copy()
   if group=='boot':mask=mask.filter(ImageFilter.MinFilter(5))
   yy,xx=np.where(np.array(mask)>0)
   targetx=(i%6+.5)*im.width/6;targety=cell.height*.27
   pick=np.argmin((xx-targetx)**2+(yy-targety)**2)
   ImageDraw.floodfill(mask,(int(xx[pick]),int(yy[pick])),128)
   keep=Image.fromarray(np.uint8(np.array(mask)==128)*255).filter(ImageFilter.MaxFilter(9 if group=='boot' else 5))
   a[:,:,3]=np.minimum(a[:,:,3],np.array(keep));cell=Image.fromarray(a)
  # Determine meaningful painted bounds; ignore transparent RGB and pale detached specks.
  lum=(a[:,:,:3].astype(float)*[.2126,.7152,.0722]).sum(axis=2)/255
  meaningful=(a[:,:,3]>35)&(lum<.90)
  yy,xx=np.where(meaningful)
  if len(xx)==0:raise ValueError(group+' empty')
  x0,y0,x1,y1=int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)
  # Keep full generated alpha inside each sprite cell to preserve pale cloth and all detail.
  alpha=cell.getchannel('A');bb=alpha.point(lambda p:255 if p>20 else 0).getbbox()
  if bb:x0=min(x0,bb[0]);y0=min(y0,bb[1]);x1=max(x1,bb[2]);y1=max(y1,bb[3])
  crop=cell.crop((x0,y0,x1,y1));filename=f'{group}-{i:02}.png';crop.save(frames/filename)
  hh=y1-y0;ww=x1-x0
  # Upper torso ink centroid keeps the head/torso from drifting when legs extend.
  ay0=y0+int(hh*.13);ay1=y0+int(hh*.43)
  weights=(1-lum[ay0:ay1])*a[ay0:ay1,:,3]/255
  col=weights.sum(axis=0);root=float((col*np.arange(cell.width)).sum()/max(1,col.sum()))-x0
  if not actor:root=ww*.5
  arr.append(dict(path='assets/v3/frames/'+filename,w=ww,h=hh,root=root,bottom=hh,top=0,box=list(map(round,box)),crop=[x0,y0,x1,y1],scalePolicy='group-fixed-uniform'))
 nominal=statistics.median([f['h'] for f in arr])
 if group=='boarding':nominal=statistics.median([f['h'] for f in arr[:8]])
 lib[group]=dict(frames=arr,nominal=nominal,actor=actor,topAnchor=top)
for item in inputs:
 src=Path(item['source']);target=originals/(item['id']+'.png');shutil.copy2(src,target)
 im=Image.open(target);W,H=im.size
 metadata.append(dict(id=item['id'],original='assets/v3/originals/'+target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),size=[W,H],selected=item['selected'],prompt=item['prompt']))
 if not item['selected']:continue
 g=item['id'];C=item['cols'];N=item['rows']
 boxes=gutter_boxes(im,C,N)
 if g=='ship':
  for name,box in [('ship-intact',(0,0,840,515)),('ship-hull',(840,300,W,515)),('mast',(210,515,700,H)),('mast-broken',(1000,515,1400,H))]:extract(name,im,[box])
 elif g=='boat':
  for name,box in [('boat',(0,0,1030,390)),('oar',(0,665,1000,820)),('flag',(1040,385,W,H))]:extract(name,im,[box])
 elif g=='studyProps':
  for name,box in [('instrument',(0,0,W*.52,H*.47)),('stone',(W*.55,0,W,H*.455)),('book',(0,H*.49,W*.57,H*.94)),('sailor',(W*.60,H*.465,W,H))]:extract(name,im,[box])
 elif g=='env':
  # Generated columns include gutters; crop the excessive top blank area to recompose vertically.
  for i,name in enumerate(['coast','desert','temple']):
   box=(i*W/3+5,H*.26,(i+1)*W/3-5,H)
   cell=im.crop(tuple(map(round,box)));filename=name+'.png';cell.save(frames/filename)
   lib[name]=dict(frames=[dict(path='assets/v3/frames/'+filename,w=cell.width,h=cell.height,root=cell.width*.5,bottom=cell.height)],nominal=cell.height,environment=True)
 elif g=='salvo':
  boxes=[(0,0,350,H/2),(350,0,747,H/2),(747,0,1130,H/2),(1130,0,W,H/2),(0,H/2,418,H),(418,H/2,805,H),(805,H/2,1180,H),(1180,H/2,W,H)]
  extract(g,im,boxes,True)
 else:extract(g,im,boxes,g not in ['hands','boot'],g=='boot')
(dest/'library.json').write_text(json.dumps(lib,ensure_ascii=False,indent=2),encoding='utf8')
(dest/'provenance.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:dict(frames=len(v['frames']),nominal=round(v['nominal']),size=[[f['w'],f['h']] for f in v['frames']]) for k,v in lib.items()},ensure_ascii=False))
qa=R/'out/crop-check';qa.mkdir(parents=True,exist_ok=True)
for name in ['generalWalk','boot','surveyor','boarding','walk2','salvo','hands','horse']:
 group=lib[name];sheet=Image.new('RGB',(1200,660),'#efefeb');draw=ImageDraw.Draw(sheet)
 scale=min(270/group['nominal'],170/max(f['w'] for f in group['frames']))
 for i,f in enumerate(group['frames']):
  x=200*(i%6)+100;y=330*(i//6)+300
  pic=Image.open(R/f['path']);pic=pic.resize((round(f['w']*scale),round(f['h']*scale)),Image.Resampling.LANCZOS)
  sheet.paste(pic,(round(x-f['root']*scale),y-pic.height),pic)
  draw.line((x-90,y,x+90,y),fill='#b5b5b0');draw.text((x-88,y+6),f"{i:02} {f['w']}x{f['h']}",fill='black')
 sheet.save(qa/(name+'.jpg'),quality=94)
