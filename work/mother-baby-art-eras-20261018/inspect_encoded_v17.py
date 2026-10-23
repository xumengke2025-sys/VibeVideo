from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
FF=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
source=R/'out/outside-life-sample-v17.mp4'
dest=R/'qa/v17/sample';dest.mkdir(parents=True,exist_ok=True)
subprocess.run([str(FF),'-v','error','-y','-i',str(source),'-frames:v','144',str(dest/'encoded-%03d.png')],check=True,timeout=180)
frames=sorted(dest.glob('encoded-[0-9][0-9][0-9].png'))
assert len(frames)==144,len(frames)
def sheet(name,ids,box,size):
 w,h=size;result=Image.new('RGB',(w*4,(h+24)*((len(ids)+3)//4)),'#f4ead8');draw=ImageDraw.Draw(result)
 for k,n in enumerate(ids):
  with Image.open(frames[n]) as im:thumb=im.convert('RGB').crop(box).resize(size)
  x=k%4*w;y=k//4*(h+24);result.paste(thumb,(x,y+24));draw.text((x+6,y+5),f'{30+n/24:.3f}s | frame {n}',fill='#342b23')
 result.save(dest/name)
seen=list(range(0,144,4));env=list(range(0,144,6))
sheet('encoded-actor-sheet.png',seen,(205,1000,855,1560),(360,310))
sheet('encoded-outside-sheet.png',env,(0,0,1080,1000),(360,333))
cuts={32:list(range(42,55)),34:list(range(90,103))}
for cut,ids in cuts.items():sheet(f'encoded-cut-{cut}-sheet.png',ids,(0,0,1080,1920),(280,498))
coverage={'source':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'decoded_frames':len(frames),'interval_seconds':[30,36],'actor_sample_frames':seen,'environment_sample_frames':env,'transition_sample_frames':cuts,'capture':'Decoded MP4 samples for production inspection; exporting sheets does not imply viewing; not normal-speed playback or a full independent review'}
(dest/'coverage.json').write_text(json.dumps(coverage,indent=2),encoding='utf8')
print(json.dumps({'decoded':len(frames),'actor_samples':len(seen),'environment_samples':len(env),'cut_samples':sum(map(len,cuts.values()))}))
