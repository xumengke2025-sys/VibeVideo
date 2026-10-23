"""V12: ceremonial society, full-length street population and working river craft.
All new assets are editable solid geometry. The setting remains fantasy Babylon.
"""
import bpy, math, json, random, ast, time
import numpy as np
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent;QA=BASE/'qa/v12'
R=random.Random(2026102112)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'babylon-city-v11.blend'))
scene=bpy.context.scene
def stage(s):print('V12_BUILD',s,flush=True)
tree=ast.parse((ROOT/'build_city.py').read_text(encoding='utf8'))
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'srgb','color','node','surface','textured'}],type_ignores=[]),'materials','exec'))
linen=bpy.data.materials['Natural flax canvas'];navy=bpy.data.materials['Indigo handwoven cloth'];red=bpy.data.materials['Madder dyed fabric'];wood=bpy.data.materials['Dark date palm timber'];dark=bpy.data.materials['Interior shade']
skin=bpy.data.materials['Sunlit warm skin'];gold=textured('V12 chased warm bronze','b08a45',.38,True)
ivory=textured('V12 ritual linen','e0d6bc',.9);teal=textured('V12 malachite painted timber','29756d',.59);lapis=textured('V12 indigo painted timber','244d78',.52);ochre=textured('V12 red ochre painted timber','9b4531',.67)
cord=textured('V12 twisted flax rope','b49b65',.87);leather=textured('V12 dark leather','60432d',.81)

