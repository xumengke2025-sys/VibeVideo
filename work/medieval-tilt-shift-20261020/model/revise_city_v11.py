"""User-directed revision: irregular lived-in traffic, legible sculpture and two civic sites.

Preserves the v10 city, river crossings, boat parenting, materials and horizon.
All traffic is precomputed at 8 Hz with fixed seed, obstacles and local separation.
"""
import ast, bpy, bmesh, json, math, random, time
import numpy as np
from pathlib import Path
from collections import defaultdict
from mathutils import Vector, Matrix
from mathutils.geometry import tessellate_polygon

ROOT = Path(__file__).resolve().parent
QA = ROOT.parent / 'qa/v11'
QA.mkdir(parents=True, exist_ok=True)
R = random.Random(2026102111)
bpy.ops.wm.open_mainfile(filepath=str(ROOT / 'babylon-city-v10.blend'))
scene = bpy.context.scene
linen = bpy.data.materials['Natural flax canvas']
for filename, selected in [('build_city.py', None), ('enrich_city_v8.py', {'box','uvball','rod','inst','group_new','instance_collection_from','clear_houses','frieze','statue'})]:
    tree = ast.parse((ROOT / filename).read_text(encoding='utf8'))
    defs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and (selected is None or n.name in selected)]
    exec(compile(ast.Module(body=defs, type_ignores=[]), filename, 'exec'))
blue = [bpy.data.materials['Lapis fired glaze '+str(i)] for i in range(8)]
clay = [bpy.data.materials['Sun dried brick '+str(i)] for i in range(6)]
for var, name in [('stone','Worn limestone'),('wood','Dark date palm timber'),('potmat','Hand fired terracotta'),('leafmat','Palm leaf'),('leaflight','Palm young leaf'),('sand','Alluvial sand'),('buff','Ivory glazed relief'),('ochre','Ochre glazed accent'),('dark','Interior shade'),('linen','Natural flax canvas'),('bronze','Oxidized bronze')]:
    globals()[var] = bpy.data.materials[name]
cloths = [bpy.data.materials[n] for n in ['Natural flax canvas','Madder dyed fabric','Indigo handwoven cloth','Saffron handwoven cloth','Faded sage cloth']]
gold = bpy.data.materials['V8 aged royal bronze']
batch = defaultdict(lambda: [[], []]); counts = defaultdict(int); _spheres = {}
# Beveled block batch prototype, reused by brick courses and paving.
bpy.ops.mesh.primitive_cube_add(size=1)
proto = bpy.context.object
mod = proto.modifiers.new('Soft brick arris','BEVEL'); mod.width=.035; mod.segments=2
bpy.ops.object.modifier_apply(modifier=mod.name)
pv = [v.co.copy() for v in proto.data.vertices]; pf = [tuple(p.vertices) for p in proto.data.polygons]
bpy.data.objects.remove(proto, do_unlink=True)

def stage(name):
    print('V11_BUILD_STAGE', name, flush=True)
    (QA/'build-progress.json').write_text(json.dumps({'stage':name,'objects':len(scene.objects),'time':time.time()}),encoding='utf8')

# Remove all earlier people and animals. Their local collection assets are reused.
removed = []
for key in ['actor_names','v8_crowd','v8_animals']:
    for name in json.loads(scene.get(key, '[]')):
        ob = bpy.data.objects.get(name)
        if ob:
            for child in list(ob.children):
                bpy.data.objects.remove(child, do_unlink=True)
            removed.append(name); bpy.data.objects.remove(ob, do_unlink=True)
    scene[key] = '[]'
stage('old_lane_and_synchronous_traffic_removed')

