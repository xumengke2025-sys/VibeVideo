"""Deterministic original stereo instrumental; no speech assets are opened."""
import hashlib, json, subprocess, sys, wave
from pathlib import Path
import numpy as np

R = Path(__file__).resolve().parent
sys.path.insert(0, str(R.parent/'tools/python'))
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
plan = json.loads((R/'plan.json').read_text(encoding='utf-8'))
score = plan['soundtrack']
SR = score['sample_rate']; N = round(SR*plan['duration'])
rng = np.random.default_rng(20261013)
music = np.zeros((N,2), dtype=np.float32)
fx = np.zeros_like(music); accents = np.zeros_like(music)
ledger = []

def add(buf, at, signal, gain=1, pan=0, kind=None, event=None):
    k = round(at*SR)
    signal = np.asarray(signal, dtype=np.float32)
    if k < 0: signal=signal[-k:]; k=0
    length = min(len(signal), N-k)
    if length <= 0: return
    signal = signal[:length]
    if signal.ndim == 1:
        # Equal-power pan preserves energy without hard-panning transients.
        buf[k:k+length,0] += signal*gain*np.cos((pan+1)*np.pi/4)
        buf[k:k+length,1] += signal*gain*np.sin((pan+1)*np.pi/4)
    else: buf[k:k+length] += signal*gain
    if kind: ledger.append({'kind':kind,'at':at,'sample':k,'event':event})

def ts(seconds): return np.arange(round(seconds*SR), dtype=np.float64)/SR
def freq(midi): return 440*2**((midi-69)/12)
def env(t, attack=.005, decay=5): return (1-np.exp(-t/attack))*np.exp(-t*decay)

def kick():
    t=ts(.48); phase=2*np.pi*(48*t+78*.025*(1-np.exp(-t/.025)))
    a=np.sin(phase)*np.exp(-t*9)*np.minimum(t/.001,1)
    a+=rng.normal(0,1,len(t))*.10*np.exp(-t*350)
    return np.tanh(a*1.7)*.72

def snare():
    t=ts(.21); noise=rng.normal(0,1,len(t))
    high=noise-np.convolve(noise,np.ones(7)/7,mode='same')
    tone=np.sin(2*np.pi*182*t)*np.exp(-t*27)
    return (high*.30*np.exp(-t*23)+tone*.20)*np.minimum(t/.0008,1)

def hat(opened=False):
    t=ts(.18 if opened else .047); noise=rng.normal(0,1,len(t))
    high=noise-np.convolve(noise,np.ones(9)/9,mode='same')
    return high*np.exp(-t*(25 if opened else 90))*.10*np.minimum(t/.0006,1)

def bass(note, length):
    t=ts(length); f=freq(note)
    a=np.sin(2*np.pi*f*t)+.24*np.sin(2*np.pi*f*2*t)+.08*np.sin(2*np.pi*f*3*t)
    return np.tanh(a*1.15)*env(t,.006,3.7)*np.minimum((length-t)/.045,1)*.32

def pluck(note, length=.5, bright=1):
    t=ts(length); f=freq(note)
    a=np.sin(2*np.pi*f*t)+.30*bright*np.sin(2*np.pi*f*2*t)+.12*bright*np.sin(2*np.pi*f*3*t)
    return a*env(t,.003,8.5)*.13*np.minimum((length-t)/.04,1)

def bell(note):
    t=ts(.8); f=freq(note)
    return (np.sin(2*np.pi*f*t)*np.exp(-t*6)+.23*np.sin(2*np.pi*f*2.003*t)*np.exp(-t*12))*np.minimum(t/.002,1)*.15

def pad(notes, length):
    t=ts(length); stereo=np.zeros((len(t),2))
    envelope=np.minimum(t/.38,1)*np.minimum((length-t)/.6,1)
    for i,note in enumerate(notes):
        f=freq(note)
        for channel,detune in enumerate([-.003,.003]):
            stereo[:,channel] += (np.sin(2*np.pi*f*(1+detune)*t+i*.7)+.16*np.sin(2*np.pi*f*2*t))*envelope*.023
    return stereo

