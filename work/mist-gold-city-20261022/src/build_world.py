"""Fog and Gold: original shared three-dimensional 18th-century city.
Run with Blender 4.5 --background --python src/build_world.py.
All dimensions metres, all movable objects have stable names and parents.
"""
import bpy,math,random,sys,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from geometry import Mesh,empty,curve,material
R=random.Random(221018);bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene
M={}
for key,hex,rough,metal,texture in [('stone','cdbb96',.76,0,8),('trim','e4d7b7',.64,0,20),('brick','8f5844',.82,0,12),('roof','895044',.76,0,24),('slate','4e625d',.6,0,25),('copper','508e7e',.49,.55,18),('brass','b79a58',.32,.72,30),('wood','4e3627',.77,0,10),('oak','8e6d42',.7,0,18),('iron','333c3c',.52,.65,0),('glass','384f52',.24,.25,0),('dark','262b2a',.8,0,0),('cream','e7d7b1',.85,0,25),('navy','243b62',.7,0,18),('wine','742b39',.56,0,20),('skin','c39773',.78,0,0),('leather','4a2e23',.8,0,12),('road','787c71',.95,0,30),('pave','a39f8b',.91,0,25),('grass','63705b',.98,0,8),('leaf','526848',.95,0,8),('water','486f70',.18,.3,0)]:M[key]=material(key,hex,rough,metal,texture)
def stage(s):print('BUILD',s,flush=True)
def arch(m,x,y,z,w,h,mat):
 # Solid arched opening inset in a stone facade, in XZ plane.
 r=w/2;vs=[(x-r,y,z),(x+r,y,z)]+[(x+r*math.cos(i*math.pi/12),y,z+h-r+r*math.sin(i*math.pi/12)) for i in range(13)];m.add(vs,[tuple(range(len(vs)))],mat)
 for i in range(12):
  a=i*math.pi/12;b=(i+1)*math.pi/12;m.add([(x+rr*math.cos(t),y-.025,z+h-r+rr*math.sin(t)) for rr,t in [(r,a),(r,b),(r+.14,b),(r+.14,a)]],[(0,1,2,3)],M['trim'])
def window(m,x,y,z,w=1,h=1.65,arched=False):
 if arched:arch(m,x,y,z,w,h,M['glass'])
 else:m.box((x,y,z+h/2),(w,.06,h),M['glass'])
 for xx in [x-w/2-.08,x+w/2+.08]:m.box((xx,y-.06,z+h/2),(.14,.16,h+.16),M['trim'])
 for zz in [z-.08,z+h+.08]:m.box((x,y-.09,zz),(w+.34,.25,.15),M['trim'])
 m.box((x,y-.07,z+h/2),(.05,.08,h),M['oak']);m.box((x,y-.07,z+h*.52),(w,.08,.05),M['oak'])
def roof(m,w,d,z,h,mat):
 m.add([(-w/2,-d/2,z),(w/2,-d/2,z),(w/2,d/2,z),(-w/2,d/2,z),(0,-d/2,z+h),(0,d/2,z+h)],[(0,1,4),(3,5,2),(0,4,5,3),(1,2,5,4)],mat)
 m.rod((0,-d/2-.1,z+h),(0,d/2+.1,z+h),.12,M['trim'])
 # Actual seams on both roof slopes remain visible at medium distance.
 for u in [i/8 for i in range(1,8)]:
  for side in [-1,1]:m.rod((side*w/2*(1-u),-d/2,z+h*u+.025),(side*w/2*(1-u),d/2,z+h*u+.025),.026,M['brick'],n=4)
