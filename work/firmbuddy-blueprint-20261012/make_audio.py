import sys,asyncio,json,subprocess,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools/python'))
import edge_tts
import numpy as np
import imageio_ffmpeg
FF=Path(imageio_ffmpeg.get_ffmpeg_exe())
entries=[
(.65,3.2,'下午三点的客户拜访。'),(3.2,6.2,'谈什么？依据在哪？下一步怎么做？'),
(8.1,11.9,'从商机中心找到值得研判的线索。'),(12,16.2,'先看公告来源，再明确需要核实的问题。'),
(18.4,22.7,'企业画像、资本运作、信披合规。'),(23,27.7,'多位专家围绕同一问题，补齐专业视角。'),
(30.6,34.3,'打开知识档案，查规则、找资料。'),(34.4,38.9,'让分析连回来源与版本。'),
(41.6,47.0,'把客户情况、沟通重点和待核实问题，整理成拜访策略包。'),(47.2,51.0,'再确认后续跟进任务。'),
(52.3,55.8,'从一条线索，到一次有准备的拜访。'),(56,59.9,'Firm Buddy，让专业协同，走进客户经营。')]
async def synth():
 for i,(start,end,txt) in enumerate(entries):
  file=ROOT/'audio'/f'voice-{i:02}.mp3'
  if not file.exists():
   await edge_tts.Communicate(txt,'zh-CN-YunxiNeural',rate='+12%',volume='+0%').save(str(file))
  print('voice',i,flush=True)
# Online voice was unavailable (HTTP 403). Use already rendered local SAPI WAVs.
sr=48000;n=sr*60;voice=np.zeros(n,dtype=np.float64);rng=np.random.default_rng(19);meta=[]
for i,(start,end,txt) in enumerate(entries):
 src=ROOT/'audio'/f'voice-{i:02}.wav';raw=subprocess.check_output([str(FF),'-v','error','-i',str(src),'-f','f32le','-acodec','pcm_f32le','-ac','1','-ar',str(sr),'-'])
 a=np.frombuffer(raw,dtype=np.float32).astype(np.float64)
 # Remove encoder padding and long edge pauses only; preserve a short release.
 nz=np.flatnonzero(np.abs(a)>.003)
 if len(nz):a=a[max(0,nz[0]-int(.045*sr)):min(len(a),nz[-1]+int(.12*sr))]
 dur=len(a)/sr;available=end-start;speed=max(1,dur/available)
 if speed>1.30:raise RuntimeError(f'Voice {i} too long: {dur:.2f}s for {available:.2f}s')
 if speed>1:
  raw=subprocess.run([str(FF),'-v','error','-f','f32le','-ar',str(sr),'-ac','1','-i','-','-af',f'atempo={speed:.6f}','-f','f32le','-acodec','pcm_f32le','-'],input=a.astype('<f4').tobytes(),stdout=subprocess.PIPE,check=True).stdout
  a=np.frombuffer(raw,dtype='<f4').astype(np.float64)[:int(available*sr)]
 peak=np.max(np.abs(a));a=a*.60/max(peak,.01);offset=round(start*sr);voice[offset:offset+len(a)]+=a
 meta.append({'id':i,'text':txt,'start':start,'end':start+len(a)/sr,'original_duration':dur,'speed':speed,'source':str(src),'voice':'Microsoft Huihui Desktop; Zira for English brand'})
fx=np.zeros(n);music=np.zeros(n)
def add(buf,t,a):
 k=int(t*sr);end=min(n,k+len(a));buf[k:end]+=a[:end-k]
# Original restrained plucked motif, no external music sample.
notes=[146.832,220,293.665,329.628,440,329.628,293.665,220]
for i,t in enumerate(np.arange(.4,59,.625)):
 f=notes[i%8];tt=np.arange(int(.7*sr))/sr
 a=(np.sin(2*np.pi*f*tt)+.32*np.sin(2*np.pi*2*f*tt)+.13*np.sin(2*np.pi*3*f*tt))*np.exp(-tt*8)*(1-np.exp(-tt*120))*.023
 add(music,t,a)
for t in [1,2.4,7.7,10.5,20.9,22.2,23.5,31.4,33.2,36.5,42.5,43.1,43.7,48.35,49.3,56.3]:
 tt=np.arange(int(.16*sr))/sr;a=rng.normal(0,1,len(tt))*np.exp(-tt*55)*.022+np.sin(2*np.pi*900*tt)*np.exp(-tt*40)*.015;add(fx,t,a)
for start,end,_ in entries:
 music[int(start*sr):int(end*sr)]*=.45
mix=voice+music+fx;mix*=np.minimum(np.arange(n)/(sr*.08),1)*np.minimum((n-np.arange(n))/(sr*.3),1);mix=np.clip(mix,-.95,.95)
for name,data in [('mix',mix),('narration',voice),('music',music),('foley',fx)]:
 with wave.open(str(ROOT/'audio'/f'{name}.wav'),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((data*32767).astype('<i2').tobytes())
(ROOT/'audio/timing.json').write_text(json.dumps({'synthesized_voice':True,'provider':'Windows SAPI offline','voice':'Huihui; Zira for English brand','music':'Original synthesized plucked motif, not a licensed orchestral recording','duration':60,'sample_rate':sr,'peak':float(np.max(np.abs(mix))),'entries':meta},ensure_ascii=False,indent=2),encoding='utf-8')
print('AUDIO COMPLETE',flush=True)
