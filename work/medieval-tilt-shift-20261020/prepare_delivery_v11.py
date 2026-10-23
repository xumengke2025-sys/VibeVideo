"""Extract current encoded-film evidence; does not claim it was viewed/heard."""
from pathlib import Path
import hashlib,json,subprocess,math,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent;QA=ROOT/'qa/v11'
FF=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
sample='--sample' in sys.argv
if sample:
 video=ROOT/'delivery/v11-街景修复样段.mp4'
 dest=QA/'sample-encoded';dest.mkdir(exist_ok=True)
 subprocess.run([str(FF),'-y','-v','error','-i',str(video),'-vsync','0',str(dest/'%05d.png')],check=True)
 frames=list(range(72));paths=[dest/f'{i+1:05d}.png' for i in frames]
else:
 engineering=json.loads((ROOT/'delivery/engineering-check-v11.json').read_text(encoding='utf8'))
 video=Path(engineering['video']);assert hashlib.sha256(video.read_bytes()).hexdigest()==engineering['sha256']
 frames=[0,12,48,96,168,288,384,504,576,647,648,756,875,876,972,1067,1068,1176,1283,1284,1392,1492,1493,1560,1622,1623,1752,1800,1823]
 dest=QA/'encoded-frames';dest.mkdir(exist_ok=True);paths=[]
 for f in frames:
  path=dest/f'{f:05d}.png';paths.append(path)
  subprocess.run([str(FF),'-y','-v','error','-ss',f'{f/24:.9f}','-i',str(video),'-map','0:v:0','-frames:v','1',str(path)],check=True)
manifest=[]
for f,path in zip(frames,paths):
 assert path.exists()
 manifest.append({'frame':f+588 if sample else f,'seconds':(f+588 if sample else f)/24,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
size=24 if sample else 6;columns=6 if sample else 3;tw=180 if sample else 270;th=round(tw*16/9);sheets=[]
for start in range(0,len(manifest),size):
 part=manifest[start:start+size];out=Image.new('RGB',(columns*tw,math.ceil(len(part)/columns)*(th+25)),'#202020');draw=ImageDraw.Draw(out)
 for i,item in enumerate(part):
  with Image.open(item['path']) as im:
   im=im.convert('RGB');im.thumbnail((tw,th));x=i%columns*tw;y=i//columns*(th+25);out.paste(im,(x,y+25));draw.text((x+5,y+5),f"f{item['frame']:04d} | {item['seconds']:.3f}s",fill='white')
 path=QA/f"{'sample' if sample else 'film'}-sheet-{start//size:02d}.jpg";out.save(path,quality=94);sheets.append(str(path))
report={'video':str(video),'video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'method':'Evidence extraction only; viewing is recorded separately.','extracted_frames':manifest,'contact_sheets':sheets,'actual_viewed_frames':[],'audio_perceived':False,'independent_review':False}
path=QA/('sample-encoded-evidence.json' if sample else 'producer-evidence-v11.json');path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'frames':len(frames),'sheets':sheets},ensure_ascii=False))
