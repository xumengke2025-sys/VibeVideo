"""Remove disconnected interpolation debris touching the empty atlas-cel edge."""
import build_motion_v21 as a
import numpy as np,json,hashlib
from PIL import Image
M=json.loads((a.D/'manifest.json').read_text());rows=[]
for r in M['scenes']+M['bridges']:
    atlas=np.array(Image.open(a.D/r['file']).convert('RGBA'));removed=0
    for f in range(r['frames']):
        im=atlas[f//6*560:f//6*560+560,f%6*700:f%6*700+700]
        edge=np.zeros((560,700),bool);edge[:2]=True;edge[-2:]=True;edge[:,:2]=True;edge[:,-2:]=True
        if not np.any(im[:,:,3][edge]>0):continue
        n,lab,stats,_=a.cv2.connectedComponentsWithStats(np.uint8(im[:,:,3]>6),8)
        hits=set(np.unique(lab[edge]));hits.discard(0)
        for k in hits:
            assert stats[k,a.cv2.CC_STAT_AREA]<=256,(r['file'],f,stats[k].tolist())
            pix=lab==k;removed+=int(pix.sum());im[pix]=0
        removed+=int(np.count_nonzero(im[:,:,3][edge]));im[edge]=0
    if removed:
        Image.fromarray(atlas).save(a.D/r['file'],compress_level=3);r['sha256']=hashlib.sha256((a.D/r['file']).read_bytes()).hexdigest()
        p=a.Q/(r['file'][:-4]+'.json');d=json.loads(p.read_text());d['record']=r;p.write_text(json.dumps(d,indent=2))
    rows.append({'file':r['file'],'cleared_disconnected_edge_pixels':removed})
(a.D/'manifest.json').write_text(json.dumps(M,indent=2));(a.Q/'matte-clean.json').write_text(json.dumps(rows,indent=2));print(json.dumps({'changed_assets':sum(r['cleared_disconnected_edge_pixels']>0 for r in rows),'cleared_edge_pixels':sum(r['cleared_disconnected_edge_pixels'] for r in rows)}))
