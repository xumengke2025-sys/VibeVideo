"""Original editable alpine miniature world. Blender 4.5; metres; Z up.
No Babylon geometry is imported. Static meshes are grouped by real assembly.
"""
import bpy, math, random, json, sys
from pathlib import Path
from mathutils import Vector, Matrix
R=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(Path(__file__).parent))
rng=random.Random(221022)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for block in list(bpy.data.materials): bpy.data.materials.remove(block)
M=[]
def mat(name,color,rough=.65,metal=0,texture=None,emission=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 if emission:p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emission
 if texture:
  tc=n.new('ShaderNodeTexCoord');v=n.new('ShaderNodeVectorMath');v.operation='MULTIPLY';v.inputs[1].default_value=(2,30,5) if texture=='wood' else (8,8,8)
  l.new(tc.outputs['Generated'],v.inputs[0]);noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=4;noise.inputs['Detail'].default_value=3;l.new(v.outputs[0],noise.inputs['Vector'])
  ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.15;ramp.color_ramp.elements[1].position=.85
  ramp.color_ramp.elements[0].color=(*(c*.65 for c in color),1);ramp.color_ramp.elements[1].color=(*(min(1,c*1.2) for c in color),1);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
  bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.045 if texture=='stone' else .002 if texture=='metal' else .018;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
 M.append(m);return len(M)-1
SN=mat('Snow | cream crystalline surface',(.83,.87,.89),.82,texture='snow')
ST=mat('Blue grey masonry',(.27,.34,.39),.92,texture='stone')
MR=mat('Mortar',(.14,.19,.21),1)
WO=mat('Honey larch timber',(.29,.135,.055),.64,texture='wood')
DK=mat('Aged walnut beams',(.085,.039,.02),.72,texture='wood')
PL=mat('Lime plaster',(.66,.57,.40),.92,texture='stone')
SL=mat('Slate shingles',(.09,.14,.17),.68,texture='stone')
CU=mat('Verdigris copper',(.075,.24,.22),.46,.5,texture='metal')
BR=mat('Warm brushed brass',(.52,.33,.12),.31,.78,texture='metal')
IR=mat('Forged blue black iron',(.035,.052,.062),.38,.78)
GL=mat('Amber window light',(.98,.48,.12),.38,emission=2.1)
RD=mat('Burgundy painted cargo wood',(.27,.022,.035),.6,texture='wood')
GR=mat('Forest green carriage',(.026,.115,.073),.54,texture='wood')
SK=mat('Warm skin',(.56,.32,.20),.7)
WH=mat('Cream wool and apron',(.78,.73,.59),.9)
BL=mat('Indigo wool',(.07,.12,.19),.93)
BN=mat('Chestnut horse',(.19,.075,.028),.68)
BK=mat('Leather and dark mane',(.025,.019,.014),.65)
BD=mat('Golden sourdough crust',(.66,.30,.065),.85,texture='stone')
WA=mat('Mountain water',(.025,.16,.20),.22,.32)
IC=mat('Blue ice',(.42,.61,.66),.3,.1)
PN=mat('Evergreen needles',(.025,.10,.065),.92)
RO=mat('Wet cobblestones',(.22,.26,.27),.36,texture='stone')
EM=mat('Ivory enamel',(.88,.82,.64),.32)
def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)
def ground(x,y):return max(0,.12*(y+20))+2*smooth((y-12)/10)+.12*math.sin(x*.18)*math.sin(y*.12)
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.smooth_faces=[]
 def poly(self,v,f,ma):
  k=len(self.v);self.v+=list(v);self.f += [tuple(k+i for i in face) for face in f];self.mi += [ma]*len(f)
 def box(self,p,s,ma,rz=0,rx=0):
  rot=Matrix.Rotation(rz,3,'Z')@Matrix.Rotation(rx,3,'X');v=[tuple(Vector(p)+rot@Vector((i*s[0]/2,j*s[1]/2,k*s[2]/2))) for i,j,k in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
  self.poly(v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],ma)
 def rod(self,a,b,r,ma,n=10,r2=None):
  a,b=Vector(a),Vector(b);q=(b-a).to_track_quat('Z','Y');v=[]
  for p,rad in [(a,r),(b,r if r2 is None else r2)]:
   v += [tuple(p+q@Vector((rad*math.cos(i*math.tau/n),rad*math.sin(i*math.tau/n),0))) for i in range(n)]
  self.poly(v,[tuple(range(n-1,-1,-1)),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
 def ball(self,p,s,ma,n=12,rings=8):
  v=[(p[0]+s[0]*math.sin(j*math.pi/rings)*math.cos(i*math.tau/n),p[1]+s[1]*math.sin(j*math.pi/rings)*math.sin(i*math.tau/n),p[2]+s[2]*math.cos(j*math.pi/rings)) for j in range(rings+1) for i in range(n)]
  start=len(self.f);self.poly(v,[(j*n+i,(j+1)*n+i,(j+1)*n+(i+1)%n,j*n+(i+1)%n) for j in range(rings) for i in range(n)],ma);self.smooth_faces+=list(range(start,len(self.f)))
 def torus(self,p,major,minor,ma,rot=(0,0,0),n=32):
  rot=Matrix.Rotation(rot[2],3,'Z')@Matrix.Rotation(rot[1],3,'Y')@Matrix.Rotation(rot[0],3,'X');v=[]
  for i in range(n):
   a=i*math.tau/n
   for j in range(8):
    b=j*math.tau/8;v.append(tuple(Vector(p)+rot@Vector(((major+minor*math.cos(b))*math.cos(a),(major+minor*math.cos(b))*math.sin(a),minor*math.sin(b)))))
  self.poly(v,[(i*8+j,i*8+(j+1)%8,((i+1)%n)*8+(j+1)%8,((i+1)%n)*8+j) for i in range(n) for j in range(8)],ma)
 def path(self,pts,r,ma,n=8):
  for a,b in zip(pts,pts[1:]):self.rod(a,b,r,ma,n)
 def obj(self,name,parent=None,bevel=0):
  me=bpy.data.meshes.new(name);me.from_pydata(self.v,[],self.f);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o)
  for m in M:me.materials.append(m)
  for face,index in zip(me.polygons,self.mi):face.material_index=index
  for i in self.smooth_faces:me.polygons[i].use_smooth=True
  if parent:o.parent=parent
  if bevel:
   mod=o.modifiers.new('Hand finished edges','BEVEL');mod.width=bevel;mod.segments=2
  return o
def empty(name,p=(0,0,0),parent=None):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.location=p;o.parent=parent;return o
def text(body,p,size,ma,parent=None,name=None):
 cu=bpy.data.curves.new('Engraved lettering','FONT');cu.body=body;cu.align_x='CENTER';cu.size=size;cu.extrude=.004
 ob=bpy.data.objects.new(name or body,cu);bpy.context.collection.objects.link(ob);cu.materials.append(M[ma]);ob.location=p;ob.rotation_euler=(math.pi/2,0,0);ob.parent=parent;return ob
def snowroof(m,w,d,eave,rise,thick=.2):
 for sign in [-1,1]:
  v=[];nx=12;ny=8
  for j in range(ny+1):
   u=j/ny
   for i in range(nx+1):
    x=(i/nx-.5)*(w+.65);y=sign*u*(d/2+.4);z=eave+rise*(1-u)+thick+.045*math.sin(i*2.1+j*.8)+.04*math.cos(i*1.1-j)
    v.append((x,y,z))
  m.poly(v,[(j*(nx+1)+i,j*(nx+1)+i+1,(j+1)*(nx+1)+i+1,(j+1)*(nx+1)+i) for j in range(ny) for i in range(nx)],SN)
def house(name,x,y,w=4.5,d=4,h=4.6,rot=0,style=0):
 root=empty(name,(x,y,ground(x,y)));root.rotation_euler.z=rot;m=Mesh();base=1.45
 m.box((0,0,base/2),(w,d,base),MR)
 for side in [-1,1]:
  for row in range(4):
   for col in range(int(w/.62)):
    px=-w/2+(col+.5+(row%2)*.22)*w/int(w/.62)
    if abs(px)<w/2-.1:m.box((px,side*(d/2+.012),(row+.5)*.35),(.55,.08,.29),ST)
 m.box((0,0,(h+base)/2),(w,d,h-base),PL if style%3==0 else WO)
 if style%3:
  for j in range(int((h-base)/.19)):
   zz=base+j*.19
   for sg in [-1,1]:m.box((0,sg*(d/2+.025),zz),(w,.055,.025),DK)
 for z in [base,h-.25]:m.box((0,0,z),(w+.18,d+.16,.18),DK)
 for px in [-w/2+.1,0,w/2-.1]:
  for py in [-d/2-.04,d/2+.04]:m.box((px,py,(h+base)/2),(.16,.14,h-base),DK)
 # Close front gable, with visible timber rafters.
 rise=d*.67;ez=h
 m.poly([(-w/2,-d/2,h),(w/2,-d/2,h),(w/2,0,h+rise),(-w/2,0,h+rise),(-w/2,d/2,h),(w/2,d/2,h)],[(0,1,2,3),(3,2,5,4)],WO)
 for side in [-1,1]:
  sl=math.sqrt((d/2+.35)**2+rise**2);ang=side*-math.atan2(rise,d/2+.35)
  m.box((0,side*(d/4+.175),h+rise/2),(w+.65,sl,.16),CU if style%7==0 else SL,rx=ang)
  # Tile edges remain visible at eaves and under broken snow boundaries.
  for j in range(6):
   u=(j+.5)/6
   for i in range(int(w/.38)):
    px=(i+.5)*w/int(w/.38)-w/2
    m.box((px,side*u*(d/2+.35),h+rise*(1-u)+.08),(.35,sl/6-.02,.045),SL,rx=ang)
  for i in range(int(w*2)):
   if rng.random()<.48:
    xx=rng.uniform(-w/2,w/2);zz=h-.03;length=rng.uniform(.09,.38);m.rod((xx,side*(d/2+.32),zz),(xx,side*(d/2+.32),zz-length),.035,IC,7,r2=.006)
 snowroof(m,w,d,h,rise)
 # Dormer with tiny pitched snow cap.
 if w>4.2:
  m.box((.1,-d*.27,h+rise*.54),(.95,.75,.73),DK);m.box((.1,-d*.27-.39,h+rise*.54),(.52,.03,.48),GL)
  m.box((.1,-d*.27,h+rise*.54+.42),(1.1,.95,.16),SN,rx=.13)
 for px in [-w*.27,w*.27]:
  for z in [2.15,h-.85]:
   m.box((px,-d/2-.06,z),(.75,.12,1.02),DK);m.box((px,-d/2-.13,z),(.57,.025,.83),GL)
   m.box((px,-d/2-.16,z),(.045,.045,.85),BR);m.box((px,-d/2-.16,z),(.58,.045,.045),DK)
   m.box((px,-d/2-.16,z-.56),(1.0,.32,.11),WO);m.box((px,-d/2-.16,z-.47),(.92,.3,.08),SN)
   for sg in [-1,1]:m.box((px+sg*.48,-d/2-.08,z),(.22,.1,.9),GR if style%2 else DK)
 # Side windows in both directions.
 for sg in [-1,1]:
  m.box((sg*(w/2+.04),0,h-1),(.08,.8,1),DK);m.box((sg*(w/2+.09),0,h-1),(.03,.6,.78),GL)
 m.box((0,-d/2-.06,.85),(.86,.15,1.7),DK);m.box((0,-d/2-.15,1.25),(.52,.03,.42),GL);m.ball((.3,-d/2-.21,.8),(.04,.04,.04),BR)
 for j in range(3):m.box((0,-d/2-.2-j*.2,.15-j*.045),(1.2,.45,.22),ST)
 if style%2==0:
  z=2.8;m.box((0,-d/2-.6,z),(w*.8,1.3,.16),DK)
  for px in [i*w*.8/8-w*.4 for i in range(9)]:m.box((px,-d/2-1.13,z+.45),(.065,.075,.9),WO)
  m.box((0,-d/2-1.13,z+.9),(w*.85,.12,.12),WO);m.box((0,-d/2-1.13,z+.98),(w*.85,.13,.06),SN)
 cx=w*.3;cy=d*.12;m.box((cx,cy,h+rise+.15),(.6,.65,1.3),ST);m.box((cx,cy,h+rise+.85),(.86,.85,.15),SN)
 ob=m.obj(name+' | masonry, timber, shingles and snow',root,bevel=.018)
 smoke=empty(name+' chimney emitter',(cx,cy,h+rise+1),root);smoke['smoke']=True
 return root

# Continuous snowy terrain, with roads draped over the same height function.
m=Mesh();nx=100;ny=115;v=[]
for j in range(ny+1):
 y=-65+j*1.25
 for i in range(nx+1):
  x=-65+i*1.3;z=ground(x,y)+.11*math.sin(x*.43)*math.sin(y*.51)
  # River cut in the western valley.
  river=-20+3*math.sin(y*.07);z-=1.0*math.exp(-((x-river)/2.2)**4);v.append((x,y,z))
m.poly(v,[(j*(nx+1)+i,j*(nx+1)+i+1,(j+1)*(nx+1)+i+1,(j+1)*(nx+1)+i) for j in range(ny) for i in range(nx)],SN);m.obj('Continuous snow covered valley terrain')
# Large nonrepeating mountain ridges: real sculpted mesh, not a background card.
for k,(cx,cy,rad,peak) in enumerate([(-76,94,65,73),(25,124,71,105),(94,105,65,85),(-115,20,70,81),(125,45,70,97),(-4,180,85,123)]):
 m=Mesh();n=96;rings=64;v=[]
 for j in range(rings+1):
  u=j/rings;rr=rad*u
  for i in range(n):
   a=i*math.tau/n;warp=1+.16*math.sin(a*5+k)+.10*math.cos(a*9-k)
   x=cx+rr*math.cos(a)*warp;y=cy+rr*math.sin(a)*warp
   z=5+peak*(1-u)**1.65+(7*math.sin(a*7+u*5)+3*math.sin(a*13))*math.sin(math.pi*u)+2*math.sin(u*39+a*7)*u*(1-u)
   v.append((x,y,z))
 m.poly(v,[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(rings) for i in range(n)],SN)
 ob=m.obj('Snow massif %02d'%k)
 for f in ob.data.polygons:
  # Snow stays coherent across the ridge; no random face-wise rock patches.
  f.use_smooth=True

def roadmesh(points,width,name):
 m=Mesh();v=[]
 for i,p in enumerate(points):
  p=Vector(p);t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);t.z=0;t.normalize();n=Vector((-t.y,t.x,0))
  for s in [-1,1]:q=p+n*width/2*s;q.z=ground(q.x,q.y)+.11;v.append(tuple(q))
 m.poly(v,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(points)-1)],RO)
 # irregular snow clearance boundary and cart ruts
 for side in [-1,1]:
  ps=[]
  for i in range(0,len(points),2):
   q=Vector(v[i*2+(1 if side==1 else 0)]);q.z+=.08;ps.append(tuple(q))
  m.path(ps,.10,SN,6)
 m.obj(name)
