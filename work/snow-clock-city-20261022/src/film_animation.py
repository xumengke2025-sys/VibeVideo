"""Absolute-time choreography for the one persistent bread delivery."""
import bpy,math,json
from mathutils import Vector,Matrix
import alpine_environment as E
import carriage_assets as V
import freight_assets as F
S=bpy.context.scene;O=bpy.data.objects
A=Vector(S['upper_station']);B=Vector(S['lower_station']);CA=Vector(S['cable_A']);CB=Vector(S['cable_B'])
road=[Vector(p) for p in json.loads(S['road'])];distances=[0]
for a,b in zip(road,road[1:]):distances.append(distances[-1]+(b-a).length)
carriage=V.deserialize_data(json.loads(S['carriage_data'])) if hasattr(V,'deserialize_data') else None
def sm(x):x=max(0,min(1,x));return x*x*(3-2*x)
def ramp(t,a,b):return sm((t-a)/(b-a))
def cable(u):
    p=CA.lerp(CB,u);p.z-=.65*4*u*(1-u);return p
def progress(t):
    if t<26:return 0
    if t<46:return sm((t-26)/20)
    if t<76:return 1
    return 1-.8*sm((t-76)/14)
def carrier_position(t):return cable(progress(t))-Vector((0,0,2.42))
def crate_position(t):
    initial=A+Vector((1.7,-.12,1.35));inside=carrier_position(t)+Vector((0,0,.08))
    if t<20:return initial
    if t<21:return initial.lerp(A+Vector((1.7,-.12,2.10)),ramp(t,20,21))
    if t<22.5:return (A+Vector((1.7,-.12,2.10))).lerp(A+Vector((0,0,2.10)),ramp(t,21,22.5))
    if t<23.5:return (A+Vector((0,0,2.10))).lerp(inside,ramp(t,22.5,23.5))
    if t<50:return inside
    if t<52:return inside.lerp(B+Vector((0,0,2.10)),ramp(t,50,52))
    if t<55:return (B+Vector((0,0,2.10))).lerp(B+Vector((1.70,-.12,2.10)),ramp(t,52,55))
    return (B+Vector((1.70,-.12,2.10))).lerp(B+Vector((1.70,-.12,1.35)),ramp(t,55,56))

def child(root,suffix):return next(o for o in root.children_recursive if o.name.endswith(suffix))
def person_pose(root,t,walking=0,phase=0,hands=None,crouch=0):
    rig=next(o for o in root.children if o.type=='ARMATURE')
    rig.pose.bones['root'].location=rig.data.bones['root'].matrix_local.to_3x3().inverted()@Vector((0,0,-crouch))
    for side,sign in [('L',1),('R',-1)]:
        pb=rig.pose.bones.get('upperleg01.'+side)
        if pb:pb.rotation_mode='XYZ';pb.rotation_euler.x=walking*.23*math.sin(phase+(0 if sign==1 else math.pi))
        lower=rig.pose.bones.get('lowerleg01.'+side)
        if lower:lower.rotation_mode='XYZ';lower.rotation_euler.x=-walking*.25*max(0,math.sin(phase+(0 if sign==1 else math.pi)))
        target=child(root,'hand target '+side)
        if hands:target.location=root.matrix_world.inverted()@Vector(hands[side])
        else:target.location=(sign*.24,-.16+.055*walking*math.sin(phase+(0 if sign==1 else math.pi)),1.01)

def grip_hands(root,cp):
    # These are actual palm/finger-base contacts on the wooden side grips.
    return {side:cp+Vector((-sign*.51,-.12,.23)) for side,sign in [('L',1),('R',-1)]}

def worker_position(name,t):
    station=A if name=='Baker' else B;cp=crate_position(t)
    offset=.47-.05*ramp(cp.z-station.z,1.7,2.1)
    carry=Vector((cp.x,cp.y-offset,station.z+.65))
    if name=='Baker':
        idle=A+Vector((1.7,-.85,.65))
        if t<20:return idle.lerp(carry,ramp(t,19.4,20))
        if t<23.5:return carry
        end=A+Vector((0,-.47,.65))
        if t<24:return end
        return end.lerp(idle,ramp(t,24,26))
    idle=B+Vector((0,-.70,.65));end=B+Vector((1.7,-.59,.65))
    if t<50:return idle.lerp(carry,ramp(t,49.3,50))
    if t<56:return carry
    return end.lerp(B+Vector((1.7,-.85,.65)),ramp(t,57,58))

