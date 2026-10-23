"""Measured musical energy and onset candidates, not a claim of listening."""
from pathlib import Path
import subprocess, io, wave, json
import numpy as np
ROOT=Path(__file__).resolve().parent
FF=Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
src=ROOT/'audio/user-provided-Dream-Of-Babylon.mp3'
b=subprocess.check_output([str(FF),'-v','error','-i',str(src),'-ac','1','-ar','22050','-c:a','pcm_s16le','-f','wav','pipe:1'])
with wave.open(io.BytesIO(b)) as w:
    x=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
sr=22050; hop=2205; win=4410
rms=np.array([np.sqrt(np.mean(x[i:i+win]**2)) for i in range(0,len(x)-win,hop)])
db=20*np.log10(np.maximum(rms,1e-7))
energy=np.convolve(rms,np.ones(20)/20,mode='same')
# Keep enough source after the entry; favor a strong opening with a sustained phrase.
candidates=[]
for i in range(30,len(rms)-560):
    if energy[i]>=max(energy[max(0,i-20):i+21]):
        score=float(energy[i]*.6+np.mean(energy[i:i+560])*.4)
        candidates.append((score,i/10))
candidates.sort(reverse=True)
selected=candidates[0][1] if candidates else 0
# Select a nearby positive energy attack before the sustained maximum.
onset=np.maximum(0,np.diff(db,prepend=db[0]))
center=int(selected*10);lo=max(0,center-25);hi=min(len(onset),center+6)
start=(lo+int(np.argmax(onset[lo:hi])))/10
events=[0.]
for target in [8,17,26,35,45,52]:
    lo=int((start+target-1.2)*10);hi=int((start+target+1.2)*10)
    j=lo+int(np.argmax(onset[lo:hi]))
    events.append(round(j/10-start,3))
report={'source':str(src),'duration':len(x)/sr,'analysis':'0.1s RMS, 2s smoothing, positive dB changes; energy/onset proxy only, no auditory verification',
        'strong_entry_candidates':candidates[:8],'excerpt_start':start,'excerpt_end':start+56,
        'visual_cues_seconds':events,'audio_perceived':False}
(ROOT/'audio/music-structure-v8.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=True),flush=True)
