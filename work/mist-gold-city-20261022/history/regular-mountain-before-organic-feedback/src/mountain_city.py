"""Executed in world builder. Actual relief, leveled plots, varied 1700s forms."""
from terrain import ground_z,plot_z
for key,col in [('ochre','c9a474'),('plaster','d8c9ae'),('rose','b88b76'),('ivory','e2d5b8'),('shale','5c696a'),('rock','8a8b77')]:M[key]=material(key,col,.83,0,12)
def hip_roof(m,w,d,z,h,mat,mansard=False):
 if mansard:
  rings=[(w,d,z),(w*.76,d*.78,z+h*.72),(w*.74,d*.76,z+h*.80)]
  vs=[(sx*ww/2,sy*dd/2,zz) for ww,dd,zz in rings for sx,sy in [(-1,-1),(1,-1),(1,1),(-1,1)]]
  m.add(vs,[(j*4+i,j*4+(i+1)%4,(j+1)*4+(i+1)%4,(j+1)*4+i) for j in range(2) for i in range(4)]+[(8,9,10,11)],mat)
  for x in [-w*.27,0,w*.27]:
   m.box((x,-d*.43,z+h*.40),(1.1,.9,1.4),M['trim']);window(m,x,-d*.43-.46,z+h*.40-.5,.64,.94);m.append(gable_cap(1.4,1.1,.55),(x,-d*.43,z+h*.40+.75))
 else:
  m.add([(-w/2,-d/2,z),(w/2,-d/2,z),(w/2,d/2,z),(-w/2,d/2,z),(0,-d*.25,z+h),(0,d*.25,z+h)],[(0,1,4),(1,2,5,4),(2,3,5),(3,0,4,5)],mat)
  m.rod((0,-d*.25,z+h),(0,d*.25,z+h),.1,M['trim'])
def elegant_house(w,d,h,v=0,detail=True):
 m=Mesh();wall=M[['stone','plaster','brick','ochre','rose','ivory','stone'][v%7]]
 m.box((0,0,h/2),(w,d,h),wall);m.box((0,0,.35),(w+.22,d+.22,.7),M['stone'])
 if not detail:
  for z in [h,3.7,7.3]:
   if z<=h:m.box((0,0,z),(w+.22,d+.22,.18),M['trim'])
  for side in [-1,1]:
   for xx in [-w*.28,0,w*.28]:
    for zz in [1.9,5.2,8.5,11.8]:
     if zz<h-1:m.box((xx,side*(d/2+.025),zz),(1.0,.04,1.6),M['glass'])
  if v%3:roof(m,w+.3,d+.3,h,2.5+(v%3)*.4,M['roof'] if v%2 else M['slate'])
  else:hip_roof(m,w+.3,d+.3,h,3,M['slate'])
  m.box((w*.23,d*.17,h+1.9),(.7,.8,2.8),M['brick']);return m
 for z in [h-.3,h]:m.box((0,0,z),(w+.44,d+.44,.22),M['trim'])
 floors=max(2,int(h/3.2));n=max(2,round(w/2.5));step=(h-1.3)/floors
 for face in [0,math.pi]:
  f=Mesh()
  for row in range(floors):
   for k in range(n):
    xx=(k-(n-1)/2)*w/(n+.3);zz=1.05+row*step
    if row==0 and k==n//2:continue
    window(f,xx,-d/2-.045,zz,min(1.15,w/(n+1)*.54),1.55 if row else 1.85,detail and (v%4==0 or row==0))
    if detail and row==1 and v%3==0:
     f.box((xx,-d/2-.40,zz-.1),(1.7,.75,.16),M['trim'])
     for dx in [-.7,-.35,0,.35,.7]:f.rod((xx+dx,-d/2-.75,zz),(xx+dx,-d/2-.75,zz+.65),.026,M['iron'],n=4)
     f.rod((xx-.8,-d/2-.75,zz+.65),(xx+.8,-d/2-.75,zz+.65),.04,M['iron'])
   f.box((0,-d/2-.06,row*step+.65),(w+.15,.16,.10),M['trim'])
  arch(f,0,-d/2-.08,0,1.6,2.8,M['wood']);f.box((0,-d/2-.36,.10),(2,.72,.2),M['stone'])
  if detail:
   for xx in [-w/2+.22,w/2-.22]:
    f.box((xx,-d/2-.07,h/2),(.30,.22,h),M['trim'])
    for z in range(1,int(h)):f.box((xx,-d/2-.16,z),(.48,.16,.23),M['trim'])
   f.rod((w/2-.16,-d/2-.19,.3),(w/2-.16,-d/2-.19,h),.055,M['copper'])
  m.append(f,rot=face)
 for side in [-1,1]:
  for yy in [-d*.26,d*.26]:
   for k in range(floors):m.box((side*(w/2+.025),yy,1.8+k*step),(.045,.90,1.55),M['glass'])
 roofmat=M[['roof','slate','roof','shale','copper'][v%5]]
 if v%5 in [0,3]:hip_roof(m,w+.5,d+.5,h,3.2,roofmat,v%5==0)
 else:roof(m,w+.5,d+.5,h,2.4+(v%3)*.7,roofmat)
 if detail and v%5==2:
  # Dutch/baroque shaped street gable with volutes and finial.
  for face in [-1,1]:
   f=Mesh();f.add([(-w*.44,face*(d/2+.12),h),(w*.44,face*(d/2+.12),h),(w*.21,face*(d/2+.12),h+2.2),(0,face*(d/2+.12),h+3.4),(-w*.21,face*(d/2+.12),h+2.2)],[(0,1,2,3,4)],wall)
   for sx in [-1,1]:f.ball((sx*w*.28,face*(d/2+.14),h+.8),(.4,.18,.4),M['trim']);f.rod((sx*w*.43,face*(d/2+.15),h+.05),(0,face*(d/2+.15),h+3.45),.12,M['trim'])
   f.ball((0,face*(d/2+.14),h+3.7),(.2,.2,.3),M['brass']);m.append(f)
 for xx in [-w*.27,w*.27]:
  m.box((xx,d*.15,h+1.5),(.65,.8,2.8),M['brick']);m.box((xx,d*.15,h+2.95),(.82,.96,.18),M['trim'])
 return m
