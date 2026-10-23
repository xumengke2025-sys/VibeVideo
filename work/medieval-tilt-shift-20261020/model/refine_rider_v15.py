"""Hero cyclist refinement. Work in metres; preserve the animation part contract."""
import bpy,math,json,ast,sys
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent;ROOT=P.parent
bpy.ops.wm.open_mainfile(filepath=str(P/'babylon-city-v15.blend'));scene=bpy.context.scene
for file,names in [('build_city.py',{'srgb','color','node','surface','textured'}),('revise_city_v12.py',{'Mesh'})]:
 tree=ast.parse((P/file).read_text(encoding='utf8'));exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in names],type_ignores=[]),file,'exec'))
data=json.loads(scene['v15_rider']);parts={k:bpy.data.objects[v] for k,v in data['parts'].items()};root=bpy.data.objects[data['root']];M=bpy.data.materials
if 'V15 coat seam' not in M:surface('V15 coat seam','7e6245',.9)
coat=M['V15 sand gabardine'];seam=M['V15 coat seam'];lining=M['V15 coat lining'];skin=M['V15 warm face'];hair=M['V15 dark chestnut hair'];felt=M['V15 felt brown hat'];leather=M['V15 oxblood leather'];navy=M['V15 indigo wool trousers'];scarf=M['V15 brilliant blue scarf'];steel=M['V15 brushed nickel'];brass=M['V15 polished bell brass'];black=M['V15 enamel frame'];rubber=M['V15 tyre rubber'];white=M['V15 shirt cream']
thread=surface('V15 linen topstitch','c2a47e',.88);nail=surface('V15 natural nails','c69c7e',.58)
skin.node_tree.nodes.get('Principled BSDF').inputs['Subsurface Weight'].default_value=.065
def replace(name,m):
 old=parts[name];temporary=m.bake('detail temporary');old.data=temporary.data;bpy.data.objects.remove(temporary,do_unlink=True);return old
def add(name,m):
 ob=m.bake('V15 '+name);ob.parent=root;parts[name]=ob;return ob
def strip(m,rows,mat):
 n=len(rows[0]);m.add([v for row in rows for v in row],[(j*n+i,j*n+i+1,(j+1)*n+i+1,(j+1)*n+i) for j in range(len(rows)-1) for i in range(n-1)],mat,True)
def line(m,points,r,mat):
 for a,b in zip(points,points[1:]):m.rod(a,b,r,mat,n=8)
