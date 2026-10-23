"""Composite generated handover drawings into the protected existing actor track.
Only mother's torso/arms/cup change. Original heads, infant, feet, stool stay on
the original coordinates. The pair is baked into one RGBA cel before playback.
"""
import build_motion_v21 as a
from PIL import Image,ImageDraw
import numpy as np
import json,subprocess,os
R=a.R;Q=a.Q;D=a.D
def keys():
    record=next(r for r in a.M['bridges'] if r['to']==19);old=a.load(record)
    im=np.array(Image.open(D/'handover-generated.png').convert('RGBA'));h,w=im.shape[:2]
    generated=[];out=[old[0]]
    # Stable composition transform shared by all four drawings, derived from
    # generated mother's crown/seat registration. No frame-by-frame fitting.
    for k,f in enumerate([2,4,7,9]):
        raw=im[k//2*(h//2):(k//2+1)*(h//2),k%2*(w//2):(k%2+1)*(w//2)].copy()
        raw=a.cv2.resize(raw,(700,560))
        scale=390/512;mat=np.float32([[scale,0,480-466*scale],[0,scale,130-20*scale]])
        new=a.cv2.warpAffine(a.premul(raw),mat,(700,560),flags=a.cv2.INTER_CUBIC,borderMode=a.cv2.BORDER_CONSTANT)
        # Remove generated stool before compositing; furniture stays original.
        rgb0=np.float32(raw[:,:,:3]);green=(rgb0[:,:,1]>rgb0[:,:,0]*1.06)&(rgb0[:,:,1]>rgb0[:,:,2]*1.15)
        green &= np.indices(raw.shape[:2])[0]>395
        raw[green]=0
        new=a.cv2.warpAffine(a.premul(raw),mat,(700,560),flags=a.cv2.INTER_CUBIC,borderMode=a.cv2.BORDER_CONSTANT)
        # Torso / active arms, with feathered seams on still clothing. Cup and
        # fingers form the same drawing; no independently rotated hand layers.
        mask=a.smooth((a.X-359)/10)*a.smooth((a.Y-286)/12)
        low=1-a.smooth((a.Y-393)/12)
        mask*=low
        # Retain original hair around the neck, including overlapping strands.
        base=old[f];rgb=base[:,:,:3].astype(float)
        hair=(rgb[:,:,0]>rgb[:,:,1]*1.1)&(rgb[:,:,1]<105)&(rgb[:,:,2]<100)&(a.Y<320)
        mask[hair]=0
        under=a.premul(base)
        side=a.smooth((a.X-535)/10)*a.smooth((a.Y-391)/8)*(1-a.smooth((a.Y-513)/5))
        # This clear old cel has no lowered cup: avoids two cups or residual arm.
        under=under*(1-side[:,:,None])+a.premul(old[3])*side[:,:,None]
        mixed=under*(1-mask[:,:,None])+np.clip(new,0,1)*mask[:,:,None]
        newside=new.copy();newside*=side[:,:,None]
        mixed=newside+mixed*(1-newside[:,:,3:4])
        generated.append(a.straight(mixed));out.append(generated[-1])
    out += [old[12],old[18],old[-1]]
    # The latter three poses start only once the cup has reached the floor.
    board=Image.new('RGBA',(1400,600),'#b7aeb0');d=ImageDraw.Draw(board)
    for k,frame in enumerate(out):
        im0=Image.fromarray(frame).resize((350,280));x=k%4*350;y=k//4*300
        board.alpha_composite(im0,(x,y+24));d.text((x+4,y+4),f'handover key {k}',fill='black')
    board.convert('RGB').save(Q/'handover-keys.jpg',quality=95)
    return record,out
def interpolate(keys,count):
    # Same established dual-matte interpolation, with a self-contained rebuild
    # entry. The optional ncnn model/runtime is intentionally not redistributed.
    runtime=R/'.tools/rife/runtime';tmp=R/'.tools/v21-handover';results=[]
    requested=round((count-1)*len(keys)/(len(keys)-1))
    for matte in [0,1]:
        inp=tmp/'handover-19'/str(matte)/'in';out=inp.parent/'out';inp.mkdir(parents=True,exist_ok=True);out.mkdir(exist_ok=True)
        for n,key in enumerate(keys):
            p=a.premul(key);rgb=np.uint8(np.clip((p[:,:,:3]+matte*(1-p[:,:,3:4]))*255+.5,0,255));Image.fromarray(rgb).save(inp/f'{n:08d}.png')
        p=subprocess.run([str(runtime/'rife-ncnn-vulkan.exe'),'-i',str(inp),'-o',str(out),'-m','rife-v4.6','-n',str(requested),'-g',os.environ.get('RIFE_GPU','1'),'-j','1:1:1','-f','%08d.png'],cwd=runtime,capture_output=True,timeout=180,creationflags=subprocess.CREATE_NO_WINDOW)
        (Q/f'handover-19-matte-{matte}.log').write_bytes(p.stdout+p.stderr)
        if p.returncode:raise RuntimeError('RIFE handover '+str(matte))
        files=sorted(out.glob('*.png'));assert len(files)==requested
        end=requested*(len(keys)-1)/len(keys)
        results.append([np.array(Image.open(files[min(requested-1,round(k*end/(count-1)))]).convert('RGB'),dtype=np.float32)/255 for k in range(count)])
    frames=[]
    for black,white in zip(*results):
        alpha=np.clip(1-np.median(white-black,axis=2),0,1);alpha[alpha<.04]=0
        rgb=np.clip(black/np.maximum(alpha[:,:,None],1/255),0,1);frames.append(np.uint8(np.clip(np.dstack([rgb,alpha])*255+.5,0,255)))
    return frames
if __name__=='__main__':
    import sys
    record,k=keys()
    if '--keys' in sys.argv:raise SystemExit(0)
    # Use the established GPU interpolation runtime; no new model/download.
    frames=interpolate(k,33)
    frames[0]=k[0];frames[-1]=k[-1]
    rec=a.save(record,frames);rec['half_frames']=16;rec['generated_poses']=4;rec['method']='four new handover drawings; protected existing heads/infant/legs; 33 dual-matte intermediate cels'
    (Q/'bridge-19.json').write_text(json.dumps({'record':rec,'source_frames':25,'output_frames':33,'new_generated_handover':True},indent=2))
    m=json.loads((D/'manifest.json').read_text());m['bridges']=[r for r in m['bridges'] if r['to']!=19]+[rec];m['bridges'].sort(key=lambda r:r['to']);(D/'manifest.json').write_text(json.dumps(m,indent=2))
    a.board('bridge-19-final',a.load(record),frames)
    print('handover 33 cels complete',flush=True)
