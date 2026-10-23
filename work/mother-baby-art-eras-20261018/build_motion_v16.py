"""Registered complete generated cels -> 24fps motion-compensated atlases.

No limb overlays or cyclic actor transform. Preserve the original source sheets.
OpenCV/scipy are local build dependencies only; playback uses the baked PNGs.
"""
from pathlib import Path
import sys,json,time,argparse
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'.tools/python-libs'))
import cv2
cv2.setNumThreads(2)
DEST=R/'assets/motion-v16'; QA=R/'qa/v16'; DEST.mkdir(parents=True,exist_ok=True); QA.mkdir(parents=True,exist_ok=True)
EVIDENCE=json.loads((R/'qa/v15/mechanical-check.json').read_text())['asset_registration']
EVIDENCE=sorted(EVIDENCE,key=lambda x:x['era'])
ORIGIN=(180,980); SIZE=(700,560)
CURATED={0:[[0,5],[1,4],[2,4],[3,4],[4,4],[5,5],[8,5],[9,5],[10,5],[11,7]],1:[[0,5],[1,4],[2,4],[3,4],[4,4],[5,4],[6,4],[7,4],[8,4],[10,5],[11,6]],2:[[0,5],[1,4],[2,4],[3,4],[4,4],[5,4],[6,4],[7,4],[8,4],[10,5],[11,6]],3:[[0,4],[1,4],[2,4],[3,4],[4,4],[5,4],[6,4],[7,4],[8,4],[10,5],[9,7]],5:[[0,5],[1,4],[2,4],[3,4],[4,4],[5,5],[6,5],[7,5],[10,5],[11,7]],11:[[0,5],[1,4],[2,4],[3,4],[4,4],[5,4],[6,4],[7,4],[8,4],[10,5],[11,6]],12:[[0,5],[1,4],[2,4],[3,4],[4,4],[5,4],[6,4],[7,4],[8,4],[9,5],[10,6]],18:[[0,4],[1,3],[2,4],[3,4],[4,5],[5,5],[6,5],[7,4],[8,4],[9,4],[11,6]]}

def premul(a):
    a=a.astype(np.float32)/255
    a[:,:,:3]*=a[:,:,3:4]
    return a

def straight(a):
    a=np.clip(a,0,1)
    rgb=a[:,:,:3]/np.maximum(a[:,:,3:4],1/255)
    return np.uint8(np.clip(np.dstack([rgb,a[:,:,3]])*255+.5,0,255))

def gray(a):
    # Alpha silhouette is part of the correspondence, transparent RGB is ignored.
    a=a.astype(np.float32,copy=False)
    rgb=a[:,:,:3]+(1-a[:,:,3:4])*.78
    return np.uint8(np.clip(cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)*255,0,255))

def cels(e):
    sheet=np.array(Image.open(R/'assets/sequences-v13'/f"{e['slug']}.png").convert('RGBA'))
    result=[]; gut=e['gutters']
    for k in range(12):
        row,col=divmod(k,4); x0=gut['row_x'][row][col];x1=gut['row_x'][row][col+1];y0=gut['column_y'][col][row];y1=gut['column_y'][col][row+1]
        raw=premul(sheet[y0:y1,x0:x1]);r=e['registration'][k]
        mat=np.float32([[r['scale'],0,r['x']-ORIGIN[0]],[0,r['scale'],r['y']-ORIGIN[1]]])
        result.append(cv2.warpAffine(raw,mat,SIZE,flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT).astype(np.float16))
    return result

def translation(ref,cur,rect,radius=100):
    x0,y0,x1,y1=rect
    a=gray(ref);b=gray(cur);tpl=a[y0:y1,x0:x1]
    sx=max(0,x0-radius);sy=max(0,y0-radius);ex=min(SIZE[0],x1+radius);ey=min(SIZE[1],y1+radius)
    score=cv2.matchTemplate(b[sy:ey,sx:ex],tpl,cv2.TM_CCOEFF_NORMED)
    _,v,_,(x,y)=cv2.minMaxLoc(score)
    dx,dy=sx+x-x0,sy+y-y0
    return [float(dx),float(dy),float(v)]

def stabilize(original):
    ref=original[0].astype(np.float32); shifts=[];result=[]
    yy,xx=np.mgrid[0:SIZE[1],0:SIZE[0]].astype(np.float32)
    # Match the support, shoes and stool, never the moving hand or prop.
    for k,a in enumerate(original):
        a=a.astype(np.float32)
        mom=translation(ref,a,(425,427,610,535))
        baby=translation(ref,a,(160,468,387,535))
        if k==0:mom[:2]=[0,0];baby[:2]=[0,0]
        # Use a single rigid translation for the complete pair. A horizontal
        # mother/baby displacement blend would distort a leaning face or arm.
        b=cv2.warpAffine(a,np.float32([[1,0,-mom[0]],[0,1,-mom[1]]]),SIZE,flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT)
        # Sitting supports are invariant. Feather only the lower resting area,
        # below the hands; do not crossfade two moving arms.
        side=np.clip((xx-370)/65,0,1);side=side*side*(3-2*side)
        support_y=490*(1-side)+447*side
        lock=np.clip((yy-support_y)/24,0,1);lock=lock*lock*(3-2*lock)
        b*=1-lock[:,:,None];b+=ref*lock[:,:,None]
        result.append(b.astype(np.float16));shifts.append({'cel':k,'mother':mom,'baby':baby})
    return result,shifts

def flow(a,b):
    dis=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    dis.setFinestScale(0);dis.setGradientDescentIterations(30)
    dis.setVariationalRefinementIterations(5)
    return dis.calc(gray(a),gray(b),None)

