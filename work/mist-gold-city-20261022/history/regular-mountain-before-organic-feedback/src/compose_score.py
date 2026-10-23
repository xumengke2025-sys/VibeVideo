"""Original chamber-orchestral minuet in D, 40 bars, 90s. Sampled instruments.
No previous project's composition/audio is used. GeneralUser license in assets.
"""
from pathlib import Path
import sys,json,math,wave
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'vendor'));sys.path.insert(0,str(ROOT/'src'))
from tinysoundfont import Synth
from timeline import coach_x,coach_speed,bridge_angle
SR=48000;N=90*SR;rng=np.random.default_rng(221022);events=[];score=[]
def note(t,d,ch,p,v):
 if t<0 or t>=89:return
 events.extend([(round(t*SR),1,ch,int(p),int(v)),(min(N,round((t+d)*SR)),0,ch,int(p),0)]);score.append({'t':round(t,3),'duration':round(d,3),'channel':ch,'pitch':p,'velocity':v})
chords=[(50,[62,66,69]),(47,[59,62,66]),(43,[59,62,67]),(45,[61,64,69]),(50,[57,62,66]),(54,[61,66,69]),(43,[59,62,67]),(45,[57,61,64])]
melody=[[74,73,71,69,66,69],[71,69,66,64,62,66],[67,69,71,74,71,67],[69,73,76,73,69,73],[74,78,76,74,73,71],[73,71,69,66,69,73],[74,71,67,69,71,67],[69,66,64,61,64,69]]
beat=.75;bar=beat*3
for k in range(40):
 t=k*bar;root,triad=chords[k%8]
 if k>=36:root,triad=[(43,[59,62,67]),(45,[61,64,69]),(45,[61,64,69]),(50,[62,66,69])][k-36]
 vel=62 if k<5 else 52 if k<12 else 45 if k<18 else 43 if k<28 else 57 if k<34 else 72
 if k==39:
  for p in [50,57,62,66,69,74]:note(t,1.15,0,p,54)
  note(t,1.25,1,38,51);note(t,1.2,4,50,42);note(t,1.3,3,74,47);continue
 # Legato strings, moving cello, warm horn support reserved for reveal and ending.
 for j,p in enumerate(triad):note(t+j*.014,bar-.08,0,p,vel-j*3)
 note(t,beat*1.75,1,root-12,vel+3);note(t+beat*2,beat*.82,1,root-5,vel-5)
 if k<5 or k>=33:
  for p in [root,triad[1]]:note(t+.025,bar*.86,4,p,vel-14)
 # Harpsichord broken triads; slight expressive timing and voice-led turnaround.
 for j in range(6):
  if 19<=k<28 and j%2:continue
  p=triad[[0,1,2,1,2,1][j]]+(12 if j==4 and k%4==3 else 0);note(t+j*beat/2+.012*math.sin(k+j),.31,2,p,46 if k<18 else 35 if k<28 else 51)
 # Woodwind phrases, with breaths every fourth bar. Bridge passage uses longer values.
 if k<18 or k>=28:
  for j,p in enumerate(melody[k%8]):
   if k%4==3 and j>=4:continue
   note(t+j*beat/2+.04,.38 if j%2 else .43,3,p,vel+1)
 else:
  phrase=[74,78,76,73,74,71,69,73,74,76][k-18];note(t+.08,bar*.77,5,phrase,51)
 if 6<=k<16 or k>=30:note(t+beat,beat*.78,5,triad[1]+12,39);note(t+beat*2,beat*.75,5,triad[0]+12,35)
synth=Synth(gain=-14,samplerate=SR);sf=synth.sfload((ROOT/'assets/GeneralUser-GS.sf2').read_bytes(),max_voices=256)
for ch,program,pan in [(0,48,44),(1,42,74),(2,6,53),(3,68,78),(4,60,35),(5,73,67)]:synth.program_select(ch,sf,0,program);synth.control_change(ch,10,pan);synth.control_change(ch,7,100)
music=np.zeros((N,2),np.float32);cursor=0
for at,kind,ch,p,v in sorted(events):
 if at>cursor:music[cursor:at]=np.frombuffer(synth.generate(at-cursor),np.float32).reshape(-1,2);cursor=at
 if kind:synth.noteon(ch,p,v)
 else:synth.noteoff(ch,p)
