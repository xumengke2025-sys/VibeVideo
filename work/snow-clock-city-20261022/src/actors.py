"""Source asset anatomy and newly authored eighteenth-century garments.
MakeHuman hm08 mesh + skeleton + weights are CC0; no MakeHuman code imported.
"""
import bpy,json,math
from pathlib import Path
from mathutils import Vector,Matrix
import craft as C
R=Path(__file__).resolve().parents[1]

def _bind_weights(ob,rig,vertex_weights):
    """Bind built garments in their original modelling coordinates."""
    groups={}
    for i,entries in enumerate(vertex_weights):
        for bone,weight in entries:
            if weight>0:
                if bone not in groups:groups[bone]=ob.vertex_groups.new(name=bone)
                groups[bone].add([i],weight,'REPLACE')
    mod=ob.modifiers.new('Accessory follows retained skeleton','ARMATURE');mod.object=rig
    bpy.context.view_layer.objects.active=ob
    while ob.modifiers.find(mod.name)>0:bpy.ops.object.modifier_move_up(modifier=mod.name)


def _bind_rigid(ob,rig,bone):
    _bind_weights(ob,rig,[[(bone,1)] for _ in ob.data.vertices])


def _bind_torso(ob,rig):
    levels=[(.90,'root'),(.97,'spine05'),(1.05,'spine04'),(1.14,'spine03'),(1.24,'spine02'),(1.40,'spine01')]
    weights=[]
    for v in ob.data.vertices:
        z=v.co.z
        if z<=levels[0][0]:entries=[(levels[0][1],1)]
        elif z>=levels[-1][0]:entries=[(levels[-1][1],1)]
        else:
            lo,hi=next((a,b) for a,b in zip(levels,levels[1:]) if a[0]<=z<=b[0]);u=(z-lo[0])/(hi[0]-lo[0]);entries=[(lo[1],1-u),(hi[1],u)]
        weights.append(entries)
    _bind_weights(ob,rig,weights)