def house(w,d,h,variant=0,detail=1):
 m=Mesh();wall=M['brick'] if variant%5==0 else M['stone'];m.box((0,0,h/2),(w,d,h),wall)
 for z in [.3,h,h-.3]+([3.5,6.8] if h>8 else [3.5]):m.box((0,0,z),(w+.3,d+.28,.20),M['trim'])
 if not detail:
  for side in [-1,1]:
   for x in [-w*.28,0,w*.28]:
    for z in [1.8,4.9,8.0]:
     if z<h-1:m.box((x,side*(d/2+.03),z),(1.05,.05,1.6),M['glass']);m.box((x,side*(d/2+.05),z-.85),(1.3,.16,.12),M['trim'])
  roof(m,w+.4,d+.4,h,3,M['slate'] if variant%4==0 else M['roof']);m.box((w*.25,d*.22,h+2),(.7,.7,2.7),M['brick']);return m
 # Ashlar corners and plinths.
 if detail:
  for x in [-w/2,w/2]:
   for y in [-d/2,d/2]:
    for z in range(1,int(h),1):m.box((x,y,z),(.42,.42,.36),M['trim'])
 n=max(2,round(w/2.4));rows=max(2,round((h-1)/3.15))
 for face in [0,math.pi]:
  facade=Mesh()
  for row in range(rows):
   for k in range(n):
    if row==0 and k==n//2:continue
    window(facade,(k-(n-1)/2)*w/(n+.3),-d/2-.05,.95+row*3.05,.85 if w<9 else 1.12,1.55,variant%3==0)
  arch(facade,0,-d/2-.12,0,1.5,2.65,M['wood']);facade.box((0,-d/2-.65,.16),(2.1,1.2,.32),M['trim'])
  facade.rod((w/2-.25,-d/2-.28,.5),(w/2-.25,-d/2-.28,h),.065,M['copper'])
  m.append(facade,rot=face)
 # Side windows prevent empty gable walls.
 for side in [-1,1]:
  for yy in [-d*.26,d*.26]:
   for z in [1.7,4.8,7.9]:
    if z<h-1:m.box((side*(w/2+.02),yy,z),(.06,1,1.6),M['glass']);m.box((side*(w/2+.07),yy,z-.88),(.24,1.3,.14),M['trim'])
 roof(m,w+.55,d+.55,h,2.8 if w<10 else 3.6,M['slate'] if variant%4==0 else M['roof'])
 for x in [-w*.29,w*.28]:
  m.box((x,d*.26,h+2),(.7,.85,3),M['brick']);m.box((x,d*.26,h+3.5),(.93,1.05,.22),M['trim']);m.box((x,d*.26,h+3.63),(.47,.57,.10),M['dark'])
 if detail:
  for x in [-w*.23,w*.23]:
   m.box((x,-d*.19,h+1.25),(1.4,1.1,1.5),M['trim']);window(m,x,-d*.19-.56,h+.7,.8,1);m.append(gable_cap(1.7,1.4,.65), (x,-d*.19,h+2))
 return m
def gable_cap(w,d,h):
 m=Mesh();roof(m,w,d,0,h,M['slate']);return m
stage('materials')
exec(compile((ROOT/'src/mountain_city.py').read_text(encoding='utf8'),str(ROOT/'src/mountain_city.py'),'exec'))
# Cathedral with twin bell towers, drum, copper dome, apse, buttresses, steps.
m=Mesh();m.box((0,0,10),(19,31,20),M['stone']);m.box((0,0,.5),(23,36,1),M['trim'])
for x in [-10,10]:
 for y in [-11,-3,5,13]:m.box((x,y,5.5),(1.3,2,11),M['trim']);m.rod((x,y,10),(x*.84,y,16),.38,M['trim'])
for y in [-10,-2,6,13]:
 for side in [-1,1]:
  ww=Mesh();window(ww,0,0,5.5,2.4,7,True);m.append(ww,(side*9.58,y,0),-side*math.pi/2)
roof(m,20,32,20,7,M['copper'])
for j in range(7):m.box((0,-18-j*.55,.55-j*.07),(18+j*.65,1.2,.22),M['trim'])
fac=Mesh();arch(fac,0,-16.05,.8,4.2,8.8,M['wood']);arch(fac,0,-16.1,11,4.5,6.1,M['glass'])
for x in [-7,-4.6,4.6,7]:
 fac.rod((x,-16.8,1),(x,-16.8,16),.5,M['trim'],.42,20);fac.box((x,-16.8,16), (1.3,1.1,.6),M['trim'])
