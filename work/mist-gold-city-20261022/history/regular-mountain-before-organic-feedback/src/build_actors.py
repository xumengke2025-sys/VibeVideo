"""Executed by build_world: actors and mechanical assets with stable topology."""
def person(role,phase=0,variant=0,lod=False,wave=0):
 m=Mesh();cloth=M[['navy','wine','cream','oak','slate','brick'][variant%6]];skin=M['skin'];a=math.sin(phase);n=6 if lod else 10
 if role=='monk':cloth=M['wood']
 # Coats, breeches, waistcoat, stockings, buckled shoes.
 skirt=role in ['lady','monk'];hem=.18 if skirt else .65
 m.ring((0,0,hem),[(.32 if skirt else .23,0),(.24,.5),(.21,1.30-hem)],cloth,n,.76)
 m.ball((0,0,1.22),(.225,.15,.21),cloth,n,5)
 if not lod:m.box((0,.145,1.13),(.20,.035,.33),M['cream'])
 for side in [-1,1]:
  # Grounded alternating stance, swing lift. Local forward +Y.
  p=(phase/math.tau+(0 if side==1 else .5))%1
  if p<.62:fy=.29-.58*p/.62;lift=0
  else:u=(p-.62)/.38;fy=-.29+.58*(u*u*(3-2*u));lift=.14*math.sin(math.pi*u)
  knee=(side*.105,fy*.4,.43+lift*.5);foot=(side*.11,fy,.08+lift)
  m.rod((side*.11,0,.78),knee,.068,cloth,n=n);m.rod(knee,foot,.05,M['cream'],n=n);m.ball((foot[0],foot[1]+.055,foot[2]),(.078,.14,.054),M['leather'],n,4)
  shoulder=(side*.22,0,1.30);elbow=(side*.30,-side*a*.10,1.06);hand=(side*.25,-side*a*.18,.85)
  if role=='worker':elbow=(side*.3,.14,1.03);hand=(side*.23,.25,1.10)
  if wave and side==1:elbow=(.35,.02,1.58);hand=(.42+.10*math.sin(phase*2),.05,1.95)
  m.rod(shoulder,elbow,.065,cloth,n=n);m.rod(elbow,hand,.05,cloth,n=n);m.ball(hand,(.055,.05,.07),skin,n,4)
 m.rod((0,0,1.34),(0,0,1.48),.07,skin,n=n);m.ball((0,0,1.60),(.13,.12,.17),skin,n,6)
 if not lod:
  m.ball((0,.12,1.60),(.035,.045,.045),skin,8,4)
  for side in [-1,1]:m.ball((side*.05,.111,1.63),(.016,.012,.012),M['dark'],6,3)
 if role=='monk':m.ball((0,-.025,1.63),(.16,.12,.19),cloth,8,5);m.ball((0,.06,1.61),(.11,.08,.14),skin,8,5)
 elif role=='lady':m.ring((0,0,1.71),[(.24,0),(.25,.05),(.15,.07),(.1,.16),(0,.16)],M['cream'],n)
 elif role=='worker':m.ring((0,0,1.72),[(.17,0),(.17,.05),(.14,.12),(0,.12)],cloth,n);m.box((0,.16,.95),(.29,.035,.48),M['cream'])
 else:
  m.ring((0,0,1.71),[(.24,0),(.24,.05),(.14,.06),(.13,.18),(0,.18)],M['dark'],n)
  if not lod:
   for i in range(3):
    a=i*math.tau/3;m.rod((.24*math.cos(a),.24*math.sin(a),1.75),(.24*math.cos(a+2.1),.24*math.sin(a+2.1),1.75),.04,M['brass'],n=4)
 if role=='worker' and variant%3==0:
  m.rod((-.62,.08,1.39),(.62,.08,1.39),.032,M['oak'])
  for x in [-.58,.58]:m.rod((x,.08,1.38),(x,.08,.6),.012,M['oak'],n=4);m.ring((x,.08,.39),[(.16,0),(.21,.25),(.0,.25)],M['oak'],8)
 return m
def morph_actor(name,role,variant=0,lod=False,waving=False):
 ob=person(role,0,variant,lod).bake(name);ob.shape_key_add(name='Basis');count=6
 for k in range(1,count):
  mm=person(role,k*math.tau/count,variant,lod);key=ob.shape_key_add(name='Stride '+str(k));key.data.foreach_set('co',[x for p in mm.v for x in p])
 if waving:
  # Wave shape replaces right arm; same topology.
  mm=person(role,.5,variant,lod,1);key=ob.shape_key_add(name='Wave');key.data.foreach_set('co',[x for p in mm.v for x in p])
  mm=person(role,2.1,variant,lod,1);key=ob.shape_key_add(name='Wave alternate');key.data.foreach_set('co',[x for p in mm.v for x in p])
 return ob
