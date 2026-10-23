import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'model/babylon-city-v11.blend'))
scene=bpy.context.scene
names=json.loads(scene['v8_boats'])+['Animated canal boat']
out={'boats':[],'resident':[],'roads':[],'animation':[]}
for name in names:
 ob=bpy.data.objects[name]
 out['boats'].append({'name':name,'location':list(ob.location),'rotation':list(ob.rotation_euler),'properties':{k:ob[k] for k in ob.keys()},'children':[{'name':c.name,'location':list(c.location),'bounds':[list(v) for v in c.bound_box]} for c in ob.children]})
for ob in bpy.data.collections['V8 resident module 0'].objects:out['resident'].append({'name':ob.name,'location':list(ob.location),'dimensions':list(ob.dimensions)})
for ob in scene.objects:
 if any(s in ob.name.lower() for s in ['avenue','road','cross street','quay paving','paving']):
  out['roads'].append({'name':ob.name,'location':list(ob.location),'dimensions':list(ob.dimensions)})
 if ob.animation_data:out['animation'].append(ob.name)
(ROOT/'qa/v12/scene-inventory.json').write_text(json.dumps(out,indent=2,default=list),encoding='utf8')
print('INVENTORY_READY',len(scene.objects),len(bpy.data.materials),flush=True)
