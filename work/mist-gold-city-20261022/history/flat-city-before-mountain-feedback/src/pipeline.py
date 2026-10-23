"""Standalone project pipeline. sample -> full -> assemble; missing-frame resume.
Runtime executables can be supplied through BLENDER, FFMPEG, FFPROBE environment.
"""
from pathlib import Path
import os,sys,json,hashlib,subprocess,time,collections
from PIL import Image,ImageDraw
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
BLENDER=Path(os.environ.get('BLENDER',str(ROOT.parents[1]/'tools/blender-portable/blender-4.5.3-windows-x64/blender.exe')))
FF=Path(os.environ.get('FFMPEG','D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'));FP=Path(os.environ.get('FFPROBE',str(FF.with_name('ffprobe.exe'))))
MODE=sys.argv[1] if len(sys.argv)>1 else 'sample';VERSION=os.environ.get('FOG_VERSION','v1');OUT=ROOT/'render'/('frames-'+VERSION);OUT.mkdir(exist_ok=True);QA=ROOT/'qa'/VERSION;QA.mkdir(exist_ok=True)
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
inputs=['model/fog-gold-city.blend','src/render_film.py','src/timeline.py','src/geometry.py','audio/final-mix.wav'];manifest={'inputs':{p:digest(ROOT/p) for p in inputs},'samples':32,'width':1080,'height':1920,'fps':24,'duration':90,'frames':2160,'engine':'Cycles OptiX','compositor':'GPU fixed Gaussian layers with animated screen/depth CoC'}
mp=ROOT/'render'/('frozen-'+VERSION+'.json')
if mp.exists():assert json.loads(mp.read_text(encoding='utf8'))==manifest,'Inputs changed; use new FOG_VERSION, preserve old frames.'
else:mp.write_text(json.dumps(manifest,indent=2),encoding='utf8')
env=os.environ.copy();env.update(FOG_OUTPUT=str(OUT.relative_to(ROOT)),FOG_SAMPLES='32',FOG_PERCENT='100')
status={'mode':MODE,'version':VERSION,'started':time.time(),'completed':0,'target':0,'last_frame':None};statusfile=ROOT/'render/status.json'
def status_save():status['updated']=time.time();statusfile.write_text(json.dumps(status,indent=2),encoding='utf8')
def run_frames(frames,label):
 if not frames:return
 logdir=ROOT/'render'/('logs-'+VERSION);logdir.mkdir(exist_ok=True);tail=collections.deque(maxlen=25)
 args=['range',str(frames[0]),str(frames[-1]+1)] if frames==list(range(frames[0],frames[-1]+1)) else ['stills']+[str(f) for f in frames]
 with (logdir/(label+'.log')).open('a',encoding='utf8') as log:
  p=subprocess.Popen([str(BLENDER),'--background','--python-exit-code','1','--python',str(ROOT/'src/render_film.py'),'--']+args,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf8',errors='replace');status['blender_pid']=p.pid;status_save()
  for line in p.stdout:
   tail.append(line)
   if any(s in line for s in ['FRAME_READY','Error','Traceback','out of memory']):log.write(line);log.flush()
   if line.startswith('FRAME_READY'):
    status['completed']+=1;status['last_frame']=int(line.split()[1]);status['last_render_seconds']=float(line.split()[2]);status_save()
    if status['completed']%24==0:print('PROGRESS',status['completed'],'/',status['target'],'frame',status['last_frame'],flush=True)
  p.wait()
  if p.returncode:log.write(''.join(tail));raise RuntimeError('Blender exit '+str(p.returncode))
def assemble(start,end,name):
 dur=(end-start)/24;video=ROOT/'delivery'/name
 subprocess.run([str(FF),'-y','-hide_banner','-loglevel','warning','-framerate','24','-start_number',str(start),'-i',str(OUT/'%05d.png'),'-ss',str(start/24),'-i',str(ROOT/'audio/final-mix.wav'),'-map','0:v:0','-map','1:a:0','-frames:v',str(end-start),'-t',str(dur),'-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-threads:v','2','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',str(video)],check=True)
 probe=json.loads(subprocess.check_output([str(FP),'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)],text=True,encoding='utf8'));vs=next(s for s in probe['streams'] if s['codec_type']=='video');au=next(s for s in probe['streams'] if s['codec_type']=='audio');decode=subprocess.run([str(FF),'-v','error','-i',str(video),'-c:v','rawvideo','-c:a','pcm_s16le','-f','null','NUL'],capture_output=True,text=True,encoding='utf8')
 report={'path':str(video),'sha256':digest(video),'width':vs['width'],'height':vs['height'],'fps':vs['r_frame_rate'],'frames':int(vs['nb_read_frames']),'duration':float(probe['format']['duration']),'channels':au['channels'],'sample_rate':au['sample_rate'],'decode_exit':decode.returncode,'decode_errors':decode.stderr,'audio_listened':False}
 assert (report['width'],report['height'],report['fps'],report['frames'])==(1080,1920,'24/1',end-start)
 assert abs(report['duration']-dur)<.05 and report['channels']==2 and decode.returncode==0
 (QA/(video.stem+'-engineering.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print('VIDEO_READY',str(video),flush=True);return video
if MODE in ['sample','full']:
 frames=list(range(960,1728)) if MODE=='sample' else list(range(2160));status['target']=len(frames);status['completed']=sum((OUT/f'{f:05d}.png').exists() for f in frames);status_save()
 for a in range(0,len(frames),48):
  batch=frames[a:a+48];missing=[f for f in batch if not (OUT/f'{f:05d}.png').exists()]
  for attempt in range(2):
   try:run_frames(missing,'%05d-%05d'%(batch[0],batch[-1]));break
   except RuntimeError:
    if attempt:raise
    missing=[f for f in batch if not (OUT/f'{f:05d}.png').exists()]
  for f in batch:
   with Image.open(OUT/f'{f:05d}.png') as im:assert im.size==(1080,1920);im.verify()
 status['state']='encoding';status_save();assemble(frames[0],frames[-1]+1,'雾金之城-升桥样段-'+VERSION+'.mp4' if MODE=='sample' else '雾金之城-'+VERSION+'.mp4');status['state']='complete';status_save()
elif MODE=='assemble':assemble(0,2160,'雾金之城-'+VERSION+'.mp4')
elif MODE=='sheets':
 frames=list(range(960,1728,24));tw,th=180,320
 for a in range(0,len(frames),12):
  sub=frames[a:a+12];sheet=Image.new('RGB',(4*tw,3*(th+25)),(25,28,29));draw=ImageDraw.Draw(sheet)
  for k,f in enumerate(sub):
   with Image.open(OUT/f'{f:05d}.png') as im:im=im.resize((tw,th));x=k%4*tw;y=k//4*(th+25);sheet.paste(im,(x,y));draw.text((x+4,y+th+4),f'{f/24:.2f}s / f{f}',fill='white')
  sheet.save(QA/('sample-sheet-%02d.jpg'%(a//12)),quality=93)