traffic=[];prototypes={}
for i in range(12):
 role=['gentleman','lady','worker','monk'][i%4];ob=morph_actor('Hidden shared distant actor '+str(i),role,i,True);ob.hide_render=True;ob.hide_viewport=True;prototypes[i]=ob.data
for i in range(760):
 close=i<210
 side=-1 if i%2 else 1
 if close:
  y=R.uniform(-55,170);x=side*R.choice([17.3,19.2,62.7]);speed=R.uniform(.45,.95);axis='y'
 else:
  y=R.uniform(-70,575);x=side*(R.choice([24,58,92,126,160,194,228,262]) + R.choice([-4.3,4.3]));speed=R.uniform(.45,1.1);axis='y'
 if i%5==0:
  y=18+36*R.randrange(-2,13)+R.choice([-4.5,4.5]);x=side*R.uniform(22,260);axis='x'
  if side<0 and 30<y<113:y=126+R.choice([-4.5,4.5])
 if axis=='y' and abs(x)<20 and abs(y-18)<8:y+=17
 role=['gentleman','lady','worker','monk'][i%4]
 if close:ob=morph_actor('Resident %03d'%i,role,i)
 else:ob=bpy.data.objects.new('Distant resident %03d'%i,prototypes[i%12]);sc.collection.objects.link(ob)
 direction=R.choice([-1,1]);scale=R.uniform(.89,1.08);ob.scale=(scale,scale,scale);ob.location=(x,y,2.27)
 # Non-wrapping tracks: actors move through open corridors, pauses differ.
 data={'name':ob.name,'base':[x,y,2.27],'axis':axis,'direction':direction,'speed':speed,'phase':R.random()*math.tau,'close':close,'pause':R.uniform(10,72) if i%7==0 else -100,'duration':R.uniform(2,7),'role':role}
 traffic.append(data)
# Near-bridge spectators remain on quays while long-distance city life continues.
for i in range(10):
 ob=morph_actor('Bridge spectator %02d'%i,['worker','gentleman','lady'][i%3],i);ob.location=(-22.5-i*.85,20.7,2.27) if i<5 else (-17.3,10-(i-5)*1.3,2.27);ob.rotation_euler.z=-math.pi/2
 traffic.append({'name':ob.name,'base':list(ob.location),'axis':'x','direction':1,'speed':.85,'phase':i*.8,'close':True,'watcher':True,'crossing':i<5})
for by in [-54,126,234,378]:
 for i in range(8):
  ob=morph_actor('Stone bridge walker %s %s'%(by,i),'gentleman' if i%3 else 'lady',i,True);direction=1 if i%2 else -1
  traffic.append({'name':ob.name,'base':[-direction*(35+i*2.6),by+direction*1.8,2.25],'axis':'x','direction':direction,'speed':.48,'phase':i,'close':True,'pause':-100,'duration':0,'stone_bridge':by})
foreman=morph_actor('Bridge traffic foreman','worker',0,waving=True);foreman.location=(-18.4,14.1,2.3);foreman.rotation_euler.z=math.pi/2
sc['traffic']=json.dumps(traffic)
# Horses and carriages are articulated; wheels are true rotating spoked wheels.
def horse(parent,x,y,variant=0):
 root=empty('Horse body '+str(variant),(x,y,0),parent);m=Mesh();coat=M['wood'] if variant%2 else M['oak']
 m.ball((0,0,1.40),(.40,.94,.48),coat,16,8);m.rod((0,.55,1.5),(0,.94,2.13),.30,coat,.22,14);m.ball((0,1.13,2.10),(.23,.48,.28),coat,12,7);m.ball((0,1.48,1.98),(.20,.21,.19),coat,10,6)
 for side in [-1,1]:
  m.rod((side*.12,.96,2.29),(side*.16,.96,2.62),.07,coat,.012,8);m.ball((side*.21,1.10,2.17),(.028,.036,.029),M['dark'],8,4)
 m.rod((0,-.75,1.55),(0,-1.21,.70),.11,M['dark'],.025,10)
 m.rod((0,.62,1.78),(0,.84,2.29),.1,M['dark']);m.ring((0,0,1.77),[(.38,0),(.34,.06)],M['leather'],12,1.8)
 for yy in [.8,1.36]:m.rod((-.23,yy,1.98),(.23,yy,1.98),.025,M['leather'])
 ob=m.bake('Horse torso head harness '+str(variant));ob.parent=root
 for side in [-1,1]:
  for fore in [-1,1]:
   hip=empty('Horse leg %s %s %s'%(variant,side,fore),(side*.25,fore*.57,1.36),root);m=Mesh();m.rod((0,0,0),(0,.03,-.59),.10,coat,.063,10);m.rod((0,.03,-.59),(0,.0,-1.24),.063,coat,.045,10);m.box((0,.06,-1.28),(.16,.23,.13),M['dark']);ob=m.bake('Horse articulated limb');ob.parent=hip;hip['side']=side;hip['fore']=fore
 # Traces and reins remain parented to the vehicle and attached to bridle.
 for side in [-1,1]:curve('Harness trace',[(x+side*.27,y+.78,1.86),(x+side*.35,y-.8,1.42),(x+side*.4,-.65,1.18)],.018,M['leather'],parent)
 return root
