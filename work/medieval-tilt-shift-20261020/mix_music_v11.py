from pathlib import Path
import json, subprocess, wave, io
import numpy as np
ROOT=Path(__file__).resolve().parent;A=ROOT/'audio'
FF='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
sr=48000;duration=76;n=duration*sr
def read(path,offset=0,duration=76):
    raw=subprocess.check_output([FF,'-v','error','-ss',str(offset),'-i',str(path),'-t',str(duration),'-ac','2','-ar',str(sr),'-c:a','pcm_s16le','-f','wav','pipe:1'])
    with wave.open(io.BytesIO(raw)) as w:return np.frombuffer(w.readframes(sr*duration),dtype='<i2').reshape(-1,2).astype(np.float32)/32768
music=read(A/'user-provided-Dream-Of-Babylon.mp3',29.5)
assert len(music)==n
source=read(A/'ambience.wav');env=np.zeros((n,2),np.float32);weight=np.zeros(n,np.float32)
overlap=2*sr;period=len(source)-overlap
for start in range(0,n,period):
    length=min(len(source),n-start);w=np.ones(length,np.float32)
    if start:w[:min(overlap,length)]=np.linspace(0,1,min(overlap,length))
    if start+length<n:w[-overlap:]=np.linspace(1,0,overlap)
    env[start:start+length]+=source[:length]*w[:,None];weight[start:start+length]+=w
env/=np.maximum(weight[:,None],1e-6)
t=np.arange(n)/sr
fade=np.sin(np.minimum(t/.15,1)*np.pi/2)**2*np.sin(np.maximum(0,np.minimum((duration-t)/3,1))*np.pi/2)**2
mix=(music+env*.25)*fade[:,None]
mix*=min(1,.9/float(np.max(np.abs(mix))))
raw=A/'music-v11-raw.wav'
with wave.open(str(raw),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(mix,-.999,.999)*32767).astype('<i2').tobytes())
result=subprocess.run([FF,'-y','-hide_banner','-i',str(raw),'-af','loudnorm=I=-17:TP=-1.5:LRA=13:print_format=json','-ar','48000','-c:a','pcm_s24le',str(A/'final-mix-v11.wav')],capture_output=True,text=True,encoding='utf8',check=True)
measure=json.JSONDecoder().raw_decode(result.stderr[result.stderr.rfind('{'):])[0]
(A/'mix-v11-evidence.json').write_text(json.dumps({'duration':76,'source_excerpt':[29.5,105.5],'fade_in':.15,'fade_out':[73,76],'ambience_loop_crossfade_seconds':2,'loudness':measure,'actual_listening':False},indent=2),encoding='utf8')
print('V11_AUDIO_READY',json.dumps(measure))
