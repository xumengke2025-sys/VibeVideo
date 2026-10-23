"""Eighteenth century Alpine carriage.  Z up, -Y forward, metres.

The assembly origin is the rear axle ground projection.  Source animal anatomy
is the CC0 Lyndon Daniels / ChadM horse.  Geometry, harness and coach are new.
"""
import bpy, math, json, sys, random
from pathlib import Path
from mathutils import Vector, Matrix, Quaternion
sys.path.insert(0,str(Path(__file__).resolve().parent))
import craft as C
import actors
R=Path(__file__).resolve().parents[1]
OUT=R/'render/carriage-assets'

def tube(name,pts,r,mat,parent):
    """Smooth sampled three dimensional joinery/forged iron curve."""
    return C.curve(name,pts,r,mat,parent)

def arcpts(a,b,c,n=28):
    a,b,c=Vector(a),Vector(b),Vector(c)
    return [(1-t)**2*a+2*t*(1-t)*b+t*t*c for t in [i/n for i in range(n+1)]]

def side_panel(m,x,points,thick,mat):
    n=len(points);v=[(x+dx,y,z) for dx in [-thick/2,thick/2] for y,z in points]
    m.add(v,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat)

def wheel(parent,name,x,y,r):
    hub=C.root(name,(x,y,r),parent);m=C.Mesh();rot=Matrix.Rotation(math.pi/2,3,'Y')
    # Axle orientation is local X. Felloe is wooden, tire is iron, no rubber.
    m.torus((0,0,0),r-.041,.037,C.DK,rot,96)
    for xx in [-.025,.025]:m.torus((xx,0,0),r-.009,.014,C.IR,rot,96)
    for i in range(12):
        a=i*math.tau/12;ay=.11*math.sin(a);az=.11*math.cos(a);by=(r-.06)*math.sin(a);bz=(r-.06)*math.cos(a)
        m.beam((0,ay,az),(0,by,bz),.032,.034,C.WO)
        m.rod((-.049,(r-.055)*math.sin(a),(r-.055)*math.cos(a)),(.049,(r-.055)*math.sin(a),(r-.055)*math.cos(a)),.011,C.BR,8)
    m.rod((-.095,0,0),(.095,0,0),.092,C.DK,36)
    m.rod((-.105,0,0),(.105,0,0),.058,C.BR,32)
    m.torus((.101 if x>0 else -.101,0,0),.063,.009,C.IR,rot,40)
    m.obj(name+' | mortised spokes, felloe, wrought tire',hub,.003)
    return {'object':hub,'radius':r}

