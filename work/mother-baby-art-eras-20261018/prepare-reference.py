from pathlib import Path
import hashlib, json, re, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
REF = PROJECT / 'reference-sources/upstream-videos/huashu-art-motion/art-motion-35-styles.mp4'
SOURCE = PROJECT / 'reference-sources/video-films-20261014/alchaincyf--huashu-art-motion/scripts/engine'
BIN = Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc')
INPUT = Path('D:/腾讯电脑管家文件搬家/xwechat_files/wxid_6965669652111_a61a/temp/RWTemp/2026-10/9e20f478899dc29eb19741386f9343c8')
NAMES = [
 ('mother-01.jpg','00b67f60e92b287827e1b476b4275e96.jpg'),
 ('mother-02.jpg','82c2bf271a99a159b726cd1688227246.jpg'),
 ('mother-03.jpg','81c9dce166e901634def65affaa47b00.jpg'),
 ('baby-01.jpg','46f7cdf8fc82c60a836977f9f6663059.jpg'),
 ('baby-02.jpg','ef2533f50e70e57718678803c60f5c85.jpg'),
 ('baby-03.jpg','df7c8a2aa70df5a2caf9fe44b02e4c27.jpg'),
]
def save(p, obj):
 p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
def digest(p):
 return hashlib.sha256(p.read_bytes()).hexdigest()

assets = ROOT / 'assets/references'
assets.mkdir(parents=True, exist_ok=True)
manifest=[]
for dst,src in NAMES:
 a,b=INPUT/src,assets/dst
 if not b.exists(): shutil.copy2(a,b)
 with Image.open(b) as im: size=im.size
 assert digest(a)==digest(b)
 manifest.append({'path':str(b),'original':str(a),'size':size,'sha256':digest(b),'user_provided':True})
save(assets/'manifest.json', manifest)

research=ROOT/'research'
frames=research/'reference-frames'
frames.mkdir(parents=True,exist_ok=True)
probe=json.loads(subprocess.check_output([str(BIN/'ffprobe.exe'),'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(REF)],text=True,timeout=120))
save(research/'reference-metadata.json',{'video':str(REF),'sha256':digest(REF),'probe':probe})
vs=next(s for s in probe['streams'] if s['codec_type']=='video')
total=int(vs['nb_read_frames'])
fps=int(vs['r_frame_rate'].split('/')[0])/int(vs['r_frame_rate'].split('/')[1])
if len(list(frames.glob('*.jpg')))!=total:
 subprocess.run([str(BIN/'ffmpeg.exe'),'-v','error','-y','-i',str(REF),'-vf','scale=576:324','-q:v','2','-start_number','0',str(frames/'%05d.jpg')],check=True,timeout=240)
files=sorted(frames.glob('*.jpg'))
assert len(files)==total
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14)
sheets=[]
for n in range(0,total,99):
 group=files[n:n+99]
 sheet=Image.new('RGB',(9*284,11*182),(246,239,227))
 d=ImageDraw.Draw(sheet)
 for j,p in enumerate(group):
  with Image.open(p) as im: im=im.resize((284,160),Image.Resampling.LANCZOS)
  x,y=(j%9)*284,(j//9)*182
  sheet.paste(im,(x,y)); k=n+j
  d.text((x+4,y+162),f'{k:04d} | {k/fps:06.3f}s',font=font,fill=(38,31,27))
 out=research/f'continuous-{n:04d}-{n+len(group)-1:04d}.jpg'
 sheet.save(out,quality=92)
 sheets.append({'path':str(out),'start_frame':n,'end_frame':n+len(group)-1,'actual_viewed':False})

raw=(SOURCE/'eras_gallery.js').read_text(encoding='utf-8')
parts=re.split(r"\{ id: '",raw)[1:]
eras=[]; t=0
for part in parts:
 sid=part.split("'",1)[0]
 name=re.search(r"name: '([^']+)'",part).group(1)
 year=int(re.search(r'year: (-?\d+)',part).group(1))
 eighths=int(re.search(r'eighths: (\d+)',part).group(1))
 dur=eighths*60/128/2
 eras.append({'id':sid,'name':name,'year':year,'source_t0':t,'source_t1':t+dur,'source_only_timing':True})
 t+=dur
save(research/'reference-style-order.json',eras)
save(research/'coverage.json',{'video_sha256':digest(REF),'source_resolution':[vs['width'],vs['height']],'extraction_resolution':[576,324],'fps':fps,'frame_count':total,'sheets':sheets,'actually_viewed_ranges':[],'realtime_playback':False,'audio_present':any(s['codec_type']=='audio' for s in probe['streams']),'note':'Extracted all frames; extraction is not evidence of actual visual inspection. Current source and release differ.'})
print(json.dumps({'input_photos':len(manifest),'frames':total,'fps':fps,'sheets':len(sheets),'styles':len(eras),'source_duration':t},ensure_ascii=False))
