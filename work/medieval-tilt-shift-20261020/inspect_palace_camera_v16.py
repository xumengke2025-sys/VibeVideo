import bpy,sys,json,itertools
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));import v15_route
bpy.ops.wm.open_mainfile(filepath=str(P/'model/babylon-city-v16-palace.blend'))
s=bpy.context.scene;c=s.camera;s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.resolution_percentage=100
data=[]
for pos,lens,target in [((-60,0,95),30,(60,8,7)),((-80,-35,100),25,(46,16,7)),((-60,-45,95),24,(47,18,8)),((-75,-30,100),28,(55,12,7))]:
 c.location=pos;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=lens;bpy.context.view_layer.update()
 points=[world_to_camera_view(s,c,Vector(p)) for p in itertools.product([53,100],[-27,27],[.4,13])]+[world_to_camera_view(s,c,Vector(p)) for p in itertools.product([84,97],[-10,10],[20,26.5])]
 rider=[list(world_to_camera_view(s,c,Vector(v15_route.state(t)['position'])+Vector((0,0,1)))) for t in [25,27,29,30.95]]
 data.append({'position':pos,'lens':lens,'target':target,'palace_bbox':[min(p.x for p in points),min(p.y for p in points),max(p.x for p in points),max(p.y for p in points)],'rider':rider})
(P/'qa/v16/camera-candidates.json').write_text(json.dumps(data,indent=2),encoding='utf8');print('CAMERA_CANDIDATES',json.dumps(data),flush=True)
