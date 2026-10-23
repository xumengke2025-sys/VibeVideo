import bpy,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'model/babylon-city-v8.blend'))
rows=[]
for ob in bpy.context.scene.objects:
    if any(s in ob.name.lower() for s in ['bridge','lateen','boat mast','sail edge']):
        pts=[ob.matrix_world@Vector(v) for v in ob.bound_box] if ob.type in ['MESH','CURVE'] else [ob.location]
        rows.append({'name':ob.name,'parent':ob.parent.name if ob.parent else None,'min':[round(min(v[i] for v in pts),3) for i in range(3)],'max':[round(max(v[i] for v in pts),3) for i in range(3)]})
(ROOT/'qa/v9').mkdir(exist_ok=True,parents=True)
(ROOT/'qa/v9/geometry-before.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
print(json.dumps(rows,indent=2),flush=True)
