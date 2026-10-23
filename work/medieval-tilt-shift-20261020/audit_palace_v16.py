import bpy,sys,json,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));import v16_camera,v15_route
bpy.ops.wm.open_mainfile(filepath=str(P/'model/babylon-city-v16-palace.blend'))
s=bpy.context.scene;c=s.camera;s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.resolution_percentage=100
deps=bpy.context.evaluated_depsgraph_get();rows=[]
for i in range(25*4,31*4):
 t=i/4;pose=v16_camera.camera(t);c.location=pose['position'];c.rotation_euler=(Vector(pose['target'])-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=pose['lens'];bpy.context.view_layer.update()
 p=Vector(v15_route.state(t)['position'])+Vector((0,0,1.8));d=p-c.location;hit,where,n,index,ob,matrix=s.ray_cast(deps,c.location,d.normalized(),distance=d.length-.30)
 rows.append({'time':t,'projection':list(world_to_camera_view(s,c,p)),'static_occluder':ob.name if hit else None})
(P/'qa/v16/palace-rider-visibility.json').write_text(json.dumps(rows,indent=2),encoding='utf8');print('RIDER_OCCLUSION',json.dumps([r for r in rows if r['static_occluder']]),flush=True)
