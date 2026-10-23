"""V8: inhabited Babylon-inspired ensemble; true geometry, shared street network.
Fantasy reconstruction, not an archaeological reconstruction of all monuments.
"""
import bpy, math, random, json, ast, time
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.geometry import tessellate_polygon
from collections import defaultdict
ROOT=Path(__file__).resolve().parent;R=random.Random(202610208)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'babylon-city-v6.blend'))
scene=bpy.context.scene
linen=bpy.data.materials['Natural flax canvas']
tree=ast.parse((ROOT/'build_city.py').read_text(encoding='utf8'))
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'helpers','exec'))
blue=[bpy.data.materials['Lapis fired glaze '+str(i)] for i in range(8)]
clay=[bpy.data.materials['Sun dried brick '+str(i)] for i in range(6)]
for var,name in [('stone','Worn limestone'),('wood','Dark date palm timber'),('potmat','Hand fired terracotta'),('leafmat','Palm leaf'),('leaflight','Palm young leaf'),('sand','Alluvial sand'),('buff','Ivory glazed relief'),('ochre','Ochre glazed accent'),('dark','Interior shade'),('redcloth','Madder dyed fabric'),('bronze','Oxidized bronze'),('mortar','Recessed dusty mortar')]:
    globals()[var]=bpy.data.materials[name]
batch=defaultdict(lambda:[[],[]]);counts=defaultdict(int)
bpy.ops.mesh.primitive_cube_add(size=1);proto=bpy.context.object
be=proto.modifiers.new('Soft arris','BEVEL');be.width=.035;be.segments=2
bpy.ops.object.modifier_apply(modifier=be.name)
pv=[v.co.copy() for v in proto.data.vertices];pf=[tuple(p.vertices) for p in proto.data.polygons]
bpy.data.objects.remove(proto,do_unlink=True)
cloths=[linen,redcloth,bpy.data.materials['Indigo handwoven cloth'],bpy.data.materials['Saffron handwoven cloth'],bpy.data.materials['Faded sage cloth']]
gold=textured('V8 aged royal bronze','aa8241',.32,True)
skin=bpy.data.materials['Sunlit warm skin']
fur=[textured('V8 animal hide '+str(i),c,.86) for i,c in enumerate(['786452','c9b999','9c8062','64574c'])]

# Direct data API avoids an entire-city dependency update for every little part.
def box(name,pos,size,mat,bevel=.04):
    sx,sy,sz=[v/2 for v in size]
    verts=[(-sx,-sy,-sz),(sx,-sy,-sz),(sx,sy,-sz),(-sx,sy,-sz),(-sx,-sy,sz),(sx,-sy,sz),(sx,sy,sz),(-sx,sy,sz)]
    ob=objmesh(name,verts,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat);ob.location=pos
    if bevel:
        m=ob.modifiers.new('Worn arris','BEVEL');m.width=bevel;m.segments=2
        ob.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return ob
_spheres={}
def uvball(name,pos,size,mat,segments=20):
    key=(segments,mat.name)
    if key not in _spheres:
        vv=[];ff=[];rings=10
        for j in range(rings+1):
            a=math.pi*j/rings
            for i in range(segments):
                b=math.tau*i/segments;vv.append((math.sin(a)*math.cos(b),math.sin(a)*math.sin(b),math.cos(a)))
        for j in range(rings):
            for i in range(segments):
                a=j*segments+i;b=j*segments+(i+1)%segments;ff.append((a,a+segments,b+segments,b))
        me=bpy.data.meshes.new('V8 shared sculptural sphere');me.from_pydata(vv,[],ff);me.materials.append(mat)
        for p in me.polygons:p.use_smooth=True
        _spheres[key]=me
    ob=bpy.data.objects.new(name,_spheres[key]);scene.collection.objects.link(ob);ob.location=pos;ob.scale=size
    return ob