class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.m=[];self.sm=[]
 def add(self,vs,fs,mat,smooth=False):
  if mat not in self.m:self.m.append(mat)
  i=self.m.index(mat);n=len(self.v);self.v.extend(vs);self.f.extend([tuple(n+k for k in f) for f in fs]);self.mi.extend([i]*len(fs));self.sm.extend([smooth]*len(fs))
 def ball(self,p,s,mat,n=12,rings=6):
  vs=[(p[0]+s[0]*math.sin(math.pi*j/rings)*math.cos(math.tau*i/n),p[1]+s[1]*math.sin(math.pi*j/rings)*math.sin(math.tau*i/n),p[2]+s[2]*math.cos(math.pi*j/rings)) for j in range(rings+1) for i in range(n)]
  fs=[((j+1)*n+i,(j+1)*n+(i+1)%n,j*n+(i+1)%n,j*n+i) for j in range(rings) for i in range(n)];self.add(vs,fs,mat,True)
 def ring(self,p,profile,mat,n=20,ys=1):
  vs=[(p[0]+r*math.cos(math.tau*i/n),p[1]+r*ys*math.sin(math.tau*i/n),p[2]+z) for r,z in profile for i in range(n)]
  fs=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(profile)-1) for i in range(n)];self.add(vs,fs,mat,True)
 def rod(self,a,b,r,mat,r2=None,n=10):
  a,b=Vector(a),Vector(b);d=b-a;rot=d.to_track_quat('Z','Y').to_matrix();r2=r if r2 is None else r2
  vs=[tuple((a+b)/2+rot@Vector((rad*math.cos(math.tau*i/n),rad*math.sin(math.tau*i/n),z))) for z,rad in [(-d.length/2,r),(d.length/2,r2)] for i in range(n)]
  self.add(vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat,True)
 def box(self,p,s,mat):
  vs=[(p[0]+x*s[0]/2,p[1]+y*s[1]/2,p[2]+z*s[2]/2) for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
  self.add(vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat)
 def bake(self,name,link=True):
  me=bpy.data.meshes.new(name);me.from_pydata(self.v,[],self.f);me.update()
  for m in self.m:me.materials.append(m)
  for p,i,sm in zip(me.polygons,self.mi,self.sm):p.material_index=i;p.use_smooth=sm
  ob=bpy.data.objects.new(name,me)
  if link:scene.collection.objects.link(ob)
  return ob
 def append(self,other,pos,rot=0,scale=1):
  co,si=math.cos(rot),math.sin(rot);n=len(self.v);self.v.extend([(pos[0]+scale*(co*x-si*y),pos[1]+scale*(si*x+co*y),pos[2]+scale*z) for x,y,z in other.v])
  ids=[]
  for m in other.m:
   if m not in self.m:self.m.append(m)
   ids.append(self.m.index(m))
  self.f.extend([tuple(n+k for k in f) for f in other.f]);self.mi.extend([ids[k] for k in other.mi]);self.sm.extend(other.sm)

def figure(role,phase=0,lod=False,variant=0):
 m=Mesh();a=math.sin(phase);cloth=[linen,navy,red,ivory][variant%4]
 if lod:
  # These citizens are only a few pixels tall in the city view. Retain the
  # head/shoulder/robe/leg silhouette with 106 vertices rather than 700.
  m.ring((0,0,.32),[(.25,0),(.22,.68),(.19,1.02)],cloth,6,.78)
  m.ball((0,0,1.57),(.13,.12,.17),skin,6,3)
  for side in [-1,1]:
   m.rod((side*.20,0,1.28),(side*.25,-.06,.86),.055,skin,n=4)
   m.rod((side*.10,0,.4),(side*.11,-.04,.06),.045,skin,n=4)
  return m
 military=role in ['soldier','officer'];egypt=role in ['envoy','attendant'];priest=role in ['priest','acolyte'];worker=role in ['crew','towman']
 if military:cloth=navy
 elif egypt or priest:cloth=ivory
 elif worker:cloth=[navy,red,linen][variant%3]
 n=8 if lod else 20
 # Distinct hems: priest's ankle robe, soldier's knee tunic, short worker kilt.
 hem=.17 if priest else .58 if military else .60 if egypt or worker else .37
 m.ring((0,0,hem),[(.27,0),(.245,.38),(.20,1.3-hem)],cloth,n,.79)
 if egypt or worker:
  m.ball((0,0,1.20),(.215,.13,.30),skin,8 if lod else 16)
  m.ring((0,0,.91),[(.218,0),(.22,.065)],cloth,n,.75)
 else:m.ball((0,0,1.18),(.225,.14,.24),cloth,8 if lod else 16)
 for side in [-1,1]:
  dy=side*a*(.11 if not priest else .05)
  knee=(side*.11,dy,.40);foot=(side*.12,dy*1.5,.08+max(0,side*a)*.035)
  m.rod((side*.1,0,.73),knee,.055,skin);m.rod(knee,foot,.045,skin);m.ball((foot[0],foot[1]-.045,foot[2]),(.075,.135,.045),leather,8,4)
  shoulder=(side*.22,0,1.31)
  if priest or egypt:elbow=(side*.31,-.11,1.07);hand=(side*.22,-.32,1.15+.025*a)
  elif role=='towman':elbow=(side*.28,-.13,1.02);hand=(side*.22,-.42,1.10)
  elif military:elbow=(side*.31,-.04,1.02);hand=(side*.34,-.18,1.07)
  elif role=='crew':elbow=(side*.30,-.13,1.06);hand=(side*.25,-.36,1.11+.055*a)
  else:elbow=(side*.27,side*a*.10,1.05);hand=(side*.24,side*a*.17,.85)
  m.rod(shoulder,elbow,.063,skin);m.rod(elbow,hand,.048,skin);m.ball(hand,(.052,.055,.07),skin,8,4)
 m.rod((0,0,1.32),(0,0,1.49),.07,skin)
 m.ball((0,-.01,1.58),(.13,.12,.17),skin,8 if lod else 16,5 if lod else 8)
 if not lod:
  m.ball((0,-.127,1.58),(.028,.045,.052),skin,8,4)
  for side in [-1,1]:
   m.ball((side*.052,-.119,1.625),(.018,.01,.012),dark,8,4);m.ball((side*.13,0,1.58),(.025,.04,.045),skin,8,4)
 if military:
  m.ring((0,0,1.63),[(.15,0),(.152,.12),(.11,.25),(.012,.38)],gold,n)
  # Overlapping bronze scales read as armour below the helmet.
  if not lod:
   for j in range(6):
    for k in range(5):m.ball(((k-2)*.077,-.139-(2-abs(k-2))*.006,1.32-j*.064),(.043,.027,.045),gold,8,4)
  else:m.box((0,-.125,1.13),(.35,.04,.39),gold)
  m.box((0,.14,1.02),(.36,.045,.65),red)
  m.ball((-.35,-.25,1.02),(.265,.055,.38),gold,12,7);m.ball((-.35,-.306,1.02),(.222,.014,.33),lapis,12,7);m.ball((-.35,-.331,1.02),(.07,.035,.07),gold,10,5)
  m.rod((.34,-.18,.10),(.34,-.18,2.48),.018,wood)
  m.add([(.34,-.18,2.75),(.26,-.18,2.46),(.42,-.18,2.46),(.34,-.14,2.46)],[(0,1,2),(0,3,1),(0,2,3),(1,3,2)],gold)
 elif priest:
  m.ring((0,0,1.67),[(.152,0),(.16,.08),(.12,.25),(.105,.31),(.0,.31)],ivory,n)
  m.ring((0,0,1.68),[(.158,0),(.16,.045)],gold,n)
  for side in [-1,1]:m.box((side*.09,-.15,1.03),(.075,.035,.66),navy)
  m.ring((0,-.37,1.10+.025*a),[(.06,0),(.16,.08),(.17,.11),(.13,.11)],gold,16)
  if role=='priest':
   m.rod((.34,-.19,.08),(.34,-.19,2.08),.025,gold);m.ring((.34,-.19,1.98),[(.09,0),(.11,.09),(.07,.16)],gold,16)
 elif egypt:
  m.ball((0,.018,1.62),(.159,.128,.185),dark,12,6)
  # Front of face stays exposed by splitting the wig into side locks.
  m.ball((0,-.03,1.59),(.115,.116,.145),skin,12,6)
  for side in [-1,1]:m.box((side*.145,-.006,1.50),(.065,.20,.23),dark)
  m.ring((0,0,1.39),[(.08,.02),(.245,-.025),(.248,-.07),(.085,-.02)],gold,n,.74)
  m.ring((0,0,1.37),[(.12,0),(.23,-.045)],lapis,n,.75)
  m.box((0,-.195,.78),(.15,.025,.34),lapis)
  if role=='envoy':
   m.rod((.35,-.18,.18),(.35,-.18,2.45),.022,gold)
   for j in range(9):
    th=(j-4)*.17;m.rod((.35,-.18,2.1),(.35+.38*math.sin(th),-.18,2.1+.38*math.cos(th)),.026,ivory)
  else:m.box((0,-.39,1.14),(.40,.25,.20),ochre);m.box((0,-.39,1.26),(.42,.27,.035),gold)
 elif role=='towman':
  m.rod((-.22,-.12,1.32),(.21,-.16,.98),.028,cord)
  m.ring((0,0,1.68),[(.14,0),(.14,.07),(.09,.11)],linen,12)
 elif role=='crew':m.ring((0,0,1.67),[(.14,0),(.16,.05),(.1,.12)],red if variant%2 else linen,12)
 else:m.ring((0,0,1.67),[(.14,0),(.15,.07),(.09,.10)],cloth,n)
 return m

role_cols={}
for role in ['priest','acolyte','soldier','officer','envoy','attendant','crew','towman']+['citizen'+str(i) for i in range(4)]:
 cols=[]
 for k in range(6):
  col=bpy.data.collections.new(f'V12 {role} stride {k}');col.use_fake_user=True
  ob=figure(role,k*math.tau/6,variant=int(role[-1]) if role.startswith('citizen') else 0).bake(col.name,False);col.objects.link(ob);cols.append(col.name)
 role_cols[role]=cols
stage('distinct_role_meshes_baked')

traffic=np.load(BASE/'traffic-v11.npz');names=[str(n) for n in traffic['names']];state=traffic['state'].copy();regions=traffic['regions']
role_counts={};assigned=[]
for i,(name,region) in enumerate(zip(names,regions)):
 if not name.startswith('V11 human '):continue
 role=None
 if region=='temple':role='priest' if i%3 else 'acolyte'
 elif region=='shrine' and i%3:role='priest' if i%2 else 'acolyte'
 elif region=='grain' and i%4==0:role='crew'
 elif region=='palace':role='envoy' if i%3==0 else 'attendant' if i%3==1 else 'soldier'
 if role:
  ob=bpy.data.objects[name];ob.instance_collection=bpy.data.collections[role_cols[role][0]];ob['stride_modules']=json.dumps(role_cols[role]);ob['role']=role
  role_counts[role]=role_counts.get(role,0)+1;assigned.append({'name':name,'role':role,'region':str(region)})
  if region in ['temple','shrine']:
   target=np.array([52,49]) if region=='temple' else np.array([-47,148])
   delta=target-state[:,i,:2];stationary=state[:,i,5]<.5
   state[stationary,i,3]=np.arctan2(delta[stationary,0],-delta[stationary,1])

special=[]
def person(role,pos,yaw=0,kind='stationary',**extra):
 ob=bpy.data.objects.new('V12 '+role+' event '+str(len(special)),None);scene.collection.objects.link(ob);ob.instance_type='COLLECTION';ob.instance_collection=bpy.data.collections[role_cols[role][0]];ob.location=pos;ob.rotation_euler.z=yaw
 ob['stride_modules']=json.dumps(role_cols[role]);ob['role']=role
 d={'name':ob.name,'role':role,'base':list(pos),'yaw':yaw,'kind':kind,'phase':R.random()*math.tau,**extra};special.append(d);return ob
# A diplomatic reception at the south gate: gifts face welcoming officials.
for i,(x,y) in enumerate([(-.5,-7),(1.1,-6.3),(.2,-4.8),(1.7,-3.9)]):person('envoy' if i<2 else 'attendant',(x,y,.04),-.9,phase=i*.8)
for x,y in [(-2.5,-8.5),(3.2,-7.2),(-2.0,-2),(3.5,-1.4)]:person('soldier',(x,y,.04),.4 if x<0 else -.7)
person('priest',(-1.6,-6.6,.04),1.2)
# A compact patrol crosses the market during its shot; civilians keep flowing.
for j in range(5):
 for col in range(2):person('officer' if j==0 and col==0 else 'soldier',(1.5+col*1.1,-9+j*1.45,.04),math.pi,'patrol',speed=2.4)
# Ritual workers stand on the shrine dais and present vessels toward the sanctuary.
for i,(x,y,z) in enumerate([(-49,147,1.02),(-45,147,1.02),(-47,143.3,.32)]):person('priest' if i<2 else 'acolyte',(x,y,z),math.pi)
# Remove only old actors that enter the protected interaction spaces.
keep=[];removed=[]
for i,name in enumerate(names):
 p=state[:,i,:2];hit=np.zeros(len(p),bool)
 for ev in special:
  b=np.array(ev['base'][:2]);ep=np.tile(b,(len(p),1))
  if ev['kind']=='patrol':ep[:,1]+=np.arange(len(p))/8*ev['speed']
  hit|=(np.linalg.norm(p-ep,axis=1)<.80)
 if hit.any() and regions[i]=='avenue':bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True);removed.append(name)
 else:keep.append(i)
