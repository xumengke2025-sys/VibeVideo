"""Create separate versioned production entry without altering v14 frozen inputs."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
s=(P/'render_city_v14.py').read_text(encoding='utf8').replace('v14','v15').replace('V14','V15')
# Reuse the completed city actions and cached population; the rider has its own clock.
s=s.replace('import v15_motion','import v14_motion\nimport v15_motion')
s=s.replace('v15data=v15_motion.setup(scene)','v14data=v14_motion.setup(scene)\nrider_data=v15_motion.setup(scene)')
s=s.replace('detail=v15_motion.update(v15data,t)','detail=v14_motion.update(v14data,t)')
s=s.replace("w=v15data['wakes'][-1]","w=v14data['wakes'][-1]")
s=s.replace("traffic-v15.npz","traffic-v14.npz").replace("v15-timeline.json","v14-timeline.json")
s=s.replace("def at(t):","def city_at(t):")
s=s.replace("scene.frame_end=1824","scene.frame_end=2160")
insertion='''
def at(t):
 state=city_at(min(75.95,t*76/90))
 pose=v15_motion.camera(t);action=v15_motion.update(rider_data,t)
 cam.location=pose['position'];target=Vector(pose['target']);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=pose['lens']
 if mode=='character':
  base=Vector(action['position']);cam.location=base+Vector((3.2,3.8,2.8));target=base+Vector((0,0,1.08));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=60
 bpy.context.view_layer.update();subject=Vector(action['position'])+Vector((0,0,1.15));projected=world_to_camera_view(scene,cam,subject)
 focus.outputs[0].default_value=1/max(.1,(subject-cam.location).length)
 # Smoothly open a small corridor around this persistent moving protagonist.
 forward=Vector((-math.sin(action['yaw']),math.cos(action['yaw']),0));normal=Vector((forward.y,-forward.x,0));rp=Vector(action['position'])
 for ob in v15actors+mid_objects+v8crowd:
  delta=ob.location-rp;along=delta.dot(forward);across=delta.dot(normal)
  if abs(along)<3.8 and abs(across)<1.15 and ob.location.z<2:
   weight=smooth((3.8-abs(along))/1.5);shift=(1.15-abs(across))*weight*(1 if across>=0 else -1);ob.location+=normal*shift
 for ob,ev,keys in zip(special_objects,special,special_keys):
  role=ev['role'];response=0
  if role in ['envoy','attendant']:response=v15_motion.route.pulse(t,12.7,13.4,15.2,16)
  elif role=='crew':response=v15_motion.route.pulse(t,35.8,36.5,38,39)
  if response:
   delta=rp-ob.location;look=math.atan2(delta.x,-delta.y);difference=(look-ob.rotation_euler.z+math.pi)%math.tau-math.pi;ob.rotation_euler.z+=difference*.7*response;blend_pose(keys,.5+.35*response*math.sin(t*3))
 # West-bank team stays on its paved towpath while passing the cyclist.
 for tow in tows:
  if tow.get('bank_side')=='west':
   for name in tow['team']:
    man=special_objects[special_index[name]];gap=abs(man.location.y-rp.y);man.location.x+=.45*smooth((4-gap)/2) if gap<4 and abs(rp.x-22.8)<1 else 0
 bpy.context.view_layer.update()
 for tow in tows:
  par=bpy.data.objects[tow['boat']];anchor=par.matrix_world@Vector(tow['attachment']);points=bpy.data.objects[tow['rope']].data.splines[0].points
  lead=special_objects[special_index[tow['team'][0]]];end=lead.matrix_world@Vector((0,-.2,1.16))
  for j,point in enumerate(points[:9]):
   u=j/8;v=anchor.lerp(end,u);v.z-=.27*math.sin(math.pi*u);point.co=(*v,1)
  for j,name in enumerate(tow['team'][1:],9):
   man=special_objects[special_index[name]];v=man.matrix_world@Vector((0,-.2,1.16));points[j].co=(*v,1)
 half=.13 if pose['shot'] in [3,6] else .095
 if mode=='character':half=.44
 if pose['shot']==8:half=.12+.075*pose['progress']
 band_center.outputs[0].default_value=max(.22,min(.76,projected.y));band_half.outputs[0].default_value=half;band_tilt.outputs[0].default_value=.035
 blur_strength.outputs[0].default_value=smooth(t/3)*(.9-.18*pose['progress'] if pose['shot']==8 else 1)
 f=smooth(t/.18)*(1-smooth((t-88.5)/1.5));fade.inputs[2].default_value=(f,f,f,1)
 state.update(time=t,shot=pose['shot'],position=list(cam.location),target=list(target),lens=cam.data.lens,rider=action,rider_projection=list(projected))
 return state

'''
s=s.replace("if mode=='audit':",insertion+"if mode=='audit':")
s=s.replace("for seconds in [53.5,55,56.3,57.2,58.2,59.5,60.4,61.2,61.8,31.5,73,57.2]:", "for seconds in [0,8,13.5,22,29,36,50.5,64,67.8,70,76,86,13.5]:")
s=s.replace("max(r['action']['offering_max_reach'] for r in report)","max(r['rider']['max_arm_reach'] for r in report)")
s=s.replace("if mode=='proof':frames=[24,288,528,756,1115,1392,1752]","if mode=='character':frames=[528,1632]\nelif mode=='proof':frames=[96,324,552,864,1212,1536,1632,1872,2064]")
s=s.replace("else:frames=list(range(1824))","else:frames=list(range(2160))")
s=s.replace("if mode=='preview':scene.render.resolution_percentage=50;scene.cycles.samples=20","if mode=='preview':scene.render.resolution_percentage=35;scene.cycles.samples=12\nif 'CITY_SCALE' in os.environ:scene.render.resolution_percentage=int(os.environ['CITY_SCALE'])")
s=s.replace("if mode=='stills':scene.cycles.samples=32","if mode in ['stills','character']:scene.cycles.samples=32")
(P/'render_city_v15.py').write_text(s,encoding='utf8')
print('V15_RENDERER_PREPARED')
