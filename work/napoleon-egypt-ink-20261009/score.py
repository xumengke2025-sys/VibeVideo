"""Original instrumental and effects. No narration, samples or music downloads."""
import numpy as np, wave, json, subprocess
from pathlib import Path
R=Path(__file__).parent; SR=48000; DUR=60; N=SR*DUR
rng=np.random.default_rng(1798); audio=np.zeros((N,2),np.float64)
def add(start,sound,pan=0,gain=1):
 i=round(start*SR); k=min(len(sound),N-i)
 if k<=0:return
 p=np.clip(pan,-1,1); audio[i:i+k,0]+=sound[:k]*np.sqrt((1-p)/2)*gain;audio[i:i+k,1]+=sound[:k]*np.sqrt((1+p)/2)*gain
def resonant(start,freq,length,gain=.03,pan=0,plucked=False):
 t=np.arange(round(length*SR))/SR
 env=(1-np.exp(-t/(.007 if plucked else .8)))*np.exp(-t/(1.6 if plucked else length*.45))
 env*=np.clip((length-t)/.8,0,1); sig=np.zeros_like(t)
 for h in range(1,7):sig+=np.sin(2*np.pi*(freq*h+.08*h*h)*t+.35*h)*np.exp(-t*h*.08)/(h**(1.9 if plucked else 2.5))
 sig*=env*(.94+.06*np.sin(t*2*np.pi*4.7))
 add(start,sig,pan,gain)
 # Quiet asymmetric room tails from original signal, deterministic.
 for d,g in [(.23,.17),(.41,.12),(.71,.06)]:add(start+d,sig,-pan,gain*g)
def noise_effect(start,length,gain=.04,pan=0,kind='wind'):
 t=np.arange(round(length*SR))/SR;n=rng.normal(0,1,len(t));kernel=np.ones(35 if kind=='wind' else 5);kernel/=len(kernel);n=np.convolve(n,kernel,mode='same')
 if kind=='cannon':s=(n*.7+np.sin(2*np.pi*(42*t-10*t*t))*np.exp(-t*4))*np.exp(-t*3.2)*(1-np.exp(-t*100))
 elif kind=='paper':s=n*np.exp(-t*1.5)*(.25+.75*np.sin(t*19)**2)
 else:s=n*(np.sin(np.pi*t/length)**2)
 add(start,s,pan,gain)
t=np.arange(N)/SR
wind=np.convolve(rng.normal(0,1,N),np.ones(100)/100,mode='same')
bed=wind*(.009+.005*np.sin(t*.17)**2)*np.clip(t/2,0,1)*np.clip((60-t)/2,0,1)
audio[:,0]+=bed;audio[:,1]+=np.roll(bed,211)
# Slow bowed harmonics and a sparse oud-like plucked motif in D minor.
for s,f in [(0,73.416),(6,110),(13,87.307),(19,73.416),(25,69.296),(30,65.406),(36,73.416),(43,110),(50,87.307),(54,73.416)]:resonant(s,f,9,.040)
notes=[(2.5,293.66),(5,220),(8.8,146.83),(11.1,174.61),(14,220),(17.4,293.66),(20,349.23),(23,220),(26,146.83),(29,138.59),(33,130.81),(38,174.61),(40.5,220),(43,293.66),(47,220),(50.5,174.61),(54.4,293.66),(57,146.83)]
for k,(s,f) in enumerate(notes):resonant(s,f,4.5,.057,(-.3 if k%2 else .3),True)
noise_effect(.7,.5,.05,0,'paper');resonant(.7,180,.8,.055)
for s in [7.2,16.1,36.4,39.4,43]:noise_effect(s,1.2,.075,-.15,'paper')
for s,pan in [(26.6,-.4),(29.3,.45),(32.1,0)]:noise_effect(s,3,.19,pan,'cannon')
for s in [7,12,26,30,46,50]:noise_effect(s,5,.12,.1,'wind')
for s in np.arange(18,23,.65):resonant(s,56,.7,.020)
resonant(54.4,587.33,5.6,.035)
audio*=np.minimum(np.clip(t/.6,0,1),np.clip((60-t)/1.7,0,1))[:,None]
peak=np.max(np.abs(audio));audio*=.78/max(peak,1e-9)
with wave.open(str(R/'out/score.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(audio,-1,1)*32767).astype('<i2').tobytes())
(R/'out/audio-evidence.json').write_text(json.dumps({'duration':60,'sr':SR,'channels':2,'original_synthetic':True,'peak_dbfs':float(20*np.log10(np.max(np.abs(audio)))),'rms_dbfs':float(20*np.log10(np.sqrt(np.mean(audio**2)))),'listened':False},indent=2))
print('Original score and effects written: 60.000 seconds',flush=True)