np.savez_compressed(BASE/'traffic-v12.npz',state=state[:,keep],names=np.array([names[i] for i in keep]),hz=traffic['hz'],duration=traffic['duration'],radii=traffic['radii'][keep],regions=regions[keep])
scene['v11_actors']=json.dumps([names[i] for i in keep])
stage('ceremonies_and_diplomatic_reception_placed')

# Add close citizens with their own cached avoidance, rather than filling the
# foreground with static distant cones or arranging people in regular rows.
old=state[:,keep];old_r=traffic['radii'][keep]
event_ground=[ev for ev in special if ev['base'][2]<1]
fixed=np.concatenate([old[:,:,:2],np.array([[ev['base'][:2] for ev in event_ground]]*len(old),np.float32)],axis=1)
for k,ev in enumerate(event_ground):
 if ev['kind']=='patrol':fixed[:,len(keep)+k,1]+=np.arange(len(old))/8*ev['speed']
fixed_r=np.concatenate([old_r,np.full(len(event_ground),.40)])
fixed_r[:len(keep)][old[0,:,2]>1]=0
fixed[:,np.concatenate([old[0,:,2]>1,np.zeros(len(event_ground),bool)]),:]=10000
near=[];phases=[];angles=[];targets=[];near_names=[]
def walkable(p):
 x,y=p
 return -6<x<6 and -23<y<138 and not (-6.6<x<-2.3 and 47.4<y<52.6) and not (-6.5<x<-3.0 and -14<y<-10) and not ((x+4.8)**2+(y+12)**2<2.1**2)