if cursor<N:music[cursor:]=np.frombuffer(synth.generate(N-cursor),np.float32).reshape(-1,2)
dry=music.copy()
for sec,gain in [(.137,.09),(.227,.075),(.379,.06),(.571,.045),(.823,.033),(1.19,.019)]:n=round(sec*SR);music[n:]+=dry[:-n,::-1]*gain
tm=np.arange(N)/SR;music*=np.interp(tm,[0,.15,40,43,60,66,78,84,88.5,90],[.65,1,1,.78,.78,1,1.1,1.15,.8,0])[:,None]
music*=.65/max(np.max(np.abs(music)),1e-6)
foley=np.zeros((N,2),np.float32);sounds=[]
def noise(d,lo,hi):
 n=int(d*SR);a=rng.normal(0,1,n);f=np.fft.rfftfreq(n,1/SR);a=np.fft.irfft(np.fft.rfft(a)*(1-np.exp(-(f/lo)**2))/(1+(f/hi)**4),n);return a/(a.std()+1e-8)
def put(t,a,volume,pan=.5,label=None):
 start=round(t*SR);n=min(len(a),N-start)
 if n>0:foley[start:start+n]+=a[:n,None]*volume*np.array([math.cos(pan*math.pi/2),math.sin(pan*math.pi/2)])
 if label:sounds.append({'t':t,'duration':len(a)/SR,'kind':label})
water=noise(90,50,1800);water*=np.interp(tm,[0,20,28,40,65,78,90],[.1,.25,1,.75,.5,.2,.05])
put(0,water,.006,.6,'canal water bed')
def bell(t,freq,amp):
 s=np.arange(6*SR)/SR;a=np.zeros_like(s)
 for ratio,g,d in [(1,1,.9),(2.01,.42,1.1),(2.71,.25,1.3),(4.1,.12,1.8)]:a+=g*np.sin(math.tau*freq*ratio*s)*np.exp(-s*d)
 a*=np.minimum(s*250,1);put(t,a,amp,.30,'distant church bell')
for t,f,a in [(4.6,392,.045),(7.2,493.88,.025),(77,392,.025),(79.8,587.33,.018)]:bell(t,f,a)
# Horse impacts are derived from the same integrated coach distance, so stops are silent.
last=None
for t in np.arange(29,80,1/96):
 step=int((coach_x(t)+140)/.375)
 if step!=last and coach_speed(t)>.05:
  s=np.arange(int(.13*SR))/SR;a=(noise(.13,160,2300)*.7+.5*np.sin(math.tau*170*s))*np.exp(-s*48);put(float(t),a,.018,.38)
 last=step
sounds.append({'t':29,'duration':51,'kind':'distance-synchronised hoofbeats, silent while stopped'})
for start,end in [(44,49),(60,64)]:
 for t in np.arange(start,end,.23):
  s=np.arange(int(.18*SR))/SR;a=(np.sin(math.tau*1200*s)*.35+np.sin(math.tau*1837*s)*.2+noise(.18,500,5000)*.45)*np.exp(-s*35);put(float(t),a,.023,.52)
 sounds.append({'t':start,'duration':end-start,'kind':'bridge chain and ratchet'})
for t in [43.1,49,64,65.1]:
 s=np.arange(int(.45*SR))/SR;a=(noise(.45,50,1100)+.6*np.sin(math.tau*88*s))*np.exp(-s*17);put(t,a,.035,.47,'timber gate / bridge end stop')
for t in [28.4,33.9,42.3,61.8]:
 s=np.arange(int(1.5*SR))/SR;a=noise(1.5,800,6000)*np.sin(math.pi*s/1.5)**2;put(t,a,.014,.78,'brief steam vent')
foley*=np.interp(tm,[0,.3,87,90],[0,1,1,0])[:,None];mix=music+foley;mix*=.89/max(.89,np.max(np.abs(mix)))
def save(name,a):
 with wave.open(str(ROOT/'audio'/name),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
for name,a in [('music.wav',music),('foley.wav',foley),('final-mix.wav',mix)]:save(name,a)
(ROOT/'audio/score-notes.json').write_text(json.dumps(score,indent=2),encoding='utf8');(ROOT/'audio/sound-events.json').write_text(json.dumps(sounds,indent=2),encoding='utf8')
(ROOT/'audio/engineering.json').write_text(json.dumps({'duration':90,'sample_rate':SR,'channels':2,'peak':float(np.max(np.abs(mix))),'rms':float(np.sqrt(np.mean(mix**2))),'notes':len(score),'audio_listened':False,'method':'Original composition, GeneralUser GS sampled instruments; signal checks do not certify listening.'},indent=2),encoding='utf8');print('AUDIO_READY',len(score),flush=True)