def build_horse(parent,position=(0,-3.85,0)):
    horse=actors.horse('Chestnut draught mare',position);horse.parent=parent
    rig=next(o for o in horse.children_recursive if o.type=='ARMATURE')
    body=next(o for o in horse.children_recursive if o.type=='MESH' and 'Plane' in o.name)
    source=rig.parent;sourcebase=source.location.copy()
    for pb in rig.pose.bones:
        for c in list(pb.constraints):pb.constraints.remove(c)
        pb.matrix_basis=Matrix.Identity(4)
    bpy.context.view_layer.update()
    # Separate deform bones at the existing hoof endpoints keep the solid hoof
    # horizontal during stance instead of bending it with the lower leg.
    names=[('front_left','Bone_L.002',0),('front_right','Bone_R.002',.50),('hind_left','Bone_R.005',.75),('hind_right','Bone_L.005',.25)]
    rest={label:(rig.data.bones[b].tail_local.copy(),rig.matrix_world@rig.data.bones[b].tail_local) for label,b,phase in names}
    bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
    for label,b,phase in names:
        q=rig.data.edit_bones.new('hoof_'+label);q.head=rest[label][0];q.tail=q.head+Vector((0,-.7,0));q.parent=rig.data.edit_bones[b];q.use_connect=False
    bpy.ops.object.mode_set(mode='OBJECT');rig.select_set(False)
    targets=[];foot_indices={}
    for label,b,phase in names:
        local=horse.matrix_world.inverted()@rest[label][1]
        target=C.root('Hoof target | '+label,local,horse)
        ik=rig.pose.bones[b].constraints.new('IK');ik.target=target;ik.chain_count=2;ik.use_tail=True;ik.iterations=120;ik.use_stretch=False
        pole=C.root('Hock pole | '+label,(local.x,local.y+(-1 if 'front' in label else 1),.6),horse)
        # Natural bend direction is retained from source rest pose. No pole is
        # needed; a weak preferred bend avoids branch flips around full extension.
        rig.pose.bones[b].ik_stretch=0
        rig.pose.bones[b].parent.ik_stretch=0
        vg=body.vertex_groups.new(name='hoof_'+label);selected=[]
        for v in body.data.vertices:
            q=horse.matrix_world.inverted()@(body.matrix_world@v.co)
            if abs(q.x-local.x)<.19 and abs(q.y-local.y)<.27 and q.z<.22:
                w=min(1,max(0,(.22-q.z)/.08))
                if w<=0:continue
                old=[(g.group,g.weight) for g in v.groups]
                for group,weight in old:body.vertex_groups[group].add([v.index],weight*(1-w),'REPLACE')
                vg.add([v.index],w,'REPLACE')
                if w>.99:selected.append(v.index)
        foot_indices[label]=selected
        sole_offset=min((horse.matrix_world.inverted()@(body.matrix_world@body.data.vertices[i].co)).z for i in selected)
        targets.append({'label':label,'bone':b,'hoof':'hoof_'+label,'target':target,'rest':local.copy(),'phase':phase,'sole_offset':sole_offset,'rest_rot':rig.data.bones['hoof_'+label].matrix_local.to_3x3().copy()})
    # A genuine small-scale hair shader, with dark socks and a soft satin coat.
    coat=body.data.materials[0];n=coat.node_tree.nodes;l=coat.node_tree.links;p=n.get('Principled BSDF')
    p.inputs['Roughness'].default_value=.55;p.inputs['Coat Weight'].default_value=.15;p.inputs['Coat Roughness'].default_value=.35
    tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=105;tex.inputs['Detail'].default_value=2
    bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.008
    l.new(tex.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
    body.data.materials.append(C.M[C.LE])
    for poly in body.data.polygons:
        q=horse.matrix_world.inverted()@(body.matrix_world@poly.center)
        if q.z<.13:poly.material_index=1
    return {'root':horse,'rig':rig,'body':body,'source':source,'sourcebase':sourcebase,'feet':targets,'foot_indices':foot_indices}

def make_harness(parent):
    # All positions are local to the mare, whose body is 1.96 m high. Curves
    # follow the actual source anatomy and stay outside the coat surface.
    m=C.Mesh();le=C.LE;br=C.BR
    # Padded collar: broad oval in the angled plane at base of the neck.
    pts=[]
    for i in range(65):
        a=i*math.tau/64;pts.append((.335*math.cos(a)-.02,-.54-.16*math.sin(a),1.20+.44*math.sin(a)))
    tube('Padded full draught collar',pts,.048,le,parent)
    tube('Brass bound collar hames',[(x*1.09,y-.025,z) for x,y,z in pts],.017,br,parent)
    # Saddle girth around the chest, belly and back. Curved straps are geometry.
    pts=[(.33*math.cos(a)-.02,-.05,1.13+.38*math.sin(a)) for a in [i*math.tau/64 for i in range(65)]]
    tube('Chest girth and belly strap',pts,.022,le,parent)
    pts=[(.34*math.cos(a)-.02,.48,1.13+.37*math.sin(a)) for a in [i*math.tau/64 for i in range(65)]]
    tube('Breeching strap',pts,.025,le,parent)
    tube('Back strap',[(0,-.4,1.56),(0,-.05,1.55),(0,.4,1.54),(0,.75,1.45)],.021,le,parent)
    # Poll / cheek / nose straps; small brass bit rings at the lips.
    for sign in [-1,1]:
        tube('Cheekpiece',[(sign*.115,-1.38,1.86),(sign*.14,-1.47,1.65),(sign*.14,-1.60,1.39)],.014,le,parent)
        tube('Throat latch',[(sign*.12,-1.39,1.82),(sign*.16,-1.31,1.61),(0,-1.37,1.54)],.012,le,parent)
        m.torus((sign*.15,-1.61,1.39),.036,.008,br,Matrix.Rotation(math.pi/2,3,'Y'),24)
        m.torus((sign*.355,-.05,1.23),.043,.009,br,Matrix.Rotation(math.pi/2,3,'Y'),24)
        m.box((sign*.345,-.05,1.27),(.035,.08,.065),br)
        tube('Leather shaft tug',[(sign*.34,-.05,1.31),(sign*.48,-.10,1.31),(sign*.535,-.10,1.25),(sign*.49,-.10,1.15),(sign*.40,-.05,1.18),(sign*.34,-.05,1.31)],.012,le,parent)
        tube('Trace from hame to swingletree',[(sign*.34,-.52,1.20),(sign*.48,-.06,1.14),(sign*.50,.5,1.06),(sign*.48,1.63,.85)],.019,le,parent)
    tube('Noseband',[(-.14,-1.62,1.40),(-.10,-1.69,1.38),(0,-1.72,1.36),(.10,-1.69,1.38),(.14,-1.62,1.40)],.017,le,parent)
    tube('Browband',[(-.12,-1.41,1.78),(0,-1.45,1.79),(.12,-1.41,1.78)],.013,le,parent)
    m.obj('Harness buckles and bit rings',parent,.003)

def build_driver(parent):
    driver=actors.human('Coachman',(0,-1.67,.77));driver.parent=parent
    rig=next(o for o in driver.children if o.type=='ARMATURE')
    # The original weighted skin and coat are retained, while knees are posed
    # and feet placed on the front footboard. Extra static shoes are replaced.
    for o in list(driver.children):
        if 'buttons and buckled shoes' in o.name or 'coat skirts' in o.name:
            bpy.data.objects.remove(o,do_unlink=True)
    targets=[o for o in driver.children if 'hand target' in o.name]
    for o in targets:o.location=(.18 if o.name.endswith('L') else -.18,-.44,1.13)
    # Use analytic two segment rotations, with both twist segments sharing the
    # thigh rotation and lower legs hanging vertically. This gives a stable
    # seated pose without IK moving the pelvis off the bench.
    for side in ['L','R']:
        pb=rig.pose.bones['upperleg01.'+side];pb.rotation_mode='QUATERNION'
        local_axis=pb.bone.matrix_local.to_3x3().inverted()@Vector((1,0,0))
        pb.rotation_quaternion=Quaternion(local_axis,-math.pi/2+.08)
        pb=rig.pose.bones['lowerleg01.'+side];pb.rotation_mode='QUATERNION'
        local_axis=pb.bone.matrix_local.to_3x3().inverted()@Vector((1,0,0))
        pb.rotation_quaternion=Quaternion(local_axis,math.pi/2-.04)
    # Sculpted coat tail over the edge of the bench, naturally hiding the seat.
    m=C.Mesh();m.box((0,.05,.91),(.47,.35,.08),C.BL)
    for s in [-1,1]:
        m.box((s*.14,-.19,.84),(.22,.36,.06),C.BL)
    m.obj('Coachman | seated coat tails',driver,.025)
    bpy.context.view_layer.update()
    # Mount each shoe on the posed foot transform so the ankles remain joined.
    for side in ['L','R']:
        pb=rig.pose.bones['foot.'+side];p=pb.head
        shoe=C.Mesh();shoe.ellipsoid((p.x,p.y-.055,p.z-.025),(.07,.13,.052),C.LE,24,12)
        shoe.box((p.x,p.y-.13,p.z+.005),(.063,.024,.035),C.BR)
        shoe.obj('Coachman | posed buckle shoe '+side,driver,.002)
    return driver

def build_carriage(name='Alpine post carriage',position=(0,0,0),with_driver=True):
    """Return (root, animation) using metres, forward -Y, rear axle at origin.

    Call pose_at(animation,t,distance,speed) after placing/orienting root on road.
    distance is cumulative travelled metres; it controls wheels and hoof phase.
    Do not additionally rotate wheels or translate the horse independently.
    """
    if not C.M:C.palette()
    root=C.root(name,position);body=C.root('Sprung coach body',(0,0,0),root)
    green=C.material('Coach | deep forest green lacquer',(.018,.075,.049),.40)
    pinstripe=C.material('Coach | ochre pinstripe',(.55,.33,.095),.48)
    leather=C.material('Coach | black leather roof',(.024,.020,.017),.75)
    m=C.Mesh();ch=C.Mesh();details=C.Mesh()
    # Longitudinal frame; paired leaf springs make the body visibly suspended.
    for x in [-.53,.53]:
        ch.beam((x,.35,.67),(x,-1.92,.67),.085,.105,C.DK)
        for cy in [0,-1.65]:
            for layer in range(5):
                half=.49-layer*.04;pts=[(x,cy+half*(2*i/32-1),.69+.19*(1-(2*i/32-1)**2)+layer*.014) for i in range(33)]
                tube('Layered steel leaf spring',pts,.012,C.IR,root)
            for yy in [cy-.47,cy+.47]:ch.rod((x,yy,.67),(x,yy,.84),.023,C.IR,12)
            ch.box((x,cy,.77),(.13,.12,.16),C.IR)
    ch.rod((-.91,0,.58),(.91,0,.58),.043,C.IR,24)
    ch.rod((-.83,-1.65,.46),(.83,-1.65,.46),.041,C.IR,24)
    ch.rod((0,-1.65,.46),(0,-1.65,.76),.065,C.BR,24)
    # Swept wood tub with sloping ends, recessed door, beaded edges.
    profile=[(.51,.93),(.36,1.56),(.18,1.73),(-.87,1.73),(-1.17,1.48),(-1.30,1.01),(-1.08,.86),(.25,.86)]
    for s in [-1,1]:
        side_panel(m,s*.65,profile,.105,green)
        tube('Coach curved lower bead',[(s*.713,y,z+.055) for y,z in profile]+[(s*.713,profile[0][0],profile[0][1]+.055)],.017,C.BR,body)
        # Single carriage door between separate framed panes.
        side_panel(m,s*.715,[(-.74,.98),(-.74,1.64),(-.06,1.64),(-.06,.98)],.023,green)
        for yy in [-.74,-.06]:tube('Door stile',[(s*.732,yy,.99),(s*.732,yy,2.23)],.016,pinstripe,body)
        for z in [1.0,1.60,2.23]:tube('Door rail',[(s*.732,-.74,z),(s*.732,-.06,z)],.016,pinstripe,body)
        details.rod((s*.74,-.14,1.62),(s*.78,-.14,1.62),.026,C.BR,16)
        details.rod((s*.79,-.14,1.62),(s*.79,-.23,1.62),.012,C.BR,12)
        for yy in [-.69]:
            for zz in [1.15,1.46]:details.box((s*.74,yy,zz),(.026,.05,.065),C.BR)
        # Open glazing apertures: small posts, clear pane, tan curtain gathered.
        for yy in [-1.0,-.74,-.06,.27]:m.box((s*.65,yy,1.98),(.065,.065,.54),C.DK)
        for z in [1.72,2.24]:m.box((s*.65,-.37,z),(.075,1.40,.075),C.DK)
        for yy in [-.92,.18]:
            for k in range(4):m.rod((s*.63,yy+k*.026,1.76),(s*.63,yy+k*.026,2.21),.018,C.CL,10)
        # Side step and iron supports clearly clear the moving wheel envelope.
        details.box((s*.80,-.69,.62),(.29,.63,.065),C.DK,wood=True)
        for yy in [-.95,-.42]:details.beam((s*.57,yy,.84),(s*.81,yy,.64),.033,.036,C.IR)
        # Heraldic badge on the green panel is modest and period restrained.
        details.ellipsoid((s*.74,-.41,1.30),(.018,.13,.15),C.BR,24,14)
        details.ellipsoid((s*.759,-.41,1.30),(.008,.107,.125),green,24,14)
        for j in range(6):
            a=j*math.tau/6;details.ellipsoid((s*.771,-.41+.071*math.sin(a),1.30+.081*math.cos(a)),(.007,.013,.018),C.BR,12,8)
    m.box((0,.39,1.27),(1.24,.11,.73),green);m.box((0,-1.16,1.28),(1.24,.10,.63),green)
    m.box((0,-.36,.94),(1.22,1.56,.10),C.DK,wood=True)
    # Upholstered facing seats within the apertures.
    for yy in [.14,-.91]:
        m.box((0,yy,1.15),(1.13,.32,.13),leather)
        m.box((0,yy+(.14 if yy>0 else -.14),1.44),(1.12,.08,.49),leather)
        for x in [-.41,-.21,0,.21,.41]:details.ellipsoid((x,yy+(-.075 if yy>0 else .075),1.45),(.012,.007,.012),C.BR,10,6)
    # Curved leather roof over bent ribs; geometry remains open at windows.
    roof=C.Mesh();nx=24;ny=20;v=[]
    for j in range(ny+1):
        y=-1.18+j*1.65/ny
        for i in range(nx+1):
            x=-.76+i*1.52/nx;v.append((x,y,2.29+.16*(1-(x/.78)**2)+.025*math.sin((y+1.18)*math.pi/1.65)))
    roof.add(v,[(j*(nx+1)+i,j*(nx+1)+i+1,(j+1)*(nx+1)+i+1,(j+1)*(nx+1)+i) for j in range(ny) for i in range(nx)],leather,smooth=True)
    ro=roof.obj('Hand sewn leather canopy',body,0);ro.modifiers.new('Leather thickness','SOLIDIFY').thickness=.033
    for yy in [-1.18,.47]:tube('Canopy rolled piping',[(-.76+i*1.52/48,yy,2.29+.16*(1-((-.76+i*1.52/48)/.78)**2)) for i in range(49)],.018,C.BR,body)
    # Driver sits above the front axle. Bench cushion touches the posed pelvis.
    m.box((0,-1.58,1.65),(1.17,.50,.12),leather)
    m.box((0,-1.33,1.84),(1.17,.08,.39),leather)
    for s in [-1,1]:
        m.beam((s*.50,-1.54,.79),(s*.50,-1.54,1.60),.08,.08,C.DK)
        tube('Driver bench rail',[(s*.57,-1.88,1.72),(s*.57,-1.92,1.93),(s*.57,-1.35,1.97)],.023,C.BR,body)
    m.box((0,-2.11,1.03),(1.13,.43,.07),C.DK,wood=True)
    m.box((0,-2.28,1.17),(1.13,.06,.27),leather)
    for s in [-1,1]:
        details.beam((s*.46,-1.55,1.45),(s*.46,-2.12,1.0),.035,.04,C.IR)
        # Period candle lamps hang from forged brackets ahead of the body.
        details.beam((s*.60,-1.15,1.40),(s*.83,-1.15,1.75),.025,.025,C.IR)
        C.lantern((s*.84,-1.15,1.97),body)
    ch.obj('Timber chassis and kingpin',root,.007)
    m.obj('Coach | joinery, green curved body and leather seats',body,.014)
    details.obj('Coach | brass fittings and footboards',body,.004)
    wheels=[wheel(root,'Rear wheel '+str(s),s*.87,0,.58) for s in [-1,1]]+[wheel(root,'Front wheel '+str(s),s*.81,-1.65,.46) for s in [-1,1]]
    # Curved shafts connect the front pivot to leather shaft tugs, with no
    # rigid pole through the animal. A swingletree carries the pair of traces.
    for s in [-1,1]:
        pts=arcpts((s*.55,-1.61,.73),(s*.75,-2.40,.95),(s*.49,-3.95,1.22),48)
        tube('Bent ash shaft '+str(s),pts,.038,C.WO,root)
        for y in [-2.1,-2.5]:
            q=pts[min(range(len(pts)),key=lambda i:abs(pts[i].y-y))]
            hoop=C.Mesh();hoop.torus(q,.042,.007,C.IR,Matrix.Rotation(math.pi/2,3,'X'),24);hoop.obj('Shaft binding',root,.002)
    tr=C.Mesh();tr.rod((-.49,-2.22,.85),(.49,-2.22,.85),.037,C.WO,20);tr.rod((0,-2.22,.77),(0,-2.22,.94),.024,C.IR,16);tr.obj('Pivoted wooden swingletree',root,.003)
    horse=build_horse(root);make_harness(horse['root'])
    driver=build_driver(body) if with_driver else None
    reins=[];hands=[]
    bpy.context.view_layer.update()
    if driver:
        drig=next(o for o in driver.children if o.type=='ARMATURE')
        for side in ['R','L']:
            pb=drig.pose.bones['finger2-1.'+side]
            hands.append(root.matrix_world.inverted()@(drig.matrix_world@((pb.head+pb.tail)*.5)))
    for s in [-1,1]:
        start=hands[0 if s<0 else 1] if hands else (s*.18,-2.11,1.90)
        pts=[start,(s*.23,-2.65,1.74),(s*.38,-3.7,1.62),(s*.38,-4.50,1.56),(s*.15,-5.46,1.39)]
        reins.append(tube('Continuous leather rein '+str(s),pts,.008,C.LE,root))
    data={'root':root,'body':body,'wheels':wheels,'horse':horse,'driver':driver,'reins':reins,'stride':.64,'duty':.68,'speed':.5}
    root['origin']='Ground projection below rear axle';root['forward']='-Y';root['dimensions_m']='Width 1.95 / total length 6.2 / height 2.5'
    root['animation']='carriage_assets.pose_at(animation, t_seconds, distance_metres, speed_m_s)'
    pose_at(data,0,0,0)
    return root,data

def _hermite(a,b,ma,mb,u):
    return (2*u**3-3*u*u+1)*a+(u**3-2*u*u+u)*ma+(-2*u**3+3*u*u)*b+(u**3-u*u)*mb

def serialize_data(data):
    """JSON-safe animation state for a saved .blend, using exact object names.

    Store this result next to the blend or as a JSON scene custom property.
    It contains no executable code and does not duplicate the mesh data.
    """
    def encode(value):
        if isinstance(value,bpy.types.Object):return {'$object':value.name}
        if isinstance(value,Vector):return {'$vector':list(value)}
        if isinstance(value,Matrix):return {'$matrix':[list(row) for row in value]}
        if isinstance(value,Quaternion):return {'$quaternion':list(value)}
        if isinstance(value,dict):return {k:encode(v) for k,v in value.items()}
        if isinstance(value,(list,tuple)):return [encode(v) for v in value]
        if value is None or isinstance(value,(str,int,float,bool)):return value
        raise TypeError('Unsupported carriage animation state: '+type(value).__name__)
    return {'schema':'snow-clock-city.carriage.v1','data':encode(data)}

def deserialize_data(payload):
    """Resolve serialize_data() after opening its matching .blend scene.

    Also accepts JSON text. Missing named objects raise KeyError so a stale
    manifest cannot silently animate the wrong assembly.
    """
    if isinstance(payload,str):payload=json.loads(payload)
    if payload.get('schema')!='snow-clock-city.carriage.v1':raise ValueError('Unsupported carriage state schema')
    def decode(value):
        if isinstance(value,dict):
            if '$object' in value:
                ob=bpy.data.objects.get(value['$object'])
                if ob is None:raise KeyError('Carriage object missing from scene: '+value['$object'])
                return ob
            if '$vector' in value:return Vector(value['$vector'])
            if '$matrix' in value:return Matrix(value['$matrix'])
            if '$quaternion' in value:return Quaternion(value['$quaternion'])
            return {k:decode(v) for k,v in value.items()}
        if isinstance(value,list):return [decode(v) for v in value]
        return value
    return decode(payload['data'])

def pose_at(data,t,distance,speed=.5):
    """Deterministic four-beat walk. Stance feet move backward at road speed.

    Road translation/heading belong to caller. distance controls phase rather
    than wall time, so slowing the coach also slows the legs and every wheel.
    """
    for w in data['wheels']:w['object'].rotation_euler.x=distance/w['radius']
    horse=data['horse'];rig=horse['rig'];stride=data['stride'];duty=data['duty']
    horse['source'].location=horse['sourcebase']+Vector((0,0,-.075+.003*math.cos(distance/stride*math.tau*2)))
    for foot in horse['feet']:
        phase=(distance/stride+foot['phase'])%1
        p=foot['rest'].copy();p.z-=foot.get('sole_offset',.0057 if 'front' in foot['label'] else 0);lift=0;pitch=0
        if speed>.002:
            if phase<duty:
                y=-stride*duty/2+stride*phase
            else:
                u=(phase-duty)/(1-duty);y=_hermite(stride*duty/2,-stride*duty/2,stride*(1-duty),stride*(1-duty),u)
                lift=.105*math.sin(math.pi*u)**2;pitch=-.13*math.sin(math.pi*u)
            p.y+=y;p.z+=lift
        foot['target'].location=p
    bpy.context.view_layer.update()
    # Hoof rest axes are in rig coordinates; maintain level soles independently
    # of the cannon bone, with a small controlled toe pitch only during swing.
    for foot in horse['feet']:
        pb=rig.pose.bones[foot['hoof']];mat=foot['rest_rot'].to_4x4();mat.translation=rig.pose.bones[foot['bone']].tail
        pb.matrix=mat
    data['body'].location.z=.004*math.sin(distance*math.tau/.48) if speed>.002 else 0
    bpy.context.view_layer.update()
    return data

def inspect_source():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    C.palette();h=actors.horse('Reference horse');bpy.context.view_layer.update()
    rig=next(o for o in h.children_recursive if o.type=='ARMATURE')
    data={'objects':[], 'bones':[]}
    for o in h.children_recursive:
        if o.type=='MESH':
            data['objects'].append({'name':o.name,'bb':[list(o.matrix_world@Vector(q)) for q in o.bound_box]})
    for b in rig.pose.bones:
        data['bones'].append({'name':b.name,'head':list(rig.matrix_world@b.head),'tail':list(rig.matrix_world@b.tail),'constraints':[c.type for c in b.constraints]})
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'source-alignment.json').write_text(json.dumps(data,indent=2),encoding='utf8')
    bpy.ops.wm.save_as_mainfile(filepath=str(R/'model/carriage-reference.blend'))

