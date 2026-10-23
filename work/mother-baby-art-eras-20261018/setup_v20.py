from pathlib import Path
import json
from PIL import Image
import sys,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent/'.tools/python-libs'))
import cv2
R=Path(__file__).resolve().parent
for name in ['film/index-v19.html','film/sequences-v19.js','render-v19.mjs','render-batched-v19.mjs','preview-v19.mjs']:
    s=(R/name).read_text(encoding='utf8').replace('v19','v20')
    (R/name.replace('v19','v20')).write_text(s,encoding='utf8')
p=R/'film/index-v20.html';s=p.read_text(encoding='utf8').replace('<script src="transitions-v16.js">','<script src="environment-life-v20.js"></script><script src="transitions-v16.js">');p.write_text(s,encoding='utf8')
p=R/'film/sequences-v20.js';s=p.read_text(encoding='utf8').replace('let manifest;','let manifest,cushions;')
s=s.replace('STOP_ENV_V15.draw(c,bg[i],held.time,i,held.k);','ENV_LIFE_V20.draw(c,bg[i],held.time,i,held.k);')
s=s.replace("ellipse(c,555,1508,208,14,'rgba(65,43,27,.10)');", "ellipse(c,555,1508,208,14,'rgba(65,43,27,.10)');drawCushion(c,p);")
s=s.replace('function actors(c,t,forceEra)', '''function drawCushion(c,p){const draw=(i,a)=>{c.globalAlpha=a;c.drawImage(cushions,i%5*300,Math.floor(i/5)*90,300,90,310,1435,290,87)};if(p.from===p.to)draw(p.from,1);else {draw(p.from,1);draw(p.to,smooth(p.progress));}c.globalAlpha=1;}
function actors(c,t,forceEra)''')
s=s.replace('await STOP_ENV_V15.ready;','await STOP_ENV_V15.ready;cushions=await load("../assets/motion-v20/cushions-atlas.png");')
s=s.replace("route:'independent infant skull-arc size registration with protected adult face and seamless shared-contact mapping; dual-matte RGBA'", "route:'v19 infant size retained byte-for-byte above support; independently fixed cushion layer; local rooted environment motion'")
p.write_text(s,encoding='utf8')
a=Image.open(R/'assets/motion-v20/cushions-generated.png').convert('RGBA');out=Image.new('RGBA',(1500,360))
# Generation has equal 5-column layout with four baseline-centred rows.
for i in range(20):
    x0=round(i%5*a.width/5);x1=round((i%5+1)*a.width/5)
    y0=[95,310,530,740][i//5];y1=[275,490,710,930][i//5]
    im=a.crop((x0,y0,x1,y1));arr=np.array(im);n,lab,stats,_=cv2.connectedComponentsWithStats(np.uint8(arr[:,:,3]>20),8);main=1+np.argmax(stats[1:,4]);keep=cv2.dilate(np.uint8(lab==main),np.ones((3,3),np.uint8));arr[keep==0]=0;im=Image.fromarray(arr);bbox=im.getchannel('A').point(lambda v:255 if v>20 else 0).getbbox();im=im.crop(bbox)
    im=im.resize((270,60),Image.Resampling.NEAREST if i==17 else Image.Resampling.LANCZOS)
    out.alpha_composite(im,(i%5*300+15,i//5*90+15))
out.save(R/'assets/motion-v20/cushions-atlas.png')