for i in range(180):
 for attempt in range(1000):
  p=np.array([R.uniform(-5.8,5.8),R.uniform(-22.5,137.5)])
  if walkable(p) and np.all(np.linalg.norm(fixed[0]-p,axis=1)>fixed_r+.43) and (not near or np.min(np.linalg.norm(np.array(near)-p,axis=1))>.78):break
 else:raise RuntimeError('Close crowd packing failed')
 near.append(p);phases.append(R.random()*math.tau);angles.append(R.random()*math.tau);targets.append(np.array([R.uniform(-5,5),R.uniform(-21,136)]))
 col=role_cols['citizen'+str(i%4)];ob=bpy.data.objects.new('V12 close citizen '+str(i),None);scene.collection.objects.link(ob);ob.instance_type='COLLECTION';ob.instance_collection=bpy.data.collections[col[0]];ob['stride_modules']=json.dumps(col);ob.location=(*p,.04);ob.scale=(R.uniform(.91,1.07),)*3;near_names.append(ob.name)
near=np.array(near);targets=np.array(targets);phases=np.array(phases);angles=np.array(angles);cache=np.zeros((len(old),len(near),7),np.float32)
speeds=np.array([R.uniform(.5,1.25) for _ in near])
for step in range(len(old)):
 delta=targets-near;distance=np.linalg.norm(delta,axis=1)
 for i in np.where(distance<.8)[0]:targets[i]=[R.uniform(-5,5),R.uniform(-21,136)]
 vel=delta/np.maximum(.1,distance[:,None])*speeds[:,None]
 sep=near[:,None,:]-fixed[step][None,:,:];ds=np.linalg.norm(sep,axis=2);safe=fixed_r[None,:]+.39
 push=(sep/np.maximum(.01,ds[:,:,None])*np.maximum(0,safe+.4-ds)[:,:,None]).sum(axis=1)*1.6
 vel+=push;length=np.linalg.norm(vel,axis=1);vel*=np.minimum(1,1.5/np.maximum(.1,length))[:,None]
 proposed=near+vel/8
 for i in range(len(near)):
  if not walkable(proposed[i]):proposed[i]=near[i];targets[i]=[R.uniform(-5,5),R.uniform(-21,136)]
 for iteration in range(8):
  for i in range(len(near)):
   offset=proposed[i]-fixed[step];d=np.linalg.norm(offset,axis=1);mask=d<fixed_r+.38
   for off,dd,rr in zip(offset[mask],d[mask],fixed_r[mask]):
    q=proposed[i]+off/max(.001,dd)*(rr+.39-dd)
    if walkable(q):proposed[i]=q
  off=proposed[:,None,:]-proposed[None,:,:];d=np.linalg.norm(off,axis=2)
  pairs=list(zip(*np.where(np.triu(d<.70,k=1))))
  for i,j in pairs:
   dd=d[i,j];corr=off[i,j]/max(.001,dd)*(.71-dd)*.5
   if walkable(proposed[i]+corr):proposed[i]+=corr
   if walkable(proposed[j]-corr):proposed[j]-=corr
 actual=(proposed-near)*8;speed=np.linalg.norm(actual,axis=1);moving=speed>.08
 yaw=np.arctan2(actual[:,0],-actual[:,1]);angles+=np.clip((yaw-angles+math.pi)%math.tau-math.pi,-.26,.26)*moving
 phases+=speed/8*4.3;pose=((phases%math.tau)/math.tau*6).astype(int);pose[~moving]=0
 cache[step,:,0:2]=proposed;cache[step,:,2]=.04+np.sin(phases*2)*.012*moving;cache[step,:,3]=angles;cache[step,:,4]=pose;cache[step,:,5]=moving;cache[step,:,6]=phases;near=proposed
 if step%160==0:stage('close_crowd_cache_'+str(step))
