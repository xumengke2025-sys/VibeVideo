"""Complete-cel cross-era handoffs; dual-matte RIFE keeps the room independent."""
from pathlib import Path
import argparse,os,json,subprocess,time,hashlib
import numpy as np
from PIL import Image,ImageDraw
from clean_matte_v17 import clean_border
from build_motion_v16 import R,EVIDENCE,SIZE,ORIGIN,cels,stabilize,CURATED,cv2,premul,straight
Q=R/'qa/v17';D=R/'assets/motion-v17';Q.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True)
TMP=Path(os.environ.get('LOCALAPPDATA','C:/Users/67236/AppData/Local'))/'Temp/mother-baby-v17-rife'
RUNTIME=R/'.tools/rife/runtime'

def run(frames,count,label):
    # Two neutral mattes recover transparent complete drawings without involving
    # the room. They also preserve exact endpoint alpha from the source cels.
    results=[]
    for bg in [0,1]:
        folder=TMP/label/str(bg);inp=folder/'in';out=folder/'out';inp.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
        for n,a in enumerate(frames):
            a=a.astype(np.float32);rgb=np.uint8(np.clip((a[:,:,:3]+bg*(1-a[:,:,3:4]))*255+.5,0,255))
            Image.fromarray(rgb).save(inp/f'{n:08d}.png')
        proc=subprocess.run([str(RUNTIME/'rife-ncnn-vulkan.exe'),'-i',str(inp),'-o',str(out),'-m','rife-v4.6','-n',str(count),'-g',os.environ.get('RIFE_GPU','1'),'-j','1:1:1','-f','%08d.png'],cwd=RUNTIME,capture_output=True,timeout=180,creationflags=subprocess.CREATE_NO_WINDOW)
        (Q/f'{label}-matte-{bg}.log').write_bytes(proc.stdout+proc.stderr)
        if proc.returncode:raise RuntimeError(f'RIFE {label}/{bg}: {proc.returncode}')
        files=sorted(out.glob('*.png'))
        if len(files)!=count:raise RuntimeError(f'frame count {label}: {len(files)} != {count}')
        results.append([np.asarray(Image.open(p).convert('RGB'),dtype=np.float32)/255 for p in files])
    rgba=[]
    for k,(black,white) in enumerate(zip(*results)):
        a=np.clip(1-np.median(white-black,axis=2),0,1);rgb=np.clip(black/np.maximum(a[:,:,None],.0039),0,1)
        a[a<.025]=0
        rgba.append(np.uint8(np.clip(np.dstack([rgb,a])*255+.5,0,255)))
    for k,src in [(0,frames[0]),(count-1,frames[-1])]:
        alpha=np.clip(src[:,:,3:4].astype(np.float32),0,1);rgba[k]=np.uint8(np.clip(np.dstack([src[:,:,:3]/np.maximum(alpha,1/255),alpha])*255+.5,0,255))
    return rgba

def base_endpoint(i,last=False):
    cache=TMP/f'fixed-{i:02d}.npy'
    if cache.exists():fixed=np.load(cache)
    else:
        fixed,_=stabilize(cels(EVIDENCE[i]));TMP.mkdir(parents=True,exist_ok=True);np.save(cache,np.array(fixed))
    ids=[p[0] for p in CURATED.get(i,[[k,4] for k in range(12)])]
    return fixed[ids[-1] if last else ids[0]]

def endpoint(i,last=False):
    if i==19:return modern_cels()[-1 if last else 0]
    return base_endpoint(i,last)

def bounds(a):
    ys,xs=np.where(a[:,:,3]>.35);return np.array([xs.min(),ys.min(),xs.max()+1,ys.max()+1],dtype=float)

def split_gutters(proj,n):
    splits=[0];length=len(proj)
    for k in range(1,n):
        center=length*k/n;radius=length/n*.19;lo=round(center-radius);hi=round(center+radius)
        vals=proj[lo:hi];candidates=np.where(vals==vals.min())[0]+lo;splits.append(int(candidates[np.argmin(np.abs(candidates-center))]))
    return splits+[length]

