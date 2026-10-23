"""Decouple fixed support from v19 actor cels; never rescale the infant.

Manually registered contact contours seed a narrow local alpha segmentation.
Optical flow transports the support mask, not actor pixels. The unmasked actor
pixels remain byte-identical to v19. Fixed cushions are composited separately.
"""
from pathlib import Path
import json,sys,hashlib,argparse
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'.tools/python-libs'))
import cv2
cv2.setNumThreads(2)
FLOW=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
FLOW.setFinestScale(0)
S=R/'assets/motion-v19';D=R/'assets/motion-v20';Q=R/'qa/v20'
D.mkdir(exist_ok=True);Q.mkdir(exist_ok=True)
M=json.loads((S/'manifest.json').read_text())
Y,X=np.indices((560,700),dtype=np.float32)
# Contact contour coordinates in v19's 700x560 registration canvas. The
# polygons follow the lower edge of garments/feet, with a small refinement band.
PATHS=[
[(135,435),(181,448),(185,466),(193,479),(220,486),(233,489),(246,500),(262,505),(272,502),(282,480),(298,486),(317,493),(334,497),(344,490),(357,468),(370,448)],
[(175,428),(230,442),(229,465),(236,477),(251,483),(265,489),(276,499),(288,500),(297,490),(302,482),(323,480),(341,484),(351,492),(361,494),(372,488),(384,469),(390,441),(402,435)],
[(180,438),(215,455),(218,470),(223,482),(239,489),(258,491),(270,489),(280,496),(294,504),(304,505),(314,499),(321,482),(333,484),(351,492),(364,494),(377,480),(384,464),(393,446)],
[(155,435),(211,450),(212,467),(222,477),(242,482),(253,485),(262,489),(276,500),(285,504),(296,503),(305,494),(311,481),(325,482),(340,486),(352,491),(364,488),(376,468),(386,438)],
[(150,432),(209,443),(209,461),(220,475),(242,479),(257,479),(270,487),(281,492),(293,490),(304,480),(308,473),(325,473),(340,477),(353,479),(363,474),(376,459),(387,435)],
[(172,433),(224,448),(222,466),(229,478),(251,485),(269,490),(276,501),(285,509),(296,511),(303,504),(305,487),(320,489),(335,492),(348,500),(358,500),(369,491),(378,475),(389,440)],
[(155,435),(188,451),(187,465),(202,474),(224,476),(237,476),(246,481),(259,489),(270,492),(280,490),(287,481),(288,475),(313,478),(326,486),(337,489),(346,487),(360,475),(369,457),(380,435)],
[(140,440),(171,459),(175,470),(189,477),(191,489),(211,497),(236,502),(246,510),(261,516),(275,514),(287,505),(291,494),(318,495),(334,501),(350,506),(361,506),(375,495),(385,478),(394,445)],
[(155,438),(210,454),(211,469),(219,481),(239,488),(260,489),(270,500),(280,506),(292,505),(302,496),(310,485),(329,488),(344,494),(355,496),(368,487),(381,469),(390,439)],
[(155,442),(208,458),(212,473),(229,479),(243,490),(257,497),(267,503),(278,505),(288,502),(297,494),(300,482),(322,485),(339,492),(352,497),(363,497),(373,486),(384,472),(394,441)],
[(150,435),(190,460),(190,475),(203,483),(221,489),(232,495),(250,502),(266,506),(279,505),(287,497),(289,488),(308,486),(326,493),(339,498),(351,497),(365,486),(378,467),(388,440)],
[(150,435),(207,449),(208,464),(214,476),(226,483),(244,491),(255,496),(269,502),(282,503),(291,496),(299,483),(314,484),(335,490),(345,494),(356,492),(368,479),(379,460),(390,435)],
[(145,435),(197,451),(198,472),(207,483),(228,488),(235,488),(241,495),(253,502),(265,503),(277,498),(285,488),(293,488),(303,486),(308,508),(341,514),(365,506),(365,440)],
[(150,435),(210,449),(210,468),(216,480),(229,488),(248,492),(259,500),(271,505),(282,506),(292,501),(301,490),(306,481),(324,485),(337,491),(347,497),(360,499),(373,491),(385,471),(394,438)],
[(155,435),(223,447),(221,466),(226,481),(239,489),(254,492),(265,500),(274,504),(284,502),(294,492),(299,486),(319,486),(333,493),(344,496),(355,492),(369,475),(377,451),(391,435)],
[(170,440),(221,460),(227,478),(243,486),(257,493),(268,501),(278,505),(288,503),(297,495),(301,487),(317,489),(340,495),(351,500),(364,499),(378,486),(388,467),(398,438)],
[(170,439),(225,458),(225,477),(238,488),(260,492),(280,499),(293,504),(305,504),(317,495),(323,486),(340,487),(362,495),(375,499),(389,496),(401,483),(412,461),(419,441)],
[(155,440),(199,458),(199,476),(217,482),(235,490),(249,497),(267,504),(281,505),(290,498),(298,488),(313,488),(327,496),(343,500),(354,496),(365,487),(373,469),(383,439)],
[(160,437),(220,451),(220,476),(230,487),(252,493),(263,500),(277,506),(289,506),(300,499),(307,489),(321,490),(339,497),(351,501),(365,499),(379,485),(393,467),(403,438)],
[(170,435),(199,443),(199,483),(204,494),(214,500),(229,500),(239,495),(243,487),(251,491),(268,497),(278,503),(291,506),(302,503),(311,495),(314,490),(336,489),(354,496),(369,499),(382,497),(396,483),(406,461),(415,436)]
]
def frames(r):
    a=np.array(Image.open(S/r['file']).convert('RGBA'))
    return [a[f//6*560:f//6*560+560,f%6*700:f%6*700+700].copy() for f in range(r['frames'])]
def gray(a):
    rgb=a[:,:,:3].astype(np.float32);alpha=a[:,:,3:4]/255
    return cv2.cvtColor(np.uint8(rgb*alpha+np.array([150,120,140])*(1-alpha)),cv2.COLOR_RGB2GRAY)
def initial_mask(a,i):
    pts=PATHS[i];p=np.array(pts+[(pts[-1][0]+5,540),(pts[0][0]-5,540)],np.int32)
    m=np.zeros((560,700),np.uint8);cv2.fillPoly(m,[p],255)
    # The reference alpha carries transparent space around the cushion.
    return m
def correct_mask(a,m,era,f=0):
    m=m.copy();r,g,b=[a[:,:,k].astype(float) for k in range(3)]
    # Preserve the adult's connected cream/red footwear, including its toe left
    # of the nominal adult crop. The mask may never truncate this contact edge.
    shoe=((r>170)&(g>145)&(b>95))|((r>110)&(r>g*1.6)&(r>b*1.6))
    shoe&=(X>=385)&(Y>455)&(a[:,:,3]>12)
    n,lab,stats,_=cv2.connectedComponentsWithStats(shoe.astype(np.uint8),8)
    protect=np.zeros_like(m)
    for k in range(1,n):
        xx,yy,ww,hh,area=stats[k]
        if xx+ww>438 and area>30:protect[lab==k]=255
    protect=cv2.dilate(protect,np.ones((3,3),np.uint8));m[protect>0]=0
    m[(Y>519)&(X<385)]=255
    if era==12:
        prop=(X>275)&(Y>420)&(r>g*1.55)&(r>b*1.65)&(a[:,:,3]>3)
        prop=cv2.dilate(prop.astype(np.uint8),np.ones((3,3),np.uint8));m[prop>0]=0
        cx=np.interp(f,[0,12,24,36,47],[250,248,231,236,243]);cy=484;rx=np.interp(f,[0,24,47],[20,18,19]);ry=18
        foot=((X-cx)/rx)**2+((Y-cy)/ry)**2<1;m[foot]=0
    if era==17:
        gold=(X<405)&(X>130)&(Y>470)&(r>130)&(g>85)&(r>g*1.12)&(b<g*.58)
        gold=cv2.dilate(gold.astype(np.uint8),np.ones((3,3),np.uint8));m[gold>0]=255
    return m
def refine(a,m):
    """Narrow edge-aware graph cut: cannot alter anatomy outside an 8px band."""
    y0,y1,x0,x1=405,537,95,435
    mm=m[y0:y1,x0:x1];aa=a[y0:y1,x0:x1]
    definite=cv2.erode(mm,np.ones((9,9),np.uint8))>127
    possible=cv2.dilate(mm,np.ones((9,9),np.uint8))>127
    labels=np.where(possible,cv2.GC_PR_FGD,cv2.GC_BGD).astype(np.uint8)
    labels[definite]=cv2.GC_FGD
    labels[aa[:,:,3]<8]=cv2.GC_BGD
    if not np.any(labels==cv2.GC_FGD):return m
    cv2.setRNGSeed(2020)
    cv2.grabCut(aa[:,:,:3].copy(),labels,None,np.zeros((1,65)),np.zeros((1,65)),2,cv2.GC_INIT_WITH_MASK)
    result=np.zeros_like(m);result[y0:y1,x0:x1]=np.uint8((labels==cv2.GC_FGD)|(labels==cv2.GC_PR_FGD))*255
    return result
def transported(ref,a,mask):
    flow=FLOW.calc(gray(a),gray(ref),None)
    return cv2.remap(mask,X+flow[:,:,0],Y+flow[:,:,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
def cut(a,m):
    out=a.copy();out[:,:,3]=np.uint8(a[:,:,3].astype(np.float32)*(1-m.astype(np.float32)/255)+.5)
    out[out[:,:,3]==0,:3]=0
    n,lab,stats,centers=cv2.connectedComponentsWithStats(np.uint8(out[:,:,3]>10),8)
    for j in range(1,n):
        x,y,w,h,area=stats[j]
        if y>420 and x<430 and area<500:out[lab==j]=0
    return out
def save(r,ff):
    sheet=Image.new('RGBA',(r['columns']*700,r['rows']*560))
    for i,a in enumerate(ff):sheet.paste(Image.fromarray(a),(i%6*700,i//6*560))
    p=D/r['file'];sheet.save(p,compress_level=3);o=dict(r);o['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();return o
def checkpoint(out):
    merged=dict(out)
    if (D/'manifest.json').exists():
        prior=json.loads((D/'manifest.json').read_text())
        for key in ['scenes','bridges']:
            records={r['file']:r for r in prior[key]};records.update({r['file']:r for r in out[key]});merged[key]=[records[k] for k in sorted(records)]
    p=D/'manifest.json.new';p.write_text(json.dumps(merged,indent=2));p.replace(D/'manifest.json')
def board(r,ff,mm):
    b=Image.new('RGB',(1750,740),'#baa5b7');d=ImageDraw.Draw(b)
    for j,f in enumerate([0,len(ff)//4,len(ff)//2,3*len(ff)//4,len(ff)-1]):
        for row in range(3):
            a=ff[f].copy()
            if row==1:
                a= cut(a,mm[f])
            if row==2:
                a[:,:,:3]=np.uint8(a[:,:,:3]*(1-mm[f][:,:,None]/255*.65)+np.array([230,20,90])*mm[f][:,:,None]/255*.65)
            im=Image.new('RGBA',(700,560),'#baa5b7');im.alpha_composite(Image.fromarray(a));crop=im.crop((70,320,430,540)).resize((350,214))
            b.paste(crop.convert('RGB'),(j*350,row*245+25));d.text((j*350+5,row*245+5),f'{r["file"]} F{f} '+['source','actor only','mask'][row],fill='black')
    b.save(Q/(r['file'].replace('.png','-separation.jpg')),quality=95)
def build(only,bridge_only=False):
    all_masks={};out={**M,'version':20,'route':'v19 pixels retained; support masks transported by optical flow; stationary cushion is a separate runtime layer','scenes':[],'bridges':[]}
    for r in M['scenes']:
        if bridge_only:continue
        i=r['era']
        if only and i not in only:continue
        ff=frames(r);base=refine(ff[0],initial_mask(ff[0],i));refs={0:base}
        if i==12:
            for f in [24,47]:
                p=[(140,435),(178,452),(178,476),(188,487),(207,493),(218,499),(234,503),(246,503),(255,501),(269,498),(278,487),(290,485),(292,530),(380,530),(385,440),(390,540),(135,540)]
                mask=np.zeros((560,700),np.uint8);cv2.fillPoly(mask,[np.array(p,np.int32)],255);refs[f]=refine(ff[f],mask)
        mm=[]
        for f,a in enumerate(ff):
            near=min(refs,key=lambda k:abs(k-f));mm.append(refs[near] if near==f else transported(ff[near],a,refs[near]))
        # Refine transported visible boundary where colour contrast is reliable.
        mm=[refine(a,m) for a,m in zip(ff,mm)]
        mm=[correct_mask(a,cv2.GaussianBlur(m,(3,3),.45),i,f) for f,(a,m) in enumerate(zip(ff,mm))]
        all_masks[i]=[mm[0],mm[-1]]
        (Q/'masks').mkdir(exist_ok=True)
        np.savez_compressed(Q/'masks'/f'scene-{i:02d}.npz',masks=np.stack(mm))
        out['scenes'].append(save(r,[cut(a,m) for a,m in zip(ff,mm)]));checkpoint(out);board(r,ff,mm);print(r['file'],flush=True)
    if bridge_only:
        required={x for r in M['bridges'] if r['to'] in only for x in [r['from'],r['to']]}
        for i in required:
            with np.load(Q/'masks'/f'scene-{i:02d}.npz') as archive:
                masks=archive['masks'];all_masks[i]=[masks[0].copy(),masks[-1].copy()]
    for r in M['bridges']:
        if bridge_only and r['to'] not in only:continue
        a,b=r['from'],r['to']
        if a not in all_masks or b not in all_masks:continue
        ff=frames(r);ma=all_masks[a][-1];mb=all_masks[b][0];mm=[]
        for f,im in enumerate(ff):
            if f==0:m=ma
            elif f==len(ff)-1:m=mb
            else:
                q=f/(len(ff)-1);m0=transported(ff[0],im,ma);m1=transported(ff[-1],im,mb)
                m=np.uint8(np.clip(m0.astype(float)*(1-q)+m1*q,0,255));m=refine(im,m);m=cv2.GaussianBlur(m,(3,3),.45);m=correct_mask(im,m,12 if 12 in [a,b] else (17 if 17 in [a,b] else a),47 if a==12 else 0)
            mm.append(m)
        out['bridges'].append(save(r,[cut(im,m) for im,m in zip(ff,mm)]));checkpoint(out);board(r,ff,mm);print(r['file'],flush=True)
    if only and (D/'manifest.json').exists():
        old=json.loads((D/'manifest.json').read_text())
        for k in ['scenes','bridges']:
            records={r['file']:r for r in old[k]};records.update({r['file']:r for r in out[k]});out[k]=[records[s] for s in sorted(records)]
    (D/'manifest.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--only',default='');p.add_argument('--bridges',default='');args=p.parse_args();build(set(map(int,filter(None,(args.bridges or args.only).split(',')))),bool(args.bridges))
