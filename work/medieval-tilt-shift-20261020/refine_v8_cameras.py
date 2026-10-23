from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parent
p=ROOT/'v8-timeline.json'
old=ROOT/'history/v8/timeline-before-visibility-fix.json';old.parent.mkdir(parents=True,exist_ok=True)
if not old.exists():shutil.copy2(p,old)
d=json.loads(p.read_text(encoding='utf8'))
# The royal monument stands in front of the gate, so approach its front court.
# The former target behind the gate allowed a tower to cover the entire subject.
d['shots'][1]=[8,16,[15,-36,34],[14,-25,36],[-4.8,-12,3.7],[-4.8,-12,3.7],46,46]
d['shots'][5]=[44.4,51,[27,15,51],[31,25,55],[52,43,7.5],[52,43,7.5],42,44]
for i,e in enumerate(d['events']):e['camera']=d['shots'][i][2:]
d['visibility_changes']=['Royal shot moved to the gate forecourt; visual proof pending.']
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
proof=ROOT/'render/proof-v8/00288.png';archive=ROOT/'qa/v8/royal-gate-occluded-00288.png';archive.parent.mkdir(parents=True,exist_ok=True)
if proof.exists():
    archive=ROOT/'qa/v8/royal-house-occluded-00288.png'
    if not archive.exists():shutil.move(str(proof),str(archive))
print('Royal camera updated; old proof archived.')
