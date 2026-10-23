"""Original Babylonian fantasy architecture. Blender 4.5, Z-up, metres.
Model proof first: geometry/lighting/palette are inspectable without depth of field.
No generated image is used as a projection, background, or replacement for geometry.
"""
import bpy, math, random, json, os, sys, time
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.geometry import tessellate_polygon
from collections import defaultdict
R=random.Random(20261020)
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'out'; OUT.mkdir(exist_ok=True,parents=True)
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
MODE=argv[0] if argv else 'proof'
tstart=time.time()
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'
def srgb(h):
 h=h.lstrip('#');return tuple(((int(h[i:i+2],16)/255+.055)/1.055)**2.4 if int(h[i:i+2],16)/255>.04045 else int(h[i:i+2],16)/255/12.92 for i in (0,2,4))
def color(h):return (*srgb(h),1)
def node(ns,kind,name,x=0,y=0):
 n=ns.new(kind);n.label=name;n.location=(x,y);return n
def surface(name,base,rough=.7,metal=0,coat=0):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=color(base)
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color(base);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['Coat Weight'].default_value=coat;p.inputs['Coat Roughness'].default_value=.22
 return m
def textured(name,base,rough=.8,glaze=False):
 m=surface(name,base,rough,.06 if glaze else 0,.5 if glaze else 0);ns=m.node_tree.nodes;lk=m.node_tree.links;p=ns.get('Principled BSDF')
 tc=node(ns,'ShaderNodeTexCoord','World scale',-850,0);noise=node(ns,'ShaderNodeTexNoise','Mineral / glaze irregularity',-650,100);noise.inputs['Scale'].default_value=8 if glaze else 4;noise.inputs['Detail'].default_value=4;noise.inputs['Roughness'].default_value=.7;lk.new(tc.outputs['Object'],noise.inputs['Vector'])
 ramp=node(ns,'ShaderNodeValToRGB','Subtle colour variation',-420,190);c=srgb(base);ramp.color_ramp.elements[0].position=.15;ramp.color_ramp.elements[0].color=tuple(v*.65 for v in c)+(1,);ramp.color_ramp.elements[1].position=.85;ramp.color_ramp.elements[1].color=tuple(min(1,v*1.23) for v in c)+(1,);lk.new(noise.outputs['Fac'],ramp.inputs[0]);lk.new(ramp.outputs['Color'],p.inputs['Base Color'])
 fine=node(ns,'ShaderNodeTexNoise','Pits and surface grain',-650,-230);fine.inputs['Scale'].default_value=145 if glaze else 95;fine.inputs['Detail'].default_value=3;lk.new(tc.outputs['Object'],fine.inputs['Vector']);bump=node(ns,'ShaderNodeBump','Micro relief',-170,-120);bump.inputs['Strength'].default_value=.19 if glaze else .4;bump.inputs['Distance'].default_value=.014 if glaze else .035;lk.new(fine.outputs['Fac'],bump.inputs['Height']);lk.new(bump.outputs['Normal'],p.inputs['Normal'])
 rr=node(ns,'ShaderNodeMapRange','Nonuniform roughness',-180,80);rr.inputs['From Min'].default_value=0;rr.inputs['From Max'].default_value=1;rr.inputs['To Min'].default_value=rough-.10;rr.inputs['To Max'].default_value=rough+.13;lk.new(noise.outputs['Fac'],rr.inputs['Value']);lk.new(rr.outputs[0],p.inputs['Roughness'])
 return m
