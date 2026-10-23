"""Production world assembled from the approved detailed asset families."""
import bpy,sys,math,json,random,os,time
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
import craft as C, architecture_assets as A, alpine_environment as E, carriage_assets as V, freight_assets as F, actors

def clone(root,name,position,rotation=0,scale=1):
    originals=[root]+list(root.children_recursive);mapping={}
    for old in originals:
        new=old.copy();new.name=name+' | '+old.name;bpy.context.collection.objects.link(new);mapping[old]=new
    for old,new in mapping.items():
        new.parent=mapping.get(old.parent)
        for mod in new.modifiers:
            if mod.type=='ARMATURE' and mod.object in mapping:mod.object=mapping[mod.object]
        if new.type=='ARMATURE':
            for bone in new.pose.bones:
                for con in bone.constraints:
                    if hasattr(con,'target') and con.target in mapping:con.target=mapping[con.target]
    rr=mapping[root];rr.name=name;rr.location=position;rr.rotation_euler.z=rotation;rr.scale=(scale,scale,scale)
    return rr

def roadpath():
    # Uniform samples of a gently graded cardinal spline; no steps on this route.
    pts=[(23,-37),(21,-27),(17,-18),(11,-10),(3,-6),(-7,-3),(-17,1),(-24,8)]
    out=[]
    for i in range(len(pts)-1):
        p0=Vector(pts[max(0,i-1)]);p1=Vector(pts[i]);p2=Vector(pts[i+1]);p3=Vector(pts[min(len(pts)-1,i+2)])
        for j in range(22):
            t=j/22;p=.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t)
            out.append((p.x,p.y,E.ground(p.x,p.y)+.15))
    return out

def setts(points,width,name,seed=3):
    rng=random.Random(seed);m=C.Mesh();edge=C.Mesh()
    mats=[C.material(name+' granite '+str(i),(.24,.25,.25),.47,texture='rock_boulder_dry',tint=(.51+i*.045,.57+i*.045,.61+i*.045)) for i in range(4)]
    dist=0;last=Vector(points[0]);sample=[]
    for a,b in zip(points,points[1:]):
        a,b=Vector(a),Vector(b);d=(b-a).length
        steps=max(1,round(d/.31))
        for j in range(steps):sample.append((a.lerp(b,j/steps),(b-a).normalized()))
    for row,(p,tan) in enumerate(sample):
        side=Vector((-tan.y,tan.x,0)).normalized();rot=Matrix.Rotation(math.atan2(side.y,side.x),3,'Z')
        n=round(width/.38)
        for j in range(n):
            pos=p+side*((j-(n-1)/2)*.38+(row%2)*.10);pos.z=E.ground(pos.x,pos.y)+.14+rng.uniform(-.005,.005)
            m.box(pos,(.36,.29,.12),rng.choice(mats),rot,jitter=.01,seed=row*90+j)
        for s in [-1,1]:
            pos=p+side*s*(width/2+.12);pos.z=E.ground(pos.x,pos.y)+.16
            if row%2==0:edge.box(pos,(.28,.60,.24),C.ST,rot,jitter=.02,seed=row)
    m.obj(name+' | hand laid wet cobbles',None,.014);edge.obj(name+' | irregular kerbs',None,.018)

def square(x,y,w,d):
    m=C.Mesh();rng=random.Random(67)
    for j in range(round(d/.30)):
        for i in range(round(w/.38)):
            xx=x-w/2+i*.38+(j%2)*.13;yy=y-d/2+j*.30
            m.box((xx,yy,E.ground(xx,yy)+.15),(.36,.28,.12),C.ST,jitter=.009,seed=i+j*30)
    m.obj('Clock square | irregular cleared granite',None,.015)

