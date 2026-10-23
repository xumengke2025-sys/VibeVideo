from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
FF=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
V=R/'out/mother-baby-20-eras-portrait-v17-40s.mp4'
O=R/'qa/v17/transitions';O.mkdir(parents=True,exist_ok=True)
frames=O/'thumbs';frames.mkdir(exist_ok=True)
subprocess.run([str(FF),'-v','error','-y','-i',str(V),'-vf','scale=270:480','-q:v','3',str(frames/'%04d.jpg')],check=True,timeout=180)
files=sorted(frames.glob('*.jpg'));assert len(files)==960,len(files)
offsets=[-8,-6,-4,-2,0,2,4,7]
rows=[]
for to in range(1,20):
    pic=Image.new('RGB',(1080,2*504),'#eee6d5');d=ImageDraw.Draw(pic)
    for k,off in enumerate(offsets):
        f=to*48+off;im=Image.open(files[f]);x=k%4*270;y=k//4*504
        pic.paste(im,(x,y+24));d.text((x+5,y+5),f'{f/24:.3f}s | F{f}',fill='#302719')
    pic.save(O/f'cut-{to*2:02d}.jpg',quality=92)
    rows.append({'cut_seconds':to*2,'frames':[to*48+off for off in offsets]})
# A compact overview gives each era a midpoint without rescaling its actors.
pic=Image.new('RGB',(1080,4*408),'#eee6d5');d=ImageDraw.Draw(pic)
for i in range(20):
    im=Image.open(files[i*48+24]).crop((45,255,225,390)).resize((216,162))
    x=i%5*216;y=i//5*204;pic.paste(im,(x,y+24));d.text((x+5,y+5),f'era {i:02d} | {i*2+1}s',fill='#302719')
pic.crop((0,0,1080,816)).save(O/'all-actors-midpoint.jpg',quality=94)
(O/'capture.json').write_text(json.dumps({'video_sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'decoded_thumbnails':960,'thumbnail_size':[270,480],'transition_samples':rows,'scope':'Exported for production checks. Capturing is not evidence of actual viewing or a new independent review.'},indent=2),encoding='utf8')
print(json.dumps({'decoded':960,'cut_sheets':19,'midpoint_actors':20}))
