"""Original river palace inspired by the user's image; fantasy, not archaeology.
Preserves v15 rider, road network, towpaths, bridge and all prior files.
"""
import bpy,math,json,ast,random,sys
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent;ROOT=P.parent
bpy.ops.wm.open_mainfile(filepath=str(P/'babylon-city-v15-detail.blend'));scene=bpy.context.scene
for file,names in [('build_city.py',{'srgb','color','node','surface','textured'}),('revise_city_v12.py',{'Mesh'})]:
 tree=ast.parse((P/file).read_text(encoding='utf8'))
 exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in names],type_ignores=[]),file,'exec'))
R=random.Random(161025);M=bpy.data.materials
stone=M['Worn limestone'];blue=[M['Lapis fired glaze '+str(i)] for i in range(8)]
ivory=M['Ivory glazed relief'];gold=M['V8 aged royal bronze'];wood=M['Dark date palm timber'];dark=M['Interior shade']
reds=[textured('V16 palace red masonry '+str(i),c,.79) for i,c in enumerate(['9b6049','ab6b50','b47658','bd8261'])]
for mat in reds:
 for n in mat.node_tree.nodes:
  if n.type=='BUMP':n.inputs['Strength'].default_value=.21;n.inputs['Distance'].default_value=.025
teal=M['V12 malachite painted timber'];linen=M['Natural flax canvas'];potmat=M['Hand fired terracotta'];leaf=M['Palm leaf']
removed=[]
for o in list(scene.objects):
 x,y,z=o.location
 if 46<x<105 and -32<y<30 and o.instance_collection and any(s in o.instance_collection.name.lower() for s in ['inhabited','courtyard']):
  removed.append(o.name);bpy.data.objects.remove(o,do_unlink=True)
 elif 47<x<103 and -29<y<28 and o.name.startswith(('Awning tied pole','Woven goods bale','Market counter','Date fruit cluster','Terrace foliage')):
  removed.append(o.name);bpy.data.objects.remove(o,do_unlink=True)
meshes={k:Mesh() for k in ['masonry','trim','columns','glaze','reliefs','doors','courtyard','stairs','roof','planting','people']}
def box(k,p,s,mat):meshes[k].box(p,s,mat)
def rod(k,a,b,r,mat,**kw):meshes[k].rod(a,b,r,mat,**kw)
def ball(k,p,s,mat,**kw):meshes[k].ball(p,s,mat,**kw)
def ring(k,p,profile,mat,**kw):meshes[k].ring(p,profile,mat,**kw)
def band(x,y,w,d,z,h,mat):
 box('trim',(x,y-d/2-.055,z),(w+.20,.18,h),mat)
 box('trim',(x-w/2-.055,y,z),(.18,d+.20,h),mat)
 box('trim',(x+w/2+.055,y,z),(.18,d+.20,h),mat)
 box('trim',(x,y+d/2+.055,z),(w+.20,.18,h),mat)
def tiles(axis,plane,lo,hi,z,h,seed=0):
 # Actual jointed glazed bricks, with recessed mortar from the supporting wall.
 for j in range(max(1,int(h/.29))):
  zz=z+.145+j*.29
  start=lo-.32*(j%2)
  for i in range(math.ceil((hi-start)/.66)):
   a=max(lo,start+i*.66);b=min(hi,start+(i+1)*.66-.024)
   if b<=a:continue
   p=(plane,(a+b)/2,zz) if axis=='X' else ((a+b)/2,plane,zz)
   s=(.095,b-a,.265) if axis=='X' else (b-a,.095,.265)
   box('glaze',p,s,blue[(i*3+j+seed)%8])
def rosette(x,y,z,r=.34,axis='X'):
 def p(a,b,c):return (x+c,y+a,z+b) if axis=='X' else (x+a,y+c,z+b)
 ball('reliefs',p(0,0,-.055),(r*.25,r*.25,r*.25),gold,n=12,rings=5)
 for j in range(8):
  a=math.tau*j/8;v=p(math.cos(a)*r*.60,math.sin(a)*r*.60,-.07)
  ball('reliefs',v,(.065,r*.22,r*.22) if axis=='X' else (r*.22,.065,r*.22),ivory,n=10,rings=5)
