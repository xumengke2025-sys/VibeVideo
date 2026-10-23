"""Original 90-second chamber waltz, licensed sampled instruments, authored foley.
This is new musical content; no music from the Babylon film is used.
"""
from pathlib import Path
import numpy as np, math,sys,json,wave,struct
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'vendor'))
from tinysoundfont import Synth
SR=48000;N=90*SR;rng=np.random.default_rng(20261022);events=[];notes=[]
def note(t,d,ch,p,v):
 if 0<=t<89:
  events.extend([(round(t*SR),'on',ch,int(p),int(v)),(min(N,round((t+d)*SR)),'off',ch,int(p),0)]);notes.append([round(t,4),round(d,4),ch,int(p),int(v)])
# 3/4, quarter = .75 s, forty bars. G major, warm open inner voices.
beat=.75;bar=2.25
chords=[[43,55,59,62],[40,55,59,64],[36,55,60,64],[38,54,57,62],[43,55,59,62],[45,57,60,64],[38,54,57,60],[43,55,59,62]]
for b in range(39):
 t=b*bar;c=chords[b%8];soft=43<=t<60;vel=38 if soft else 48 if t<12 else 56 if t<74 else 60
 note(t,bar+.15,1,c[0]+12,vel-8);note(t,bar+.2,2,c[0],vel-16)
 if not soft:
  for p in c[1:]:note(t,bar*.95,0,p,vel)
 else:
  for p in c[1:3]:note(t,bar*.85,0,p,vel-13)
 for j in [0,1,2]:
  note(t+j*beat,.42,4,c[1+j]+12,vel-13+(5 if j==0 else 0))
 if 12<=t<43 or 74<=t<86:
  for j in range(6):note(t+j*beat/2,.24,5,c[1+j%3]+12,43+(j%3)*3)
# Gentle recurring eight-bar melody, antecedent / answering phrase.
motif=[(0,67,1),(1,71,.5),(1.5,74,.5),(2,71,1),(3,69,1.5),(4.5,67,.5),(5,64,1),
 (6,67,1),(7,69,1),(8,72,1),(9,74,1.5),(10.5,72,.5),(11,69,1),
 (12,71,1.5),(13.5,74,.5),(14,79,1),(15,76,1),(16,74,1),(17,72,1),
 (18,71,1),(19,69,.5),(19.5,67,.5),(20,66,1),(21,69,1),(22,67,2)]
for start,ch,v,trans in [(9,3,58,0),(27,6,55,0),(60,3,52,0),(74,6,61,0)]:
 for off,p,d in motif:
  tt=start+off*beat
  if tt<min(start+18,87):note(tt,d*beat*.94,ch,p+trans,v+(3 if off%3==0 else -2))
for t,p in [(2.25,79),(6.75,74),(12,79),(18,83),(26.25,86),(35.25,83),(42,79),(57,74),(68,79),(78.75,83),(84,79)]:note(t,1.4,7,p,38)
# Thin chamber texture for the unloading, with breathing space around contacts.
for t,p in [(45,74),(48,71),(51.75,69),(55.5,67),(58.5,71)]:note(t,1.8,3,p,42)
# Final cadence and a two-second natural release.
for p in [43,55,59,62,67]:note(85.5,2.4,0,p,49)
note(85.5,2.5,1,55,42);note(85.5,2.5,2,43,36);note(86,1.4,3,67,48);note(86.25,2,7,79,28)
programs={0:48,1:42,2:43,3:73,4:45,5:46,6:68,7:8}
synth=Synth(gain=-12,samplerate=SR);sf=synth.sfload((R/'assets/GeneralUser-GS.sf2').read_bytes(),max_voices=192)
for ch,p in programs.items():synth.program_select(ch,sf,0,p)
for ch,pan in [(0,48),(1,78),(2,64),(3,46),(4,36),(5,86),(6,72),(7,66)]:synth.control_change(ch,10,pan)
music=np.zeros((N,2),np.float32);cursor=0
for at,kind,ch,p,v in sorted(events,key=lambda e:(e[0],e[1]=='on')):
 if at>cursor:music[cursor:at]=np.frombuffer(synth.generate(at-cursor),np.float32).reshape(-1,2);cursor=at
 if kind=='on':synth.noteon(ch,p,v)
 else:synth.noteoff(ch,p)
if cursor<N:music[cursor:]=np.frombuffer(synth.generate(N-cursor),np.float32).reshape(-1,2)
dry=music.copy()
for delay,g in [(.071,.13),(.119,.11),(.211,.09),(.347,.065),(.553,.04),(.811,.025)]:
 n=round(delay*SR);music[n:]+=dry[:-n,::-1]*g
