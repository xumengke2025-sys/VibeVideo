from pathlib import Path
import sys,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'.tools/python-libs'))
import cv2
cv2.setNumThreads(2)
V=R/'out/mother-baby-20-eras-portrait-v20-40s.mp4';Q=R/'qa/v20/final'
samples=[('lantern',10.45,11.45,(780,240,1030,650)),('curtain',18.4,19.4,(640,650,900,1130)),('vine',38.45,39.45,(840,340,1080,820))]
joins=list(range(836,845));wanted=set(joins)
for _,a,b,_ in samples:wanted.update([round(a*24),round(b*24)])
cap=cv2.VideoCapture(str(V));found={};f=0
while True:
    ok,a=cap.read()
    if not ok:break
    if f in wanted:found[f]=Image.fromarray(cv2.cvtColor(a,cv2.COLOR_BGR2RGB))
    f+=1
cap.release();total=f;assert total==960 and len(found)==len(wanted)
sheet=Image.new('RGB',(900,1500),'#eee6d5');d=ImageDraw.Draw(sheet)
for k,(name,a,b,box) in enumerate(samples):
    aa=found[round(a*24)].crop(box);bb=found[round(b*24)].crop(box)
    delta=Image.fromarray(np.uint8(np.clip(np.abs(np.array(aa).astype(np.int16)-np.array(bb).astype(np.int16))*5,0,255)))
    for j,im in enumerate([aa,bb,delta]):
        im.thumbnail((300,470));sheet.paste(im,(j*300,k*500+26));d.text((j*300+5,k*500+6),f'{name} | '+([f'{round(a*24)/24:.3f}s',f'{round(b*24)/24:.3f}s','difference x5'][j]),fill='#342b23')
sheet.save(Q/'encoded-environment-details.png')
sheet=Image.new('RGB',(1050,912),'#eee6d5');d=ImageDraw.Draw(sheet)
for k,f in enumerate(joins):
    im=found[f].crop((180,980,880,1540)).resize((350,280));x=k%3*350;y=k//3*304
    sheet.paste(im,(x,y+24));d.text((x+5,y+5),f'join 35s | F{f} | {f/24:.3f}s',fill='#342b23')
sheet.save(Q/'encoded-join-35.png')
report={'video_sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'decoded_frames':total,'background_pairs':[{'name':n,'frames':[round(a*24),round(b*24)],'crop':box} for n,a,b,box in samples],'join_35_frames':joins,'scope':'Encoded detail pairs and consecutive 35s render-batch join frames; capture alone does not establish viewing.'}
(Q/'environment-capture.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps({'captured':len(found)}))
