"""Original music-box sketch and material foley; no speech, no reference audio."""
from pathlib import Path
import numpy as np, wave, json
SR=48000; DUR=60; rng=np.random.default_rng(20261013)
audio=np.zeros((SR*DUR,2),np.float32)
def place(signal,t,gain=.1,pan=0):
    start=round(t*SR); n=min(len(signal),len(audio)-start)
    if n<=0:return
    p=np.clip(pan,-1,1);audio[start:start+n,0]+=signal[:n]*gain*np.sqrt((1-p)/2);audio[start:start+n,1]+=signal[:n]*gain*np.sqrt((1+p)/2)
def bell(note,length=2.4):
    x=np.arange(round(SR*length))/SR; f=440*2**((note-69)/12)
    a=np.zeros(len(x));
    for ratio,amp,decay in [(1,.68,1.8),(2,.18,3.2),(2.756,.075,4.7),(5.4,.022,7.0)]:
        a+=amp*np.cos(2*np.pi*f*ratio*x)*np.exp(-x*decay)
    a*=np.minimum(1,x/.008)*(1-np.exp(-(length-x)*12));return a.astype(np.float32)
def pluck(note,length=1.8):
    # A damped delay-line string, generated with a stable seeded excitation.
    f=440*2**((note-69)/12);period=round(SR/f);buff=rng.uniform(-1,1,period)
    a=np.zeros(round(SR*length),np.float32)
    for i in range(len(a)):
        j=i%period;a[i]=buff[j];buff[j]=.496*(buff[j]+buff[(j+1)%period])
    return a*np.minimum(1,np.arange(len(a))/SR/.004)
beat=60/78
melody=[74,78,81,78,76,74,71,69,71,74,78,76,74,71,69,74]
notes=[]
for k,t in enumerate(np.arange(0,53,beat*2)):
    note=melody[k%len(melody)]; quiet=.78 if t>40 else 1
    place(bell(note),float(t),.062*quiet,pan=-.16 if k%2 else .16);notes.append({'t':float(t),'note':note})
    if k%2==0:
        for j,n in enumerate([50,57,62]):place(pluck(n),float(t+j*.12),.021*quiet,pan=-.25+j*.25)
for t,n in [(53.3,74),(54.9,78),(56.4,81),(57.8,86)]:place(bell(n,3),t,.045,pan=.06)
def noise(length,tau=12):
    n=round(length*SR);x=rng.normal(0,1,n)
    # moving-average band-limiting for soft bristle and fabric noise
    x=np.convolve(x,np.ones(tau)/tau,mode='same');env=np.sin(np.linspace(0,np.pi,n))**1.3
    return (x*env).astype(np.float32)
for t in [2.4,12.7,30.15]:place(noise(.22,18),t,.035)
for a,b in [(5.2,10.2),(17.5,27)]:
    for t in np.arange(a,b,.39):place(noise(.09,28),float(t),.025,pan=-.15)
for t,p in [(42,-.5),(44.3,.5),(46.6,-.5)]:place(noise(2.1,35),t,.056,pan=p)
for t,n in [(43.2,86),(45.3,90),(47.4,93)]:place(bell(n,2),t,.055,pan=.22)
place(noise(.5,16),58,.063,pan=.3);place(noise(.66,10),58.4,.055,pan=-.2);place(noise(.15,28),59.3,.055)
# Gentle night ambience, a sparse synthetic cricket pair, well below the melody.
for t in np.arange(48.9,57.5,1.83):
    tt=np.arange(round(.1*SR))/SR;s=np.sin(2*np.pi*3700*tt)*np.sin(np.pi*tt/.1)**2
    place(s,float(t),.0035,pan=.55);place(s,float(t+.18),.0035,pan=.55)
audio*=np.minimum(1,np.arange(len(audio))/SR/.4)[:,None]
audio*=np.minimum(1,(DUR-np.arange(len(audio))/SR)/1.5)[:,None]
peak=float(np.abs(audio).max()); audio*=.68/max(peak,.001)
audio=np.clip(audio,-.95,.95)
p=Path(__file__).parent
with wave.open(str(p/'score.wav'),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((audio*32767).astype('<i2').tobytes())
(p/'score-events.json').write_text(json.dumps({'duration':DUR,'sample_rate':SR,'type':'original synthesized music-box sketch and foley','speech':False,'notes':notes,'peak':float(np.abs(audio).max())},indent=2),encoding='utf-8')
print('score.wav: 60 s / 48 kHz / stereo / no speech')