np.savez_compressed(BASE/'traffic-v12.npz',state=np.concatenate([old,cache],axis=1),names=np.array([names[i] for i in keep]+near_names),hz=traffic['hz'],duration=traffic['duration'],radii=np.concatenate([old_r,np.full(len(near),.33)]),regions=np.concatenate([regions[keep],np.array(['avenue']*len(near))]))
scene['v11_actors']=json.dumps([names[i] for i in keep]+near_names)

# Far citizens use solid low-detail silhouettes, batched beyond readable gait scale.
# Every avenue section is populated; near/mid figures retain individual motion.
templates=[figure('civilian',0,True,i) for i in range(4)]
lod_meshes=[t.bake('V12 mid distance citizen '+str(i),False).data for i,t in enumerate(templates)]
far=Mesh();mid=[];occupied=[];street_counts={}
def crowd(pos,yaw=None,dynamic=False):
 yaw=R.random()*math.tau if yaw is None else yaw;s=R.uniform(.88,1.12);v=R.randrange(4)
 if dynamic:
  ob=bpy.data.objects.new('V12 circulating citizen '+str(len(mid)),lod_meshes[v]);scene.collection.objects.link(ob);ob.location=pos;ob.rotation_euler.z=yaw;ob.scale=(s,)*3
  mid.append({'name':ob.name,'base':list(pos),'yaw':yaw,'phase':R.random()*math.tau,'speed':R.uniform(.12,.28),'span':R.uniform(.8,2.2)})
 else:far.append(templates[v],pos,yaw,s)
 occupied.append(pos)