def isolate(raw,box):
    raw=raw.copy();n,labels,stats,_=cv2.connectedComponentsWithStats(np.uint8(raw[:,:,3]>180),8);kept=np.zeros(raw.shape[:2],np.uint8)
    for k in range(1,n):
        if stats[k,cv2.CC_STAT_AREA]>=18 and stats[k,cv2.CC_STAT_WIDTH]>3:kept[labels==k]=255
    kept=cv2.dilate(kept,np.ones((3,3),np.uint8));raw[:,:,3]=np.minimum(raw[:,:,3],kept)
    yy,xx=np.where(raw[:,:,3]>128);raw=raw[yy.min():yy.max()+1,xx.min():xx.max()+1]
    scale=(box[3]-box[1])/raw.shape[0];x=(box[0]+box[2])/2-raw.shape[1]*scale/2;y=box[3]-raw.shape[0]*scale
    return cv2.warpAffine(premul(raw),np.float32([[scale,0,x],[0,scale,y]]),SIZE,flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT).astype(np.float16)

def modern_cels():
    im=np.asarray(Image.open(R/'assets/bridges-v17/modern-action.png').convert('RGBA'));alpha=im[:,:,3]>180
    ys=split_gutters(alpha.sum(axis=1),2);box=bounds(base_endpoint(19));result=[]
    for row in range(2):
        xs=split_gutters(alpha[ys[row]:ys[row+1]].sum(axis=0),4)
        for col in range(4):result.append(isolate(im[ys[row]:ys[row+1],xs[col]:xs[col+1]],box))
    return result

def generated(i):
    if i==19:
        im=np.asarray(Image.open(R/'assets/bridges-v17/prop-recovery-v3.png').convert('RGBA'))
        a=endpoint(18,True);b=endpoint(19);ba,bb=bounds(a),bounds(b);result=[]
        alpha=im[:,:,3]>180;ys=split_gutters(alpha.sum(axis=1),2)
        for row in range(2):
            xs=split_gutters(alpha[ys[row]:ys[row+1]].sum(axis=0),4)
            for col in range(4):
                t=(row*4+col+1)/9
                result.append(isolate(im[ys[row]:ys[row+1],xs[col]:xs[col+1]],ba*(1-t)+bb*t))
        return [a]+result+[b]
    batch=(i-1)//4;row=(i-1)%4;rows=3 if batch==4 else 4
    im=np.asarray(Image.open(R/f'assets/bridges-v17/batch-{batch}.png').convert('RGBA'));h,w=im.shape[:2]
    a=endpoint(i-1,True);b=endpoint(i);ba,bb=bounds(a),bounds(b);result=[]
    alpha=im[:,:,3]>180
    ys=split_gutters(alpha.sum(axis=1),rows);xsplit=split_gutters(alpha[ys[row]:ys[row+1]].sum(axis=0),4)
    for col,t in enumerate([.10,.36,.64,.90]):
        raw=im[ys[row]:ys[row+1],xsplit[col]:xsplit[col+1]]
        result.append(isolate(raw,ba*(1-t)+bb*t))
    return [a]+result+[b]

def remove_white(image):
    # A connected exterior matte retains white clothes enclosed by ink outlines.
    rgb=image.astype(np.float32)/255;minimum=image.min(axis=2)
    white=np.uint8(minimum>249);pad=np.pad(white,1,constant_values=1)
    flood=pad.copy();cv2.floodFill(flood,None,(0,0),2);outside=flood[1:-1,1:-1]==2
    solid=np.uint8(~outside);distance=cv2.distanceTransform(solid,cv2.DIST_L2,3)
    alpha=np.ones(minimum.shape,np.float32);alpha[outside]=0
    near=cv2.dilate(np.uint8(distance>1.4),np.ones((3,3),np.uint8))==0
    edge=near & (minimum>239);alpha[edge]=np.clip((255-minimum[edge].astype(np.float32))/16,0,1)
    color=np.clip((rgb-(1-alpha[:,:,None]))/np.maximum(alpha[:,:,None],1/255),0,1)
    return np.uint8(np.clip(np.dstack([color,alpha])*255+.5,0,255))

