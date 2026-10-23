"""Read the active render's checkpoint; never starts or restarts a renderer."""
from pathlib import Path
import json,time
p=Path(__file__).resolve().parent/'render/pipeline-status.json'
last=-1
while True:
    try:s=json.loads(p.read_text(encoding='utf8'))
    except (OSError,json.JSONDecodeError):time.sleep(2);continue
    n=s.get('completed_frames',0)
    if n!=last:
        elapsed=s.get('elapsed_seconds',0)
        eta=round((1344-n)*elapsed/max(1,n)/60)
        print(json.dumps({'frames':n,'total':1344,'percent':round(100*n/1344,1),'estimated_render_minutes_remaining':eta,'stage':s['stage']},ensure_ascii=False),flush=True)
        last=n
    if s['stage'] not in ['rendering','encoding']:break
    time.sleep(50)