def worker_feet(root,name,t):
    """Plant each ankle during stance, then swing to the next landing."""
    rig=next(o for o in root.children if o.type=='ARMATURE');period=.24
    for side,phase in [('L',0),('R',.5)]:
        cycle=math.floor(t/period+phase);start=(cycle-phase)*period;u=(t-start)/period
        offset=root.matrix_world.to_3x3()@rig.data.bones['foot.'+side].head_local
        p=worker_position(name,start)+offset;q=worker_position(name,start+period)+offset
        if u<=.52:point=p
        else:
            v=(u-.52)/.48;point=p.lerp(q,sm(v))
            point.z+=.045*math.sin(math.pi*sm(v))*min(1,(q-p).length/.04)
        child(root,'foot target '+side).location=root.matrix_world.inverted()@point

def worker_pose(root,name,t,cp,bp):
    station=A if name=='Baker' else B
    acquire,release=(ramp(t,19.4,20),1-ramp(t,23.5,24)) if name=='Baker' else (ramp(t,49.5,50),1-ramp(t,56,56.7))
    holding=acquire*release
    height=cp.z-station.z
    crouch=.05+holding*.25*(1-ramp(height,1.35,2.10))
    root.location=worker_position(name,t);root.rotation_euler.z=math.pi;bpy.context.view_layer.update()
    hands={side:root.matrix_world@Vector((sign*.24,-.16,1.01)) for side,sign in [('L',1),('R',-1)]}
    grip=grip_hands(root,cp)
    for side in hands:hands[side]=hands[side].lerp(grip[side],holding)
    if name=='Porter':
        # The worker pulls the actual brass latch, then releases; a retained
        # torsion hinge takes over the final opening beyond arm's reach.
        lid_weight=ramp(t,47.6,48)*(1-ramp(t,48.30,48.60))
        latch=O['Freight lid hinge'].matrix_world@Vector((0,-.91,.02))
        hands['L']=hands['L'].lerp(latch,lid_weight)
        # Open the bread box by its front edge after it rests on the table.
        bread_weight=ramp(t,56.5,57)*(1-ramp(t,57.20,57.50))
        edge=O['Bread crate lid'].matrix_world@Vector((-.26,-.60,.025))
        hands['L']=hands['L'].lerp(edge,bread_weight)
    worker_feet(root,name,t)
    person_pose(root,t,0,0,hands,crouch)

def road_at(distance):
    d=max(0,min(distances[-1]-.001,distance));i=next(i for i in range(len(distances)-1) if distances[i]<=d<distances[i+1]);u=(d-distances[i])/(distances[i+1]-distances[i]);p=road[i].lerp(road[i+1],u)
    tangent=road[min(len(road)-1,i+2)]-road[max(0,i-1)]
    return p,math.atan2(tangent.x,-tangent.y),math.atan2(tangent.z,math.hypot(tangent.x,tangent.y))

def camera_pose(t):
    p0=carrier_position(27);p1=carrier_position(43)
    keys=[
      (0,(53,-84,12),(0,15,14),48),(12,(51,-70,72),(0,15,10),48),
      (17,(10,-5,34),(-10,20,11),51),(23,tuple(A+Vector((10,-15,15))),tuple(A+Vector((.3,0,1.8))),58),
      (27,tuple(p0+Vector((12,-17,15))),tuple(p0+Vector((0,0,1))),57),
      (43,tuple(p1+Vector((11,-14,12))),tuple(p1+Vector((0,0,1))),58),
      (47,(16,-8.5,15.8),(8.7,2.6,B.z+1.8),59),
      (59,(16,-8.5,15.8),(8.7,2.6,B.z+1.8),59),
      (62,(4,-6,21),(-2,6.6,16.6),65),(68,(4,-6,21),(-2,6.6,16.6),65),
      (74,(26,-34,36),(1,5,7),50),(86,(58,-89,89),(0,7,10),46),
      (90,(60,-92,92),(0,7,10),46)]
    for a,b in zip(keys,keys[1:]):
        if a[0]<=t<=b[0]:
            u=sm((t-a[0])/(b[0]-a[0]));return Vector(a[1]).lerp(Vector(b[1]),u),Vector(a[2]).lerp(Vector(b[2]),u),a[3]+(b[3]-a[3])*u
    return Vector(keys[-1][1]),Vector(keys[-1][2]),keys[-1][3]