blue=[textured('Lapis fired glaze '+str(i),c,.28,True) for i,c in enumerate(['164460','1c4b66','123d59','224a63','15455f','235774','1b3c53','315a6a'])]
clay=[textured('Sun dried brick '+str(i),c,.85) for i,c in enumerate(['ae8960','b4936b','bfa079','a58968','c4a477','b9a080'])]
stone=textured('Worn limestone','c9b796',.82);mortar=textured('Recessed dusty mortar','7d7867',.93);buff=textured('Ivory glazed relief','d0b57a',.36,True);ochre=textured('Ochre glazed accent','b9914f',.33,True);wood=textured('Dark date palm timber','65503c',.82);potmat=textured('Hand fired terracotta','b57651',.73);dark=surface('Interior shade','3a322b',.9);bronze=textured('Oxidized bronze','586157',.36,True);leafmat=surface('Palm leaf','526449',.73);leaflight=surface('Palm young leaf','74805a',.68);sand=textured('Alluvial sand','a99677',.94);linen=textured('Natural flax canvas','c9b58e',.9);redcloth=textured('Madder dyed fabric','815247',.93)
materials=blue+clay+[stone,mortar,buff,ochre,wood,potmat,dark,bronze,leafmat,leaflight,sand,linen,redcloth]
# Mesh batches are real disjoint beveled solids, not cuboids with a brick picture.
batch=defaultdict(lambda:[[],[]]);counts=defaultdict(int)
bpy.ops.mesh.primitive_cube_add(size=1)
proto=bpy.context.object;be=proto.modifiers.new('Brick arris bevel','BEVEL');be.width=.042;be.segments=2
bpy.context.view_layer.objects.active=proto;bpy.ops.object.modifier_apply(modifier=be.name)
pv=[v.co.copy() for v in proto.data.vertices];pf=[tuple(p.vertices) for p in proto.data.polygons];bpy.data.objects.remove(proto,do_unlink=True)
def brick(name,pos,size,mat,rz=0,jitter=0):
 v,f=batch[(name,mat.name)];start=len(v);rot=Matrix.Rotation(rz,3,'Z');p=Vector(pos)
 for q in pv:
  w=rot@Vector((q.x*size[0],q.y*size[1],q.z*size[2]));v.append(tuple(w+p))
 f.extend(tuple(start+i for i in face) for face in pf);counts['beveled_blocks']+=1
def flush():
 for (name,mn),(v,f) in list(batch.items()):
  me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.materials.append(bpy.data.materials[mn]);ob=bpy.data.objects.new(name,me);scene.collection.objects.link(ob)
 batch.clear()
def objmesh(name,verts,faces,mat):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(name,me);scene.collection.objects.link(ob);me.materials.append(mat);return ob
def box(name,pos,size,mat,bevel=.04):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
 if bevel:
  m=o.modifiers.new('Rounded / worn edges','BEVEL');m.width=bevel;m.segments=3
  m=o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o
def uvball(name,pos,size,mat,segments=20):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=10,location=pos);o=bpy.context.object;o.name=name;o.scale=size;o.data.materials.append(mat)
 for p in o.data.polygons:p.use_smooth=True
 return o
def curve(name,pts,r,mat):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=2;s=cu.splines.new('BEZIER');s.bezier_points.add(len(pts)-1)
 for q,p in zip(s.bezier_points,pts):q.co=p;q.handle_left_type='AUTO';q.handle_right_type='AUTO'
 ob=bpy.data.objects.new(name,cu);scene.collection.objects.link(ob);cu.materials.append(mat);return ob
def rod(name,a,b,r,mat,r2=None):
 d=Vector(b)-Vector(a);p=(Vector(a)+Vector(b))/2;bpy.ops.mesh.primitive_cone_add(vertices=10,radius1=r,radius2=r if r2 is None else r2,depth=d.length,location=p);ob=bpy.context.object;ob.name=name;ob.rotation_euler=d.to_track_quat('Z','Y').to_euler();ob.data.materials.append(mat)
 for q in ob.data.polygons:q.use_smooth=True
 return ob
def lathe(name,pos,profile,mat,scale=1):
 verts=[];faces=[];N=36
 for r,z in profile:
  for i in range(N):a=i/N*math.tau;verts.append((pos[0]+r*scale*math.cos(a),pos[1]+r*scale*math.sin(a),pos[2]+z*scale))
 for j in range(len(profile)-1):
  for i in range(N):a=j*N+i;b=j*N+(i+1)%N;faces.append((a,b,b+N,a+N))
 ob=objmesh(name,verts,faces,mat)
 for p in ob.data.polygons:p.use_smooth=True
 return ob
def pot(x,y,z,s=1):
 lathe('Pot / open neck',(x,y,z),[(.2,0),(.27,.03),(.38,.2),(.43,.5),(.36,.76),(.18,.9),(.18,1),(.22,1.03),(.22,1.08),(.14,1.08),(.14,.94),(.31,.73),(.37,.5),(.2,.12)],potmat,s)
 for side in [-1,1]:curve('Ceramic loop handle',[(x+side*.2*s,y,z+.9*s),(x+side*.44*s,y,z+.88*s),(x+side*.5*s,y,z+.62*s),(x+side*.38*s,y,z+.57*s)],.035*s,potmat)
