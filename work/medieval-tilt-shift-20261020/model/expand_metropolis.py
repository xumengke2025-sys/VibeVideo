"""Connect streets and extend an inhabited metropolis into atmospheric distance."""
import bpy,math,random,json,time
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent;R=random.Random(61904)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'babylon-city-v4.blend'))
scene=bpy.context.scene
def material(name,hex,rough=.85):
 m=bpy.data.materials.new(name);m.use_nodes=True
 rgb=[int(hex[i:i+2],16)/255 for i in (0,2,4)];col=[((x+.055)/1.055)**2.4 for x in rgb]
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough
 return m
clay=[bpy.data.materials['Sun dried brick '+str(i)] for i in range(6)]
stone=bpy.data.materials['Worn limestone'];wood=bpy.data.materials['Dark date palm timber'];dark=bpy.data.materials['Interior shade'];blue=bpy.data.materials['Indigo handwoven cloth']
palette=clay+[stone,wood,dark,blue,bpy.data.materials['Palm leaf'],bpy.data.materials['Natural flax canvas']]
def mesh_obj(name,vs,fs,mats,indices=None):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
 for m in mats:me.materials.append(m)
 if indices:
  for p,i in zip(me.polygons,indices):p.material_index=i
 ob=bpy.data.objects.new(name,me);scene.collection.objects.link(ob);return ob
def boxgeom(vs,fs,mi,pos,size,mat):
 x,y,z=pos;w,d,h=[q/2 for q in size];n=len(vs)
 vs.extend([(x+sx*w,y+sy*d,z+sz*h) for sx,sy,sz in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]])
 fs.extend([tuple(n+i for i in f) for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]]);mi.extend([mat]*6)
def box(name,pos,size,mat):
 vs=[];fs=[];mi=[];boxgeom(vs,fs,mi,pos,size,0);return mesh_obj(name,vs,fs,[mat])

# Clear a continuous 16m processional avenue. Existing handmade gate and market stay.
removed=[]
for ob in list(scene.objects):
 if ob.instance_type=='COLLECTION' and ob.location.y>36 and abs(ob.location.x)<13:
  removed.append(ob.name);bpy.data.objects.remove(ob,do_unlink=True);continue
 if ob.name.startswith('Distant inhabited courtyard') and 24<ob.location.x<47:
  bpy.data.objects.remove(ob,do_unlink=True)
for ob in list(scene.objects):
 if ob.instance_type=='COLLECTION' and ob.location.y>90 and any(abs(ob.location.y-y)<7.5 for y in [108,170,234]):
  bpy.data.objects.remove(ob,do_unlink=True)
# The original rear enceinte crossed the avenue. Open a real 10m gateway in it.
for ob in list(scene.objects):
 if ob.name.startswith(('Mudbrick enceinte','Wall coping')) and abs(ob.location.y-150)<.01:bpy.data.objects.remove(ob,do_unlink=True)
 elif ob.name.startswith('Engaged wall buttress') and abs(ob.location.y-148.57)<.1 and abs(ob.location.x)<5:bpy.data.objects.remove(ob,do_unlink=True)
 elif ob.type=='MESH' and ob.name.startswith(('Enceinte brick face','Enceinte crenel','Enceinte crenel cap')):
  me=ob.data;verts=[tuple(v.co) for v in me.vertices];faces=[]
  for p in me.polygons:
   c=p.center
   if 147<c.y<153 and abs(c.x)<5:continue
   faces.append(tuple(p.vertices))
  new=bpy.data.meshes.new('Open gateway courses');new.from_pydata(verts,[],faces)
  for m in me.materials:new.materials.append(m)
  ob.data=new
for x,w in [(-31,52),(14,18)]:
 box('Rear wall beside open avenue',(x,150,3),(w,2.5,6),clay[0]);box('Rear wall coping beside gateway',(x,150,6.1),(w,2.8,.26),stone)