def setup_preview():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    C.M.clear();C.palette();root,data=build_carriage()
    road=C.Mesh();rng=random.Random(410)
    for j in range(55):
        y=-7+j*.20
        for i in range(22):
            x=-3.7+i*.34+(j%2)*.17
            road.box((x,y,-.055+rng.uniform(-.004,.004)),(.327,.188,.10),C.ST,jitter=.007,seed=i+j*41)
    road.obj('Cleared wet stone paving',bevel=.014)
    C.drift('Snow bank left',(-7,-3.8),(-10,6),lambda x,y:.08+.08*math.sin(x*1.7+y*.7)**2,None,.25)
    C.drift('Snow bank right',(3.85,7),(-10,6),lambda x,y:.08+.08*math.sin(x*1.3+y*.9)**2,None,.25)
    for x in [-3.8,3.8]:
        for j in range(20):
            m=C.Mesh();m.box((x,-7+j*.56,.02),(.20,.54,.18),C.ST,jitter=.015,seed=j);m.obj('Road kerb',bevel=.012)
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
    try:
        prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
        for d in prefs.devices:d.use=d.type!='CPU'
        scene.cycles.device='GPU'
    except Exception:pass
    scene.world.color=(.16,.20,.26)
    world=bpy.data.worlds.new('Clear winter air');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.36,.47,.62,1);world.node_tree.nodes['Background'].inputs[1].default_value=.48;scene.world=world
    sun=bpy.data.lights.new('Low morning sun','SUN');sun.energy=2.6;sun.angle=.16;sun.color=(1,.79,.58)
    ob=bpy.data.objects.new('Low morning sun',sun);bpy.context.collection.objects.link(ob);ob.rotation_euler=(.50,-.6,-.4)
    area=bpy.data.lights.new('Sky fill','AREA');area.energy=420;area.shape='DISK';area.size=7;ob=bpy.data.objects.new('Sky fill',area);bpy.context.collection.objects.link(ob);ob.location=(3,-6,7)
    camera=bpy.data.cameras.new('Carriage portrait');cam=bpy.data.objects.new('Carriage portrait',camera);bpy.context.collection.objects.link(cam);cam.location=(7,-9.2,6.5)
    cam.rotation_euler=(Vector((0,-2.25,1.05))-cam.location).to_track_quat('-Z','Y').to_euler();camera.type='ORTHO';camera.ortho_scale=10.5;scene.camera=cam
    scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.render.resolution_percentage=100
    scene.render.fps=24;scene.frame_start=1;scene.frame_end=96
    scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast'
    return scene,root,data