def wallface(name,axis,c,start,end,z0,z1,palette,bw=.52,bh=.22,depth=.12):
 row=0;z=z0+bh/2
 while z<z1:
  a=start-bw/2*(row%2)
  while a<end:
   lo=max(a,start);hi=min(a+bw,end)
   if hi-lo>.09:
    mid=(lo+hi)/2;dep=depth+R.uniform(-.012,.012)
    pos=(mid,c,z+R.uniform(-.006,.006)) if axis=='X' else (c,mid,z+R.uniform(-.006,.006));size=(hi-lo-.018,dep,bh-.018) if axis=='X' else (dep,hi-lo-.018,bh-.018)
    brick(name,pos,size,R.choice(palette))
   a+=bw
  row+=1;z+=bh
def rosette(x,y,z,s=1):
 uvball('Rosette centre',(x,y-.035,z),(.095*s,.05*s,.095*s),buff,12)
 for k in range(8):
  a=k*math.tau/8;ob=uvball('Eight petal ceramic rosette',(x+math.cos(a)*.18*s,y,z+math.sin(a)*.18*s),(.105*s,.042*s,.055*s),ochre,10);ob.rotation_euler[1]=-a
def relief_lion(x,y,z,s=1,flip=1):
 def p(a,b,c=0):return (x+flip*a*s,y-c*s,z+b*s)
 def ball(n,a,b,sx,sz,depth=.065,mat=buff):return uvball(n,p(a,b,.04),(sx*s,depth*s,sz*s),mat,16)
 ball('Lion muscular flank',0,.4,.57,.2);ball('Lion chest',.48,.44,.22,.29);ball('Lion head',.67,.69,.2,.2);ball('Lion muzzle',.84,.63,.17,.095);ball('Raised ear',.63,.88,.07,.09)
 for a,b,c,d in [(-.4,.36,-.5,.03),(-.2,.29,-.13,.03),(.43,.33,.38,.03),(.59,.33,.68,.03)]:curve('Lion leg',[p(a,b,.06),p((a+c)/2,b*.5,.06),p(c,d,.07)],.055*s,buff);ball('Lion paw',c+.07,d,.13,.05)
 curve('Lion curled tail',[p(-.5,.47,.05),p(-.82,.69,.05),p(-.86,.97,.05),p(-.7,1.03,.05)],.032*s,buff)
 for i in range(7):a=i/6*math.pi;curve('Mane engraved braid',[p(.56+math.cos(a)*.13,.65+math.sin(a)*.18,.10),p(.5+math.cos(a)*.16,.59+math.sin(a)*.22,.11)],.018*s,ochre)
 uvball('Lion inlaid eye',p(.75,.77,.13),(.023*s,.023*s,.023*s),dark,10)
def tower(cx):
 w=6.8;d=7.2;h=18.5;y=0
 box('Tower masonry core',(cx,y,h/2),(w-.16,d-.16,h),mortar,.12)
 for axis,c,a,b in [('X',-d/2,cx-w/2,cx+w/2),('X',d/2,cx-w/2,cx+w/2),('Y',cx-w/2,-d/2,d/2),('Y',cx+w/2,-d/2,d/2)]:wallface('Individual lapis bricks',axis,c,a,b,.14,h,blue)
 # Thicker, slightly projecting plinth and cap carry age and weight.
 for z,wadd,hh,ma in [(.28,.32,.45,stone),(1.15,.15,.18,buff),(15.8,.22,.2,ochre),(16.1,.3,.24,buff),(17.6,.33,.3,ochre),(18.35,.45,.35,blue[1])]:
  box('Tower dressed cornice',(cx,0,z),(w+wadd,d+wadd,hh),ma,.045)
 for xx in [-1,1]:
  wallface('Vertical ivory edge mosaic','X',-3.705,cx+xx*2.9-.14,cx+xx*2.9+.14,1.3,15.55,[buff,ochre],.26,.23,.08)
 for level in [3.1,6.8,10.5]:
  for offset in [-1.55,1.35]:relief_lion(cx+offset,-3.73,level,1.28,1 if cx<0 else -1)
  for offset in [-2.5,-1.25,0,1.25,2.5]:rosette(cx+offset,-3.79,level+1.95,.54)
 for i in range(9):
  x=cx-w/2+.37+i*.76
  for yy in [-3.55,3.55]:
   brick('Battlement lower step',(x,yy,18.9),(.64,.6,.8),R.choice(blue));brick('Battlement upper step',(x,yy,19.37),(.37,.57,.18),R.choice(blue))
 for yy in [-2.7,-1.2,.3,1.8,2.9]:
  for x in [cx-w/2,cx+w/2]:brick('Side battlement',(x,yy,18.9),(.6,.64,.8),R.choice(blue))
 # Recessed arrow slots with stone reveals, no fake painted windows.
 for x in [cx-1.7,cx+1.7]:
  box('Deep upper slot',(x,-3.69,16.85),(.26,.16,.9),dark,.015)
  for dx in [-.2,.2]:brick('Slot jamb',(x+dx,-3.78,16.85),(.12,.22,1.1),buff)