def cat(points,steps=20):
 out=[];p=[Vector(points[0])]+[Vector(x) for x in points]+[Vector(points[-1])]
 for k in range(1,len(p)-2):
  a,b,c,d=p[k-1:k+3]
  for j in range(steps):
   t=j/steps;v=.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t);out.append(tuple(v))
 out.append(points[-1]);return out
route=cat([(14,-43,0),(12,-27,0),(3,-18,0),(-3,-10,0),(2,-5,0),(12,-5,0),(19,4,0),(19,15,0)],24)
route=[(x,y,ground(x,y)+.15) for x,y,z in route];roadmesh(route,3.5,'Continuous carriage road | 3.5m stone corridor')
cross=cat([(-21,0,0),(-12,-2,0),(0,-4,0),(10,-3,0)],20);roadmesh(cross,2.8,'Mill bridge to market lane')
upper=cat([(-24,24,0),(-12,20,0),(0,24,0),(15,23,0),(28,25,0)],20);roadmesh(upper,2,'Upper bakery lane | pedestrian access')
for yy in [-15,10,31]:roadmesh(cat([(-25,yy,0),(-8,yy+1,0),(7,yy-1,0),(27,yy,0)],16),1.7,'Pedestrian side lane '+str(yy))
# plaza flat-ish paving, stones with mortar seams
m=Mesh()
for j in range(23):
 for i in range(25):
  x=-5+i*.52;y=-4+j*.48
  if (x-1)**2+(y-1.5)**2<44:m.box((x,y,ground(x,y)+.13),(.48,.44,.13),RO)