bins={};placed=0
while placed<3900:
 x=R.uniform(-6.8,6.8);y=R.uniform(141,1785)
 if abs(y-150)<2 and abs(x)>3.6:continue
 key=(int(x),int(y));neighbours=[p for dx in [-1,0,1] for dy in [-1,0,1] for p in bins.get((key[0]+dx,key[1]+dy),[])]
 if any((x-p[0])**2+(y-p[1])**2<.78**2 for p in neighbours):continue
 bins.setdefault(key,[]).append((x,y));placed+=1
 crowd((x,y,.06),R.choice([0,math.pi])+R.uniform(-.65,.65),y<420)
street_counts['processional_avenue']=len(occupied)
crossings=[170,234]+list(range(310,1800,76))
for y in crossings:
 for x0 in np.arange(-245,246,3.2):
  if abs(x0)<8 or 21<x0<44:continue
  for k in range(R.choice([1,1,2])):
   x=x0+R.uniform(-.8,.8);yy=y+R.uniform(-1.8,1.8)
   crowd((x,yy,.05),R.choice([-math.pi/2,math.pi/2])+R.uniform(-.5,.5),y<250 and abs(x)<110)
street_counts['cross_streets']=len(occupied)-street_counts['processional_avenue']
# Citizens on bridge decks connect both banks; correct elevation on solid ramps.
for y in [32,108,170,234,310,386]:
 for x in np.arange(21.3,45,.95):
  yy=y+R.uniform(-1.25,1.25)
  z=.06 if x<20.8 or x>45.2 else .06+(x-20.8)/2*1.39 if x<22.8 else 1.45 if x<=43.2 else 1.45-(x-43.2)/2*1.39
  crowd((x,yy,z+.015),R.choice([-math.pi/2,math.pi/2])+R.uniform(-.20,.20),False)
# Far quays carry workers and trade traffic too.
for x in [20.7,45.2]:
 for y in np.arange(161,900,4.2):crowd((x+R.uniform(-1.0,1.0),y+R.uniform(-1,1),.07),R.choice([0,math.pi])+R.uniform(-.6,.6),y<350)
far.bake('V12 continuous distant city crowds')
scene['v12_mid_crowd']=json.dumps(mid)
stage('avenue_crossings_and_quays_populated_'+str(len(occupied)))

# Paint and furnish all visible river craft without changing the existing hull paths.
boats=[bpy.data.objects[n] for n in json.loads(scene['v8_boats'])]
for i,par in enumerate(boats):
 hull=next(o for o in par.children if o.name.startswith('Carvel wooden'))
 hull.data=hull.data.copy();hull.data.materials.clear();hull.data.materials.append([teal,ochre,lapis,teal][i])
 sail=next(o for o in par.children if o.name.startswith('V8 woven square sail'))
 sail.data=sail.data.copy();sail.data.materials.clear()
 for mat in [ivory,[lapis,ochre,teal,ochre][i]]:sail.data.materials.append(mat)
 for p in sail.data.polygons:p.material_index=1 if (p.index%12) in [0,1,10,11] or p.index//12 in [0,7] else 0
 m=Mesh();s=[.65,.7,.65,.6][i];L=4.5*s
 for side in [-1,1]:
  for j in range(14):
   y=-L+(j+.5)*2*L/14;w=1.25*s*max(.12,1-(y/L)**2)**.5
   m.rod((side*w,y-L/14,.98*s),(side*w,y+L/14,.98*s),.036,gold)
  m.rod((side*.70*s,-2.0*s,.9*s),(side*.18*s,0,4.65*s),.014,cord)
  m.rod((side*.70*s,2.0*s,.9*s),(side*.18*s,0,4.65*s),.014,cord)
 for y in [-2.5*s,2.5*s]:
  m.rod((0,y,.7*s),(0,y,1.5*s),.065,wood);m.ball((0,y,1.53*s),(.11,.15,.12),gold,12,6)
 for j in range(6):m.box((0,(-2.5+j)*s,.80*s),(1.15*s,.43*s,.07*s),wood)
 ob=m.bake('V12 painted rails rigging and deck '+str(i));ob.parent=par
 for j,(x,y) in enumerate([(-.14,-2.4*s),(.17,2.25*s)]):
  p=person('crew',(x,y,.81*s),0 if j else math.pi,'aboard',boat=par.name);p.parent=par;p.scale=(.73,)*3
 # Sweeps and steering oar, visible beyond the hull.
 m=Mesh();m.rod((.27,2.1*s,1.35*s),(1.5,3.4*s,-.05),.028,wood);m.box((1.5,3.4*s,-.08),(.16,.5,.035),ochre)
 ob=m.bake('V12 merchant steering sweep '+str(i));ob.parent=par

