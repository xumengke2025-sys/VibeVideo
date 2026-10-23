import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
f=R/'assets/models/horse/riggedHorse.blend'
with bpy.data.libraries.load(str(f),link=False) as (src,dst):dst.objects=src.objects
rows=[]
for o in dst.objects:
    if o is None:continue
    bpy.context.collection.objects.link(o)
bpy.context.view_layer.update()
for o in dst.objects:
    if o is None:continue
    row={'name':o.name,'type':o.type,'location':list(o.location),'scale':list(o.scale),'dimensions':list(o.dimensions),'parent':o.parent.name if o.parent else None}
    if o.type=='MESH':row.update(verts=len(o.data.vertices),materials=[m.name for m in o.data.materials],modifiers=[(m.name,m.type) for m in o.modifiers])
    if o.type=='ARMATURE':row['bones']=[{'name':b.name,'head':list(b.head_local),'tail':list(b.tail_local),'parent':b.parent.name if b.parent else None} for b in o.data.bones]
    rows.append(row)
(f.parent/'inspection.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
print(json.dumps([{k:v for k,v in row.items() if k!='bones'} for row in rows],indent=2))