m.obj('Clock square individual paving')
# Pedestrian stairs connect upper terrace without crossing carriage route.
m=Mesh()
for j in range(45):
 y=3+j*.38;z=ground(-8,y);m.box((-8,y,z+.12),(1.9,.42,.24),ST)
 for sg in [-1,1]:
  if j%5==0:m.rod((-8+sg,y,z),(-8+sg,y,z+.9),.055,DK)
for sg in [-1,1]:m.path([(-8+sg,3+j*.5,ground(-8,3+j*.5)+.9) for j in range(35)],.055,DK)
m.obj('Stepped pedestrian ascent with handrails')
# River and wooden footbridge.
m=Mesh();v=[]
for i in range(120):
 y=-50+i*.85;cx=-20+3*math.sin(y*.07)
 for sg in [-1,1]:v.append((cx+sg*1.3,y,ground(cx,y)-.65))
m.poly(v,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(119)],WA);m.obj('Flowing mountain leat')
m=Mesh();bz=ground(-20,0)+.35
for i in range(20):m.box((-23+i*.35,0,bz),( .32,2.4,.17),WO)
for sy in [-1.12,1.12]:
 for xx in [-23,-21.4,-19.8,-18.2,-16.6]:m.rod((xx,sy,bz), (xx,sy,bz+1),.065,DK)
 m.rod((-23.2,sy,bz+1),(-16.2,sy,bz+1),.08,WO)
