"""Original, deterministic preview composition + process sound design; no recordings."""
from pathlib import Path
import json, wave
import numpy as np
ROOT=Path(__file__).resolve().parent
SR=48000; DUR=5; n=SR*DUR
t=np.arange(n)/SR; random=np.random.default_rng(77231)
music=np.zeros((n,2)); sfx=np.zeros((n,2))
def put(dst,x,at,pan=0):
    start=round(at*SR); end=min(n,start+len(x))
    if end<=start:return
    dst[start:end,0]+=x[:end-start]*np.sqrt((1-pan)/2)
    dst[start:end,1]+=x[:end-start]*np.sqrt((1+pan)/2)
def note(midi,length,amp):
    q=np.arange(round(length*SR))/SR; f=440*2**((midi-69)/12)
    attack=1-np.exp(-q*150)
    env=attack*np.exp(-q*3.5/length)*np.minimum(1,(length-q)/.06)
    return amp*env*(np.sin(2*np.pi*f*q)+.27*np.sin(2*np.pi*f*2.002*q)+.09*np.sin(2*np.pi*f*3*q))
beat=60/96
# Two soft broken-chord bars: Fmaj9 -> G6. Melodic line above a distinct bass.
notes=[(0,53,.105,1.65),(.0,69,.085,1.5),(.625,72,.082,1.4),(1.25,76,.078,1.3),(1.875,74,.07,1.25),(2.5,55,.10,1.8),(2.5,71,.084,1.45),(3.125,74,.085,1.5),(3.75,76,.07,1.2),(4.375,74,.055,.625)]
for i,(at,key,vol,l) in enumerate(notes):put(music,note(key,l,vol),at,(-.18 if i%2 else .18))
for at,keys in [(0,[57,60,64]),(2.5,[59,62,67])]:
    for j,key in enumerate(keys):put(music,note(key,2.45,.036),at,.3*(j-1))
# Warm airy steam, becoming dry air: filtered noise with slow envelope.
noise=random.normal(0,1,n); low=np.convolve(noise,np.ones(13)/13,'same'); hiss=noise-low
steam=.058*low+.009*hiss
steam_env=np.clip(t/.15,0,1)*(1-.76*np.clip((t-1.6)/1.8,0,1))*(1-.8*np.clip((t-4.5)/.5,0,1))
put(sfx,steam*steam_env,0,-.12)
for i in range(6):
    at=2.2+i*.37; l=.24; q=np.arange(round(SR*l))/SR
    z=random.normal(0,1,len(q)); z=np.convolve(z,np.ones(5)/5,'same')
    envelope=np.sin(np.pi*q/l)**2
    put(sfx,z*envelope*.033,at,(-.4+i*.14))
q=np.arange(round(1.5*SR))/SR; z=random.normal(0,1,len(q)); z=np.convolve(z,np.ones(24)/24,'same')
put(sfx,z*np.sin(np.pi*q/1.5)**2*.13,1.55,.18)
mix=(music+sfx)*2.5
fade=np.minimum(1,t/.035)*np.minimum(1,(DUR-t)/.17)
mix*=fade[:,None]
peak=float(np.max(np.abs(mix)))
if peak>.88:mix*=.88/peak
out=ROOT/'audio'/'preview.wav';out.parent.mkdir(exist_ok=True)
with wave.open(str(out),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((mix*32767).astype('<i2').tobytes())
report={'sample_rate':SR,'samples':n,'duration':DUR,'channels':2,'peak_dbfs':float(20*np.log10(np.max(np.abs(mix))+1e-12)),'rms_dbfs':float(20*np.log10(np.sqrt(np.mean(mix**2))+1e-12)),'bpm':96,'source':'original deterministic synthesis','listened':False,'notes':notes,'events':[{'start':0,'end':5,'sound':'steam-to-dry-air'},{'start':1.55,'end':3.05,'sound':'air-turn'},{'start':2.2,'end':4.29,'sound':'leaf-rustle'}]}
(ROOT/'technical'/'audio-evidence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['duration','peak_dbfs','rms_dbfs','bpm']}))
