"""V14: water contact, regional detail and an explicit offering handover."""
import bpy,ast,json,math,random
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent;ROOT=P.parent
bpy.ops.wm.open_mainfile(filepath=str(P/'babylon-city-v13.blend'))
scene=bpy.context.scene;R=random.Random(2026102214)
for file,names in [('build_city.py',{'srgb','color','node','surface','textured'}),('revise_city_v12.py',{'Mesh'})]:
 tree=ast.parse((P/file).read_text(encoding='utf8'))
 exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in names],type_ignores=[]),file,'exec'))
M=bpy.data.materials
skin=M['Sunlit warm skin'];linen=M['V12 ritual linen'];blue=M['Indigo handwoven cloth'];wood=M['Dark date palm timber'];gold=M['V12 chased warm bronze'];dark=M['Interior shade'];stone=M['Worn limestone'];potmat=M['Hand fired terracotta'];leather=M['V12 dark leather']
def log(s):print('V14_BUILD',s,flush=True)
def node_math(nt,op,a,b=None):
 n=nt.nodes.new('ShaderNodeMath');n.operation=op
 for i,x in enumerate([a,b]):
  if x is None:continue
  if isinstance(x,(float,int)):n.inputs[i].default_value=x
  else:nt.links.new(x,n.inputs[i])
 return n.outputs[0]

# Slow broad current under smaller anisotropic waves, rather than a uniform fill.
water=M['Canal water / rippled reflection'];nt=water.node_tree;p=nt.nodes.get('Principled BSDF')
p.inputs['Base Color'].default_value=color('345d60');p.inputs['Metallic'].default_value=.06;p.inputs['Roughness'].default_value=.21;p.inputs['Transmission Weight'].default_value=.10
tc=nt.nodes.new('ShaderNodeNewGeometry');mapping=nt.nodes.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(1,.45,1);nt.links.new(tc.outputs['Position'],mapping.inputs[0])
fine_noise=next(n for n in nt.nodes if n.type=='TEX_NOISE');nt.links.new(tc.outputs['Position'],fine_noise.inputs['Vector'])
flow=nt.nodes.new('ShaderNodeTexNoise');flow.name='V14 long current';flow.noise_dimensions='4D';flow.inputs['Scale'].default_value=.65;flow.inputs['Detail'].default_value=2;nt.links.new(mapping.outputs[0],flow.inputs['Vector'])
coarse=nt.nodes.new('ShaderNodeBump');coarse.inputs['Strength'].default_value=.28;coarse.inputs['Distance'].default_value=.09;nt.links.new(flow.outputs['Fac'],coarse.inputs['Height'])
oldb=next(n for n in nt.nodes if n.type=='BUMP' and n!=coarse);oldb.inputs['Strength'].default_value=.24;oldb.inputs['Distance'].default_value=.045;nt.links.new(coarse.outputs['Normal'],oldb.inputs['Normal'])
ram=nt.nodes.new('ShaderNodeValToRGB');ram.color_ramp.elements[0].position=.14;ram.color_ramp.elements[0].color=color('24484d');ram.color_ramp.elements[1].position=.88;ram.color_ramp.elements[1].color=color('426c6c');nt.links.new(flow.outputs['Fac'],ram.inputs[0]);nt.links.new(ram.outputs[0],p.inputs['Base Color'])
rough=nt.nodes.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.17;rough.inputs['To Max'].default_value=.29;nt.links.new(flow.outputs['Fac'],rough.inputs['Value']);nt.links.new(rough.outputs[0],p.inputs['Roughness'])

# Localized quay wetting, preserving dry upper pavements and non-quay buildings.
wet={}
for ob in list(scene.objects):
 if ob.type!='MESH' or not any(k in ob.name.lower() for k in ['quay retaining','continuous quay','canal retaining','quay cap']):continue
 ob.data=ob.data.copy()
 for i,mat in enumerate(ob.data.materials):
  if mat.name not in wet:
   cp=mat.copy();cp.name='V14 damp '+mat.name;tn=cp.node_tree;bs=tn.nodes.get('Principled BSDF')
   geo=tn.nodes.new('ShaderNodeNewGeometry');sep=tn.nodes.new('ShaderNodeSeparateXYZ');tn.links.new(geo.outputs['Position'],sep.inputs[0])
   h=node_math(tn,'SUBTRACT',.83,sep.outputs['Z']);h=node_math(tn,'MULTIPLY',h,1.4);h=node_math(tn,'MAXIMUM',h,0);h=node_math(tn,'MINIMUM',h,.65)
   mix=tn.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[2].default_value=(.45,.52,.46,1)
   if bs.inputs['Base Color'].is_linked:tn.links.new(bs.inputs['Base Color'].links[0].from_socket,mix.inputs[1])
   else:mix.inputs[1].default_value=bs.inputs['Base Color'].default_value
   tn.links.new(h,mix.inputs[0]);tn.links.new(mix.outputs[0],bs.inputs['Base Color']);wet[mat.name]=cp
  ob.data.materials[i]=wet[mat.name]