fac.box((0,-16.6,17),(18,1.6,.7),M['trim']);fac.add([(-9,-17,17),(9,-17,17),(0,-17,23)],[(0,1,2)],M['trim']);m.append(fac)
for x in [-11.2,11.2]:
 m.box((x,-10,15),(6.1,7,30),M['stone'])
 for z in [7,16,25,30]:m.box((x,-10,z),(6.6,7.5,.42),M['trim'])
 for xx in [x-2.9,x+2.9]:
  for yy in [-13.4,-6.6]:
   for z in range(2,29):m.box((xx,yy,z),(.48,.48,.44),M['trim'])
 for z in [4,11,19]:window(m,x,-13.55,z,1.5,3.4,True)
 for side in [-1,1]:
  ww=Mesh();window(ww,0,0,25.6,2.4,3.6,True);m.append(ww,(x+side*3.08,-10,0),-side*math.pi/2)
 for xx in [x-1.5,x+1.5]:arch(m,xx,-13.55,25.8,1.3,3.1,M['dark'])
 m.ring((x,-10,30),[(3.3,0),(2.8,1),(2.6,3.5),(1.3,5.3),(.7,5.8)],M['copper'],32)
 m.ring((x,-10,35.8),[(.65,0),(.65,2.5),(.05,7)],M['copper'],20)
 m.rod((x,-10,42),(x,-10,44),.09,M['brass']);m.rod((x-.55,-10,43.3),(x+.55,-10,43.3),.08,M['brass'])
m.ring((0,5,23),[(7,0),(7,6),(7.3,6.4)],M['stone'],48)
for i in range(16):
 a=i*math.tau/16;m.rod((6.9*math.cos(a),5+6.9*math.sin(a),23),(6.9*math.cos(a),5+6.9*math.sin(a),29.3),.20,M['trim'])
profile=[(7.4*math.cos(i*math.pi/24),8.7*math.sin(i*math.pi/24)) for i in range(13)];m.ring((0,5,29.4),profile,M['copper'],48)
for i in range(16):
 a=i*math.tau/16
 for j in range(12):
  r,z=profile[j];r2,z2=profile[j+1];m.rod((r*math.cos(a),5+r*math.sin(a),29.45+z),(r2*math.cos(a),5+r2*math.sin(a),29.45+z2),.055,M['brass'],n=6)
m.ring((0,5,38.1),[(.85,0),(.85,2.7),(1.1,2.9),(.0,4.5)],M['copper']);m.rod((0,5,42.6),(0,5,44.2),.09,M['brass'])
ob=m.bake('Cathedral of the Morning Bell');ob.location=(-42,73.3,32.1);ob.scale=(.86,.78,1.10)
plaza=Mesh();plaza.box((-42,43,2.3),(39,23,.16),M['pave'])
for side in [-1,1]:
 for j in range(8):plaza.box((-42+side*(4+j*1.8),40,2.4),(.2,17,.05),M['trim'])
plaza.ring((-42,40,2.4),[(3,0),(3,.5),(2.7,.6),(2.5,.3)],M['trim']);plaza.ring((-42,40,2.4),[(2.45,.25),(0,.25)],M['water']);plaza.ring((-42,40,2.7),[(.5,0),(.3,2.5),(1.3,2.8),(1.3,3.1),(.4,3.2),(.0,4.2)],M['stone']);plaza.bake('Cathedral plaza and fountain').location.z=14.75
# Civic clocktower, readable hands and roman-inspired hour marks.
m=Mesh();m.box((0,0,12),(7.2,7.2,24),M['stone'])
for z in [1,9,17,24]:m.box((0,0,z),(7.8,7.8,.4),M['trim'])
for face in range(4):
 f=Mesh();f.rod((0,-3.65,20),(0,-3.82,20),2.35,M['brass'],n=48);f.rod((0,-3.83,20),(0,-3.87,20),2.10,M['cream'],n=48)
 for i in range(12):
  a=i*math.tau/12;f.rod((1.78*math.sin(a),-3.94,20+1.78*math.cos(a)),(1.98*math.sin(a),-3.94,20+1.98*math.cos(a)),.055,M['dark'],n=4)
 f.rod((0,-3.96,20),(-.9,-3.96,20.6),.07,M['dark']);f.rod((0,-3.97,20),(.4,-3.97,21.65),.05,M['dark']);arch(f,0,-3.65,1,2.6,5,M['wood']);m.append(f,rot=face*math.pi/2)
