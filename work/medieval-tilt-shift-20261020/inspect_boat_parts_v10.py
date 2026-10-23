import bpy,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'model/babylon-city-v9.blend'))
rows=[]
for ob in bpy.context.scene.objects:
    if ob.name.startswith(('Boat crossbench','Carvel wooden river boat','Raised boat gunwale','Animated canal boat')):
        pts=[ob.matrix_world@Vector(v) for v in ob.bound_box] if ob.type in ['MESH','CURVE'] else [ob.location]
        rows.append({'name':ob.name,'type':ob.type,'parent':ob.parent.name if ob.parent else None,'vertices':len(ob.data.vertices) if ob.type=='MESH' else None,'min':[round(min(v[i] for v in pts),4) for i in range(3)],'max':[round(max(v[i] for v in pts),4) for i in range(3)]})
(ROOT/'qa/v10').mkdir(parents=True,exist_ok=True)
(ROOT/'qa/v10/boat-parts-before.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
print('BOAT_PARTS_INSPECTED',len(rows),flush=True)
