"""Absolute-time deterministic state. Shared contact anchors and carrier path.
Can be loaded into Blender to bake editable animation, or used frame-addressably.
"""
import bpy, math, json
from mathutils import Vector
S=bpy.context.scene;O=bpy.data.objects;A=Vector(S['cable_A']);B=Vector(S['cable_B'])
road=[Vector(p) for p in json.loads(S['road'])];length=[0]
for a,b in zip(road,road[1:]):length.append(length[-1]+(b-a).length)
def sm(x):x=max(0,min(1,x));return x*x*(3-2*x)
def ramp(t,a,b):return sm((t-a)/(b-a))
def lerp(a,b,u):return Vector(a).lerp(Vector(b),u)
def cable(u):
 p=A.lerp(B,u);p.z-=.85*4*u*(1-u);return p
def basket_u(t):
 if t<26:return 0
 if t<46:return sm((t-26)/20)
 if t<76:return 1
 return 1-.72*sm((t-76)/14)
def carrier_at(t):return cable(basket_u(t))-Vector((0,0,3.8))
def ground(x,y):return max(0,.12*(y+20))+2*sm((y-12)/10)+.12*math.sin(x*.18)*math.sin(y*.12)
def road_at(d):
 d=max(0,min(length[-1]-.001,d));i=next(i for i in range(len(length)-1) if length[i]<=d<length[i+1]);u=(d-length[i])/(length[i+1]-length[i]);p=road[i].lerp(road[i+1],u);tan=road[i+1]-road[i];return p,-math.atan2(tan.x,tan.y)+math.pi
def set_segment(ob,a,b):
 a,b=Vector(a),Vector(b);ob.location=a;ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();ob.scale=(1,1,(b-a).length)
def pose_person(root,t,phase=0,walk=0,hands=None):
 name=root.name
 for sg in [-1,1]:
  leg=O[name+' leg '+str(sg)];leg.rotation_euler.x=walk*.5*math.sin(phase+(math.pi if sg==1 else 0))
  shoulder=Vector((sg*.235,0,1.24))
  hand=Vector(hands[sg] if hands else (sg*.30,-.08+walk*.19*math.sin(phase+(math.pi if sg==-1 else 0)),.80))
  # Geometric two-bone IK; wrist remains exactly on the authored grip.
  delta=hand-shoulder;dist=delta.length;mid=(shoulder+hand)*.5
  bend=Vector((sg*.3,-.65,-.15));bend-=delta.normalized()*bend.dot(delta.normalized());bend.normalize();elbow=mid+bend*math.sqrt(max(.003,.47**2-(dist/2)**2))
  set_segment(O[name+' upper arm '+str(sg)],shoulder,elbow);set_segment(O[name+' fore arm '+str(sg)],elbow,hand);O[name+' hand '+str(sg)].location=hand
def crate_at(t):
 bp=carrier_at(t)+Vector((0,0,.18));initial=A-Vector((0,0,3.8))+Vector((1.75,-.15,.18))
 if t<20:return initial
 if t<21:return initial+Vector((0,0,1.05*ramp(t,20,21)))
 if t<22:return (initial+Vector((0,0,1.05))).lerp(bp+Vector((0,0,1.05)),ramp(t,21,22))
 if t<23:return bp+Vector((0,0,1.05*(1-ramp(t,22,23))))
 if t<50:return bp
 raised=B-Vector((0,0,3.8))+Vector((0,0,1.23));dest=Vector((10.5,3.0,ground(8,1)+.8+.97))
 if t<52:return bp.lerp(raised,ramp(t,50,52))
 clear=raised+Vector((0,1.5,0));highdest=Vector((dest.x,dest.y,raised.z))
 if t<53.5:return raised.lerp(clear,ramp(t,52,53.5))
 if t<55:return clear.lerp(highdest,ramp(t,53.5,55))
 return highdest.lerp(dest,ramp(t,55,56))
def pose(t):
 p0=carrier_at(27);p1=carrier_at(43)
 keys=[(0,(55,-78,29),(-2,7,12),47),(12,(50,-68,70),(0,12,8),47),(18,(9,-1,31),(-13,22,9),52),(23,(0,3,25),(-12,21,9),55),(27,tuple(p0+Vector((13,-21,17))),tuple(p0+Vector((0,0,.8))),53),(43,tuple(p1+Vector((11,-18,14))),tuple(p1+Vector((0,0,.8))),55),(48,(20,2,16),(9,1.8,4.8),57),(59,(20,2,16),(9.2,2,4.8),57),(64,(6,-5,21),(-2,5.3,13.8),58),(68,(6,-5,21),(-2,5.3,13.8),58),(74,(27,-32,34),(3,2,6),48),(86,(65,-92,97),(0,15,12),46),(90,(68,-96,101),(0,15,12),46)]
 for a,b in zip(keys,keys[1:]):
  if a[0]<=t<=b[0]:
   u=sm((t-a[0])/(b[0]-a[0]));return lerp(a[1],b[1],u),lerp(a[2],b[2],u),a[3]+(b[3]-a[3])*u
 return Vector(keys[-1][1]),Vector(keys[-1][2]),keys[-1][3]
