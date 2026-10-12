"""Original deterministic synthesized score and synchronized contact sounds.
No external recordings, voice clone, samples or downloaded music.
"""
import numpy as np, wave, json, hashlib
from pathlib import Path
R=Path(__file__).parent; SR=48000; N=52*SR
out=np.zeros((N,2),dtype=np.float64); events=[]
def add(start,signal,gain=.1,pan=0,label=''):
    n0=int(start*SR); n=min(len(signal),N-n0)
    if n<=0:return
    out[n0:n0+n,0]+=signal[:n]*gain*np.sqrt((1-pan)/2)
    out[n0:n0+n,1]+=signal[:n]*gain*np.sqrt((1+pan)/2)
    if label:events.append({'time':start,'event':label,'gain':gain,'pan':pan})
def chime(freq,dur=2.4):
    t=np.arange(int(SR*dur))/SR
    attack=np.minimum(t/.009,1)
    return attack*(np.sin(2*np.pi*freq*t)*np.exp(-t*2.1)+.24*np.sin(2*np.pi*freq*2.003*t)*np.exp(-t*3.4)+.10*np.sin(2*np.pi*freq*3.99*t)*np.exp(-t*5))
def pad(freq,dur):
    t=np.arange(int(SR*dur))/SR; env=np.minimum(t/1.4,1)*np.minimum((dur-t)/1.6,1)
    return env*(np.sin(2*np.pi*freq*t)+.28*np.sin(2*np.pi*freq*2*t))
def air(dur,seed):
    rng=np.random.default_rng(seed); n=int(dur*SR); x=rng.normal(size=n)
    x=np.convolve(x,np.ones(60)/60,mode='same');t=np.arange(n)/SR
    return x*np.sin(np.pi*t/dur)**2*1.7
# A sparse D-minor/add9 motif recurs at the macro beginning and the system return.
for section,starts in [(0,[.6,2.2,3.9,5.4]),(7,[7.2,9.2,11.2]),(14,[14.2,16.5,19]),(41,[41.4,42.9,44.2,45.5]),(47,[47.4,48.5,49.6])]:
    notes={0:[587.33,880,698.46,659.25],7:[293.66,440,523.25],14:[220,293.66,349.23],41:[587.33,698.46,880,1174.66],47:[880,698.46,587.33]}[section]
    for i,(at,f) in enumerate(zip(starts,notes)):add(at,chime(f,3.1),.105 if section!=14 else .07,(-.22 if i%2==0 else .22),f'motif {section}: {f}Hz')
for at,dur,fs,level in [(0,7,[146.83,220],.022),(7,7,[146.83,261.63],.024),(14,7.7,[110,174.61],.025),(32,8.8,[146.83,220,293.66],.021),(41,6,[146.83,220,349.23],.030),(47,5,[146.83,220],.020)]:
    for f in fs:add(at,pad(f,dur),level,label=f'pad {f}Hz')
for at,dur in [(6.6,.7),(13.45,.8),(40.5,.9),(46.5,.8)]:add(at,air(dur,int(at*100)),.09,0,'scale transition breath')
# Causal contacts: incident interface, second interface, sum/result appearance.
for at,f,pan,label in [(23,523.25,-.25,'incident onset'),(24.4,880,-.10,'upper interface contact'),(25.5,880,.17,'lower interface contact'),(28.0,659.25,.25,'two paths resolved'),(34.3,1174.66,0,'in-phase sum appears'),(38.4,293.66,.35,'out-of-phase result quietens')]:add(at,chime(f,1.9),.09 if at<32 else .105,pan,label)
# Equal-pitch chimes together support the phase lesson; music is illustrative.
for at in [32.7,33.7,34.7,35.7]:
    add(at,chime(587.33,1.3),.05,-.3);add(at,chime(587.33,1.3),.05,.3)
# A very soft heartbeat anchors system reveal; no impact on every cut.
for at in [41.4,42.9,44.2]:add(at,chime(73.42,1.2),.09,0,'system return low pulse')
fade=np.minimum(np.arange(N)/SR/.06,1)*np.minimum((52-np.arange(N)/SR)/.8,1)
out*=fade[:,None]; peak=float(np.abs(out).max());out*=.62/max(peak,.62)
with wave.open(str(R/'soundtrack.wav'),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes((out*32767).astype('<i2').tobytes())
(R/'sound-events.json').write_text(json.dumps({'duration':52,'sample_rate':SR,'original_synthesized':True,'voice':False,'description':'Sparse recurring chime motif, pads, transition breaths and causal contact cues. No claim of studio orchestral quality.','events':events,'peak':float(np.abs(out).max()),'rms':float(np.sqrt(np.mean(out**2))),'sha256':hashlib.sha256((R/'soundtrack.wav').read_bytes()).hexdigest()},ensure_ascii=False,indent=2),encoding='utf-8')
print('Soundtrack',round(float(np.abs(out).max()),3),round(float(np.sqrt(np.mean(out**2))),4),len(events),'events')
