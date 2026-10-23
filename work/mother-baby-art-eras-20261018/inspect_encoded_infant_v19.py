"""Time-indexed infant-size evidence from the delivered MP4 itself."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'.tools/python-libs'));import cv2
V=R/'out/mother-baby-20-eras-portrait-v19-40s.mp4';Q=R/'qa/v19/final';Q.mkdir(parents=True,exist_ok=True)
rows=[[i*48+k for k in [10,18,26,34,42]] for i in range(20)]
continuous={'pat':list(range(610,634)),'fan':list(range(786,810)),'milk':list(range(870,894)),'final-cut':list(range(904,928))}
wanted=set(sum(rows,[])+sum(continuous.values(),[]));frames={};c=cv2.VideoCapture(str(V));idx=0
while True:
    ok,a=c.read()
    if not ok:break
    if idx in wanted:frames[idx]=Image.fromarray(cv2.cvtColor(a[980:1540,180:880],cv2.COLOR_BGR2RGB))
    idx+=1
c.release();assert idx==960 and len(frames)==len(wanted)
for page in range(4):
    board=Image.new('RGB',(1400,1260),'#f1e7d4');d=ImageDraw.Draw(board)
    for j,ids in enumerate(rows[page*5:page*5+5]):
        for k,f in enumerate(ids):
            board.paste(frames[f].resize((280,224)),(k*280,j*252+25));d.text((k*280+5,j*252+5),f'encoded v19 | {f/24:.3f}s',fill='#403026')
    board.save(Q/f'infant-encoded-{page}.png')
for name,ids in continuous.items():
    board=Image.new('RGB',(1400,304*6),'#f1e7d4');d=ImageDraw.Draw(board)
    for k,f in enumerate(ids):
        board.paste(frames[f].resize((350,280)),(k%4*350,k//4*304+24));d.text((k%4*350+5,k//4*304+5),f'{f/24:.3f}s | F{f}',fill='#403026')
    board.save(Q/f'continuous-encoded-{name}.png')
report={'video_sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'decoded_frames':idx,'era_sample_frames':rows,'continuous_frames':continuous,'captured_frames':len(frames),'scope':'Actual encoded crops for manual viewing. Capture alone is not review.'}
(Q/'infant-capture.json').write_text(json.dumps(report,indent=2));print(json.dumps({'decoded':idx,'captured':len(frames)}))
