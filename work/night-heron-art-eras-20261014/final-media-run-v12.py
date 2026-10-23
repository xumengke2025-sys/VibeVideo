from pathlib import Path
import json,subprocess,array,math,sys,wave
root=Path(__file__).resolve().parent;version='film-run-v12-natural-heron-final';out=root/'out'/version;qa=root/'qa'/version;qa.mkdir(exist_ok=True)
ff='D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
wav=qa/'decoded-audio.wav'
subprocess.run([ff,'-v','error','-y','-i',str(out/'video.mp4'),'-vn','-c:a','pcm_s16le','-ar','48000','-ac','2',str(wav)],check=True,capture_output=True)
with wave.open(str(wav),'rb') as w:b=w.readframes(w.getnframes())
v=array.array('h');v.frombytes(b)
stats={'decodedSamplesPerChannel':len(v)//2,'duration':len(v)/2/48000,'peakPCM':max(abs(n) for n in v)/32768,'rms':math.sqrt(sum((n/32768)**2 for n in v)/len(v)),'samplesAtPCMFullScale':sum(abs(n)>=32767 for n in v),'perception':'signal analysis only; not listened'}
(qa/'encoded-audio-statistics.json').write_text(json.dumps(stats,indent=2),encoding='utf8')
print(json.dumps(stats))
