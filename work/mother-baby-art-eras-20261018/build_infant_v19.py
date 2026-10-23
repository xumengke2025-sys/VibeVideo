"""Video cel registration: an independently calibrated infant, with one continuous
coordinate field through shared contact areas. No duplicated layers or cut limbs.
The adult face, upper body and the environment remain anchored.
"""
from pathlib import Path
import json,hashlib,argparse
import numpy as np
from PIL import Image,ImageDraw
from measure_infant_v19 import R,Q,head,cv2
S=R/'assets/motion-v18';D=R/'assets/motion-v19';D.mkdir(exist_ok=True)
M=json.loads((S/'manifest.json').read_text());Y,X=np.mgrid[:560,:700].astype(np.float32)
TARGET=130.
def smooth(a):
    a=np.clip(a,0,1);return a*a*(3-2*a)
def load(r):
    atlas=np.array(Image.open(S/r['file']).convert('RGBA'));return [atlas[f//6*560:f//6*560+560,f%6*700:f%6*700+700].copy() for f in range(r['frames'])]
def observe(frames,label=''):
    values=np.array([head(a)[0] for a in frames]);smoothed=values.copy()
    # A tiny centered temporal filter removes contour-quantization noise.
    for k in range(len(values)):
        smoothed[k]=np.median(values[max(0,k-2):min(len(values),k+3)],axis=0)
    # At these contact poses the mother's palm occludes the crown. The visible
    # unoccluded head arc was checked in the source cels; do not fit the palm.
    if label=='scene-12.png':
        smoothed[35:,2]=np.interp(np.arange(35,len(frames)),[35,40,45,47],[71.8,72.5,72.,72.])
    if label=='bridge-13.png':
        smoothed[:6,2]=np.interp(np.arange(6),[0,3,5],[72.,73.,73.1])
    return smoothed
def register(a,p):
    cx,cy,r=p;scale=TARGET/(2*r)
    # Rigid infant core with a smooth shared-contact band joining the fixed adult.
    core=max(350.,cx+r+8)
    # Integrate an inverse stationary flow. A fixed-point inverse was unstable
    # near the adult protection boundary and could duplicate a piece of a sleeve.
    # In the infant core each step is an exact similarity transform; protected
    # adult pixels remain fixed. Small steps preserve a continuous sampling map.
    sx=X.copy();sy=Y.copy()
    for _ in range(16):
        face_distance=np.sqrt(((sx-460)/130)**2+((sy-210)/115)**2)
        w=(1-smooth((sx-core)/(460-core)))*smooth((sy-220)/65)*smooth((face_distance-1)/.2)
        step=np.exp(-np.log(scale)*w/16)
        sx=cx+(sx-cx)*step
        sy=505.+(sy-505.)*step
    af=a.astype(np.float32)/255;af[:,:,:3]*=af[:,:,3:4]
    out=cv2.remap(af,sx.astype(np.float32),sy.astype(np.float32),cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT)
    out=np.clip(out,0,1);out[:,:,:3]/=np.maximum(out[:,:,3:4],1/255)
    return np.uint8(np.clip(out*255+.5,0,255))
def save(r,frames):
    sheet=Image.new('RGBA',(r['columns']*700,r['rows']*560))
    for i,a in enumerate(frames):sheet.paste(Image.fromarray(a),(i%6*700,i//6*560))
    p=D/r['file'];sheet.save(p,compress_level=3);o=dict(r);o['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();return o
def board(r,before,after,params):
    sheet=Image.new('RGB',(1400,510),'#402b3b');draw=ImageDraw.Draw(sheet)
    for col,f in enumerate([0,round((len(before)-1)*.25),round((len(before)-1)*.5),round((len(before)-1)*.75),len(before)-1]):
        for row,seq in enumerate([before,after]):
            im=Image.new('RGBA',(700,560),'#ab6692');im.alpha_composite(Image.fromarray(seq[f]));sheet.paste(im.convert('RGB').resize((280,224)),(col*280,row*255+28));draw.text((col*280+4,row*255+6),f'{r["file"]} F{f} '+('before' if row==0 else 'corrected'),fill='white')
    sheet.save(Q/(r['file'].replace('.png','-comparison.jpg')),quality=94)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--only',default='');args=ap.parse_args();only=set(map(int,filter(None,args.only.split(','))))
    params={};observations=[];out={'version':19,'fps':24,'duration':40,'frames':960,'route':'Infant skull-arc registration independent of adult crown-height; fixed adult, smooth contact field; inherited dual-matte alpha','scenes':[],'bridges':[]}
    for r in M['scenes']:
        frames=load(r);p=observe(frames,r['file']);params[r['era']]=p
        if only and r['era'] not in only:continue
        result=[register(a,q) for a,q in zip(frames,p)];out['scenes'].append(save(r,result));board(r,frames,result,p)
        observations.append({'file':r['file'],'parameters':p.tolist(),'before_diameters':[float(2*head(a)[0][2]) for a in frames],'after_diameters':[float(2*head(a)[0][2]) for a in result]});print(r['file'],flush=True)
    for r in M['bridges']:
        if only and not (r['from'] in only and r['to'] in only):continue
        frames=load(r);p=observe(frames,r['file'])
        # Keep identical source endpoint pixels under identical transforms.
        p[0]=params[r['from']][-1];p[-1]=params[r['to']][0]
        result=[register(a,q) for a,q in zip(frames,p)];out['bridges'].append(save(r,result));board(r,frames,result,p)
        observations.append({'file':r['file'],'parameters':p.tolist(),'before_diameters':[float(2*head(a)[0][2]) for a in frames],'after_diameters':[float(2*head(a)[0][2]) for a in result]});print(r['file'],flush=True)
    if only and (D/'manifest.json').exists():
        previous=json.loads((D/'manifest.json').read_text())
        for key in ['scenes','bridges']:
            combined={r['file']:r for r in previous[key]};combined.update({r['file']:r for r in out[key]});out[key]=[combined[k] for k in sorted(combined)]
        old={r['file']:r for r in json.loads((Q/'infant-registration.json').read_text())};old.update({r['file']:r for r in observations});observations=[old[k] for k in sorted(old)]
    (D/'manifest.json').write_text(json.dumps(out,indent=2));(Q/'infant-registration.json').write_text(json.dumps(observations,indent=2))