# Subtle per-building firing/weather variation; preserve the established palette.
for mat in [m for m in list(M) if m.name.startswith('Sun dried brick')]:
 tn=mat.node_tree;bs=tn.nodes.get('Principled BSDF');oi=tn.nodes.new('ShaderNodeObjectInfo');mp=tn.nodes.new('ShaderNodeMapRange');mp.inputs['To Min'].default_value=.84;mp.inputs['To Max'].default_value=1.09;tn.links.new(oi.outputs['Random'],mp.inputs['Value'])
 mix=tn.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.65;tn.links.new(bs.inputs['Base Color'].links[0].from_socket,mix.inputs[1]);tn.links.new(mp.outputs[0],mix.inputs[2]);tn.links.new(mix.outputs[0],bs.inputs['Base Color'])
log('water_and_materials')

# Quiet wake ribbons are separate geometry above the water, attached by animation.
wake_mat=bpy.data.materials.new('V14 soft reflective wake');wake_mat.use_nodes=True
wn=wake_mat.node_tree;wn.nodes.clear();out=wn.nodes.new('ShaderNodeOutputMaterial');mix=wn.nodes.new('ShaderNodeMixShader');mix.inputs[0].default_value=.20;trans=wn.nodes.new('ShaderNodeBsdfTransparent');bs=wn.nodes.new('ShaderNodeBsdfPrincipled');bs.inputs['Base Color'].default_value=color('679393');bs.inputs['Roughness'].default_value=.30
wn.links.new(trans.outputs[0],mix.inputs[1]);wn.links.new(bs.outputs[0],mix.inputs[2]);wn.links.new(mix.outputs[0],out.inputs[0])
boats=[bpy.data.objects[n] for n in json.loads(scene['v8_boats'])]+[bpy.data.objects['Animated canal boat']]
wakes=[]
for idx,boat in enumerate(boats):
 hull=next((o for o in boat.children if 'Carvel wooden' in o.name or 'hull' in o.name.lower()),None)
 if hull is None:
  hull=next((o for o in boat.children if o.type=='MESH'),None)
 if hull:
  corners=[boat.matrix_world.inverted()@hull.matrix_world@Vector(v) for v in hull.bound_box]
  lo=Vector(tuple(min(v[k] for v in corners) for k in range(3)));hi=Vector(tuple(max(v[k] for v in corners) for k in range(3)))
  cx,cy=(lo.x+hi.x)/2,(lo.y+hi.y)/2;half=max(.8,(hi.y-lo.y)/2);width=max(.4,(hi.x-lo.x)/2)
 else:cx,cy,half,width=0,0,2.8,.8
 mesh=Mesh()
 for side in [-1,1]:
  for trail in range(3):
   vs=[];fs=[]
   for j in range(33):
    u=j/32;yy=half*.60-u*(half*1.7+3.0);xx=side*(width*(.40+.60*math.sin(min(1,u*2)*math.pi/2))+u*u*(.65+trail*.35))
    w=(.065+.045*trail)*math.sin(math.pi*u)**.7
    for off in [-w,w]:vs.append((xx+off,yy,.002*trail))
   fs=[(j*2,j*2+1,j*2+3,j*2+2) for j in range(32)];mesh.add(vs,fs,wake_mat)
 wake=mesh.bake('V14 moving wake '+str(idx));wakes.append({'name':wake.name,'boat':boat.name,'center':[cx,cy,0],'half':half,'index':idx})
scene['v14_wakes']=json.dumps(wakes)

