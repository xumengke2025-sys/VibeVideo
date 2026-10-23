"""Editable bicycle, tailored coat and articulated travelling man in the v14 city."""
import bpy,math,json,ast,sys,random
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent;ROOT=P.parent
bpy.ops.wm.open_mainfile(filepath=str(P/'babylon-city-v14.blend'));scene=bpy.context.scene
for file,names in [('build_city.py',{'srgb','color','node','surface','textured'}),('revise_city_v12.py',{'Mesh'})]:
 tree=ast.parse((P/file).read_text(encoding='utf8'));exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in names],type_ignores=[]),file,'exec'))
sys.path.insert(0,str(ROOT));import v15_route
M=bpy.data.materials
coat=textured('V15 sand gabardine','bb9870',.86);seam=surface('V15 coat seam','7e6245',.9);lining=surface('V15 coat lining','605947',.91)
navy=textured('V15 indigo wool trousers','243439',.83);scarf=textured('V15 brilliant blue scarf','126789',.77);skin=textured('V15 warm face','bf8c65',.63)
hair=surface('V15 dark chestnut hair','34251d',.88);hat=textured('V15 felt brown hat','5b4937',.85);leather=textured('V15 oxblood leather','623b30',.57)
black=surface('V15 enamel frame','183735',.30, .53);rubber=surface('V15 tyre rubber','292b28',.91);steel=surface('V15 brushed nickel','889d98',.27,.83);brass=surface('V15 polished bell brass','b59650',.24,.78);white=surface('V15 shirt cream','e2d5b6',.87)
for mat in [coat,navy,scarf,skin,hat,leather]:
 bump=next((n for n in mat.node_tree.nodes if n.type=='BUMP'),None)
 if bump:bump.inputs['Strength'].default_value=.13;bump.inputs['Distance'].default_value=.003
root=bpy.data.objects.new('V15 persistent trenchcoat cyclist',None);scene.collection.objects.link(root)
parts={}
def baked(mesh,name,parent=root):
 ob=mesh.bake('V15 '+name);ob.parent=parent;parts[name]=ob.name;return ob
def torus(mesh,center,r,thick,mat,n=64,m=10,axis='X',start=0,end=math.tau):
 vs=[]
 for i in range(n+1):
  a=start+(end-start)*i/n
  for j in range(m):
   b=math.tau*j/m;rr=r+thick*math.cos(b)
   v=(thick*math.sin(b),rr*math.sin(a),rr*math.cos(a)) if axis=='X' else (rr*math.cos(a),rr*math.sin(a),thick*math.sin(b))
   vs.append(tuple(center[k]+v[k] for k in range(3)))
 fs=[(i*m+j,i*m+(j+1)%m,(i+1)*m+(j+1)%m,(i+1)*m+j) for i in range(n) for j in range(m)];mesh.add(vs,fs,mat,True)
def strip(mesh,rows,mat):
 n=len(rows[0]);mesh.add([p for row in rows for p in row],[(j*n+i,j*n+i+1,(j+1)*n+i+1,(j+1)*n+i) for j in range(len(rows)-1) for i in range(n-1)],mat,True)
# The wheels rotate independently: tyre, 32 crossed spokes, hub and valve.
for label,y in [('rear wheel',-.62),('front wheel',.62)]:
 m=Mesh();torus(m,(0,0,0),.331,.029,rubber);torus(m,(0,0,0),.305,.012,steel)
 for side in [-1,1]:
  m.rod((side*.055,0,0),(side*.075,0,0),.052,brass,n=20)
  for j in range(16):
   a=math.tau*j/16+.045*side;b=a+.18*side;m.rod((side*.06,.04*math.sin(a),.04*math.cos(a)),(side*.009,.303*math.sin(b),.303*math.cos(b)),.0034,steel,n=5)
 m.rod((-.08,0,0),(.08,0,0),.025,steel,n=16);m.rod((.012,0,.292),(.012,0,.316),.006,brass,n=8)
 ob=baked(m,label);ob.location=(0,y,.36)
m=Mesh();bb=(0,0,.43);seat=(0,-.29,.96);head=(0,.40,.96);rear=(0,-.62,.36);front=(0,.62,.36)
for a,b in [(bb,seat),(seat,head),(head,bb),(rear,seat),(rear,bb)]:m.rod(a,b,.021,black,n=16)
for side in [-1,1]:
 for a,b in [((side*.055,-.62,.36),(side*.042,-.29,.96)),((side*.055,-.62,.36),(side*.07,0,.43)),((side*.055,.62,.36),(side*.055,.40,.91))]:m.rod(a,b,.014,black,n=12)
 m.rod((side*.055,-.62,.36),(side*.055,-.42,.82),.006,steel,n=8)
 m.rod((side*.055,.62,.36),(side*.055,.44,.80),.006,steel,n=8)
 for yy in [-.62,.62]:torus(m,(0,yy,.36),.384,.012,black,n=40,m=8,start=-1.30,end=1.3)
