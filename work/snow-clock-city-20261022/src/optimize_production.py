"""Render-specific forest LOD; preserve the fully editable original production v2."""
import bpy,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'model/clock-city-production-v2.blend'))
before=sum(len(m.polygons) for m in bpy.data.meshes)
changes=[]
for i in range(3):
 high=bpy.data.collections.get('ENV Fir variant '+str(i)+' LOD0')
 low=bpy.data.collections['ENV Fir variant '+str(i)+' LOD1']
 for ob in bpy.data.objects:
  if ob.instance_collection==high:ob.instance_collection=low
 for ob in list(low.objects):
  if ob.type!='MESH':continue
  original=len(ob.data.polygons)
  # Source objects live outside the active scene; use a temporary scene link.
  temp=ob.name not in bpy.context.scene.objects
  if temp:bpy.context.scene.collection.objects.link(ob)
  bpy.context.view_layer.update();bpy.context.view_layer.objects.active=ob
  ob.select_set(True)
  mod=ob.modifiers.new('Forest render LOD - scan silhouette retained','DECIMATE');mod.ratio=.18
  bpy.ops.object.modifier_apply(modifier=mod.name)
  ob.select_set(False)
  if temp:bpy.context.scene.collection.objects.unlink(ob)
  changes.append(dict(name=ob.name,before=original,after=len(ob.data.polygons)))
 if high:
  for ob in list(high.objects):bpy.data.objects.remove(ob,do_unlink=True)
  bpy.data.collections.remove(high)
bpy.data.orphans_purge(do_recursive=True)
bpy.ops.file.pack_all()
bpy.context.scene['render_lod_note']='All trees use shared 4% scan LOD; original high-resolution geometry remains in production-v2.blend. Buildings and hero action unchanged.'
out=R/'model/clock-city-production-v3.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(out))
(R/'render/production-lod-report.json').write_text(json.dumps(dict(model=str(out),before_faces=before,after_faces=sum(len(m.polygons) for m in bpy.data.meshes),trees=changes),indent=2),encoding='utf8')
print('LOD_MODEL_READY',flush=True)
