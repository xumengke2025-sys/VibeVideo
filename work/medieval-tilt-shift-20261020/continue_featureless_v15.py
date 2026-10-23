"""Record the bounded camera correction and preserve unaffected sample evidence."""
from pathlib import Path
import json, hashlib, shutil

P=Path(__file__).resolve().parent
mp=P/'render/frozen-v15-manifest.json'
old=json.loads(mp.read_text(encoding='utf8'))
s=(P/'v15_motion.py').read_text(encoding='utf8')
new_line='  # Keep the persistent rider framed; the former distant-garden target pushed him offscreen.'
old_line='  if si==4:target=target.lerp(Vector((-48,87,12)),.14)'
assert s.count(new_line)==1
assert hashlib.sha256(s.replace(new_line,old_line).encode()).hexdigest()==old['files']['v15_motion.py'], 'Unexpected changes beyond bounded camera fix'
for name,h in old['files'].items():
    if name!='v15_motion.py':
        assert hashlib.sha256((P/name).read_bytes()).hexdigest()==h,name
archive=P/'render/history-v15-before-garden-focus-fix'
archive.mkdir(exist_ok=True)
shutil.copy2(mp,archive/mp.name)
source=P/'qa/v15/sample-source.json'
d=json.loads(source.read_text(encoding='utf8'))
assert d['manifest']==old
shutil.copy2(source,archive/source.name)
invalid=[f for f in d['frames'] if 1056<=f<1320]
for f in invalid:
    path=Path(d['folder'])/f'{f:05d}.png'
    if path.exists():shutil.move(str(path),str(archive/path.name))
new=json.loads(json.dumps(old))
new['files']['v15_motion.py']=hashlib.sha256((P/'v15_motion.py').read_bytes()).hexdigest()
mp.write_text(json.dumps(new,indent=2),encoding='utf8')
d.update(manifest=new,frames=[f for f in d['frames'] if f not in invalid])
source.write_text(json.dumps(d,indent=2),encoding='utf8')
evidence={'reason':'Distant garden look target pushed cyclist out of frame in shot 4. Removed only this conditional target adjustment.','changed_frame_range':[1056,1319],'old_manifest':str(archive/mp.name),'new_manifest':str(mp),'invalidated_sample_frames':invalid,'retained_sample_frames':d['frames'],'validation':'Reverse patch reconstructs exact old v15_motion hash; all other frozen input hashes unchanged. Reuse is outside conditional time range only.','producer_observation':'Viewed 23 representative sample thumbnails and original 1632, 1212. Rider featureless; shot 4 framing needs rerender. No independent or audio review claimed.'}
(P/'qa/v15/garden-focus-fix.json').write_text(json.dumps(evidence,indent=2),encoding='utf8')
cp=P/'CHECKPOINT-v15.json';c=json.loads(cp.read_text(encoding='utf8'))
c['status']='featureless_samples_camera_fix'
c['completed']+=['Rebuilt revision 4 rider with no facial features or eyeballs','Rendered 181 final-size sample frames; reviewed 23 representative thumbnails and original frames 1632,1212','Corrected only shot 4 look target after actual output showed rider outside frame; preserved unaffected frozen samples with reverse-patch hash evidence']
c['verification']+=['No active Babylon renderer at continuation; other project Blender allowed to finish','Featureless rider visibly confirmed at sample frame 1632 (68s)']
c['unresolved']=['Corrected 44–55s camera proof pending','Continuous sample action verification pending','Full 2160-frame film pending','Actual listening unavailable']
c['next_action']='Render corrected shot 4 proof, inspect action windows, then run frozen v15 full pipeline without interrupting other projects.'
cp.write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf8')
print('BOUNDED_CAMERA_FIX_READY',invalid,'retained',len(d['frames']))