# Selected roof props are anchored by ray casting to real roofs, not empty courtyards.
deps=bpy.context.evaluated_depsgraph_get();decor=Mesh();roof_sites=[]
houses=[o for o in scene.objects if o.type=='MESH' and o.name.startswith('Metropolis courtyard') and abs(o.location.x)<230 and -10<o.location.y<430]
R.shuffle(houses)
for ob in houses[:95]:
 corners=[ob.matrix_world@Vector(v) for v in ob.bound_box];low=Vector(tuple(min(v[k] for v in corners) for k in range(3)));high=Vector(tuple(max(v[k] for v in corners) for k in range(3)))
 x=low.x+(high.x-low.x)*.18;y=low.y+(high.y-low.y)*.43
 hit,loc,norm,face,found,_=scene.ray_cast(deps,Vector((x,y,high.z+3)),Vector((0,0,-1)),distance=20)
 if not hit or norm.z<.8 or found.original!=ob:continue
 z=loc.z+.025;roof_sites.append([x,y,z]);v=R.randrange(3)
 if v==0:
  for j in range(3):decor.ring((x+j*.36,y,z),[(.13,0),(.23,.18),(.20,.42),(.10,.51),(.12,.54)],potmat,12)
 elif v==1:
  for j in range(5):decor.rod((x-.3,y-.5+j*.20,z+.12),(x+.45,y-.5+j*.20,z+.12),.08,wood,n=8)
  decor.box((x+.1,y,z+.24),(1.1,1.35,.09),M['Natural flax canvas'])
 else:
  for dx in [-.48,.48]:
   for dy in [-.65,.65]:decor.rod((x+dx,y+dy,z),(x+dx,y+dy,z+1.15),.035,wood,n=6)
  decor.add([(x-.55,y-.72,z+1.15),(x+.55,y-.72,z+1.15),(x+.55,y+.72,z+1.15),(x-.55,y+.72,z+1.15),(x,y,z+1.03)],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],M['Madder dyed fabric'] if x<0 else M['Natural flax canvas'])
decor.bake('V14 regional roof life')

# Organic variation stays within existing planted margins.
for ob in scene.objects:
 if ob.name.startswith(('V8 hanging garden foliage','Trailing garden foliage','Terrace foliage')):
  ob.scale.x*=R.uniform(.76,1.18);ob.scale.y*=R.uniform(.82,1.18);ob.scale.z*=R.uniform(.8,1.30);ob.location.x+=R.uniform(-.13,.13);ob.location.y+=R.uniform(-.1,.1)
garden=Mesh()
for k in range(4):
 w=38-k*7;z=(k+1)*4.4+.15;x=-51-w/2+1.5
 for y in [77.4,87.8]:
  garden.ring((x,y,z),[(.28,0),(.43,.36),(.36,.72),(.25,.79),(.29,.82)],potmat,16)
  garden.box((x+.58,y+1.25,z+.40),(.80,1.8,.13),wood)
  for yy in [y+.6,y+1.9]:garden.box((x+.58,yy,z+.19),(.6,.18,.38),stone)
garden.bake('V14 terrace vessels and benches')
log('roof_and_garden_details')

# Two readable articulated ceremonial figures, persistent tray, and offering altar.
special=json.loads(scene['v12_special']);removed={'V12 priest event 19','V12 priest event 20'}
for name in removed:bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)
scene['v12_special']=json.dumps([e for e in special if e['name'] not in removed])
rigs=[]
for i in range(2):
 root=bpy.data.objects.new('V14 offering '+str(i),None);scene.collection.objects.link(root)
 body=Mesh();body.ring((0,0,.15),[(.30,0),(.28,.42),(.22,1.1)],linen,28,.8);body.ball((0,0,1.19),(.23,.15,.25),linen,20)
 # Light folds, sash and distinct collars improve only these foreground figures.
 for j in range(9):
  a=(j-4)*.19;body.rod((.22*math.sin(a),-.17*math.cos(a),1.13),(.28*math.sin(a),-.23*math.cos(a),.25),.013,M['Natural flax canvas'],n=6)
 body.ring((0,0,1.35),[(.09,0),(.25,-.06),(.22,-.10)],gold,24,.75)
 for side in [-1,1]:body.box((side*.10,-.18,.93),(.055,.025,.69),blue)
 body.rod((0,0,1.31),(0,0,1.48),.07,skin);body.ball((0,0,1.59),(.14,.125,.17),skin,20,10);body.ball((0,-.132,1.59),(.027,.036,.05),skin,10)
 for side in [-1,1]:body.ball((side*.052,-.119,1.63),(.014,.009,.01),dark,10,4)
 body.ring((0,0,1.69),[(.15,0),(.16,.06),(.13,.22),(.08,.30)],linen,24);body.ring((0,0,1.70),[(.16,0),(.162,.035)],gold,24)
 bo=body.bake('V14 ceremonial body '+str(i));bo.parent=root
 pieces={}
 for side in [-1,1]:
  for part in ['upper','forearm','thigh','shin']:
   m=Mesh();m.rod((0,0,-.5),(0,0,.5),.061 if part=='upper' else .047,skin,n=12);ob=m.bake(f'V14 limb {i} {side} {part}');ob.parent=root;pieces[f'{side}:{part}']=ob.name
  m=Mesh();m.ball((0,0,0),(.055,.055,.07),skin,12);ob=m.bake(f'V14 hand {i} {side}');ob.parent=root;pieces[f'{side}:hand']=ob.name
  m=Mesh();m.ball((0,-.04,0),(.08,.14,.045),leather,12);ob=m.bake(f'V14 foot {i} {side}');ob.parent=root;pieces[f'{side}:foot']=ob.name
 rigs.append({'root':root.name,'parts':pieces,'index':i})
