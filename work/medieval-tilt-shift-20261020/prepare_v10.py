from pathlib import Path
from datetime import datetime
import json,hashlib
ROOT=Path(__file__).resolve().parent
for filename in ['render_city_v9.py','render_pipeline_v9.py','assemble_city_v9.py']:
    src=(ROOT/filename).read_text(encoding='utf8')
    dst=ROOT/filename.replace('v9','v10')
    assert not dst.exists(),dst
    text=src.replace('v9','v10')
    if filename=='assemble_city_v9.py':
        text=text.replace("'independent_review':'pending'","'independent_review':'single-round budget already used; producer verification only'")
    dst.write_text(text,encoding='utf8')
assert (ROOT/'render_city_v10.py').read_text(encoding='utf8').replace('v10','v9')==(ROOT/'render_city_v9.py').read_text(encoding='utf8')
cp=json.loads((ROOT/'CHECKPOINT.json').read_text(encoding='utf8'))
cp.update(version='v10',status='v10_targeted_followup_prepared',updated_at=datetime.now().isoformat(timespec='seconds'),next_action='Build parenting-only model fix, render formal frames 744 and 852, inspect the repair and era details, then render full 1344-frame version and deliver with producer verification and existing independent-review limits.')
cp['v10_followup']={'authorization':'Continued user goal: finish full film and confirm era appearance and tilt-shift features after v9 delivery.','scope':['attach legacy crossbenches to animated hull','era-specific source and output evidence','retain all established photography and audio'],'review':'No new independent review round; prior budget remains 1/1. New output receives producer verification only.'}
cp['unresolved']=['v10 source change needs formal render and full output','Era-style verification must be tied to actual output; exact archaeological reconstruction is not claimed','Actual listening unavailable; musical climax remains unverified']
(ROOT/'CHECKPOINT.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf8')
print('V10_SOURCES_PREPARED',flush=True)
