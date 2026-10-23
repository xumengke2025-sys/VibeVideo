"""Small meaningful pre-render checks for music mapping and physical path clearances."""
from pathlib import Path
import json,math,ast,wave
ROOT=Path(__file__).resolve().parent
t=json.loads((ROOT/'v8-timeline.json').read_text(encoding='utf8'))
shots=t['shots'];assert shots[0][0]==0 and shots[-1][1]==56
for i,s in enumerate(shots):
    assert s[0]<s[1]
    if i:assert abs(s[0]-shots[i-1][1])<1e-6
    for a in s[2:6]:assert len(a)==3 and all(math.isfinite(v) for v in a)
    assert s[6]>0 and s[7]>0
assert t['music']['excerpt_end']<t['music']['duration']
for p in ['render_city_v8.py','model/enrich_city_v8.py','mix_music_v8.py']:
    ast.parse((ROOT/p).read_text(encoding='utf8'))
# Merchant hull envelope stays within canal and between bridge y=32 and y=108.
for x,y,s in [(29,45,.65),(37,60,.7),(29,80,.65),(37,94,.6)]:
    assert 24<x-1.25*s and x+1.25*s<41.5
    travel=.36*12;half=9*s/2
    assert y-travel-half>34 and y+travel+half<106
report={'timeline':'continuous 0–56s','music_source':[t['music']['excerpt_start'],t['music']['excerpt_end']],
        'syntax':'passed','new_boat_clearances':'conservative hull envelopes clear of banks and both bridges',
        'visual_quality':'not assessed by these checks','audio_perceived':False}
(ROOT/'qa/v8').mkdir(parents=True,exist_ok=True)
(ROOT/'qa/v8/setup-check.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report))