m.obj('Timber bridge with rails')

# Explicit buildings arranged beside real lanes; no random road intersections.
houses=[(-13,25,6,4.7,5.3,0,'Bakery'),(-23,17,4.6,4,4.7,.08,'Mill house'),(-15,13,4.7,4,5.2,-.06,'Clockmaker'),(-18,6,4,3.6,4.5,.02,'Habitation'),(-13,-8,4.3,4,4.4,.12,'Habitation'),(-8,-16,4.5,4,4.7,-.1,'Habitation'),(14,-13,5.8,4.4,5.4,-.1,'Golden Pine Inn'),(25,-3,4.8,4,4.8,.17,'Grocer'),(26,15,4.4,4,4.5,.1,'Habitation'),(9,20,5,4.3,5,-.1,'Habitation'),(-2,28,4.7,4,5.2,.05,'Habitation')]
for row,yy in enumerate([-25,-12,8,19,31,41]):
 for xx in [-28,-21,-14,-5,3,11,20,29]:
  if any((xx-a[0])**2+(yy-a[1])**2<40 for a in houses):continue
  if any((xx-p[0])**2+(yy-p[1])**2<31 for p in route):continue
  if abs(xx-(-20+3*math.sin(yy*.07)))<4:continue
  if yy<13 and -8<xx<13:continue
  if yy>17 and -17<xx<-9:continue
  houses.append((xx+rng.uniform(-.5,.5),yy, rng.uniform(3.5,4.7),rng.uniform(3.2,4.1),rng.uniform(4,5.5),rng.uniform(-.15,.15),'Chalet'))
# Infill creates actual street walls and clusters, with alternate roof axes.
for xx,yy in [(-27,-6),(-13,-1),(-9,7),(-23,28),(-18,34),(-10,34),(4,34),(15,30),(23,28),(30,34),(1,18),(-2,40),(14,40),(25,41),(-6,-25),(2,-28),(21,-24),(26,-14),(-28,38),(31,5)]:
 if min(((xx-a[0])**2+(yy-a[1])**2 for a in houses))<22:continue
 if min(((xx-p[0])**2+(yy-p[1])**2 for p in route))<23:continue
 houses.append((xx,yy,rng.uniform(3.2,4.4),rng.uniform(3,4.2),rng.uniform(3.5,5.8),math.pi/2 if rng.random()<.45 else -.16,'Infill cottage'))
for i,(x,y,w,d,h,rot,name) in enumerate(houses):
 ho=house('%02d %s'%(i,name),x,y,w,d,h,rot,i)
 if name in ['Bakery','Clockmaker','Golden Pine Inn','Grocer']:
  m=Mesh();m.box((0,-d/2-.19,1.95),(w*.7,.12,.5),DK);m.obj('Carved shop sign',ho,.025)
  text({'Bakery':'BOULANGERIE','Clockmaker':'HORLOGER','Golden Pine Inn':'AUBERGE DU PIN','Grocer':'EPICERIE'}[name],(0,-d/2-.27,1.82),.22,EM,ho)

# Small alpine church and clock: enamel, patinated roofs, bell, real hinge bird.
church=house('Chapel nave',-5,10,4,6,5.8,0,7)
tz=ground(-2,6);tower=empty('Clock tower',(-2,6,tz));m=Mesh()
m.box((0,0,6),(3.3,3.1,12),ST)
for z,w in [(1,3.7),(7.9,3.55),(10.7,3.7),(12,3.85)]:m.box((0,0,z),(w,w,.2),PL)
for sx in [-1.5,1.5]:m.box((sx,-1.58,6),(.22,.16,12),PL)
for sg in [-1,1]:
 for xx in [-1.35,1.35]:m.rod((xx,sg*1.35,12),(xx,sg*1.35,14.1),.13,DK)
m.rod((0,0,14),(0,0,17),2.4,CU,4,r2=.05);m.rod((0,0,17),(0,0,18),.07,BR);m.ball((0,0,17.9),(.16,.16,.16),BR)
m.torus((0,-1.65,9.5),1.14,.09,BR,rot=(math.pi/2,0,0));m.rod((0,-1.66,9.5),(0,-1.72,9.5),1.08,EM,64)
for i in range(60):
 a=i*math.tau/60;r=.96;m.rod((math.sin(a)*r,-1.76,9.5+math.cos(a)*r),(math.sin(a)*(r-(.11 if i%5==0 else .045)),-1.76,9.5+math.cos(a)*(r-(.11 if i%5==0 else .045))),.014,IR,6)