def at(t):
    u=progress(t);bp=carrier_position(t);basket=O['Bread cable basket'];basket.location=bp
    # Keep the running rollers on the bearing line. A restrained swing acts
    # about the cable contact instead of translating the whole trolley off it.
    basket.rotation_euler=(0,0,0)
    trolley=O['Carrier trolley'];trolley.rotation_euler.z=F.CABLE_HEADING
    grade=(CB.z-CA.z-.65*4*(1-2*u))/math.hypot(CB.x-CA.x,CB.y-CA.y)
    trolley.rotation_euler.x=math.atan(grade)
    for name in ['Carrier roller front','Carrier roller rear']:
        O[name].rotation_euler.x=-u*(CA-CB).length/.080
    opening=(1-ramp(t,24,25)) if t<26 else ramp(t,48,49.5)*(1-ramp(t,72,73.5))
    O['Freight lid hinge'].rotation_euler.x=-1.48*opening
    gate_open=(1-ramp(t,24,25)) if t<26 else ramp(t,47.6,49.3)*(1-ramp(t,71.8,73.5))
    for sign in [-1,1]:
        gate=O.get('Freight loading gate '+str(sign))
        if gate:gate.rotation_euler.z=sign*1.60*gate_open
    cp=crate_position(t);O['One persistent bread crate'].location=cp
    O['Bread crate lid'].rotation_euler.x=-1.60*ramp(t,57,58)
    for name,lock in [('Hill freight station',1-ramp(t,25,26)),('Square freight station',ramp(t,46.5,47.5)*(1-ramp(t,74,75)))]:
        for sg in [-1,1]:O[name+' clamp '+str(sg)].location.x=sg*(.85-.16*lock)
        O[name+' sheave'].rotation_euler.x=-u*(CA-CB).length/.58
    # Fixed raised work treads support the workers while knee/ankle IK
    # changes their carrying height; all acquire/release paths are continuous.
    for name in ['Baker','Porter']:
        worker_pose(O[name],name,t,cp,bp)
    for name in json.loads(S['residents']):
        ob=O[name];bt=math.floor(t*12)/12;phase=ob['phase'];base=Vector((*ob['base'],0));axis=Vector((*ob['axis'],0));wave=math.sin(bt*.14+phase);p=base+axis*(wave*ob['span']);p.z=E.ground(p.x,p.y)+.22;ob.location=p
        direction=axis*(1 if math.cos(bt*.14+phase)>0 else -1);ob.rotation_euler.z=math.atan2(direction.x,-direction.y)
        person_pose(ob,t,.75,bt*3.6+phase)
    if carriage:
        d=8+t*.48;p,yaw,pitch=road_at(d);carriage['root'].location=p;carriage['root'].rotation_euler=( -pitch,0,yaw);V.pose_at(carriage,t,d,.48)
    O['Working waterwheel'].rotation_euler.x=t*.32
    parts=json.loads(S['tower_parts']);hit=1
    for when in [62,64,66]:
        if when-.5<t<when:hit=min(hit,1-ramp(t,when-.5,when))
        elif when<=t<when+.7:hit=min(hit,ramp(t,when,when+.7))
    O[parts['hammer']].rotation_euler.y=.32*hit
    wing=ramp(t,62,63.4)*(1-ramp(t,66.8,68.2))
    O[parts['wing_left']].rotation_euler.y=-1.05*(1-wing);O[parts['wing_right']].rotation_euler.y=1.05*(1-wing)
    for name in json.loads(S['smoke']):
        for ob in O[name].children:
            j=ob['puff_index'];phase=(t*.12+j/6)%1;ob.location=(phase*1.65,phase*.45,phase*3.5);radius=.12+phase*.5;ob.scale=(radius*.72,radius*.72,radius*1.35)
            ob.color=(1,1,1,sm(phase/.12)*(1-sm((phase-.65)/.35)))
    steam=O.get('Fresh bread steam')
    if steam:
        steam.location=cp+Vector((0,0,.40))
        for ob in steam.children:
            phase=((t-57)*.25+ob['puff_index']/6)%1
            ob.location=(phase*.16,phase*.05,phase*.55);radius=.025+.06*phase;ob.scale=(radius,radius,radius*1.8)
            envelope=ramp(t,57,58)*(1-ramp(t,63,66))
            ob.color=(1,1,1,.40*envelope*sm(phase/.12)*(1-sm((phase-.65)/.35)))
    cam,target,lens=camera_pose(t);S.camera.location=cam;S.camera.rotation_euler=(target-cam).to_track_quat('-Z','Y').to_euler();S.camera.data.lens=lens
    if S.use_nodes:
        n=S.node_tree.nodes
        if n.get('Focus reciprocal'):n['Focus reciprocal'].outputs[0].default_value=1/(target-cam).length
        if n.get('Tilt strength'):n['Tilt strength'].outputs[0].default_value=(.66-.30*ramp(t,74,86))*ramp(t,0,3)
        if n.get('Focus band image'):n['Focus band image'].image=bpy.data.images['Wide focus band' if 43<t<69 else 'Narrow focus band']
    bpy.context.view_layer.update()
    return {'seconds':t,'carrier':list(bp),'crate':list(cp),'camera':list(cam),'focus':list(target),'cable_u':u}
