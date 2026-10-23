from pathlib import Path
import sys,json,math,wave
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'python-deps'))
from tinysoundfont import Synth
SR=48000; N=SR*60; rng=np.random.default_rng(18150618)
timeline=json.loads((ROOT/'events.json').read_text())
events=[]
def note(t,d,ch,p,v):
 if 0<=t<60:
  events.append((round(t*SR),'on',ch,int(p),int(v)))
  events.append((min(N,round((t+d)*SR)),'off',ch,int(p),0))
# Original minor-key motif and orchestration. Instruments are licensed sampled
# GeneralUser GS programs, not oscillators masquerading as an orchestra.
chords=[[38,45,50,53],[34,41,46,50],[31,38,43,46],[33,40,45,49]]
for start,end,step,vel in [(0,14,3.5,44),(14,26,3,61),(26,35,2.25,54),(35,45.5,2.625,91),(50,60,5,36)]:
 for k,t in enumerate(np.arange(start,end,step)):
  chord=chords[k%4]
  if start==26:chord=chords[(k+2)%4]
  dur=min(step+.3,end-t)
  for p in chord[1:]:note(t,dur,0,p+12,vel)
  note(t,dur,1,chord[0]+12,max(30,vel-8))
  note(t,dur,2,chord[0],max(28,vel-16))
  if start==35:
   for p in chord[1:]:note(t,dur-.2,4,p+12,vel-15)
   note(t,dur-.2,5,chord[0]+24,vel-18)
  if start==26:note(t,dur,7,chord[2]+12,42)
# A single continuous thematic arc, with tension altered in the middle section.
motif=[(0,62,1.45),(1.5,69,.9),(2.5,65,.95),(3.5,64,.9),(4.5,62,2.2),(7,60,.8),(8,61,1.5)]
for base,scale,vel,transpose in [(4,1,46,-12),(15,.85,68,0),(27,.8,55,-12),(35,1.1,99,0)]:
 for off,p,d in motif:
  if base+off*scale<45.5:note(base+off*scale,d*scale,3,p+transpose,vel)
for t in np.arange(14,25.8,.375):
 k=int((t-14)/3)%4; c=chords[k]
 note(t,.23,0,c[1+int((t-14)/.375)%3]+12,51+(int(t*8)%3)*4)
for t in np.arange(35,45.45,.25):
 c=chords[int((t-35)/2.625)%4]
 note(t,.18,7,c[1+int((t-35)*4)%3]+24,64+(int(t*4)%4)*5)
for t in np.arange(4,14,.75):note(t,.14,9,38,42 if int(t/.75)%2 else 58)
for t in np.arange(14,26,.375):note(t,.10,9,38,49 if int(t/.375)%2 else 67)
for t in np.arange(28,35,.75):note(t,.12,9,38,46)
for t in np.arange(35,45.45,.375):
 note(t,.15,9,38,72 if int(t/.375)%2 else 87)
 if int((t-35)/.375)%4==0:note(t,1.3,6,38,95)
for t in [6,14,20,26,35,40.25,43]:note(t,2.2,6,38 if t!=26 else 33,74 if t<35 else 105)
for t in [35,40.25,43]:note(t,1.5,9,49,57)
for p,d,off in [(62,2.4,0),(60,2,2.5),(57,3,4.5)]:note(50+off,d,1,p-12,38)
synth=Synth(gain=-13,samplerate=SR)
sf=synth.sfload((ROOT/'audio-assets/GeneralUser-GS.sf2').read_bytes(),max_voices=384)
programs={0:48,1:42,2:43,3:60,4:57,5:56,6:47,7:44}
for ch,p in programs.items():synth.program_select(ch,sf,0,p)
synth.program_select(9,sf,128,0,is_drums=True)
for ch,pan in [(0,45),(1,78),(2,64),(3,90),(4,30),(5,80),(6,54),(7,65),(9,60)]:
 synth.control_change(ch,10,pan);synth.control_change(ch,7,100)
music=np.zeros((N,2),np.float32);cursor=0
for at,kind,ch,p,v in sorted(events,key=lambda e:(e[0],e[1]=='on')):
 if at>cursor:
  music[cursor:at]=np.frombuffer(synth.generate(at-cursor),np.float32).reshape(-1,2);cursor=at
 if kind=='on':synth.noteon(ch,p,v)
 else:synth.noteoff(ch,p)
