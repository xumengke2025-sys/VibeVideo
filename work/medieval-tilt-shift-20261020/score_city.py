"""Original 56-second city score. Licensed sampled GM instruments; no speech.
Near-Eastern fantasy palette, not a claim of historical Babylonian reconstruction.
"""
from pathlib import Path
import sys,json,math,wave,shutil
import numpy as np
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'audio';OUT.mkdir(exist_ok=True)
SOURCE=ROOT.parent/'waterloo-20261012'
sys.path.insert(0,str(SOURCE/'python-deps'))
from tinysoundfont import Synth
SR=48000;D=56;N=SR*D;beat=2/3;bar=8/3;R=np.random.default_rng(3309)
events=[]
def note(t,d,ch,p,v):
 t=max(0,t);end=min(54.1,t+d)
 if end<=t:return
 events.extend([(round(t*SR),1,ch,int(p),int(v)),(round(end*SR),0,ch,int(p),0)])
# Open voicings give the melody air. First 20 bars, then an unmetered four-second tail.
chords=[(50,57,62,65),(50,57,62,65),(46,53,58,62),(48,55,60,64),
 (50,57,62,65),(46,53,58,62),(43,50,55,58),(45,52,57,62),
 (50,57,62,65),(48,55,60,64),(46,53,58,62),(50,57,62,65),
 (43,50,55,58),(46,53,58,62),(50,57,62,65),(48,55,60,64),
 (46,53,58,62),(43,50,55,58),(45,52,57,61),(50,57,62,65)]
for b,c in enumerate(chords):
 start=b*bar
 if start>=52:break
 v=34 if b<3 else 42 if b<7 else 32 if b<11 else 40 if b<15 else 48 if b<18 else 35
 for p in [c[0]-12,c[1],c[3]]:note(start+.03,min(bar+.25,52-start),2,p,v)
 # Nylon plucks occupy gaps rather than constantly doubling the tune.
 pattern=[(0,c[0]),(1.5,c[2]),(2.5,c[1]),(3.25,c[3])]
 if b<3:pattern=[(0,c[0]),(2.5,c[2])]
 if 7<=b<10:pattern=[(0,c[0]),(2,c[1])]
 for off,p in pattern:
  t=start+off*beat
  if t<51.5:note(t+R.uniform(-.012,.012),.9,0,p,41+int(R.integers(-5,5)))
 if b in [3,5,11,14,16]:
  for k,p in enumerate([c[1],c[2],c[3],c[2]+12]):note(start+k*beat*.5,.8,3,p,30+k*2)
 if 3<=b<7 or 14<=b<18:
  for off,p,vv in [(0,41,35),(2,64,27),(3.5,62,20)]:note(start+off*beat,.16,9,p,vv)
# A four-note ascending gesture returns in different registers and spacing.
phrases=[
 (1.3,[(0,62,1.2),(1.5,64,.7),(2.5,65,1.2),(4.2,69,1.5)],43),
 (8.0,[(0,69,1.4),(1.7,67,.7),(2.7,65,1.0),(4.2,64,.7),(5.2,62,1.6)],51),
 (15.0,[(0,65,.8),(1.2,67,.9),(2.6,69,1.6)],46),
 (21.0,[(0,62,1.2),(2.1,60,.9),(3.5,62,1.3)],39),
 (28.0,[(0,67,1.3),(1.7,69,1.0),(3,70,1.1),(4.5,69,1.4),(6.3,65,1.1),(8,67,1)],49),
 (38.0,[(0,69,1.5),(2,72,1.3),(3.7,74,1.7),(6,72,.8),(7.2,69,1.2)],51),
 (48.0,[(0,67,.8),(1.1,65,.9),(2.3,64,.9),(4,62,1.9)],43)]
for t,seq,v in phrases:
 for off,p,d in seq:note(t+off,d,1,p,v)
for p in [38,50,57,62,65]:note(52,1.7,2,p,33)
for off,p in [(0,50),(.14,57),(.29,62),(.45,65)]:note(52+off,1.1,3,p,34)

