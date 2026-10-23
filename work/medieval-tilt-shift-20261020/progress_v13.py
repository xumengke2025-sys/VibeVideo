from pathlib import Path
from datetime import datetime, timezone
import json
r=Path(__file__).resolve().parent
status=json.loads((r/'render/pipeline-status-v13.json').read_text(encoding='utf8'))
files=list((r/'render/frames-v13').glob('[0-9][0-9][0-9][0-9][0-9].png'))
snapshot={'saved_frames':len(files),'total_frames':1824,'as_of':datetime.now(timezone.utc).isoformat(),'stage':status['stage']}
p=r/'CHECKPOINT.json';c=json.loads(p.read_text(encoding='utf8'));c['v13_revision_progress']['last_progress_snapshot']=snapshot;c['v13_revision_progress']['active_pipeline_pid']=int((r/'render/pipeline-v13.pid').read_text().strip()) if (r/'render/pipeline-v13.pid').exists() else None;c['v13_revision_progress']['pipeline_session_id']=None;c['v13_revision_progress']['monitor_cell_id']=None;c['updated_at']=snapshot['as_of'];p.write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(snapshot,ensure_ascii=False))
pointer=r/'render/active-v13-log.txt'
log=r/pointer.read_text(encoding='utf-8-sig').strip() if pointer.exists() else r/'render/full-v13.log'
lines=log.read_text(encoding='utf8').splitlines();print('\n'.join(lines[-2:]))
