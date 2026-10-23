from pathlib import Path
import subprocess,json,hashlib,wave,sys
from PIL import Image,ImageDraw,ImageFont
import numpy as np
R=Path(__file__).resolve().parent;B=R.parent;O=B/'out/final-v18-business-story'
sys.path.insert(0,str(B/'tools/python'))
import imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe();video=O/'video.mp4'
evidence=json.loads((O/'evidence.json').read_text(encoding='utf-8'))
assert evidence['decoded'] and evidence['count']==4620 and evidence['duration']==154
assert evidence['sha256']==hashlib.sha256(video.read_bytes()).hexdigest()
times=[2,8,15,21,26,31,35,40,44,49,56,66,74,80,88,96,101,107,117,122,128,134,141,151]
frames=[]
for t in times:
 dest=O/f'decoded-{t}.jpg'
 subprocess.run([FF,'-v','error','-y','-threads','1','-ss',str(t),'-i',str(video),'-frames:v','1','-threads:v','1','-q:v','2',str(dest)],check=True,timeout=30)
 frames.append((t,dest))
cols=4;w=480;h=270;rows=(len(frames)+cols-1)//cols
sheet=Image.new('RGB',(cols*w,rows*(h+24)),'#101e2c');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
for i,(t,dest) in enumerate(frames):
 im=Image.open(dest).convert('RGB').resize((w,h));x=i%cols*w;y=i//cols*(h+24);sheet.paste(im,(x,y));d.text((x+10,y+h+2),f'{t:.2f}s',font=font,fill='white')
sheet.save(O/'final-overview.jpg',quality=94)
with wave.open(str(R/'audio/mix.wav'),'rb') as wav:original=np.frombuffer(wav.readframes(wav.getnframes()),'<i2').reshape(-1,2).astype(np.float32)/32768
audio=subprocess.run([FF,'-v','error','-i',str(video),'-vn','-f','s16le','-ac','2','-ar','48000','-'],capture_output=True,check=True,timeout=60).stdout
decoded=np.frombuffer(audio,'<i2').reshape(-1,2).astype(np.float32)/32768;sync=[]
for at in [6,26.4,38,43.6,54.4,78.8,92.4,115.2,134.4,143.2,148.8]:
 k=round(at*48000);n=12000;ref=original[k:k+n,0];scores=[]
 for shift in range(-8,9):
  cand=decoded[k+shift:k+shift+n,0];scores.append((float(np.dot(ref,cand)/(np.linalg.norm(ref)*np.linalg.norm(cand)+1e-12)),shift))
 corr,shift=max(scores);assert abs(shift)<=1 and corr>.96;sync.append(dict(time=at,lag_samples=shift,correlation=corr))
base=json.loads((R/'original-video-continuity.json').read_text(encoding='utf-8'))
history={f:hashlib.sha256((B/'v16'/f).read_bytes()).hexdigest()==h for f,h in base['base_hashes'].items()};assert all(history.values())
v17=json.loads((R/'v17-preserved.json').read_text(encoding='utf-8'))
history.update({'v17/'+f:hashlib.sha256((B/'v17'/f).read_bytes()).hexdigest()==h for f,h in v17.items()});assert all(history.values())
report=dict(video_sha256=evidence['sha256'],frames=4620,size=[1920,1080],duration=154,decode=True,audio_channels=2,audio_sample_rate=48000,aac_alignment=sync,peak=float(np.max(np.abs(decoded))),actual_listening=False,independent_review='Historical budget already used; no new independent review',extracted_final_times=times,visual_observation='Pending actual final sheet inspection',original_preserved=history)
(O/'delivery-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(duration=154,frames=4620,decode=True,audio_sync=sync,overview=str(O/'final-overview.jpg'))))
