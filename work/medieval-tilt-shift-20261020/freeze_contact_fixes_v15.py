"""Freeze exact scoped follow/stop edits, preserving all prior rendered evidence."""
from pathlib import Path
import json,hashlib,shutil,sys,math
P=Path(__file__).resolve().parent
mp=P/'render/frozen-v15-manifest.json';old=json.loads(mp.read_text())
motion=P/'v15_motion.py';route=P/'v15_route.py'
old_motion='  # Keep the persistent rider framed; the former distant-garden target pushed him offscreen.'
new_motion='  # A short look-ahead keeps the cyclist visible while crossing the garden street.\n  if si==4:target=p+Vector((ahead.x*.15,ahead.y*.15,1.0))'
route_insert='    # Align the last approach tangent with the stop chord, avoiding a tiny\n    # reverse before stopping that used to flip yaw by about ninety degrees.\n    if p[0]==64:return tuple((NODES[i+1][k]-p[k])/(NODES[i+1][0]-p[0]) for k in [1,2])\n'
for path,cur,prev in [(motion,new_motion,old_motion),(route,route_insert,'')]:
    s=path.read_text();assert s.count(cur)==1
    assert hashlib.sha256(s.replace(cur,prev).encode()).hexdigest()==old['files'][path.name]
for name,h in old['files'].items():
    if name not in ['v15_motion.py','v15_route.py']:assert hashlib.sha256((P/name).read_bytes()).hexdigest()==h
archive=P/'render/history-v15-before-contact-fix';archive.mkdir(exist_ok=True)
shutil.copy2(mp,archive/mp.name)
source=P/'qa/v15/sample-source.json';d=json.loads(source.read_text());shutil.copy2(source,archive/source.name)
affected=lambda f:1056<=f<1320 or f>=1464
moved=[]
for path in (P/'render/sample-v15').glob('*.png'):
    if path.stem.isdigit() and affected(int(path.stem)):
        shutil.move(str(path),str(archive/path.name));moved.append(int(path.stem))
new=json.loads(json.dumps(old))
for path in [motion,route]:new['files'][path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
mp.write_text(json.dumps(new,indent=2))
d.update(manifest=new,frames=[f for f in d['frames'] if not affected(f)])
source.write_text(json.dumps(d,indent=2))
sys.path.insert(0,str(P));import v15_route as r
step=lambda f:abs((r.state((f+1)/24)['yaw']-r.state(f/24)['yaw']+math.pi)%math.tau-math.pi)*180/math.pi
restart=max(step(f) for f in range(1668,1685));assert restart<5
e={'changed_inputs':['v15_motion.py','v15_route.py'],'invalidated_ranges':[[1056,1319],[1464,2159]],'why_invalidate_remainder':'Route tangent changes cumulative wheel/crank distance after stop approach. Full remainder is conservatively rerendered. 61s includes camera look-ahead before changed interval at 62s.','reverse_patch_hash_match':True,'retained_samples':d['frames'],'archived_sample_frames':sorted(moved),'restart_yaw_step_max_degrees':restart,'static_scope':'Position and heading before 61s unchanged except shot 4 target; no model, material, light, audio or compositor change.'}
(P/'qa/v15/contact-fix-source.json').write_text(json.dumps(e,indent=2))
print('CONTACT_FIX_FROZEN','retained',len(d['frames']),'restart yaw step',restart)
