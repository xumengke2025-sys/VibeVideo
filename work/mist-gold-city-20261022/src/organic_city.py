"""Build the city from irregular urban-layout.json. No rectangular housing grid."""
layout=json.loads((ROOT/'model/urban-layout.json').read_text(encoding='utf8'));sc['urban_roads']=json.dumps(layout['roads'])
base=Mesh();base.box((0,800,-7),(2500,2800,10),M['rock'])
for side in [-1,1]:
 for xx in range(10,657,6):
  for yy in range(-180,1731,9):
   base.add([(side*x,y,ground_z(side*x,y)-.12) for x,y in [(xx,yy),(xx+6,yy),(xx+6,yy+9),(xx,yy+9)]],[(0,1,2,3)],M['grass'] if xx>120 else M['pave'],True)
 base.box((side*10,750,1.2),(2,1900,2.4),M['stone']);base.box((side*13.1,750,2.25),(6.2,1900,.18),M['trim'])
base.bake('01 Sculpted mountain terrain and valley quays')
water=Mesh();water.box((0,750,.02),(18,2100,.10),M['water']);water.bake('Canal water')
nt=M['water'].node_tree;p=nt.nodes.get('Principled BSDF');no=nt.nodes.new('ShaderNodeTexNoise');no.inputs['Scale'].default_value=3.4;bu=nt.nodes.new('ShaderNodeBump');bu.inputs['Strength'].default_value=.18;bu.inputs['Distance'].default_value=.10;nt.links.new(no.outputs['Fac'],bu.inputs['Height']);nt.links.new(bu.outputs[0],p.inputs['Normal'])
roads=Mesh()
for road in layout['roads']:
 pts=road['points'];half=road['width']/2
 for a,b in zip(pts,pts[1:]):
  dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
  if length<.01:continue
  nx,ny=-dy/length*half,dx/length*half;n=max(1,int(length/3))
  for k in range(n):
   x0,y0=a[0]+dx*k/n,a[1]+dy*k/n;x1,y1=a[0]+dx*(k+1)/n,a[1]+dy*(k+1)/n
   co=[(x0+nx,y0+ny),(x0-nx,y0-ny),(x1-nx,y1-ny),(x1+nx,y1+ny)];roads.add([(x,y,ground_z(x,y)+.045) for x,y in co],[(0,1,2,3)],M['road'] if road['width']>5.5 else M['pave'])
roads.bake('02 Winding arteries and unequal old town lanes')
def warped_house(q,h,v,detail):
 # Front edge q0-q1, rear edge q3-q2; one continuous perimeter parcel.
 a,b,c,d=q;w=math.dist(a,b);depth=(math.dist(a,d)+math.dist(b,c))/2;mid=((a[0]+b[0])/2,(a[1]+b[1])/2);z=ground_z(*mid)+.10
 m=elegant_house(w,depth,h,v,detail)
 def co(x,y,zz):
  u=x/w+.5;f=y/depth+.5;fx=a[0]+u*(b[0]-a[0]);fy=a[1]+u*(b[1]-a[1]);bx=d[0]+u*(c[0]-d[0]);by=d[1]+u*(c[1]-d[1]);return(fx+(bx-fx)*f,fy+(by-fy)*f,z+zz)
 m.v=[co(x,y,zz) for x,y,zz in m.v]
 low=min(ground_z(*p) for p in q)-.3
 m.add([(x,y,zz) for zz in [low,z] for x,y in q],[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],M['stone'])
 return m
blocks=0
garden=Mesh()
def tree(x,y,h):
 z=ground_z(x,y);garden.rod((x,y,z),(x,y,z+h*.7),.13,M['wood'],.06,6)
 for j in range(4):garden.ball((x+.16*math.sin(x+j),y+.16*math.cos(y-j),z+h*(.36+j*.15)),(.7,.72,h*.27),M['leaf'],8,5)
for block in layout['blocks']:
 co=block['polygon'];cx=sum(p[0] for p in co)/len(co);cy=sum(p[1] for p in co)/len(co)
 if block['garden']:
  # Planted courts are deliberate holes in the dense urban fabric.
  for j in range(8):
   p=co[j%len(co)];tree(cx*.55+p[0]*.45,cy*.55+p[1]*.45,R.uniform(4,8))
  continue
 batch=Mesh();detail=abs(cx)<220 and cy<320
 for parcel in block['parcels']:
  q=parcel['quad'];w=math.dist(q[0],q[1])
  if w<2.7:continue
  batch.append(warped_house(q,parcel['height'],parcel['variant'],detail));blocks+=1
 if batch.v:batch.bake('Old town perimeter block %04d'%block['id'])
 if block['area']>1200:
  for j in range(3):tree(cx+R.uniform(-3,3),cy+R.uniform(-3,3),R.uniform(3.5,6))
garden.bake('Enclosed court trees and hillside gardens')
stage('organic perimeter architecture '+str(blocks));sc['building_count']=blocks;sc['distant_building_count']=sum(len(b['parcels']) for b in layout['blocks'] if sum(p[1] for p in b['polygon'])/len(b['polygon'])>320)
# One hilltop palace, separate from the mixed merchants' and craftsmen's quarters.
m=Mesh();x,y=-160,162;z=plot_z(x,y,61,55);terrace_base(m,x,y,65,59,z)
m.append(elegant_house(56,15,19,0,True),(x,y+14,z))
for side in [-1,1]:
 m.append(elegant_house(15,43,17,4,True),(x+side*23,y-4,z));m.append(elegant_house(18,18,23,0,True),(x+side*23,y-21,z))
 for yy in range(-20,17,3):m.rod((x+side*14,y+yy,z+.2),(x+side*14,y+yy,z+7.4),.26,M['trim'],.21,12)
 m.box((x+side*14,y-2,z+7.7),(2.2,41,.45),M['trim'])
m.ring((x,y+14,z+19),[(5.5,0),(5.5,4),(5.9,4.4),(5.6,5),(4.8,8),(3,10.7),(.6,12),(.5,14),(0,15)],M['copper'],40);m.bake('Ducal ridge palace with inner court')
for i,(x,y) in enumerate([(-111,144),(143,183),(-179,267),(212,365),(-245,520),(314,695)]):
 m=Mesh();z=plot_z(x,y,22,24);terrace_base(m,x,y,24,27,z)
 if i%2==0:
  m.ring((x,y,z),[(8,0),(8,12),(8.6,12.3)],M['stone'],32)
  for k in range(16):
   a=k*math.tau/16;m.rod((x+8.1*math.cos(a),y+8.1*math.sin(a),z+.5),(x+8.1*math.cos(a),y+8.1*math.sin(a),z+11.8),.32,M['trim'],.26,10)
  m.ring((x,y,z+12.5),[(8.5,0),(7.9,1),(7.1,4),(5.4,7),(2.8,9),(.5,11),(0,13)],M['copper'],32)
 else:palace(m,x,y,26,26,17,i)
 m.bake('Neighbourhood rotunda or merchant guildhall '+str(i))
