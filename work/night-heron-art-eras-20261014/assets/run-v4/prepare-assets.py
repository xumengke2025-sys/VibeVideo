"""Non-destructive atlas extraction; retain full square coordinates for animation."""
from PIL import Image,ImageFilter,ImageDraw
from pathlib import Path
import json,hashlib
import numpy as np
from collections import deque
root=Path(__file__).resolve().parent
out=[]
for p in sorted(root.glob('era-*-atlas.png')):
    era=int(p.name.split('-')[1]); im=Image.open(p).convert('RGBA'); w,h=im.size
    if abs(w-h)>4: raise ValueError((p.name,im.size))
    folder=root/f'era-{era:02d}';folder.mkdir(exist_ok=True)
    items=[]
    # Label connected silhouettes across the entire last row. This retains long
    # otter tails crossing a nominal cell border without copying a neighbour.
    y0=round(h*.715); alpha=np.asarray(im.getchannel('A'))[y0:,:]
    solid=alpha>55; seen=np.zeros(solid.shape,dtype=np.uint8); comps=[]
    hh,ww=solid.shape
    for yy,xx in zip(*np.where(solid)):
        if seen[yy,xx]:continue
        todo=deque([(int(xx),int(yy))]);seen[yy,xx]=1;coords=[]
        while todo:
            px,py=todo.popleft();coords.append((px,py))
            for nx,ny in ((px-1,py),(px+1,py),(px,py-1),(px,py+1)):
                if 0<=nx<ww and 0<=ny<hh and solid[ny,nx] and not seen[ny,nx]:
                    seen[ny,nx]=1;todo.append((nx,ny))
        if len(coords)>800:
            ar=np.array(coords);comps.append((len(coords),ar))
    selected=[]
    for cx in [.125,.375,.63,.875]:
        candidates=[v for v in comps if abs(v[1][:,0].mean()/w-cx)<.125]
        if not candidates:raise ValueError(('No last-row component',era,cx))
        _,ar=max(candidates,key=lambda v:v[0]); selected.append(ar)
    # Bird drawings stay in their authored coordinates; remove only disconnected
    # crowns/reed fragments intruding from adjacent atlas cells.
    def clean_bird(cell):
        aa=np.asarray(cell.getchannel('A'));solid=aa>55;seen=np.zeros(solid.shape,np.uint8);groups=[]
        for yy,xx in zip(*np.where(solid)):
            if seen[yy,xx]:continue
            todo=deque([(int(xx),int(yy))]);seen[yy,xx]=1;pts=[]
            while todo:
                px,py=todo.popleft();pts.append((px,py))
                for nx,ny in ((px-1,py),(px+1,py),(px,py-1),(px,py+1)):
                    if 0<=nx<384 and 0<=ny<384 and solid[ny,nx] and not seen[ny,nx]:seen[ny,nx]=1;todo.append((nx,ny))
            if len(pts)>500:groups.append(pts)
        pts=max(groups,key=len);mk=np.zeros((384,384),np.uint8);ar=np.array(pts);mk[ar[:,1],ar[:,0]]=255
        mk=Image.fromarray(mk).filter(ImageFilter.MaxFilter(7));cell.putalpha(Image.fromarray(np.minimum(np.asarray(mk),aa)));return cell
    for k in range(16):
        x=k%4;y=k//4
        top=round(y*h/4)
        roi=[round(x*w/4),top,round((x+1)*w/4),round((y+1)*h/4)]
        if k>=12:
            ar=selected[k-12]; mask=np.zeros((hh,ww),np.uint8);mask[ar[:,1],ar[:,0]]=255
            # Expand 3px to retain antialiasing and adjacent detached ink grains.
            mk=Image.fromarray(mask).filter(ImageFilter.MaxFilter(7))
            layer=im.crop((0,y0,w,h));layer.putalpha(Image.fromarray(np.minimum(np.asarray(mk),alpha)))
            bounds=layer.getbbox(); roi=[bounds[0],bounds[1]+y0,bounds[2],bounds[3]+y0]
            crop=layer.crop(bounds);cell=Image.new('RGBA',(384,384))
            factor=min(352/crop.width,352/crop.height)
            crop=crop.resize((round(crop.width*factor),round(crop.height*factor)),Image.Resampling.NEAREST if era==16 else Image.Resampling.LANCZOS)
            cell.alpha_composite(crop,((384-crop.width)//2,368-crop.height))
        else:
            cell=im.crop(roi).resize((384,384),Image.Resampling.NEAREST if era==16 else Image.Resampling.LANCZOS)
            cell=clean_bird(cell)
        # Very low alpha is invisible fringe, never remove meaningful semi-transparent ink.
        a=cell.getchannel('A'); a=a.point(lambda v:0 if v<3 else v);cell.putalpha(a)
        name=(f'run-{k}' if k<8 else f'feed-{k-8}' if k<12 else ['owner-neutral','owner-down','fish','reeds'][k-12])+'.png'
        cell.save(folder/name)
        items.append({'name':name,'alphaBounds':cell.getbbox(),'cell':k,'atlasROI':roi})
    out.append({'era':era,'atlas':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':[w,h],'cells':items})
(root/'manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared',len(out),'atlases')
