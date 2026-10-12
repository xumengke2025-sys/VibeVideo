"""Synthesize event foley + ambience bed from the SAME clip contract, optionally mix synthetic narration
(edge-tts, declared in narration.json), then master and mux. No music, no cloned human voice.
Generation does not imply listening acceptance. Requires numpy."""
import argparse, hashlib, json, math, re, subprocess, wave, tempfile
from pathlib import Path
import numpy as np

RATE = 48000

def timestamp(t):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

def synth(e, seed):
    d=e['sound']['duration'];kind=e['sound']['kind'];n=round(d*RATE);t=np.arange(n)/RATE
    rng=np.random.default_rng(seed);noise=rng.normal(0,1,n)
    fade=np.minimum(t/.012,1)*np.minimum((d-t)/.05,1)
    def ma(k): return np.convolve(noise,np.ones(k)/k,'same')
    if kind=='paper':
        smooth=np.convolve(noise,np.ones(5)/5,'same')
        x=(noise-smooth)*.12*(.65+.35*np.sin(2*np.pi*7*t)**2)
    elif kind=='click':
        x=(np.sin(2*np.pi*1800*t)*.6+np.sin(2*np.pi*3100*t)*.2+noise*.12)*np.exp(-t*65)
    elif kind=='stamp':
        x=(np.sin(2*np.pi*(100*t-35*t*t))*.7+noise*.14)*np.exp(-t*22)
    elif kind=='flow':
        x=np.convolve(noise,np.ones(23)/23,'same')*.75*(.8+.2*np.sin(2*np.pi*.7*t))
    elif kind=='tone':
        f=e['sound'].get('frequency',330)
        x=(np.sin(2*np.pi*f*t)+.2*np.sin(2*np.pi*2*f*t))*np.exp(-t*8)
    elif kind=='tick':
        x=(np.sin(2*np.pi*2600*t)*.5+np.sin(2*np.pi*3900*t)*.2)*np.exp(-t*90)
    elif kind=='whoosh':
        env=np.sin(np.pi*np.clip(t/d,0,1))**1.6
        sweep=ma(41)-ma(9)  # broadband band-pass character
        x=(ma(61)*.55+sweep*.55)*env*.9
    elif kind=='pluck':
        f=e['sound'].get('frequency',440)
        x=(np.sin(2*np.pi*f*t)*.7+np.sin(2*np.pi*2*f*t)*.22+np.sin(2*np.pi*3*f*t)*.08)*np.exp(-t*4.2)
    elif kind=='chime':
        f=e['sound'].get('frequency',523)
        env=np.minimum(t/.05,1)*np.exp(-t*2.4)
        x=(np.sin(2*np.pi*f*t)*.5+np.sin(2*np.pi*f*1.5*t)*.28+np.sin(2*np.pi*f*2.0*t)*.18)*env
    elif kind=='sub':
        x=(np.sin(2*np.pi*46*t)*.8+np.sin(2*np.pi*31*t)*.4)*np.exp(-t*3.2)
    else: raise ValueError('Unknown sound '+kind)
    return x*fade*e['sound']['gain']

def bed(plan):
    d=plan['duration'];n=round(d*RATE);t=np.arange(n)/RATE
    rng=np.random.default_rng(plan['seed']+97);noise=rng.normal(0,1,n)
    b=np.convolve(noise,np.ones(901)/901,'same')*.34+np.sin(2*np.pi*30*t)*.05
    b*=(.8+.2*np.sin(2*np.pi*.05*t))
    return b*.5

def decode_mp3(ffmpeg, src, dst):
    subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(src),'-ac','1','-ar',str(RATE),'-c:a','pcm_s16le',str(dst)],check=True,timeout=60)

def load_wav(path):
    with wave.open(str(path),'rb') as w:
        data=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768.0
    return data

