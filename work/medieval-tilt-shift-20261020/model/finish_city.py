"""City v4: original geometry, coherent garden/street dressing and cinematic light.
Run with Blender 4.5 background. Preserve every earlier model.
"""
import bpy,math,random,json,ast,time
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.geometry import tessellate_polygon
from collections import defaultdict
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'out';R=random.Random(441902)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'babylon-city-v3.blend'))
scene=bpy.context.scene
# Reuse only the original geometry helper definitions, not the scene reset/build.
tree=ast.parse((ROOT/'build_city.py').read_text(encoding='utf8'))
linen=bpy.data.materials['Natural flax canvas']
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'geometry_helpers','exec'))
blue=[bpy.data.materials['Lapis fired glaze '+str(i)] for i in range(8)]
clay=[bpy.data.materials['Sun dried brick '+str(i)] for i in range(6)]
stone=bpy.data.materials['Worn limestone'];wood=bpy.data.materials['Dark date palm timber'];linen=bpy.data.materials['Natural flax canvas'];potmat=bpy.data.materials['Hand fired terracotta'];leafmat=bpy.data.materials['Palm leaf'];leaflight=bpy.data.materials['Palm young leaf'];sand=bpy.data.materials['Alluvial sand'];buff=bpy.data.materials['Ivory glazed relief'];ochre=bpy.data.materials['Ochre glazed accent'];dark=bpy.data.materials['Interior shade'];redcloth=bpy.data.materials['Madder dyed fabric']
batch=defaultdict(lambda:[[],[]]);counts=defaultdict(int)
bpy.ops.mesh.primitive_cube_add(size=1);proto=bpy.context.object;be=proto.modifiers.new('Soft edges','BEVEL');be.width=.045;be.segments=2;bpy.ops.object.modifier_apply(modifier=be.name);pv=[v.co.copy() for v in proto.data.vertices];pf=[tuple(p.vertices) for p in proto.data.polygons];bpy.data.objects.remove(proto,do_unlink=True)
cloths=[linen,redcloth,textured('Indigo handwoven cloth','3d6370',.91),textured('Saffron handwoven cloth','b98d53',.94),textured('Faded sage cloth','7e8871',.96)]
greens=[surface('Garden foliage '+str(i),c,.81) for i,c in enumerate(['354b2c','596839','647744','405f3b','7e8651'])]
flower=surface('Small warm flowers','bea175',.8)

# Twelve courtyard families. Roof silhouette, wall colour and activity vary independently.
sources=[bpy.data.collections['Courtyard house module '+str(i)] for i in range(3)]
variants=[]
for i in range(12):
 src=sources[i%3];coll=bpy.data.collections.new('Varied inhabited block '+str(i));variants.append(coll)
 for ob in src.objects:
  if ob.name.startswith(('Pot /','Ceramic loop','Roof exposed')) and R.random()<.62:continue
  cp=ob.copy();coll.objects.link(cp)
  if cp.type=='MESH' and any(m and m.name.startswith('Sun dried') for m in cp.data.materials):
   cp.data=cp.data.copy()
   for k,m in enumerate(cp.data.materials):
    if m and m.name.startswith('Sun dried'):cp.data.materials[k]=clay[(i+k)%6]
 before=set(scene.objects);h=5.2+(i%3)*.8;w=7.5+(i%3)*.6;d=7.5+(i%3)*.5
 if i%4 in [0,1]:
  box('Roof sleeping chamber',(-w*.26,d*.22,h+1.15),(w*.39,d*.39,2.3),clay[(i+2)%6],.1)
  box('Roof room deep window',(-w*.26,d*.02-.03,h+1.3),(.48,.13,.72),dark,.02)
  box('Roof room sill',(-w*.26,d*.02-.15,h+.9),(.8,.35,.12),stone,.025)
 if i%4==2:canopy(0,0,h+1.4,w*.57,d*.5,cloths[i%5])
 if i%3==0:
  ob=box('Woven rooftop drying rug',(w*.31,-d*.15,h+.035),(w*.19,d*.35,.025),cloths[(i+2)%5],.02);ob.rotation_euler.z=.08
 if i%3==1:
  for k in range(6):rod('Bundled reed rolls',(w*.28,-2+k*.5,h+.12),(w*.28+.65,-2+k*.5,h+.12),.12,linen)
 flush()
 for ob in set(scene.objects)-before:
  for c in list(ob.users_collection):c.objects.unlink(ob)
  coll.objects.link(ob)
for ob in scene.objects:
 if ob.instance_type=='COLLECTION' and ob.instance_collection in sources:
  ob.instance_collection=R.choice(variants)
  if ob.name.startswith('Distant inhabited'):ob.location.x+=R.uniform(-.6,.6);ob.location.y+=R.uniform(-.5,.5)