def arch():
 r=3.6;spring=7.9;front=-3.6;back=3.6
 # Extrados to flat top, each angular slice is solid through the passage.
 v=[];f=[];n=64
 for y in [front,back]:
  for i in range(n+1):a=math.pi*i/n;v.extend([(r*math.cos(a),y,spring+r*math.sin(a)),(r*math.cos(a),y,14.6)])
 layer=2*(n+1)
 for i in range(n):
  a=2*i;f.extend([(a,a+2,a+3,a+1),(a+layer,a+1+layer,a+3+layer,a+2+layer),(a,a+layer,a+2+layer,a+2)])
 f.extend([(0,1,layer+1,layer),(2*n,2*n+layer,2*n+1+layer,2*n+1)])
 o=objmesh('True barrel-vault portal',v,f,blue[1]);bev=o.modifiers.new('Gate arrises','BEVEL');bev.width=.035;bev.segments=2
 for j in range(3):
  rr=r+.1+j*.23
  for i in range(45):
   a=math.pi*(i+.5)/45
   brick('Radial glazed arch voussoirs',(rr*math.cos(a),front-.09,spring+rr*math.sin(a)),(.23,.17,.22),buff if j==1 else R.choice(blue))
 for x in [-3.7,3.7]:
  box('Passage gate jamb',(x,0,4),(.32,7.2,8),blue[3],.06)
  for z in [i*.3+.2 for i in range(26)]:brick('Portal ochre border',(x,front-.1,z),(.22,.15,.27),ochre)
 wallface('Arch spandrel bricks','X',front-.04,-3.5,3.5,12.1,14.4,blue)
 box('Portal parapet',(0,0,14.7),(7.7,7.4,.4),buff,.04)
 for i in range(10):brick('Portal battlement',(-3.3+i*.73,-3.58,15.2),(.52,.65,.8),R.choice(blue))
 for x in [-2.8,-1.4,0,1.4,2.8]:rosette(x,front-.2,13.2,.75)
 # Open heavy timber doors, recessed 2m behind entrance.
 for side in [-1,1]:
  for k in range(8):
   y=-1+k*.45;x=side*(3.46+.06*k)
   brick('Open cedar door planks',(x,y,3.7),(.22,.42,7.2),wood)
   for z in [1,2.6,4.2,5.8,7]:uvball('Bronze door rivet',(x-side*.14,y,z),(.035,.055,.055),bronze,8)
def wall(x0,x1,y,height):
 box('Mudbrick enceinte',((x0+x1)/2,y,height/2),(x1-x0,2.5,height),clay[0],.06)
 wallface('Enceinte brick face','X',y-1.27,x0,x1,.1,height,clay,.6,.25,.12)
 box('Wall coping',((x0+x1)/2,y,height+.1),(x1-x0+.2,2.8,.26),stone,.05)
 for i in range(int((x1-x0)/1.15)):
  x=x0+.5+i*1.15;brick('Enceinte crenel',(x,y-1.04,height+.65),(.66,.65,1),R.choice(clay));brick('Enceinte crenel cap',(x,y-1.04,height+1.18),(.76,.73,.14),stone)
 for x in range(math.ceil(x0)+1,math.floor(x1),4):box('Engaged wall buttress',(x,y-1.43,height*.49),(.78,.55,height*.98),clay[2],.06)
def stairs(x,y,z,w,n,rise=.19,run=.32,axis=1):
 for i in range(n):brick('Worn stair tread',(x,y+axis*(i+.5)*run,z+(i+.5)*rise),(w,run+.025,rise),stone)