sfpath=SOURCE/'studio/audio-assets/GeneralUser-GS.sf2'
programs={0:24,1:75,2:48,3:46}
s=Synth(gain=-11,samplerate=SR);sf=s.sfload(sfpath.read_bytes(),max_voices=256)
for ch,prog in programs.items():s.program_select(ch,sf,0,prog)
s.program_select(9,sf,128,0,is_drums=True)
for ch,pan in [(0,43),(1,70),(2,61),(3,88),(9,57)]:
 s.control_change(ch,10,pan);s.control_change(ch,7,100);s.control_change(ch,91,28)
music=np.zeros((N,2),np.float32);cursor=0
for at,on,ch,p,v in sorted(events):
 if at>cursor:music[cursor:at]=np.frombuffer(s.generate(at-cursor),np.float32).reshape(-1,2);cursor=at
 if on:s.noteon(ch,p,v)
 else:s.noteoff(ch,p)
if cursor<N:music[cursor:]=np.frombuffer(s.generate(N-cursor),np.float32).reshape(-1,2)
dry=music.copy()
for delay,g in [(.173,.12),(.287,.09),(.431,.08),(.677,.06),(1.013,.04),(1.517,.025)]:
 n=int(delay*SR);music[n:]+=dry[:-n,::-1]*g
time=np.arange(N)/SR
music*=np.interp(time,[0,.9,7,18,21,27,38,46,52,54.5,56],[0,.8,1,1,.72,.82,1,1,.9,.6,0])[:,None]
music*=.64/(np.max(np.abs(music))+1e-9)
# Quiet original ambience. No synthetic speech or invented crowd recording.
env=np.zeros_like(music)
def noise(n,lo,hi):
 a=R.normal(0,1,n);f=np.fft.rfftfreq(n,1/SR);win=(1-np.exp(-(f/max(1,lo))**2))/(1+(f/hi)**4);a=np.fft.irfft(np.fft.rfft(a)*win,n);return a/(np.std(a)+1e-9)
wind=noise(N,30,500);amp=.0035*(.8+.2*np.sin(time*.43))
env[:,0]+=wind*amp;env[:,1]+=np.roll(wind,1301)*amp
water=noise(N,250,2300);wa=np.interp(time,[0,8,18,27,29,36,40,48,56],[.001,.002,.001,.002,.006,.006,.002,.002,.001])
env[:,0]+=water*wa;env[:,1]+=np.roll(water,3113)*wa*.8
def put(t,a,g,pan):
 n=min(len(a),N-int(t*SR));i=int(t*SR)
 if n>0:env[i:i+n]+=a[:n,None]*g*np.array([math.cos(pan*math.pi/2),math.sin(pan*math.pi/2)])
for t in np.arange(19.5,27.5,.69):
 tt=np.arange(int(.12*SR))/SR;a=noise(len(tt),280,1900)*np.exp(-tt*50)*(1-np.exp(-tt*900));put(t,a,.007,.37)
for t in [28.9,31.5,34.4,36.3]:
 tt=np.arange(int(.8*SR))/SR;a=noise(len(tt),180,3200)*np.sin(np.pi*tt/.8)**2;put(t,a,.005,.66)
envelope=np.interp(time,[0,1,54,56],[0,1,1,0]);env*=envelope[:,None]
def save(name,a):
 with wave.open(str(OUT/name),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
save('music.wav',music);save('ambience.wav',env);save('mix-raw.wav',music+env)
lic=SOURCE/'studio/audio-assets/LICENSE-GeneralUser.txt'
shutil.copy2(lic,OUT/lic.name)
report={'duration':56,'sample_rate':SR,'channels':2,'bpm':90,'meter':'4/4','bars':21,'resolution_seconds':52,'last_note_off':54.1,'events':len(events),'programs':programs,'source':str(sfpath),'score':'original composed note sequence','ambience':'original synthesized wind, water, light footsteps; no voice','listened':False,'raw_peak_dbfs':float(20*np.log10(np.max(np.abs(music+env))))}
(OUT/'score-evidence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report))