tt=np.arange(N)/SR;music*=np.interp(tt,[0,1,42,44,59,61,73,75,87,90],[.12,.72,.85,.58,.58,.80,.8,.92,.8,0])[:,None]
foley=np.zeros((N,2),np.float32)
def noise(d,lo,hi):
 n=round(d*SR);a=rng.normal(0,1,n);f=np.fft.rfftfreq(n,1/SR);w=(1-np.exp(-(f/max(lo,1))**2))/(1+(f/hi)**4);a=np.fft.irfft(np.fft.rfft(a)*w,n);return a/(np.std(a)+1e-9)
def put(t,a,g,pan=.5):
 i=round(t*SR);n=min(len(a),N-i)
 if n>0:foley[i:i+n]+=a[:n,None]*g*np.array([math.cos(pan*math.pi/2),math.sin(pan*math.pi/2)])
wind=noise(90,30,550)*(.0018+.0008*np.sin(tt*.27));foley[:,0]+=wind;foley[:,1]+=np.roll(wind,1301)*.86
water=noise(90,500,4200)*.0012;foley[:,0]+=water*np.interp(tt,[0,20,27,37,45,90],[.4,.8,1,1,.4,.4]);foley[:,1]+=np.roll(water,371)*.6
def tap(t,vol,kind='wood',pan=.5):
 d=.24;x=np.arange(round(d*SR))/SR
 a=noise(d,140,2200)*np.exp(-x*65)*.25+np.sin(2*np.pi*(190 if kind=='wood' else 310)*x)*np.exp(-x*35)*.7;put(t,a,vol,pan)
for t,g in [(22,.10),(23.95,.05),(46.7,.05),(47.5,.045),(49.5,.035),(56,.13),(57.8,.035)]:tap(t,g)
for t in np.arange(27,45.4,.27):tap(t,.009*(1-abs(t-36)/18),'metal',.42)
for t in np.arange(4,89,.68):
 envelope=float(np.interp(t,[0,12,27,37,45,60,74,90],[.003,.005,.008,.02,.006,.008,.026,.009]))
 for off,g in [(0,1),(.18,.8),(.34,.7),(.48,.85)]:tap(t+off,envelope*g,'hoof',.65)
for t in np.arange(12,83,1.07):
 a=noise(.18,550,2800)*np.exp(-np.arange(round(.18*SR))/SR*24);put(t,a,.0035,.3 if int(t)%2 else .7)
for hit in [62,64,66]:
 d=7;x=np.arange(round(d*SR))/SR;a=np.zeros_like(x)
 for ratio,amp,decay in [(1,1,.55),(2.01,.38,.7),(2.76,.24,.95),(4.07,.13,1.3),(5.4,.08,1.6)]:a+=amp*np.sin(2*np.pi*392*ratio*x)*np.exp(-x*decay)
 a*=np.minimum(1,x*1000);put(hit,a,.055,.46);put(hit+.14,a,.012,.65);tap(hit,.015,'metal',.46)
mix=music+foley;peak=float(np.max(np.abs(mix)));gain=min(1,.86/max(peak,1e-8));mix*=gain
def wav(path,data):
 with wave.open(str(path),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(data,-1,1)*32767).astype('<i2').tobytes())
for name,data in [('music',music*gain),('foley',foley*gain),('final-mix',mix)]:wav(R/'audio'/f'{name}.wav',data)
(R/'audio/score-notes.json').write_text(json.dumps({'tempo':80,'meter':'3/4','duration':90,'programs':programs,'notes':notes},indent=2),encoding='utf8')
# Standard editable MIDI, 480 ticks/beat, tempo fixed at 80.
def vlq(n):
 b=[n&127];n>>=7
 while n:b.insert(0,(n&127)|128);n>>=7
 return bytes(b)
ev=[(0,b'\xff\x51\x03\x0b\x71\xb0'),(0,b'\xff\x58\x04\x03\x02\x18\x08')]
for ch,p in programs.items():ev.append((0,bytes([0xC0+ch,p])))
for t,d,ch,p,v in notes:ev.extend([(round(t/beat*480),bytes([0x90+ch,p,v])),(round((t+d)/beat*480),bytes([0x80+ch,p,0]))])
data=b'';last=0
for tick,msg in sorted(ev,key=lambda e:e[0]):data+=vlq(tick-last)+msg;last=tick
data+=b'\x00\xff\x2f\x00';(R/'audio/first-bread-original.mid').write_bytes(b'MThd'+struct.pack('>IHHH',6,0,1,480)+b'MTrk'+struct.pack('>I',len(data))+data)
(R/'audio/audio-report.json').write_text(json.dumps({'duration':90,'sample_rate':SR,'channels':2,'peak':float(np.max(np.abs(mix))),'rms':float(np.sqrt(np.mean(mix**2))),'music':'New original chamber waltz rendered with GeneralUser GS licensed samples','foley':'Authored synthesis, not field recordings','actual_listening':'not yet performed; waveform checks are not listening'},indent=2),encoding='utf8')
print('AUDIO_READY',90,peak,gain)