m.ring((0,0,24),[(4.2,0),(3.1,2.3),(2.9,4.5),(1.1,7.4),(.1,9)],M['copper']);m.rod((0,0,33),(0,0,36),.12,M['brass']);ob=m.bake('Municipal astronomical clocktower');ob.location=(-20,105,2.2)
stage('landmarks')
exec(compile((ROOT/'src/ceremonial_terrace.py').read_text(encoding='utf8'),str(ROOT/'src/ceremonial_terrace.py'),'exec'))
# Industrial buildings retain pitched roofs, stone arches and low brick chimneys.
for x,y,w,d,h in [(39,-25,23,20,10),(39,9,23,20,11),(41,49,25,19,10),(74,-24,20,19,9)]:
 bz=plot_z(x,y,w,d);ob=house(w,d,h,0,True).bake('Workshop and warehouse');ob.location=(x,y,bz)
 m=Mesh();m.ring((x+5,y+4,bz),[(1.3,0),(1.0,18),(1.3,18.2),(1.25,19.2)],M['brick'],16);m.ring((x+5,y+4,bz+19.2),[(1,0),(.95,.2)],M['dark'],16);m.bake('Low brick workshop chimney')
# Water wheel X axis, rim and paddles parented to one hub.
hub=empty('Waterwheel hub',(11.5,-24,3.0));m=Mesh()
for x in [-.7,.7]:
 for i in range(32):
  a=i*math.tau/32;b=(i+1)*math.tau/32;m.rod((x,3.2*math.sin(a),3.2*math.cos(a)),(x,3.2*math.sin(b),3.2*math.cos(b)),.13,M['oak']);
 for i in range(10):a=i*math.tau/10;m.rod((x,0,0),(x,3.2*math.sin(a),3.2*math.cos(a)),.09,M['oak'])
for i in range(24):
 a=i*math.tau/24;m.add([(x,r*math.sin(a+da),r*math.cos(a+da)) for x,r,da in [(-.9,3.05,-.06),(.9,3.05,-.06),(.9,3.6,.06),(-.9,3.6,.06)]],[(0,1,2,3)],M['oak'])
ob=m.bake('Waterwheel paddles spokes and rim');ob.parent=hub
m=Mesh();m.rod((10.1,-24,3),(17,-24,3),.22,M['iron']);m.box((16,-24,2.8),(1.2,2,4.8),M['stone']);m.bake('Waterwheel axle and bearing')
m=Mesh();m.ring((19,-13,2.2),[(1.1,0),(1.15,.4),(1.15,3.6),(1,4),(.7,4.4)],M['brass']);m.rod((19,-13,6.6),(19,-13,8.5),.15,M['copper']);m.rod((19,-13,8.5),(17,-13,8.5),.15,M['copper']);m.box((19,-13,2.3),(3,3,.4),M['stone']);m.bake('Steam pump boiler with explicit exhaust')
# Arcaded masonry bridges, besides the low opening bridge.
for by in [-54,126,234,378]:
 m=Mesh()
 for side in [-1,1]:m.box((side*10.3,by,1.7),(2.6,6,3.4),M['stone'])
 for i in range(32):
  x=-9.1+i*18.2/32;z=2.5+4.5*math.sqrt(max(0,1-(x/9.2)**2));m.box((x,by,z),(.62,6,.7),M['stone'])
  for y in [by-3,by+3]:m.box((x,y,z+.6),(.64,.45,1.3),M['trim'])
 # Ramps reconnect to road surface.
 for side in [-1,1]:
  for i in range(10):x=side*(9+i*.8);z=2.2+.9*(1-i/10);m.box((x,by,z-.25),(.84,6,.5),M['stone'])
 m.bake('Stone arch bridge '+str(by))