def terrace_base(m,x,y,w,d,z):
 low=min(ground_z(x+dx,y+dy) for dx in [-w/2,w/2] for dy in [-d/2,d/2])-.25
 m.box((x,y,(low+z)/2),(w,d,z-low),M['stone']);m.box((x,y,z),(w+.3,d+.3,.16),M['trim'])
 for zz in range(int(low)+1,int(z)):
  m.box((x,y-d/2-.015,zz),(w,.025,.032),M['rock'])
  if z-low>4 and zz%3==0:
   for xx in range(int(x-w/2)+1,int(x+w/2),3):m.box((xx,y-d/2-.03,zz+.5),(.035,.035,1),M['rock'])
def place_house(batch,x,y,w,d,h,v,detail=True,rotation=0):
 z=plot_z(x,y,w,d);terrace_base(batch,x,y,w+.4,d+.4,z);batch.append(elegant_house(w,d,h,v,detail),(x,y,z),rotation)
def palace(batch,x,y,w,d,h,v=0):
 z=plot_z(x,y,w,d);terrace_base(batch,x,y,w+2,d+2,z)
 batch.append(elegant_house(w,d*.27,h,v,True),(x,y-d*.36,z))
 for side in [-1,1]:batch.append(elegant_house(w*.22,d*.70,h-2,v+side,True),(x+side*w*.39,y+d*.13,z))
 batch.box((x,y,z+.13),(w*.54,d*.50,.2),M['pave'])
 batch.ring((x,y,z+.2),[(1.7,0),(1.7,.4),(1.5,.6),(0,.6)],M['trim'])
 # Central pediment and portico, true slender columns.
 for xx in [-3,-1,1,3]:batch.rod((x+xx,y-d/2-1,z),(x+xx,y-d/2-1,z+6),.24,M['trim'],.20,12)
 batch.box((x,y-d/2-1,z+6),(7.5,1.4,.5),M['trim']);batch.add([(x-4,y-d/2-1.8,z+6.2),(x+4,y-d/2-1.8,z+6.2),(x,y-d/2-1.8,z+8.3)],[(0,1,2)],M['trim'])
# Relief mesh: canal bed stays open; no scale-only terrain illusion.
base=Mesh();base.box((0,750,-6),(2800,2900,8),M['rock'])
for side in [-1,1]:
 for xx in range(10,651,6):
  for yy in range(-180,1651,9):
   vs=[(side*x,y,ground_z(side*x,y)-.12) for x,y in [(xx,yy),(xx+6,yy),(xx+6,yy+9),(xx,yy+9)]];base.add(vs,[(0,1,2,3)],M['grass'] if xx>300 else M['pave'],True)
 base.box((side*10,720,1.2),(2,1900,2.4),M['stone']);base.box((side*13.1,720,2.25),(6.2,1900,.18),M['trim'])