m.rod((0,-.29,.96),(0,-.34,1.075),.016,steel,n=12);m.ball((0,-.36,1.07),(.115,.19,.045),leather,24,10)
# Handlebar has a curved upright and real grip positions.
m.rod((0,.40,.96),(0,.46,1.19),.018,steel,n=16)
for side in [-1,1]:
 m.rod((0,.46,1.19),(side*.18,.49,1.22),.013,steel,n=12);m.rod((side*.18,.49,1.22),(side*.30,.53,1.22),.020,leather,n=12)
 m.rod((side*.23,.545,1.235),(side*.23,.58,1.18),.006,brass,n=8)
m.ball((-.14,.47,1.25),(.035,.035,.022),brass,20,10)
for side in [-1,1]:
 for yy in [-.7,-.5,-.3]:m.rod((side*.16,yy,.89),(side*.16,yy+.15,.89),.007,steel,n=8)
 m.rod((side*.15,-.73,.89),(side*.15,-.62,.37),.008,steel,n=8)
m.box((0,-.63,.96),(.27,.31,.14),leather)
for xx in [-.08,.08]:m.box((xx,-.63,1.035),(.025,.33,.012),brass)
for zz in [.42,.53,.64]:m.rod((.11,-.20,zz),(.11,.15,zz),.008,steel,n=8)
# Chain loop and gear teeth remain a stable mesh, connected to the rear axle.
for center,r in [((.075,0,.43),.105),((.075,-.62,.36),.044)]:
 torus(m,center,r,.007,brass,n=48,m=6)
 for j in range(24):
  a=math.tau*j/24;m.ball((center[0],center[1]+r*math.sin(a),center[2]+r*math.cos(a)),(.008,.008,.008),steel,6,3)
for side in [-1,1]:m.rod((.078,0,.43+side*.105),(.078,-.62,.36+side*.044),.005,steel,n=6)
# Vintage headlamp, leather front bag and small blue pennant identify the bicycle.
m.ball((0,.61,1.14),(.045,.062,.044),brass,20,10);m.ball((0,.662,1.14),(.038,.010,.034),white,20,8)
m.box((0,.60,1.02),(.30,.18,.18),leather)
for side in [-1,1]:m.box((side*.09,.695,1.04),(.024,.014,.11),brass)
baked(m,'bicycle chassis')
for side in [-1,1]:
 m=Mesh();m.rod((0,0,0),(0,0,1),.015,steel,n=12);baked(m,'crank '+str(side))
 m=Mesh();m.box((0,.04,0),(.14,.10,.032),rubber)
 for yy in [0,.04,.08]:m.rod((-.07,yy,.018),(.07,yy,.018),.004,brass,n=6)
 baked(m,'pedal '+str(side))
# Tailored seated torso, collar, lapels, belt, epaulettes, buttons and back vent.
body=Mesh();rows=[]
for z,rx,ry,cy in [(1.03,.21,.14,-.30),(1.21,.20,.14,-.24),(1.43,.25,.15,-.14),(1.60,.245,.125,-.06),(1.65,.15,.105,-.01)]:
 rows.append([(rx*math.cos(a),cy+ry*math.sin(a),z) for a in [math.tau*j/32 for j in range(33)]])
strip(body,rows,coat);body.ring((0,-.24,1.20),[(.205,0),(.208,.045)],leather,32,.69)
body.box((0,-.087,1.22),(.070,.025,.055),brass)
for side in [-1,1]:
 body.add([(side*.045,.065,1.64),(side*.20,.052,1.55),(side*.11,.029,1.36),(side*.025,.076,1.54)],[(0,1,2,3)],lining)
 body.add([(side*.042,.079,1.65),(side*.18,.068,1.55),(side*.10,.047,1.38),(side*.025,.087,1.54)],[(0,1,2,3)],coat)
 body.box((side*.12,-.051,1.39),(.12,.015,.025),lining)
 body.box((side*.18,-.018,1.624),(.13,.09,.02),coat)
 for zz in [1.29,1.40,1.51]:body.ball((side*.068,.019+(zz-1.3)*.17,zz),(.012,.009,.012),brass,10,4)
