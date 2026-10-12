"""Original stereo ambient score with event sounds, generated from production-plan.json."""
import json,math,hashlib,subprocess,re,wave,argparse
from pathlib import Path
import numpy as np
RATE=48000
root=Path(__file__).parent
ap=argparse.ArgumentParser();ap.add_argument('--ffmpeg',required=True);a=ap.parse_args()
plan=json.loads((root/'production-plan.json').read_text(encoding='utf-8'))
out=root/'out-final';out.mkdir(exist_ok=True)
t=np.arange(round(plan['duration']*RATE))/RATE
fade=np.clip(t/.6,0,1)*np.clip((15-t)/1.0,0,1)
swell=.4+.6*np.exp(-((t-7.6)/2.7)**2)
bed=np.zeros((len(t),2))
for j,f in enumerate([73.416,110,146.832,174.614,220]):
    for ch in range(2):bed[:,ch]+=np.sin(2*np.pi*(f+ch*.14)*t+j*.7)*(.023/(1+j*.22))
bed*=fade[:,None]*swell[:,None]
rng=np.random.default_rng(9913);ledger=[]
for e in plan['sound_events']:
    d=e['duration'];u=np.arange(round(d*RATE))/RATE;noise=rng.normal(0,1,len(u));kind=e['kind']
    env=np.clip(u/.008,0,1)*np.clip((d-u)/.2,0,1)
    if kind=='air':x=np.convolve(noise,np.ones(35)/35,'same')*np.sin(np.pi*u/d)
    elif kind=='rise':x=(np.convolve(noise,np.ones(7)/7,'same')*.35+np.sin(2*np.pi*(180*u+420*u*u))*.1)*(u/d)**2
    elif kind=='impact':x=(np.sin(2*np.pi*(82*u-12*u*u))*.7*np.exp(-u*5)+np.sin(2*np.pi*1760*u)*.18*np.exp(-u*3)+noise*.09*np.exp(-u*18))
    elif kind=='bell':x=(np.sin(2*np.pi*e['frequency']*u)+.22*np.sin(2*np.pi*e['frequency']*2.73*u))*np.exp(-u*3.5)
    elif kind=='resolve':x=sum(np.sin(2*np.pi*f*u+j*.3) for j,f in enumerate([293.665,349.228,440]))/3*np.exp(-u*.7)
    else:raise ValueError(kind)
    x*=env*e['gain'];pan=e.get('pan',0);st=np.column_stack([x*math.sqrt((1-pan)/2),x*math.sqrt((1+pan)/2)])
    start=round(e['at']*RATE);end=min(len(bed),start+len(st));bed[start:end]+=st[:end-start];ledger.append({**e,'sample':start})
bed*=np.clip((15-t)/.45,0,1)[:,None];peak=float(np.max(np.abs(bed)));assert peak<1 and np.all(np.isfinite(bed))
wav=out/'sound.wav'
with wave.open(str(wav),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE);w.writeframes((bed*32767).astype('<i2').tobytes())
first=subprocess.run([a.ffmpeg,'-hide_banner','-i',str(wav),'-af','loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True,timeout=60)
m=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',first.stderr)[-1])
assert all(math.isfinite(float(m[k])) for k in ['input_i','input_tp','input_lra','input_thresh','target_offset'])
norm=f"loudnorm=I=-18:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
video=out/'icecube-news-portrait.mp4'
subprocess.run([a.ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(out/'icecube-news-silent.mp4'),'-i',str(wav),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-af',norm,'-ar',str(RATE),'-t','15','-movflags','+faststart',str(video)],check=True,timeout=90)
evidence={'events':ledger,'sample_rate':RATE,'channels':2,'pre_master_peak_dbfs':20*math.log10(peak),'pre_master_rms_dbfs':20*math.log10(float(np.sqrt(np.mean(bed**2)))),'first_pass':m,'target_lufs':-18,'listened':False,'scope':'Original synthesized ambient score and illustrative event sound; no real detector recording or narration','video':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest()}
(out/'sound-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'events':len(ledger),'video':str(video)},ensure_ascii=False))
