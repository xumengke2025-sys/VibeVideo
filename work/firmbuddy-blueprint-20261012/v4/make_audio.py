import json, subprocess, wave, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'tools/python'))
import imageio_ffmpeg
FF=Path(imageio_ffmpeg.get_ffmpeg_exe())
plan=json.loads((ROOT/'plan.json').read_text(encoding='utf-8'))
sr=48000; n=sr*plan['duration']; voice=np.zeros(n); meta=[]
for i,s in enumerate(plan['shots']):
    src=ROOT/'audio'/f'voice-{i:02}.wav'
    raw=subprocess.check_output([str(FF),'-v','error','-i',str(src),'-f','f32le','-acodec','pcm_f32le','-ac','1','-ar',str(sr),'-'])
    a=np.frombuffer(raw,dtype='<f4').astype(np.float64)
    nz=np.flatnonzero(np.abs(a)>.003)
    if len(nz):a=a[max(0,nz[0]-int(.05*sr)):min(len(a),nz[-1]+int(.14*sr))]
    start=s['start']+.24; available=s['end']-start-.24; dur=len(a)/sr
    speed=max(1,dur/available)
    if speed>1.20:raise RuntimeError(f'Voice {i}: needs {speed:.3f} speed; revise speech rather than rush')
    if speed>1:
        raw=subprocess.run([str(FF),'-v','error','-f','f32le','-ar',str(sr),'-ac','1','-i','-','-af',f'atempo={speed:.6f}','-f','f32le','-acodec','pcm_f32le','-'],input=a.astype('<f4').tobytes(),stdout=subprocess.PIPE,check=True).stdout
        a=np.frombuffer(raw,dtype='<f4').astype(np.float64)[:int(available*sr)]
    a*=.64/max(np.max(np.abs(a)),.01); k=round(start*sr);voice[k:k+len(a)]+=a
    meta.append({'id':s['id'],'text':s['voiceover'],'spoken_text':s['voiceover'].replace('AI','人工智能'),'start':start,'end':start+len(a)/sr,'original_duration':dur,'speed':speed})
music=np.zeros(n);fx=np.zeros(n);rng=np.random.default_rng(19)
def add(buf,t,a):
    k=round(t*sr); end=min(n,k+len(a));buf[k:end]+=a[:end-k]
notes=[146.832,220,293.665,329.628,293.665,220,196,246.942]
for j,t in enumerate(np.arange(.35,67,.6)):
    f=notes[j%len(notes)];tt=np.arange(int(.75*sr))/sr
    a=(np.sin(2*np.pi*f*tt)+.22*np.sin(2*np.pi*2*f*tt)+.08*np.sin(2*np.pi*3*f*tt))*np.exp(-tt*6.5)*(1-np.exp(-tt*100))*.023
    add(music,t,a)
for t in [1.4,1.72,2.04,3.2,9,12,17,17.9,18.8,21,24.2,27,28.6,30.5,32.2,33.6,36.2,39,40.2,41,41.5,47.2,48,49.2,51.9,52,55.5,58.5,64.5]:
    tt=np.arange(int(.15*sr))/sr
    a=(rng.normal(0,1,len(tt))*.013+np.sin(2*np.pi*880*tt)*.014)*np.exp(-tt*42)
    add(fx,t,a)
for start,end in [(7.2,9),(27,28.6),(38.5,39.3),(50.6,51.9),(61,64.5)]:
    tt=np.arange(round((end-start)*sr))/sr
    a=rng.normal(0,1,len(tt));a=np.convolve(a,np.ones(15)/15,mode='same')*.013*np.sin(np.pi*tt/(end-start))**2
    add(fx,start,a)
for e in meta:music[int(e['start']*sr):int(e['end']*sr)]*=.40
fade=np.minimum(np.arange(n)/(sr*.15),1)*np.minimum((n-np.arange(n))/(sr*.6),1)
mix=np.clip((voice+music+fx)*fade,-.93,.93)
for name,data in [('mix',mix),('narration',voice),('music',music),('foley',fx)]:
    with wave.open(str(ROOT/'audio'/f'{name}.wav'),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((data*32767).astype('<i2').tobytes())
def stamp(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(ROOT/'audio/narration.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(e["start"])} --> {stamp(e["end"])}\n{e["text"]}' for i,e in enumerate(meta))+'\n',encoding='utf-8')
(ROOT/'audio/timing.json').write_text(json.dumps({'duration':plan['duration'],'sample_rate':sr,'provider':'Windows SAPI offline','voice':'Microsoft Huihui Desktop','music':'Original synthesized plucked motif','peak':float(np.max(np.abs(mix))),'entries':meta,'listening_verified':False},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'duration':68,'entries':[{'id':e['id'],'end':round(e['end'],2),'speed':round(e['speed'],3)} for e in meta]},ensure_ascii=False))
