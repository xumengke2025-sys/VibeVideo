"""Synthesize original event foley, ambience bed and SRT from the SAME clip contract.
No TTS, no external audio, no real recordings. Requires numpy.
Generation does not imply listening acceptance."""
import argparse, hashlib, json, math, re, subprocess, wave
from pathlib import Path
import numpy as np

RATE = 48000

def timestamp(t):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

def synth(e, seed):
    d=e['sound']['duration'];kind=e['sound']['kind'];n=round(d*RATE);t=np.arange(n)/RATE
    rng=np.random.default_rng(seed);noise=rng.normal(0,1,n)
    fade=np.minimum(t/.02,1)*np.minimum((d-t)/.08,1)
    def ma(k): return np.convolve(noise,np.ones(k)/k,'same')
    if kind=='spark':
        x=np.zeros(n);ticks=max(2,int(d*2.5))
        for i in range(ticks):
            st=int(rng.uniform(0,max(d-.02,.001))*RATE);ln=int(.008*RATE);seg=np.arange(ln)/RATE
            tick=(np.sin(2*np.pi*5200*seg)*.5+np.sin(2*np.pi*3600*seg)*.3)*np.exp(-seg*900)
            en=min(n,st+ln);x[st:en]+=tick[:en-st]*float(rng.uniform(.6,1.0))
        x*=.5
    elif kind=='rumble':
        body=np.sin(2*np.pi*27*t+1.8*np.sin(2*np.pi*.25*t))+.6*np.sin(2*np.pi*41*t+.7*t)
        env=np.sin(np.pi*np.clip(t/d,0,1))**2.2
        x=(body*.5+ma(601)*.42)*env
    elif kind=='air':
        env=np.sin(np.pi*np.clip(t/d,0,1))**1.5
        x=(ma(301)*.8+np.sin(2*np.pi*55*t)*.10)*env
    elif kind=='gulp':
        up=np.minimum(t/.16,1.0);down=np.exp(-np.maximum(t-.16,0)*3.4)
        water=ma(241)*up*down*.95
        glug=np.sin(2*np.pi*(115*t-26*t*t))*np.exp(-np.maximum(t-.12,0)*4.2)*.6
        x=(water+glug)*up
    elif kind=='spray':
        hp=noise-ma(17)
        env=np.exp(-t*1.05)*(0.72+0.28*np.sin(2*np.pi*3.1*t))
        x=hp*.55*env
    elif kind=='stamp':
        x=(np.sin(2*np.pi*(100*t-35*t*t))*.7+noise*.14)*np.exp(-t*22)
    elif kind=='thump':
        x=(np.sin(2*np.pi*52*t)*.85*np.exp(-t*8)+np.sin(2*np.pi*36*t)*.5*np.exp(-t*4.6)+noise*.12*np.exp(-t*120))
    elif kind=='moan':
        f=88-46*np.clip(t/d,0,1)
        phase=2*np.pi*np.cumsum(f)/RATE
        env=np.minimum(t/.55,1)*np.minimum(np.maximum(d-t,0)/1.15,1)
        x=(np.sin(phase)*(1+.22*np.sin(2*np.pi*4.3*t))+.35*np.sin(2*phase)+.12*np.sin(3*phase))*env*.62
    else: raise ValueError('Unknown sound '+kind)
    return x*fade*e['sound']['gain']

def bed(plan):
    d=plan['duration'];n=round(d*RATE);t=np.arange(n)/RATE
    rng=np.random.default_rng(plan['seed']+97);noise=rng.normal(0,1,n)
    b=np.convolve(noise,np.ones(901)/901,'same')*.38+np.sin(2*np.pi*24*t)*.06
    b*=(.8+.2*np.sin(2*np.pi*.07*t))
    return b*.55

def build(plan):
    mix=bed(plan);ledger=[{'event':'ambience-bed','visual_at':0,'at':0,'sample':0,'duration':plan['duration'],'kind':'bed'}]
    for i,e in enumerate(plan['events']):
        if not e.get('sound'): continue
        at=e['at']+e['sound'].get('offset',0)
        x=synth(e,plan['seed']+i);a=round(at*RATE);b=min(len(mix),a+len(x));mix[a:b]+=x[:b-a]
        ledger.append({'event':e['id'],'visual_at':e['at'],'at':at,'sample':a,'duration':e['sound']['duration'],'kind':e['sound']['kind']})
    for a,b in plan.get('silences',[]):
        ia,ib=round(a*RATE),round(b*RATE);fade=240
        if ia>=fade:mix[ia-fade:ia]*=np.linspace(1,0,fade)
        mix[ia:ib]=0
        if ib+fade<=len(mix):mix[ib:ib+fade]*=np.linspace(0,1,fade)
    return mix,ledger

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--clip',default='whale');ap.add_argument('--out',type=Path);ap.add_argument('--ffmpeg');ap.add_argument('--lufs',type=float,default=-18);a=ap.parse_args()
    root=Path(__file__).parent;plan=json.loads((root/'clips'/f'{a.clip}.json').read_text(encoding='utf-8'))
    out=a.out or root/'out'/a.clip;out.mkdir(parents=True,exist_ok=True);mix,ledger=build(plan)
    peak=float(np.max(np.abs(mix)));assert math.isfinite(peak) and peak<1,'Clipping/NaN'
    wav=out/'sound.wav'
    with wave.open(str(wav),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(RATE);f.writeframes((mix*32767).astype('<i2').tobytes())
    srt='\n\n'.join(f"{i+1}\n{timestamp(c['start'])} --> {timestamp(c['end'])}\n{c['text']}" for i,c in enumerate(plan['captions']))
    if srt:(out/(a.clip+'.srt')).write_text(srt+'\n',encoding='utf-8')
    evidence={'clip':a.clip,'sample_rate':RATE,'events':ledger,'pre_master_peak_dbfs':20*math.log10(max(peak,1e-12)),
              'pre_master_rms_dbfs':20*math.log10(max(float(np.sqrt(np.mean(mix*mix))),1e-12)),
              'silences':plan.get('silences',[]),'listened':False,
              'scope':'Original synthesized ambience and event foley; no narration, no music, no external recordings.'}
    if a.ffmpeg:
        output=out/(a.clip+'.mp4')
        first=subprocess.run([a.ffmpeg,'-hide_banner','-i',str(wav),'-af',f'loudnorm=I={a.lufs}:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True,timeout=60)
        measurements=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',first.stderr)[-1])
        if not all(math.isfinite(float(measurements[k])) for k in ('input_i','input_tp','input_lra','input_thresh','target_offset')):raise ValueError('Nonfinite loudness measurement')
        norm=(f"loudnorm=I={a.lufs}:TP=-1.5:LRA=11:measured_I={measurements['input_i']}:"
              f"measured_TP={measurements['input_tp']}:measured_LRA={measurements['input_lra']}:"
              f"measured_thresh={measurements['input_thresh']}:offset={measurements['target_offset']}:linear=true")
        subprocess.run([a.ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(out/(a.clip+'-silent.mp4')),'-i',str(wav),
                        '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-af',norm,'-ar',str(RATE),'-shortest','-movflags','+faststart',str(output)],check=True,timeout=90)
        evidence['master']={'target_lufs':a.lufs,'target_true_peak_db':-1.5,'first_pass':measurements}
        evidence['video']={'file':str(output),'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}
    (out/'sound-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'clip':a.clip,'events':len(ledger),'peak_dbfs':evidence['pre_master_peak_dbfs'],'output':str(out)},ensure_ascii=False))
if __name__=='__main__':main()