def density(at):
    return next((s['gain'] for s in score['density'] if s['start']<=at<s['end']),.18)

chords=[[62,65,69,76],[58,62,65,69],[60,65,69,74],[60,64,67,74]]
roots=[38,34,41,36]
# Sustained harmony crosses scene boundaries; phrased drums remain action-anchored.
for i,at in enumerate(np.arange(0,88,6.4)):
    notes=chords[i%4];length=min(6.7,90-at)
    add(music,at,pad(notes,length),gain=.9,kind='harmony')

beat_times=[]
for phrase_index,phrase in enumerate(score['phrases']):
    step=(phrase['end']-phrase['start'])/phrase['beats']
    phrase['bpm']=60/step
    for beat in range(phrase['beats']):
        at=phrase['start']+beat*step; d=density(at)
        beat_times.append(at)
        chord=chords[(phrase_index+beat//8)%4]; root=roots[(phrase_index+beat//8)%4]
        # Four-on-floor propulsion, with more room for expert and evidence reading.
        if d>.6 or beat%2==0: add(music,at,kick(),gain=.45*d,kind='kick')
        if beat%4 in [1,3]: add(music,at,snare(),gain=.45*d,pan=.08,kind='snare')
        for sub in [0,.5]:
            when=at+sub*step
            add(music,when,hat(),gain=(.32 if sub==0 else .55)*d,pan=(-.3 if sub==0 else .3),kind='hat')
        if beat%4==3 and d>.8: add(music,at+.75*step,hat(True),gain=.25,pan=.2)
        for offset,note in [(0,root),(.75,root+12)] if beat%2==0 else [(.5,root+7)]:
            add(music,at+offset*step,bass(note,step*.65),gain=.78*d,kind='bass')
        # Syncopated filtered plucks form a recognisable recurring phrase.
        pattern=[0,2,1,3,2,1,3,1]
        for sub in [.25,.75]:
            note=chord[pattern[(beat*2+int(sub*2))%8]]+12
            add(music,at+sub*step,pluck(note,step*1.1,bright=.75),gain=(.65 if d>.7 else .25),pan=np.sin(beat*.8)*.45,kind='arp')
        if beat%8 in [0,3,6] and d>.65:
            add(music,at+.5*step,bell(chord[[2,1,3][[0,3,6].index(beat%8)]]+12),gain=.45,pan=-.16)

# Echo repeats are quiet and stereo; only tonal music gets delays, never speech.
for delay,gain in [(.19,.075),(.38,.045),(.57,.025)]:
    k=round(delay*SR)
    music[k:] += music[:-k,::-1].copy()*gain

# Duck the bed under every kick with an analytic short pump.
sidechain=np.ones(N,dtype=np.float32)
for at in beat_times:
    k=round(at*SR); length=min(round(.16*SR),N-k)
    if length>0: sidechain[k:k+length]*=1-.14*np.exp(-np.arange(length)/(SR*.045))
music*=sidechain[:,None]

# Three tiny rests stop the moving mechanism before a firm musical result.
for start,end in score['breaks']:
    k0,k1=round(start*SR),round(end*SR)
    u=np.arange(k1-k0)/max(k1-k0-1,1)
    cut=np.where(u<.10,1-u/.10,.025)
    music[k0:k1]*=cut[:,None]

for event in score['events']:
    at=event['at']; kind=event['sound']; eid=event['id']
    if kind in ['downbeat','drop','accent']:
        add(accents,at,kick(),gain=.42 if kind!='accent' else .23,kind='event-kick',event=eid)
        note=62 if kind=='drop' else 74
        add(accents,at,bell(note),gain=.8 if kind=='drop' else .45,kind='event-tone',event=eid)
        if kind=='drop':
            t=ts(.32); noise=rng.normal(0,1,len(t)); a=noise-np.convolve(noise,np.ones(10)/10,mode='same')
            add(accents,at,a*.025*np.exp(-t*13)*np.minimum(t/.002,1),pan=.08,kind='event-air',event=eid)
    elif kind=='relay': add(accents,at,pluck(event['note'],.65),gain=1.6,pan=0,kind='event-note',event=eid)
    elif kind=='tick':
        t=ts(.09); a=(np.sin(2*np.pi*1860*t)*.10+rng.normal(0,1,len(t))*.026)*np.exp(-t*65)*np.minimum(t/.0007,1)
        add(fx,at,a,gain=.9,pan=0,kind='mechanical-tick',event=eid)
    elif kind=='travel':
        t=ts(.8); noise=rng.normal(0,1,len(t)); smooth=np.convolve(noise,np.ones(17)/17,mode='same')
        add(fx,at,smooth*.055*np.sin(np.pi*t/.8)**2,pan=-.2,kind='rail-air',event=eid)
    elif kind=='resolve':
        add(accents,at,pad([50,62,65,69,76],1.6),gain=2,kind='final-chord',event=eid)
        add(accents,at,bell(74),gain=.6,kind='final-note',event=eid)

# Short pickups terminate exactly at the big contact moments.
for anchor in [b['end'] for b in plan['burdens']]:
    for offset,gain in [(.60,.13),(.40,.18),(.20,.25)]:
        add(music,anchor-offset,snare(),gain=gain,pan=.12,kind='pickup')

music += accents
fade=np.minimum(np.arange(N)/(SR*.06),1)*np.minimum((N-1-np.arange(N))/(SR*.62),1)
music*=fade[:,None]; fx*=fade[:,None]
premix=music+fx
peak=float(np.max(np.abs(premix))); gain=.87/max(peak,.01)
music*=gain; fx*=gain; mix=music+fx
R.joinpath('audio').mkdir(exist_ok=True)
def save(name,data):
    with wave.open(str(R/'audio'/name),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
        w.writeframes(np.rint(np.clip(data,-1,1)*32767).astype('<i2').tobytes())
save('music.wav',music);save('foley.wav',fx);save('premix.wav',mix)
# Two-pass loudness normalisation avoids arbitrary volume and adds true-peak headroom.
first=subprocess.run([FF,'-v','info','-i',str(R/'audio/premix.wav'),'-af','loudnorm=I=-15:TP=-1.5:LRA=9:print_format=json','-f','null','-'],capture_output=True,check=True,timeout=60)
log=first.stderr.decode('utf-8',errors='replace')
stats=json.loads(log[log.rfind('{'):log.rfind('}')+1])
af=f"loudnorm=I=-15:TP=-1.5:LRA=9:measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:offset={stats['target_offset']}:linear=true:print_format=json"
second=subprocess.run([FF,'-v','info','-y','-i',str(R/'audio/premix.wav'),'-af',af,'-ar',str(SR),'-ac','2','-c:a','pcm_s16le',str(R/'audio/mix.wav')],capture_output=True,check=True,timeout=60)
log=second.stderr.decode('utf-8',errors='replace'); result=json.loads(log[log.rfind('{'):log.rfind('}')+1])
with wave.open(str(R/'audio/mix.wav'),'rb') as w:
    data=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2)/32768
    duration=w.getnframes()/w.getframerate()
assert duration==plan['duration'] and np.max(np.abs(data))<.99
assert all(not s['voiceover'] for s in plan['shots'])
sync=[]
for e in score['events']:
    triggers=[x for x in ledger if x['event']==e['id']]
    assert triggers, e['id']
    error=min(abs(x['sample']/SR-e['at']) for x in triggers)
    assert error<=1/SR
    sync.append({'id':e['id'],'visual_seconds':e['at'],'audio_sample':round(e['at']*SR),'error_ms':error*1000,'action':e['action']})
timing={'duration':duration,'sample_rate':SR,'channels':2,'provider':'Original deterministic instrumental synthesis','voiceover':False,'speech_assets_read':0,'narration_captions':False,'entries':[], 'peak':float(np.max(np.abs(data))),'loudness':result,'phrases':score['phrases'],'action_sync':sync,'sound_ledger':ledger,'listening_verified':False,'mix_sha256':hashlib.sha256((R/'audio/mix.wav').read_bytes()).hexdigest()}
(R/'audio/timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:timing[k] for k in ['duration','channels','peak','loudness','voiceover','speech_assets_read']},ensure_ascii=False))
