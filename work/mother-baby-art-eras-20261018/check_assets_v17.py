"""Baked-cel alpha margins and stored digest checks, not anatomy review."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent;D=R/'assets/motion-v17'
m=json.loads((D/'manifest.json').read_text());records=m['scenes']+m['bridges'];issues=[];frames=0
for r in records:
    p=D/r['file']
    if hashlib.sha256(p.read_bytes()).hexdigest()!=r['sha256']:issues.append({'file':r['file'],'reason':'digest mismatch'})
    with Image.open(p) as im:alpha=np.asarray(im.getchannel('A'))
    for f in range(r['frames']):
        x=f%r['columns']*r['width'];y=f//r['columns']*r['height']
        a=alpha[y:y+r['height'],x:x+r['width']]>127
        if not a.any():issues.append({'file':r['file'],'frame':f,'reason':'empty character cel'})
        elif a[0].any() or a[-1].any() or a[:,0].any() or a[:,-1].any():issues.append({'file':r['file'],'frame':f,'reason':'solid drawing touches crop border'})
        frames+=1
result={'atlases':len(records),'baked_cels':frames,'issues':issues,'scope':'Stored source hashes and solid alpha at complete-cel borders; not topology, contact or aesthetic validation'}
(R/'qa/v17/asset-boundary-check.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k!='scope'}))
assert not issues,result
