"""Eight-second D-minor pickup, followed by the retained 52-second body score."""
from pathlib import Path
import wave,json,hashlib
import numpy as np
R=Path(__file__).resolve().parent
SR=48000
def read(p):
 with wave.open(str(p),'rb') as w:
  assert w.getframerate()==SR and w.getnchannels()==2
  return np.frombuffer(w.readframes(w.getnframes()),'<i2').reshape(-1,2).astype(np.float32)/32768
def save(p,a):
 with wave.open(str(p),'wb') as w:
  w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.rint(np.clip(a,-1,1)*32767).astype('<i2').tobytes())
retained=R/'audio/retained-v10.wav'
if not retained.exists():retained.write_bytes((R.parent/'v10/audio/mix.wav').read_bytes())
out=np.zeros((60*SR,2),np.float32);out[8*SR:]=read(retained)
rng=np.random.default_rng(20261021);ledger=[]
def add(at,a,gain=1,pan=0,kind=''):
 k=round(at*SR);n=min(len(a),len(out)-k)
 if n<=0:return
 out[k:k+n,0]+=a[:n]*gain*np.cos((pan+1)*np.pi/4)
 out[k:k+n,1]+=a[:n]*gain*np.sin((pan+1)*np.pi/4)
 if kind:ledger.append(dict(at=at,sample=k,kind=kind))
def pluck(note,length=.6):
 t=np.arange(round(SR*length))/SR;f=440*2**((note-69)/12)
 return (np.sin(2*np.pi*f*t)+.23*np.sin(4*np.pi*f*t))*(1-np.exp(-t/.003))*np.exp(-t*8)*.16
def kick():
 t=np.arange(round(SR*.4))/SR
 return np.sin(2*np.pi*(48*t+2*(1-np.exp(-t/.025))))*np.exp(-t*13)*np.minimum(t/.002,1)*.26
for i in range(20):
 at=i*.4
 add(at,kick(),gain=.8 if i>=10 else .6,kind='150bpm-kick')
 add(at+.1,pluck([74,77,81,76,77,74,81,77][i%8]),.7 if i>=10 else .4,pan=(-.25 if i%2 else .25),kind='arpeggio')
 t=np.arange(round(SR*.065))/SR;n=rng.normal(0,1,len(t));n-=np.convolve(n,np.ones(9)/9,'same')
 add(at+.2,n*np.exp(-t*70)*.025,.65,pan=.2,kind='hat')
 if i%2==0:add(at,pluck([38,38,34,41,36][i//4],.7),1.5,kind='bass')
for i in range(4):add(.1+i*.21,pluck(86-i*2,.2),.8,kind='pain-marker')
add(4,kick(),.9,kind='cards-open');add(6.4,pluck(86,.8),1,kind='card-extract')
out[:8*SR]*=(np.minimum(np.arange(8*SR)/(SR*.03),1)*np.minimum((8*SR-1-np.arange(8*SR))/(SR*.07),1))[:,None]
for at in [8,10.7]:add(at,pluck(81 if at==8 else 86,.3),.32,kind='card-handoff')
assert np.max(np.abs(out))<.99
save(R/'audio/mix.wav',out)
timing=json.loads((R.parent/'v10/audio/timing.json').read_text(encoding='utf-8'))
for e in timing.get('action_sync',[]):e['visual_seconds']+=8;e['audio_sample']+=8*SR
timing.update(duration=60,prefix_seconds=8,prefix_bpm=150,prefix_events=ledger,listening_verified=False,mix_sha256=hashlib.sha256((R/'audio/mix.wav').read_bytes()).hexdigest(),peak=float(np.max(np.abs(out))))
(R/'audio/timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(duration=60,channels=2,sample_rate=SR,peak=float(np.max(np.abs(out))),opening_events=len(ledger))))
