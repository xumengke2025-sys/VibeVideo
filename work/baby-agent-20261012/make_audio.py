"""Original short jazz cue, additive/FM timbres and original material foley.
No external music, voice cloning or instrument samples. 32 bars at 128 BPM.
"""
import json,wave,math
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parent;out=R/'audio';out.mkdir(exist_ok=True)
E=json.loads((R/'events.json').read_text(encoding='utf8'));sr=48000;N=sr*60
music=np.zeros((N,2),dtype=np.float32);fx=np.zeros_like(music);rng=np.random.default_rng(73)
bt=60/E['bpm'];bar=bt*4
def put(buf,t,a,vol=1,pan=0):
 k=max(0,round(t*sr));n=min(len(a),N-k)
 if n<=0:return
 buf[k:k+n,0]+=a[:n]*vol*math.sqrt((1-pan)/2);buf[k:k+n,1]+=a[:n]*vol*math.sqrt((1+pan)/2)
def env(tt,d,attack=.008,release=.08):
 return np.minimum(tt/attack,1)*np.where(tt<d,1,np.exp(-(tt-d)*6/release))*np.minimum((d+release-tt)/.006,1).clip(0,1)
def horn(m,d,vel=.07):
 tt=np.arange(int((d+.085)*sr))/sr;f=440*2**((m-69)/12)
 v=.002*np.sin(TAU*5.2*tt)*np.minimum(tt/.15,1);phase=TAU*f*np.cumsum(1+v)/sr
 a=sum(np.sin(h*phase+.10*h)*(.64**(h-1))/h**.35 for h in range(1,9))
 return (a*env(tt,d,.014,.085)*vel).astype('f4')
def bass(m,d):
 tt=np.arange(int((d+.07)*sr))/sr;f=440*2**((m-69)/12)
 a=(np.sin(TAU*f*tt)+.35*np.sin(TAU*2*f*tt)+.16*np.sin(TAU*3*f*tt))*np.exp(-tt*4.8)*(1-np.exp(-tt*180))
 return (a*env(tt,d,.005,.07)*.11).astype('f4')
def vibe(m,d,vol=.06):
 tt=np.arange(int((d+.55)*sr))/sr;f=440*2**((m-69)/12)
 a=np.sin(TAU*f*tt+1.2*np.sin(TAU*3*f*tt)*np.exp(-tt*9))
 a*=np.exp(-tt*3.7)*(1-np.exp(-tt*160))*(.85+.15*np.cos(TAU*6*tt))
 return (a*vol).astype('f4')
def drum(kind):
 dur={'kick':.16,'brush':.12,'hat':.065,'bongo':.13}[kind];tt=np.arange(int(dur*sr))/sr
 noise=rng.standard_normal(len(tt))
 if kind=='kick':a=np.sin(TAU*(57*tt+3*(1-np.exp(-tt*38))))*np.exp(-tt*32)*.10
 elif kind=='brush':a=(noise-np.roll(noise,1))*.018*np.exp(-tt*31)*(1-np.exp(-tt*170))
 elif kind=='hat':a=(noise-np.roll(noise,1))*.007*np.exp(-tt*70)
 else:a=np.sin(TAU*(220*tt+2*(1-np.exp(-tt*70))))*np.exp(-tt*28)*.035
 return a.astype('f4')
TAU=math.pi*2
chords=[([38,45,48,52],[62,65,69,72]),([43,50,53,57],[62,65,67,70]),([45,52,55,61],[61,64,67,69]),([38,45,48,52],[62,65,69,72])]
motif=[(0,69,.65),(.75,72,.20),(1.25,74,.28),(2,77,.30),(2.5,76,.22),(3.25,72,.27)]
for b in range(32):
 t=b*bar;low,high=chords[(b//2)%4]
 quiet=14<=b<18 or b>=28
 for k in range(4):
  put(music,t+k*bt,bass(low[k],bt*.72),.75 if quiet else 1,-.1)
  put(music,t+k*bt,drum('kick'),.45 if quiet else .8)
  if k in [1,3]:put(music,t+k*bt,drum('brush'),.5 if quiet else 1,.15)
  put(music,t+(k+.65)*bt,drum('hat'),.45 if quiet else .85,.35)
  if 8<=b<14:put(music,t+(k+.5)*bt,drum('bongo'),.7,-.4)
 # Motif alternates vibraphone and a soft brass voice, never famous spy-theme notes.
 for off,n,d in motif:
  nn=n+(0 if b<8 else (-2 if b<16 else (3 if b<24 else 0)))
  if b%2==0 or quiet:put(music,t+off*bt,vibe(nn,d*bt),.85,-.25)
  elif b%4==1:put(music,t+off*bt,horn(nn,d*bt,.045),.8,.20)
 # Light syncopated chord answers and stronger scene boundaries.
 if not quiet and b%2==1:
  for off in [1.5,3.0]:
   for n in high[:3]:put(music,t+off*bt,horn(n,.10,.025),1,.15)
for t in E['scenes'][:-1]:
 for n in [50,62,65,69]:put(music,t,horn(n,.18,.035),1,(n-62)/35)
for t in [56.25,57.1875,58.125]:
 for n in [50,62,65,69,76]:put(music,t,vibe(n,.8,.03),1,(n-62)/35)
def foley(kind):
 d={'paper':.38,'slap':.12,'tap':.14,'quack':.24}[kind];tt=np.arange(int(d*sr))/sr
 if kind=='paper':
  n=rng.standard_normal(len(tt));n=np.convolve(n,np.ones(8)/8,'same');a=n*.085*np.sin(np.pi*tt/d)**2
 elif kind=='slap':a=rng.standard_normal(len(tt))*.075*np.exp(-tt*70)+np.sin(TAU*180*tt)*.08*np.exp(-tt*48)
 elif kind=='tap':a=np.sin(TAU*760*tt)*.08*np.exp(-tt*35)+np.sin(TAU*1400*tt)*.015*np.exp(-tt*40)
 else:
  f=380-190*(tt/d);ph=TAU*np.cumsum(f)/sr
  a=(np.sin(ph)+.5*np.sin(2*ph)+.25*np.sin(4*ph))*np.sin(np.pi*tt/d)**1.5*.07
 return a.astype('f4')
for ev in E['foley']:put(fx,ev['t'],foley(ev['kind']),ev['gain'],.15)
mix=music+fx
# Exact intentional stop-time, all tails included. 5ms boundary fades avoid clicks.
a,b=E['stop_time'];ia,ib=round(a*sr),round(b*sr)
fade=240;mix[ia-fade:ia]*=np.linspace(1,0,fade)[:,None];mix[ia:ib]=0;mix[ib:ib+fade]*=np.linspace(0,1,fade)[:,None]
mix[:2400]*=np.linspace(0,1,2400)[:,None];mix[-24000:]*=np.linspace(1,0,24000)[:,None]
peak=float(np.max(np.abs(mix)));gain=min(1.5,.88/max(.01,peak));mix*=gain
for name,buf in [('music',music),('foley',fx),('mix',mix)]:
 with wave.open(str(out/(name+'.wav')),'wb') as w:
  w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(buf,-1,1)*32767).astype('<i2').tobytes())
(out/'audio-info.json').write_text(json.dumps({'duration':60,'sample_rate':sr,'bpm':128,'bars':32,'music':'Original programmed short jazz cue with synthesized instrument timbres','external_samples':False,'voice':False,'intentional_silence':[a,b],'peak':float(np.max(np.abs(mix))),'rms':float(np.sqrt(np.mean(mix**2)))},indent=2),encoding='utf8')
print('Audio complete',flush=True)