if cursor<N:music[cursor:]=np.frombuffer(synth.generate(N-cursor),np.float32).reshape(-1,2)
time=np.arange(N)/SR
env=np.interp(time,[0,.8,14,35,45.5,45.8,46.2,48,50,54,57,60],[.3,.8,.92,1,1,.08,.03,.01,.65,.55,.26,0])
music*=env[:,None]
# A diffuse stereo concert-hall tail; no copyrighted music is incorporated.
reverb=music.copy()
for delay,gain in [(.137,.10),(.223,.10),(.373,.075),(.521,.055),(.797,.036),(1.103,.025)]:
 n=int(delay*SR);reverb[n:]+=music[:-n,::-1]*gain
music=reverb
foley=np.zeros((N,2),np.float32)
def filtered_noise(d,lo,hi):
 n=int(d*SR);a=rng.normal(0,1,n);f=np.fft.rfftfreq(n,1/SR)
 w=(1-np.exp(-(f/max(1,lo))**2))/(1+(f/hi)**4)
 a=np.fft.irfft(np.fft.rfft(a)*w,n)
 return a/(np.std(a)+1e-8)
def put(t,a,volume,pan=.5):
 start=int(t*SR)
 if start<0:return
 n=min(len(a),N-start)
 if n>0:foley[start:start+n]+=a[:n,None]*volume*np.array([math.cos(pan*math.pi/2),math.sin(pan*math.pi/2)])
wind=filtered_noise(60,10,750)
wind_env=.014+.012*(.5+.5*np.sin(time*.33))+.025*np.clip((time-53)/7,0,1)
foley[:,0]+=wind*wind_env;foley[:,1]+=np.roll(wind,1511)*wind_env*.85
def cannon(t,pan,vol=1):
 d=3.2;s=np.arange(int(d*SR))/SR
 rumble=filtered_noise(d,15,170)*np.exp(-s*1.6)
 crack=filtered_noise(d,280,6500)*np.exp(-s*35)
 boom=np.sin(2*np.pi*(48*s+26*(1-np.exp(-s*5))/5))*np.exp(-s*3)
 put(t,(rumble*.2+boom*.21+crack*.15)*np.minimum(s*1000,1),.65*vol,pan)
def volley(t,vol):
 for k in range(17):
  d=.85;s=np.arange(int(d*SR))/SR
  a=filtered_noise(d,180,4500)*np.exp(-s*22)+.4*np.sin(2*np.pi*96*s)*np.exp(-s*10)
  put(t+k*.009+rng.random()*.013,a,vol*.058,.2+.6*k/16)
 for off,pan in [(.18,.25),(.24,.75),(.4,.45)]:cannon(t+off,pan,.28*vol)
for e in timeline['EVENTS']:
 if e['kind']=='cannon':cannon(e['t'],.25+.16*(e['x']+3))
 if e['kind']=='volley':volley(e['t'],1.15 if e['t']>40 else .7)
def tap(t,vol,pan=.5,kind='hoof'):
 d=.16;s=np.arange(int(d*SR))/SR
 a=filtered_noise(d,150,2400)*np.exp(-s*55)+.65*np.sin(2*np.pi*170*s)*np.exp(-s*35)
 put(t,a,vol,pan)
for t in np.arange(14.2,26,.155):tap(t,.032 if t<20 else .021,.3+.2*math.sin(t))
for t in np.arange(26,31,.18):tap(t,.025,.7)
for t in np.arange(35,45.8,.375):
 for off,pan in [(0,.25),(.025,.75),(.061,.45)]:tap(t+off,.028,pan,'step')
for t in np.arange(48.1,55,.28):tap(t+rng.random()*.12,.017,.2+rng.random()*.6,'step')
for t in [1,3.4,5,28,36,40,48,54,56.5]:
 a=filtered_noise(.8,900,4500);s=np.arange(len(a))/SR
 put(t,a*np.sin(np.pi*s/.8)**2,.005 if t<48 else .012,.45)
for t in [8.17,9.27,10.47]:tap(t,.031,.4)
# Separate stems are retained for user-directed revisions.
def save(name,a):
 with wave.open(str(ROOT/name),'wb') as w:
  w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
save('music.wav',music);save('foley.wav',foley)
mix=music+foley
peak=float(np.max(np.abs(mix)));gain=.89/max(peak,1e-6);mix*=gain
mix*=np.interp(time,[0,.15,59.4,60],[0,1,1,0])[:,None]
save('audio.wav',mix)
report={'seconds':60,'sample_rate':SR,'channels':2,'peak_dbfs':20*math.log10(float(np.max(np.abs(mix)))),'rms_dbfs':20*math.log10(float(np.sqrt(np.mean(mix**2)))),'clipped_samples':int(np.sum(np.abs(mix)>=1)),'source':'Original instrumental score using GeneralUser GS sampled instruments; original synthesized battle foley; no speech','programs':programs,'note_events':len(events),'mix_gain':gain}
(ROOT/'audio-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
