"""Ray evidence for actual static route and follow-camera obstructions."""
import bpy,sys,json,math
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));import v15_route as route;import v15_motion as motion
bpy.ops.wm.open_mainfile(filepath=str(P/'model/babylon-city-v15.blend'));scene=bpy.context.scene
for ob in scene.objects:
 if ob.name.startswith('V15') and ob.parent:ob.hide_set(True)
deps=bpy.context.evaluated_depsgraph_get()
def solid(o):
 name=o.name.lower()
 return not any(s in name for s in ['citizen','resident','actor','soldier','priest','acolyte','envoy','attendant','crew','towman','crowd','offering','limb','foot','hand','v15'])
blocked=[];obscured=[];poses=[];corrections=[]
for i in range(32,360):
 t=i/4;s=route.state(t);pos=Vector(s['position']);ahead=Vector(route.position(min(90,t+.25)))-Vector(route.position(t));direction=Vector((ahead.x,ahead.y,0))
 if direction.length>.001:
  length=direction.length;direction.normalize()
  for z in [.35,1.0,1.9]:
   hit,point,normal,face,ob,matrix=scene.ray_cast(deps,pos+Vector((0,0,z)),direction,distance=length)
   if hit and solid(ob):blocked.append({'time':t,'height':z,'object':ob.name,'point':list(point)})
 p=motion.camera(t,corrected=False);start=Vector(p['position']);target=pos+Vector((0,0,1.2));delta=target-start
 hit,point,normal,face,ob,matrix=scene.ray_cast(deps,start,delta.normalized(),distance=max(.1,delta.length-1.0))
 if hit and solid(ob):
  obscured.append({'time':t,'object':ob.name,'distance_before_subject':(target-point).length})
  for rise in [4,8,12,18,25,35,50,65,85,110]:
   elevated=start+Vector((0,0,rise));ray=target-elevated
   hit2,point2,n2,f2,ob2,m2=scene.ray_cast(deps,elevated,ray.normalized(),distance=max(.1,ray.length-1))
   if not hit2 or not solid(ob2):corrections.append([t,rise+2]);break
 if i%4==0:poses.append({'time':t,'position':list(pos),'speed':s['speed'],'distance':s['distance']})
out={'path_samples':328,'route_hits':blocked,'camera_hits':obscured,'route_length':route.ARC[-1],'poses':poses,'note':'Static ray evidence only; crowd avoidance and final animation still need actual output inspection.'}
(P/'qa/v15/route-ray-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
(P/'qa/v15/camera-height-corrections.json').write_text(json.dumps({'samples':corrections,'method':'Minimum clear elevation at .25sec static-ray samples; smooth 1.25sec upper envelopes in camera function. Actual frames still required.'},indent=2),encoding='utf8')
print('V15_ROUTE_AUDIT',len(blocked),len(obscured),json.dumps(blocked[:8]+obscured[:8],ensure_ascii=False),flush=True)