def contact_report(data):
    root=data['root'];horse=data['horse'];body=horse['body'];rig=horse['rig'];records=[]
    sub=[m for m in body.modifiers if m.type=='SUBSURF']
    for m in sub:m.show_viewport=False
    for frame in range(96):
        distance=frame/24*.48;root.location.y=-distance;pose_at(data,frame/24,distance,.48)
        evalbody=body.evaluated_get(bpy.context.evaluated_depsgraph_get());vertices=evalbody.data.vertices
        item={'frame':frame,'distance':distance,'feet':{}}
        for f in horse['feet']:
            coords=[evalbody.matrix_world@vertices[i].co for i in horse['foot_indices'][f['label']]]
            actual=rig.matrix_world@rig.pose.bones[f['bone']].tail;target=f['target'].matrix_world.translation
            item['feet'][f['label']]={'stance':((distance/data['stride']+f['phase'])%1)<data['duty'],'ik_error_mm':(actual-target).length*1000,'sole_z_mm':min(v.z for v in coords)*1000,'target':list(target)}
        records.append(item)
    for m in sub:m.show_viewport=True
    summary={'frames':96,'duration_seconds':4,'fps':24,'speed_m_s':.48,'max_ik_error_mm':max(f['ik_error_mm'] for r in records for f in r['feet'].values()),'stance_sole_z_mm':[min(f['sole_z_mm'] for r in records for f in r['feet'].values() if f['stance']),max(f['sole_z_mm'] for r in records for f in r['feet'].values() if f['stance'])],'max_stance_target_displacement_mm':0,'records':records}
    for prev,nxt in zip(records,records[1:]):
        for label,a in prev['feet'].items():
            b=nxt['feet'][label]
            if a['stance'] and b['stance']:
                summary['max_stance_target_displacement_mm']=max(summary['max_stance_target_displacement_mm'],(Vector(a['target'])-Vector(b['target'])).length*1000)
    (OUT/'contact-report.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    root.location.y=0;pose_at(data,0,0,0)
    return summary

def verify_and_save():
    """No render: validate serializer and all 96 contact states, save asset."""
    OUT.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    C.M.clear();C.palette();root,data=build_carriage()
    payload=serialize_data(data);text=json.dumps(payload,ensure_ascii=False)
    restored=deserialize_data(text)
    assert restored['root'] is root
    assert restored['horse']['feet'][0]['target'] is data['horse']['feet'][0]['target']
    summary=contact_report(restored)
    bpy.context.scene['carriage_animation']=text
    (OUT/'carriage-animation.json').write_text(text,encoding='utf8')
    bpy.ops.wm.save_as_mainfile(filepath=str(R/'model/carriage-asset-only.blend'))
    # Reload the actual saved file to test the persistent-name protocol, then
    # evaluate one moving pose rather than merely checking JSON syntax.
    bpy.ops.wm.open_mainfile(filepath=str(R/'model/carriage-asset-only.blend'))
    restored=deserialize_data(bpy.context.scene['carriage_animation'])
    pose_at(restored,1.25,.6,.48)
    report={'serializer_roundtrip':'pass','saved_blend_reload':'pass','moving_pose_after_reload':'pass','contact_max_ik_error_mm':summary['max_ik_error_mm'],'contact_stance_sole_range_mm':summary['stance_sole_z_mm'],'stance_target_displacement_mm':summary['max_stance_target_displacement_mm']}
    (OUT/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    print(json.dumps(report))

def render_preview(args):
    OUT.mkdir(parents=True,exist_ok=True);scene,root,data=setup_preview()
    contact_report(data)
    if 'quick' in args:scene.render.resolution_percentage=50;scene.cycles.samples=24
    if 'walk' in args:
        scene.render.resolution_percentage=50;scene.cycles.samples=24
        for frame in range(96):
            scene.frame_set(frame+1);distance=frame/24*.48;root.location.y=.95-distance;pose_at(data,frame/24,distance,.48)
            scene.render.filepath=str(OUT/'walk'/('%04d.png'%frame));bpy.ops.render.render(write_still=True)
    else:
        for frame in [0,8,16,24]:
            pose_at(data,frame/24,frame/24*.48,.48 if frame else 0)
            scene.render.filepath=str(OUT/('proof-%02d.png'%frame));bpy.ops.render.render(write_still=True)
    # Restore canonical dimensions and resting pose in the editable asset.
    pose_at(data,0,0,0);scene.render.resolution_percentage=100
    bpy.ops.wm.save_as_mainfile(filepath=str(R/'model/carriage-alpine.blend'))

if __name__=='__main__':
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    if args and args[0]=='inspect':inspect_source()
    elif args and args[0]=='verify':verify_and_save()
    else:render_preview(args)
