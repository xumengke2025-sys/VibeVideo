from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent;M=json.loads((R/'assets/motion-v20/manifest.json').read_text());rows=[];issues=[]
for r in M['scenes']+M['bridges']:
    a=np.array(Image.open(R/'assets/motion-v19'/r['file']).convert('RGBA'));b=np.array(Image.open(R/'assets/motion-v20'/r['file']).convert('RGBA'));upper=0;rgb=0;edge=0
    for f in range(r['frames']):
        x=f%6*700;y=f//6*560;aa=a[y:y+560,x:x+700];bb=b[y:y+560,x:x+700]
        upper+=np.count_nonzero(aa[:405,:,3]!=bb[:405,:,3]);rgb+=np.count_nonzero(np.any(aa[:,:,:3]!=bb[:,:,:3],axis=2)&(bb[:,:,3]>0))
        edge+=np.count_nonzero(bb[[0,-1],:,3]>128)+np.count_nonzero(bb[:,[0,-1],3]>128)
    h=hashlib.sha256((R/'assets/motion-v20'/r['file']).read_bytes()).hexdigest()
    if h!=r['sha256'] or upper or rgb or edge:issues.append(r['file'])
    rows.append({'file':r['file'],'frames':r['frames'],'upper_actor_alpha_changed':int(upper),'retained_rgb_changed':int(rgb),'solid_border_pixels':int(edge),'hash_matches':h==r['sha256']})
result={'version':20,'cels':sum(r['frames'] for r in rows),'rows':rows,'issues':issues,'meaning':'No actor coordinate resampling or scale changes. v19 RGB retained exactly; alpha edits limited to support neighbourhood below y=405. Cushion uses one constant runtime rectangle for all eras, independent of actor frames.'}
(R/'qa/v20/fixed-layer-check.json').write_text(json.dumps(result,indent=2));print(json.dumps({'cels':result['cels'],'issues':issues}));assert not issues