m.rod((0,-1.82,9.5),(0,-1.82,10.26),.035,IR);m.rod((0,-1.82,9.5),(-.47,-1.82,9.23),.045,IR);m.ball((0,-1.84,9.5),(.075,.04,.075),BR)
m.box((0,-1.9,7.5),(1.9,.65,.16),BR);m.obj('Tower stonework, copper spire and clock dial',tower,.025)
for lab,x,z in [('XII',0,10.2),('III',.75,9.4),('VI',0,8.68),('IX',-.75,9.4)]:text(lab,(x,-1.79,z),.21,IR,tower)
bell=empty('Bronze bell',(0,0,12.8),tower);m=Mesh();m.rod((0,0,.4),(0,0,-.45),.32,BR,32,r2=.68);m.torus((0,0,-.45),.67,.06,BR);m.rod((0,0,.6),(0,0,1),.08,IR);m.obj('Cast bronze bell',bell)
hammer=empty('Bell hammer pivot',(.95,-.1,13.1),tower);m=Mesh();m.rod((0,0,0),(-.4,0,-.75),.045,IR);m.ball((-.4,0,-.75),(.16,.15,.16),IR);m.obj('Bell hammer arm and contact head',hammer)
bird=empty('Mechanical bird', (0,-2.06,7.8),tower);m=Mesh();m.ball((0,0,.16),(.24,.17,.27),BR);m.ball((0,-.08,.42),(.17,.15,.15),BR);m.rod((0,-.16,.42),(0,-.43,.40),.08,BR,8,r2=0);m.ball((-.08,-.18,.46),(.025,.025,.025),IR);m.ball((.08,-.18,.46),(.025,.025,.025),IR);m.rod((0,0,-.1),(0,0,-.32),.07,BR);m.obj('Bird body with pivot axle',bird)
for sg in [-1,1]:
 wing=empty('Bird wing '+str(sg),(sg*.18,0,.23),bird);m=Mesh()
 for j in range(6):m.rod((0,j*.035,0),(sg*(.55-j*.045),j*.065,-.28-j*.025),.045,BR,8,r2=.012)
 m.torus((0,0,0),.075,.018,IR,rot=(math.pi/2,0,0),n=16);m.obj('Articulated feather plates',wing)
 # short visible crank linkage behind wing.
 m=Mesh();m.rod((sg*.1,.13,.1),(sg*.28,.13,.24),.025,IR);m.obj('Bird hinge crank '+str(sg),bird)

# Transport stations and supported sagging cable.
A=Vector((-13,21,ground(-13,21)+4.8));B=Vector((8,1,ground(8,1)+4.8))
def cable(u,offset=0):
 p=A.lerp(B,u);p.z-=.85*4*u*(1-u);p.y+=offset;return tuple(p)
m=Mesh();m.path([cable(i/120) for i in range(121)],.045,IR);m.path([cable(i/120,.22) for i in range(121)],.022,IR);m.obj('Continuous load cable and haulage line')
for nm,P in [('Upper',A),('Square',B)]:
 z=P.z-4.8;root=empty(nm+' station',(P.x,P.y,z));m=Mesh()
 deck_w=7 if nm=='Square' else 5;deck_d=5.6 if nm=='Square' else 4.2;deck_y=.2 if nm=='Square' else -.5
 m.box((0,deck_y,.58),(deck_w,deck_d,.35),DK)
 for i in range(int(deck_w/.26)):m.box((-deck_w/2+.13+i*.26,deck_y,.79),(.245,deck_d-.1,.10),WO)
 for x in [-1.7,1.7]:
  for y in [.65,-1.2]:
   m.box((x,y,2.6),(.22,.22,4.2),DK);m.rod((x,y,3.5),(x*.55,y,4.6),.08,WO)
 m.box((0,.65,4.6),(3.65,.24,.27),DK);m.box((0,-1.2,4.6),(3.65,.24,.27),DK)
 # Platform below carrier; no roof hiding the mechanism or worker hands.
 for i in range(4):m.box((-2,-2.6-i*.25,.62-i*.15),(1.1,.4,.25),ST)
 m.rod((-.6,0,4.8),(.6,0,4.8),.08,IR);m.obj(nm+' station frame, deck, braces and axle',root,.025)
 pulley=empty(nm+' drive wheel',(0,0,5.28),root);m=Mesh();m.torus((0,0,0),.48,.055,BR,rot=(math.pi/2,0,0))
 for i in range(8):a=i*math.tau/8;m.rod((0,0,0),(.44*math.cos(a),0,.44*math.sin(a)),.025,BR)
 m.rod((0,-.2,0),(0,.2,0),.09,IR);m.obj('Pulley spokes and rim',pulley)
 m=Mesh();m.box((1.9,0,1.15),(.5,.7,.55),DK);m.rod((1.9,-.4,1.3),(1.9,.4,1.3),.13,IR);m.obj(nm+' traction capstan pedestal',root,.02)
for u in [.37,.7]:
 p=Vector(cable(u));m=Mesh()
 for sg in [-1,1]:
  base=(p.x+sg*1.4,p.y+.7,ground(p.x+sg*1.4,p.y+.7));m.rod(base,(p.x+sg*.75,p.y+.7,p.z+.2),.12,DK)
 m.rod((p.x-1,p.y+.7,p.z+.2),(p.x+1,p.y+.7,p.z+.2),.13,DK);m.rod((p.x,p.y+.7,p.z+.2),(p.x,p.y,p.z+.2),.06,IR);m.torus((p.x,p.y,p.z+.16),.16,.035,BR,rot=(math.pi/2,0,0));m.obj('Cable trestle '+str(u))
carrier=empty('Red carrier')
m=Mesh();m.box((0,0,.09),(2.05,1.45,.18),DK)
for side in [-1,1]:
 for j in range(5):m.box((side*1,0,.25+j*.17),(.08,1.45,.14),RD)
 for j in range(5):m.box((0,side*.7,.25+j*.17),(2,.08,.14),RD)
 for x in [-.87,.87]:m.box((x,side*.75,.6),(.065,.065,1.1),BR)