# Bascule leaves and load-bearing portal pylons.
for side in [-1,1]:
 pivot=empty('Bridge pivot '+str(side),(side*9.25,18,3.1));m=Mesh();length=9.25
 for i in range(30):m.box((-side*(i+.5)*length/30,0,-.14),(length/30-.015,6.8,.28),M['oak'])
 for yy in [-3.18,3.18]:
  m.box((-side*length/2,yy,-.40),(length,.23,.48),M['iron'])
  for i in range(13):
   xx=-side*(i+.1)*length/13;m.rod((xx,yy,0),(xx,yy,1.05),.045,M['iron'])
  m.rod((0,yy,1.05),(-side*length,yy,1.05),.07,M['brass'])
 ob=m.bake('Moving bridge leaf '+str(side));ob.parent=pivot
 m=Mesh()
 for yy in [-3.7,3.7]:
  x=side*11.3;m.box((x,18+yy,6.8),(.8,.8,9.2),M['stone']);m.box((x,18+yy,11.55),(1.3,1.3,.3),M['trim']);m.rod((x,18+yy,11.8),(x,18+yy,13),.28,M['brass']);m.rod((x-.3,18+yy,12.6),(x+.3,18+yy,12.6),.4,M['iron'])
  curve('Lift chain %s %s'%(side,yy),[(side*1.2,18+yy*.8,3.4),(x,18+yy,9.6),(side*13,18+yy,5)],.055,M['iron'])
  weight=Mesh();weight.box((0,0,0),(1.05,1.05,1.8),M['iron']);ob=weight.bake('Counterweight %s %s'%(side,yy));ob.location=(side*13,18+yy,5)
 m.bake('Bridge stone support towers '+str(side))
 # Approach is a real wedge meeting raised deck, wheel and hoof ground uses same function.
 m=Mesh();x0=side*9.25;x1=side*19;m.add([(x0,14.6,2.15),(x1,14.6,2.15),(x1,21.4,2.15),(x0,21.4,2.15),(x0,14.6,3.1),(x1,14.6,2.25),(x1,21.4,2.25),(x0,21.4,3.1)],[(4,5,6,7),(0,1,5,4),(2,3,7,6)],M['pave']);m.bake('Bridge approach ramp '+str(side))
 gate=empty('Traffic gate '+str(side),(side*19,14.7,2.25));m=Mesh();m.rod((0,0,0),(0,0,1.4),.12,M['oak']);m.bake('Gate post '+str(side)).parent=gate
 m=Mesh();m.box((0,2.9,0),(.15,5.8,.15),M['cream']);m.box((0,2.9,.03),(.18,1.1,.18),M['wine']);ob=m.bake('Gate arm '+str(side));ob.parent=gate;ob.location.z=1.4
stage('bridges and industrial mechanics')
# Market: fabric supported by timber, produce, crates, barrels and lamps.
def barrel(m,p,s=1):m.ring(p,[(.34*s,0),(.42*s,.2*s),(.44*s,.65*s),(.34*s,.9*s),(.0,.9*s)],M['oak'],12);[m.ring((p[0],p[1],p[2]+z*s),[(r*s,0),(r*s,.06*s)],M['iron'],12) for z,r in [(.15,.4),(.72,.41)]]
props=Mesh()
# Quay ashlar joints and slab seams are geometry, with a deliberately small depth.
for side in [-1,1]:
 for y in range(-65,175,2):
  for z in [.45,1.1,1.75]:props.box((side*8.99,y+(0.6 if z==1.1 else 0),z),(.018,.024,.62),M['pave'])
  props.box((side*13.1,y,2.347),(6.1,.022,.009),M['pave'])
 for z in [.13,.78,1.43,2.08]:props.box((side*8.99,55,z),(.018,240,.025),M['pave'])
for side in [-1,1]:
 for i in range(36):
  y=-65+i*8;x=side*12
  if abs(y-18)<8 or any(abs(y-by)<5 for by in [-54,126,234]):continue
  props.rod((x,y,2.3),(x,y,4.8),.065,M['iron']);props.box((x,y,4.7),(.38,.38,.65),M['brass']);props.box((x,y,4.75),(.27,.27,.45),M['cream']);props.ring((x,y,5.08),[(.3,0),(.0,.3)],M['iron'],8)
for i in range(10):
 x=-28;y=-58+i*7.6
 if abs(y-18)<7:continue
 for dx in [-1.4,1.4]:
  for dy in [-1.15,1.15]:props.rod((x+dx,y+dy,2.25),(x+dx,y+dy,5.1),.07,M['wood'])
 props.box((x,y,3.1),(2.8,2.1,.25),M['oak'])
 for k in range(8):props.box((x-1.4+(k+.5)*.35,y,5.12),(.35,2.8,.07),M['cream'] if k%2 else M['wine'] if i%2 else M['navy'])
 for k in range(20):props.ball((x+R.uniform(-1.2,1.2),y+R.uniform(-.8,.8),3.3),(.12,.12,.12),M['brick'] if k%3 else M['leaf'],6,4)