def carriage(name,paint,scale=1):
 root=empty(name);m=Mesh();m.box((0,0,1.28),(1.75,3.15,.22),M['wood']);m.box((0,-.2,2.25),(1.62,2.25,1.70),paint);m.box((0,-.2,3.12),(1.85,2.52,.20),M['dark'])
 for side in [-1,1]:
  m.box((side*.825,-.17,2.57),(.04,1.25,.66),M['glass']);m.box((side*.86,-.17,2.13),(.06,1.32,.10),M['brass']);m.box((side*.90,-.15,1.1),(.34,1.75,.12),M['wood'])
  for yy in [-.87,.53]:m.rod((side*.85,yy,2.14),(side*.85,yy,2.96),.04,M['brass'])
  m.rod((side*.66,.6,1.1),(side*.66,4.6,1.2),.055,M['oak'])
  m.box((side*.81,1.35,2.1),(.22,.24,.37),M['brass']);m.box((side*.81,1.36,2.1),(.15,.25,.25),M['cream'])
 m.box((0,1.35,1.9),(1.55,.55,.18),M['leather']);m.box((0,-1.5,1.75),(1.4,.55,.55),M['oak']);m.bake(name+' body').parent=root
 for side in [-1,1]:
  for yy in [-1.15,1.08]:
   wheel=empty(name+' wheel',(side*1.03,yy,.72),root);m=Mesh()
   for j in range(24):
    a=j*math.tau/24;b=(j+1)*math.tau/24;m.rod((0,.69*math.sin(a),.69*math.cos(a)),(0,.69*math.sin(b),.69*math.cos(b)),.055,M['iron']);
   for j in range(12):a=j*math.tau/12;m.rod((0,0,0),(0,.67*math.sin(a),.67*math.cos(a)),.034,M['oak'])
   m.rod((-.13,0,0),(.13,0,0),.14,M['brass']);m.bake(name+' spoked wheel').parent=wheel
 for j,x in enumerate([-.57,.57]):horse(root,x,3.3,j)
 driver=person('gentleman',0,1);ob=driver.bake(name+' seated driver');ob.parent=root;ob.location=(0,1.35,1.22);ob.scale=(.85,.85,.85)
 for x in [-.57,.57]:curve('Driver rein',[(0,1.55,2.22),(x,2.6,1.98),(x,4.66,2.03)],.012,M['leather'],root)
 root.scale=(scale,scale,scale);return root
coach=carriage('Burgundy Royal Mail coach',M['wine']);coach.rotation_euler.z=-math.pi/2
others=[]
for i in range(14):
 ob=carriage('City carriage %02d'%i,M[['navy','wood','cream','slate'][i%4]],.9);x=R.choice([-1,1])*R.choice([24,58,92,126]);y=R.uniform(-65,430);direction=R.choice([-1,1]);others.append({'name':ob.name,'x':x,'y':y,'direction':direction,'speed':R.uniform(.75,1.5)})