def build(plan, root, ffmpeg, narration):
    n=round(plan['duration']*RATE)
    mix=bed(plan);ledger=[{'event':'ambience-bed','visual_at':0,'at':0,'sample':0,'duration':plan['duration'],'kind':'bed'}]
    for i,e in enumerate(plan['events']):
        if not e.get('sound'): continue
        at=e['at']+e['sound'].get('offset',0)
        x=synth(e,plan['seed']+i);a=round(at*RATE);b=min(len(mix),a+len(x));mix[a:b]+=x[:b-a]
        ledger.append({'event':e['id'],'visual_at':e['at'],'at':at,'sample':a,'duration':e['sound']['duration'],'kind':e['sound']['kind']})
    voice_records=[]
    if narration:
        tmp=Path(tempfile.mkdtemp(prefix='entropy-narration-'))
        placed={c.get('file'):c for c in plan.get('narration',[])}
        for cue in narration:
            src=root/cue['file'];dst=tmp/(Path(cue['file']).stem+'.wav')
            decode_mp3(ffmpeg,src,dst);data=load_wav(dst)
            ref=placed.get(cue['file'],{})
            start=cue.get('start',ref.get('start',0));end=cue.get('end',ref.get('end',round(start+len(data)/RATE,3)))
            a=round(start*RATE);b=min(len(mix),a+len(data));mix[a:b]+=data[:b-a]
            voice_records.append({'file':cue['file'],'start':start,'end':end,
                'samples':int(len(data)),'measured_duration':round(len(data)/RATE,3),'declared_duration':cue.get('duration'),
                'fits_declared':abs(len(data)/RATE-cue.get('duration',len(data)/RATE))<=0.15})
        ledger.append({'event':'narration','files':len(narration),'voice':'zh-CN-YunxiNeural','synthetic':True})
    for a,b in plan.get('silences',[]):
        ia,ib=round(a*RATE),round(b*RATE);fade=240
        if ia>=fade:mix[ia-fade:ia]*=np.linspace(1,0,fade)
        mix[ia:ib]=0
        if ib+fade<=len(mix):mix[ib:ib+fade]*=np.linspace(0,1,fade)
    return mix,ledger,voice_records

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--clip',default='entropy');ap.add_argument('--out',type=Path);ap.add_argument('--ffmpeg');ap.add_argument('--lufs',type=float,default=-16);a=ap.parse_args()
    root=Path(__file__).parent;plan=json.loads((root/'clips'/f'{a.clip}.json').read_text(encoding='utf-8'))
    narration=None
    nar_path=root/'narration.json'
    if plan.get('narration') and nar_path.is_file():
        narration=json.loads(nar_path.read_text(encoding='utf-8'))
        for cue in narration:
            if not (root/cue['file']).is_file(): raise SystemExit(f"Missing narration file {cue['file']}")
    out=a.out or root/'out'/a.clip;out.mkdir(parents=True,exist_ok=True)
    mix,ledger,voice_records=build(plan,root,a.ffmpeg,narration)
    peak=float(np.max(np.abs(mix)));assert math.isfinite(peak) and peak<1,'Clipping/NaN'
    wav=out/'sound.wav'
    with wave.open(str(wav),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(RATE);f.writeframes((mix*32767).astype('<i2').tobytes())
    srt='\n\n'.join(f"{i+1}\n{timestamp(c['start'])} --> {timestamp(c['end'])}\n{c['text']}" for i,c in enumerate(plan['captions']))
    if srt:(out/(a.clip+'.srt')).write_text(srt+'\n',encoding='utf-8')
    evidence={'clip':a.clip,'sample_rate':RATE,'events':ledger,'voice_synthesis':voice_records,
              'pre_master_peak_dbfs':20*math.log10(max(peak,1e-12)),
              'pre_master_rms_dbfs':20*math.log10(max(float(np.sqrt(np.mean(mix*mix))),1e-12)),
              'silences':plan.get('silences',[]),'listened':False,
              'scope':'Original synthesized foley and ambience; narration is a public synthetic voice (edge-tts) declared in narration.json; no music, no cloned human voice.'}
    if a.ffmpeg:
        output=out/(a.clip+'.mp4')
        first=subprocess.run([a.ffmpeg,'-hide_banner','-i',str(wav),'-af',f'loudnorm=I={a.lufs}:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True,timeout=90)
        measurements=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',first.stderr)[-1])
        if not all(math.isfinite(float(measurements[k])) for k in ('input_i','input_tp','input_lra','input_thresh','target_offset')):raise ValueError('Nonfinite loudness measurement')
        norm=(f"loudnorm=I={a.lufs}:TP=-1.5:LRA=11:measured_I={measurements['input_i']}:"
              f"measured_TP={measurements['input_tp']}:measured_LRA={measurements['input_lra']}:"
              f"measured_thresh={measurements['input_thresh']}:offset={measurements['target_offset']}:linear=true")
        subprocess.run([a.ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(out/(a.clip+'-silent.mp4')),'-i',str(wav),
                        '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-af',norm,'-ar',str(RATE),'-shortest','-movflags','+faststart',str(output)],check=True,timeout=180)
        evidence['master']={'target_lufs':a.lufs,'target_true_peak_db':-1.5,'first_pass':measurements}
        evidence['video']={'file':str(output),'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}
    (out/'sound-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'clip':a.clip,'events':len(ledger),'voice_cues':len(voice_records),'peak_dbfs':evidence['pre_master_peak_dbfs'],'output':str(out)},ensure_ascii=False))
if __name__=='__main__':main()