def panel(m,vs,mat,thick=.005):
 n=len(vs);m.add(vs+[(x,y-thick,z) for x,y,z in vs],[tuple(range(n)),tuple(reversed(range(n,2*n)))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat)
def ellipse(m,c,rx,ry,rz,mat,n=48):
 # A closed horizontal decorative piping ellipse.
 pts=[(c[0]+rx*math.cos(i*math.tau/n),c[1]+ry*math.sin(i*math.tau/n),c[2]) for i in range(n+1)];line(m,pts,rz,mat)
def torus(m,center,r,thick,mat,n=80,k=8,start=0,end=math.tau):
 vs=[]
 for i in range(n+1):
  a=start+(end-start)*i/n
  for j in range(k):
   b=math.tau*j/k;rr=r+thick*math.cos(b);vs.append((center[0]+thick*math.sin(b),center[1]+rr*math.sin(a),center[2]+rr*math.cos(a)))
 m.add(vs,[(i*k+j,i*k+(j+1)%k,(i+1)*k+(j+1)%k,(i+1)*k+j) for i in range(n) for j in range(k)],mat,True)
# Face: intentionally featureless miniature head per explicit user direction.
m=Mesh();rows=[]
profile=[(1.731,.047,.047,.053),(1.751,.065,.060,.055),(1.785,.084,.077,.058),(1.823,.102,.090,.063),(1.858,.115,.099,.068),(1.900,.118,.099,.068),(1.943,.111,.094,.063),(1.979,.098,.084,.056),(2.010,.071,.066,.051),(2.024,.001,.001,.048)]
for z,rx,ry,cy in profile:
 rows.append([(rx*math.cos(a),cy+ry*math.sin(a),z) for a in [i*math.tau/48 for i in range(49)]])
strip(m,rows,skin)
# Hair is a quiet back-of-head silhouette below the hat, without facial features.
rows=[]
for z,r in [(1.954,.113),(1.976,.105),(2.008,.078)]:
 rows.append([(r*math.cos(a),.055+r*.86*math.sin(a),z) for a in [math.pi+math.pi*i/32 for i in range(33)]])
strip(m,rows,hair);replace('face and moustache',m)
# Felt fedora has a shaped brim, pinched crown, grosgrain and bound edge.
m=Mesh();rows=[]
for j in range(9):
 u=j/8;r=.124+.077*u;rows.append([(r*math.cos(a),.045+r*.82*math.sin(a),2.006+.020*u*u+.009*u*math.cos(2*a)) for a in [i*math.tau/96 for i in range(97)]])
strip(m,rows,felt)
for z,r in [(2.007,.126),(2.040,.128),(2.087,.123),(2.136,.112),(2.169,.098),(2.182,.067),(2.178,.012)]:
 pass
rows=[]
for z,r in [(2.007,.126),(2.040,.128),(2.087,.123),(2.136,.112),(2.169,.098),(2.182,.067),(2.178,.012)]:
 rows.append([(r*math.cos(a)*(1-.09*max(0,math.sin(a))*(z-2.04)/.14),.045+r*.82*math.sin(a),z-.012*max(0,math.sin(a))**4*(z>2.13)) for a in [i*math.tau/80 for i in range(81)]])
strip(m,rows,felt);m.ball((0,.045,2.176),(.015,.015,.004),felt,32,12);m.ring((0,.045,2.035),[(.129,0),(.128,.026)],leather,80,.82)
ellipse(m,(0,.045,2.043),.129,.106,.0017,seam);ellipse(m,(0,.045,2.058),.128,.105,.0015,seam)
edge=[(.201*math.cos(a),.045+.201*.82*math.sin(a),2.026+.009*math.cos(2*a)) for a in [i*math.tau/96 for i in range(97)]];line(m,edge,.0025,seam)
m.box((-.126,.028,2.050),(.009,.033,.025),leather);replace('felt hat',m)
# Tailored torso with curved seams, relief lapels and stitched pockets.
prof=[(1.025,.198,.130,-.30),(1.10,.199,.137,-.28),(1.20,.196,.141,-.24),(1.30,.215,.148,-.205),(1.40,.236,.152,-.15),(1.50,.249,.143,-.097),(1.59,.238,.126,-.054),(1.64,.180,.106,-.018),(1.67,.095,.080,.012)]
def front(x,z):
 for a,b in zip(prof,prof[1:]):
  if a[0]<=z<=b[0]:
   u=(z-a[0])/(b[0]-a[0]);rx=a[1]+(b[1]-a[1])*u;ry=a[2]+(b[2]-a[2])*u;cy=a[3]+(b[3]-a[3])*u;return cy+ry*math.sqrt(max(.02,1-(x/rx)**2))
 return .10
def fitted_panel(m,vs,mat,offset=.009):
 # Subdivide the polygon and project every vertex onto the tailored torso.
 for k in range(1,len(vs)-1):
  a,b,c=[Vector(v) for v in [vs[0],vs[k],vs[k+1]]];verts=[];faces=[];index={};n=12
  for i in range(n+1):
   for j in range(n+1-i):
    v=a+(b-a)*(i/n)+(c-a)*(j/n);v.y=front(v.x,v.z)+offset;index[i,j]=len(verts);verts.append(tuple(v))
  for i in range(n):
   for j in range(n-i):
    faces.append((index[i,j],index[i+1,j],index[i,j+1]))
    if j<n-i-1:faces.append((index[i+1,j],index[i+1,j+1],index[i,j+1]))
  m.add(verts,faces,mat,True)
def fitted_edge(m,vs):
 for a,b in zip(vs,vs[1:]+vs[:1]):
  pts=[]
  for i in range(13):
   v=Vector(a).lerp(Vector(b),i/12);v.y=front(v.x,v.z)+.014;pts.append(tuple(v))
  line(m,pts,.0014,thread)
m=Mesh();rows=[]
for z,rx,ry,cy in prof:
 rows.append([((rx+.0015*math.cos(a*8))*math.cos(a),cy+ry*math.sin(a),z) for a in [i*math.tau/64 for i in range(65)]])
strip(m,rows,coat);m.rod((0,.020,1.62),(0,.048,1.755),.057,skin,n=32)
fitted_panel(m,[(-.055,.108,1.665),(.055,.108,1.665),(.037,front(.037,1.49)+.003,1.49),(-.037,front(-.037,1.49)+.003,1.49)],white,.004)
for side in [-1,1]:
 vs=[(side*.029,front(side*.029,1.642)+.010,1.642),(side*.166,front(side*.166,1.593)+.015,1.593),(side*.128,front(side*.128,1.413)+.012,1.413),(side*.058,front(side*.058,1.521)+.014,1.521)]
 fitted_panel(m,vs,coat,.012);fitted_edge(m,vs)
 # Collar rolls around neck and folds back into each lapel.
 vs=[(side*.030,.111,1.666),(side*.112,.083,1.650),(side*.145,.070,1.613),(side*.074,.116,1.632)];fitted_panel(m,vs,coat,.021);fitted_edge(m,vs)
 for z in [1.28,1.391,1.50]:
  x=side*.073;y=front(x,z)+.008;m.ball((x,y,z),(.011,.006,.011),leather,20,10)
  for dx in [-.002,.002]:m.ball((x+dx,y+.005,z),(.0009,.0008,.001),thread,8,4)
 x=side*.148;z=1.315;y=front(x,z)+.010
 panel(m,[(x-.050,y,z+.016),(x+.050,y,z+.025),(x+.047,y+.002,z-.011),(x-.049,y+.002,z-.020)],coat)
 line(m,[(x-.046,y+.003,z-.014),(x+.044,y+.003,z-.006)],.0014,thread)
 # Side and shoulder seams contour the garment.
 line(m,[(side*rx*.94,cy-ry*.22,z) for z,rx,ry,cy in prof[:-1]],.0015,seam)
 vs=[(side*.105,-.028,1.635),(side*.23,-.035,1.606),(side*.23,-.102,1.603),(side*.12,-.087,1.636)];panel(m,vs,coat);m.ball((side*.125,-.047,1.640),(.009,.009,.003),leather,16,8)
# Belt with articulated buckle and keeper.
m.ring((0,-.242,1.188),[(.200,0),(.202,.039)],coat,64,.70);ellipse(m,(0,-.242,1.190),.203,.142,.0012,seam);ellipse(m,(0,-.242,1.225),.204,.143,.0012,thread)
for x in [-.035,.035]:m.rod((x,-.093,1.187),(x,-.093,1.227),.004,brass,n=10)
for z in [1.187,1.227]:m.rod((-.035,-.093,z),(.035,-.093,z),.004,brass,n=10)
m.rod((0,-.087,1.187),(0,-.087,1.223),.0025,brass,n=10)
replace('tailored torso',m)
for side in [-1,1]:
 m=Mesh();rows=[];pivot=Vector((side*.06,-.30,1.20))
 for j in range(17):
  u=j/16;rows.append([tuple(Vector((side*(.014+.24*k/16)*(1+.14*u),-.32-.16*u+.19*math.sin(k/16*math.pi)+.009*u*math.sin(k*1.2),1.20-.42*u+.055*math.sin(k/16*math.pi)))-pivot) for k in range(17)])
 strip(m,rows,coat);line(m,rows[-1],.0017,thread);ob=replace('coat tail '+str(side),m);ob.location=pivot
 # Sleeves use a shaped profile. Elbow ends are capped by rounded joint covers.
 for name,mat,radii in [('upper arm',coat,[.061,.074,.073,.065,.059]),('forearm',coat,[.057,.061,.056,.049,.045]),('thigh',navy,[.073,.086,.085,.074,.064]),('shin',navy,[.060,.067,.060,.052,.043])]:
  m=Mesh();rows=[]
  for j,rad in enumerate(radii):
   z=-.5+j*.25;rows.append([(rad*math.cos(a),rad*.92*math.sin(a),z) for a in [i*math.tau/32 for i in range(33)]])
  strip(m,rows,mat);m.add(rows[0][:-1],[tuple(reversed(range(32)))],mat);m.add(rows[-1][:-1],[tuple(range(32))],mat)
  if name in ['upper arm','forearm']:
   line(m,[(r*.97,0,-.5+j*.25) for j,r in enumerate(radii)],.0015,seam)
   if name=='forearm':
    m.ring((0,0,.37),[(.050,0),(.049,.075)],coat,32,.92)
    m.ball((.047,0,.40),(.003,.009,.014),leather,16,8)
  replace(name+' '+str(side),m)
 for label,rad,mat in [('elbow joint',.063,coat),('knee joint',.067,navy)]:
  m=Mesh();m.ball((0,0,0),(rad,rad*.94,rad),mat,32,16);add(label+' '+str(side),m)
 # Human hands: palm, articulated curled fingers, thumb and fingernails.
 def hand_mesh(opened):
  m=Mesh();m.ball((0,-.015,.022),(.033,.037,.020),skin,32,14)
  for k in range(4):
   x=(k-1.5)*.016;length=[.055,.064,.060,.047][k];pts=[]
   for j in range(7):
    u=j/6;a=-.25+u*2.9;curled=Vector((x,.005+.027*math.sin(a),.002+.027*math.cos(a)));straight=Vector((x,.005+length*u,.024+.002*math.sin(u*math.pi)));pts.append(tuple(curled.lerp(straight,opened)))
   for j,(a,b) in enumerate(zip(pts,pts[1:])):m.rod(a,b,.0067-j*.00045,skin,r2=.0063-j*.00045,n=12)
   m.ball(pts[2],(.0068,.0068,.0068),skin,16,8);m.ball(pts[-1],(.005,.006,.0038),skin,16,8)
   p=pts[-1];m.ball((p[0],p[1],p[2]+.003),(.0035,.005,.0014),nail,12,6)
  pts=[(side*-.023,-.036,.023),(side*-.042,-.016,.021),(side*-.039,.010,.011),(side*-.026,.019,.003)]
  if opened:pts=[(x*(1+.2*opened),y-.012*opened,z+.005*opened) for x,y,z in pts]
  for a,b in zip(pts,pts[1:]):m.rod(a,b,.009,skin,r2=.007,n=14)
  return m
 ob=replace('hand '+str(side),hand_mesh(0));ob.shape_key_add(name='Basis');key=ob.shape_key_add(name='Open greeting');key.data.foreach_set('co',[v for p in hand_mesh(1).v for v in p])
 # Shoes: shaped toe/vamp, separate welt and sole, ankle, laces and eyelets.
 m=Mesh();m.ball((0,.054,.045),(.062,.133,.042),leather,40,18);m.ball((0,-.028,.095),(.053,.063,.100),leather,32,16)
 m.ball((0,.055,.013),(.065,.138,.014),rubber,40,12);m.box((0,-.026,.004),(.108,.092,.025),rubber)
 ellipse(m,(0,.055,.025),.063,.135,.002,thread)
 for j in range(5):
  y=-.014+j*.016;z=.133-j*.012
  for side2 in [-1,1]:m.ball((side2*.024,y,z),(.0045,.004,.002),brass,12,6)
  m.rod((-.023,y,z+.002),(.023,y+.014,z-.009),.002,thread,n=8);m.rod((.023,y,z+.002),(-.023,y+.014,z-.009),.002,thread,n=8)
 line(m,[(-.049,.09,.062),(0,.11,.076),(.049,.09,.062)],.0015,seam);replace('boot '+str(side),m)
# Bicycle finishing: frame lugs, actual fender sheets, brake cables, chain links.
m=Mesh()
for p in [(0,0,.43),(0,-.29,.96),(0,.40,.96),(0,-.62,.36)]:m.ball(p,(.027,.029,.029),black,24,12)
for yy in [-.62,.62]:
 rows=[]
 for i in range(65):
  a=-1.28+2.56*i/64;rows.append([(x,yy+.389*math.sin(a),.36+.389*math.cos(a)) for x in [-.038,-.025,0,.025,.038]])
 strip(m,rows,black)
 for x in [-.039,.039]:line(m,[(x,yy+.389*math.sin(a),.36+.389*math.cos(a)) for a in [-1.28+2.56*i/64 for i in range(65)]],.0022,steel)
for side in [-1,1]:
 line(m,[(side*.23,.56,1.22),(side*.29,.43,1.14),(side*.17,.36,.95),(side*.08,.46,.64)],.0026,rubber)
 line(m,[(side*.08,.46,.64),(side*.065,.59,.61)],.003,steel)
 m.ball((side*.055,.62,.36),(.014,.027,.027),brass,20,10)
 # Leather saddle binding and front satchel stitching.
 line(m,[(side*.102,-.47,1.077),(side*.112,-.36,1.091),(side*.081,-.20,1.075)],.002,thread)
 for j in range(9):m.rod((side*.147,.696, .947+j*.016),(side*.147,.696,.954+j*.016),.0009,thread,n=6)
for center,r,count in [((.084,0,.43),.105,30),((.084,-.62,.36),.044,14)]:
 for i in range(count):
  a=math.tau*i/count;m.rod((center[0],center[1]+r*math.sin(a),center[2]+r*math.cos(a)),(center[0],center[1]+(r+.007)*math.sin(a),center[2]+(r+.007)*math.cos(a)),.003,steel,n=6)
for sign in [-1,1]:
 for i in range(40):
  u=i/40;y=-.62+.62*u;z=.36+sign*.044+u*(.07+sign*.061);m.rod((.082,y,z),(.082,y+.010,z+.001),.003,steel,n=6)
add('cycle crafted details',m)
# Separate the fork, handlebar, front bag and fender into a real steering group.
# The original chassis was assembled from disconnected watertight subparts;
# partition those subparts, rather than cutting through frame tubes.
def steering_partition(ob):
 me=ob.data;adj=[set() for v in me.vertices]
 for edge in me.edges:
  a,b=edge.vertices;adj[a].add(b);adj[b].add(a)
 seen=set();front=set()
 for i in range(len(adj)):
  if i in seen:continue
  stack=[i];component=[];seen.add(i)
  while stack:
   j=stack.pop();component.append(j)
   for k in adj[j]:
    if k not in seen:seen.add(k);stack.append(k)
  if sum(me.vertices[j].co.y for j in component)/len(component)>.36:front.update(component)
 result=[]
 for use_front in [False,True]:
  mesh=Mesh();indices=[j for j in range(len(me.vertices)) if (j in front)==use_front];lookup={j:k for k,j in enumerate(indices)}
  mesh.v=[tuple(me.vertices[j].co) for j in indices];mesh.m=list(me.materials)
  for face in me.polygons:
   if (face.vertices[0] in front)==use_front:mesh.f.append(tuple(lookup[j] for j in face.vertices));mesh.mi.append(face.material_index);mesh.sm.append(face.use_smooth)
  result.append(mesh)
 return result
static,turning=steering_partition(parts['bicycle chassis']);replace('bicycle chassis',static)
pivot=Vector((0,.40,.96));turning.v=[tuple(Vector(v)-pivot) for v in turning.v];steer=add('steering assembly',turning);steer.location=pivot
wheel=parts['front wheel'];wheel.parent=steer;wheel.location-=pivot
static,turning=steering_partition(parts['cycle crafted details']);replace('cycle crafted details',static)
turning.v=[tuple(Vector(v)-pivot) for v in turning.v];detail=add('front crafted details',turning);detail.parent=steer
data['parts']={k:v.name for k,v in parts.items()};data['detail_revision']=4;scene['v15_rider']=json.dumps(data)
scene['v15_hero_refinement']='featureless miniature head per user; sculpted fedora; stitched tailored coat; shaped sleeves; greeting hand shape; laced leather boots; fenders, cables, lugs and chain links'
bpy.ops.wm.save_as_mainfile(filepath=str(P/'babylon-city-v15-detail.blend'),compress=True)
(ROOT/'qa/v15/hero-detail-evidence.json').write_text(json.dumps({'revision':4,'source':'babylon-city-v15.blend','output':'babylon-city-v15-detail.blend','parts':len(parts),'features':scene['v15_hero_refinement'],'actual_closeup_validation':'pending'},indent=2),encoding='utf8')
print('V15_HERO_DETAIL_READY',len(parts),flush=True)
