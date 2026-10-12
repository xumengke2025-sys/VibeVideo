"""Mix original synthesized ambience with the explicitly synthetic Chinese narration."""
from pathlib import Path
import json, subprocess, wave, math, io
import numpy as np

ROOT=Path(__file__).parent
FFMPEG=ROOT.parents[1]/'node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
RATE=48000;DURATION=90;N=RATE*DURATION
mix=np.zeros((N,2),np.float32);speech=np.zeros((N,2),np.float32)
records=json.loads((ROOT/'narration.json').read_text(encoding='utf-8'))
evidence=[]

def decode(file,tempo=1):
 args=[str(FFMPEG),'-hide_banner','-loglevel','error','-i',str(file)]
 if tempo>1.0001:args+=['-af',f'atempo={tempo:.8f}']
 args+=['-f','wav','-c:a','pcm_s16le','-ac','1','-ar',str(RATE),'pipe:1']
 raw=subprocess.run(args,check=True,stdout=subprocess.PIPE).stdout
 with wave.open(io.BytesIO(raw),'rb') as f:
  return np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(np.float32)/32768.

for r in records:
 file=ROOT/r['file'];clip=decode(file);original=len(clip)/RATE
 available=r['end']-r['start']-.18
 tempo=max(1,original/available)
 if tempo>1.001:clip=decode(file,tempo)
 assert len(clip)/RATE<=available+.06,'Narration overflows its scene'
 peak=max(.001,float(np.max(np.abs(clip))))
 clip*=.60/peak
 fade=min(500,len(clip)//4);clip[:fade]*=np.linspace(0,1,fade);clip[-fade:]*=np.linspace(1,0,fade)
 start=int(r['start']*RATE);end=min(N,start+len(clip));speech[start:end,0]+=clip[:end-start];speech[start:end,1]+=clip[:end-start]
 evidence.append({**r,'original_duration':round(original,4),'atempo':round(tempo,5),'mixed_duration':round(len(clip)/RATE,4),'actual_end':round(r['start']+len(clip)/RATE,4)})

def note(start,duration,freq,gain,pan=.5,bell=False):
 i=int(start*RATE);j=min(N,int((start+duration)*RATE));t=np.arange(j-i,dtype=np.float64)/RATE
 if bell:
  env=(1-np.exp(-t*75))*np.exp(-t*3.8)
  signal=np.sin(2*np.pi*freq*t+.9*np.sin(2*np.pi*freq*2.01*t)*np.exp(-t*5))*env
 else:
  env=np.minimum(1,t/1.5)*np.minimum(1,np.maximum(0,(duration-t)/2))
  signal=(np.sin(2*np.pi*freq*t+.09*np.sin(t*.71))+.19*np.sin(2*np.pi*freq*2.003*t))*env
 mix[i:j,0]+=signal*gain*math.cos(pan*np.pi/2);mix[i:j,1]+=signal*gain*math.sin(pan*np.pi/2)

for start,duration,chord in [(0,28,[73.416,146.832,220,293.665]),(24,32,[65.406,130.813,196,261.626]),(52,25,[58.27,116.541,174.614,233.082]),(74,16,[73.416,146.832,220,293.665])]:
 for i,freq in enumerate(chord):note(start,duration,freq,.010,(i+.5)/len(chord))
for i,start in enumerate([.2,12,25,40,54,62,72,80,86]):note(start,1.5,[587.33,440,659.25,783.99,523.25,659.25,880,587.33,440][i],.020,.3+.4*(i%2),True)

# Scene-aligned narration presence controls quiet ambience, with smooth edges.
duck=np.ones(N,np.float32)
for r in evidence:
 a=max(0,int((r['start']-.1)*RATE));b=min(N,int((r['actual_end']+.16)*RATE));duck[a:b]=.43
edge=2400
for r in evidence:
 a=max(0,int((r['start']-.1)*RATE));b=min(N,int((r['actual_end']+.16)*RATE))
 if a>=edge:duck[a-edge:a]=np.linspace(1,.43,edge)
 if b+edge<N:duck[b:b+edge]=np.linspace(.43,1,edge)
mix*=duck[:,None];mix+=speech
mix[:int(.15*RATE)]*=np.linspace(0,1,int(.15*RATE))[:,None]
mix[-int(.5*RATE):]*=np.linspace(1,0,int(.5*RATE))[:,None]
peak=float(np.max(np.abs(mix)));assert peak<.99,'Mix would clip'
pcm=(np.clip(mix,-1,1)*32767).astype('<i2')
with wave.open(str(ROOT/'soundtrack.wav'),'wb') as f:
 f.setnchannels(2);f.setsampwidth(2);f.setframerate(RATE);f.writeframes(pcm.tobytes())
(ROOT/'audio-evidence.json').write_text(json.dumps({'duration':DURATION,'sample_rate':RATE,'peak_dbfs':round(20*math.log10(peak),3),'rms_dbfs':round(20*math.log10(float(np.sqrt(np.mean(mix**2)))),3),'voice_disclosure':'AI-generated Chinese narration, public zh-CN-YunxiNeural voice; no human cloned','actual_listening':False,'cues':evidence},ensure_ascii=False,indent=2),encoding='utf-8')

def stamp(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
srt=[]
for i,r in enumerate(evidence):srt.append(f"{i+1}\n{stamp(r['start'])} --> {stamp(r['actual_end'])}\n{r['text']}\n")
(ROOT/'narration.srt').write_text('\n'.join(srt),encoding='utf-8')
print(json.dumps({'audio':'soundtrack.wav','duration':DURATION,'peak_dbfs':round(20*math.log10(peak),2),'cues':len(evidence),'max_atempo':round(max(x['atempo'] for x in evidence),4)},ensure_ascii=False))