def canopy(x,y,z,w,d,material=linen):
 verts=[];faces=[];N=24;M=18
 for j in range(M+1):
  v=j/M
  for i in range(N+1):
   u=i/N;zz=z-.36*math.sin(u*math.pi)*math.sin(v*math.pi)+.035*math.sin(u*34)*(v*.6+.4);verts.append((x+(u-.5)*w,y+(v-.5)*d,zz))
 for j in range(M):
  for i in range(N):a=j*(N+1)+i;faces.append((a,a+1,a+N+2,a+N+1))
 ob=objmesh('Tensioned woven awning',verts,faces,material);sol=ob.modifiers.new('Fabric thickness','SOLIDIFY');sol.thickness=.008
 for p in ob.data.polygons:p.use_smooth=True
 for xx in [-w/2,w/2]:
  for yy in [-d/2,d/2]:rod('Awning tied pole',(x+xx,y+yy,.05),(x+xx,y+yy,z+.15),.047,wood);curve('Hemp tie rope',[(x+xx,y+yy,z),(x+xx*1.04,y+yy*1.03,z-.12),(x+xx,y+yy,z-.4)],.014,linen)
 for yy in [-d/2,d/2]:curve('Stitched canopy hem',[(x-w/2,y+yy,z),(x,y+yy,z+.02),(x+w/2,y+yy,z)],.018,linen)
def house(x,y,w,d,h,index):
 # Four walls around a genuine inner courtyard; lintels and door openings have depth.
 box('House western wing',(x-w*.38,y,h/2),(w*.24,d,h),R.choice(clay),.06);box('House eastern wing',(x+w*.38,y,h/2),(w*.24,d,h*.92),R.choice(clay),.06);box('House rear wing',(x,y+d*.36,h/2),(w,d*.28,h),R.choice(clay),.06)
 for side in [-1,1]:box('Entrance wing',(x+side*w*.3,y-d*.4,h/2),(w*.36,d*.2,h),R.choice(clay),.06)
 box('Door stone lintel',(x,y-d*.4,2.8),(w*.24+.15,d*.21,.28),stone,.05);box('Upper entrance room',(x,y-d*.4,(h+3)/2),(w*.25,d*.2,h-3),R.choice(clay),.06)
 wallface('Hand laid house street brick','X',y-d/2-.02,x-w/2,x+w/2,3.1,h,clay,.6,.25,.09)
 for a in [x-w*.35,x+w*.35]:wallface('Lower door piers','X',y-d/2-.025,a-w*.12,a+w*.12,.1,3,clay,.6,.25,.1)
 for xx in [x-w/2,x+w/2]:box('Flat roof parapet',(xx,y,h+.3),(.23,d,.6),clay[index%len(clay)],.06)
 for yy in [y-d/2,y+d/2]:box('Flat roof parapet',(x,yy,h+.3),(w,.23,.6),clay[(index+1)%len(clay)],.06)
 # Reed mat roofs and exposed structural beam ends.
 for i in range(9):
  yy=y-d*.42+i*d*.1
  rod('Roof exposed joist',(x-w/2-.16,yy,h-.13),(x+w/2+.16,yy,h-.13),.08,wood)
 for i in range(3):pot(x-w*.33+i*.65,y+d*.22,h+.08,R.uniform(.55,.86))
 stairs(x+w*.34,y-d*.32,.05,1.25,math.floor(h/.21),.21,.26)
 if index%2==0:canopy(x,y-d/2-1.3,2.9,w*.78,2.8,linen if index%4 else redcloth)
 # Dark slots are backed by timber lattice and deep brick surrounds.
 for xx in [x-w*.29,x+w*.29]:
  box('Window recess',(xx,y-d/2-.075,3.8),(.7,.1,.85),dark,.01)
  for k in [-2,-1,0,1,2]:rod('Window grille',(xx+k*.13,y-d/2-.16,3.45),(xx+k*.13,y-d/2-.16,4.18),.022,wood)
  box('Window lintel',(xx,y-d/2-.14,4.28),(.95,.28,.17),wood,.02)
