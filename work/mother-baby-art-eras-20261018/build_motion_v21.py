"""Re-time existing native animation cels without rounding-step jitter.

Optical flow interpolates sub-cel samples in premultiplied RGBA. A locally
transported clear drawing repairs transparent hand/prop interiors only; faces,
the infant core, feet, and the independent stationary support are protected.
No global scaling, limb rotation, or added character layers are used.
"""
from pathlib import Path
import sys,json,hashlib,argparse,gc
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'.tools/python-libs'))
import cv2
cv2.setNumThreads(2)
S=R/'assets/motion-v20';D=R/'assets/motion-v21';Q=R/'qa/v21'
D.mkdir(exist_ok=True);Q.mkdir(exist_ok=True)
M=json.loads((S/'manifest.json').read_text())
Y,X=np.indices((560,700),dtype=np.float32)
FLOW=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM);FLOW.setFinestScale(0)
def smooth(x):
    x=np.clip(x,0,1);return x*x*(3-2*x)
def premul(a):
    b=a.astype(np.float32)/255;b[:,:,:3]*=b[:,:,3:4];return b
def straight(a):
    a=np.clip(a,0,1);a[:,:,:3]/=np.maximum(a[:,:,3:4],1/255)
    o=np.uint8(np.clip(a*255+.5,0,255));o[o[:,:,3]==0,:3]=0;return o
def gray(a):
    b=premul(a);return cv2.cvtColor(np.uint8((b[:,:,:3]+(1-b[:,:,3:4])*.5)*255),cv2.COLOR_RGB2GRAY)
