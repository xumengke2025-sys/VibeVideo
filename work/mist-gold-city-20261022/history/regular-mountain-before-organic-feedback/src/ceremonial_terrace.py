"""Cathedral rock terrace, double staircase and arcaded civic retaining facade."""
m=Mesh();m.box((-42,77.5,22),(32,37,20),M['stone']);m.box((-42,77.5,32),(33,37,.3),M['trim'])
m.box((-42,41,9.5),(39,24,15),M['stone']);m.box((-42,41,17),(39.4,24.4,.35),M['trim'])
# Solid spandrels are built above the arches, leaving actual recesses.
for side in [-1,1]:
 x=-42+side*19.5
 for y in [32,38,44,50]:
  m.box((x,y,9.5),(1.3,1.2,15),M['trim'])
  for j in range(16):
   a=j*math.pi/16;b=(j+1)*math.pi/16
   m.add([(x+side*.18,y+3+rr*math.cos(t),11+rr*math.sin(t)) for rr,t in [(2.4,a),(2.4,b),(3,b),(3,a)]],[(0,1,2,3)],M['trim'])
  m.box((x,y+3,15.6),(1.6,6,2),M['stone'])
 # Balustrade around the forecourt; openings at stairs.
 for y in range(30,53):
  m.rod((x,y,17.2),(x,y,18.3),.10,M['trim'],.08,8)
 m.rod((x,29,18.4),(x,53,18.4),.14,M['trim'])
# Two flights ascending laterally from forecourt to upper platform, landing in centre.
for side in [-1,1]:
 for i in range(70):
  x=-42+side*(16-i*.215);z=17+i*(15/70)
  m.box((x,55.5,(17+z)/2),(.23,5,max(.3,z-17)),M['trim'])
  for yy in [53.1,57.9]:
   if i%4==0:m.rod((x,yy,z),(x,yy,z+1),.085,M['trim'])
   if i:m.rod((x,yy,z+1),(x+side*.215,yy,z+1-15/70),.09,M['trim'])
 m.box((-42,58,31.9),(4,4,.4),M['trim'])
# Quay-to-forecourt switchback stair, all treads tied to measured rise.
for j in range(2):
 for i in range(35):
  y=29+i*.31 if j==0 else 39.85-i*.31;x=-20.6-j*3.7;z=2.25+(j*35+i)*14.75/70
  m.box((x,y,z-.15),(3.5,.33,.3),M['trim'])
m.box((-22.45,40.4,9.5),(7.4,1.5,.35),M['trim']);m.box((-25,29.1,17),(4,2,.35),M['trim'])
# Stone voussoirs, plinth and pilasters on cathedral terrace.
for x in [-57,-51,-45,-39,-33,-27]:
 m.box((x,54,24),(1.1,1.3,15),M['trim'])
 for z in range(18,32):m.box((x,53.3,z),(1.3,.12,.12),M['stone'])
m.bake('Cathedral monumental terraced approach and stairs')
# Side promenade joins the west contour road to upper platform.
m=Mesh()
for y in range(59,99,2):
 z=32.12;m.box((-59.2,y,z-.15),(3.2,2.1,.3),M['pave'])
m.bake('Cathedral upper promenade')
# Deep vaulted storage rooms articulate the exposed load-bearing podium.
m=Mesh()
for x,z0,ystart,count in [(-25.96,13,62,5),(-22.46,3,32,4)]:
 for j in range(count):
  y=ystart+j*6;f=Mesh();arch(f,0,0,z0,4.5,9.2,M['dark']);m.append(f,(x,y,0),math.pi/2)
  for zz in [z0-.3,z0+10.1]:m.box((x+.06,y,zz),(.25,5.8,.25),M['trim'])
 for zz in range(int(z0),32 if x<-25 else 17):
  m.box((x+.015,ystart+(count-1)*3,zz),(.025,count*6,.045),M['rock'])
m.bake('Vaulted terrace facade ashlar joints and recesses')
