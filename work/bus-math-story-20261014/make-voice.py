import asyncio, json, sys, subprocess, pathlib, time, wave, math, io
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'.deps'))
import edge_tts
FF=ROOT.parents[1]/'node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
FP=FF.with_name('ffprobe.exe')
VOICE=ROOT/'audio'
VOICE.mkdir(exist_ok=True)

async def speak(text,file,role=None):
    kwargs={'voice':'zh-CN-XiaoxiaoNeural','rate':'-8%','pitch':'+2Hz'}
    if role=='A': kwargs.update(pitch='+8Hz')
    if role=='B': kwargs.update(pitch='+14Hz')
    for attempt in range(3):
        try:
            await asyncio.wait_for(edge_tts.Communicate(text,**kwargs).save(str(file)),timeout=40)
            return
        except Exception as e:
            if attempt==2: raise
            print('voice retry',file.name,type(e).__name__,flush=True)
            await asyncio.sleep(1)

def duration(file):
    return float(subprocess.check_output([str(FP),'-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(file)],text=True).strip())

async def main():
    rows=json.loads((ROOT/'narration.json').read_text(encoding='utf-8'))
    if '--test' in sys.argv:
        await speak('你好，小朋友！让长长巴士帮我们破解相遇谜案。',VOICE/'test.mp3')
        print('voice test seconds',duration(VOICE/'test.mp3'),flush=True)
        return
    for i,row in enumerate(rows):
        file=VOICE/f'{i:02}.mp3'
        if not file.exists() or file.stat().st_size<1000:
            await speak(row['text'],file,row.get('role'))
        row['audio']=str(file.relative_to(ROOT)).replace('\\','/')
        row['speechDuration']=duration(file)
        print(f'voice {i+1}/{len(rows)}: {row["speechDuration"]:.2f}s',flush=True)
    # Speech is the clock. Give children extra pauses at causal and equation events.
    t=0;stages=[];current=None
    for i,row in enumerate(rows):
        if row['stage']!=current:
            if stages: stages[-1]['end']=t
            current=row['stage'];stages.append({'id':current,'start':t})
        row['start']=round(t,4);row['voiceStart']=round(t+.3,4)
        row['duration']=round(row['speechDuration']+1.15,4)
        t+=row['duration'];row['end']=round(t,4)
    stages[-1]['end']=round(t,4)
    plan={'fps':24,'width':1080,'height':1920,'duration':math.ceil(t*24)/24,'narration':rows,'stages':stages,'events':[]}
    for s in stages:
        if s['id'] in ['passA','passB']:
            plan['events'].append({'id':s['id']+'-front','at':s['start']+1.0,'kind':'tick'})
            plan['events'].append({'id':s['id']+'-rear','at':s['start']+(7.0 if s['id']=='passA' else 3.0),'kind':'tick'})
        if s['id']=='ending':plan['events'].append({'id':'high-five','at':s['start']+1.6,'kind':'clap'})
    (ROOT/'timeline.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
    # Mix whole measured sentences at their precise positions; SFX are independent events.
    rate=48000;import numpy as np
    mix=np.zeros((int((plan['duration']+.1)*rate),2),dtype=np.float32)
    for row in rows:
        pcm=subprocess.check_output([str(FF),'-v','error','-i',str(ROOT/row['audio']),'-f','wav','-c:a','pcm_s16le','-ac','1','-ar',str(rate),'pipe:1'])
        with wave.open(io.BytesIO(pcm),'rb') as decoded: a=np.frombuffer(decoded.readframes(decoded.getnframes()),dtype='<i2').astype(np.float32)/32768
        n=int(row['voiceStart']*rate);mix[n:n+len(a)]+=a[:,None]*.94
    # A quiet original pentatonic toy-piano pattern; dip under every spoken line.
    notes=[60,64,67,69,67,64,62,67]
    for j,at in enumerate(np.arange(0,plan['duration'],.6)):
        dur=.48;tt=np.arange(int(dur*rate))/rate;f=440*2**((notes[j%len(notes)]-69)/12)
        a=(np.sin(2*np.pi*f*tt)+.27*np.sin(2*np.pi*f*2*tt))*np.exp(-tt*12)*np.minimum(1,tt*300)
        n=int(at*rate);m=min(len(a),len(mix)-n)
        mix[n:n+m]+=a[:m,None]*.012
    rng=np.random.default_rng(20261014)
    for ev in plan['events']:
        tt=np.arange(int(.16*rate))/rate
        a=(rng.normal(0,1,len(tt))*.4 if ev['kind']=='clap' else np.sin(2*np.pi*(740-300*tt)*tt))*np.exp(-tt*32)*np.minimum(1,tt*1000)
        n=int(ev['at']*rate);mix[n:n+len(a)]+=a[:,None]*(.10 if ev['kind']=='clap' else .07)
    fade=int(.3*rate);mix[:fade]*=np.linspace(0,1,fade)[:,None];mix[-fade:]*=np.linspace(1,0,fade)[:,None]
    peak=float(np.abs(mix).max());mix*=min(1,.92/max(peak,1e-8));pcm=(np.clip(mix,-1,1)*32767).astype('<i2')
    with wave.open(str(VOICE/'mix.wav'),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(rate);f.writeframes(pcm.tobytes())
    def stamp(t):
        ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
    (ROOT/'narration.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["voiceStart"])} --> {stamp(r["end"]-.15)}\n{r["text"]}' for i,r in enumerate(rows)),encoding='utf-8')
    print('timeline duration',plan['duration'],'mix peak',peak,flush=True)

asyncio.run(main())
