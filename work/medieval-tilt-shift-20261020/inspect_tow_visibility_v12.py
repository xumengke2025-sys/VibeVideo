import bpy,json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parent
source=(ROOT/'render_city_v12.py').read_text(encoding='utf8').split("if mode=='proof':frames=")[0]
exec(compile(source,str(ROOT/'render_city_v12.py'),'exec'),globals())
records=[]
for t in [27.5,31.5,36]:
 at(t);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
 for ob,ev in zip(special_objects,special):
  if ev['kind']!='tow':continue
  p=ob.matrix_world@Vector((0,0,1.35));delta=p-cam.location
  hit,point,normal,index,blocker,matrix=scene.ray_cast(dg,cam.location,delta.normalized(),distance=delta.length-.12)
  samples=[]
  for x in [21.6,22.2,22.7,23.2,23.7,24.2]:
   q=Vector((x,p.y,p.z));d=q-cam.location
   visible,v,n,i,blocker2,m=scene.ray_cast(dg,cam.location,d.normalized(),distance=d.length-.12)
   down,ground,nn,ii,groundob,mm=scene.ray_cast(dg,Vector((x,p.y,5)),Vector((0,0,-1)),distance=6)
   samples.append({'x':x,'blocker':blocker2.name if visible else None,'surface_z':ground.z if down else None,'surface':groundob.name if down else None})
  records.append({'time':t,'name':ob.name,'world':list(p),'blocker':blocker.name if hit else None,'block_position':list(point) if hit else None,'candidate_positions':samples})
(ROOT/'qa/v12/tow-visibility-diagnosis.json').write_text(json.dumps(records,indent=2),encoding='utf8')
for r in records:print('TOW_VISIBILITY',r['time'],r['name'],r['world'],r['blocker'],r['candidate_positions'],flush=True)