def lion(x,y,z,scale=1):
 # Bas-relief silhouette stands out from the blue frieze, facing the quay.
 def p(u,v,d=0):return (x-d,y+u*scale,z+v*scale)
 ball('reliefs',p(0,.68,.12),(.16*scale,.83*scale,.30*scale),ivory,n=18,rings=8)
 ball('reliefs',p(.74,.92,.13),(.20*scale,.28*scale,.35*scale),gold,n=16,rings=8)
 ball('reliefs',p(.91,1.04,.19),(.20*scale,.22*scale,.22*scale),ivory,n=16,rings=8)
 for j,u in enumerate([-.57,-.27,.37,.66]):
  rod('reliefs',p(u,.55,.14),p(u+(-.16 if j%2 else .10),.13,.14),.075*scale,ivory,n=10)
  box('reliefs',p(u+(-.19 if j%2 else .13),.10,.14),(.20*scale,.28*scale,.10*scale),ivory)
 last=p(-.68,.79,.13)
 for j in range(1,9):
  a=j/8;v=p(-.68-.56*math.sin(a*1.7),.79+.53*a,.12);rod('reliefs',last,v,.038*scale,gold,n=8);last=v
def column(x,y,z,h,r=.31):
 ring('columns',(x,y,z),[(r*1.9,0),(r*1.9,.16),(r*1.55,.24),(r*1.55,.43),(r*1.15,.56),(r,.64),(r*.82,h-.55),(r*1.12,h-.43),(r*1.12,h-.25)],ivory,n=24)
 ring('columns',(x,y,z+.56),[(r*1.11,0),(r*1.11,.13)],gold,n=24)
 box('columns',(x,y,z+h-.14),(r*3.5,r*3.5,.28),ivory)
 # Fine bands give the shafts a crafted scale without stripe-like noise.
 ring('columns',(x,y,z+h-.68),[(r*.90,0),(r*.90,.10)],blue[4],n=24)
def mass(x,y,w,d,z,h):
 box('masonry',(x,y,z+h/2),(w,d,h),reds[1]);band(x,y,w,d,z+.23,.38,stone)
 band(x,y,w,d,z+h-.42,.31,gold);band(x,y,w,d,z+h+.04,.38,ivory)
 box('roof',(x,y,z+h+.24),(w+.7,d+.7,.20),stone)
 # Pilasters articulate the solid walls and keep their scale readable.
 for yy in [y-d/2+.7+i*3.4 for i in range(max(1,int((d-1.4)/3.4))+1)]:
  box('masonry',(x-w/2-.14,yy,z+h*.47),(.35,.47,h*.89),reds[2])
 tiles('X',x-w/2-.20,y-d/2,y+d/2,z+1.05,1.45)
 tiles('Y',y-d/2-.20,x-w/2,x+w/2,z+1.05,1.45,2)
 for yy in range(math.ceil(y-d/2)+2,math.floor(y+d/2)-1,4):rosette(x-w/2-.24,yy,z+h-1.05,.29)
 for xx in range(math.ceil(x-w/2)+2,math.floor(x+w/2)-1,4):rosette(xx,y-d/2-.24,z+h-1.05,.29,'Y')

# Three receding levels, a real open court, and two tall river-facing wings.
box('masonry',(77,0,2.65),(46,54,4.5),reds[0]);band(77,0,46,54,4.95,.35,stone)
tiles('X',53.91,-27,27,1.5,1.45)
tiles('Y',-27.09,54,100,1.5,1.45,3)
for yy in range(-23,25,5):lion(53.77,yy,1.57,.94)
for yy in range(-25,27,4):
 box('masonry',(53.72,yy,2.6),(.52,.55,4.3),reds[2])