# Two visually distinct civic complexes; preserve the avenue and canal corridors.
def clear_site(cx,cy,w,d):
    clear_houses(cx,cy,w,d)
    for ob in list(scene.objects):
        # The inherited core also contains already-realised courtyard meshes.
        # Removing collection instances alone leaves old walls inside new sites.
        residential=ob.name.startswith(('Metropolis courtyard','Courtyard neighbourhood','East bank courtyard','Distant inhabited courtyard','Foreground street block'))
        if residential and abs(ob.location.x-cx)<w/2+30 and abs(ob.location.y-cy)<d/2+30:
            if ob.type=='MESH':
                corners=[ob.matrix_world@Vector(v) for v in ob.bound_box]
                if max(v.x for v in corners)>cx-w/2-1 and min(v.x for v in corners)<cx+w/2+1 and max(v.y for v in corners)>cy-d/2-1 and min(v.y for v in corners)<cy+d/2+1:
                    bpy.data.objects.remove(ob,do_unlink=True);continue
        if ob.name.startswith(('Terrace foliage','Trailing garden foliage')) and abs(ob.location.x-cx)<w/2+2 and abs(ob.location.y-cy)<d/2+2:
            bpy.data.objects.remove(ob,do_unlink=True)

def cornice(x,y,w,d,h):
    box('V11 limestone roof coping',(x,y,h+.12),(w+.3,d+.3,.28),stone,.035)
    for xx in [x-w/2+.55+i*1.5 for i in range(max(1,int(w/1.5)))]:
        box('V11 stepped blue merlon',(xx,y-d/2,h+.64),(.55,.62,.8),blue[3],.025)
    frieze(x,y-d/2-.07,max(.5,h-2.3),w)

# Courtyard temple at the west end of a new cross-street, open toward the city.
cx,cy=-47,143
clear_site(cx,cy,37,34)
box('V11 temple raised paving',(cx,cy,.12),(36,33,.32),stone,.06)
for x,y,w,d,h in [(-62,143,5,30,10),(-32,143,5,30,10),(-47,156,26,5,13),(-58,128,10,4,9),(-36,128,10,4,9)]:
    box('V11 civic temple masonry',(x,y,h/2),(w,d,h),clay[2],.065)
    cornice(x,y,w,d,h)
for x in [-52.5,-41.5]:
    box('V11 blue shrine entrance pier',(x,153,8.3),(3,2,8),blue[1],.06)
    for z in [5,10.8]:box('V11 shrine ivory band',(x,151.96,z),(3.15,.16,.22),buff,.02)
    for z in [5.6,8,10.2]:rosette(x,151.83,z,1.3)
box('V11 shrine dark doorway',(-47,153,6.1),(7.5,.25,10),dark,.02)
box('V11 shrine lintel',(-47,152.6,12),(14,.9,1.5),blue[2],.04)
box('V11 low ritual dais',(-47,148,.5),(10,5,1),stone,.04)
for i in range(5):box('V11 shrine access tread',(-47,144.8+i*.47,(i+1)*.1),(6,.5,(i+1)*.2),stone,.02)
for x in [-57,-37]:
    for y in [133,139,145,150]:
        rod('V11 timber courtyard column',(x,y,.3),(x,y,5.8),.22,wood)
        box('V11 glazed column footing',(x,y,.5),(.75,.75,.6),blue[3],.03)
        box('V11 column capital',(x,y,5.8),(.85,.85,.24),buff,.025)
    box('V11 portico architrave',(x,141.5,5.95),(.6,19,.35),wood,.03)
    canopy(x,141.5,6.2,5,20,linen)
for x,y in [(-54,134),(-40,134),(-54,148),(-40,148)]:
    pot(x,y,.3,.8)
for x,y in [(-62,124),(-31,124),(-64,162),(-30,162)]:palm(x,y,6.4)
clear_site(-17,132,23,6)
box('V11 connected temple cross street',(-17,132,.012),(29,5.6,.08),stone,.025)
for i in range(5):
    box('V11 transverse street paver',(-28+i*5.5,132,.07),(4.8,4.8,.045),stone,.015)

# Canal grain exchange, four storage wings and a working quay rather than another tower.
cx,cy=62,141
clear_site(cx,cy,35,32)
box('V11 exchange courtyard paving',(cx,cy,.08),(33,31,.2),stone,.035)
for x,y,w,d,h in [(76,141,5,29,10),(62,154,26,5,8.5),(62,128,26,5,8.5),(48,134,4,11,7.5),(48,149,4,10,7.5)]:
    box('V11 granary thick mudbrick wall',(x,y,h/2),(w,d,h),clay[4],.08)
    cornice(x,y,w,d,h)
    if w>d:
        for xx in [x-w/2+2+j*3 for j in range(int((w-2)/3))]:
            box('V11 recessed granary ventilation',(xx,y-d/2-.035,h-1.6),(.6,.06,.7),dark,.015)
