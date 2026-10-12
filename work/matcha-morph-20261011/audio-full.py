"""Deterministic 35-second original instrumental and process sound timeline."""
from pathlib import Path
import json,wave
import numpy as np
ROOT=Path(__file__).resolve().parent
SR=48000; DUR=35; n=SR*DUR
t=np.arange(n)/SR; random=np.random.default_rng(77231)
music=np.zeros((n,2)); sfx=np.zeros((n,2))
def put(dst,x,at,pan=0):
 start=round(at*SR); end=min(n,start+len(x))
 if end<=start:return
 dst[start:end,0]+=x[:end-start]*np.sqrt((1-pan)/2)
 dst[start:end,1]+=x[:end-start]*np.sqrt((1+pan)/2)
def note(midi,length,amp,soft=False):
 q=np.arange(round(length*SR))/SR; f=440*2**((midi-69)/12)
 env=(1-np.exp(-q*(18 if soft else 150)))*np.exp(-q*(1.4 if soft else 3.5)/length)*np.minimum(1,(length-q)/.08)
 return amp*env*(np.sin(2*np.pi*f*q)+.24*np.sin(2*np.pi*f*2.002*q)+.075*np.sin(2*np.pi*f*3*q))
chords=[[53,57,60,64,69],[50,57,60,65,69],[55,59,62,67,71],[52,59,62,67,71],[53,57,60,64,69],[57,60,64,67,72],[55,59,62,67,71],[53,57,60,64,69]]
notes=[]
for bar in range(14):
 at=bar*2.5; keys=chords[bar%8]; amp=.085 if bar<12 else .068
 put(music,note(keys[0],2.45,amp),at,-.1)
 for j in range(4):
  key=keys[1+j]; q=at+j*.625
  put(music,note(key+12,1.6,amp*.58),q,(-.22 if j%2 else .22));notes.append([q,key+12])
 for j,key in enumerate(keys[1:4]):put(music,note(key,2.45,.022,True),at,(j-1)*.32)
 # A subtle delayed pluck keeps the soundtrack airy without per-cut impacts.
 for j in range(4):put(music,note(keys[j+1]+12,1.2,.011),at+j*.625+.24,.32)
def noise(at,length,level,window=13,pan=0):
 q=np.arange(round(length*SR))/SR; z=random.normal(0,1,len(q)); z=np.convolve(z,np.ones(window)/window,'same'); env=np.sin(np.pi*q/length)**2
 put(sfx,z*env*level,at,pan)
noise(3.1,.85,.1,24,-.2);noise(6.1,.65,.1,5,.2)
noise(7,4.6,.12,13,-.12);noise(10.4,3.8,.15,24,.18)
for i in range(7):noise(11.4+i*.4,.26,.06,5,-.3+i*.1)
for i in range(8):noise(15.6+i*.26,.15,.085,4,(i%3-1)*.3)
for i in range(12):noise(20.15+i*.22,.22,.13,25,-.25)
noise(23.4,.8,.08,8,0)
noise(25.4,2.6,.22,7,.12)
for i in range(25):noise(29.25+i*.135,.12,.12,8,(-.14 if i%2 else .14))
# A gentle final cadence and an actual fade to silence, rather than an abrupt loop cut.
for j,key in enumerate([53,60,64,69]):put(music,note(key,1.7,.025,True),33.2,(j-1.5)*.15)
outmix=(music+sfx)*2.25; fade=np.minimum(1,t/.045)*np.minimum(1,(DUR-t)/1.15);outmix*=fade[:,None]
peak=float(np.max(np.abs(outmix)))
if peak>.88:outmix*=.88/peak
out=ROOT/'audio'/'full.wav'
with wave.open(str(out),'wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((outmix*32767).astype('<i2').tobytes())
report={'sample_rate':SR,'samples':n,'duration':DUR,'channels':2,'peak_dbfs':float(20*np.log10(np.max(np.abs(outmix))+1e-12)),'rms_dbfs':float(20*np.log10(np.sqrt(np.mean(outmix**2))+1e-12)),'bpm':96,'source':'original deterministic instrumental and process synthesis','listened':False,'narration':False,'events':[{'start':3.1,'end':3.95,'id':'shade-cloth'},{'start':6.1,'end':6.75,'id':'picked-leaf'},{'start':7,'end':11.6,'id':'steam'},{'start':10.4,'end':14.2,'id':'dry-air'},{'start':15.6,'end':17.57,'id':'refine'},{'start':20.15,'end':22.79,'id':'mill-friction'},{'start':25.4,'end':28,'id':'water'},{'start':29.25,'end':32.61,'id':'whisk'},{'start':33.2,'end':35,'id':'cadence-fade'}]}
(ROOT/'technical'/'audio-full-evidence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['duration','peak_dbfs','rms_dbfs','bpm']}))
