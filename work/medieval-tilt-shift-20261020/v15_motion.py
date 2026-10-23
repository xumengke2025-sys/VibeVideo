"""Deterministic cyclist contacts, secondary cloth motion and true world follow."""
import bpy,math,json,bisect
from pathlib import Path
from mathutils import Vector,Matrix
import v15_route as route
def bone(ob,a,b):
 a,b=Vector(a),Vector(b);ob.location=(a+b)/2;ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();ob.scale.z=(b-a).length
def joint(a,b,length,bend):
 a,b=Vector(a),Vector(b);axis=(b-a).normalized();v=Vector(bend);v-=axis*v.dot(axis)
 if v.length<.001:v=Vector((1,0,0))
 return (a+b)/2+v.normalized()*math.sqrt(max(.0001,length*length-(a-b).length_squared/4))
def setup(scene):
 d=json.loads(scene['v15_rider']);d['root_ob']=bpy.data.objects[d['root']];d['objects']={k:bpy.data.objects[v] for k,v in d['parts'].items()};return d
def update(d,t):
 s=route.state(t);root=d['root_ob'];o=d['objects'];root.location=s['position'];root.rotation_euler=(0,s['lean'],s['yaw'])
 before=route.state(max(0,t-.08));after=route.state(min(90,t+.08));yaw_delta=(after['yaw']-before['yaw']+math.pi)%math.tau-math.pi
 steering=max(-.35,min(.35,math.atan(1.24*yaw_delta/.16/max(.5,s['speed'])))) if s['speed']>.15 else 0
 steering_pivot=Vector((0,.40,.96));steering_transform=Matrix.Translation(steering_pivot)@Matrix.Rotation(steering,4,'Z')@Matrix.Translation(-steering_pivot)
 if 'steering assembly' in o:o['steering assembly'].rotation_euler.z=steering
 for name in ['rear wheel','front wheel']:o[name].rotation_euler.x=s['wheel_angle']
 phi=s['crank_angle'];stop=s['stop'];max_leg=0;max_arm=0
 pivot=Vector((0,-.30,1.05));angle=-.06*s['hat_tip']-.60*s['duck'];upper=Matrix.Translation(pivot)@Matrix.Rotation(angle,4,'X')@Matrix.Translation(-pivot)
 for side in [-1,1]:
  angle=phi+(math.pi if side==1 else 0);center=Vector((side*.13,0,.43));pedal=center+Vector((0,.17*math.sin(angle),.17*math.cos(angle)))
  bone(o['crank '+str(side)],center,pedal);o['pedal '+str(side)].location=pedal
  hip=Vector((side*.11,-.30,1.05));foot=pedal+Vector((side*.01,0,.025))
  if side==-1:foot=foot.lerp(Vector((-.30,-.34,.012)),stop)
  knee=joint(hip,foot,.53,(0,1,.12));max_leg=max(max_leg,(hip-foot).length)
  bone(o['thigh '+str(side)],hip,knee);bone(o['shin '+str(side)],knee,foot);o['boot '+str(side)].location=foot;o['boot '+str(side)].rotation_euler.x=.05*math.sin(angle)*(1-stop)
  if 'knee joint '+str(side) in o:o['knee joint '+str(side)].location=knee
  shoulder=upper@Vector((side*.225,-.07,1.59));hand=steering_transform@Vector((side*.28,.53,1.22))
  if side==-1:
   wave=s['wave'];hand=hand.lerp(Vector((-.41,-.01,1.96+.07*math.sin(t*10))),wave)
   hand=hand.lerp(upper@Vector((-.16,.15,2.04)),s['hat_tip'])
  elbow=joint(shoulder,hand,.38,(side,-.2,-.6));max_arm=max(max_arm,(shoulder-hand).length)
  bone(o['upper arm '+str(side)],shoulder,elbow);bone(o['forearm '+str(side)],elbow,hand);o['hand '+str(side)].location=hand
  if 'elbow joint '+str(side) in o:o['elbow joint '+str(side)].location=elbow
  greeting=s['wave'] if side==-1 else 0
  wrist=o['hand '+str(side)];wrist.rotation_euler=(greeting*.65,0,steering*(1-greeting)-side*greeting*.15)
  if wrist.data.shape_keys:wrist.data.shape_keys.key_blocks['Open greeting'].value=greeting*(1-s['hat_tip'])
 for name in ['tailored torso','face and moustache','felt hat','scarf collar']:o[name].matrix_basis=upper
 for side in [-1,1]:
  o['coat tail '+str(side)].rotation_euler.x=.025*math.sin(t*5.7+side)+.035*min(1,s['speed']/5);o['coat tail '+str(side)].rotation_euler.y=side*.025*math.sin(t*4.1)
 scarf=o['scarf streamer'];pivot=Vector((0,-.02,1.74));scarf.matrix_basis=upper@Matrix.Translation(pivot)@Matrix.Rotation(.12*min(1,s['speed']/5)+.045*math.sin(t*6.1),4,'X')@Matrix.Rotation(.12*math.sin(t*3.3),4,'Z')@Matrix.Translation(-pivot)
 s.update(max_leg_reach=max_leg,max_arm_reach=max_arm)
 return s
RANGES=[(0,8),(8,19),(19,31),(31,44),(44,55),(55,64),(64,74),(74,81),(81,90)]
_path=Path(__file__).resolve().parent/'qa/v15/camera-height-corrections.json'
CORRECTIONS=json.loads(_path.read_text(encoding='utf8'))['samples'] if _path.exists() else []
def camera(t,corrected=True):
 s=route.state(t);p=Vector(s['position']);si=next((i for i,(a,b) in enumerate(RANGES) if a<=t<b),8);a,b=RANGES[si];u=route.ramp(t,a,b)
 if si==0:
  pos=Vector((-43,-126,6.6)).lerp(Vector((-47,-92,83)),u);target=Vector((0,60,9));lens=45+3*u
 else:
  offsets={1:(12,-9,20) if t<15 else (8,12,16),2:(8,12,16) if t<25 else (-12,-9,20),3:(8,12,16),4:(-8,12,16),5:(8,12,16),6:(-7,-8,14),7:(12,-9,20),8:(22,-32,44)}
  if si==3:
   v=route.ramp(t,38.2,39.5);offsets[3]=tuple(a+(b-a)*v for a,b in zip((8,12,16),(0,-3,25)))
  pos=p+Vector(offsets[si]);ahead=Vector(route.position(min(90,t+.8)))-Vector(route.position(t));target=p+Vector((ahead.x*.6,ahead.y*.6,1.0));lens=50 if si in [1,2,5,6,7] else 47
  # A short look-ahead keeps the cyclist visible while crossing the garden street.
  if si==4:target=p+Vector((ahead.x*.15,ahead.y*.15,1.0))
  if si==6:target=target.lerp(Vector((-48,147,2.1)),.23)
  if si==8:
   pos=p+Vector((22,-32,44)).lerp(Vector((-40,-95,150)),u);target=target.lerp(Vector((0,180,5)),u*.65);lens=47-2*u
 # Authored offsets were compared with static ray evidence. Do not use the
 # old per-hit elevation correction: it produced unwanted vertical excursions.
 return {'position':list(pos),'target':list(target),'lens':lens,'shot':si,'progress':u,'rider':s}