def run_white(frames,count,label):
    folder=TMP/label/'white';inp=folder/'in';out=folder/'out';inp.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
    for n,a in enumerate(frames):
        a=a.astype(np.float32);rgb=np.uint8(np.clip((a[:,:,:3]+(1-a[:,:,3:4]))*255+.5,0,255));Image.fromarray(rgb).save(inp/f'{n:08d}.png')
    # ncnn's directory clock includes a trailing interval holding the last input.
    # Request extra outputs then resample ONLY the moving [0,N-1] interval.
    requested=round((count-1)*len(frames)/(len(frames)-1))
    proc=subprocess.run([str(RUNTIME/'rife-ncnn-vulkan.exe'),'-i',str(inp),'-o',str(out),'-m','rife-v4.6','-n',str(requested),'-g',os.environ.get('RIFE_GPU','1'),'-j','1:1:1','-f','%08d.png'],cwd=RUNTIME,capture_output=True,timeout=180,creationflags=subprocess.CREATE_NO_WINDOW)
    (Q/f'{label}-white.log').write_bytes(proc.stdout+proc.stderr)
    if proc.returncode:raise RuntimeError(f'RIFE {label}: {proc.returncode}')
    files=sorted(out.glob('*.png'))
    if len(files)!=requested:raise RuntimeError(f'frame count {label}: {len(files)} != {requested}')
    end=requested*(len(frames)-1)/len(frames)
    result=[remove_white(np.asarray(Image.open(files[min(len(files)-1,round(k*end/(count-1)))]).convert('RGB'))) for k in range(count)]
    result[0]=straight(frames[0]);result[-1]=straight(frames[-1]);return result

