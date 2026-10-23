import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'tools/resource-monitor'))
import psutil
rows=[]
for p in psutil.process_iter(['pid','ppid','name','cmdline','memory_info']):
    try:
        d=p.info;command=' '.join(d['cmdline'] or [])
        if d['name'].lower()=='blender.exe' or ('python' in d['name'].lower() and ('render_pipeline_v14' in command or 'src/pipeline.py' in command)):
            rows.append({'pid':d['pid'],'parent':d['ppid'],'command':command,'rss':d['memory_info'].rss})
    except (psutil.NoSuchProcess,psutil.AccessDenied):pass
print(json.dumps({'memory':dict(psutil.virtual_memory()._asdict()),'processes':rows},ensure_ascii=False))
