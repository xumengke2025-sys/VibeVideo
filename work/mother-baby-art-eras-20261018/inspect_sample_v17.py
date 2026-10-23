from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;FF=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
V=R/'out/continuity-last-pair-v17.mp4';Q=R/'qa/v17/sample-last';Q.mkdir(parents=True,exist_ok=True)
subprocess.run([str(FF),'-v','error','-y','-i',str(V),'-vf','crop=700:560:180:980,scale=350:280','-q:v','2',str(Q/'%04d.jpg')],check=True,timeout=90)
files=sorted(Q.glob('[0-9][0-9][0-9][0-9].jpg'));assert len(files)==64
for page in range(4):
    pic=Image.new('RGB',(1400,1200),'#eee4d3');d=ImageDraw.Draw(pic)
    for k in range(16):
        f=page*16+k;x=k%4*350;y=k//4*300;pic.paste(Image.open(files[f]),(x,y+20));d.text((x+4,y+3),f'F{896+f} | {(896+f)/24:.3f}s',fill='#342a20')
    pic.save(Q/f'page-{page}.jpg')
(Q/'capture.json').write_text(json.dumps({'video':str(V),'sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'frames':64,'start_frame':896,'end_frame':959,'capture_only':True},indent=2),encoding='utf8')
print('64 encoded sample frames exported')
