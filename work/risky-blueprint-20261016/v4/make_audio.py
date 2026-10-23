"""Deterministic original stereo instrumental; no speech assets are opened."""
import hashlib, json, subprocess, sys, wave
from pathlib import Path
import numpy as np

R = Path(__file__).resolve().parent
FF = str(R.parents[2]/'node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
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

# A quiet, deliberate 120 BPM score. Picture and score share event contacts.
def felt(note,length=1.5):
    t=ts(length);f=freq(note)
    sig=(np.sin(2*np.pi*f*t+1.3*np.sin(2*np.pi*f*2*t)*np.exp(-t*7))
         +.18*np.sin(2*np.pi*f*3*t)*np.exp(-t*9))
    return sig*env(t,.004,3.4)*np.minimum((length-t)/.12,1)*.14

def mallet(note,length=.8):
    t=ts(length);f=freq(note)
    return (np.sin(2*np.pi*f*t)+.2*np.sin(2*np.pi*f*3.97*t)*np.exp(-t*10))*env(t,.002,6)*.14

chords=[[50,57,62,65,76],[46,53,58,62,69],[48,55,60,65,74],[45,52,57,62,69],
        [50,57,62,65,76],[46,53,58,62,69],[48,55,60,64,74],[45,52,57,62,69],
        [46,53,58,62,69],[50,57,62,65,76]]
levels=[.36,.48,.56,.40,.42,.30,.68,.80,.52,.32]
for bar,notes in enumerate(chords):
    at=bar*8;level=levels[bar]
    # Rich sustain with an eight-second phrase. Keep transients clearly distinct.
    add(music,at,pad(notes[1:],min(8.6,80-at)),gain=1.4*level,kind='phrase-harmony')
    motif=[notes[2]+12,notes[3]+12,notes[1]+12,notes[2]+12]
    for j,offset in enumerate([0,2,4,6]):
        add(music,at+offset,felt(motif[j],1.85),gain=.75*level,pan=[-.2,.15,-.12,.2][j],kind='theme')
    for beat in range(16):
        when=at+beat*.5
        # Solid half-time pulse; avoid the previous constant busy dance beat.
        if beat%4==0:
            add(music,when,kick(),gain=.25*level,kind='pulse')
            add(music,when,bass(notes[0]-12,1.4),gain=.55*level,kind='bass')
        if beat%4==2:add(music,when,snare(),gain=.11*level,pan=.12,kind='soft-rim')
        if 48<=when<64:
            add(music,when,hat(),gain=.17*level,pan=(-.15 if beat%2 else .15),kind='clock')
            if beat%2:add(music,when,mallet(notes[1+beat%3]+12),gain=.33*level,pan=(-.22 if beat%4==1 else .22),kind='counterpoint')
        elif beat%2==0 and 8<=when<72:
            add(music,when,hat(),gain=.07*level,pan=.1,kind='quiet-clock')

# Beat-aligned stereo echoes from the tonal bed; no off-grid 0.19s delays.
for delay,gain in [(.25,.10),(.5,.06),(.75,.025)]:
    k=round(delay*SR);music[k:]+=music[:-k,::-1].copy()*gain

# Deliberate breath before lock, assumption-change, and archive contact.
for anchor in [10,18,36,44,52,62,64,68,75]:
    a,b=round((anchor-.18)*SR),round(anchor*SR)
    u=np.linspace(0,1,b-a)
    music[a:b]*=(1-.82*np.sin(u*np.pi/2)**2)[:,None]

for event in score['events']:
    at=event['at'];eid=event['id'];kind=event['sound']
    if kind=='lock':
        t=ts(.18)
        metal=(np.sin(2*np.pi*970*t)+.27*np.sin(2*np.pi*2340*t))*env(t,.0015,35)*.12
        add(fx,at,metal,gain=.65,kind='contact',event=eid)
        add(accents,at,mallet(event['note']),gain=.6,kind='contact-tone',event=eid)
    elif kind=='scan':
        t=ts(.8);noise=rng.normal(0,1,len(t));smooth=np.convolve(noise,np.ones(31)/31,mode='same')
        add(fx,at-.8,smooth*np.sin(np.pi*t/.8)**2*.045,kind='scan-approach')
        add(accents,at,felt(event['note'],1),gain=.6,kind='scan-arrival',event=eid)
    elif kind=='resolve':
        add(accents,at,pad([50,57,62,65,76],4.8),gain=1.8,kind='resolve-chord',event=eid)
        add(accents,at,felt(74,2),gain=.8,kind='resolve-note',event=eid)
    else:
        add(accents,at,mallet(event['note']+12),gain=.75 if kind=='drop' else .55,kind='action-note',event=eid)
        if kind in ['drop','bell']:add(accents,at,kick(),gain=.30 if kind=='drop' else .15,kind='action-pulse',event=eid)

# Three anticipation notes lead into the new-hypothesis contact on beat 104.
for i,note in enumerate([62,65,69]):
    add(music,50.5+i*.5,mallet(note+12),gain=.25+i*.12,pan=-.2+i*.2,kind='assumption-pickup')

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
assert all(not s.get('voiceover') for s in plan['shots'])
sync=[]
for e in score['events']:
    triggers=[x for x in ledger if x['event']==e['id']]
    assert triggers, e['id']
    error=min(abs(x['sample']/SR-e['at']) for x in triggers)
    assert error<=1/SR
    sync.append({'id':e['id'],'visual_seconds':e['at'],'audio_sample':round(e['at']*SR),'error_ms':error*1000,'action':e['id']})
timing={'duration':duration,'sample_rate':SR,'channels':2,'provider':'Original deterministic instrumental synthesis','voiceover':False,'speech_assets_read':0,'narration_captions':False,'entries':[], 'peak':float(np.max(np.abs(data))),'loudness':result,'phrases':score['phrases'],'action_sync':sync,'sound_ledger':ledger,'listening_verified':False,'mix_sha256':hashlib.sha256((R/'audio/mix.wav').read_bytes()).hexdigest()}
(R/'audio/timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:timing[k] for k in ['duration','channels','peak','loudness','voiceover','speech_assets_read']},ensure_ascii=False))