def rod(name,a,b,r,mat,r2=None):
    d=Vector(b)-Vector(a);L=d.length;N=10;r2=r if r2 is None else r2
    vv=[(rad*math.cos(i/N*math.tau),rad*math.sin(i/N*math.tau),z) for z,rad in [(-L/2,r),(L/2,r2)] for i in range(N)]
    ff=[tuple(reversed(range(N))),tuple(range(N,2*N))]
    ff += [(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
    ob=objmesh(name,vv,ff,mat);ob.location=(Vector(a)+Vector(b))/2;ob.rotation_euler=d.to_track_quat('Z','Y').to_euler()
    for p in ob.data.polygons:p.use_smooth=True
    return ob
def stage(label):
    print('BUILD_STAGE',label,flush=True)
    (ROOT/'out/build-v8-progress.json').write_text(json.dumps({'stage':label,'objects':len(scene.objects),'time':time.time()}),encoding='utf8')
stage('source_loaded_direct_mesh_helpers_ready')

def group_new(before,name,origin=(0,0,0)):
    flush();objects=set(scene.objects)-before
    parent=bpy.data.objects.new(name,None);scene.collection.objects.link(parent)
    # Geometry was built around zero, so parent translations are simple world paths.
    for ob in objects:ob.parent=parent
    parent.location=origin
    return parent

def instance_collection_from(before,name):
    flush();col=bpy.data.collections.new(name)
    for ob in set(scene.objects)-before:
        for c in list(ob.users_collection):c.objects.unlink(ob)
        col.objects.link(ob)
    return col

def inst(col,name,pos,scale=1,rot=0):
    ob=bpy.data.objects.new(name,None);ob.instance_type='COLLECTION';ob.instance_collection=col
    scene.collection.objects.link(ob);ob.location=pos;ob.scale=(scale,)*3;ob.rotation_euler.z=rot
    return ob

def clear_houses(cx,cy,w,d):
    for ob in list(scene.objects):
        if ob.instance_type=='COLLECTION' and ob.instance_collection and ('courtyard' in ob.instance_collection.name.lower() or 'inhabited block' in ob.instance_collection.name.lower()):
            if abs(ob.location.x-cx)<w/2+5 and abs(ob.location.y-cy)<d/2+5:
                bpy.data.objects.remove(ob,do_unlink=True)

def frieze(x,y,z,w):
    wallface('V8 individual blue palace bricks','X',y,x-w/2,x+w/2,z,z+2,blue,.52,.23,.12)
    for zz in [z+.08,z+1.92]:box('V8 ivory frieze edge',(x,y-.08,zz),(w,.16,.13),buff,.02)
    for xx in range(math.ceil(x-w/2)+2,math.floor(x+w/2),4):
        relief_lion(xx,y-.13,z+.3,1.05)

# Processional Way: real lion relief panels at the gate's approach and palace.
for side in [-1,1]:
    for yy in [-24,-17,-10,10,18,25,40,48,56]:
        before=set(scene.objects)
        box('V8 lapis processional panel core',(0,0,1.35),(5,.5,2.7),blue[1],.06)
        frieze(0,-.27,.35,4.9)
        for xx in [-2.55,2.55]:
            box('V8 glazed boundary pilaster',(xx,0,1.6),(.5,.8,3.2),blue[3],.04)
            box('V8 boundary pilaster cap',(xx,0,3.23),(.7,.95,.2),buff,.03)
        par=group_new(before,'V8 processional lion wall',(side*8.1,yy,0))
        par.rotation_euler.z=-side*math.pi/2

# Royal palace: articulated wings around an open paved court, not a sealed box.
stage('processional_blue_walls_done')
clear_houses(-46,34,32,28)
box('V8 royal court foundation',(-46,34,.18),(33,30,.45),stone,.08)
for x,y,w,d,h in [(-59,34,6,28,11),(-33,34,6,28,11),(-46,46,26,5,13),(-56,21,12,4,10),(-36,21,12,4,10)]:
    box('V8 palace masonry',(x,y,h/2),(w,d,h),clay[3],.09)
    frieze(x,y-d/2-.05,h-2.7,w)
    for xx in [x-w/2+.5+i*2 for i in range(max(1,int(w/2)))]:
        box('V8 palace recessed pilaster',(xx,y-d/2-.14,h*.42),(.48,.35,h*.8),blue[2],.04)
    box('V8 palace ivory cornice',(x,y,h+.1),(w+.4,d+.4,.35),buff,.04)
    for xx in range(math.ceil(x-w/2),math.floor(x+w/2),2):
        brick('V8 palace stepped merlon',(xx,y-d/2,h+.75),(.7,.6,1.1),blue[2])
paving(-53,-39,25,43)
for xx in [-53,-39]:
    for yy in [27,33,39]:
        rod('V8 court timber column',(xx,yy,0),(xx,yy,5.5),.22,wood)
        box('V8 column blue base',(xx,yy,.4),(.65,.65,.8),blue[3],.04)
        box('V8 column capital',(xx,yy,5.6),(.85,.85,.25),buff,.04)
        pot(xx,yy+1,.1,.7)
canopy(-46,43,6,10,4,cloths[2])
paving(-29,-8,29.6,34.3)

# Separate hanging garden, a deliberate legendary reconstruction beside the palace.
stage('palace_done')
clear_houses(-51,83,39,39)
foliage_mesh=bpy.data.meshes.get('Individual garden leaves')
def shrub8(x,y,z,s=1,trail=False):
    ob=bpy.data.objects.new('V8 hanging garden foliage',foliage_mesh);scene.collection.objects.link(ob)
    ob.location=(x,y,z);ob.scale=(s,s,s);ob.rotation_euler.z=R.random()*math.tau
    if trail:ob.rotation_euler.x=2.4
for k in range(4):
    w=38-k*7;d=36-k*6;z=k*4.4;h=4.4
    box('V8 garden retaining tier',(-51,83,z+h/2),(w,d,h),clay[(k+1)%6],.09)
    box('V8 garden walkable terrace',(-51,83,z+h),(w+.5,d+.5,.28),stone,.05)
    frieze(-51,83-d/2-.12,z+.4,w)
    for xx in range(math.ceil(-51-w/2)+1,math.floor(-51+w/2),2):
        if not -56<xx<-46:shrub8(xx,83-d/2+.65,z+h+.2,1.25)
        if R.random()<.75 and not -56<xx<-46:shrub8(xx,83-d/2-.1,z+h-.15,.95,True)
    for yy in range(math.ceil(83-d/2)+1,math.floor(83+d/2),3):
        for xx in [-51-w/2+.7,-51+w/2-.7]:shrub8(xx,yy,z+h+.2,1.3)
    for xx in [-51-w/2+2,-51+w/2-2]:
        for yy in [83-d/2+2,83+d/2-2]:
            before=set(scene.objects);palm(xx,yy,4.5)
            for o in set(scene.objects)-before:o.location.z+=z+h
    # Solid switchback stairs stand on the lower terrace, with a landing onto
    # the next one. Each flight crosses the facade instead of floating forward.
    front=83-d/2;cy=front-1.5;n=22;run=.28;direction=1 if k%2==0 else -1
    startx=-54.08 if direction==1 else -47.92
    for j in range(n):
        height=(j+1)*h/n
        box('V8 supported garden stair',(startx+direction*(j+.5)*run,cy,z+height/2),(run+.015,1.6,height),stone,.018)
    endx=startx+direction*n*run
    box('V8 garden stair landing',(endx,front-.55,z+h-.12),(1.6,2,.24),stone,.025)
canopy(-51,83,22,8,7,linen)
for xx in [-55,-47]:rod('V8 garden pavilion post',(xx,80,17.7),(xx,80,22),.18,wood)

# Blue and ochre bands make the existing sacred precinct read at every scale.
stage('terraced_garden_done')
for k in range(7):
    w=52-6.25*k;d=48-5.6*k;z=.2+k*4.25
    wallface('V8 temple wide glazed course','X',82-d/2-.3,68-w/2,68+w/2,z+2.6,z+3.7,blue,.55,.23,.1)
    wallface('V8 temple western glazed course','Y',68-w/2-.3,82-d/2,82+d/2,z+2.6,z+3.7,blue,.55,.23,.1)
    box('V8 temple gold line',(68,82-d/2-.39,z+3.8),(w,.15,.15),ochre,.025)

# Sculpted royal and divine votive figures; layered robe, beard, headdress and staff.
def statue(kind):
    flush();before=set(scene.objects)
    box('V8 statue blue plinth',(0,0,.35),(1.65,1.5,.7),blue[2],.06)
    box('V8 statue inscribed pedestal',(0,0,.85),(1.35,1.25,.35),stone,.04)
    # Deliberately fluted skirt surface with a recognisable hem and belt.
    vs=[];fs=[];N=48
    for j in range(15):
        u=j/14;z=1.1+u*2.0;r=.57-.23*u
        for i in range(N):
            a=i/N*math.tau;rr=r+.018*math.cos(a*16)
            vs.append((rr*math.cos(a),rr*.72*math.sin(a),z))
    for j in range(14):
        for i in range(N):a=j*N+i;b=j*N+(i+1)%N;fs.append((a,b,b+N,a+N))
    objmesh('V8 carved robe pleats',vs,fs,gold)
    uvball('V8 sculpted royal torso',(0,0,3.2),(.5,.28,.65),gold,24)
    lathe('V8 engraved royal belt',(0,0,2.8),[(.4,0),(.42,.07),(.4,.14)],buff)
    uvball('V8 carved face',(0,-.02,3.98),(.25,.22,.35),gold,24)
    uvball('V8 sculpted nose',(0,-.24,3.99),(.055,.075,.11),gold,16)
    for side in [-1,1]:
        uvball('V8 brow ridge',(side*.105,-.218,4.07),(.09,.035,.032),gold,12)
        uvball('V8 inset obsidian eye',(side*.104,-.246,4.04),(.025,.012,.014),dark,12)
        uvball('V8 sculpted ear',(side*.26,0,3.99),(.05,.075,.1),gold,12)
        rod('V8 statue upper arm',(side*.4,0,3.52),(side*.52,-.08,3.08),.13,gold,.11)
        rod('V8 statue bent forearm',(side*.52,-.08,3.08),(side*.17,-.4,3.2),.11,gold,.075)
        uvball('V8 statue hand',(side*.17,-.4,3.2),(.09,.08,.13),gold,12)
    for row in range(7):
        for col in range(5):
            uvball('V8 carved curled beard',((col-2)*.085,-.23-row*.008,3.87-row*.085),(.051,.061,.055),gold,10)
    lathe('V8 royal cap',(0,0,4.17),[(.27,0),(.26,.23),(.22,.34),(.18,.38)],blue[1])
    uvball('V8 closed royal crown',(0,0,4.54),(.18,.18,.085),blue[1],24)
    for j in range(3):lathe('V8 diadem band',(0,0,4.18+j*.085),[(.275,0),(.28,.035)],buff)
    if kind=='divine':
        for side in [-1,1]:
            for j in range(3):
                curve('V8 divine horned crown',[(side*.21,-.01,4.22+j*.1),(side*.4,-.08,4.31+j*.1),(side*.29,-.05,4.5+j*.1)],.042,gold)
        rod('V8 divine staff',(.67,-.3,1.05),(.67,-.3,4.28),.045,gold)
        lathe('V8 staff ring',(.67,-.3,4.28),[(.12,0),(.14,.04),(.10,.09)],gold)
    else:
        rod('V8 royal sceptre',(.19,-.46,2.1),(.19,-.46,3.48),.045,gold)
    return instance_collection_from(before,'V8 '+kind+' statue module')
king=statue('royal');deity=statue('divine')
for pos,s in [((-4.8,-12,0),1.65),((-46,31,0),1.5)]:inst(king,'V8 royal monument',pos,s)
for pos,s in [((45,43,4.3),1.45),((59,43,4.3),1.45)]:inst(deity,'V8 divine monument',pos,s)

# Crowd uses linked detailed resident modules, with small groups and clear travel lanes.
stage('royal_and_divine_statues_done')
oldactors=[bpy.data.objects[n] for n in json.loads(scene['actor_names'])]
crowdcols=[]
for i in range(10):
    source=oldactors[i];head=next(o for o in source.children if o.name.startswith('Resident sculpted head'))
    origin=Vector((head.location.x,head.location.y,0))
    col=bpy.data.collections.new('V8 resident module '+str(i))
    for o in source.children:
        cp=o.copy();cp.parent=None;cp.location=o.location-origin;col.objects.link(cp)
    crowdcols.append(col)
newactors=[]
for i in range(230):
    if i<130:
        x=R.choice([-4.8,-3.6,2.7,4,5.2])+R.uniform(-.25,.25);y=R.uniform(8,100)
        span=78;axis='y';speed=R.choice([-1,1])*R.uniform(.65,1.1)
    elif i<190:
        x=R.choice([20.5,45.5])+R.uniform(-.5,.5);y=R.uniform(40,99);span=50;axis='y';speed=R.choice([-1,1])*.75
    else:
        x=R.uniform(-55,-38);y=R.uniform(26,42);span=0;axis='y';speed=0
    ob=inst(crowdcols[i%10],'V8 crowd actor',(x,y,0),R.uniform(.92,1.08),math.pi if speed<0 else 0)
    ob['base']=list(ob.location);ob['speed']=speed;ob['span']=span;ob['phase']=R.random()*6.28
    newactors.append(ob.name)

def animal(kind):
    before=set(scene.objects);m=fur[0 if kind=='donkey' else 1]
    uvball('V8 '+kind+' torso',(0,0,1.03),(.32,.68,.39),m)
    rod('V8 '+kind+' neck',(0,-.42,1.1),(0,-.62,1.59),.19,m,.14)
    uvball('V8 '+kind+' head',(0,-.73,1.62),(.17,.29,.19),m)
    uvball('V8 animal muzzle',(0,-.95,1.52),(.145,.15,.1),fur[3])
    for side in [-1,1]:
        for yy in [-.43,.45]:
            rod('V8 animal upper leg',(side*.23,yy,.96),(side*.25,yy+.06,.48),.075,m,.05)
            rod('V8 animal lower leg',(side*.25,yy+.06,.48),(side*.25,yy,.12),.048,m,.035)
            box('V8 animal hoof',(side*.25,yy-.025,.07),(.115,.19,.13),wood,.035)
        ear=uvball('V8 animal long ear',(side*.12,-.63,1.91),(.055,.075,.23 if kind=='donkey' else .1),m,12);ear.rotation_euler.y=side*.25
        uvball('V8 animal eye',(side*.158,-.78,1.65),(.02,.027,.025),dark,12)
    curve('V8 animal tail',[(0,.55,1.18),(0,.85,.83),(.1,.9,.55)],.03,m)
    if kind=='donkey':
        box('V8 woven saddle cloth',(0,.05,1.41),(.72,.7,.07),cloths[2],.04)
        for side in [-1,1]:
            box('V8 caravan pannier',(side*.4,.05,1.13),(.25,.55,.45),wood,.08)
            for yy in [-.12,.16]:pot(side*.41,yy,1.35,.24)
        curve('V8 donkey bridle',[(-.18,-.86,1.56),(0,-1.02,1.56),(.18,-.86,1.56)],.016,linen)
    else:
        for side in [-1,1]:curve('V8 goat horn',[(side*.1,-.56,1.75),(side*.14,-.44,1.94),(side*.15,-.27,1.88)],.038,wood)
    return instance_collection_from(before,'V8 '+kind+' module')
donkey=animal('donkey');goat=animal('goat');animals=[]
stage('crowd_and_animal_prototypes_done')
for i in range(18):
    ob=inst(donkey,'V8 moving pack donkey',(-.8 if i%2 else .6,15+i*3.9,0),.88,math.pi)
    ob['base']=list(ob.location);ob['speed']=1.25;ob['phase']=i*.6;animals.append(ob.name)
for i in range(16):
    ob=inst(goat,'V8 market goat',(R.uniform(2,5),R.uniform(62,75),0),R.uniform(.65,.85))
    ob['base']=list(ob.location);ob['speed']=.18;ob['phase']=i;animals.append(ob.name)

# More stalls and loaded quay platforms, clear of the bridge crossing at y=32.
for x,y in [(12,15),(12,42),(12,58),(12,72),(-11,45),(-11,61),(48,68),(48,87),(48,97)]:
    canopy(x,y,3.2,3.1,3.0,R.choice(cloths));market(x,y+.3)
    for k in range(5):
        box('V8 stacked cargo bale',(x-1+k*.5,y+1.5,.3+(.48 if k%2 else 0)),(.55,.45,.55),cloths[k%5],.08)
for yy in [45,68,91]:
    box('V8 merchant landing',(42.2,yy,.7),(3.1,6,.25),wood,.04)
    for q in range(8):pot(43+R.uniform(-.4,.4),yy-2+q*.5,.85,R.uniform(.5,.8))

# Shallow square-sailed merchants between bridges, plus mastless cargo barges.
flush()
boats=[]
for i,(x,y,s) in enumerate([(29,45,.65),(37,60,.7),(29,80,.65),(37,94,.6)]):
    before=set(scene.objects);boat(0,0,s);flush()
    for ob in list(set(scene.objects)-before):
        if ob.name.startswith(('Cream lateen','Sail edge rope')):bpy.data.objects.remove(ob,do_unlink=True)
    verts=[];faces=[]
    for j in range(9):
        for k in range(13):
            u=k/12;v=j/8;verts.append(((u-.5)*3.8*s,.15+.38*math.sin(math.pi*u)*math.sin(math.pi*v),2*s+v*2.7*s))
    for j in range(8):
        for k in range(12):n=j*13+k;faces.append((n,n+1,n+14,n+13))
    objmesh('V8 woven square sail',verts,faces,linen)
    rod('V8 yard',(-2*s,.15,4.7*s),(2*s,.15,4.7*s),.045,wood)
    par=group_new(before,'V8 animated merchant boat',(x,y,0));par['base']=list(par.location);par['phase']=i;par['speed']=(-1 if i%2 else 1)*.36
    boats.append(par.name)
flush()
scene['v8_crowd']=json.dumps(newactors);scene['v8_animals']=json.dumps(animals);scene['v8_boats']=json.dumps(boats)
stage('boats_and_all_geometry_done')
scene['city_version']='v8';scene['v8_scope']='Neo-Babylonian inspired fantasy royal city, garden attribution and statues are interpretive'
scene['v8_reliefs_face_street']=True
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.22
scene.view_settings.exposure=.3
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'babylon-city-v8.blend'))
(ROOT/'out/model-v8-evidence.json').write_text(json.dumps({'new_crowd':230,'existing_crowd':66,'pack_donkeys':18,'goats':16,'new_boats':4,'royal_statues':2,'divine_statues':2,'new_landmarks':['royal courtyard palace','separate terraced hanging garden','processional lion walls','broad ziggurat lapis courses','merchant quays'],'scope':'model created; appearance and motion pending actual render'},indent=2),encoding='utf8')
print('MODEL_V8_READY',flush=True)