for sg in [-1,1]:
 m.rod((sg*.9,0,1.1),(sg*.9,0,2.9),.055,IR);m.rod((sg*.9,0,2.9),(0,0,3.8),.055,IR)
m.rod((-.2,0,3.96),(.2,0,3.96),.09,IR);m.torus((0,0,3.96),.16,.04,BR,rot=(math.pi/2,0,0),n=20);m.obj('Cargo basket slats and upright suspension',carrier,.018)
lid=empty('Basket lid hinge',(-1.06,0,1.13),carrier);m=Mesh();m.box((1.06,0,0),(2.12,1.5,.12),RD)
for x in [.20,1.92]:m.box((x,0,.075),(.07,1.5,.045),BR)
m.torus((.35,.50,.1),.10,.023,BR,rot=(math.pi/2,0,0),n=16)
m.obj('Basket hinged lid',lid,.02)
crate=empty('Persistent bread crate');m=Mesh();m.box((0,0,.05),(1.25,.8,.1),WO)
for sg in [-1,1]:
 for j in range(3):m.box((0,sg*.4,.16+j*.13),(1.25,.055,.11),WO);m.box((sg*.625,0,.16+j*.13),(.055,.8,.11),WO)
 m.box((sg*.63,0,.34),(.04,.28,.1),DK)
for i in range(3):
 for j in range(2):
  x=(i-1)*.35;y=(j-.5)*.33;m.ball((x,y,.43),(.16,.145,.16),BD,16,10)
  for off in [-.05,.03]:m.rod((x-.09,y+off,.565),(x+.09,y+off+.025,.56),.012,WH,6)
m.obj('Bread crate and six scored loaves',crate,.012)
cl=empty('Bread crate lid',(0,.42,.65),crate);m=Mesh();m.box((0,-.42,0),(1.32,.86,.065),WO);m.obj('Crate hinged cover',cl,.01)
table=empty('Bakery arrival table',(10.5,3.0,ground(8,1)+.8));m=Mesh();m.box((0,0,.9),(2.1,1.35,.14),WO)
for x in [-.85,.85]:
 for y in [-.5,.5]:m.box((x,y,.45),(.12,.12,.9),DK)
m.obj('Market workbench',table,.035)
for side in [-1,1]:
 clamp=empty('Dock locking jaw '+str(side),(8+side*1.22,1, B.z-3.8+.32));m=Mesh();m.box((0,0,0),(.25,.32,.2),BR);m.box((0,0,-.25),(.1,.1,.5),IR);m.obj('Sliding restraint',clamp,.02)

# Tailored eighteenth-century figures, articulated limbs, coat tails and hats.
def person(name,color=BL,apron=False):
 root=empty(name);m=Mesh();m.rod((0,0,.69),(0,0,1.28),.24,color,12,r2=.19);m.box((0,-.075,.63),(.51,.32,.33),color)
 m.ball((0,0,1.51),(.145,.135,.19),SK);m.ball((0,-.13,1.49),(.04,.05,.05),SK);m.rod((0,0,1.65),(0,0,1.76),.17,WH if apron else DK,16,r2=.12)
 if not apron:m.rod((0,0,1.66),(0,0,1.69),.27,DK,3)
 if apron:m.box((0,-.205,1.02),(.35,.035,.55),WH)
 for zz in [.92,1.06,1.2]:m.ball((0,-.23,zz),(.024,.018,.024),BR)
 m.obj(name+' coat, head and cap',root)
 for sg in [-1,1]:
  leg=empty(name+' leg '+str(sg),(sg*.12,0,.75),root);m=Mesh();m.rod((0,0,0),(0,0,-.57),.075,WH);m.box((0,-.075,-.66),(.17,.30,.18),BK);m.obj(name+' stocking and shoe '+str(sg),leg,.018)
  for part in ['upper','fore']:
   limb=empty(name+' '+part+' arm '+str(sg),parent=root);m=Mesh();m.rod((0,0,0),(0,0,1),.07,color if part=='upper' else WH);m.obj('Sleeve '+part,limb)
  hand=empty(name+' hand '+str(sg),parent=root);m=Mesh();m.ball((0,0,0),(.075,.06,.07),SK);m.obj('Hand',hand)
 root['person']=True;root['apron']=apron;return root
loader=person('Baker',WH,True);worker=person('Station porter',BL,True)
residents=[]
for i in range(42):
 o=person('Resident %02d'%i,[BL,RD,GR,WO][i%4]);o['phase']=rng.random()*math.tau
 if i<24:
  j=int(i/24*(len(route)-20))+8;p=route[j];o['base']=[p[0]+(-1 if i%2 else 1)*1.2,p[1],p[2]];o['axis']=[.7,.4];o['span']=1.2
 else:
  x,y=[(-8,18),(-13,19),(0,-1),(4,3),(3,7),(-18,0),(12,-9),(-7,-12),(3,25)][(i-24)%9];o['base']=[x+rng.uniform(-.6,.6),y+rng.uniform(-.6,.6),ground(x,y)+.16];o['axis']=[.6,.2];o['span']=.5
 residents.append(o.name)
# A wood carrier's bundle stays attached to his torso.
m=Mesh()
for j in range(5):m.rod((-.28+j*.12,.26,.78),(-.28+j*.12,.26,1.55),.055,WO)
m.path([(-.33,.24,1.1),(0,.33,1.1),(.33,.24,1.1)],.025,IR);m.obj('Bundled firewood',bpy.data.objects['Resident 30'])

# Horse-drawn wheeled carriage; shafts, leather harness and reins share parent.
cart=empty('Green carriage');m=Mesh();m.box((0,.8,1.05),(1.65,2.4,.35),GR);m.box((0,1.2,1.58),(1.7,1.7,.75),GR)
for sg in [-1,1]:
 m.box((sg*.81,1.2,2.3),(.09,1.8,1),DK);m.box((sg*.84,1.2,2.3),(.03,1.35,.65),GL)
 m.rod((sg*.73,-.3,1),(sg*.73,-3.3,1.12),.055,WO)
