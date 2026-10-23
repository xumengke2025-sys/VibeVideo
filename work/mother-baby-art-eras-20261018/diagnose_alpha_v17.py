from pathlib import Path
import sys,json
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'.tools/python-libs'))
import cv2
cv2.setNumThreads(2)
m=json.loads((R/'assets/motion-v17/manifest.json').read_text());bad=[]
for r in m['scenes']+m['bridges']:
    with Image.open(R/'assets/motion-v17'/r['file']) as im:a=np.array(im.getchannel('A'))
    for f in range(r['frames']):
        x=f%r['columns']*r['width'];y=f//r['columns']*r['height'];cell=a[y:y+r['height'],x:x+r['width']]
        if not ((cell[0]>127).any() or (cell[-1]>127).any() or (cell[:,0]>127).any() or (cell[:,-1]>127).any()):continue
        n,lab,stats,_=cv2.connectedComponentsWithStats(np.uint8(cell>127),8)
        ids=np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]]));ids=ids[ids>0]
        bad.append({'file':r['file'],'frame':f,'border_components':[stats[k].tolist() for k in ids]})
(R/'qa/v17/alpha-diagnosis.json').write_text(json.dumps(bad,indent=2))
areas=[s[4] for b in bad for s in b['border_components']]
print(json.dumps({'affected_cels':len(bad),'border_components':len(areas),'max_area':max(areas,default=0),'examples':bad[:3]}))