# A compact leafy bush is made of actual folded leaves and branches, not smooth spheres.
vv=[];ff=[];mi=[]
for j in range(340):
 a=R.random()*math.tau;r=R.random()**.48;z=R.uniform(.08,1.05)*(1-.4*r)
 center=Vector((math.cos(a)*r*.65,math.sin(a)*r*.65,z));sz=R.uniform(.07,.17);u=Vector((math.cos(a),math.sin(a),R.uniform(-.4,.5)))*sz;v=Vector((-math.sin(a),math.cos(a),.3))*sz*.4;n=len(vv)
 vv.extend([tuple(center-u),tuple(center+v),tuple(center+u),tuple(center-v),tuple(center+Vector((0,0,.025)))]);ff.extend([(n,n+1,n+4),(n+1,n+2,n+4),(n+2,n+3,n+4),(n+3,n,n+4)]);mi.extend([R.randrange(5)]*4)
me=bpy.data.meshes.new('Individual garden leaves');me.from_pydata(vv,[],ff)
for m in greens:me.materials.append(m)
for p,m in zip(me.polygons,mi):p.material_index=m
def shrub(x,y,z,s=1,trail=False):
 ob=bpy.data.objects.new('Terrace foliage' if not trail else 'Trailing garden foliage',me);scene.collection.objects.link(ob);ob.location=(x,y,z);ob.rotation_euler.z=R.random()*math.tau;ob.scale=(s,s,s*R.uniform(.8,1.3))
 if trail:ob.rotation_euler.x=math.pi*.8
 return ob
for k in range(6):
 w=52-6.25*k;d=48-5.6*k;z=.2+(k+1)*4.25+.2
 for x in [68-w/2+1.15+i*1.5 for i in range(int((w-2.3)/1.5)+1)]:
  if abs(x-68)<2.8:continue
  shrub(x,82-d/2+1,z,R.uniform(.75,1.15))
  if R.random()<.6:shrub(x,82-d/2-.2,z,R.uniform(.6,.95),True)
 for y in [82-d/2+2.5+i*1.6 for i in range(int((d-5)/1.6)+1)]:
  shrub(68-w/2+1,y,z,R.uniform(.8,1.2))
  if R.random()<.5:shrub(68-w/2-.05,y,z,.7,True)
 # Airier upper-level palm silhouettes.
 if k in [0,2,4]:
  for side in [-1,1]:
   before=set(scene.objects);palm(68+side*(w/2-1.6),82-d/2+1.5,R.uniform(3.4,4.7))
   for o in set(scene.objects)-before:o.location.z+=z
# Plantings follow the quays and irregular roof courts.
for y in range(-14,143,7):
 for x in [22,44]:
  if abs(y-32)<5 or abs(y-108)<5:continue
  for n in range(3):shrub(x+R.uniform(-.4,.4),y+n*.7,.1,R.uniform(.65,1.0))
for x,y,h in [(-34,25,10),(-17,44,10),(-41,65,9),(-18,77,10),(6,53,9),(-3,122,12),(60,22,10),(79,30,11),(-36,-19,10),(11,-24,8),(-48,105,11)]:palm(x,y,h)
for ob in list(scene.objects):
 if ob.instance_type=='COLLECTION' and ob.instance_collection in variants and ob.location.y<150 and R.random()<.48:
  shrub(ob.location.x+R.uniform(-2,2),ob.location.y+R.uniform(-2,2),R.uniform(5.9,7.6)*ob.scale.z,1.6)

# Populated market fronts, low stalls, cloth drying lines and stacked provisions.
for x,y,w,d in [(-9,18,3.6,3.3),(9,24,3.2,3),(-9,30,3.3,3),(18,49,3.5,3.4),(-5,50,4,3.5),(17,76,3.2,3),(-21,39,4.2,3),(47,14,3.2,4),(-8,-17,3,2.5)]:
 canopy(x,y,3.05,w,d,R.choice(cloths));market(x,y+.45)
 for i in range(3):
  box('Woven goods bale',(x+R.uniform(-1,1),y+1.7,.28),(.6,.45,.55),R.choice(cloths),.09)
for x,y,z in [(-14,13,6.5),(13,28,6.9),(-25,30,6.6),(-24,17,7.5)]:
 for i in range(3):
  ob=box('Folded dyed textiles',(x+R.uniform(-1,1),y+R.uniform(-1,1),z+.05+i*.08),(.85,1.2,.07),cloths[(i+2)%5],.02);ob.rotation_euler.z=R.random()*.3

# Shrine west wall now shares the physical glaze and framed architectural detail.
wallface('Sanctuary west blue bricks','Y',62.66,77.3,86.5,30.2,36.1,blue,.5,.23,.1)
for yy in [78.2,80.3,82.4,84.5,86]:
 box('Shrine west golden pilaster',(62.52,yy,33.1),(.17,.16,5.8),buff,.03)
for z in [30.5,35.6]:box('Shrine lapis relief border',(62.46,82,z),(.15,9.3,.18),ochre,.025)

