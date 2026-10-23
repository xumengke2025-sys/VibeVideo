from pathlib import Path
import sys,json
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'.tools/python-libs'));import cv2
Q=R/'qa/v19';Q.mkdir(parents=True,exist_ok=True)
YY,XX=np.mgrid[:560,:700]
def head(a):
    rgb=a[:,:,:3].astype(float)
    mask=(a[:,:,3]>180)&(rgb.mean(axis=2)<132)&(XX>70)&(XX<365)&(YY>210)&(YY<435)
    mask=cv2.morphologyEx(mask.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
    n,labels,stats,centers=cv2.connectedComponentsWithStats(mask,8)
    choices=[k for k in range(1,n) if stats[k,4]>400 and centers[k,0]<320 and stats[k,1]<390]
    if not choices:raise ValueError('No infant hair component')
    k=max(choices,key=lambda k:stats[k,4]);cs,_=cv2.findContours(np.uint8(labels==k),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # Dark costume outlines sometimes join the hair. Only use the upper head,
    # excluding the neck, bib and held prop from the size observation.
    top=int(stats[k,1]);seed=int(np.where((labels==k)&(YY<top+55))[1].mean());runs=[]
    # Fit the *outer* skull arc, not the face, bib, bottle or reaching hand.
    opaque=np.uint8(a[:,:,3]>180)
    # Alpha reconstruction can leave tiny internal pinholes in hair highlights.
    # These are texture, never part of the exterior skull contour.
    opaque=cv2.morphologyEx(opaque,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
    outer,_=cv2.findContours(opaque,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    opaque[:]=0;cv2.drawContours(opaque,outer,-1,1,cv2.FILLED)
    edge=(opaque-cv2.erode(opaque,np.ones((3,3),np.uint8)))>0
    near_hair=cv2.dilate(np.uint8(labels==k),np.ones((5,5),np.uint8))>0
    py,px=np.where(edge&near_hair&(YY<top+80)&(XX<365))
    if len(px)>30:
        A=np.column_stack([2*px,2*py,np.ones(len(px))]);v=np.linalg.lstsq(A,px*px+py*py,rcond=None)[0]
        cx,cy=v[:2];radius=np.sqrt(max(0,v[2]+cx*cx+cy*cy))
        if 48<radius<90 and top+35<cy<top+100:
            return np.array([cx,cy,radius]),stats[k].tolist()
    for row in range(top+30,min(top+80,500)):
        line=(a[row,:,3]>180);changes=np.diff(np.r_[False,line,False].astype(int));starts=np.where(changes==1)[0];ends=np.where(changes==-1)[0]
        for left,right in zip(starts,ends):
            if left<seed<right and 65<right-left<190 and right<390:
                runs.append([left,right])
    if len(runs)<5:
        hull=cv2.convexHull(max(cs,key=cv2.contourArea));(x,y),radius=cv2.minEnclosingCircle(hull)
        return np.array([x,y,radius]),stats[k].tolist()
    runs=np.array(runs);widths=runs[:,1]-runs[:,0];width=float(np.percentile(widths,75));close=np.abs(widths-width)<5
    x=float(np.mean(runs[close].mean(axis=1)));radius=width/2;y=top+radius
    return np.array([x,y,radius]),stats[k].tolist()
if __name__=='__main__':
    m=json.loads((R/'assets/motion-v18/manifest.json').read_text());records=[]
    for page in range(4):
        board=Image.new('RGB',(1400,1400),'#46304a');d=ImageDraw.Draw(board)
        for row,r in enumerate(m['scenes'][page*5:page*5+5]):
            atlas=Image.open(R/'assets/motion-v18'/r['file'])
            for col,f in enumerate([0,12,24,36,47]):
                x=f%6*700;y=f//6*560;a=np.array(atlas.crop((x,y,x+700,y+560)));h,stat=head(a);im=Image.fromarray(a);draw=ImageDraw.Draw(im);cx,cy,rr=h;draw.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),outline='lime',width=3)
                bg=Image.new('RGBA',im.size,'#ba78a2');bg.alpha_composite(im);bg=bg.resize((280,224));board.paste(bg.convert('RGB'),(col*280,row*280+35));d.text((col*280+5,row*280+8),f'{r["era"]} F{f} diameter={rr*2:.1f}',fill='white');records.append({'scene':r['era'],'frame':f,'head':h.tolist(),'component':stat})
        board.save(Q/f'infant-measure-{page}.jpg')
    (Q/'infant-before-samples.json').write_text(json.dumps(records,indent=2));diam=[r['head'][2]*2 for r in records];print(json.dumps({'min':min(diam),'max':max(diam)}))
