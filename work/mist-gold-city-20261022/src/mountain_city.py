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
exec(compile((ROOT/'src/organic_city.py').read_text(encoding='utf8'),str(ROOT/'src/organic_city.py'),'exec'))
