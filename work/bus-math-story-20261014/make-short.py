import pathlib,json,wave,numpy as np
ROOT=pathlib.Path(__file__).resolve().parent
spec=[
('intro',2,'两位跑步伙伴，约好一起去生日会。'),
('mystery',4,'追上甲→6秒离开；再30秒遇乙→2秒离开。'),
('units',2,'18千米/小时＝5米/秒。'),
('solveA',3,'同向：先求速度差，再求小甲速度。'),
('solveB',3,'迎面：先求速度和，再求小乙速度。'),
('flag',3,'车尾离甲时插旗。到离乙，共32秒。'),
('mapbus',2,'车尾与乙齐平：小乙在160米处。'),
('mapA',2,'同样32秒：小甲在80米处。'),
('gap',2,'两人之间，还剩80米。'),
('close',2,'迎面跑，空隙每秒少5米。'),
('answer',3,'从车尾离开乙算起，再过16秒相遇！'),
('ending',2,'击掌！同向看差，迎面看和。'),
]
t=0;stages=[];rows=[]
for id,duration,text in spec:
    stages.append(dict(id=id,start=t,end=t+duration))
    rows.append(dict(stage=id,text=text,start=t,end=t+duration,duration=duration));t+=duration
plan=dict(short=True,fps=24,width=1080,height=1920,duration=t,audio_mode='music_only',audio='audio/music-only-30s.wav',stages=stages,captions=rows,events=[],motion_note='6秒、2秒、32秒、16秒动作均为加速示意；算式来自同一解析模型')
(ROOT/'timeline-short.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
with wave.open(str(ROOT/'audio/music-only.wav'),'rb') as f:
    rate=f.getframerate();audio=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').reshape(-1,2).astype(float)
short=audio[:30*rate].copy()
# Preserve the original final musical phrase and ending fade.
short[26*rate:]=audio[-4*rate:]
n=int(.08*rate)
short[26*rate-n:26*rate]*=np.linspace(1,0,n)[:,None]
short[26*rate:26*rate+n]*=np.linspace(0,1,n)[:,None]
with wave.open(str(ROOT/'audio/music-only-30s.wav'),'wb') as f:
    f.setnchannels(2);f.setsampwidth(2);f.setframerate(rate);f.writeframes(short.astype('<i2').tobytes())
brief=json.loads((ROOT/'brief.json').read_text(encoding='utf-8'))
brief.update(duration_target_seconds=30,active_timeline='timeline-short.json',user_update='2026-10-14 用户要求压缩至30秒；保留核心条件和解法，加速演示，纯音乐')
(ROOT/'brief.json').write_text(json.dumps(brief,ensure_ascii=False,indent=2),encoding='utf-8')
print('30-second plan and music complete')
