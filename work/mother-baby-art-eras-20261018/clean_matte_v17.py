"""Remove tiny disconnected matte components that touch a cel border.

This corrects exterior-matte extraction noise; no character contour is moved.
"""
from pathlib import Path
import sys,json,hashlib,shutil
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'.tools/python-libs'))
import cv2
cv2.setNumThreads(2)

def clean_border(frame):
    frame=frame.copy();a=frame[:,:,3]
    n,lab,stats,_=cv2.connectedComponentsWithStats(np.uint8(a>127),8)
    ids=np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]]));ids=ids[ids>0]
    for k in ids:
        if stats[k,cv2.CC_STAT_AREA]>128:
            raise ValueError('Substantial drawing reaches border; manual repair required')
    if len(ids):
        mask=np.uint8(np.isin(lab,ids));mask=cv2.dilate(mask,np.ones((3,3),np.uint8))>0
        frame[mask]=0
    return frame

if __name__=='__main__':
    D=R/'assets/motion-v17';m=json.loads((D/'manifest.json').read_text());report=[]
    backup=R/'qa/v17/matte-backup';backup.mkdir(exist_ok=True)
    for r in m['scenes']+m['bridges']:
        p=D/r['file'];im=np.array(Image.open(p).convert('RGBA'));changed=0
        for f in range(r['frames']):
            x=f%r['columns']*r['width'];y=f//r['columns']*r['height'];cell=im[y:y+r['height'],x:x+r['width']]
            cleaned=clean_border(cell)
            if not np.array_equal(cell,cleaned):im[y:y+r['height'],x:x+r['width']]=cleaned;changed+=1
        if changed:
            if not (backup/p.name).exists():shutil.copy2(p,backup/p.name)
            Image.fromarray(im).save(p,compress_level=3)
        r['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
        report.append({'file':p.name,'changed_cels':changed})
    (D/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8')
    (R/'qa/v17/matte-cleanup.json').write_text(json.dumps({'method':'Only disconnected border components <=128 pixels and their 1-pixel matte fringe removed; original atlases backed up','atlases':report},indent=2),encoding='utf8')
    print(json.dumps({'changed_atlases':sum(r['changed_cels']>0 for r in report),'changed_cels':sum(r['changed_cels'] for r in report)}))
