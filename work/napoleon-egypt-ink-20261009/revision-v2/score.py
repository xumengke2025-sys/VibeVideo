from pathlib import Path
import numpy as np,json,wave,sys
ROOT=Path(__file__).resolve().parent
plan=json.loads((ROOT/'plan.json').read_text(encoding='utf-8-sig'))
sr=48000;duration=plan['duration'];n=int(sr*duration);rng=np.random.default_rng(1798)
audio=np.zeros((n,2),dtype=np.float64)
def add(at,sig,gain=.1,pan=0):
 start=int(round(at*sr));end=min(n,start+len(sig));skip=max(0,-start);start=max(0,start)
 if end<=start:return
 sig=sig[skip:skip+end-start]*gain
 audio[start:end,0]+=sig*np.sqrt((1-pan)/2);audio[start:end,1]+=sig*np.sqrt((1+pan)/2)
def filtered_noise(length,width=20):
 a=rng.normal(0,1,length+width);return np.convolve(a,np.ones(width)/np.sqrt(width),mode='valid')[:length]
def event(kind,seed):
 dur={'齐射':1.6,'远炮':2.2,'木断':1.3,'水面闷响':1.7,'刷石':1.1,'笔端接触记录':1.3,'浅浪覆盖':2.5,'划桨':.6,'footstep':.16,'hoof':.12}.get(kind,.38)
 tt=np.arange(int(sr*dur))/sr;white=filtered_noise(len(tt),2 if kind in ['木断','索具绷响','齐射'] else 30)
 if kind in ['footstep','hoof']:
  sig=(white*.6+np.sin(2*np.pi*(85 if kind=='hoof' else 140)*tt)*.3)*np.exp(-tt*35)
 elif kind in ['齐射','远炮','木断','帆和木材受击']:
  sig=white*np.exp(-tt*(5 if kind=='齐射' else 3))+np.sin(2*np.pi*(65*tt-14*tt*tt))*np.exp(-tt*4)*.65
 elif kind in ['刷石','笔端接触记录','纸边落定','布面拂动']:
  sig=white*(.18+.16*np.sin(tt*43)**2)*np.sin(np.pi*tt/dur)**2
 else:sig=(white*.45+np.sin(2*np.pi*117*tt)*.25)*np.exp(-tt*10)*np.minimum(1,tt/.005)
 return sig*np.minimum(1,tt/.003),(.19 if kind in ['齐射','远炮'] else .12)
# Quiet wind and water, with separate shot-specific levels; no dialogue or borrowed music.
tt=np.arange(n)/sr;ambient=filtered_noise(n,400)*.018
sea=np.logical_or(tt<9, np.logical_and(tt>=28,tt<38))| (tt>=49)
ambient+=filtered_noise(n,100)*(.015+sea*.015)*(.6+.4*np.sin(tt*1.3)**2)
ambient*=np.minimum(1,tt/.1)*np.clip((60-tt)/.55,0,1)
audio[:,0]+=ambient;audio[:,1]+=np.roll(ambient,213)*.9
for i,e in enumerate(plan['events']):
 if not e.get('sound'):continue
 sig,gain=event(e['sound']['kind'],i);add(e['at']+e['sound'].get('offset',0),sig,e['sound'].get('gain',gain),(i%3-1)*.18)
# Sparse bowed resonances: an original sound bed, no claim of recorded orchestral music.
for at,freq in [(2.6,146.83),(7.2,110),(11,130.81),(17.5,98),(24.6,146.83),(28.4,92.5),(33.5,73.42),(39,130.81),(43.7,164.81),(49.4,110),(55.7,146.83)]:
 d=4.1;t=np.arange(int(d*sr))/sr;env=np.sin(np.pi*np.clip(t/d,0,1))**2*np.exp(-t*.35)
 sig=sum(np.sin(2*np.pi*freq*k*t+.08*np.sin(t*4.4))*env/(k*k) for k in range(1,7));add(at,sig,.019,.1)
peak=float(np.max(np.abs(audio)));audio*=min(1,.86/max(peak,1e-9));audio*=np.minimum(1,tt[:,None]/.03)*np.clip((60-tt[:,None])/.12,0,1)
target=ROOT/'out/score.wav';target.parent.mkdir(exist_ok=True)
with wave.open(str(target),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(audio,-1,1)*32767).astype('<i2').tobytes())
(ROOT/'out/audio-evidence.json').write_text(json.dumps({'sample_rate':sr,'channels':2,'duration':60,'peak_before_gain':peak,'finite':bool(np.isfinite(audio).all()),'events':len(plan['events']),'source':'plan.json','listened':False},indent=2),encoding='utf8')
print(target)