mass(81,-20,36,14,5.1,8.3);mass(81,20,36,14,5.1,8.3)
mass(92,0,14,27,5.1,13.5)
mass(87,0,22,30,13.65,6.4)
mass(90.5,0,13,19,20.30,5.0)
# Real balcony slabs and lower supports connect the upper gallery to the court.
box('roof',(75.8,0,13.47),(6.5,30,.36),stone)
for yy in [-10,-5,0,5,10]:column(79,yy,5.25,8.04,.36)
# Open river colonnade and upper arcades. Roofs have actual visible thickness.
for yy in range(-24,25,3):column(60.4,yy,5.14,6.8,.32)
box('roof',(61.8,0,12.15),(6.5,51,.42),ivory);band(61.8,0,6.5,51,12.48,.22,gold)
for yy in range(-12,13,3):column(74.6,yy,13.65,5.5,.27)
box('roof',(76.3,0,19.36),(5,29,.36),ivory)
for yy in range(-8,9,2):column(82.9,yy,20.30,4.6,.22)
box('roof',(84.4,0,25.12),(4.6,18.7,.30),ivory)
# Southern side columns are seen in the opening city reveal.
for xx in range(66,98,3):column(xx,-26.1,5.14,6.8,.30)
box('roof',(81.5,-25.3,12.15),(35.5,3.9,.42),ivory)
for xx in range(79,98,3):column(xx,-16.5,13.65,5.5,.25)
box('roof',(88,-15.8,19.36),(22.5,3.5,.36),ivory)
# Entrance wall and paired tall doorways; dark voids are set behind jambs.
for yy in [-7,7]:
 box('doors',(84.91,yy,8.65),(.09,3.1,6.9),dark)
 for side in [-1,1]:
  box('doors',(84.72,yy+side*1.75,8.65),(.55,.45,7.5),blue[3])
  box('doors',(84.47,yy+side*2.05,8.65),(.38,.22,7.95),ivory)
 box('doors',(84.62,yy,12.35),(.65,3.9,.65),gold)
 box('doors',(84.80,yy,8.40),(.12,2.8,6.1),wood)
 for z in [6.4,8.6,10.8]:box('doors',(84.71,yy,z),(.10,2.85,.10),gold)
# Courtyard pavement, a small reflecting basin and a connected staircase.
box('courtyard',(72.3,0,5.13),(24,25,.16),stone)
for x in range(62,84,2):
 for y in range(-12,13,2):box('courtyard',(x,y,5.23),(1.91,1.91,.035),stone)
box('courtyard',(73,0,5.32),(8,6,.36),blue[2]);box('courtyard',(73,0,5.54),(7.3,5.3,.07),M['Canal water / rippled reflection'])
for side in [-1,1]:
 for y in range(-12,13,2):box('courtyard',(73+side*4.1,y*.25,5.55),(.27,.56,.30),ivory)
box('stairs',(45.8,0,1.02),(2.8,10,.26),stone)
# Extend the existing riverside walk to the south end of this new frontage.
box('courtyard',(43.85,-26,1.025),(3.5,12,.15),stone)
for y in range(-31,-19,2):box('courtyard',(41.7,y,.92),(1,1.94,.22),stone)
for i in range(26):
 x=47.2+(i+.5)*.267;h=(i+1)*4.07/26
 box('stairs',(x,0,1.13+h/2),(.28,7.0,h),stone)
 for side in [-1,1]:box('stairs',(x,side*3.8,1.13+h/2+.39),(.29,.55,h+.78),blue[2])
for y in [-4.7,4.7]:
 box('stairs',(52.7,y,5.43),(2.6,1.8,.55),stone)
 # Freestanding lions face the arriving traveller; no relation to the rider face.
 ball('reliefs',(52.5,y,6.25),(1.03,.47,.50),ivory,n=24,rings=10)
 for dx in [-.68,.63]:
  for dy in [-.30,.30]:rod('reliefs',(52.5+dx,y+dy,6.02),(52.4+dx,y+dy,5.7),.12,ivory,n=12)
 ball('reliefs',(51.55,y,6.65),(.43,.38,.43),gold,n=20,rings=10)
 ball('reliefs',(51.32,y,6.68),(.32,.27,.27),ivory,n=20,rings=10)
# Battlements, bronze standards and woven fabric give the roofline silhouette.
for x,y,w,d,z in [(87,0,22,30,20.35),(90.5,0,13,19,25.55)]:
 for yy in range(math.ceil(y-d/2),math.floor(y+d/2)+1,2):
  for xx in [x-w/2,x+w/2]:box('roof',(xx,yy,z+.39),(.58,.70,.78),blue[3])
 for xx in range(math.ceil(x-w/2),math.floor(x+w/2)+1,2):
  for yy in [y-d/2,y+d/2]:box('roof',(xx,yy,z+.39),(.70,.58,.78),blue[3])
