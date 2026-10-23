"""Compare authored follow offsets against static scenery; no renderer or mutation."""
import bpy,sys,json,math
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));import v15_route as r
bpy.ops.wm.open_mainfile(filepath=str(P/'model/babylon-city-v15.blend'));scene=bpy.context.scene
for ob in scene.objects:
 if ob.name.startswith('V15') and ob.parent:ob.hide_set(True)
deps=bpy.context.evaluated_depsgraph_get()
def solid(ob):
 return not any(s in ob.name.lower() for s in ['citizen','resident','actor','soldier','priest','acolyte','envoy','attendant','crew','towman','crowd','offering','limb','foot','hand','v15'])
offsets=[(0,-12,17),(0,12,17),(8,12,16),(-8,12,16),(12,-9,20),(-12,-9,20),(8,5,23),(-8,5,23),(0,-3,25),(0,3,25),(16,0,25),(-16,0,25)]
segments=[(8,15),(15,19),(19,25),(25,31),(31,39),(39,44),(44,51),(51,55),(55,64),(64,74),(74,81),(81,87)]
report=[]
for a,b in segments:
 scores=[]
 for off in offsets:
  hits=[]
  for j in range(round(a*4),round(b*4)):
   t=j/4;target=Vector(r.state(t)['position'])+Vector((0,0,1.2));start=target+Vector(off);delta=target-start
   hit,point,n,f,ob,m=scene.ray_cast(deps,start,delta.normalized(),distance=delta.length-.8)
   if hit and solid(ob):hits.append([t,ob.name])
  scores.append({'offset':off,'hits':len(hits),'examples':hits[:4]})
 report.append({'range':[a,b],'candidates':sorted(scores,key=lambda x:x['hits'])})
(P/'qa/v15/camera-candidates.json').write_text(json.dumps(report,indent=2),encoding='utf8')
for d in report:print('CAMERA_CANDIDATE',d['range'],d['candidates'][:3],flush=True)