# Two tow teams move with their boats. Individual y spacing and x offsets vary.
# The larger local barges receive paint as well, so colour remains visible in
# the canal's focused region rather than only on the background square sailers.
for i,ob in enumerate([o for o in scene.objects if o.name.startswith('Carvel wooden') and (not o.parent or not o.parent.name.startswith('V8 animated'))]):
 ob.data=ob.data.copy();ob.data.materials.clear();ob.data.materials.append([teal,lapis,ochre,teal][i%4])
for i,ob in enumerate([o for o in scene.objects if o.name.startswith('Raised boat gunwale')]):
 ob.data=ob.data.copy();ob.data.materials.clear();ob.data.materials.append(gold if i%2 else ochre)
for i,ob in enumerate([o for o in scene.objects if o.name.startswith('V9 bound woven cargo bale')]):
 if i%4==0:
  ob.data=ob.data.copy();ob.data.materials.clear();ob.data.materials.append(navy if i%8 else red)
m=Mesh()
for x in [33.45,34.55]:
 for y in [88.4,89.8]:m.rod((x,y,.68),(x,y,2.5),.035,wood)
m.box((34,89.1,2.5),(1.25,1.6,.06),ochre)
ob=m.bake('V12 barge sun awning');ob.parent=bpy.data.objects['Animated canal boat']
tows=[]
# The old x=20.6 quay route ran behind the house wings and below the coping.
# A continuous paved towpath rests on the real quay cap, with two passing lanes.
m=Mesh();quay_material=bpy.data.objects['Continuous quay cap'].data.materials[0]
m.box((23.35,68,.965),(1.8,164,.38),quay_material)
m.bake('V12 continuous raised paved towpath')
for index,par in enumerate([boats[0],bpy.data.objects['Animated canal boat']]):
 bank=23.0 if index==0 else 23.7;local=(0,1.8,.95) if index==0 else (34,84.8,1.0)
 cu=bpy.data.curves.new('V12 working tow rope','CURVE');cu.dimensions='3D';cu.bevel_depth=.035;cu.bevel_resolution=2
 sp=cu.splines.new('POLY');sp.points.add(11);cu.materials.append(cord)
 ro=bpy.data.objects.new('V12 boat to towpath rope '+str(index),cu);scene.collection.objects.link(ro)
 team=[]
 for j in range(4):
  p=person('towman',(bank+R.uniform(-.07,.07),0,1.17),math.pi if index==0 else 0,'tow',boat=par.name,tow_index=index,offset=4.8+j*1.05)
  team.append(p.name)
 tows.append({'boat':par.name,'rope':ro.name,'bank':bank,'attachment':list(local),'team':team,'direction':1 if index==0 else -1})
scene['v12_special']=json.dumps(special);scene['v12_tows']=json.dumps(tows)
scene['city_version']='v12';scene['v12_scope']='Priests, Babylonian guards/patrol, Egyptian embassy, continuous avenue crowds and painted crewed river craft with tow teams.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'babylon-city-v12.blend'))
report={'roles':role_counts,'reassigned':assigned,'special_characters':len(special),'continuous_road_citizens':len(occupied),'individually_moving_mid_distance':len(mid),'street_counts':street_counts,'removed_old_actors_for_interaction_space':removed,'remaining_v11_actors':len(keep),'boats_refined':4,'tow_teams':2,'source':'v11 geometry, v11 traffic cache and original modeled role modules','historical_scope':'Babylon inspired fantasy. Garments and diplomatic scenario are artistic interpretations, not a specific documented visit.'}
(QA/'model-evidence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
stage('model_saved')