for y in [-21,21]:
 rod('roof',(61,y,12.4),(61,y,17),.052,gold,n=12)
 ball('roof',(61,y,17.14),(.18,.18,.24),gold,n=16,rings=8)
 vs=[(61+.18*math.sin(i*.7),y+u*2,16.6-v*2.0) for v in [0,1] for i,u in enumerate([j/10 for j in range(11)])]
 meshes['roof'].add(vs,[(i,i+1,i+12,i+11) for i in range(10)],M['Madder dyed fabric'])
for x,y,z in [(66,-10,5.25),(66,10,5.25),(80,-11,13.9),(80,11,13.9)]:
 ring('planting',(x,y,z),[(.46,0),(.67,.32),(.58,.90),(.43,1.1)],potmat,n=24)
 rod('planting',(x,y,z+.4),(x+.12,y,z+4.8),.10,wood,r2=.075,n=12)
 for j in range(10):
  a=j*math.tau/10;vs=[]
  for k in range(9):
   u=k/8;r=2.1*u;zz=z+4.8+.6*math.sin(math.pi*u)-.75*u
   width=.22*math.sin(math.pi*u)
   for sign in [-1,1]:vs.append((x+r*math.cos(a)+sign*width*math.sin(a),y+r*math.sin(a)-sign*width*math.cos(a),zz))
  meshes['planting'].add(vs,[(2*k,2*k+1,2*k+3,2*k+2) for k in range(8)],leaf)
# Small groups on terraces stay irregular and leave the stair approach open.
skin=M['Sunlit warm skin'];cloths=[linen,M['Indigo handwoven cloth'],M['Madder dyed fabric']]
people=[]
for i,(x,y,z) in enumerate([(58,-17,5.25),(58.7,-16.3,5.25),(57.1,18,5.25),(58,18.4,5.25),(64,8.5,5.25),(64.7,9.5,5.25),(78,8,13.9),(78.7,8.7,13.9)]):
 p=Mesh();p.ring((0,0,.15),[(.24,0),(.20,.8),(.22,1.2)],cloths[i%3],n=16,ys=.75)
 p.ball((0,0,1.59),(.13,.12,.17),skin,n=12,rings=6)
 for side in [-1,1]:p.rod((side*.21,0,1.23),(side*.25,-.15,.94),.052,skin,n=8)
 meshes['people'].append(p,(x,y,z),rot=R.uniform(-2.5,2.5));people.append([x,y,z])
objects=[]
for key,mesh in meshes.items():
 if not mesh.v:continue
 ob=mesh.bake('V16 river palace '+key);objects.append(ob.name)
 if key in ['masonry','trim','roof','stairs','doors','courtyard']:
  bevel=ob.modifiers.new('Small worn masonry edges','BEVEL');bevel.width=.035;bevel.segments=2
  ob.modifiers.new('Area weighted stone normals','WEIGHTED_NORMAL')
scene['v16_palace']=json.dumps({'objects':objects,'footprint':[46,-27,100,27],'highest_roof':26.4,'river_facing':'west','entrance':[47.2,0,1.13],'protected_bridge_y':32,'protected_east_towpath_x':43.4,'people':people})
scene['city_version']='v16-palace';scene['v16_scope']='Layered red and lapis river palace, continuous colonnades, open court, stair, reliefs and roof terraces. Original featureless v15 cyclist preserved.'
bpy.ops.wm.save_as_mainfile(filepath=str(P/'babylon-city-v16-palace.blend'))
report={'source':'babylon-city-v15-detail.blend','model':str(P/'babylon-city-v16-palace.blend'),'removed_residential_objects':removed,'new_mesh_objects':objects,'new_vertices':sum(len(bpy.data.objects[n].data.vertices) for n in objects),'palace':json.loads(scene['v16_palace']),'historical_status':'Fantasy architecture inspired by user reference, not a verified reconstruction','rider':'v15 detail rev4 featureless geometry unchanged','render_required':'All frames use this new world; do not mix v15 pixels'}
(ROOT/'qa/v16/palace-model.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('V16_PALACE_MODEL_READY',report['new_vertices'],len(removed),flush=True)
