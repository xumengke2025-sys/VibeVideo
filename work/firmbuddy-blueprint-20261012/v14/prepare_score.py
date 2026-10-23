from pathlib import Path
import json
R=Path(__file__).resolve().parent
p=R/'plan.json';plan=json.loads(p.read_text(encoding='utf-8'))
for b in plan['burdens']:
 if b['id']=='collection':b['end']=21.6
for s in plan['shots']:s['voiceover']=False
for e in plan['soundtrack']['events']:
 if e['id']=='collection':e['at']=21.6
 e['action']='burden accepted by machine' if e['id'] in {b['id'] for b in plan['burdens']} else e['id']
p.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
src=(R.parent/'v7/make_audio.py').read_text(encoding='utf-8')
a=src.index('for at,notes,length in [(0,chords[0]');b=src.index('\n    add(music,at,pad',a)
src=src[:a]+"for i,at in enumerate(np.arange(0,88,6.4)):\n    notes=chords[i%4];length=min(6.7,90-at)"+src[b:]
src=src.replace('for anchor in [12.1,21.4,31.2,37.9,47.5]:',"for anchor in [b['end'] for b in plan['burdens']]:")
(R/'make_audio.py').write_text(src,encoding='utf-8')
s=(R/'scene-body.js').read_text(encoding='utf-8').replace("});if(T>8.4&&T<11.7)movingRoute(paths.toHall,8.4,11.7);}","});}")
(R/'scene-body.js').write_text(s,encoding='utf-8')
print('90-second score prepared with six unloading cues')