def landing(name,xy):
    x,y=xy;g=E.ground(x,y);p=(x,y,g+2.7);m=C.Mesh()
    # Footings reach the actual slope; an east approach follows a contour,
    # keeping the stair off the descending carriage road in front.
    for j in range(11):
        for i in range(15):
            xx=x-2.35+(i+.5)*.4;yy=y-2.2+(j+.5)*.4;base=E.ground(xx,yy)-.12;top=g+2.6
            m.box((xx,yy,(base+top)/2),(.405,.405,top-base),C.ST)
    yy=y-1.2;run=.28;n=20;end_x=x+3.65;start_x=end_x+n*run
    bottom=E.ground(start_x,yy);top=g+3.1
    for i in range(n):
        xx=start_x-(i+.5)*run;high=bottom+(top-bottom)*(i+1)/n;base=E.ground(xx,yy)-.10
        m.box((xx,yy,(base+high)/2),(run+.012,1.5,max(.08,high-base)),C.ST)
    for side in [-1,1]:
        for i in [0,5,10,15,19]:
            xx=start_x-(i+.5)*run;z=bottom+(top-bottom)*(i+1)/n
            m.box((xx,yy+side*.82,z+.48),(.08,.08,.96),C.DK,wood=True)
        m.beam((start_x-run/2,yy+side*.82,bottom+(top-bottom)/n+.98),(end_x+run/2,yy+side*.82,top+.98),.07,.08,C.WO)
    m.obj(name+' | dressed stone gallery and stair',None,.016)
    return p

def add_smoke(position,name):
    mat=bpy.data.materials.get('Thin chimney vapour')
    if not mat:
        mat=bpy.data.materials.new('Thin chimney vapour');mat.use_nodes=True;n=mat.node_tree.nodes;n.clear();l=mat.node_tree.links
        out=n.new('ShaderNodeOutputMaterial');p=n.new('ShaderNodeBsdfPrincipled');p.inputs['Base Color'].default_value=(.62,.69,.75,1);p.inputs['Roughness'].default_value=1
        info=n.new('ShaderNodeObjectInfo');alpha=n.new('ShaderNodeMath');alpha.operation='MULTIPLY';alpha.inputs[1].default_value=.07
        l.new(info.outputs['Alpha'],alpha.inputs[0]);l.new(alpha.outputs[0],p.inputs['Alpha']);l.new(p.outputs[0],out.inputs[0]);mat.surface_render_method='DITHERED'
    root=C.root(name,position)
    for j in range(6):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1);o=bpy.context.object;o.name=name+' puff '+str(j);o.parent=root;o.data.materials.append(mat);o['puff_index']=j
        for poly in o.data.polygons:poly.use_smooth=True
    return root

