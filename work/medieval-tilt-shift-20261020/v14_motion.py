"""Absolute-time v14 local actions. Requires Blender; no independent clocks."""
import bpy,math,json
from mathutils import Vector
def smooth(x):
 x=max(0,min(1,x));return x*x*(3-2*x)
def ramp(t,a,b):return smooth((t-a)/(b-a))
def blend(a,b,u):return Vector(a).lerp(Vector(b),u)
def setup(scene):
 return {'rigs':json.loads(scene['v14_rigs']),'wakes':json.loads(scene['v14_wakes'])}
def bone(ob,a,b):
 a,b=Vector(a),Vector(b);ob.location=(a+b)/2;ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();ob.scale.z=(b-a).length
def update(data,t):
 # Bowl is held by giver, shared at transfer, held by receiver, then on the altar.
 meet=ramp(t,55,56.3);take=ramp(t,57.2,58.2);turn=ramp(t,58.2,59.5);advance=ramp(t,59.5,60.4);setdown=ramp(t,60.4,61.2);release=ramp(t,61.2,61.8)
 giver=Vector((-49,147,1.02));receiver=Vector((-47.85,147+.27*advance,1.02))
 yaw=-math.pi/2-math.pi/2*turn
 front=Vector((math.sin(yaw),-math.cos(yaw),0))
 bowl=blend((-48.62,147,2.18),(-48.43,147,2.18),meet)
 held=receiver+front*.43+Vector((0,0,1.18))
 bowl=bowl.lerp(held,take);bowl=bowl.lerp(Vector((-47.85,147.85,2.055)),setdown)
 dish=bpy.data.objects['V14 persistent offering dish'];dish.location=bowl
 angle=yaw+math.pi/2 if take else 0
 grip_axis=Vector((math.cos(yaw),math.sin(yaw),0))
 max_reach=0
 for cfg in data['rigs']:
  i=cfg['index'];root=bpy.data.objects[cfg['root']];root.location=giver if i==0 else receiver;root.rotation_euler.z=math.pi/2 if i==0 else yaw
  bpy.context.view_layer.update();inv=root.matrix_world.inverted()
  for side in [-1,1]:
   shoulder=Vector((side*.22,0,1.31));rest=Vector((side*.27,-.10,.86))
   if i==0:
    contact=bowl+Vector((-.17,side*.15,.055));hand=inv@contact
    hand=hand.lerp(rest,ramp(t,57.3,58.3))
   else:
    contact=bowl+grip_axis*(side*.16)-front*.17+Vector((0,0,.055));hand=rest.lerp(inv@contact,ramp(t,55.8,57.1));hand=hand.lerp(rest,release)
   v=hand-shoulder;d=v.length;max_reach=max(max_reach,d)
   axis=v.normalized();bend=Vector((0,.0,-1));bend-=axis*bend.dot(axis)
   if bend.length<.001:bend=Vector((0,1,0))
   elbow=(shoulder+hand)/2+bend.normalized()*math.sqrt(max(.002,.32**2-(d/2)**2))
   pieces=cfg['parts'];bone(bpy.data.objects[pieces[f'{side}:upper']],shoulder,elbow);bone(bpy.data.objects[pieces[f'{side}:forearm']],elbow,hand);bpy.data.objects[pieces[f'{side}:hand']].location=hand
   foot=Vector((side*.12,-.035,.06));hip=Vector((side*.10,0,.73));knee=Vector((side*.11,-.04,.40))
   if i==1 and 59.5<t<60.4:foot.y+=side*.075*math.sin((t-59.5)/.9*math.tau);foot.z+=max(0,side*math.sin((t-59.5)/.9*math.tau))*.045
   bone(bpy.data.objects[pieces[f'{side}:thigh']],hip,knee);bone(bpy.data.objects[pieces[f'{side}:shin']],knee,foot);bpy.data.objects[pieces[f'{side}:foot']].location=foot
 # Wake direction and strength follow actual analytic boat velocity.
 for w in data['wakes']:
  boat=bpy.data.objects[w['boat']];ob=bpy.data.objects[w['name']];center=boat.matrix_world@Vector(w['center']);speed=-.58 if w['index']==4 else math.cos(math.floor(t*8)/8*.04)*boat['speed']*.48
  ob.location=(center.x,center.y,.249);ob.rotation_euler.z=0 if speed>=0 else math.pi;ob.scale.y=.65+min(1,abs(speed)*1.2)
  ob.hide_render=abs(speed)<.015
 water=bpy.data.materials['Canal water / rippled reflection'];water.node_tree.nodes['V14 long current'].inputs['W'].default_value=t*.035
 return {'offering_dish':list(bowl),'offering_max_reach':max_reach,'offering_stage':('rest' if t<55 else 'handover' if t<58.2 else 'turn' if t<59.5 else 'place' if t<61.2 else 'resting_on_table')}
