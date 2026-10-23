import bpy,bmesh,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'babylon-city-v8.blend'))
count=0
for mesh in bpy.data.meshes:
    if mesh.name.startswith('V8 shared sculptural sphere'):
        bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free();count+=1
# Move east quay pedestrians away from the raised temple forecourt.
for kind in ['royal','divine']:
    col=bpy.data.collections.get('V8 '+kind+' statue module')
    if col and not any(o.name.startswith('V8 closed royal crown') for o in col.objects):
        bm=bmesh.new();bmesh.ops.create_uvsphere(bm,u_segments=24,v_segments=12,radius=1)
        me=bpy.data.meshes.new('V8 closed crown mesh');bm.to_mesh(me);bm.free()
        me.materials.append(bpy.data.materials['Lapis fired glaze 1'])
        for p in me.polygons:p.use_smooth=True
        ob=bpy.data.objects.new('V8 closed royal crown',me);col.objects.link(ob)
        ob.location=(0,0,4.54);ob.scale=(.18,.18,.085)
for name in json.loads(bpy.context.scene['v8_crowd']):
    ob=bpy.data.objects[name]
    if ob.location.x>40:
        ob.location.x=21.1;ob['base']=list(ob.location)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'babylon-city-v8.blend'))
print('V8_NORMALS_AND_QUAY',count,flush=True)
