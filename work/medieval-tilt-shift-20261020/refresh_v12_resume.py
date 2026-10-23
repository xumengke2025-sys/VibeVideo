"""Record resumed production without changing frozen visual inputs."""
import json
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parent
p = root / 'CHECKPOINT.json'
d = json.loads(p.read_text(encoding='utf8'))
count = len(list((root / 'render/frames-v12').glob('*.png')))
now = datetime.now(timezone.utc).isoformat()
d['updated_at'] = now
d['status'] = 'v12_full_rendering'
d['render_session_id'] = 19720
r = d['v12_revision']
r['full_render_session'] = 19720
r['last_progress_snapshot'] = {'saved_frames': count, 'total_frames': 1824, 'as_of': now, 'render_session': 19720}
r['resume_note'] = 'Session 71351 absent and no Blender/pipeline process found. Preserved 1501 PNGs, resumed same frozen pipeline in tracked session 19720; startup manifest verified unchanged.'
p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps({'saved_frames': count, 'session': 19720, 'as_of': now}))
