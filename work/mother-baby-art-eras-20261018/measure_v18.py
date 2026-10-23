from pathlib import Path
import numpy as np,json
from PIL import Image,ImageDraw
import build_continuity_v17 as b
R=Path(__file__).resolve().parent;Q=R/'qa/v18';Q.mkdir(exist_ok=True)
def face(a,person):
    im=b.straight(a);rgb=im[:,:,:3].astype(float)
    r,g,bl=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    mask=(im[:,:,3]>160)&(r>145)&(g>75)&(r>g*1.10)&(g>bl*1.08)&(r-g<115)
    yy,xx=np.mgrid[:560,:700]
    mask &= ((xx>335)&(xx<580)&(yy>90)&(yy<330)) if person=='mother' else ((xx>90)&(xx<355)&(yy>235)&(yy<450))
    mask=b.cv2.morphologyEx(np.uint8(mask),b.cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
    n,labels,stats,c=b.cv2.connectedComponentsWithStats(mask,8)
    candidates=[i for i in range(1,n) if stats[i,4]>200]
    k=max(candidates,key=lambda i:stats[i,4])
    x,y,w,h=stats[k,:4];segment=labels==k
    widths=[]
    for row in range(y+12,min(y+80,560)):
        xs=np.where(segment[row])[0]
        if len(xs)>10:widths.append(int(xs[-1]-xs[0]+1))
    return [int(x),int(y),int(np.percentile(widths,85)),min(int(h),80)]
if __name__=='__main__':
    board=Image.new('RGB',(1400,1200),'#392743');draw=ImageDraw.Draw(board);data=[]
    for i in range(20):
        a=b.endpoint(i);im=Image.fromarray(b.straight(a));d=ImageDraw.Draw(im)
        rec={'era':i}
        for who,color in [('mother','cyan'),('baby','lime')]:
            x,y,w,h=face(a,who);d.rectangle([x,y,x+w,y+h],outline=color,width=3);rec[who]=[x,y,w,h]
        bg=Image.new('RGBA',im.size,'#b4269a');bg.alpha_composite(im);bg.thumbnail((280,280));x=i%5*280;y=i//5*300;board.paste(bg.convert('RGB'),(x,y+22));draw.text((x+5,y+3),str(i),fill='white');data.append(rec)
    board.save(Q/'face-measure.jpg');(Q/'face-measure.json').write_text(json.dumps(data,indent=2));print(json.dumps(data))