for i in range(85):
 x=R.choice([14,17,18.5])+R.uniform(-.5,.5);y=R.choice([-39,-8,40,58])+R.uniform(-3,3)
 if i%3:props.box((x,y,2.7),(.7,.8,.9),M['oak']);props.box((x,y,3.17),(.75,.85,.06),M['wood'])
 else:barrel(props,(x,y,2.25))
props.bake('Market awnings cargo barrels and quay lamps')
# Gardens, trees, railings and distant silhouette. Grounded trunks, clustered foliage.
green=Mesh()
for i in range(65):
 side=R.choice([-1,1]);x=-15.6 if side<0 else 18.8;y=-70+i*9.1
 if abs(y-18)<7 or (side==-1 and -62<x<-20 and 25<y<105):continue
 z=ground_z(x,y);h=R.uniform(3.2,5.5);green.rod((x,y,z),(x,y,z+h),.16,M['wood'],.08)
 for j in range(4):green.ball((x+R.uniform(-.6,.6),y+R.uniform(-.6,.6),z+h+j*.5),(1.2,1.1,1.55),M['leaf'],8,5)
green.bake('Courtyard gardens and street trees')
# Fixed outer hill for camera reveal.
hill=Mesh()
for x in range(-180,181,12):
 for y in range(-150,-87,8):
  def hz(xx,yy):return 2+16*math.exp(-((yy+108)/17)**2)+2.6*math.sin(xx*.022)
  hill.add([(xx,yy,hz(xx,yy)) for xx,yy in [(x,y),(x+12,y),(x+12,y+8),(x,y+8)]],[(0,1,2,3)],M['grass'],True)
hill.bake('Fixed foreground hillside')
scrub=Mesh()
for i in range(600):
 x=R.uniform(-160,160);y=R.uniform(-137,-94);z=hz(x,y)
 if i%5==0:
  h=R.uniform(.25,.8);scrub.ball((x,y,z+h*.35),(h*1.5,h,h*.65),M['rock'],7,4)
 else:
  h=R.uniform(.18,.6)
  for j in range(3):scrub.rod((x+R.uniform(-.3,.3),y,z),(x+R.uniform(-.4,.4),y+.08,z+h),.015,M['leaf'],.003,3)
for i in range(42):
 x=R.uniform(-130,130);y=R.uniform(-127,-98);h=R.uniform(.4,1.3);scrub.ball((x,y,hz(x,y)+h*.45),(h,h*.8,h*.6),M['leaf'],9,5)
scrub.bake('Meadow grasses and limestone outcrops on reveal hill')
stage('world complete')
# Lighting and camera; no background image is used.
world=bpy.data.worlds.new('Cool dawn atmosphere');sc.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.36,.48,.60,1);world.node_tree.nodes['Background'].inputs[1].default_value=.35
ld=bpy.data.lights.new('Low morning golden sun','SUN');ld.energy=3.4;ld.angle=.10;ld.color=(1,.80,.57);ob=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(ob);ob.rotation_euler=(1.08,-.28,-.68)
ca=bpy.data.cameras.new('Cinema camera');cam=bpy.data.objects.new('Cinema camera',ca);sc.collection.objects.link(cam);sc.camera=cam;ca.clip_end=2500;ca.lens=46
sc.render.resolution_x=1080;sc.render.resolution_y=1920;sc.render.resolution_percentage=100;sc.render.fps=24;sc.frame_start=1;sc.frame_end=2160
sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=.15
sc['world_units']='metres';sc['title']='Fog and Gold / 雾金之城';sc['building_count']=blocks;sc['road_network']='Irregular perimeter blocks, winding ridge arteries and valley quays, original urban-layout.json'
exec(compile((ROOT/'src/build_actors.py').read_text(encoding='utf8'),str(ROOT/'src/build_actors.py'),'exec'))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'model/fog-gold-city.blend'));stage('saved')