m.box((0,1.2,2.86),(1.95,2.1,.18),DK);m.box((0,1.2,2.98),(1.94,2.08,.08),SN)
m.box((0,-.25,1.6),(1.5,.5,.18),WO);m.obj('Carriage body, shafts and lantern windows',cart,.05)
for yy in [-.1,1.85]:
 for sg in [-1,1]:
  wh=empty('Carriage wheel %.2f %d'%(yy,sg),(sg*.99,yy,.62),cart);m=Mesh();m.torus((0,0,0),.59,.055,IR,rot=(0,math.pi/2,0));m.torus((0,0,0),.52,.055,WO,rot=(0,math.pi/2,0))
  for j in range(12):a=j*math.tau/12;m.rod((0,0,0),(0,.52*math.cos(a),.52*math.sin(a)),.027,WO)
  m.rod((-.13,0,0),(.13,0,0),.11,BR);m.obj('Twelve spoke wooden wheel',wh)
horse=empty('Horse',(0,-3,0),cart);m=Mesh();m.ball((0,0,1.25),(.39,.9,.52),BN,18,12);m.rod((0,-.56,1.35),(0,-1.0,2.08),.31,BN,16,r2=.22);m.ball((0,-1.14,2.04),(.22,.40,.23),BN,16,10);m.ball((0,-1.43,1.96),(.22,.18,.18),BN)
for sg in [-1,1]:m.rod((sg*.12,-1.04,2.19),(sg*.15,-1.1,2.52),.07,BN,10,r2=.022);m.ball((sg*.21,-1.24,2.12),(.027,.03,.03),BK)
m.path([(0,-.65,1.6),(0,-.78,1.95),(0,-.99,2.26)],.09,BK);m.path([(0,.8,1.46),(.08,1.1,1.1),(.1,1.18,.5)],.07,BK)
m.torus((0,-.42,1.3),.4,.045,BK,rot=(math.pi/2,0,0));m.path([(-.24,-1.35,2),(-.24,-1,2.2),(.24,-1,2.2),(.24,-1.35,2)],.025,BK);m.obj('Chestnut horse body, head, mane and harness',horse)
for sg in [-1,1]:
 for yy in [-.55,.55]:
  leg=empty('Horse leg %d %.2f'%(sg,yy),(sg*.25,yy,1.2),horse);m=Mesh();m.rod((0,0,0),(0,.04,-.48),.09,BN);m.rod((0,.04,-.48),(0,-.03,-1.02),.065,BN);m.box((0,-.055,-1.1),(.16,.23,.2),BK);m.obj('Horse articulated leg and hoof',leg,.02)
driver=person('Coachman',GR);driver.parent=cart;driver.location=(0,-.2,1.25)
m=Mesh()
for sg in [-1,1]:m.path([(sg*.19,-.52,2.45),(sg*.34,-1.8,2.13),(sg*.24,-4.35,2)],.018,BK)
m.obj('Continuous leather reins to bridle',cart)

# Market awning is furled until the delivery. Small warm props.
stall=empty('Breakfast stall',(4,-.1,ground(4,-.1)));m=Mesh();m.box((0,0,1),(2.6,1.1,.16),WO)
for x in [-1.25,1.25]:
 for y in [-.5,.5]:m.rod((x,y,0),(x,y,2.6),.07,DK)
for i in range(7):m.box((-1.4+i*.46,0,2.65),(.46,1.7,.06),RD if i%2 else WH,rx=.08)
m.obj('Striped linen breakfast awning and counter',stall)
for x in [-.8,0,.7]:
 m=Mesh();m.rod((x,0,1.09),(x,0,1.32),.13,EM,12);m.obj('Breakfast cups',stall)
# Waterwheel with visible vanes, axle, driven water channel.
wheel=empty('Working water wheel',(-20,15,ground(-20,15)+1));m=Mesh()
for y in [-.4,.4]:
 m.torus((0,y,0),1.4,.09,DK,rot=(math.pi/2,0,0))
 for j in range(12):a=j*math.tau/12;m.rod((0,y,0),(1.32*math.cos(a),y,1.32*math.sin(a)),.055,WO)
for j in range(18):a=j*math.tau/18;m.box((1.34*math.cos(a),0,1.34*math.sin(a)),(.35,.95,.12),WO,rx=0)
m.rod((0,-.8,0),(0,.8,0),.15,IR);m.obj('Waterwheel spokes, buckets and axle',wheel)
# Evergreens, logs, fences; geometry survives parallax.
for i in range(150):
 x=rng.uniform(-65,65);y=rng.uniform(-48,75)
 if -32<x<33 and -30<y<45:continue
 z=ground(x,y);h=rng.uniform(3,7);m=Mesh();m.rod((x,y,z),(x,y,z+h),.14,DK,8,r2=.04)
 for j in range(6):
  zz=z+h*(.2+j*.12);rad=h*(.22-j*.027)
  m.rod((x,y,zz),(x,y,zz+h*.34),rad,PN,11,r2=0);m.rod((x+.04,y,zz+.17),(x,y,zz+h*.35+.1),rad*.85,SN,11,r2=0)
 m.obj('Snow pine %03d'%i)
# Road pavers, irregular snow tracks, terraces and inhabited street furniture.
m=Mesh()
for j in range(0,len(route)-1):
 p=Vector(route[j]);d=Vector(route[j+1])-p;theta=math.atan2(d.y,d.x);normal=Vector((-math.sin(theta),math.cos(theta),0))
 for k in range(-3,4):
  q=p+normal*k*.43;m.box((q.x,q.y,ground(q.x,q.y)+.16),(.40,.38,.045),RO,rz=theta)
 if j%2==0:
  for sg in [-1,1]:
   q=p+normal*(1.85+sg*.09);m.ball((q.x,q.y,ground(q.x,q.y)+.035),(.09,.17,.012),ST,8,4)
