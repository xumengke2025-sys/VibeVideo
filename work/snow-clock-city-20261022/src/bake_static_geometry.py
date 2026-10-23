"""Bake rigid bevel/normal modifiers once; keep rigs and original source models."""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'model/clock-city-production-v3.blend'))
deps=bpy.context.evaluated_depsgraph_get();done=[]
for ob in list(bpy.data.objects):
 if ob.type!='MESH' or not ob.modifiers:continue
 if any(m.type not in {'BEVEL','WEIGHTED_NORMAL','TRIANGULATE'} for m in ob.modifiers):continue
 old=len(ob.data.polygons)
 mesh=bpy.data.meshes.new_from_object(ob.evaluated_get(deps),preserve_all_data_layers=True,depsgraph=deps)
 for mod in list(ob.modifiers):ob.modifiers.remove(mod)
 ob.data=mesh
 done.append(dict(name=ob.name,before=old,after=len(mesh.polygons)))
bpy.data.orphans_purge(do_recursive=True)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'model/clock-city-production-v4.blend'))
(R/'render/static-geometry-bake.json').write_text(json.dumps(dict(objects=len(done),baked=done),indent=2),encoding='utf8')
print('STATIC_BAKE_READY',len(done),flush=True)
