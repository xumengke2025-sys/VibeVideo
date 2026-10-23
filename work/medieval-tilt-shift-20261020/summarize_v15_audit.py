from pathlib import Path
import json,collections
P=Path(__file__).resolve().parent;d=json.loads((P/'qa/v15/route-ray-audit.json').read_text(encoding='utf8'))
for key in ['route_hits','camera_hits']:
 groups=collections.defaultdict(list)
 for r in d[key]:groups[r['object']].append(r['time'])
 print(key,json.dumps({k:[round(min(v),2),round(max(v),2),len(v)] for k,v in groups.items()},ensure_ascii=False))