def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    C.M.clear()
    C.palette();random.seed(2217)
    cache=R/'model/environment-assets-v2.blend'
    if cache.exists():E.load_environment_cache()
    else:E.build_environment(tree_density=.7,terrain_step=1.5)
    assets=A.build_variants()
    # Apply the identical static edge treatment once before linked instances.
    # This retains the approved geometry while avoiding a bevel evaluation for
    # every copy of a house in every frame.
    for root in assets.values():
        for ob in root.children_recursive:
            if ob.type=='MESH' and ob.modifiers:
                bpy.context.view_layer.objects.active=ob
                for mod in list(ob.modifiers):
                    bpy.ops.object.modifier_apply(modifier=mod.name)
    placements={'tower':(-2,7,0),'chapel':(-13,16,-.07),'inn':(-14,-9,.1),'workshop':(-19.333,11.494,.15),'grocer':(16,8,-.18),'cottage':(21,-2,-.2)}
    for key,(x,y,rot) in placements.items():assets[key].location=(x,y,E.ground(x,y));assets[key].rotation_euler.z=rot
    bakery=C.chalet('Hill bakery',(-15,26,E.ground(-15,26)),seed=71)
    # Distinct buildings lead from lower commerce to upper homes. Linked detail
    # meshes keep bevels and texture fidelity affordable for distant streets.
    houses=[('cottage',-24,22,.18,.92),('cottage',-24,33,.25,1.05),('inn',-12,39,-.1,.87),('workshop',-2,33,-.2,.85),('cottage',9,31,.12,.92),('cottage',20,28,-.18,1.05),('grocer',26,17,-.23,.85),('workshop',26,-15,-.25,.9),('cottage',4,-18,.12,.92),('cottage',-5,-17,.05,.86),('grocer',-23,-13,.22,.83),('cottage',-28,3,.21,.80),('inn',29,39,-.3,.78),('cottage',3,43,-.1,.82),('workshop',-27,43,.12,.80),('cottage',13,18,-.15,.80)]
    for i,(typ,x,y,rot,sc) in enumerate(houses):clone(assets[typ],'Neighbourhood '+str(i),(x,y,E.ground(x,y)),rot,sc)
    road=roadpath();setts(road,4.4,'Continuous valley carriage road');square(3,1,18,11)
    # Side lanes are walkable; steep connections explicitly use steps.
    side_lanes=[('Upper bakery lane',[(-30,21),(-30,18),(-20,18),(-18.5,21.7),(-5,21.7)],2.2),('Eastern market lane',[(13,-13),(16,1),(20.8,3.8),(20.8,12.7),(18,15),(18,24)],2.5),('Western craftsmen lane',[(-23,5),(-24,9),(-24.7,14),(-23.7,17),(-19.2,18)],2.1)]
    for name,points,width in side_lanes:
        pp=[]
        for p0,p1 in zip(points,points[1:]):
            count=max(1,round(math.dist(p0,p1)/.35))
            pp.extend((p0[0]+(p1[0]-p0[0])*i/count,p0[1]+(p1[1]-p0[1])*i/count,0) for i in range(count))
        setts(pp,width,name,seed=len(name))
    stairs=C.Mesh()
    for i in range(37):
        y=7+i*.40;x=3.5;z=E.ground(x,y)+.17
        stairs.box((x,y,z-.16),(2.0,.42,.32),C.ST)
    stairs.obj('Pedestrian stair from clock square to bakery terrace',None,.016)
    upper=landing('Hill station',(-6.6,21.0));lower=landing('Square station',(8,3))
    ca=Vector(upper)+Vector((0,0,3.62));cb=Vector(lower)+Vector((0,0,3.62))
    span=math.hypot(cb.x-ca.x,cb.y-ca.y);grade=(cb.z-ca.z)/span
    F.station('Hill freight station',upper,slope=grade-2.6/span)
    F.station('Square freight station',lower,slope=grade+2.6/span)
    F.basket();F.crate()
    # A load bearing line and a parallel return/haul line have equal endpoints.
    for offset in [0,F.HAUL_OFFSET]:
        pts=[]
        for j in range(181):
            u=j/180;p=ca.lerp(cb,u);p.z-=.65*4*u*(1-u);p+=F.CABLE_SIDE*offset;pts.append(p)
        C.curve('Main bearing cable' if offset==0 else 'Continuous haul cable',pts,.016 if offset==0 else .010,C.IR)
    # The upper return of the traction rope completes the sheave-to-sheave loop.
    heading=Matrix.Rotation(F.CABLE_HEADING,3,'Z')
    def return_contact(endpoint,slope):
        normal=Vector((0,-slope,1)).normalized()
        return endpoint+heading@(Vector((F.HAUL_OFFSET,0,0))+2*F.SHEAVE_RADIUS*normal)
    ra=return_contact(ca,grade-2.6/span);rb=return_contact(cb,grade+2.6/span)
    pts=[]
    for j in range(181):
        u=j/180;p=ra.lerp(rb,u);p.z-=.65*4*u*(1-u);pts.append(p)
    C.curve('Upper return of continuous traction rope',pts,.010,C.IR)
    baker=actors.human('Baker',Vector(upper)+Vector((1.7,-1.0,.4)),True)
    porter=actors.human('Porter',Vector(lower)+Vector((0,-1.0,.4)))
    baker.rotation_euler.z=math.pi;porter.rotation_euler.z=math.pi
    # Idle townspeople use real skinned anatomy; linked mesh copies retain rigs.
    resident=actors.human('Resident 00',(-3,-5,E.ground(-3,-5)+.23));names=[resident.name]
    lanes=[(-10,-4,1,0,3),(-16,2,0,1,2),(-23,7,0,1,3),(14,-9,0,1,4),(18,16,0,1,4),(-20,19.4,1,0,3),(-2,24,1,0,2),(9,28,1,0,2),(3,2,1,0,2),(-6,0,1,0,2),(-16,-14,1,0,2),(22,-15,0,1,3),(3,-15.2,1,0,2),(21,35,1,0,2),(-13,35,1,0,2),(-26.5,28.5,0,1,2),(7,-5,1,0,2),(11,13,0,1,2)]
    for i,(x,y,dx,dy,span) in enumerate(lanes):
        rr=clone(resident,'Resident %02d'%(i+1),(x,y,E.ground(x,y)+.22),0,.92+(i%4)*.03);rr['base']=[x,y];rr['axis']=[dx,dy];rr['span']=span;rr['phase']=i*1.731;names.append(rr.name)
    resident['base']=[-3,-5];resident['axis']=[1,0];resident['span']=2;resident['phase']=0
    carriage,data=V.build_carriage();bpy.context.scene['carriage_data']=json.dumps(V.serialize_data(data) if hasattr(V,'serialize_data') else {})
    # A narrow flowing watercourse remains open beside the waterwheel house.
    water=C.material('Flowing winter millrace',(.035,.13,.17),.20,.20);wm=C.Mesh()
    for j in range(70):
        y=-22+j*.65;x=-32+.8*math.sin(y*.10);z=E.ground(x,y)-.06
        wm.box((x,y,z),(2.2,.67,.07),water)
    wm.obj('Unfrozen moving millrace',None,0)
    for x in [-33.3,-30.7]:C.drift('Icy stream bank',(x-.40,x+.40),(-24,25),lambda xx,yy:E.ground(xx,yy)+.12,None,.4)
    mill=clone(assets['cottage'],'Waterwheel house',(-27.8,15,E.ground(-27.8,15)),math.pi/2,.68)
    wheel=C.root('Working waterwheel',(-31.1,15,E.ground(-31.1,15)+1.4));ww=C.Mesh();rot=Matrix.Rotation(math.pi/2,3,'Y')
    for x in [-.32,.32]:ww.torus((x,0,0),1.2,.07,C.DK,rot,64)
    for j in range(14):
        a=j*math.tau/14;rr=Matrix.Rotation(a,3,'X');ww.box((0,1.17*math.sin(a),1.17*math.cos(a)),(.86,.24,.12),C.WO,rr,wood=True)
        for x in [-.30,.30]:ww.beam((x,0,0),(x,1.15*math.sin(a),1.15*math.cos(a)),.06,.08,C.DK)
    ww.rod((-.5,0,0),(1.4,0,0),.14,C.DK,24);ww.obj('Larch mill wheel and paddles',wheel,.009)
    bridge=C.Mesh()
    for i in range(27):bridge.box((-34.4+i*.20,-1,E.ground(-32,-1)+.35),(.19,2.3,.14),C.WO,wood=True,seed=i)
    for y in [-2.1,.1]:bridge.beam((-34.5,y,E.ground(-32,-1)+1.4),(-29.1,y,E.ground(-32,-1)+1.4),.08,.08,C.DK)
    bridge.obj('Timber bridge over the active millrace',None,.008)
    # Stalls surround the square without filling the unloading view.
    for x,y in [(-6,-1),(0,-1),(15,1)]:
        pr=C.Mesh()
        for xx in [x-.8,x+.8]:
            for yy in [y-.4,y+.4]:pr.box((xx,yy,E.ground(x,y)+.55),(.09,.09,.9),C.DK,wood=True)
        pr.box((x,y,E.ground(x,y)+1.04),(1.95,1.04,.10),C.WO,wood=True);pr.obj('Market trestle',None,.009)
    smoke=[]
    # Foreground bank physically masks the opening, then the camera rises.
    C.drift('Near snow bank',(-20,80),(-61,-54),lambda x,y:11+3*math.sin((y+61)*math.pi/7)**2+.3*math.sin(x*.13),None,.7)
    S=bpy.context.scene;S['upper_station']=list(upper);S['lower_station']=list(lower);S['cable_A']=list(ca);S['cable_B']=list(cb);S['road']=json.dumps(road);S['residents']=json.dumps(names);S['smoke']=json.dumps(smoke);S['tower_parts']=assets['tower']['animation_parts']
    # Persist animation data using custom properties made by the carriage asset.
    if hasattr(V,'data_to_json'):S['carriage_data']=V.data_to_json(data)
    world=bpy.data.worlds.new('Winter dawn in the mountain pass');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.36,.48,.68,1);world.node_tree.nodes['Background'].inputs[1].default_value=.40;S.world=world
    def light(name,kind,loc,energy,color,target,size=1):
        ld=bpy.data.lights.new(name,kind);ld.energy=energy;ld.color=color
        if kind=='AREA':ld.shape='DISK';ld.size=size
        elif kind=='SUN':ld.angle=.11
        ob=bpy.data.objects.new(name,ld);bpy.context.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
    light('Low warm morning sun','SUN',(-50,-40,55),2.5,(1,.78,.53),(0,5,0))
    light('Valley sky reflection','AREA',(0,-20,75),13000,(.62,.76,1),(0,10,0),65)
    camera=bpy.data.cameras.new('Film camera');ob=bpy.data.objects.new('Film camera',camera);bpy.context.collection.objects.link(ob);S.camera=ob
    camera.clip_end=1200;S.render.resolution_x=1080;S.render.resolution_y=1920;S.render.fps=24;S.frame_start=1;S.frame_end=2160
    S.view_settings.view_transform='AgX';S.view_settings.look='AgX - Medium High Contrast';S.view_settings.exposure=.65
    S.render.engine='CYCLES';S.cycles.samples=48
    import world_grounding
    world_grounding.add_grounding()
    bpy.context.view_layer.update()
    # Emit from actual chimney caps after grounding, including moved/scaled homes.
    for root in [assets['inn'],assets['workshop'],assets['cottage'],bpy.data.objects['Neighbourhood 1'],bpy.data.objects['Neighbourhood 4'],bpy.data.objects['Neighbourhood 6']]:
        chimney=next((ob for ob in root.children_recursive if ob.type=='MESH' and 'capped stone chimney' in ob.name),None)
        if chimney:
            cap=max(v.co.z for v in chimney.data.vertices)
            top=[v.co for v in chimney.data.vertices if v.co.z>cap-.04]
            local=sum(top,Vector())/len(top)
            smoke.append(add_smoke(chimney.matrix_world@local,'Chimney '+str(len(smoke))).name)
    # The approved bakery has its chimney integrated into the masonry mesh.
    emitter=add_smoke(bakery.matrix_world@Vector((1.75,1,9.03)),'Bakery chimney');smoke.append(emitter.name)
    S['smoke']=json.dumps(smoke)
    steam=add_smoke((0,0,0),'Fresh bread steam');steam['bread_steam']=True
    bpy.context.view_layer.update();bpy.ops.file.pack_all()
    # Keep name-based handles, never Python object addresses, for fresh processes.
    S['carriage_root']=carriage.name
    bpy.ops.outliner.orphans_purge(do_local_ids=True,do_linked_ids=True,do_recursive=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(R/'model/clock-city-production-v2.blend'))
    (R/'render/world-build.json').write_text(json.dumps({'objects':len(bpy.data.objects),'mesh_faces':sum(len(m.polygons) for m in bpy.data.meshes),'stations':[upper,lower],'road_points':len(road),'largest_meshes':[{'name':m.name,'faces':len(m.polygons),'users':m.users} for m in sorted(bpy.data.meshes,key=lambda m:len(m.polygons),reverse=True)[:15]],'status':'built; camera and motion pending sample verification'},indent=2),encoding='utf8')
    print('WORLD_READY',flush=True)

if __name__=='__main__':build()