# Low hills close the bare artificial horizon; foreground ridge produces real occlusion.
def terrain(name,y0,y1,zfunc,mat):
 vs=[];fs=[];nx=100;ny=24
 for j in range(ny+1):
  y=y0+(y1-y0)*j/ny
  for i in range(nx+1):
   x=-700+1400*i/nx;vs.append((x,y,zfunc(x,y)))
 for j in range(ny):
  for i in range(nx):n=j*(nx+1)+i;fs.append((n,n+1,n+nx+2,n+nx+1))
 ob=objmesh(name,vs,fs,mat)
 for p in ob.data.polygons:p.use_smooth=True
 return ob
terrain('Distant alluvial hills',295,1000,lambda x,y: -.35+(3+24*(.5+.5*math.sin(x*.009+y*.004))+10*math.sin(x*.018+y*.011)**2)*min(1,(y-295)/100),sand)
terrain('Opening dune ridge',-215,-65,lambda x,y: -1+9*math.exp(-((y+117)/18)**2)*(1+.13*math.sin(x*.045))+.25*math.sin(x*.1+y*.07),sand)

# Original linen residents. Hierarchy retains inspectable gait parts for deterministic motion.
actors=[]
skin=surface('Sunlit warm skin','9c7554',.84)
for i in range(66):
 if i<30:x=R.uniform(-6,6);y=R.uniform(-21,53)
 elif i<50:x=R.choice([21,45])+R.uniform(-1,1);y=R.uniform(7,130)
 else:x=R.uniform(-40,17);y=R.uniform(44,120)
 before=set(scene.objects);m=cloths[i%5];h=R.uniform(.93,1.1)
 rod('Resident robe',(x,y,.38*h),(x,y,1.28*h),.25*h,m,.14*h)
 uvball('Resident sculpted head',(x,y,1.49*h),(.115*h,.13*h,.16*h),skin,16)
 uvball('Resident head wrap',(x,y,1.61*h),(.15*h,.15*h,.07*h),linen,16)
 for side in [-1,1]:
  rod('Resident arm',(x+side*.14*h,y,1.22*h),(x+side*.25*h,y-.04,.74*h),.065*h,m,.045*h)
  leg=rod('Walking leg '+str(side),(x+side*.09*h,y,.06),(x+side*.09*h,y,.49*h),.045*h,skin)
  box('Leather sandal',(x+side*.09*h,y-.04,.07),(.12,.24,.09),wood,.025)
 if i%4==0:lathe('Carried produce basket',(x+.31,y,.76),[(.12,0),(.19,.22),(.20,.25)],wood)
 new=set(scene.objects)-before;par=bpy.data.objects.new('Animated resident '+str(i),None);scene.collection.objects.link(par)
 for ob in new:ob.parent=par
 par['phase']=R.random()*6.28;par['speed']=R.uniform(.12,.25);par['base_y']=y;par['walk']=i<50;actors.append(par.name)

# A fourth boat travels only inside the two bridges, so it never collides with their arches.
before=set(scene.objects);boat(34,87,.82);parts=set(scene.objects)-before
par=bpy.data.objects.new('Animated canal boat',None);scene.collection.objects.link(par)
for ob in parts:ob.parent=par
flush()

# Balance the warm key with a cool, readable sky fill. Keep microrelief subtle.
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.18
sun=bpy.data.objects['Warm late afternoon key'];sun.data.energy=2.8;sun.data.color=(1,.87,.66);sun.data.angle=math.radians(2.0);sun.rotation_euler=(math.radians(59),math.radians(-18),math.radians(-32))
scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.1
for mat in bpy.data.materials:
 if mat.use_nodes:
  for n in mat.node_tree.nodes:
   if n.type=='BUMP' and mat.name.startswith(('Sun dried','Worn','Alluvial')):n.inputs['Strength'].default_value=.22
scene.cycles.samples=48;scene.cycles.adaptive_threshold=.06;scene.cycles.use_denoising=True;scene.cycles.use_persistent_data=True
scene.render.resolution_percentage=100;scene.render.image_settings.color_mode='RGB'
scene['city_version']='v4';scene['actor_names']=json.dumps(actors);scene['scope']='Babylonian fantasy city streets; no dragon'
cam=scene.camera;cam.data.dof.use_dof=False
camera((-48,-104,83),(19,45,9),58)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'babylon-city-v4.blend'))
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
scene.cycles.device='GPU'
for label,pos,target,lens in [('city-overview',(-48,-104,83),(19,45,9),58),('market-street',(24,-30,25),(0,19,5),46),('canal-gardens',(1,20,39),(52,75,15),44)]:
 camera(pos,target,lens);scene.render.filepath=str(OUT/(label+'-v4.png'));bpy.ops.render.render(write_still=True);print('PROOF_READY',label,flush=True)
(OUT/'model-v4-evidence.json').write_text(json.dumps({'model':'babylon-city-v4.blend','resolution':[1080,1920],'dof':False,'variants':12,'actors':66,'scope':'model stills; final animation not yet validated'},indent=2),encoding='utf8')