def human(name,p=(0,0,0),baker=False):
    directory=R/'assets/models/makehuman';verts=[];faces=[];group='';uv=[];faceuv=[]
    for line in (directory/'base.obj').read_text().splitlines():
        a=line.split()
        if not a:continue
        if a[0]=='v':verts.append(Vector(tuple(map(float,a[1:4]))))
        elif a[0]=='vt':uv.append(tuple(map(float,a[1:3])))
        elif a[0]=='g':group=a[1]
        elif a[0]=='f' and group=='body':
            faces.append(tuple(int(q.split('/')[0])-1 for q in a[1:]));faceuv.append([uv[int(q.split('/')[1])-1] for q in a[1:]])
    used=set(i for f in faces for i in f);low=min(verts[i].y for i in used);high=max(verts[i].y for i in used);scale=1.73/(high-low)
    def convert(v):return Vector((v.x*scale,-v.z*scale,(v.y-low)*scale))
    coords=[convert(v) for v in verts]
    character=C.root(name,p)
    rigdata=json.loads((directory/'default.mhskel').read_text());weights=json.loads((directory/'default_weights.mhw').read_text())['weights']
    joints={key:sum((coords[i] for i in indices),Vector())/len(indices) for key,indices in rigdata['joints'].items()}
    arm=bpy.data.armatures.new(name+' skeleton');rig=bpy.data.objects.new(name+' rig',arm);bpy.context.collection.objects.link(rig);rig.parent=character
    bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
    for key,b in rigdata['bones'].items():
        bone=arm.edit_bones.new(key);bone.head=joints[b['head']];bone.tail=joints[b['tail']]
        if (bone.tail-bone.head).length<1e-5:bone.tail.z+=.001
    for key,b in rigdata['bones'].items():
        if b['parent']:arm.edit_bones[key].parent=arm.edit_bones[b['parent']]
    # A short palm bone solves both wrist direction and finger-base contact.
    for side in ['L','R']:
        grip=arm.edit_bones.new('grip.'+side)
        grip.head=arm.edit_bones['wrist.'+side].head
        grip.tail=arm.edit_bones['finger3-1.'+side].head
        grip.parent=arm.edit_bones['lowerarm02.'+side]
        arm.edit_bones['wrist.'+side].parent=grip
    bpy.ops.object.mode_set(mode='OBJECT');rig.select_set(False)
    # The body mesh remains anatomically continuous. Surfaces under opaque
    # garments use garment colours; neck, head and articulated hands use skin.
    m=C.Mesh();m.add(coords,faces,C.SK,faceuv,smooth=True)
    ob=m.obj(name+' | anatomical base',character,0)
    for poly in ob.data.polygons:
        co=sum((coords[i] for i in poly.vertices),Vector())/len(poly.vertices)
        if co.z<.12:poly.material_index=C.LE
        elif co.z<.52:poly.material_index=C.CL
        elif co.z<.91:poly.material_index=C.DK
        elif co.z<1.46 and abs(co.x)<.25:poly.material_index=C.BL
    for bone,entries in weights.items():
        vg=ob.vertex_groups.new(name=bone)
        for vi,w in entries:
            if vi<len(coords):vg.add([vi],w,'REPLACE')
    am=ob.modifiers.new('Deform by retained editable skeleton','ARMATURE');am.object=rig
    su=ob.modifiers.new('Skin smooth surface','SUBSURF');su.levels=1;su.render_levels=1
    # Clothing shells retain the source weights, with a deliberate loose fit.
    shells=[]
    for label,select,mat,inflate in [
        ('Wool coat and sleeves',lambda c:.87<c.z<1.46 and (abs(c.x)<.26 or c.z>1.08),C.BL,.019),
        ('Knee breeches',lambda c:.52<c.z<.97 and abs(c.x)<.25,C.DK,.018),
    ]:
        selected=[f for f in faces if all(select(coords[i]) for i in f)]
        ids=sorted(set(i for f in selected for i in f));index={old:new for new,old in enumerate(ids)}
        vv=[]
        for old in ids:
            v=coords[old].copy();normal=ob.data.vertices[old].normal
            v+=normal*inflate
            v+=normal*(.0035*math.sin(v.z*91+v.x*28)+.002*math.cos(v.y*77))
            vv.append(v)
        mm=C.Mesh();mm.add(vv,[tuple(index[i] for i in f) for f in selected],mat,smooth=True)
        cloth=mm.obj(name+' | '+label,character,0)
        for bone,entries in weights.items():
            entries=[(index[i],w) for i,w in entries if i in index]
            if entries:
                vg=cloth.vertex_groups.new(name=bone)
                for i,w in entries:vg.add([i],w,'REPLACE')
        mod=cloth.modifiers.new('Cloth follows body rig','ARMATURE');mod.object=rig
        mod=cloth.modifiers.new('Tailored surface','SUBSURF');mod.levels=1;mod.render_levels=1
        mod=cloth.modifiers.new('Fabric thickness','SOLIDIFY');mod.thickness=.006;shells.append(cloth)
    # Lower coat panels and a creased linen apron conceal anatomical contours.
    skirt=C.Mesh();v=[];nx=24;nz=12
    for j in range(nz+1):
        t=j/nz;z=.64+t*.55
        for i in range(nx+1):
            a=-math.pi+2*math.pi*i/nx;rx=.235-.065*t;ry=.14-.025*t
            v.append((rx*math.cos(a),ry*math.sin(a)+.008*math.sin(i*2+j*.3),z))
    skirt.add(v,[(j*(nx+1)+i,j*(nx+1)+i+1,(j+1)*(nx+1)+i+1,(j+1)*(nx+1)+i) for j in range(nz) for i in range(nx)],C.BL,smooth=True)
    so=skirt.obj(name+' | coat skirts',character,0);so.modifiers.new('Hem thickness','SOLIDIFY').thickness=.008
    _bind_torso(so,rig)
    if baker:
        ap=C.Mesh();v=[];nx=16;nz=18
        for j in range(nz+1):
            t=j/nz;z=.63+t*.67;w=.21 if t<.78 else .135
            for i in range(nx+1):
                u=i/nx*2-1;y=-.16-.012*math.cos(u*9)*(1-t)-.022*(1-t)
                v.append((u*w,y,z+.009*math.cos(u*5)*(1-t)))
        ap.add(v,[(j*(nx+1)+i,j*(nx+1)+i+1,(j+1)*(nx+1)+i+1,(j+1)*(nx+1)+i) for j in range(nz) for i in range(nx)],C.CL,smooth=True)
        apron=ap.obj(name+' | tied linen apron',character,0);apron.modifiers.new('Linen thickness','SOLIDIFY').thickness=.004
        _bind_torso(apron,rig)
        strap=C.Mesh();points=[(-.12,-.135,1.28),(-.08,-.09,1.43),(.08,-.09,1.43),(.12,-.135,1.28)]
        for a,b in zip(points,points[1:]):strap.beam(a,b,.018,.012,C.CL)
        _bind_torso(strap.obj(name+' | apron neck strap',character,.002),rig)
    accessories=C.Mesh()
    for zz in [1.03,1.12,1.21,1.30,1.39]:accessories.ellipsoid((.04,-.143,zz),(.011,.007,.011),C.BR,12,6)
    _bind_torso(accessories.obj(name+' | coat buttons',character,.002),rig)
    for side in ['L','R']:
        shoe=C.Mesh();x=arm.bones['foot.'+side].head_local.x
        shoe.ellipsoid((x,-.055,.057),(.070,.145,.057),C.LE,24,12)
        shoe.box((x,-.16,.089),(.070,.025,.041),C.BR)
        _bind_rigid(shoe.obj(name+' | buckled shoe '+side,character,.002),rig,'foot.'+side)
    head=joints['head____head'];top=max(c.z for c in coords[:13380]);hat=C.Mesh()
    # Small cap has a folded band and fabric crown instead of an oversized ball.
    if baker:
        hat.ellipsoid((0,.012,top-.014),(.099,.088,.064),C.CL,32,16)
        hat.torus((0,.007,top-.049),.087,.012,C.CL,n=48)
    else:
        hat.ellipsoid((0,.008,top-.018),(.103,.094,.063),C.DK,32,16)
        hat.ellipsoid((0,-.04,top-.055),(.14,.14,.015),C.DK,32,8)
    _bind_rigid(hat.obj(name+' | period wool cap',character,0),rig,'head')
    # Wrist IK targets are editable scene objects. Shoulder/elbow deformation
    # uses the original weighted skin and no rigid cylinder joints.
    for side,sign in [('L',1),('R',-1)]:
        target=C.root(name+' hand target '+side,(sign*.25,-.21,1.01),character)
        c=rig.pose.bones['grip.'+side].constraints.new('IK');c.name='Palm contact IK';c.target=target;c.chain_count=5;c.use_tail=True;c.use_stretch=False;c.iterations=200
        # Source arms have two deform bones per limb; internal splits must
        # remain rigid rather than behaving like additional elbow joints.
        for segment in ['upperarm02.','lowerarm02.']:
            pb=rig.pose.bones[segment+side];pb.lock_ik_x=True;pb.lock_ik_y=True;pb.lock_ik_z=True
        for finger in range(1,6):
            for segment in [2,3]:
                pb=rig.pose.bones.get('finger%d-%d.%s'%(finger,segment,side))
                if pb:pb.rotation_mode='XYZ';pb.rotation_euler.x=.16
    if name in ['Baker','Porter']:
        for side in ['L','R']:
            foot=arm.bones['foot.'+side]
            ankle=C.root(name+' foot target '+side,foot.head_local,character)
            orient=C.root(name+' foot orientation '+side,(0,0,0),character)
            orient.rotation_euler=foot.matrix_local.to_euler()
            c=rig.pose.bones['lowerleg02.'+side].constraints.new('IK');c.name='Planted ankle';c.target=ankle;c.chain_count=4;c.use_stretch=False;c.iterations=200
            for segment in ['upperleg02.','lowerleg02.']:
                pb=rig.pose.bones[segment+side];pb.lock_ik_x=True;pb.lock_ik_y=True;pb.lock_ik_z=True
            c=rig.pose.bones['foot.'+side].constraints.new('COPY_ROTATION');c.name='Sole remains level';c.target=orient;c.target_space='WORLD';c.owner_space='WORLD'
    bpy.context.view_layer.update()
    return character