def palm(x,y,h):
 lean=R.uniform(-.7,.7);curve('Date palm trunk',[(x,y,0),(x+lean*.2,y,h*.4),(x+lean,y,h)],.18,wood)
 for k in range(int(h/.22)):
  u=k*.22/h;lathe('Old leaf scar',(x+lean*u*u,y,k*.22),[(.19,.0),(.23,.025),(.19,.06)],wood)
 v=[];f=[]
 for j in range(14):
  a=j*math.tau/14+R.uniform(-.15,.15);length=R.uniform(2.6,4.1);elev=R.uniform(.8,2);pts=[]
  for k in range(8):u=k/7;pts.append((x+lean+math.cos(a)*length*u,y+math.sin(a)*length*u,h+elev*math.sin(u*2.8)-u*.8))
  curve('Palm frond midrib',pts,.024,leaflight)
  for k in range(1,22):
   u=k/23;mid=Vector((x+lean+math.cos(a)*length*u,y+math.sin(a)*length*u,h+elev*math.sin(u*2.8)-u*.8));width=.75*math.sin(u*math.pi)**.7
   for side in [-1,1]:
    tip=mid+Vector((math.cos(a+side*.98)*width,math.sin(a+side*.98)*width,-.2));root=mid-Vector((math.cos(a)*.06,math.sin(a)*.06,0));ridge=(mid+tip)/2+Vector((0,0,.025));edge=mid+Vector((math.cos(a)*.08,math.sin(a)*.08,0));n=len(v);v.extend([tuple(root),tuple(tip),tuple(edge),tuple(ridge)]);f.extend([(n,n+1,n+3),(n+1,n+2,n+3)])
 ob=objmesh('Hundreds of individual palm leaflets',v,f,leafmat);sol=ob.modifiers.new('Leaf thickness','SOLIDIFY');sol.thickness=.003
 for j in range(4):uvball('Date fruit cluster',(x+lean+R.uniform(-.3,.3),y+R.uniform(-.3,.3),h-.35),(.16,.15,.35),ochre,12)
def market(x,y):
 box('Market counter',(x,y,.7),(2.3,.8,1.4),wood,.025)
 for k in range(8):pot(x-.9+k*.26,y+.12,1.42,R.uniform(.21,.34))
 for k in range(4):pot(x+R.uniform(-1,1),y+1.1,0,R.uniform(.5,.9))
 for k in range(3):
  xx=x-1+k*.7;lathe('Woven basket',(xx,y-.65,.05),[(.25,0),(.4,.5),(.43,.54)],wood)
  for ring in range(9):lathe('Basket wicker coil',(xx,y-.65,.05),[(.25+.18*ring/9,ring*.055),(.26+.18*ring/9,ring*.055+.023)],linen)
def paving(x0,x1,y0,y1):
 for row in range(math.ceil((y1-y0)/.67)):
  y=y0+(row+.5)*.67
  for k in range(math.ceil((x1-x0)/.85)+1):
   x=x0+(k+.5)*.85+(row%2)*.42
   if x<x1:brick('Uneven limestone street pavers',(x,y,-.035+R.uniform(-.012,.012)),(.82,.64,.13),stone,rz=R.uniform(-.016,.016))
def build():
 box('Continuous ground',(0,40,-.3),(400,400,.5),sand,.02)
 paving(-8,8,-23,35)
 tower(-7);tower(7);arch();wall(-27,-10.5,.2,7);wall(10.5,23,.2,7)
 for params in [(-17,-13,7,7,5.5,0),(-24,-9,6,8,6.7,1),(16,-11,6,7,4.6,2),(-14,14,7,8,6.4,3),(13,15,6,8,5.8,4),(-24,17,7,7,7.3,5),(-14,26,7,8,5.7,6),(13,28,7,9,6.7,7),(-25,30,8,8,6.4,8)]:house(*params)
 for p in [(-15,-18,8.8),(20,-4,10.2),(12,21,9.5),(-12,22,8.2),(-25,8,11),(22,30,10.4)]:palm(*p)
 for p in [(-12,-15),(-10,13),(11,12)]:market(*p)
 for i in range(22):pot(R.uniform(-25,-20),R.uniform(-20,-15),.02,R.uniform(.35,.7))
 # Timber quay and a water plane: visible reflection/ripple tests next to the architecture.
 box('Quay retaining wall',(24,17,-.1),(1.1,82,1.8),clay[1],.03)
 for i in range(40):brick('Quay coping stones',(23.5,-22+i*2,1),(.8,1.94,.28),stone)
 water=surface('Canal water / rippled reflection','354f51',.17,.25)
 p=water.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=.25;p.inputs['IOR'].default_value=1.333
 ns=water.node_tree.nodes;lk=water.node_tree.links;tc=node(ns,'ShaderNodeTexCoord','Water world',-700,0);noise=node(ns,'ShaderNodeTexNoise','Wind ripples',-500,0);noise.inputs['Scale'].default_value=3.3;noise.inputs['Detail'].default_value=3;lk.new(tc.outputs['Object'],noise.inputs['Vector']);bu=node(ns,'ShaderNodeBump','Water slope',-220,0);bu.inputs['Strength'].default_value=.32;bu.inputs['Distance'].default_value=.07;lk.new(noise.outputs['Fac'],bu.inputs['Height']);lk.new(bu.outputs['Normal'],p.inputs['Normal']);box('Canal surface',(33,17,.18),(17,115,.12),water,0)
 for i in range(10):brick('Timber jetty planks',(28,-11+i*.35,1),(7,.32,.18),wood)
 for x in [25,29,31]:rod('Jetty timber pile',(x,-11,-.5),(x,-11,1.5),.12,wood)
 # Small scale references, deliberately secondary to architecture.
 for x,y in [(-2,-12),(1,-8),(-1,8),(3,14),(-9,17),(12,-15)]:
  rod('Resident linen garment',(x,y,.2),(x,y,1.2),.22,linen,.13);uvball('Resident head',(x,y,1.43),(.12,.12,.15),clay[2],16);uvball('Resident linen headdress',(x,y,1.55),(.15,.15,.065),linen,16)
  for side in [-1,1]:rod('Resident sandal leg',(x+side*.08,y,0),(x+side*.08,y,.35),.04,wood)
 flush()
 print('MODEL_GEOMETRY_READY',dict(counts),flush=True)
