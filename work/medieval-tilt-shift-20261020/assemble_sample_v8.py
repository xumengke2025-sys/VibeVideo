from pathlib import Path
from PIL import Image,ImageStat,ImageDraw
import subprocess,json,hashlib
ROOT=Path(__file__).resolve().parent
FF=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
folder=ROOT/'render/sample-v8';video=ROOT/'delivery/移轴强化-v8-市集到运河-3秒样段.mp4'
for f in range(612,684):
 with Image.open(folder/f'{f:05d}.png') as im:
  assert im.size==(1080,1920);im.load()
  assert sum(ImageStat.Stat(im).mean)/3>1
subprocess.run([str(FF),'-y','-hide_banner','-loglevel','warning','-framerate','24','-start_number','612','-i',str(folder/'%05d.png'),'-ss','25.5','-i',str(ROOT/'audio/final-mix-v8.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-t','3','-movflags','+faststart',str(video)],check=True)
probe=json.loads(subprocess.check_output([str(FF.with_name('ffprobe.exe')),'-v','error','-show_streams','-show_format','-count_frames','-of','json',str(video)],text=True,encoding='utf8'))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert int(v['nb_read_frames'])==72 and a['channels']==2
canvas=Image.new('RGB',(6*180,3*350),'#15191c');draw=ImageDraw.Draw(canvas)
for j,f in enumerate(range(612,684,4)):
 im=Image.open(folder/f'{f:05d}.png');im.thumbnail((180,320));x=(j%6)*180;y=(j//6)*350;canvas.paste(im,(x,y));draw.text((x+4,y+322),f'{f/24:.3f}s',fill='white')
canvas.save(ROOT/'qa/v8/sample-contact.png')
report={'video':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'frames':72,'duration':3,'width':1080,'height':1920,'fps':24,'audio_channels':a['channels'],'audio_perceived':False,'model_sha256':hashlib.sha256((ROOT/'model/babylon-city-v8.blend').read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256((ROOT/'render_city_v8.py').read_bytes()).hexdigest(),'timeline_sha256':hashlib.sha256((ROOT/'v8-timeline.json').read_bytes()).hexdigest(),'contact':'qa/v8/sample-contact.png'}
(ROOT/'qa/v8/sample-engineering.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