for yy in [132.5,138,145,150]:
    box('V11 warehouse open doorway',(73.44,yy,1.8),(.06,1.7,3.6),dark,.01)
    box('V11 warehouse lintel',(73.28,yy,3.75),(.45,2,.28),wood,.025)
for x in [53,69]:
    canopy(x,141,4.2,5.5,15,cloths[0 if x==53 else 2])
for j in range(28):
    x=R.choice([52.5,69])+R.uniform(-1.1,1.1);y=R.uniform(134,150)
    if j%3:pot(x,y,.2,R.uniform(.5,.9))
    else:box('V11 bound grain sack',(x,y,.45),(.6,.85,.8),linen,.15)
box('V11 continuous east warehouse quay',(44.8,140,.22),(4.7,33,.35),stone,.04)
for yy in [131,145]:
    box('V11 loading platform',(42.7,yy,.6),(2.3,4.5,.25),wood,.025)
    for x in [42.2,43.3]:rod('V11 mooring bollard',(x,yy,.3),(x,yy,1.1),.12,wood)
for x,y in [(50,123),(78,124),(78,159)]:palm(x,y,5.8)

def handcart(x,y,rot):
    before=set(scene.objects)
    box('V11 cart planked bed',(0,0,.85),(1.4,2.1,.16),wood,.025)
    for side in [-1,1]:
        rod('V11 cart handle',(side*.53,-.8,.8),(side*.53,-2.3,.9),.045,wood)
        rod('V11 solid wooden cart wheel',(side*.85,0,.65),(side*.96,0,.65),.62,wood)
        rod('V11 cart wheel hub',(side*.76,0,.65),(side*1.07,0,.65),.11,bronze)
    rod('V11 cart axle',(-1,0,.65),(1,0,.65),.08,wood)
    for i in range(4):box('V11 cart goods',((i%2-.5)*.56,(i//2-.5)*.75,1.2),(.5,.64,.55),linen,.08)
    p=group_new(before,'V11 loaded handcart',(x,y,0));p.rotation_euler.z=rot
handcart(47,126,.65);handcart(57,150,-.4)
flush();stage('courtyard_temple_and_grain_exchange_built')

# Statues face the actual south entrance, with a readable three-quarter camera.
for ob in list(scene.objects):
    if ob.name.startswith('V8 divine monument'):bpy.data.objects.remove(ob,do_unlink=True)
gold=textured('V11 weathered dark bronze','665238',.48,True)
male=statue('divine');male.name='V11 bearded guardian deity'
gold=textured('V11 warm carved sandstone','c5a56b',.68)
female=statue('divine');female.name='V11 eight star goddess'
for ob in list(female.objects):
    if ob.name.startswith(('V8 carved curled beard','V8 royal cap','V8 closed royal crown','V8 diadem band')):
        bpy.data.objects.remove(ob,do_unlink=True)
    elif ob.name.startswith('V8 sculpted royal torso'):
        ob.scale.x*=.83
# An eight-point star, hair and a closed high diadem make this a distinct silhouette.
before=set(scene.objects)
uvball('V11 goddess sculpted hair',(0,.06,4.08),(.29,.22,.46),blue[0],24)
lathe('V11 goddess diadem',(0,0,4.27),[(.23,0),(.21,.34),(.08,.48),(0,.5)],gold)
verts=[]
for i in range(16):
    a=i*math.pi/8;r=.28 if i%2==0 else .105
    verts.append((r*math.sin(a),-.255,4.6+r*math.cos(a)))
objmesh('V11 eight pointed divine star',verts,[tuple(range(16))],buff)
for x in [-.24,.24]:
    for j in range(9):uvball('V11 carved goddess braid',(x,.08,4.16-j*.095),(.065,.085,.065),blue[0],12)
flush()
for ob in set(scene.objects)-before:
    for col in list(ob.users_collection):col.objects.unlink(ob)
    female.objects.link(ob)
inst(female,'V11 south facing star goddess',(47.8,50,4.3),1.48,0)
inst(male,'V11 south facing bearded deity',(56.3,50.5,4.3),1.60,0)
# Side votive monument looks inward across the court, rather than sharing a direction.
inst(bpy.data.collections['V8 royal statue module'],'V11 inward facing votive figure',(44.8,48,4.3),.65,math.pi/2)
for x in [47.2,57.2]:
    box('V11 guardian lion plinth',(x,43.2,4.5),(1.6,2.5,.4),blue[2],.04)
    uvball('V11 recumbent lion torso',(x,43.5,5.2),(.5,.84,.46),stone,20)
    uvball('V11 lion mane',(x,42.9,5.72),(.54,.4,.6),ochre,20)
    uvball('V11 lion face',(x,42.6,5.77),(.33,.27,.34),stone,20)
    for side in [-1,1]:
        uvball('V11 guardian lion paw',(x+side*.3,42.5,4.95),(.19,.42,.14),stone,16)
        uvball('V11 guardian lion eye',(x+side*.13,42.37,5.88),(.04,.025,.035),dark,12)
box('V11 offering table',(52,49,5),(2,1.5,1.4),stone,.05)
for x in [50.5,53.5]:
    lathe('V11 bronze offering basin',(x,48.2,4.3),[(.4,0),(.24,.22),(.2,1),(.55,1.15),(.58,1.28),(.43,1.25)],bronze)
for i in range(4):pot(51.3+i*.45,49,5.7,.35)
for x in [45.2,59]:
    box('V11 votive inscribed stele',(x,52.8,5.4),(1,.5,2.2),blue[1],.05)
    for i in range(9):box('V11 stele wedge inscription',(x-.28+(i%3)*.25,52.535,5.3+(i//3)*.3),(.11,.045,.06),buff,.01)
flush();stage('sculpture_axis_and_variety_built')

# Six linked stride poses per clothing style; no geometry duplication per pedestrian.
pose_scene=bpy.data.scenes.new('V11 temporary pose bake scene')
bpy.context.window.scene=pose_scene
def pose_modules(source, label, animal=False):
    variants=[]
    for pose in range(6):
        col=bpy.data.collections.new(f'V11 {label} stride {pose}')
        col.use_fake_user=True
        a=math.sin(pose*math.tau/6)
        for original in source.objects:
            ob=original.copy();ob.data=original.data;ob.parent=None
            name=original.name
            if not animal and name.startswith(('Walking leg','Leather sandal')):
                side=1 if ob.location.x>0 else -1
                ob.location.y+=side*a*.16
                if name.startswith('Walking leg'):ob.rotation_euler.x+=side*a*.30
                else:ob.location.z+=max(0,side*a)*.045
            elif not animal and name.startswith('Resident arm'):
                ob.rotation_euler.x+=a*(.12 if ob.location.x>0 else -.12)
            elif animal and 'animal' in name and ('upper leg' in name or 'lower leg' in name or 'hoof' in name):
                side=(1 if ob.location.x>0 else -1)*(1 if ob.location.y>0 else -1)
                ob.location.y+=side*a*.13
                if 'leg' in name:ob.rotation_euler.x+=side*a*.17
            col.objects.link(ob)
        # Bake rigid parts into one shared mesh per pose. This preserves actor
        # silhouette/materials while avoiding thousands of per-frame instances.
        pose_scene.collection.children.link(col)
        bpy.context.view_layer.update();depsgraph=bpy.context.evaluated_depsgraph_get()
        vv=[];ff=[];mi=[];smooth_faces=[];mats=[]
        for ob in list(col.objects):
            evaluated=ob.evaluated_get(depsgraph);data=evaluated.to_mesh()
            if data is None:raise RuntimeError(('Unbaked pose part',ob.name,ob.type))
            transform=Matrix.LocRotScale(ob.location,ob.rotation_euler.to_quaternion(),ob.scale)
            offset=len(vv);vv.extend([transform@v.co for v in data.vertices])
            local=[]
            for mat in data.materials:
                # Evaluated IDs are temporary; only attach original datablocks
                # to the saved mesh, or Blender later dereferences freed IDs.
                mat=bpy.data.materials[mat.name]
                if mat not in mats:mats.append(mat)
                local.append(mats.index(mat))
            for p in data.polygons:
                ff.append(tuple(offset+i for i in p.vertices));mi.append(local[p.material_index] if local else 0);smooth_faces.append(p.use_smooth)
            evaluated.to_mesh_clear()
            bpy.data.objects.remove(ob,do_unlink=True)
        mesh=bpy.data.meshes.new(col.name+' baked mesh');mesh.from_pydata(vv,[],ff)
        for mat in mats:mesh.materials.append(mat)
        for p,index,sm in zip(mesh.polygons,mi,smooth_faces):p.material_index=index;p.use_smooth=sm
        merged=bpy.data.objects.new(col.name+' baked actor',mesh);col.objects.link(merged)
        pose_scene.collection.children.unlink(col)
        print('V11_POSE_BAKED',label,pose,flush=True)
        variants.append(col.name)
    return variants
human_poses=[pose_modules(bpy.data.collections['V8 resident module '+str(i)],'resident '+str(i)) for i in range(10)]
donkey_poses=pose_modules(bpy.data.collections['V8 donkey module'],'pack donkey',True)
goat_poses=pose_modules(bpy.data.collections['V8 goat module'],'goat',True)
bpy.context.window.scene=scene
bpy.data.scenes.remove(pose_scene)

# Walkable regions and actual street obstructions. No lane snapping or frame wrapping.
regions={
 'avenue':(-6.4,6.4,-24,139,.02),
 'quay':(19.2,22.2,10,115,.04),
 'palace':(-51.7,-40.4,26,39,.43),
 'shrine':(-54.6,-39.4,132.5,144,.3),
 'grain':(57.8,65.8,132,148.5,.2),
 'warehouse_quay':(43.7,45.7,126,153,.41),
 'temple':(48.8,55.2,43.2,46.8,4.3),
 'goat':(3.3,6.3,63,72,.02)
}
obstacles=[(-6.5,-2.7,47.8,52.2),(-6.3,-3.3,-13.5,-10.5)]
agents=[]
def free(p,r,region):
    x0,x1,y0,y1,_=regions[region]
    if not (x0+r<=p[0]<=x1-r and y0+r<=p[1]<=y1-r):return False
    if region=='avenue':
        for a,b,c,d in obstacles:
            if a-r<p[0]<b+r and c-r<p[1]<d+r:return False
    return True
def point(region,r=.3,near=None):
    x0,x1,y0,y1,z=regions[region]
    for _ in range(500):
        p=np.array([R.uniform(x0+r,x1-r),R.uniform(y0+r,y1-r)])
        if near is not None:p=np.array(near)+np.array([R.uniform(-2,2),R.uniform(-2.5,2.5)])
        if free(p,r,region):return p
    raise RuntimeError(('No free nav point',region))
def add(region,kind='human',stationary=False,near=None,look=None,group=None):
    radius=.31 if kind=='human' else .66 if kind=='donkey' else .42
    for _ in range(600):
        p=point(region,radius,near)
        if all(np.linalg.norm(p-a['p'])>radius+a['r']+.12 or abs(regions[region][4]-regions[a['region']][4])>1 for a in agents):break
    else:raise RuntimeError(('Initial packing failed',region,kind))
    poses=human_poses[R.randrange(10)] if kind=='human' else donkey_poses if kind=='donkey' else goat_poses
    ob=inst(bpy.data.collections[poses[0]],f'V11 {kind} {len(agents):03}',(p[0],p[1],regions[region][4]),R.uniform(.91,1.08) if kind=='human' else R.uniform(.79,.96) if kind=='donkey' else R.uniform(.66,.82))
    ob['stride_modules']=json.dumps(poses)
    speed=(R.uniform(.47,1.07) if kind=='human' else R.uniform(.28,.57) if kind=='donkey' else R.uniform(.13,.32))*1.8
    yaw=R.random()*math.tau if look is None else math.atan2(look[0]-p[0],-(look[1]-p[1]))
    agents.append({'name':ob.name,'p':p,'region':region,'kind':kind,'r':radius,'speed':speed,'target':point(region,radius),'pause':R.uniform(0,12) if not stationary else 9999.,'stationary':stationary,'yaw':yaw,'phase':R.random()*math.tau,'stride':R.uniform(.76,1.15),'group':group})

for i in range(112):add('avenue')
for group,center in enumerate([(-2,16),(2.8,29),(-2.8,38),(3.5,49),(-1.8,61),(2.4,83),(-2.5,102),(2,120)]):
    for _ in range(R.choice([2,3,4])):add('avenue',stationary=True,near=center,look=center,group=group)
for center in [(-5.5,22),(5.4,40),(-5.2,57),(5.3,73)]:
    for _ in range(3):add('avenue',stationary=True,near=center,look=(center[0]*1.4,center[1]))
for _ in range(34):add('quay')
for region,count in [('palace',12),('shrine',18),('grain',18),('temple',8)]:
    for _ in range(count):add(region,stationary=R.random()<.55)
for _ in range(6):add('warehouse_quay',stationary=True,look=(42,140))
for i,center in enumerate([(-1.2,22),(2.1,43),(-2,78),(1.7,107)]):
    for j in range(2):add('avenue','donkey',stationary=j==0,near=center,group=100+i)
for _ in range(3):add('grain','donkey',stationary=True)
for _ in range(2):add('quay','donkey')
for _ in range(10):add('goat','goat',stationary=R.random()<.3)
stage('irregular_traffic_and_social_groups_placed')

# Fixed-time local steering and personal space. Positions are independent of render order.
hz=8;duration=76;steps=duration*hz+1
cache=np.zeros((steps,len(agents),7),dtype=np.float32)
minimum_separation=100.
for step in range(steps):
    t=step/hz
    bins=defaultdict(list)
    for i,a in enumerate(agents):bins[(int(math.floor(a['p'][0]/2)),int(math.floor(a['p'][1]/2)))].append(i)
    updates=[]
    for i,a in enumerate(agents):
        p=a['p'];a['pause']-=1/hz
        if np.linalg.norm(a['target']-p)<.7 and a['pause']<=0:
            a['target']=point(a['region'],a['r']);a['pause']=R.uniform(.4,8) if R.random()<.6 else 0
        delta=a['target']-p;dist=np.linalg.norm(delta)
        walking=not a['stationary'] and a['pause']<=0 and dist>.2
        vel=delta/max(dist,.01)*a['speed'] if walking else np.zeros(2)
        # A gentle, unique course preference; no synchronized oscillating rows.
        if walking:vel+=np.array([math.sin(t*.43+a['phase']),math.cos(t*.37+a['phase'])])*.09
        key=(int(math.floor(p[0]/2)),int(math.floor(p[1]/2)))
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                for j in bins.get((key[0]+dx,key[1]+dy),[]):
                    if i==j:continue
                    b=agents[j]
                    if abs(regions[a['region']][4]-regions[b['region']][4])>1:continue
                    offset=p-b['p'];d=np.linalg.norm(offset);safe=a['r']+b['r']+.22
                    if .001<d<safe+.5 and not a['stationary']:
                        vel+=offset/d*max(0,(safe+.5-d))*.95
        if a['stationary']:vel=np.zeros(2)
        speed=np.linalg.norm(vel)
        if speed>a['speed']*1.25:vel*=a['speed']*1.25/speed
        q=p+vel/hz
        if not free(q,a['r'],a['region']):
            alternatives=[p+np.array([vel[0]/hz,0]),p+np.array([0,vel[1]/hz])]
            q=next((v for v in alternatives if free(v,a['r'],a['region'])),p.copy())
            if np.linalg.norm(q-p)<.005 and walking and step%16==i%16:a['target']=point(a['region'],a['r'])
        updates.append(q)
    # Enforce personal space after steering. Repulsion alone permits head-on
    # crossings and crowd compression next to a stationary conversation group.
    projected=np.array(updates)
    radii=np.array([a['r'] for a in agents])
    desired=radii[:,None]+radii[None,:]+.045
    same_level=np.abs(np.array([regions[a['region']][4] for a in agents])[:,None]-np.array([regions[a['region']][4] for a in agents])[None,:])<1
    for iteration in range(20):
        distance=np.linalg.norm(projected[:,None,:]-projected[None,:,:],axis=2)
        pairs=list(zip(*np.where(np.triu((distance<desired-.002)&same_level,k=1))))
        if not pairs:break
        for i,j in pairs:
            a,b=agents[i],agents[j]
            offset=projected[i]-projected[j];d=np.linalg.norm(offset)
            if d>=desired[i,j]:continue
            if a['stationary'] and b['stationary']:continue
            direction=offset/max(d,1e-6) if d>1e-6 else np.array([1.,0.])
            correction=direction*(desired[i,j]-d+.006)
            wa=0. if a['stationary'] else 1.
            wb=0. if b['stationary'] else 1.
            qa=projected[i]+correction*wa/(wa+wb)
            qb=projected[j]-correction*wb/(wa+wb)
            fa=free(qa,a['r'],a['region']);fb=free(qb,b['r'],b['region'])
            if wa and fa:projected[i]=qa
            if wb and fb:projected[j]=qb
            if wa and not fb:
                qa=projected[i]+correction
                if free(qa,a['r'],a['region']):projected[i]=qa
            if wb and not fa:
                qb=projected[j]-correction
                if free(qb,b['r'],b['region']):projected[j]=qb
    # A blocked local cluster waits instead of being pushed into another body.
    # Rollbacks propagate only through its actual conflicting neighbours.
    for iteration in range(len(agents)):
        distance=np.linalg.norm(projected[:,None,:]-projected[None,:,:],axis=2)
        pairs=list(zip(*np.where(np.triu((distance<desired-.015)&same_level,k=1))))
        if not pairs:break
        for i,j in pairs:
            projected[i]=agents[i]['p'].copy();projected[j]=agents[j]['p'].copy()
    for i,(a,q) in enumerate(zip(agents,projected)):
        actual=(q-a['p'])*hz;moving=np.linalg.norm(actual)>.08
        if moving:
            yaw_target=math.atan2(actual[0],-actual[1]);difference=(yaw_target-a['yaw']+math.pi)%math.tau-math.pi
            a['yaw']+=max(-.27,min(.27,difference))
            a['phase']+=np.linalg.norm(actual)/hz*4.3/a['stride']
        z=regions[a['region']][4]+(.014*math.sin(a['phase']*2) if moving else 0)
        pose=int((a['phase']%math.tau)/math.tau*6) if moving else 0
        yaw=a['yaw']+(.06*math.sin(t*.7+a['phase']) if a['stationary'] else 0)
        cache[step,i]=[q[0],q[1],z,yaw,pose,float(moving),a['phase']]
        a['p']=q
    if step%80==0:print('V11_SIM',step,'/',steps,flush=True)

names=[a['name'] for a in agents]
np.savez_compressed(str(ROOT.parent/'traffic-v11.npz'),state=cache,names=np.array(names),hz=np.array(hz),duration=np.array(duration),radii=radii,regions=np.array([a['region'] for a in agents]))
scene['v11_actors']=json.dumps(names)
scene['city_version']='v11'
scene['v11_scope']='Irregular obstacle-aware pedestrians, paused social groups, browsing livestock, distinct entrance-facing sculpture, courtyard temple and grain exchange.'
# Recalculate normals of newly shared sculptural meshes.
for mesh in bpy.data.meshes:
    if mesh.name.startswith('V8 shared sculptural sphere') and mesh.users:
        bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'babylon-city-v11.blend'))
report={'removed_old_agents':len(removed),'new_agents':len(agents),'humans':sum(a['kind']=='human' for a in agents),'donkeys':sum(a['kind']=='donkey' for a in agents),'goats':sum(a['kind']=='goat' for a in agents),'stationary_social_and_working_figures':sum(a['stationary'] for a in agents),'cache_shape':list(cache.shape),'traffic_seed':2026102111,'regions':regions,'obstacles':obstacles,'statue_facing':'Main figures face south entrance and stair; side votive faces east into court. New camera must show faces.','new_sites':['courtyard shrine at (-47,143)','canal grain exchange at (62,141)'],'historical_scope':'Neo-Babylonian inspired fantasy; no archaeological identity asserted for new statues or buildings.','status':'Built; rendered proof and traffic clearance sampling required.'}
(QA/'model-evidence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
stage('v11_model_and_traffic_cache_saved')