m.obj('Wet road cobbles and footprints')
for xa,xb,yy in [(-30,-21,12),(-18,-10,12),(1,10,15),(24,32,12),(-31,-19,28),(0,12,30)]:
 m=Mesh()
 for j in range(4):
  for i in range(int((xb-xa)/.6)):
   x=xa+(i+.5+(j%2)*.15)*.6;z=ground(x,yy)-.6+j*.23;m.box((x,yy,z),(.55,.40,.21),ST)
 m.box(((xa+xb)/2,yy,ground((xa+xb)/2,yy)+.3),(xb-xa,.5,.14),SN);m.obj('Stone retaining terrace '+str(xa)+str(yy))
for i,(x,y) in enumerate([(-14,20),(-10,21),(6,-1),(11,2),(-14,10),(16,-16),(23,-5),(-9,1)]):
 z=ground(x,y);m=Mesh()
 for j in range(3):
  px=x+(j-1)*.58;m.rod((px,y,z),(px,y,z+.7),.26,WO,16,r2=.23)
  for zz in [.12,.55]:m.torus((px,y,z+zz),.26,.022,IR,n=20)
 m.obj('Coopered barrels '+str(i))
for x,y in [(-6,-4),(5,5),(10,-5),(-12,18),(12,-18),(-16,1)]:
 z=ground(x,y);m=Mesh();m.rod((x,y,z),(x,y,z+2.9),.045,IR);m.box((x,y,z+2.85),(.34,.34,.48),GL)
 for sg in [-1,1]:
  for ss in [-1,1]:m.rod((x+sg*.18,y+ss*.18,z+2.55),(x+sg*.18,y+ss*.18,z+3.13),.025,IR)
 m.rod((x,y,z+3.1),(x,y,z+3.4),.32,IR,4,r2=0);m.obj('Oil street lantern')
# Foreground snow ridge provides real occlusion during the opening rise.
m=Mesh();v=[]
for j in range(28):
 y=-63+j*1.2
 for i in range(30):
  x=20+i*1.2;z=ground(x,y)+20*math.exp(-((x-35)/12)**2-((y+43)/10)**2);v.append((x,y,z))
m.poly(v,[(j*30+i,j*30+i+1,(j+1)*30+i+1,(j+1)*30+i) for j in range(27) for i in range(29)],SN);m.obj('Foreground snow ridge | opening occluder')
# Soft smoke puffs use sparse transparent volume, fixed topology and wind.
sm=bpy.data.materials.new('Thin chimney smoke');sm.use_nodes=True;nodes=sm.node_tree.nodes;nodes.clear();vo=nodes.new('ShaderNodeVolumePrincipled');vo.inputs['Density'].default_value=.035;vo.inputs['Color'].default_value=(.67,.71,.73,1);out=nodes.new('ShaderNodeOutputMaterial');sm.node_tree.links.new(vo.outputs['Volume'],out.inputs['Volume'])
smokes=[]
for em in [o for o in bpy.data.objects if o.get('smoke')][:18]:
 for j in range(5):
  m=Mesh();m.ball((0,0,0),(1,1,1),0,10,6);o=m.obj('Smoke '+em.name+' '+str(j),em);o.data.materials.clear();o.data.materials.append(sm);o['puff']=j;smokes.append(o.name)
steam=[]
for j in range(5):
 m=Mesh();m.ball((0,0,0),(1,1,1),0,10,6);o=m.obj('Bread steam '+str(j));o.data.materials.clear();o.data.materials.append(sm);steam.append(o.name)

scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
world=bpy.data.worlds.new('Cold clear dawn');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.32,.43,.57,1);world.node_tree.nodes['Background'].inputs[1].default_value=.55;scene.world=world
sun_data=bpy.data.lights.new('Winter morning sun','SUN');sun=bpy.data.objects.new('Winter morning sun',sun_data);bpy.context.collection.objects.link(sun);sun.rotation_euler=(math.radians(66),math.radians(-25),math.radians(-38));sun_data.energy=2.3;sun_data.color=(1,.78,.54);sun_data.angle=.10
area_data=bpy.data.lights.new('Sky bounce','AREA');o=bpy.data.objects.new('Sky bounce',area_data);bpy.context.collection.objects.link(o);o.location=(5,-10,55);area_data.energy=1800;area_data.size=65;area_data.color=(.63,.77,1)
cam_data=bpy.data.cameras.new('Cinematic camera');cam=bpy.data.objects.new('Cinematic camera',cam_data);bpy.context.collection.objects.link(cam);scene.camera=cam;cam.location=(75,-108,99);cam.rotation_euler=(Vector((0,13,10))-cam.location).to_track_quat('-Z','Y').to_euler();cam_data.lens=46;cam_data.clip_end=1000
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.25
scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.render.resolution_percentage=100;scene.render.fps=24;scene.frame_end=2160
scene['residents']=json.dumps(residents);scene['smokes']=json.dumps(smokes);scene['steam']=json.dumps(steam);scene['cable_A']=list(A);scene['cable_B']=list(B);scene['road']=json.dumps(route)
scene['project']='Snow Clock City | original Alpine fantasy 18th-century world';scene['world_seed']=221022
bpy.ops.wm.save_as_mainfile(filepath=str(R/'model/snow-clock-city.blend'))
(R/'model/world-index.json').write_text(json.dumps({'objects':len(scene.objects),'buildings':len(houses),'road':route,'cable_A':list(A),'cable_B':list(B),'source':'src/build_world.py'},indent=2),encoding='utf8')
print('WORLD_READY',len(scene.objects),len(houses),flush=True)
