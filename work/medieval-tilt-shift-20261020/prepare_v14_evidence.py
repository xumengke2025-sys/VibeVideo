"""Render no imagery: make clearly labelled evidence sheets from actual PNGs."""
from pathlib import Path
import math,json,subprocess,sys
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;Q=P/'qa/v14';F=P/'render/sample-v14'
FF='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
records=[]
def sheet(label,frames,crop=None,width=216):
    height=round(width*(crop[3]-crop[1])/(crop[2]-crop[0])) if crop else round(width*1920/1080)
    out=Image.new('RGB',(width*6,(height+24)*math.ceil(len(frames)/6)),'#202020');draw=ImageDraw.Draw(out)
    for i,f in enumerate(frames):
        with Image.open(F/f'{f:05d}.png') as im:
            if crop:im=im.crop(crop)
            im=im.resize((width,height));x=i%6*width;y=i//6*(height+24);out.paste(im,(x,y+24));draw.text((x+5,y+5),f'{f} | {f/24:.3f}s',fill='white')
    path=Q/f'sample-{label}.jpg';out.save(path,quality=95)
    records.append({'label':label,'frames':frames,'crop':crop,'path':str(path),'viewed':False})
if '--canal-only' in sys.argv:
    sheet('canal-motion',list(range(744,768)))
    (Q/'sample-canal-evidence.json').write_text(json.dumps(records,indent=2),encoding='utf8')
    print('CANAL_SEQUENCE_SHEET_READY');sys.exit(0)
sheet('story',[48,288,528,756,934,1115,1320,1356,1380,1404,1464,1752])
sheet('offering-stages',list(range(1320,1494,12)),crop=(280,830,800,1310),width=260)
for start in [1356,1380,1452]:sheet('offering-'+str(start),list(range(start,start+24)),crop=(310,850,750,1190),width=220)
sheet('canal-motion',list(range(744,768)))
for name,start,n in [('canal',720,72),('offering',1320,174)]:
    dest=Q/f'sample-{name}.mp4'
    subprocess.run([FF,'-y','-v','error','-framerate','24','-start_number',str(start),'-i',str(F/'%05d.png'),'-ss',str(start/24),'-i',str(P/'audio/final-mix-v14.wav'),'-frames:v',str(n),'-t',str(n/24),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(dest)],check=True)
(Q/'sample-evidence.json').write_text(json.dumps(records,indent=2),encoding='utf8')
print(json.dumps({'sheets':[r['path'] for r in records],'viewing':'pending','audio_perceived':False}))