tray=Mesh();tray.ring((0,0,0),[(.04,0),(.25,.06),(.28,.10),(.25,.13),(.22,.10),(.04,.04)],gold,32)
for xx,yy in [(-.09,0),(.08,.05),(.03,-.09)]:tray.ball((xx,yy,.15),(.085,.075,.06),potmat,12)
tray.bake('V14 persistent offering dish')
altar=Mesh();altar.box((-47.85,147.85,1.49),(.7,.65,.92),stone);altar.box((-47.85,147.85,1.99),(.90,.82,.12),M['Lapis fired glaze 3']);altar.bake('V14 offering table')
scene['v14_rigs']=json.dumps(rigs)

# The closer ritual camera reveals the sanctuary door: real cedar boards,
# paired leaves, bronze straps and studs replace a featureless dark rectangle.
door=Mesh()
for leaf in [-1,1]:
 center=-47+leaf*1.87
 for j in range(5):door.box((center+(j-2)*.72,152.78,6.1),(.70,.14,9.75),wood)
 for zz in [1.5,3.7,6.2,8.7,10.7]:
  door.box((center,152.68,zz),(3.48,.07,.12),gold)
  for dx in [-1.48,-.74,0,.74,1.48]:door.ball((center+dx,152.625,zz),(.065,.038,.065),gold,10,6)
 for dx in [-1.70,1.70]:door.box((center+dx,152.67,6.1),(.09,.09,9.5),gold)
 # Handles are rings lying in the door plane, assembled as short rods.
 hx=-47+leaf*.35
 for k in range(16):
  a=math.tau*k/16;b=math.tau*(k+1)/16
  door.rod((hx+.16*math.cos(a),152.52,4.7+.21*math.sin(a)),(hx+.16*math.cos(b),152.52,4.7+.21*math.sin(b)),.03,gold,n=6)
door.bake('V14 cedar sanctuary double doors')

# Remove only cached agents whose old route intersects the new ritual workspace.
import numpy as np
tr=np.load(ROOT/'traffic-v13.npz');st=tr['state'];mask=~(((st[:,:,0]>-49.8)&(st[:,:,0]<-47.0)&(st[:,:,1]>146.1)&(st[:,:,1]<148.5)).any(axis=0));removed_traffic=[]
for name in tr['names'][~mask]:
 ob=bpy.data.objects.get(str(name))
 if ob:removed_traffic.append(str(name));bpy.data.objects.remove(ob,do_unlink=True)
np.savez_compressed(ROOT/'traffic-v14.npz',**{k:(tr[k][:,mask] if k=='state' else tr[k][mask] if k in ['names','radii','regions'] else tr[k]) for k in tr.files})

# Local mid-distance social clusters keep bridges and the central traffic lane open.
mid=json.loads(scene['v12_mid_crowd']);clusters=0;positions=[e['base'][:2] for e in mid];cluster_clearances=[]
for idx,e in enumerate(mid):
 x,y,z=e['base']
 if abs(x)<6.8 and 160<y<410 and int(y//24)%3==1 and R.random()<.55:
  anchor=round(y/24)*24+4
  for attempt in range(50):
   xx=(4.8 if x>0 else -4.8)+R.uniform(-1.1,1.1);yy=anchor+R.uniform(-4.2,4.2)
   clearance=min(math.hypot(xx-p[0],yy-p[1]) for j,p in enumerate(positions) if j!=idx)
   if clearance>1.10:
    e['base']=[xx,yy,z];e['grouped']=True;positions[idx]=[xx,yy];e['yaw']=math.atan2((4.8 if x>0 else -4.8)-xx,-(anchor-yy))+R.uniform(-.25,.25);clusters+=1;cluster_clearances.append(clearance);break
scene['v12_mid_crowd']=json.dumps(mid)
scene['city_version']='v14';scene['v14_scope']='Water contact, localized weathering, roof/garden variety, persistent offering handover and social clusters.'
bpy.ops.wm.save_as_mainfile(filepath=str(P/'babylon-city-v14.blend'))
q=ROOT/'qa/v14';q.mkdir(parents=True,exist_ok=True)
(q/'model-evidence.json').write_text(json.dumps({'roof_sites':roof_sites,'wakes':wakes,'rigs':rigs,'removed_traffic':removed_traffic,'clustered_citizens':clusters,'min_cluster_placement_clearance':min(cluster_clearances) if cluster_clearances else None,'appearance_pending':True},indent=2),encoding='utf8')
log('MODEL_READY')
