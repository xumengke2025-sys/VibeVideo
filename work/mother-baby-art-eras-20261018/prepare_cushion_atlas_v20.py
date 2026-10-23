from pathlib import Path
import json
from PIL import Image
import sys,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent/'.tools/python-libs'))
import cv2
R=Path(__file__).resolve().parent
a=Image.open(R/'assets/motion-v20/cushions-generated.png').convert('RGBA');out=Image.new('RGBA',(1500,360))
# Generation has equal 5-column layout with four baseline-centred rows.
for i in range(20):
    x0=round(i%5*a.width/5);x1=round((i%5+1)*a.width/5)
    y0=[95,310,530,740][i//5];y1=[275,490,710,930][i//5]
    im=a.crop((x0,y0,x1,y1));arr=np.array(im);n,lab,stats,_=cv2.connectedComponentsWithStats(np.uint8(arr[:,:,3]>20),8);main=1+np.argmax(stats[1:,4]);keep=cv2.dilate(np.uint8(lab==main),np.ones((3,3),np.uint8));arr[keep==0]=0;im=Image.fromarray(arr);bbox=im.getchannel('A').point(lambda v:255 if v>20 else 0).getbbox();im=im.crop(bbox)
    im=im.resize((270,60),Image.Resampling.NEAREST if i==17 else Image.Resampling.LANCZOS)
    out.alpha_composite(im,(i%5*300+15,i//5*90+15))
out.save(R/'assets/motion-v20/cushions-atlas.png')