base.bake('01 Mountain relief and continuous valley quays')
water=Mesh();water.box((0,850,.02),(18,2200,.10),M['water']);water.bake('Canal water')
nt=M['water'].node_tree;p=nt.nodes.get('Principled BSDF');no=nt.nodes.new('ShaderNodeTexNoise');no.inputs['Scale'].default_value=3.4;bu=nt.nodes.new('ShaderNodeBump');bu.inputs['Strength'].default_value=.18;bu.inputs['Distance'].default_value=.10;nt.links.new(no.outputs['Fac'],bu.inputs['Height']);nt.links.new(bu.outputs[0],p.inputs['Normal'])
roads=Mesh()
for side in [-1,1]:
 for xx in [24,58,92,126,160,194,228,262,296,330,364,398,432,466,500,534,568]:
  for yy in range(-110,1500,4):
   # Cathedral closes two grid segments; its terrace has a peripheral promenade.
   if side<0 and xx==58 and 30<yy<113:continue
   roads.add([(side*x,y,ground_z(side*x,y)+.035) for x,y in [(xx-3.5,yy),(xx+3.5,yy),(xx+3.5,yy+4),(xx-3.5,yy+4)]],[(0,1,2,3)],M['road'])
 for yy in range(-90,1500,36):
  for xx in range(16,595,2):
   if side<0 and 26<xx<64 and 30<yy<110:continue
   roads.add([(side*x,y,ground_z(side*x,y)+.05) for x,y in [(xx,yy-3.5),(xx+2,yy-3.5),(xx+2,yy+3.5),(xx,yy+3.5)]],[(0,1,2,3)],M['road'])
roads.bake('02 Connected contour roads and climbing cross streets')
blocks=0;farcount=0
for side in [-1,1]:
 for ix in range(18):
  cx=side*(41+ix*34)
  for iy in range(48):
   cy=-72+iy*36
   if ix==0 and ((side==-1 and 25<cy<115) or (side==1 and -40<cy<70)):continue
   if ix==1 and side==1 and cy==-36:continue
   if side==-1 and ix in [3,4] and cy in [144,180]:continue
   # Open gardens interrupt the housing fabric; every skyline has measured gaps.
   if (ix*7+iy*3+(1 if side>0 else 0))%29==0:continue
   batch=Mesh();detail=abs(cx)<185 and cy<260
   # Masonry terrace faces hide raw slopes and carry an entire city block.
   tz=ground_z(cx,cy);edge=cx-side*13.1;low=min(tz,ground_z(cx-side*18,cy))
   if tz-low>1:
    batch.box((edge,cy,(tz+low)/2),(1.4,26,tz-low),M['stone']);batch.box((edge,cy,tz+.05),(1.8,26,.20),M['trim'])
    if detail:
     for yy in [-9,-3,3,9]:
      f=Mesh();arch(f,0,0,low+.3,3.5,max(2,tz-low-.6),M['wood']);batch.append(f,(edge-side*.72,cy+yy,0),-side*math.pi/2)
     for zz in range(int(low)+1,int(tz)):batch.box((edge-side*.73,cy,zz),(.02,26,.035),M['rock'])
   if (ix+iy*5+(3 if side>0 else 0))%13==0 and ix>0:
    palace(batch,cx,cy,24,24,R.uniform(10,17),blocks%7);blocks+=3
   elif (ix+iy*3)%3==0:
    for dx in [-8.4,0,8.4]:place_house(batch,cx+dx,cy,8.2,R.uniform(15,23),R.uniform(10,19),blocks,detail);blocks+=1
   else:
    for dx in [-6.4,6.4]:
     for dy in [-6.6,6.6]:
      w=R.uniform(7.6,10.5);d=R.uniform(8,11);h=R.uniform(7.5,16.2);place_house(batch,cx+dx,cy+dy,w,d,h,blocks,detail,math.pi if dy>0 else 0);blocks+=1
   batch.bake('Terraced %s district %02d %02d'%(side,ix,iy))
