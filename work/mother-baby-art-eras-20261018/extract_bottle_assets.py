from pathlib import Path
from PIL import Image,ImageFilter,ImageDraw
import numpy as np,json,hashlib
R=Path(__file__).resolve().parent;A=R/'assets/bottle-v3'
def boxes(im):
 a=np.array(im.getchannel('A'));binary=a>175;par=[];area=[];bounds=[];prev=[]
 def find(i):
  while par[i]!=i:par[i]=par[par[i]];i=par[i]
  return i
 for y,row in enumerate(binary):
  d=np.diff(np.r_[False,row,False].astype('int8'));cur=[];p=0
  for x0,x1 in zip(np.where(d==1)[0],np.where(d==-1)[0]):
   n=len(par);par.append(n);area.append(int(x1-x0));bounds.append([int(x0),y,int(x1),y+1]);cur.append((x0,x1,n))
   while p<len(prev) and prev[p][1]<x0:p+=1
   q=p
   while q<len(prev) and prev[q][0]<=x1:
    v,u=find(n),find(prev[q][2])
    if v!=u:
     par[u]=v;area[v]+=area[u];b,c=bounds[v],bounds[u];bounds[v]=[min(b[0],c[0]),min(b[1],c[1]),max(b[2],c[2]),max(b[3],c[3])]
    q+=1
  prev=cur
 return sorted([(area[i],bounds[i]) for i in range(len(par)) if par[i]==i and area[i]>1800],reverse=True)
def extract_sheet(path,count):
 im=Image.open(path).convert('RGBA');w,h=im.size;cols=2 if count==4 else 4;rows=count//cols;ordered=[None]*count;found=[]
 for col in range(cols):
  x0,x1=round(col*w/cols),round((col+1)*w/cols);part=im.crop((x0,0,x1,h));alpha=np.array(part.getchannel('A'));profile=(alpha>200).sum(axis=1);smooth=np.convolve(profile,np.ones(5)/5,mode='same');cuts=[0]
  for row in range(1,rows):
   lo,hi=round(h*row/rows-h/rows*.32),round(h*row/rows+h/rows*.32)
   cuts.append(lo+int(np.argmin(smooth[lo:hi])))
  cuts.append(h)
  for row in range(rows):
   crop=part.crop((0,cuts[row],x1-x0,cuts[row+1]));components=boxes(crop);assert components,(path,row,col)
   area,b=components[0];b=[b[0]+x0,b[1]+cuts[row],b[2]+x0,b[3]+cuts[row]]
   ordered[row*cols+col]=(area,b);found.extend(components)
 cels=[]
 for row in range(rows):
  bs=[v[1] for v in ordered[row*cols:row*cols+cols]];scale=286/max(b[3]-b[1] for b in bs)
  for b in bs:
   cut=im.crop(b);cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS)
   cel=Image.new('RGBA',(500,310));cel.alpha_composite(cut,(85,302-cut.height));cels.append(cel)
 return cels,{'path':str(path),'components':len(found),'selected_boxes':[v[1] for v in ordered]}
if __name__=='__main__':
 evidence=[]
 for start in range(0,35,5):
  path=A/f'batch-{start:02d}.png'
  if not path.exists():continue
  cels,ev=extract_sheet(path,20);evidence.append(ev)
  for row in range(5):
   i=start+row;folder=A/f'era-{i:02d}';folder.mkdir(exist_ok=True)
   for col in range(4):cels[row*4+col].save(folder/f'baby-{col}.png')
   if i in [7,8,9,14]:
    ref=Image.new('RGBA',(1000,620))
    for col in range(4):ref.alpha_composite(cels[row*4+col],((col%2)*500,(col//2)*310))
    ref.save(A/f'repair-ref-{i:02d}.png')
 for i in [7,8,9,14]:
  path=A/f'repair-{i:02d}.png'
  if not path.exists():continue
  cels,ev=extract_sheet(path,4);evidence.append(ev)
  for col,cel in enumerate(cels):cel.save(A/f'era-{i:02d}'/f'baby-{col}.png')
 (A/'extraction.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf8')
 for start in range(0,35,5):
  sheet=Image.new('RGBA',(1000,850),'#f0e7d4');d=ImageDraw.Draw(sheet)
  for row in range(5):
   i=start+row;folder=A/f'era-{i:02d}'
   for col in range(4):
    path=folder/f'baby-{col}.png'
    if path.exists():sheet.alpha_composite(Image.open(path).resize((250,155),Image.Resampling.LANCZOS),(col*250,row*170+15))
   d.text((4,row*170+1),f'ERA {i:02d}',fill='#282828')
  sheet.convert('RGB').save(A/f'contact-{start:02d}.jpg',quality=96)
 print(json.dumps([{'path':Path(x['path']).name,'components':x['components']} for x in evidence]))