body.rod((0,.02,1.61),(0,.05,1.78),.062,skin,n=20)
body.add([(-.075,.096,1.69),(.075,.096,1.69),(.05,.10,1.51),(-.05,.10,1.51)],[(0,1,2,3)],white)
baked(body,'tailored torso')
# Split coat tails can move without covering the pedalling knees.
for side in [-1,1]:
 m=Mesh();rows=[]
 for j in range(9):
  u=j/8;rows.append([(side*(.02+.22*k/8)*(1+.22*u),-.32-.13*u+.19*math.sin(k/8*math.pi),1.20-.40*u+.06*math.sin(k/8*math.pi)) for k in range(9)])
 strip(m,rows,coat);ob=baked(m,'coat tail '+str(side));sol=ob.modifiers.new('Tail thickness','SOLIDIFY');sol.thickness=.008
m=Mesh();m.ball((0,.076,1.883),(.123,.109,.16),skin,32,16);m.ball((0,.182,1.886),(.033,.043,.040),skin,16,8)
for side in [-1,1]:
 m.ball((side*.125,.065,1.882),(.025,.021,.041),skin,12,8);m.ball((side*.045,.176,1.923),(.013,.010,.013),hair,12,6)
 m.rod((side*.019,.179,1.948),(side*.073,.169,1.946),.008,hair,n=8)
 m.ball((side*.025,.184,1.853),(.035,.014,.013),hair,12,5)
m.ball((0,.16,1.827),(.038,.012,.009),leather,16,5)
for j in range(7):m.rod((-.09+j*.03,-.005,1.98),(-.10+j*.03,-.028,1.93),.013,hair,n=8)
baked(m,'face and moustache')
m=Mesh();m.ring((0,.045,2.005),[(.12,0),(.19,.005),(.20,.016),(.13,.035),(.127,.14),(.103,.17),(.02,.16)],hat,48,.82);m.ring((0,.045,2.04),[(.128,0),(.129,.027)],leather,40,.82);baked(m,'felt hat')
m=Mesh();m.ring((0,.03,1.713),[(.077,0),(.091,.046),(.077,.083)],scarf,32,.8);m.ball((.055,.102,1.736),(.045,.028,.045),scarf,16,8);baked(m,'scarf collar')
m=Mesh();strip(m,[[(-.03+j*.024,-.02-u*.65,1.74-.13*u+.025*math.sin(j)) for j in range(5)] for u in [k/16 for k in range(17)]],scarf);ob=baked(m,'scarf streamer');sol=ob.modifiers.new('Woven scarf thickness','SOLIDIFY');sol.thickness=.005
for side in [-1,1]:
 for name,r,mat in [('upper arm',.067,coat),('forearm',.054,coat),('thigh',.081,navy),('shin',.059,navy)]:
  m=Mesh();m.rod((0,0,-.5),(0,0,.5),r,mat,r2=r*.85,n=18);baked(m,name+' '+str(side))
 m=Mesh();m.ball((0,0,0),(.044,.065,.038),skin,16,8);baked(m,'hand '+str(side))
 m=Mesh();m.ball((0,.05,.035),(.068,.145,.045),leather,20,10);m.box((0,.05,.003),(.13,.245,.025),rubber);m.ring((0,-.015,.06),[(.058,0),(.052,.12)],leather,20,.83);baked(m,'boot '+str(side))
scene['v15_rider']=json.dumps({'root':root.name,'parts':parts})
print('V15_RIDER_READY',len(parts),flush=True)
# Open real lanes on the city grid, without touching monuments or canal banks.
removed=[];corridors=[(-53,-40,100,128),(-51,22,99.9,106.1),(-47,0,121.8,125.8)]
for ob in list(scene.objects):
 if not ob.name.startswith(('Metropolis courtyard','Courtyard neighbourhood','Distant adobe city','East bank courtyard','V14 regional roof life')):continue
 if ob.name.startswith('V14 regional'):continue
 x,y=ob.location.x,ob.location.y
 if any(x0-4<x<x1+4 and y0-4<y<y1+4 for x0,x1,y0,y1 in corridors):removed.append(ob.name);bpy.data.objects.remove(ob,do_unlink=True)
road=Mesh();stone=M['Worn limestone']
road.box((-14.5,103,.025),(75,6,.10),stone);road.box((-47,115,.03),(5.6,34,.10),stone);road.box((-23.5,124,.03),(47,4.5,.10),stone);road.box((11.5,36,.03),(23,4,.10),stone)
for yy in [37,103]:
 rows=[[(20.5+k*.25,yy+dy,.10+1.055*v15_route.ramp(20.5+k*.25,20.5,22.5)) for dy in [-1.5,1.5]] for k in range(10)]
 strip(road,rows,stone)
for xx in range(-49,23,3):
 for yy in [100.2,105.8]:road.box((xx,yy,.10),(2.94,.13,.07),M['Lapis fired glaze 3'])