stage('mountain districts '+str(blocks));sc['distant_building_count']=farcount
# The ridge palace is a singular large composition, not another residential box.
m=Mesh();x,y=-160,162;z=plot_z(x,y,61,55);terrace_base(m,x,y,65,59,z)
m.append(elegant_house(56,15,19,0,True),(x,y+14,z))
for side in [-1,1]:
 m.append(elegant_house(15,43,17,4,True),(x+side*23,y-4,z))
 m.append(elegant_house(18,18,23,0,True),(x+side*23,y-21,z))
 for yy in range(-20,17,3):
  m.rod((x+side*14, y+yy,z+.2),(x+side*14,y+yy,z+7.4),.26,M['trim'],.21,12)
 m.box((x+side*14,y-2,z+7.7),(2.2,41,.45),M['trim'])
m.ring((x,y+14,z+19),[(5.5,0),(5.5,4),(5.9,4.4),(5.6,5),(4.8,8),(3,10.7),(.7,12),(.6,14),(0,15)],M['copper'],40)
m.box((x,y-4,z+.12),(26,25,.20),M['pave']);m.ring((x,y-5,z+.3),[(3,0),(3,.6),(2.6,.7),(0,.7)],M['trim'])
for xx in range(-28,29,4):
 m.rod((x+xx,y-29,z),(x+xx,y-29,z+1.4),.14,M['trim']);m.ball((x+xx,y-29,z+1.7),(.22,.22,.27),M['trim'])
m.rod((x-30,y-29,z+1.5),(x+30,y-29,z+1.5),.12,M['trim']);m.bake('Grand ducal ridge palace and court of arcades')
# Long, functioning retaining galleries connect the upper city visually and structurally.
g=Mesh()
for side,x,y0,y1 in [(-1,64,70,155),(-1,132,35,155),(1,96,62,186),(1,164,120,260)]:
 x*=side
 for y in range(y0,y1,7):
  z=ground_z(x,y);low=max(2.25,z-9);g.box((x,y,(z+low)/2),(2,1.2,z-low),M['stone'])
  for j in range(12):
   a=j*math.pi/12;b=(j+1)*math.pi/12;r=2.9;zc=z-3.5
   g.add([(x+side*.10, y+3.5+rr*math.cos(t),zc+rr*math.sin(t)) for rr,t in [(r,a),(r,b),(r+.55,b),(r+.55,a)]],[(0,1,2,3)],M['trim'])
  g.box((x,y+3.5,z+.25),(2.7,7.2,.6),M['trim']);g.rod((x,y,z+.5),(x,y,z+1.7),.11,M['trim']);g.rod((x,y,z+1.7),(x,y+7,z+1.7),.10,M['trim'])
g.bake('Upper city vaulted retaining galleries')
# Cypress gardens and planted edges visually soften the stepped masonry.
garden=Mesh()
for i in range(620):
 side=R.choice([-1,1]);ix=R.randrange(1,11);iy=R.randrange(0,30);x=side*(41+ix*34)+R.choice([-13.8,13.8]);y=-72+iy*36+R.choice([-13.5,13.5])
 if side<0 and -197<x<-123 and 123<y<198:continue
 if abs(y-18)<9:continue
 z=ground_z(x,y)+.05;h=R.uniform(4,8)
 garden.rod((x,y,z),(x,y,z+h*.65),.13,M['wood'],.065,6)
 for j in range(4):garden.ball((x+.12*math.sin(i+j),y+.12*math.cos(i-j),z+h*(.36+j*.15)),(.6+j*.04,.65,h*.28),M['leaf'],8,5)
garden.bake('Cypress gardens on planted terrace edges')
# Hilltop observatories, villas and chapels with distinct circular silhouettes.
for i,(x,y) in enumerate([(-111,144),(143,183),(-179,267),(212,365),(-245,520),(314,695)]):
 m=Mesh();z=plot_z(x,y,22,24);terrace_base(m,x,y,24,27,z)
 if i%2==0:
  m.ring((x,y,z),[(8,0),(8,12),(8.6,12.3)],M['stone'],32)
  for k in range(16):
   a=k*math.tau/16;m.rod((x+8.1*math.cos(a),y+8.1*math.sin(a),z+.5),(x+8.1*math.cos(a),y+8.1*math.sin(a),z+11.8),.32,M['trim'],.26,10)
  m.ring((x,y,z+12.5),[(8.5,0),(7.9,1),(7.1,4),(5.4,7),(2.8,9),(.6,9.8),(.5,12),(0,13)],M['copper'],32)
 else:palace(m,x,y,26,26,17,i)
 m.bake('Ridge rotunda or country palazzo '+str(i))