box('Rear ceremonial gateway lintel',(0,150,6.25),(11,2.8,.8),bpy.data.materials['Lapis fired glaze 2'])
# A stone pavement shader continues the near-field geometric slabs without a hard stop.
paving=material('Continuous avenue worn limestone','b8ab91');ns=paving.node_tree.nodes;lk=paving.node_tree.links;bs=ns.get('Principled BSDF')
tex=ns.new('ShaderNodeTexCoord');brick=ns.new('ShaderNodeTexBrick');brick.inputs['Scale'].default_value=1.35;brick.inputs['Brick Width'].default_value=.85;brick.inputs['Row Height'].default_value=.65;brick.inputs['Mortar Size'].default_value=.018
brick.inputs['Color1'].default_value=(.43,.37,.27,1);brick.inputs['Color2'].default_value=(.52,.46,.35,1);brick.inputs['Mortar'].default_value=(.20,.19,.16,1);lk.new(tex.outputs['Object'],brick.inputs['Vector']);lk.new(brick.outputs['Color'],bs.inputs['Base Color'])
bump=ns.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.4;bump.inputs['Distance'].default_value=.025;lk.new(brick.outputs['Fac'],bump.inputs['Height']);lk.new(bump.outputs['Normal'],bs.inputs['Normal'])
box('Continuous processional avenue',(0,990,.035),(16,1620,.018),paving)
# Continue the exact original stone courses through the entire close-view street.
vs=[];fs=[];mi=[]
for row in range(87,303):
 y=-23+(row+.5)*.67
 for k in range(20):
  x=-8+(k+.5)*.85+(row%2)*.42
  if x<8:boxgeom(vs,fs,mi,(x,y,-.035+R.uniform(-.01,.01)),(.82,.64,.13),0)
mesh_obj('Continuous near avenue individual stone slabs',vs,fs,[stone],mi)
for x in [20.7,45.2]:box('Continuous riverside walk',(x,895,.045),(3.6,1810,.02),paving)
crossings=[32,108,170,234]+list(range(310,1800,76))
for y in crossings:
  box('West connected cross street',(-316,y,.027),(656,4 if y==32 else 5.5,.015),paving)
 box('East connected cross street',(345,y,.027),(602,4 if y==32 else 5.5,.015),paving)
water=bpy.data.objects['Canal surface'];water.scale.y=1;water.dimensions.y=1900;water.location.y=850
for name in ['North canal retaining bank','East canal bank']:
 ob=bpy.data.objects[name];ob.location.y=910;ob.dimensions.y=1820
for x in [23.6,41.7]:box('Long canal coping',(x,900,.92),(1,1810,.22),stone)

# Real courtyard solids, roof parapets, setbacks and doors in 18 batched far-city families.
protos=[]
for k in range(18):
 vs=[];fs=[];mi=[];w=R.uniform(7.2,9.1);d=R.uniform(7,9);h=R.uniform(4.5,8.2)
 for x in [-w*.38,w*.38]:boxgeom(vs,fs,mi,(x,0,h/2),(w*.24,d,h),k%6)
 boxgeom(vs,fs,mi,(0,d*.37,h/2),(w,d*.26,h),(k+1)%6)
 for x in [-w*.3,w*.3]:boxgeom(vs,fs,mi,(x,-d*.4,h/2),(w*.36,d*.2,h),(k+2)%6)
 boxgeom(vs,fs,mi,(0,-d*.4,(h+2.5)/2),(w*.24,d*.2,h-2.5),(k+2)%6)
 for x in [-w/2,w/2]:boxgeom(vs,fs,mi,(x,0,h+.25),(.22,d,.5),(k+1)%6)
 for y in [-d/2,d/2]:boxgeom(vs,fs,mi,(0,y,h+.25),(w,.22,.5),(k+1)%6)
 if k%3!=0:
  boxgeom(vs,fs,mi,(-w*.28,d*.23,h+1.2),(w*.4,d*.42,2.4),(k+3)%6)
  boxgeom(vs,fs,mi,(-w*.28,d*.012,h+1.4),(.5,.05,.7),8)
 for j in range(5):boxgeom(vs,fs,mi,(0,-d*.3+j*d*.15,h-.06),(w+.2,.12,.16),7)
 if k%2:boxgeom(vs,fs,mi,(0,-d*.5-.7,2.65),(w*.7,1.5,.05),9 if k%4 else 11)
 for x in [-w*.32,w*.32]:boxgeom(vs,fs,mi,(x,-d*.501,h*.65),(.5,.035,.7),8)
 ob=mesh_obj('Metropolis courtyard prototype '+str(k),vs,fs,palette,mi);protos.append(ob.data);bpy.data.objects.remove(ob,do_unlink=True)