def interpolate(a,b,fw,bw,t):
    h,w=a.shape[:2];yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
    ax=xx-t*fw[:,:,0];ay=yy-t*fw[:,:,1]
    bx=xx-(1-t)*bw[:,:,0];by=yy-(1-t)*bw[:,:,1]
    for _ in range(2):
        fa=cv2.remap(fw,ax,ay,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
        fb=cv2.remap(bw,bx,by,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
        ax=xx-t*fa[:,:,0];ay=yy-t*fa[:,:,1]
        bx=xx-(1-t)*fb[:,:,0];by=yy-(1-t)*fb[:,:,1]
    wa=cv2.remap(a,ax,ay,cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT)
    wb=cv2.remap(b,bx,by,cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT)
    # Blend already compensated images, not unaligned silhouettes.
    return wa*(1-t)+wb*t

def metrics(frames):
    diff=[];previous=None
    for x in frames:
        a=gray(premul(x) if x.dtype==np.uint8 else x).astype(np.int16)
        if previous is not None:diff.append(float(np.abs(a-previous).mean()))
        previous=a
    diff=np.array(diff)
    return {'max_frame_mean_absdiff':float(diff.max()),'mean_frame_mean_absdiff':float(diff.mean()),'p95_frame_mean_absdiff':float(np.percentile(diff,95))}

def sheet(frames,dest,indices):
    pic=Image.new('RGB',(5*350,((len(indices)+4)//5)*300),'#ede4d3');d=ImageDraw.Draw(pic)
    for n,k in enumerate(indices):
        im=Image.fromarray(frames[k] if frames[k].dtype==np.uint8 else straight(frames[k]));bg=Image.new('RGBA',im.size,'#ede4d3');bg.alpha_composite(im);bg=bg.resize((350,280))
        x=n%5*350;y=n//5*300;pic.paste(bg.convert('RGB'),(x,y+20));d.text((x+4,y+3),f'F{k:02d}',fill='#302719')
    pic.save(dest)

def build(i):
    start=time.time();e=EVIDENCE[i];original=cels(e);fixed,shifts=stabilize(original)
    schedule=CURATED.get(i,[[k,4] for k in range(12)])
    ids=[p[0] for p in schedule]
    # Key poses sit at the centers of their original exposure. The beginning
    # and result stay still; the movement between poses uses a continuous clock.
    holds=np.array([p[1] for p in schedule]);times=np.cumsum(holds)-holds/2-.5
    # Deliberate hand trajectories are left in the complete source cels.
    flows={}
    for k in range(len(ids)-1):
        a,b=fixed[ids[k]],fixed[ids[k+1]]
        flows[k]=(flow(a,b),flow(b,a))
    frames=[];old=[]
    for f in range(48):
        if f<=times[0]:a=fixed[ids[0]]
        elif f>=times[-1]:a=fixed[ids[-1]]
        else:
            j=int(np.searchsorted(times,f,side='right')-1);t=float((f-times[j])/(times[j+1]-times[j]));fw,bw=flows[j]
            a=interpolate(fixed[ids[j]],fixed[ids[j+1]],fw,bw,t)
        frames.append(straight(a))
        j=min(int(np.searchsorted(np.cumsum(holds),f,side='right')),len(ids)-1);old.append(original[ids[j]])
    # Keep every pixel, use one fixed crop over all 48 frames.
    alpha=np.maximum.reduce([a[:,:,3] for a in frames]);ys,xs=np.where(alpha>4)
    x0=max(0,int(xs.min())-10);x1=min(SIZE[0],int(xs.max())+11);y0=max(0,int(ys.min())-10);y1=min(SIZE[1],int(ys.max())+11)
    cw,ch=x1-x0,y1-y0
    atlas=Image.new('RGBA',(cw*6,ch*8))
    for k,a in enumerate(frames):atlas.paste(Image.fromarray(a[y0:y1,x0:x1]),(k%6*cw,k//6*ch))
    file=f'{i:02d}-{e["slug"]}.png';atlas.save(DEST/file,compress_level=3)
    record={'era':i,'slug':e['slug'],'file':file,'width':cw,'height':ch,'x':x0+ORIGIN[0],'y':y0+ORIGIN[1],'columns':6,'frames':48,'shifts':shifts,'before':metrics(old),'after':metrics(frames),'key_times':times.tolist(),'cels':ids,'seconds':round(time.time()-start,2)}
    (QA/f'motion-{i:02d}.json').write_text(json.dumps(record,indent=2),encoding='utf8')
    if i in [0,8,12,18,19]:
        sheet(frames,QA/f'after-{i:02d}.jpg',list(range(0,48,3)))
        sheet(old,QA/f'before-{i:02d}.jpg',list(range(0,48,3)))
    print(json.dumps({'era':i,'seconds':record['seconds'],'max_before':record['before']['max_frame_mean_absdiff'],'max_after':record['after']['max_frame_mean_absdiff'],'crop':[x0,y0,cw,ch]}),flush=True)
    return record

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--eras',default=','.join(str(i) for i in range(20)));args=p.parse_args()
    for i in map(int,args.eras.split(',')):build(i)
    records=[json.loads(p.read_text()) for p in sorted(QA.glob('motion-*.json'))]
    (DEST/'manifest.json').write_text(json.dumps({'version':16,'fps':24,'duration':40,'origin':ORIGIN,'route':'complete-cel support registration and bidirectional motion-compensated inbetweens','scenes':records},ensure_ascii=False,indent=2),encoding='utf8')
