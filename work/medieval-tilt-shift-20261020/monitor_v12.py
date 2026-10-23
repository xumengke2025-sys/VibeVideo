import json,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent
folder=ROOT/'render/frames-v12';files=list(folder.glob('[0-9][0-9][0-9][0-9][0-9].png'));indices={int(p.stem) for p in files}
latest=max(files,key=lambda p:p.stat().st_mtime) if files else None
prefix=next((i for i in range(1824) if i not in indices),1824)
status=ROOT/'render/pipeline-status-v12.json'
d={'now':datetime.datetime.now().astimezone().isoformat(),'saved':len(files),'total':1824,'percent':round(len(files)/1824*100,1),'continuous_prefix_frames':prefix,'continuous_prefix_seconds':round(prefix/24,3),'latest_frame':int(latest.stem) if latest else None,'latest_modified':datetime.datetime.fromtimestamp(latest.stat().st_mtime).astimezone().isoformat() if latest else None}
if status.exists():
 s=json.loads(status.read_text(encoding='utf8'));d['stage']=s['stage'];d['last_checked_batch_frames']=s['completed_frames'];d['elapsed_seconds']=round(s['elapsed_seconds'])
print(json.dumps(d,ensure_ascii=False))
