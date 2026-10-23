"""Original instrumental score and reading-led timeline. No speech or SFX."""
import json, pathlib, math, wave
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parent
def save(name,data):
    (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

script=[
('intro',[(4,'小甲、小乙约好碰面，一起去巴士生日会。'),(4,'小甲向西跑 ←　小乙向东跑 →')]),
('mystery',[(8,'巴士追上小甲，6秒后车尾才离开。'),(3,'小甲：咦，你怎么还没过去呀？'),(2,'再过30秒，车头遇到迎面跑来的小乙。'),(4,'又过2秒，车尾就离开了小乙！'),(3,'巴士：我没变速！他们还要多久才能碰面？')]),
('units',[(4,'先看巴士：车身15米，车速18千米/小时。'),(4,'18千米＝18000米；1小时＝3600秒。'),(4,'换好单位：巴士每秒走5米。')]),
('passA',[(8,'同向跑，小甲也在前进。看完这6秒！'),(2,'从车头齐平，到车尾齐平，巴士多赶上15米。')]),
('solveA',[(6,'15米分成6秒：每秒多赶上2.5米。'),(6,'巴士每秒5米，减去多赶上的，就是小甲的速度。')]),
('passB',[(4,'迎面跑：巴士和小乙一起靠近。看这2秒！'),(4,'15米分成2秒：每秒一起靠近7.5米。')]),
('solveB',[(6,'7.5米里，巴士贡献5米。剩下的就是小乙的。'),(4,'分别算完才发现：两人都是2.5米/秒。')]),
('flag',[(4,'接下来只盯车尾，不要混用车头和车尾。'),(4,'车尾刚离开小甲时，在这里插一面起点旗。'),(8,'再过30秒车头遇乙，再过2秒车尾离乙。共32秒。')]),
('mapbus',[(4,'32秒里，车尾从旗子出发，走了160米。'),(4,'此刻车尾与小乙齐平，所以小乙在160米处。')]),
('mapA',[(8,'同样32秒，小甲从旗子出发，走了80米。')]),
('gap',[(4,'小甲在80米处，小乙在160米处。'),(4,'两人中间，还剩80米空隙。')]),
('close',[(5,'慢放1秒：甲走2.5米，乙也走2.5米。'),(5,'两边一起跑：空隙每秒少5米！')]),
('answer',[(8,'80米空隙，每秒少5米：再过16秒就碰面！'),(4,'记住：从车尾离开小乙的那一刻开始计时。')]),
('ending',[(3,'击掌！相遇谜案破解啦！'),(3,'巴士：我的速度没变，是你们方向不同呀！'),(4,'同向看差，迎面看和。你也是相遇小侦探！')]),
]
t=0;rows=[];stages=[]
for stage,items in script:
    begin=t
    for seconds,line in items:
        rows.append(dict(stage=stage,text=line,start=t,end=t+seconds,duration=seconds));t+=seconds
    stages.append(dict(id=stage,start=begin,end=t))
plan=dict(fps=24,width=1080,height=1920,duration=t,audio_mode='music_only',audio='audio/music-only.wav',captions=rows,stages=stages,events=[])
save('timeline.json',plan)
brief=json.loads((ROOT/'brief.json').read_text(encoding='utf-8'))
brief.update(audio_mode='music_only',narration=False,duration_target_seconds=t,music='原创趣味器乐：玩具琴、拨弦、圆润贝斯与轻打击；无语音、无额外拟音')
save('brief.json',brief)

# 120 BPM, 4/4. Eight-bar phrases and three related melodic themes.
rate=48000;beat=.5;bar=2.;mix=np.zeros((round(t*rate),2),np.float64)
rng=np.random.default_rng(20261014)
def put(at,a,volume,pan=0):
    start=round(at*rate);count=min(len(a),len(mix)-start)
    if count<=0:return
    gain=np.array([math.sqrt((1-pan)/2),math.sqrt((1+pan)/2)])
    mix[start:start+count]+=a[:count,None]*volume*gain
def note(midi,duration,kind):
    q=np.arange(round(duration*rate))/rate;f=440*2**((midi-69)/12)
    attack=np.minimum(1,q*250)
    if kind=='toy':
        a=(np.sin(2*np.pi*f*q)+.28*np.sin(2*np.pi*f*2*q)*np.exp(-q*9)+.12*np.sin(2*np.pi*f*3*q)*np.exp(-q*14))*np.exp(-q*5)
    elif kind=='pluck':
        a=sum(np.sin(2*np.pi*f*k*q)/k**1.8*np.exp(-q*(3+k)) for k in range(1,5))
    else:
        a=(np.sin(2*np.pi*f*q)+.12*np.sin(2*np.pi*f*2*q))*np.exp(-q*4)
    return a*attack*np.minimum(1,(duration-q)*80)
themes=[
 [76,None,79,81,79,None,76,74], [72,76,79,None,76,74,72,None],
 [74,None,77,81,79,77,74,None], [79,81,84,None,81,79,76,None],
 [76,79,None,76,74,None,72,74], [77,None,81,79,77,76,74,None],
 [79,76,74,None,72,74,76,None], [74,76,79,None,72,None,None,None],
]
chords=[(48,[60,64,67]),(45,[57,60,64]),(53,[60,65,69]),(55,[59,62,67])]
for b in range(math.ceil(t/bar)):
    at=b*bar;stage=next((s['id'] for s in stages if s['start']<=at<s['end']),'ending')
    calm=stage in ['units','solveA','solveB','mapbus','mapA','gap']
    energy=.74 if calm else 1.
    root,chord=chords[(b//2)%4]
    # Bass changes register and occasionally walks into the next chord.
    for offset,pitch in [(0,root),(.75,root+7),(1,root+12),(1.75,root+7)]:
        put(at+offset,note(pitch,.42,'bass'),.13*energy,-.08)
    for j in range(8):
        put(at+j*.25,note(chord[(j+b)%3]+(12 if j%4==3 else 0),.42,'pluck'),.055*energy,.38)
    motif=themes[(b+b//8)%len(themes)]
    if b%16>=8:motif=themes[(b+3)%len(themes)]
    for j,pitch in enumerate(motif):
        if pitch is not None:
            # A softer low-register answer during equations, bright reprise at ending.
            pitch-=12 if calm and b%2 else 0
            put(at+j*.25,note(pitch,.68,'toy'),.105*energy,-.3)
    # Musical percussion only; no scene sound effects or voices.
    for j in range(4):
        q=np.arange(round(.13*rate))/rate
        kick=np.sin(2*np.pi*(78*q-120*q*q))*np.exp(-q*37)*np.minimum(1,q*400)
        put(at+j*.5,kick,.065*energy)
        if j%2:
            brush=rng.normal(0,1,len(q))*np.exp(-q*55)*np.minimum(1,q*500)
            put(at+j*.5,brush,.018*energy,.1)
    if b%8==7 and not calm:
        for j,pitch in enumerate([79,81,84,88]):put(at+1+j*.25,note(pitch,.5,'toy'),.055,-.2)

# Small room reflections, conservative peaks, fade at both ends.
for delay,gain in [(.065,.08),(.11,.05)]:
    n=round(delay*rate);mix[n:]+=mix[:-n,::-1].copy()*gain
fade=round(.7*rate);mix[:fade]*=np.linspace(0,1,fade)[:,None];mix[-rate:]*=np.linspace(1,0,rate)[:,None]
peak=float(np.max(np.abs(mix)));mix*=.72/max(peak,1e-9)
pcm=(np.clip(mix,-1,1)*32767).astype('<i2')
(ROOT/'audio').mkdir(exist_ok=True)
with wave.open(str(ROOT/'audio/music-only.wav'),'wb') as f:
    f.setnchannels(2);f.setsampwidth(2);f.setframerate(rate);f.writeframes(pcm.tobytes())
save('audio/music-record.json',dict(title='长长巴士的玩具琴散步',origin='Original locally synthesized instrumental composition',script='make-music-only.py',seed=20261014,bpm=120,meter='4/4',duration=t,sample_rate=rate,channels=2,peak_dbfs=20*math.log10(.72),rms_dbfs=float(20*np.log10(np.sqrt(np.mean(mix**2)))),speech=False,sfx=False,instruments=['toy piano','plucked strings','rounded bass','light percussion'],historical_voice_files_used=False))
def stamp(x):
    ms=round(x*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'
(ROOT/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(rows)),encoding='utf-8')
print(json.dumps(dict(duration=t,stages=len(stages),captions=len(rows),audio='music_only'),ensure_ascii=False))
