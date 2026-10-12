"""Decode every video frame and create numbered, gap-free visual evidence sheets."""
import argparse,json,hashlib,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('--out',required=True);a=p.parse_args()
video=Path(a.video).resolve();out=Path(a.out).resolve();frames=out/'decoded';sheets=out/'sheets';frames.mkdir(parents=True,exist_ok=True);sheets.mkdir(exist_ok=True)
ff=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe');probe=ff.with_name('ffprobe.exe')
meta=json.loads(subprocess.check_output([str(probe),'-v','error','-show_streams','-show_format','-of','json',str(video)]));v=next(s for s in meta['streams'] if s['codec_type']=='video');num,den=map(int,v['r_frame_rate'].split('/'));fps=num/den
subprocess.run([str(ff),'-v','error','-y','-i',str(video),'-map','0:v:0','-q:v','3','-start_number','0',str(frames/'%05d.jpg')],check=True)
subprocess.run([str(ff),'-v','error','-y','-i',str(video),'-map','0:a:0','-c:a','pcm_s16le',str(out/'audio.wav')],check=True)
files=sorted(frames.glob('*.jpg'));items=[];tw,th,cols,rows=216,384,6,5
for base in range(0,len(files),cols*rows):
 batch=files[base:base+cols*rows];sheet=Image.new('RGB',(tw*cols,(th+24)*rows),'#dddcd3');d=ImageDraw.Draw(sheet)
 for i,f in enumerate(batch):
  im=Image.open(f);im.thumbnail((tw,th));x=(i%cols)*tw;y=(i//cols)*(th+24);sheet.paste(im,(x,y));d.text((x+4,y+th+3),f'{base+i:04d} | {(base+i)/fps:06.2f}s',fill='#172c28')
 name=sheets/f'{base:05d}-{base+len(batch)-1:05d}.jpg';sheet.save(name,quality=92);items.append({'start':base,'end':base+len(batch)-1,'path':str(name),'sha256':hashlib.sha256(name.read_bytes()).hexdigest()})
index={'video':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'fps':fps,'count':len(files),'audio':str(out/'audio.wav'),'sheets':items,'decoded_dir':str(frames)}
(out/'index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'frames':len(files),'sheets':len(items),'index':str(out/'index.json'),'sha256':index['sha256']},ensure_ascii=False))