sc['carriages']=json.dumps(others)
# Bell barge: keel and layered planks, cargo firmly inside hull.
def boat(name,bell=False,sail=False):
 root=empty(name);m=Mesh()
 for z,w,L in [(-.4,1.6,4.6),(-.1,2.05,5.2),(.3,2.35,5.65),(.7,2.38,5.65)]:
  points=[(-w,-L*.72,z),(-w*.52,-L,z),(0,-L*1.08,z),(w*.52,-L,z),(w,-L*.72,z),(w,L*.72,z),(w*.52,L,z),(0,L*1.08,z),(-w*.52,L,z),(-w,L*.72,z)]
  if z==-.4:previous=points
  else:m.add(previous+points,[(j,(j+1)%10,(j+1)%10+10,j+10) for j in range(10)],M['wood']);previous=points
 for i in range(23):m.box((0,-4.9+i*.44,.43),(4,.42,.12),M['oak'])
 for side in [-1,1]:m.rod((side*2.28,-4.4,.73),(side*2.28,4.4,.73),.09,M['brass'])
 for y in [-3,2.7]:
  for x in [-1.4,1.4]:barrel(m,(x,y,.5),.8)
 if bell:
  m.box((0,-.4,.75),(2.5,2.7,.5),M['wood']);m.ring((0,-.4,1),[(1.25,0),(1.4,.12),(1.32,.28),(1,.48),(.8,1.4),(.64,1.85),(.26,2.1),(.0,2.1)],M['brass'],48)
  m.ring((0,-.4,1.17),[(1.37,0),(1.37,.07)],M['brass'],48);m.rod((0,-.4,3.1),(0,-.4,3.45),.10,M['brass'])
  # Shipping gantry and flag are higher than closed bridge clearance.
  for x in [-1.7,1.7]:m.rod((x,-1.6,.5),(x,-1.6,4.3),.13,M['oak']);m.rod((x,1,.5),(x,-1.6,4.0),.065,M['iron'])
  m.rod((-1.9,-1.6,4.3),(1.9,-1.6,4.3),.14,M['oak']);m.rod((0,-1.6,4.15),(0,-.4,3.42),.04,M['iron'])
  m.rod((1.5,-3.4,.5),(1.5,-3.4,5.7),.045,M['wood'])
 else:
  for x in [-1.4,1.4]:m.rod((x,-1,.5),(x,-1,2.3),.05,M['oak']);m.rod((x,2,.5),(x,2,2.3),.05,M['oak'])
  m.add([(-1.6,-1.5,2.2),(0,-1.5,2.7),(1.6,-1.5,2.2),(-1.6,2.5,2.2),(0,2.5,2.7),(1.6,2.5,2.2)],[(0,1,4,3),(1,2,5,4)],M['cream'])
 if sail:
  m.rod((0,0,.4),(0,0,10.5),.1,M['wood']);m.rod((-2.7,0,8),(2.7,0,8),.065,M['wood']);m.add([(-2.6,0,8),(2.6,0,8),(2.2,.4,3),(-2.2,.4,3),(0,1,5.5)],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],M['cream'])
 m.bake(name+' hull cargo and equipment').parent=root
 crew=morph_actor(name+' crew','worker',2,waving=bell);crew.parent=root;crew.location=(-.8,3.8,.5)
 return root
barge=boat('Navy flag bell barge',True);flag=Mesh();flag.add([(1.5+i*.10,-3.4,5.6-j*.30) for j in range(3) for i in range(13)],[(j*13+i,j*13+i+1,(j+1)*13+i+1,(j+1)*13+i) for j in range(2) for i in range(12)],M['navy']);flag.bake('Deep blue small flag').parent=barge
boats=[]
for i,(x,y,sail) in enumerate([(-4,-28,True),(4,84,False),(-4,178,True),(4,285,False),(-3,450,True)]):
 ob=boat('Harbour vessel %02d'%i,False,sail);ob.location=(x,y,.05);boats.append({'name':ob.name,'x':x,'y':y,'moored':sail,'phase':i})
sc['boats']=json.dumps(boats)
# Steam volumes emerge from a finite list of equipment outlets, dissipate downwind.
steam=bpy.data.materials.new('Soft steam');steam.use_nodes=True;nt=steam.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');vol=nt.nodes.new('ShaderNodeVolumePrincipled');vol.inputs['Density'].default_value=.14;vol.inputs['Color'].default_value=(.8,.84,.85,1);nt.links.new(vol.outputs['Volume'],out.inputs['Volume'])
puffs=[]
for k,origin in enumerate([(17,-13,8.5),(44,-21,21.4),(44,13,21.4),(46,53,21.4)]):
 for j in range(6):
  m=Mesh();m.ball((0,0,0),(1,1,1),steam,10,6);ob=m.bake('Steam puff %s %s'%(k,j));puffs.append({'name':ob.name,'origin':origin,'phase':j/6,'seed':k})
sc['steam']=json.dumps(puffs);stage('inhabitants ships and vehicles')
