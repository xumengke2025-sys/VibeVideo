import bpy,json
from pathlib import Path
from collections import Counter
P=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(P/'model/babylon-city-v15-detail.blend'))
items=[]
for o in bpy.context.scene.objects:
 if 44<o.location.x<106 and -35<o.location.y<32:
  items.append({'name':o.name,'type':o.type,'pos':list(o.location),'dimensions':list(o.dimensions),'collection':o.instance_collection.name if o.instance_collection else None,'parent':o.parent.name if o.parent else None})
(P/'qa/v16').mkdir(parents=True,exist_ok=True)
(P/'qa/v16/site-before.json').write_text(json.dumps(items,indent=2),encoding='utf8')
print('SITE_ITEMS',len(items),json.dumps(Counter(i['name'].split('.')[0] for i in items).most_common(25)),flush=True)
