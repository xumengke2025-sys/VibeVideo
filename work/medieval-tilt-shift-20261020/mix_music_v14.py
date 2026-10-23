"""Scene-shaped original ambience beneath the unchanged user music excerpt."""
from pathlib import Path
import json, subprocess, wave, io, math
import numpy as np
ROOT=Path(__file__).resolve().parent; A=ROOT/'audio'
FF='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
SR=48000; DURATION=76; N=SR*DURATION; rng=np.random.default_rng(14022)
t=np.arange(N)/SR
raw=subprocess.check_output([FF,'-v','error','-ss','29.5','-i',str(A/'user-provided-Dream-Of-Babylon.mp3'),'-t','76','-ac','2','-ar',str(SR),'-c:a','pcm_s16le','-f','wav','pipe:1'])
with wave.open(io.BytesIO(raw)) as w: music=np.frombuffer(w.readframes(N),dtype='<i2').reshape(-1,2).astype(np.float32)/32768
assert len(music)==N
def noise(n,lo,hi):
    a=rng.normal(0,1,n); f=np.fft.rfftfreq(n,1/SR)
    filt=(1-np.exp(-(f/max(1,lo))**2))/(1+(f/hi)**4)
    a=np.fft.irfft(np.fft.rfft(a)*filt,n)
    return (a/(np.std(a)+1e-9)).astype(np.float32)
def curve(points):
    # Cosine transitions avoid gain corners at picture cuts.
    out=np.zeros(N,np.float32)
    for (a,x),(b,y) in zip(points,points[1:]):
        sel=(t>=a)&(t<b); u=(t[sel]-a)/(b-a); out[sel]=x+(y-x)*(.5-.5*np.cos(u*np.pi))
    out[t>=points[-1][0]]=points[-1][1]
    return out
env=np.zeros_like(music);events=[]
wind_gain=curve([(0,.0006),(7,.0012),(16,.0009),(27,.0007),(37,.0008),(53,.0006),(62,.0004),(68,.001),(73,.0005),(76,0)])
wind=noise(N,40,650)
env[:,0]+=wind*wind_gain;env[:,1]+=np.roll(wind,1301)*wind_gain*.92
water_gain=curve([(0,.0001),(25.8,.0002),(28,.0045),(34.5,.0045),(37.5,.0002),(66,.0002),(70,.0007),(76,0)])
water=noise(N,220,2600)*(.80+.12*np.sin(t*2.2)+.08*np.sin(t*4.7))
env[:,0]+=water*water_gain*.85;env[:,1]+=np.roll(water,3113)*water_gain
def put(at,sound,gain,pan,label):
    start=round(at*SR); n=min(len(sound),N-start)
    if n<=0:return
    env[start:start+n]+=sound[:n,None]*gain*np.array([math.cos(pan*math.pi/2),math.sin(pan*math.pi/2)])
    events.append({'time':round(at,3),'kind':label,'gain':gain,'pan':pan})
# Irregular quiet stone footfall texture in the market, spatially varied.
at=16.45
while at<26.7:
    tt=np.arange(round(.14*SR))/SR
    sound=noise(len(tt),180,1800)*np.exp(-tt*43)*(1-np.exp(-tt*850))
    put(at,sound,.0022,float(rng.uniform(.22,.78)),'market footfall texture')
    at+=float(rng.uniform(.32,.72))
# Low, soft water laps follow the canal scene, without conspicuous splashes.
for at,pan in [(28.7,.70),(30.1,.24),(32.4,.65),(34.8,.35)]:
    tt=np.arange(round(.85*SR))/SR
    sound=noise(len(tt),150,2800)*np.sin(np.pi*tt/.85)**2
    put(at,sound,.0017,pan,'quay water lap')
# Dish rests at 61.2s. Ceramic contact has a short soft body and slight ring.
tt=np.arange(round(.32*SR))/SR
contact=.45*np.sin(math.tau*1350*tt)*np.exp(-tt*34)+.25*np.sin(math.tau*2270*tt)*np.exp(-tt*45)+.3*noise(len(tt),350,2700)*np.exp(-tt*70)
contact*=1-np.exp(-tt*2200)
put(61.2,contact,.005,.5,'offering dish contacts altar')
fade=np.sin(np.minimum(t/.15,1)*np.pi/2)**2*np.sin(np.clip((DURATION-t)/3,0,1)*np.pi/2)**2
env*=fade[:,None];mix=music*fade[:,None]+env
mix*=min(1,.9/float(np.max(np.abs(mix))))
def save(path,data):
    with wave.open(str(path),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(data,-.999,.999)*32767).astype('<i2').tobytes())
save(A/'ambience-v14.wav',env);save(A/'music-v14-raw.wav',mix)
result=subprocess.run([FF,'-y','-hide_banner','-i',str(A/'music-v14-raw.wav'),'-af','loudnorm=I=-17:TP=-1.5:LRA=13:print_format=json','-ar','48000','-c:a','pcm_s24le',str(A/'final-mix-v14.wav')],capture_output=True,text=True,encoding='utf8',check=True)
measure=json.JSONDecoder().raw_decode(result.stderr[result.stderr.rfind('{'):])[0]
sections=[]
for label,a,b in [('opening',0,8),('gate',8,16),('market',16,27),('canal',27,36.5),('garden',36.5,44.5),('statue',44.5,53.5),('ritual',53.5,62.2),('return',62.2,67.6),('panorama',67.6,76)]:
    s=slice(round(a*SR),round(b*SR)); rms=lambda x:float(np.sqrt(np.mean(x*x)))
    sections.append({'scene':label,'range':[a,b],'music_rms':rms(music[s]),'ambience_rms':rms(env[s]),'ambience_relative_db':20*math.log10(max(rms(env[s]),1e-12)/max(rms(music[s]),1e-12))})
evidence={'duration':76,'source_excerpt':[29.5,105.5],'fade_in':.15,'fade_out':[73,76],'ambience':'original deterministic synthesis: scene-shaped wind, water, quiet stone footfalls and altar contact; no synthesized speech or claimed crowd recording','events':events,'scene_levels':sections,'loudness':measure,'actual_listening':False,'limitation':'Technical mix measurements only; no perceptual loudness, timbre or synchronization approval.'}
(A/'mix-v14-evidence.json').write_text(json.dumps(evidence,indent=2),encoding='utf8')
print('V14_AUDIO_READY',json.dumps({'loudness':measure,'scenes':sections}))