def at(t):
 S.frame_set(round(t*24)+1);bp=carrier_at(t);O['Red carrier'].location=bp
 u=basket_u(t);moving=0<t-26<20 or t>76
 # Pure world-Z hang: a tiny wind sway is local, never aligned to cable slope.
 sway=.012*math.sin(t*2.2)*math.sin(math.pi*u) if moving else 0;O['Red carrier'].rotation_euler=(sway,0,0)
 O['Basket lid hinge'].rotation_euler.y=-1.50*(1-ramp(t,24,25)) if t<26 else -1.5*(ramp(t,48,49.5)*(1-ramp(t,71,73)))
 cp=crate_at(t);O['Persistent bread crate'].location=cp;O['Bread crate lid'].rotation_euler.x=-1.55*ramp(t,57,58)
 for sg in [-1,1]:O['Dock locking jaw '+str(sg)].location.x=8+sg*(1.22-.17*ramp(t,46.5,47.5)*(1-ramp(t,73,74)))
 for nm in ['Upper','Square']:O[nm+' drive wheel'].rotation_euler.y=-u*62
 # Loader follows crate grips through the upper loading action, then releases.
 baker=O['Baker'];baker.location=(cp.x,cp.y+.60,A.z-4.8+.85) if t<23 else (A.x+1.8,A.y+.6,A.z-4.8+.85)
 if t<23:
  hands={sg:(sg*.63,-.60,cp.z+.34-baker.location.z) for sg in [-1,1]};pose_person(baker,t,hands=hands)
 else:pose_person(baker,t)
 porter=O['Station porter'];porter.location=(cp.x,cp.y+.6,B.z-4.8+.85) if 50<=t<56.8 else (8,1.6,B.z-4.8+.85) if t<50 else (10.5,3.6,B.z-4.8+.85)
 if 49.8<=t<56.8:
  hands={sg:(sg*.63,-.60,cp.z+.34-porter.location.z) for sg in [-1,1]};pose_person(porter,t,phase=(t-52)*5,walk=.18 if 52<t<55 else 0,hands=hands)
 elif 48<t<49.8:
  # Right palm tracks the near lid edge as the hinged lid rises.
  ang=O['Basket lid hinge'].rotation_euler.y;edge=Vector((-1.06+.35*math.cos(ang),.50,-.35*math.sin(ang)+1.13))+bp
  local=edge-porter.location;pose_person(porter,t,hands={-1:tuple(local),1:(.30,-.08,.8)})
 else:pose_person(porter,t)
 for nm in json.loads(S['residents']):
  ob=O[nm];bt=math.floor(t*12)/12;phase=ob['phase'];base=Vector(ob['base']);axis=Vector((*ob['axis'],0));motion=math.sin(bt*.16+phase)*ob['span'];p=base+axis*motion;p.z=ground(p.x,p.y)+.17;ob.location=p
  ob.rotation_euler.z=-math.atan2(axis.x,axis.y)+(0 if math.cos(bt*.16+phase)<0 else math.pi);pose_person(ob,t,bt*3.8+phase,.45)
 # Wheels are distance-driven. Horse legs continuous at output fps.
 distance=10+t*.48;p,yaw=road_at(distance);O['Green carriage'].location=p;O['Green carriage'].rotation_euler.z=yaw
 for o in O:
  if o.name.startswith('Carriage wheel '):o.rotation_euler.x=-distance/.59
 for sg in [-1,1]:
  for yy in [-.55,.55]:
   phase=distance*4.8+(0 if (sg==-1)==(yy<0) else math.pi);O['Horse leg %d %.2f'%(sg,yy)].rotation_euler.x=.34*math.sin(phase)
 pose_person(O['Coachman'],t,hands={-1:(-.19,-.32,1.2),1:(.19,-.32,1.2)})
 for sg in [-1,1]:O['Coachman leg '+str(sg)].rotation_euler.x=-.85
 O['Working water wheel'].rotation_euler.y=t*.25
 # Hammer meets bell rim at the event. Bird wings unfold about physical pins.
 hammer=-.5
 for hit in [62,64,66]:
  if hit-.6<t<hit+.5:hammer=-.5*(1-ramp(t,hit-.6,hit)) if t<hit else -.5*ramp(t,hit,hit+.5)
 O['Bell hammer pivot'].rotation_euler.y=hammer
 wing=ramp(t,62,63.4)*(1-ramp(t,66.5,68))
 for sg in [-1,1]:O['Bird wing '+str(sg)].rotation_euler.y=-sg*1.0*wing
 for nm in json.loads(S['smokes']):
  o=O[nm];j=o['puff'];ph=(t*.18+j*.8)%4;sc=.12+ph*.12;o.location=(ph*.30,ph*.09,ph*.7);o.scale=(sc,sc*.8,sc*1.3)
 for j,nm in enumerate(json.loads(S['steam'])):
  o=O[nm];u=((t-57)*.6+j*.32)%1.7;scale=(.045+.05*u)*ramp(t,57,58)*(1-ramp(t,69,74));o.location=cp+Vector(((j-2)*.14+u*.13,-.1+u*.03,.6+u*.43));o.scale=(scale,scale,scale*1.6)
 pos,target,lens=pose(t);cam=S.camera;cam.location=pos;cam.rotation_euler=(target-pos).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
 bpy.context.view_layer.update()
 if S.use_nodes:
  nt=S.node_tree
  if nt.nodes.get('Focus reciprocal'):nt.nodes['Focus reciprocal'].outputs[0].default_value=1/(target-pos).length
  if nt.nodes.get('Tilt strength'):nt.nodes['Tilt strength'].outputs[0].default_value=.7*ramp(t,0,4)
  if nt.nodes.get('Focus band image'):nt.nodes['Focus band image'].image=bpy.data.images['Wide focus band' if 43<=t<69 else 'Narrow focus band']
 return {'t':t,'camera':list(pos),'target':list(target),'basket':list(bp),'crate':list(cp),'carrier_u':basket_u(t),'carriage_distance':distance,'lens':lens}