placed=0
for iy,y0 in enumerate(range(-29,1801,12)):
 for ix,x0 in enumerate(range(-650,651,12)):
  if -116<x0<119 and 140<=y0<303:continue
  if -59<x0<98 and y0<140:continue
  if abs(x0)<15 or 18<x0<51:continue
  if any(abs(y0-y)<8 for y in crossings):continue
  # Long north/south side streets stay clear and join every transverse street.
  if any(abs(x0-x)<6.5 for x in [-510,-358,-206,160,312,464,616]):continue
  if any(math.hypot(x0-x,y0-y)<29 for x,y in [(-250,420),(220,620),(-320,1100),(315,1390)]):continue
  ob=bpy.data.objects.new('Metropolis courtyard',R.choice(protos));scene.collection.objects.link(ob);ob.location=(x0+R.uniform(-.9,.9),y0+R.uniform(-.8,.8),0);ob.rotation_euler.z=R.choice([0,math.pi/2,math.pi,math.pi*1.5])+R.uniform(-.03,.03);ob.scale=(R.uniform(.88,1.10),R.uniform(.9,1.1),R.uniform(.85,1.3));placed+=1
print('METROPOLIS_COURTYARDS',placed,flush=True)
for x in [-510,-358,-206,160,312,464,616]:box('Connected longitudinal side street',(x,890,.025),(5.5,1820,.015),paving)

# Secondary sacred compounds interrupt repetition and establish city districts.
for x,y in [(-250,420),(220,620),(-320,1100),(315,1390)]:
 for k in range(4):
  w=36-k*6;z=k*4.5
  box('Distant sacred precinct',(x,y,z+2.25),(w,w,4.5),clay[k%6]);box('Precinct blue cornice',(x,y,z+4.5),(w+.3,w+.3,.32),palette[9])
 box('Distant shrine',(x,y,20.4),(9,9,4.8),bpy.data.materials['Lapis fired glaze 2'])

# Low-detail palms have bent fronds, used only outside the detailed core.
vs=[];fs=[];mi=[];boxgeom(vs,fs,mi,(0,0,3.1),(.18,.18,6.2),7)
for j in range(14):
 a=j*math.tau/14
 for k in range(5):
  u=k/5;v=(k+1)/5;L=3.2;w=.38*math.sin((u+.1)*math.pi);n=len(vs)
  for q,s in [(u,-1),(u,1),(v,1),(v,-1)]:vs.append((math.cos(a)*L*q-math.sin(a)*w*s,math.sin(a)*L*q+math.cos(a)*w*s,6.2+1.2*math.sin(q*2.8)-q*.8))
  fs.append((n,n+1,n+2,n+3));mi.append(10)
ob=mesh_obj('Distant palm prototype',vs,fs,palette,mi);palmdata=ob.data;bpy.data.objects.remove(ob,do_unlink=True)
for ob in list(scene.objects):
 if ob.name.startswith('Metropolis courtyard') and R.random()<.24:
  p=bpy.data.objects.new('Distant neighbourhood palm',palmdata);scene.collection.objects.link(p);p.location=ob.location+Vector((4.8,3.8,0));s=R.uniform(.9,1.5);p.scale=(s,s,s);p.rotation_euler.z=R.random()*6.28

# Distant crossings connect both sides of the river. Curved intrados remains an opening.
for y in crossings[2:]:
 vs=[];fs=[];mi=[];N=20
 for i in range(N):
  u=(i+.5)/N;x=23+20*u;z=1.2+2*math.sin(u*math.pi)
  boxgeom(vs,fs,mi,(x,y,z),(1.02,5.5,.45),6)
  for side in [-1,1]:boxgeom(vs,fs,mi,(x,y+side*2.6,z+.5),(1.02,.3,.7),1)
 mesh_obj('Distant connected arched bridge',vs,fs,palette,mi)

# Move terrain well beyond the city, eliminating a visibly finite tabletop edge.
hill=bpy.data.objects['Distant alluvial hills']
for v in hill.data.vertices:
 x,y=v.co.x,v.co.y;v.co.x*=3;v.co.y=1900+(y-295)*2.5;v.co.z=-.35+(18+50*(.5+.5*math.sin(x*.007+y*.004)))*min(1,(y-295)/100)
scene['metropolis_courtyard_count']=placed;scene['connected_streets']='central avenue 1800m; 1900m canal; continuous quay walks; cross streets and bridges; lateral avenues'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'babylon-city-v5.blend'))
(ROOT/'out/metropolis-v5-evidence.json').write_text(json.dumps({'detailed_core':'v4','additional_courtyards':placed,'city_extent_m':[-650,650,-29,1800],'avenue_width_m':16,'canal_length_m':1900,'cross_street_y':crossings,'removed_avenue_obstructions':removed,'verification':'geometry construction only; camera and rendered street continuity pending'},indent=2),encoding='utf8')
