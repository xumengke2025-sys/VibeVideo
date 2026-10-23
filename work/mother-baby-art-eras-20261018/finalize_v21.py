"""Decode delivered video; export time-indexed evidence, without claiming viewing."""
from pathlib import Path
import sys,json,hashlib,subprocess,re
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'.tools/python-libs'))
import cv2
cv2.setNumThreads(2)
V=R/'out/mother-baby-20-eras-portrait-v21-40s.mp4';Q=R/'qa/v21/final';Q.mkdir(parents=True,exist_ok=True)
FF=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
p=subprocess.run([str(FF),'-hide_banner','-i',str(V),'-threads','1','-c:v','rawvideo','-f','null','-'],capture_output=True,text=True,timeout=240)
(Q/'decode-log.txt').write_text(p.stderr,encoding='utf8')
frames=re.findall(r'frame=\s*(\d+)',p.stderr);stream=re.search(r'Video:.*?(\d{3,5})x(\d{3,5}).*?(\d+(?:\.\d+)?) fps',p.stderr);dur=re.search(r'Duration: (\d+):(\d+):(\d+(?:\.\d+)?)',p.stderr)
if p.returncode or not frames or not stream or not dur:
    raise RuntimeError('Video decode failed; see qa/v21/final/decode-log.txt')
d={'sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'decode_exit':p.returncode,'frames':int(frames[-1]),'width':int(stream[1]),'height':int(stream[2]),'fps':float(stream[3]),'duration':int(dur[1])*3600+int(dur[2])*60+float(dur[3]),'audio':bool(re.search(r'Stream.*Audio:',p.stderr))}
assert p.returncode==0 and (d['frames'],d['width'],d['height'],d['fps'],d['duration'],d['audio'])==(960,1080,1920,24,40,False),d
(Q/'engineering-check.json').write_text(json.dumps(d,indent=2))
rows=[[i*48+k for k in [10,18,26,34,42]] for i in range(20)]
continuous={'pat':list(range(610,634)),'fan':list(range(786,810)),'milk':list(range(870,894)),'handover':list(range(896,929)),'final':list(range(928,960))}
full=[19,451,884,906,939];wanted=set(sum(rows,[])+sum(continuous.values(),[])+full)
captured={};cap=cv2.VideoCapture(str(V));idx=0
while True:
    ok,a=cap.read()
    if not ok:break
    if idx in wanted:
        captured[idx]=Image.fromarray(cv2.cvtColor(a[980:1540,180:880],cv2.COLOR_BGR2RGB))
        if idx in full:Image.fromarray(cv2.cvtColor(a,cv2.COLOR_BGR2RGB)).save(Q/f'full-F{idx}.png')
    idx+=1
cap.release();assert idx==960 and len(captured)==len(wanted)
for page in range(4):
    board=Image.new('RGB',(1400,1260),'#f1e7d4');dr=ImageDraw.Draw(board)
    for j,ids in enumerate(rows[page*5:page*5+5]):
        for k,f in enumerate(ids):
            board.paste(captured[f].resize((280,224)),(k*280,j*252+25));dr.text((k*280+4,j*252+5),f'v21 {f/24:.3f}s F{f}',fill='#403026')
    board.save(Q/f'eras-{page}.jpg',quality=94)
for name,ids in continuous.items():
    board=Image.new('RGB',(1400,304*((len(ids)+3)//4)),'#f1e7d4');dr=ImageDraw.Draw(board)
    for k,f in enumerate(ids):
        board.paste(captured[f].resize((350,280)),(k%4*350,k//4*304+24));dr.text((k%4*350+4,k//4*304+4),f'v21 {f/24:.3f}s F{f}',fill='#403026')
    board.save(Q/f'continuous-{name}.png')
board=Image.new('RGB',(1350,1225),'#f1e7d4');dr=ImageDraw.Draw(board)
for k,f in enumerate(full):
    im=Image.open(Q/f'full-F{f}.png').resize((270,480));board.paste(im,(k*270,25));dr.text((k*270+4,4),f'v21 {f/24:.3f}s',fill='black')
board.crop((0,0,1350,505)).save(Q/'full-check.jpg',quality=94)
(Q/'capture.json').write_text(json.dumps({'video_sha256':d['sha256'],'decoded_frames':960,'era_sample_frames':rows,'continuous_frames':continuous,'full_frames':full,'unique_captured':len(wanted),'capture_only':True,'scope':'Export alone does not establish actual viewing or independent review.'},indent=2))
print(json.dumps(d));print(json.dumps({'captured':len(wanted)}))
