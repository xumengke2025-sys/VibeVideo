"""Scene-shaped original ambience beneath the unchanged user music excerpt."""
from pathlib import Path
import json, subprocess, wave, io, math
import numpy as np
ROOT=Path(__file__).resolve().parent; A=ROOT/'audio'
FF='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
SR=48000; DURATION=90; N=SR*DURATION; rng=np.random.default_rng(14022)
t=np.arange(N)/SR
raw=subprocess.check_output([FF,'-v','error','-ss','29.5','-i',str(A/'user-provided-Dream-Of-Babylon.mp3'),'-t','90','-ac','2','-ar',str(SR),'-c:a','pcm_s16le','-f','wav','pipe:1'])
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
wind_gain=curve([(0,.0006),(7,.0012),(16,.0009),(27,.0007),(37,.0008),(53,.0006),(62,.0004),(68,.001),(87,.0005),(90,0)])
wind=noise(N,40,650)
env[:,0]+=wind*wind_gain;env[:,1]+=np.roll(wind,1301)*wind_gain*.92
water_gain=curve([(0,.0001),(30,.0002),(32,.0045),(42,.0045),(45,.0002),(66,.0002),(70,.0007),(90,0)])
water=noise(N,220,2600)*(.80+.12*np.sin(t*2.2)+.08*np.sin(t*4.7))
env[:,0]+=water*water_gain*.85;env[:,1]+=np.roll(water,3113)*water_gain
def put(at,sound,gain,pan,label):
    start=round(at*SR); n=min(len(sound),N-start)
    if n<=0:return
    env[start:start+n]+=sound[:n,None]*gain*np.array([math.cos(pan*math.pi/2),math.sin(pan*math.pi/2)])
    events.append({'time':round(at,3),'kind':label,'gain':gain,'pan':pan})
# Irregular quiet stone footfall texture in the market, spatially varied.
at=19.45
while at<30.7:
    tt=np.arange(round(.14*SR))/SR
    sound=noise(len(tt),180,1800)*np.exp(-tt*43)*(1-np.exp(-tt*850))
    put(at,sound,.0022,float(rng.uniform(.22,.78)),'market footfall texture')
    at+=float(rng.uniform(.32,.72))
# Low, soft water laps follow the canal scene, without conspicuous splashes.
for at,pan in [(32.7,.70),(35.1,.24),(38.4,.65),(42.1,.35)]:
    tt=np.arange(round(.85*SR))/SR
    sound=noise(len(tt),150,2800)*np.sin(np.pi*tt/.85)**2
    put(at,sound,.0017,pan,'quay water lap')
# Dish rests at 61.2s. Ceramic contact has a short soft body and slight ring.
tt=np.arange(round(.32*SR))/SR
contact=.45*np.sin(math.tau*1350*tt)*np.exp(-tt*34)+.25*np.sin(math.tau*2270*tt)*np.exp(-tt*45)+.3*noise(len(tt),350,2700)*np.exp(-tt*70)
contact*=1-np.exp(-tt*2200)
put(61.2*90/76,contact,.005,.5,'offering dish contacts altar')

# Quiet speed-shaped tyre and cloth layers, plus two restrained brass bell cues.
import v15_route as route
keyt=np.arange(0,DURATION+1/24,1/24);speeds=np.array([route.state(float(x))['speed'] for x in keyt]);velocity=np.interp(t,keyt,speeds)
rolling=noise(N,350,2200)*np.minimum(1,velocity/4)*.0013
env[:,0]+=rolling;env[:,1]+=np.roll(rolling,203)*.88
for at in [12.65,24.1,35.2]:
 tt=np.arange(round(.8*SR))/SR
 bell=(np.sin(math.tau*1470*tt)*np.exp(-tt*5)+.45*np.sin(math.tau*2967*tt)*np.exp(-tt*9)+.2*np.sin(math.tau*4123*tt)*np.exp(-tt*13))*(1-np.exp(-tt*3500))
 put(at,bell,.0038,.48,'bicycle brass bell')
tt=np.arange(round(.45*SR))/SR
put(65.4,noise(len(tt),700,3200)*np.sin(math.pi*tt/.45)**2,.0017,.5,'gentle bicycle braking')

fade=np.sin(np.minimum(t/.15,1)*np.pi/2)**2*np.sin(np.clip((DURATION-t)/3,0,1)*np.pi/2)**2
env*=fade[:,None];mix=music*fade[:,None]+env
mix*=min(1,.9/float(np.max(np.abs(mix))))
def save(path,data):
    with wave.open(str(path),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(data,-.999,.999)*32767).astype('<i2').tobytes())
save(A/'ambience-v15.wav',env);save(A/'music-v15-raw.wav',mix)
result=subprocess.run([FF,'-y','-hide_banner','-i',str(A/'music-v15-raw.wav'),'-af','loudnorm=I=-17:TP=-1.5:LRA=13:print_format=json','-ar','48000','-c:a','pcm_s24le',str(A/'final-mix-v15.wav')],capture_output=True,text=True,encoding='utf8',check=True)
measure=json.JSONDecoder().raw_decode(result.stderr[result.stderr.rfind('{'):])[0]
sections=[]
for label,a,b in [('opening',0,8),('gate',8,19),('market',19,31),('canal',31,44),('garden',44,55),('temple approach',55,64),('ritual',64,74),('return',74,81),('panorama',81,90)]:
    s=slice(round(a*SR),round(b*SR)); rms=lambda x:float(np.sqrt(np.mean(x*x)))
    sections.append({'scene':label,'range':[a,b],'music_rms':rms(music[s]),'ambience_rms':rms(env[s]),'ambience_relative_db':20*math.log10(max(rms(env[s]),1e-12)/max(rms(music[s]),1e-12))})
evidence={'duration':90,'source_excerpt':[29.5,119.5],'fade_in':.15,'fade_out':[87,90],'ambience':'original deterministic synthesis: scene-shaped wind, water, quiet stone footfalls, rolling tyres, brass bicycle bell, gentle braking and altar contact; no synthesized speech or claimed crowd recording','events':events,'scene_levels':sections,'loudness':measure,'actual_listening':False,'limitation':'Technical mix measurements only; no perceptual loudness, timbre or synchronization approval.'}
(A/'mix-v15-evidence.json').write_text(json.dumps(evidence,indent=2),encoding='utf8')
print('V15_AUDIO_READY',json.dumps({'loudness':measure,'scenes':sections}))
