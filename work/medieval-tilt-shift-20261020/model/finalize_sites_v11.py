"""Remove inherited enclosure strip where the new shrine replaces that site."""
from pathlib import Path
import bpy,bmesh,json
from mathutils import Vector
root=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(root/'babylon-city-v11.blend'))
with bpy.data.libraries.load(str(root/'babylon-city-v10.blend'),link=False) as (source,dest):
 inherited=set(source.objects)
changed=[]
for ob in list(bpy.context.scene.objects):
 if ob.name not in inherited or ob.type!='MESH':continue
 bounds=[ob.matrix_world@Vector(c) for c in ob.bound_box]
 lo=[min(v[k] for v in bounds) for k in range(3)];hi=[max(v[k] for v in bounds) for k in range(3)]
 if not (145<lo[1] and hi[1]<155 and lo[0]<-34.5 and hi[0]>-60):continue
 ob.data=ob.data.copy();bm=bmesh.new();bm.from_mesh(ob.data)
 inverse=ob.matrix_world.inverted()
 normal=ob.matrix_world.to_3x3().transposed()@Vector((1,0,0))
 for x in [-60,-34.5]:
  bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.0001,plane_co=inverse@Vector((x,149,0)),plane_no=normal)
 remove=[face for face in bm.faces if -60.0001<(ob.matrix_world@face.calc_center_median()).x<-34.4999]
 old=len(bm.faces)
 bmesh.ops.delete(bm,geom=remove,context='FACES')
 orphans=[v for v in bm.verts if not v.link_faces]
 if orphans:bmesh.ops.delete(bm,geom=orphans,context='VERTS')
 bm.to_mesh(ob.data);bm.free()
 changed.append({'object':ob.name,'faces_before':old,'faces_after':len(ob.data.polygons)})
bpy.ops.wm.save_as_mainfile(filepath=str(root/'babylon-city-v11.blend'))
(root.parent/'qa/v11/shrine-wall-clearance.json').write_text(json.dumps({'cut_world_x':[-60,-34.5],'inherited_y_strip':[145,155],'changed':changed,'ends':'Replacement temple side wings conceal enclosure cut ends.'},indent=2),encoding='utf8')
print('V11_SHRINE_ENCLOSURE_CLEARED',len(changed))