def load(r):
    with Image.open(S/r['file']) as im:atlas=np.array(im.convert('RGBA'))
    return [atlas[f//6*560:f//6*560+560,f%6*700:f%6*700+700].copy() for f in range(r['frames'])]
def flow(a,b):return FLOW.calc(gray(a),gray(b),None)
def warp(a,f,t):
    # Integrate the inverse map; fixed-point iteration handles nonuniform flow.
    sx=X.copy();sy=Y.copy()
    for _ in range(5):
        f0=cv2.remap(f,sx,sy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
        sx=X-t*f0[:,:,0];sy=Y-t*f0[:,:,1]
    return cv2.remap(premul(a),sx,sy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
def interpolate(a,b,t):
    if t<1e-5:return a.copy()
    if t>1-1e-5:return b.copy()
    fa=flow(a,b);fb=flow(b,a)
    return straight(warp(a,fa,t)*(1-t)+warp(b,fb,1-t)*t)
def action_mask():
    m=smooth((X-175)/20)*smooth((635-X)/20)*smooth((Y-265)/20)*smooth((480-Y)/20)
    # Full infant head and mother's face stay exactly on their existing track.
    baby=((X-277)/83)**2+((Y-350)/76)**2
    mother=((X-453)/104)**2+((Y-211)/101)**2
    m*=smooth((baby-1)/.25)*smooth((mother-1)/.2)
    m*=1-smooth((Y-429)/20)*smooth((370-X)/20)
    return m.astype(np.float32)
MASK=action_mask()
def repair(a,refs):
    # A clear nearby cel supplies pigment only where the original hand/prop
    # is translucent. It is transported INTO this pose, never drawn separately.
    alpha=a[:,:,3].astype(np.float32)/255;best=None;bestscore=None
    for ref in refs:
        f=flow(a,ref)
        p=cv2.remap(premul(ref),X+f[:,:,0],Y+f[:,:,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
        score=p[:,:,3]
        if best is None:best=p;bestscore=score.copy()
        else:
            take=score>bestscore;best[take]=p[take];bestscore=np.maximum(bestscore,score)
    # Keep the source antialias contour; repair semiopaque interiors only if a
    # nearby opaque drawing supports their location. Thin low-alpha ghosts fade.
    inner=cv2.erode(np.uint8(alpha>.16),np.ones((3,3),np.uint8)).astype(np.float32)
    weight=MASK*inner*smooth((bestscore-.78)/.17)*(1-smooth((alpha-.88)/.10))*smooth((alpha-.16)/.20)
    src=premul(a);candidate=best.copy()
    result=src*(1-weight[:,:,None])+candidate*weight[:,:,None]
    out=straight(result)
    # Isolated 1-15px debris is not a limb, bottle, cup, or effect star.
    n,lab,stats,_=cv2.connectedComponentsWithStats(np.uint8(out[:,:,3]>12),8)
    for k in range(1,n):
        if stats[k,cv2.CC_STAT_AREA]<=15:
            out[lab==k]=0
    return out,int(np.count_nonzero(weight>.05))
def save(r,frames):
    rec=dict(r);rec.update(frames=len(frames),rows=(len(frames)+5)//6)
    atlas=Image.new('RGBA',(4200,rec['rows']*560))
    for f,a in enumerate(frames):atlas.paste(Image.fromarray(a),(f%6*700,f//6*560))
    atlas.save(D/r['file'],compress_level=3);rec['sha256']=hashlib.sha256((D/r['file']).read_bytes()).hexdigest();return rec
def board(name,old,new):
    ids=np.linspace(0,len(new)-1,8).round().astype(int)
    im=Image.new('RGB',(1400,1200),'#b9afb0');d=ImageDraw.Draw(im)
    for j,f in enumerate(ids):
        for row,seq in enumerate([old,new]):
            k=round(f*(len(seq)-1)/(len(new)-1));a=Image.new('RGBA',(700,560),'#b9afb0');a.alpha_composite(Image.fromarray(seq[k]));x=j%4*350;y=j//4*600+row*300;im.paste(a.convert('RGB').resize((350,280)),(x,y+20));d.text((x+4,y+3),('v20' if row==0 else 'v21')+f' {name} F{k}',fill='black')
    im.save(Q/(name+'-comparison.jpg'),quality=94)
def process(r,isbridge=False):
    frames=load(r);original=frames
    era=r.get('era',r.get('to'));label=r['file'][:-4]
    # References coincide with clear drawing beats, not arbitrary next/prev cels.
    keycount=(10 if era==19 else 12) if not isbridge else (10 if era==19 else 6)
    keys=np.linspace(0,len(frames)-1,keycount).round().astype(int)
    repaired=[];pixels=0
    for f,a in enumerate(frames):
        if f in (0,len(frames)-1) or isbridge:repaired.append(a.copy());continue
        near=sorted(keys,key=lambda k:abs(k-f))[:2]
        out,n=repair(a,[frames[k] for k in near]);repaired.append(out);pixels+=n
    if isbridge:count=len(repaired)
    else:
        start=0 if era==0 else era*48+8
        end=959 if era==19 else (era+1)*48-(16 if era==18 else 8)
        if era==19:start=era*48+16
        count=end-start+1
    result=[]
    for f in range(count):
        q=f*(len(repaired)-1)/(count-1);a=int(q);b=min(a+1,len(repaired)-1)
        result.append(interpolate(repaired[a],repaired[b],q-a))
    assert np.array_equal(result[0],frames[0]) and np.array_equal(result[-1],frames[-1])
    record=save(r,result);record['retiming']='one baked pose per actual available output frame, sub-cel optical flow'
    if era in [0,3,12,16,18,19]:board(label,original,result)
    (Q/(label+'.json')).write_text(json.dumps({'record':record,'hand_prop_repaired_pixels':pixels,'source_frames':len(frames),'output_frames':count},indent=2))
    print(json.dumps({'file':r['file'],'poses':count,'repaired_pixels':pixels}),flush=True)
    del frames,original,repaired,result;gc.collect()
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--scenes',default='');ap.add_argument('--bridges',default='');args=ap.parse_args()
    scenes=set(map(int,filter(None,args.scenes.split(','))));bridges=set(map(int,filter(None,args.bridges.split(','))))
    for r in M['scenes']:
        if r['era'] in scenes:process(r)
    for r in M['bridges']:
        if r['to'] in bridges:process(r,True)
    records={p.stem:json.loads(p.read_text())['record'] for p in Q.glob('scene-??.json')}
    br={p.stem:json.loads(p.read_text())['record'] for p in Q.glob('bridge-??.json')}
    m=dict(M);m.update(version=21,route='Text-free video; exact-clock scene re-timing and local transported opaque hand/prop repair',scenes=[records[k] for k in sorted(records)],bridges=[br[k] for k in sorted(br)])
    (D/'manifest.json').write_text(json.dumps(m,indent=2))
