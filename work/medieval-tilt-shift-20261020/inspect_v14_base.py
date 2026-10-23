import bpy,json
from pathlib import Path
P=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(P/'model/babylon-city-v13.blend'))
s=bpy.context.scene
def info(o):
 return {'name':o.name,'type':o.type,'location':list(o.location),'scale':list(o.scale),'rotation':list(o.rotation_euler),'dimensions':list(o.dimensions),'parent':o.parent.name if o.parent else None,'collection':o.instance_collection.name if o.instance_collection else None,'materials':[m.name for m in o.data.materials] if o.type=='MESH' else []}
patterns=('quay','water','garden','statue','grain','shrine','boat','Metropolis','Courtyard','V12 circulating')
objects={k:[info(o) for o in s.objects if k.lower() in o.name.lower()][:25] for k in patterns}
mats=[]
for m in bpy.data.materials:
 if m.use_nodes:
  ps=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
  mats.append({'name':m.name,'users':m.users,'color':list(ps.inputs['Base Color'].default_value) if ps else None,'nodes':[n.name for n in m.node_tree.nodes]})
d={'objects':objects,'materials':mats,'special':json.loads(s['v12_special']),'tows':json.loads(s['v12_tows']),'boats':[info(bpy.data.objects[n])|{'base':list(bpy.data.objects[n]['base']),'speed':bpy.data.objects[n]['speed']} for n in json.loads(s['v8_boats'])], 'keys':list(s.keys())}
q=P/'qa/v14';q.mkdir(parents=True,exist_ok=True)
(q/'base-inventory.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print('V14_BASE_INVENTORY',len(s.objects),len(mats),len(d['special']),flush=True)
