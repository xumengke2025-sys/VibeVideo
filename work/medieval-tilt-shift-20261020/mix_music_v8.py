from pathlib import Path
import json,subprocess,wave,io
import numpy as np
ROOT=Path(__file__).resolve().parent;A=ROOT/'audio'
FF='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
timeline=json.loads((ROOT/'v8-timeline.json').read_text(encoding='utf8'))
start=timeline['music']['excerpt_start'];sr=48000;n=56*sr
def pcm(path,offset=0):
    b=subprocess.check_output([FF,'-v','error','-ss',str(offset),'-i',str(path),'-t','56','-ac','2','-ar',str(sr),'-c:a','pcm_s16le','-f','wav','pipe:1'])
    with wave.open(io.BytesIO(b)) as w:x=np.frombuffer(w.readframes(n),dtype='<i2').reshape(-1,2).astype(np.float32)/32768
    return np.pad(x,((0,max(0,n-len(x))),(0,0)))[:n]
music=pcm(A/'user-provided-Dream-Of-Babylon.mp3',start);env=pcm(A/'ambience.wav')
t=np.arange(n)/sr
fade=np.sin(np.minimum(t/.15,1)*np.pi/2)**2*np.sin(np.minimum((56-t)/3,1)*np.pi/2)**2
mix=(music+env*.25)*fade[:,None]
peak=float(np.max(np.abs(mix)))
if peak>.9:mix*=.9/peak
raw=A/'music-v8-raw.wav'
with wave.open(str(raw),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(mix,-.999,.999)*32767).astype('<i2').tobytes())
out=A/'final-mix-v8.wav'
r=subprocess.run([FF,'-y','-hide_banner','-i',str(raw),'-af','loudnorm=I=-17:TP=-1.5:LRA=13:print_format=json','-ar','48000','-c:a','pcm_s24le',str(out)],capture_output=True,text=True,encoding='utf8',check=True)
measure=json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0]
(A/'mix-v8-evidence.json').write_text(json.dumps({'source_excerpt':[start,start+56],'fade_in':.15,'fade_out':[53,56],'loudness':measure,'actual_listening':False},indent=2),encoding='utf8')
print('MIX_V8_READY',json.dumps(measure),flush=True)
