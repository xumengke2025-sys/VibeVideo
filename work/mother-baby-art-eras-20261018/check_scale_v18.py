from pathlib import Path
import json,sys
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'.tools/python-libs'));import cv2
cv2.setNumThreads(2);D=R/'assets/motion-v18';Q=R/'qa/v18';m=json.loads((D/'manifest.json').read_text());records=[]
yy,xx=np.mgrid[:560,:700]
for r in m['scenes']+m['bridges']:
    atlas=np.asarray(Image.open(D/r['file']).convert('RGBA'));measured=[]
    for f in range(r['frames']):
        x=f%6*700;y=f//6*560;a=atlas[y:y+560,x:x+700];rgb=a[:,:,:3].astype(float)
        dark=(a[:,:,3]>160)&(rgb.mean(axis=2)<150)&(xx>335)&(xx<640)&(yy>50)&(yy<345)
        n,lab,stats,_=cv2.connectedComponentsWithStats(np.uint8(dark),8);cs=[stats[k] for k in range(1,n) if stats[k,4]>100];top=min(int(c[1]) for c in cs)
        measured.append(520-top)
    records.append({'file':r['file'],'min_height':min(measured),'max_height':max(measured),'largest_frame_change':max(abs(a-b) for a,b in zip(measured,measured[1:])),'heights':measured})
result={'measurement':'Dark crown component to fixed seat baseline in actual baked frames; styling and internal infant proportions require visual inspection','atlases':records,'global_min':min(r['min_height'] for r in records),'global_max':max(r['max_height'] for r in records),'max_single_frame_change':max(r['largest_frame_change'] for r in records)}
(Q/'scale-check.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='atlases'}))
for page in range(4):
    board=Image.new('RGB',(1400,5*285),'#37304b');draw=ImageDraw.Draw(board)
    for row,i in enumerate(range(page*5,page*5+5)):
        r=m['scenes'][i];atlas=Image.open(D/r['file'])
        for col,f in enumerate([0,12,24,36,47]):
            a=atlas.crop((f%6*700,f//6*560,f%6*700+700,f//6*560+560));bg=Image.new('RGBA',a.size,'#9a427a');bg.alpha_composite(a);bg=bg.resize((280,224));x=col*280;y=row*285;board.paste(bg.convert('RGB'),(x,y+25));draw.text((x+4,y+4),f'era {i} F{f}',fill='white')
    board.save(Q/f'scale-board-{page}.jpg')