def horse(name,p=(0,0,0),angle=0):
    filepath=R/'assets/models/horse/riggedHorse.blend'
    with bpy.data.libraries.load(str(filepath),link=False) as (src,dst):dst.objects=[x for x in src.objects if x in ['Plane','Armature','Sphere','Sphere.002','BezierCurve','BezierCurve.005']]
    objs=[o for o in dst.objects if o]
    for o in objs:bpy.context.collection.objects.link(o)
    rig=next(o for o in objs if o.type=='ARMATURE');body=next(o for o in objs if o.name.startswith('Plane'))
    rig.animation_data_clear()
    for pb in rig.pose.bones:pb.matrix_basis=Matrix.Identity(4)
    bpy.context.view_layer.update()
    coords=[o.matrix_world@Vector(q) for o in objs if o.type=='MESH' for q in o.bound_box]
    minz=min(v.z for v in coords);maxz=max(v.z for v in coords);scale=1.96/(maxz-minz)
    assembly=C.root(name,p);assembly.rotation_euler.z=angle;transform=C.root(name+' | source alignment',(0,0,-minz*scale),assembly);transform.scale=(scale,scale,scale)
    for o in objs:
        if not o.parent:o.parent=transform
        o.name=name+' | '+o.name
        if o.type=='MESH':
            for poly in o.data.polygons:poly.use_smooth=True
    coat=bpy.data.materials.new('Horse | chestnut coat');coat.use_nodes=True;bs=coat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.19,.069,.025,1);bs.inputs['Roughness'].default_value=.6
    # Preserve any embedded source diffuse image if the old material has one.
    old=body.data.materials[0] if body.data.materials else None
    if old and old.use_nodes:
        source=next((n.image for n in old.node_tree.nodes if n.type=='TEX_IMAGE' and n.image),None)
        if source:
            n=coat.node_tree.nodes.new('ShaderNodeTexImage');n.image=source;coat.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color'])
    body.data.materials.clear();body.data.materials.append(coat)
    sub=body.modifiers.new('Smooth anatomical silhouette','SUBSURF');sub.levels=1;sub.render_levels=1
    for o in objs:
        if o.type=='MESH' and o!=body:o.data.materials.clear();o.data.materials.append(C.M[C.LE])
    return assembly
