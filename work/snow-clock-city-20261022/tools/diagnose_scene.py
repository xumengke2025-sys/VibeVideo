import bpy, json, collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'model/clock-city-production-v2.blend'))
d=bpy.context.evaluated_depsgraph_get()
counts=[]
for o in bpy.data.objects:
 if o.type=='MESH':
  e=o.evaluated_get(d)
  counts.append(dict(name=o.name,mesh=o.data.name,base=len(o.data.polygons),evaluated=len(e.data.polygons),modifiers=[(m.type,getattr(m,'levels',None),getattr(m,'render_levels',None)) for m in o.modifiers],users=o.data.users))
instances=collections.Counter(i.object.original.name for i in d.object_instances)
report=dict(objects=len(bpy.data.objects),largest=sorted(counts,key=lambda x:x['evaluated'],reverse=True)[:35],instances=instances,images=[dict(name=i.name,size=list(i.size),channels=i.channels) for i in bpy.data.images])
(R/'render/scene-memory-diagnostic.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('DIAGNOSTIC_DONE',flush=True)
