from pathlib import Path
import subprocess,json,hashlib,wave,sys
from PIL import Image,ImageDraw,ImageFont
import numpy as np
R=Path(__file__).resolve().parent;B=R.parent;O=B/'out/final-v19-mechanical-relief';sys.path.insert(0,str(B/'tools/python'))
import imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe();video=O/'video.mp4';e=json.loads((O/'evidence.json').read_text(encoding='utf-8'))
assert e['decoded'] and e['count']==3600 and e['duration']==120 and e['width']==1920 and e['height']==1080
assert e['sha256']==hashlib.sha256(video.read_bytes()).hexdigest()
times=[3,18,31,38,49,62,75,87.5,92,101.6,109,117];frames=[]
for t in times:
 d=O/f'decoded-{t}.jpg';subprocess.run([FF,'-v','error','-y','-threads','1','-ss',str(t),'-i',str(video),'-frames:v','1','-threads:v','1','-q:v','2',str(d)],check=True,timeout=30);frames.append((t,d))
w,h=480,270;im=Image.new('RGB',(1920,3*294),'#101e2c');draw=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
for i,(t,d) in enumerate(frames):
 x=i%4*w;y=i//4*294;im.paste(Image.open(d).convert('RGB').resize((w,h)),(x,y));draw.text((x+10,y+h+2),f'{t:.2f}s',font=font,fill='white')
im.save(O/'final-overview.jpg',quality=94)
with wave.open(str(R/'audio/mix.wav'),'rb') as wav:ref=np.frombuffer(wav.readframes(wav.getnframes()),'<i2').reshape(-1,2).astype(np.float32)/32768
pcm=subprocess.run([FF,'-v','error','-i',str(video),'-vn','-f','s16le','-ac','2','-ar','48000','-'],capture_output=True,check=True,timeout=60).stdout
audio=np.frombuffer(pcm,'<i2').reshape(-1,2).astype(np.float32)/32768;sync=[]
for at in [9.6,21.6,33.6,46.4,52,61.6,77.6,89.6,92.8,101.6,114.4]:
 k=round(at*48000);n=12000;a=ref[k:k+n,0];scores=[]
 for shift in range(-8,9):
  b=audio[k+shift:k+shift+n,0];scores.append((float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-12)),shift))
 corr,shift=max(scores);assert abs(shift)<=1 and corr>.96;sync.append(dict(time=at,lag_samples=shift,correlation=corr))
old=json.loads((R/'v18-preserved.json').read_text(encoding='utf-8'));preserved=all(hashlib.sha256((B/'v18'/f).read_bytes()).hexdigest()==h for f,h in old.items());assert preserved
data=dict(video_sha256=e['sha256'],duration=120,frames=3600,dimensions=[1920,1080],decode=True,audio_channels=2,sync=sync,decoded_overview=times,v18_preserved=preserved,actual_listening=False,full_normal_speed_playback=False,independent_review='No new cycle; historical budget used',observation='Pending actual final image inspection')
(O/'delivery-checks.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(data,ensure_ascii=False))