build()
# Cycles physically based light transport. No DOF in the model verification images.
scene.render.engine='CYCLES';scene.cycles.samples=80;scene.cycles.use_denoising=True;scene.cycles.seed=20261020;scene.cycles.max_bounces=8;scene.cycles.diffuse_bounces=3;scene.cycles.glossy_bounces=4
try:
 prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
 for d in prefs.devices:d.use=d.type=='OPTIX'
 scene.cycles.device='GPU';print('CYCLES_DEVICES',[(d.name,d.type,d.use) for d in prefs.devices],flush=True)
except Exception as e:print('GPU_SETUP',repr(e),flush=True)
world=bpy.data.worlds.new('Afternoon sky');scene.world=world;world.use_nodes=True;ns=world.node_tree.nodes;lk=world.node_tree.links;bg=ns.get('Background');bg.inputs['Strength'].default_value=.35;sky=node(ns,'ShaderNodeTexSky','Nishita sky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(25);sky.sun_rotation=math.radians(218);sky.sun_disc=False;sky.altitude=.15;sky.air_density=1.1;sky.dust_density=1.7;lk.new(sky.outputs[0],bg.inputs['Color'])
bpy.ops.object.light_add(type='SUN',location=(0,0,30));sun=bpy.context.object;sun.name='Warm late afternoon key';sun.data.energy=3.1;sun.data.angle=math.radians(1.0);sun.data.color=(1,.79,.55);sun.rotation_euler=(math.radians(47),math.radians(-22),math.radians(-35))
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.25
scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.render.resolution_percentage=70 if MODE=='preview' else 100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.film_transparent=False
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Model inspection camera';scene.camera=cam;cam.data.lens=48;cam.data.sensor_width=36;cam.data.clip_end=1000;cam.data.dof.use_dof=False
def camera(pos,target,lens=48):cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
camera((36,-54,31),(0,1,9.5),48)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'babylon-gate-street-v1.blend'))
manifest={'version':'model-v1','geometry':dict(counts),'objects':len(scene.objects),'render_engine':'Cycles','dof':False,'model':str(ROOT/'babylon-gate-street-v1.blend'),'external_image_assets':False,'scope':'gate + adjacent street block; full city not yet built','removed':['dragon','ember delivery'],'output_dimensions':[round(1080*scene.render.resolution_percentage/100),round(1920*scene.render.resolution_percentage/100)],'build_seconds':time.time()-tstart}
(OUT/'model-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
for label,pos,target,lens in [('gate-street',(36,-54,31),(0,1,9.5),48),('glaze-detail',(16,-18,12),(7,-3.6,8.4),67),('street-reverse',(-12,32,16),(-1,0,7),44)]:
 camera(pos,target,lens);scene.render.filepath=str(OUT/(label+'-v1.png'));bpy.ops.render.render(write_still=True);print('RENDER_READY',label,flush=True)
print('MODEL_COMPLETE',time.time()-tstart,flush=True)