def saveatlas(frames,file):
    cols=6;rows=(len(frames)+cols-1)//cols;atlas=Image.new('RGBA',(SIZE[0]*cols,SIZE[1]*rows))
    for k,f in enumerate(frames):atlas.paste(Image.fromarray(clean_border(f)),(k%cols*SIZE[0],k//cols*SIZE[1]))
    atlas.save(D/file,compress_level=3)
    return {'file':file,'x':ORIGIN[0],'y':ORIGIN[1],'width':SIZE[0],'height':SIZE[1],'columns':cols,'rows':rows,'frames':len(frames),'sha256':hashlib.sha256((D/file).read_bytes()).hexdigest()}

def contact(frames,label):
    inds=list(range(len(frames)));w=350;h=300
    board=Image.new('RGB',(5*w,((len(inds)+4)//5)*h),'#eee4d3');draw=ImageDraw.Draw(board)
    for n,k in enumerate(inds):
        bg=Image.new('RGBA',SIZE,'#f1e7d4');bg.alpha_composite(Image.fromarray(frames[k]));bg.thumbnail((w,280));x=n%5*w;y=n//5*h;board.paste(bg.convert('RGB'),(x,y+20));draw.text((x+4,y+3),f'{label} F{k:02d}',fill='#342a20')
    board.save(Q/f'{label}.jpg')

def bridge(i):
    start=time.time();keys=generated(i);count=25 if i==19 else 17;frames=run_white(keys,count,f'bridge-{i:02d}-generated-'+str(count))
    record=saveatlas(frames,f'bridge-{i:02d}.png');record.update({'to':i,'from':i-1,'cut_seconds':i*2,'seconds':round(time.time()-start,2),'method':'complete-cel dual-matte RIFE; no room pixels, no limb overlays'})
    record.update(half_frames=(count-1)//2,generated_poses=len(keys)-2)
    record['method']=f'{len(keys)-2} newly generated complete connecting poses plus original endpoints; white exterior matte, no room pixels'
    (Q/f'bridge-{i:02d}.json').write_text(json.dumps(record,indent=2),encoding='utf8');contact(frames,f'bridge-{i:02d}');contact([straight(a) for a in keys],f'keys-{i:02d}');print(json.dumps({'bridge':i,'seconds':record['seconds']}),flush=True);return record

def scene(i):
    start=time.time();endpoint(i);fixed=modern_cels() if i==19 else np.load(TMP/f'fixed-{i:02d}.npy');ids=list(range(8)) if i==19 else [p[0] for p in CURATED.get(i,[[k,4] for k in range(12)])]
    frames=run_white([fixed[k] for k in ids],48,f'scene-{i:02d}')
    # Lower supports remain the original stabilized drawings throughout the
    # action; only whole-character interpolation above the resting zone moves.
    yy,xx=np.mgrid[:SIZE[1],:SIZE[0]];side=np.clip((xx-370)/65,0,1);side=side*side*(3-2*side)
    support_y=490*(1-side)+447*side;lock=np.clip((yy-support_y)/24,0,1);lock=lock*lock*(3-2*lock)
    static=straight(fixed[ids[0]])
    for k,frame in enumerate(frames):
        a=premul(frame)*(1-lock[:,:,None])+premul(static)*lock[:,:,None];frames[k]=straight(a)
    frames[0]=straight(fixed[ids[0]]);frames[-1]=straight(fixed[ids[-1]])
    record=saveatlas(frames,f'scene-{i:02d}.png');record.update({'era':i,'slug':EVIDENCE[i]['slug'],'source_cels':ids,'seconds':round(time.time()-start,2)})
    (Q/f'scene-{i:02d}.json').write_text(json.dumps(record,indent=2),encoding='utf8');print(json.dumps({'scene':i,'seconds':record['seconds']}),flush=True);return record

def manifest():
    scenes=[json.loads(p.read_text()) for p in sorted(Q.glob('scene-*.json'))]
    bridges=[json.loads(p.read_text()) for p in sorted(Q.glob('bridge-*.json'))]
    (D/'manifest.json').write_text(json.dumps({'version':17,'fps':24,'frames':960,'duration':40,'default_bridge_frames':17,'default_bridge_half_frames':8,'generated_linking_cels':sum(b.get('generated_poses',4) for b in bridges),'route':'whole generated cels plus newly generated complete connecting poses, one shared actor timeline independent of room transitions; longer physical prop recovery before final high five','scenes':scenes,'bridges':bridges},ensure_ascii=False,indent=2),encoding='utf8')

def refs():
    for batch in range(5):
        ids=list(range(batch*4+1,min(20,batch*4+5)))
        board=Image.new('RGBA',(1400,len(ids)*600),'#f1e7d4');draw=ImageDraw.Draw(board)
        for row,i in enumerate(ids):
            for col,(era,last) in enumerate([(i-1,True),(i,False)]):
                a=endpoint(era,last);alpha=np.clip(a[:,:,3:4].astype(np.float32),0,1);raw=np.uint8(np.clip(np.dstack([a[:,:,:3]/np.maximum(alpha,1/255),alpha])*255+.5,0,255))
                board.alpha_composite(Image.fromarray(raw),(col*700,row*600+40))
                draw.text((col*700+8,row*600+8),f'BOUNDARY {i}: {EVIDENCE[era]["slug"]} '+('END' if last else 'START'),fill='#342a20')
        board.convert('RGB').save(Q/f'bridge-reference-{batch}.jpg')
    print('reference boards ready',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--bridges',default='');p.add_argument('--scenes',default='');p.add_argument('--refs',action='store_true');args=p.parse_args()
    if args.refs:refs()
    else:
        if args.scenes:
            for i in map(int,args.scenes.split(',')):scene(i)
        if args.bridges:
            for i in map(int,args.bridges.split(',')):bridge(i)
        manifest()
