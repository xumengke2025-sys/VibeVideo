"""Whole-pair scale registration and black/white reconstruction of true alpha."""
from pathlib import Path
import json,hashlib,subprocess,os,argparse
import numpy as np
from PIL import Image
import build_continuity_v17 as b
R=Path(__file__).resolve().parent;Q=R/'qa/v18';D=R/'assets/motion-v18'
Q.mkdir(exist_ok=True);D.mkdir(exist_ok=True)
TMP=b.TMP.parent/'mother-baby-v18-rife';TMP.mkdir(exist_ok=True)
b.Q=Q

def normalize(keys,label):
    # Use the crown-to-seat distance. Face skin width changes when looking down
    # or when hands touch a cheek and is not a reliable zoom measurement.
    out=[];records=[]
    for a in keys:
        im=b.straight(a);rgb=im[:,:,:3].astype(float);yy,xx=np.mgrid[:560,:700]
        dark=(im[:,:,3]>160)&(rgb.mean(axis=2)<150)&(xx>335)&(xx<640)&(yy>50)&(yy<345)
        n,lab,stats,_=b.cv2.connectedComponentsWithStats(np.uint8(dark),8)
        components=[stats[k] for k in range(1,n) if stats[k,4]>100]
        crown=min(int(c[1]) for c in components)
        box=b.bounds(a);bottom=box[3];s=390/(bottom-crown)
        mat=np.float32([[s,0,475*(1-s)],[0,s,520-s*bottom]])
        out.append(b.cv2.warpAffine(a.astype(np.float32),mat,b.SIZE,flags=b.cv2.INTER_CUBIC,borderMode=b.cv2.BORDER_CONSTANT).astype(np.float16))
        records.append({'crown':crown,'source_seated_height':float(bottom-crown),'scale':float(s),'source_bottom':float(bottom),'target_bottom':520,'target_seated_height':390})
    (Q/f'{label}-registration.json').write_text(json.dumps(records,indent=2))
    return out

def scene_keys(i):
    path=TMP/f'normalized-height-{i:02d}.npy'
    if path.exists():return list(np.load(path))
    keys=b.modern_cels() if i==19 else b.stabilize(b.cels(b.EVIDENCE[i]))[0]
    ids=list(range(8)) if i==19 else [p[0] for p in b.CURATED.get(i,[[k,4] for k in range(12)])]
    keys=normalize([keys[k] for k in ids],f'scene-{i:02d}')
    np.save(path,np.array(keys));return keys

def interpolate(keys,count,label):
    requested=round((count-1)*len(keys)/(len(keys)-1));results=[]
    for matte in [0,1]:
        root=TMP/label/str(matte);inp=root/'in';out=root/'out';inp.mkdir(parents=True,exist_ok=True);out.mkdir(exist_ok=True)
        for n,a in enumerate(keys):
            a=a.astype(np.float32);rgb=np.uint8(np.clip((a[:,:,:3]+matte*(1-a[:,:,3:4]))*255+.5,0,255));Image.fromarray(rgb).save(inp/f'{n:08d}.png')
        p=subprocess.run([str(b.RUNTIME/'rife-ncnn-vulkan.exe'),'-i',str(inp),'-o',str(out),'-m','rife-v4.6','-n',str(requested),'-g',os.environ.get('RIFE_GPU','1'),'-j','1:1:1','-f','%08d.png'],cwd=b.RUNTIME,capture_output=True,timeout=180,creationflags=subprocess.CREATE_NO_WINDOW)
        (Q/f'{label}-matte-{matte}.log').write_bytes(p.stdout+p.stderr)
        if p.returncode:raise RuntimeError(label)
        files=sorted(out.glob('*.png'));assert len(files)==requested
        end=requested*(len(keys)-1)/len(keys)
        results.append([np.asarray(Image.open(files[min(requested-1,round(k*end/(count-1)))]).convert('RGB'),dtype=np.float32)/255 for k in range(count)])
    frames=[]
    for black,white in zip(*results):
        alpha=np.clip(1-np.median(white-black,axis=2),0,1)
        alpha[alpha<.04]=0
        rgb=np.clip(black/np.maximum(alpha[:,:,None],1/255),0,1)
        frames.append(np.uint8(np.clip(np.dstack([rgb,alpha])*255+.5,0,255)))
    frames[0]=b.straight(keys[0]);frames[-1]=b.straight(keys[-1])
    return frames

def save(frames,file):
    cols=6;rows=(len(frames)+5)//6;atlas=Image.new('RGBA',(700*cols,560*rows))
    for k,a in enumerate(frames):atlas.paste(Image.fromarray(a),(k%cols*700,k//cols*560))
    p=D/file;atlas.save(p,compress_level=3)
    return {'file':file,'x':180,'y':980,'width':700,'height':560,'columns':cols,'rows':rows,'frames':len(frames),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def scene(i):
    keys=scene_keys(i);frames=interpolate(keys,48,f'scene-{i:02d}');r=save(frames,f'scene-{i:02d}.png');r.update(era=i,slug=b.EVIDENCE[i]['slug'])
    (Q/f'scene-{i:02d}.json').write_text(json.dumps(r,indent=2));print(f'scene {i} complete',flush=True)

def bridge(i):
    old=b.generated(i);keys=normalize(old[1:-1],f'bridge-{i:02d}')
    keys=[scene_keys(i-1)[-1]]+keys+[scene_keys(i)[0]]
    count=25 if i==19 else 17;frames=interpolate(keys,count,f'bridge-{i:02d}');r=save(frames,f'bridge-{i:02d}.png');r.update(to=i,**{'from':i-1},cut_seconds=i*2,half_frames=(count-1)//2,generated_poses=len(keys)-2)
    (Q/f'bridge-{i:02d}.json').write_text(json.dumps(r,indent=2));b.contact(frames,f'bridge-{i:02d}');print(f'bridge {i} complete',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--scenes',default='');ap.add_argument('--bridges',default='');args=ap.parse_args()
    for i in map(int,filter(None,args.scenes.split(','))):scene(i)
    for i in map(int,filter(None,args.bridges.split(','))):bridge(i)
    m={'version':18,'fps':24,'duration':40,'frames':960,'route':'Whole-pair crown-to-seat height registration, anchored seat baseline, dual-matte RGBA reconstruction including enclosed gaps','scenes':[json.loads(p.read_text()) for p in sorted(Q.glob('scene-??.json'))],'bridges':[json.loads(p.read_text()) for p in sorted(Q.glob('bridge-??.json'))]}
    (D/'manifest.json').write_text(json.dumps(m,indent=2))