baked(road,'connected north cycling streets',None)
# Restore lived-in street edges after opening the shared route.
R=random.Random(15023)
for i,(x,y,rz) in enumerate([(x,112,0) for x in [-30,-19,-8,3,14]]+[(x,94,math.pi) for x in [-24,-13,-2,9]]):
 col=bpy.data.collections.get('Courtyard house module '+str(i%3))
 if col:
  ob=bpy.data.objects.new('V15 north street courtyard '+str(i),None);ob.instance_type='COLLECTION';ob.instance_collection=col;scene.collection.objects.link(ob);ob.location=(x,y,0);ob.scale=(.82,.83,.86);ob.rotation_euler.z=rz
pavers=Mesh();paving_mats=[surface('V15 pale paving '+str(i),c,.85) for i,c in enumerate(['c0af92','c6b79b','bba98e'])]
for xx in range(-49,22):
 for j in range(6):pavers.box((xx+.48,100.45+j*.98,.09),(.955,.935,.025),paving_mats[(xx+j)%3])
baked(pavers,'north street individually jointed pavers',None)
stalls=Mesh()
for i,x in enumerate([-34,-22,-10,2,14]):
 y=99.4 if i%2 else 106.6
 for dx in [-1.25,1.25]:
  for dy in [-.6,.6]:stalls.rod((x+dx,y+dy,.1),(x+dx,y+dy,2.6),.035,M['Dark date palm timber'],n=8)
 strip(stalls,[[(x+dx,y+dy,2.62-.15*math.sin((dx+1.4)/2.8*math.pi)) for dx in [-1.4,-.7,0,.7,1.4]] for dy in [-.75,0,.75]],M['Madder dyed fabric'] if i%2 else M['Natural flax canvas'])
 stalls.box((x,y,.73),(2.4,.85,.12),M['Dark date palm timber'])
 for j in range(5):
  stalls.ring((x-.9+j*.43,y,.81),[(.06,0),(.14,.15),(.10,.27),(.08,.30)],M['Hand fired terracotta'],12)
 for j in range(7):stalls.ball((x-.8+j*.23,y+.21,.84),(.07,.07,.06),brass,8,4)
 stalls.box((x,y-1,.11),(2.3,.6,.015),M['Madder dyed fabric'])
baked(stalls,'north street inhabited market stalls',None)
mid=json.loads(scene['v12_mid_crowd']);new_people=0
sites=[(x+R.uniform(-.3,.3),103+side*R.uniform(1.55,2.1),.11) for x in range(-40,19,2) for side in [-1,1]]
sites += [(-47+side*R.uniform(1.5,2.1),y,.10) for y in range(109,124,3) for side in [-1,1]]
for i,p in enumerate(sites):
 col=bpy.data.collections.get('V12 citizen'+str(i%4)+' stride '+str(i%6))
 if not col:continue
 ob=bpy.data.objects.new('V15 north street visitor '+str(i),None);ob.instance_type='COLLECTION';ob.instance_collection=col;scene.collection.objects.link(ob);ob.location=p;yaw=R.uniform(-math.pi,math.pi);ob.rotation_euler.z=yaw
 mid.append({'name':ob.name,'base':list(p),'phase':R.uniform(0,math.tau),'yaw':yaw,'grouped':True});new_people+=1
scene['v12_mid_crowd']=json.dumps(mid)
print('V15_NEW_STREET_LIFE',new_people,flush=True)
# A high hanging blue ribbon prompts a little duck, leaving full pedestrian clearance.
flag=Mesh()
for yy in [100,106]:flag.rod((-12,yy,.1),(-12,yy,3.3),.05,M['Dark date palm timber'],n=12)
flag.rod((-12,100,3.3),(-12,106,3.3),.02,M['V12 twisted flax rope'],n=8)
strip(flag,[[(-12+.12*math.sin(i),100.2+i*.77,3.12-j*.25) for i in range(8)] for j in range(3)],M['Indigo handwoven cloth']);baked(flag,'north street festival ribbon',None)
scene['city_version']='v15';scene['v15_route_removed_houses']=json.dumps(removed)
bpy.ops.wm.save_as_mainfile(filepath=str(P/'babylon-city-v15.blend'),compress=True)
(ROOT/'qa/v15').mkdir(parents=True,exist_ok=True)
(ROOT/'qa/v15/model-evidence.json').write_text(json.dumps({'rider_parts':len(parts),'cleared_houses':removed,'model':str(P/'babylon-city-v15.blend'),'editable_geometry':True},indent=2),encoding='utf8')
print('V15_MODEL_SAVED',flush=True)
