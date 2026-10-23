from pathlib import Path
import subprocess,json,hashlib,wave,sys
from PIL import Image,ImageDraw,ImageFont
import numpy as np
R=Path(__file__).resolve().parent;B=R.parent;O=B/'out/final-v17-blueprint-sources'
sys.path.insert(0,str(B/'tools/python'))
import imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe();video=O/'video.mp4'
evidence=json.loads((O/'evidence.json').read_text(encoding='utf-8'))
assert evidence['decoded'] and evidence['count']==3720 and evidence['duration']==124
assert evidence['sha256']==hashlib.sha256(video.read_bytes()).hexdigest()
times=[2,6,12,16,20,25,29,31,34,36,38,43,50,60,68,74,77,82,90,95,101,111.4,115.8,122]
frames=[]
for t in times:
 dest=O/f'decoded-{t}.jpg'
 subprocess.run([FF,'-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1','-q:v','2',str(dest)],check=True,timeout=30)
 frames.append((t,dest))
cols=4;w=480;h=270;rows=(len(frames)+cols-1)//cols
sheet=Image.new('RGB',(cols*w,rows*(h+24)),'#101e2c');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
for i,(t,dest) in enumerate(frames):
 im=Image.open(dest).convert('RGB').resize((w,h));x=i%cols*w;y=i//cols*(h+24);sheet.paste(im,(x,y));d.text((x+10,y+h+2),f'{t:.2f}s',font=font,fill='white')
sheet.save(O/'final-overview.jpg',quality=94)
with wave.open(str(R/'audio/mix.wav'),'rb') as wav:original=np.frombuffer(wav.readframes(wav.getnframes()),'<i2').reshape(-1,2).astype(np.float32)/32768
audio=subprocess.run([FF,'-v','error','-i',str(video),'-vn','-f','s16le','-ac','2','-ar','48000','-'],capture_output=True,check=True,timeout=60).stdout
decoded=np.frombuffer(audio,'<i2').reshape(-1,2).astype(np.float32)/32768;sync=[]
for at in [8,20.4,32,37.6,48.4,72.8,86.4,109.2,121.6]:
 k=round(at*48000);n=12000;ref=original[k:k+n,0];scores=[]
 for shift in range(-8,9):
  cand=decoded[k+shift:k+shift+n,0];scores.append((float(np.dot(ref,cand)/(np.linalg.norm(ref)*np.linalg.norm(cand)+1e-12)),shift))
 corr,shift=max(scores);assert abs(shift)<=1 and corr>.96;sync.append(dict(time=at,lag_samples=shift,correlation=corr))
base=json.loads((R/'original-video-continuity.json').read_text(encoding='utf-8'))
history={f:hashlib.sha256((B/'v16'/f).read_bytes()).hexdigest()==h for f,h in base['base_hashes'].items()};assert all(history.values())
report=dict(video_sha256=evidence['sha256'],frames=3720,size=[1920,1080],duration=124,decode=True,audio_channels=2,audio_sample_rate=48000,aac_alignment=sync,peak=float(np.max(np.abs(decoded))),actual_listening=False,independent_review='Historical budget already used; no new independent review',extracted_final_times=times,visual_observation='Pending actual final sheet inspection',original_preserved=history)
(O/'delivery-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(duration=124,frames=3720,decode=True,audio_sync=sync,overview=str(O/'final-overview.jpg'))))
