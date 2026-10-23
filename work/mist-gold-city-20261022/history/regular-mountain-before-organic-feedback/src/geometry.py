"""Editable mesh batching, adapted from local Babylon Mesh helper; no old model dependency."""
import bpy, math
from mathutils import Vector
class Mesh:
 def __init__(self): self.v=[];self.f=[];self.mi=[];self.m=[];self.sm=[]
 def add(self,vs,fs,mat,smooth=False):
  if mat not in self.m:self.m.append(mat)
  k=self.m.index(mat);n=len(self.v);self.v.extend(vs);self.f.extend([tuple(n+i for i in f) for f in fs]);self.mi.extend([k]*len(fs));self.sm.extend([smooth]*len(fs))
 def box(self,p,s,mat):
  self.add([(p[0]+x*s[0]/2,p[1]+y*s[1]/2,p[2]+z*s[2]/2) for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]],[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat)
 def ball(self,p,s,mat,n=12,rings=7):
  self.add([(p[0]+s[0]*math.sin(math.pi*j/rings)*math.cos(math.tau*i/n),p[1]+s[1]*math.sin(math.pi*j/rings)*math.sin(math.tau*i/n),p[2]+s[2]*math.cos(math.pi*j/rings)) for j in range(rings+1) for i in range(n)], [((j+1)*n+i,(j+1)*n+(i+1)%n,j*n+(i+1)%n,j*n+i) for j in range(rings) for i in range(n)],mat,True)
 def rod(self,a,b,r,mat,r2=None,n=10):
  a,b=Vector(a),Vector(b);d=b-a;rot=d.to_track_quat('Z','Y').to_matrix();r2=r if r2 is None else r2
  self.add([tuple((a+b)/2+rot@Vector((rad*math.cos(math.tau*i/n),rad*math.sin(math.tau*i/n),z))) for z,rad in [(-d.length/2,r),(d.length/2,r2)] for i in range(n)],[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat,True)
 def ring(self,p,profile,mat,n=24,ys=1):
  self.add([(p[0]+r*math.cos(math.tau*i/n),p[1]+r*ys*math.sin(math.tau*i/n),p[2]+z) for r,z in profile for i in range(n)],[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(profile)-1) for i in range(n)],mat,True)
 def torus(self,p,r,minor,mat,n=32):
  self.add([(p[0]+(r+minor*math.cos(j*math.tau/8))*math.cos(i*math.tau/n),p[1]+(r+minor*math.cos(j*math.tau/8))*math.sin(i*math.tau/n),p[2]+minor*math.sin(j*math.tau/8)) for i in range(n) for j in range(8)],[(i*8+j,((i+1)%n)*8+j,((i+1)%n)*8+(j+1)%8,i*8+(j+1)%8) for i in range(n) for j in range(8)],mat,True)
 def append(self,other,pos=(0,0,0),rot=0,scale=1):
  co,si=math.cos(rot),math.sin(rot);n=len(self.v);self.v.extend([(pos[0]+scale*(co*x-si*y),pos[1]+scale*(si*x+co*y),pos[2]+scale*z) for x,y,z in other.v]);ids=[]
  for m in other.m:
   if m not in self.m:self.m.append(m)
   ids.append(self.m.index(m))
  self.f.extend([tuple(n+k for k in f) for f in other.f]);self.mi.extend([ids[k] for k in other.mi]);self.sm.extend(other.sm)
 def bake(self,name,col=None):
  me=bpy.data.meshes.new(name);me.from_pydata(self.v,[],self.f);me.update()
  for m in self.m:me.materials.append(m)
  for p,k,s in zip(me.polygons,self.mi,self.sm):p.material_index=k;p.use_smooth=s
  ob=bpy.data.objects.new(name,me);(col or bpy.context.scene.collection).objects.link(ob);return ob
def empty(name,loc=(0,0,0),parent=None):
 ob=bpy.data.objects.new(name,None);bpy.context.scene.collection.objects.link(ob);ob.location=loc;ob.parent=parent;return ob
def curve(name,pts,r,mat,parent=None):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=1;s=cu.splines.new('POLY');s.points.add(len(pts)-1)
 for p,v in zip(s.points,pts):p.co=(*v,1)
 ob=bpy.data.objects.new(name,cu);bpy.context.scene.collection.objects.link(ob);cu.materials.append(mat);ob.parent=parent;return ob
def material(name,hex,rough=.65,metal=0,texture=0):
 rgb=[int(hex[i:i+2],16)/255 for i in (0,2,4)];rgb=[x/12.92 if x<.04045 else ((x+.055)/1.055)**2.4 for x in rgb]
 ma=bpy.data.materials.new(name);ma.diffuse_color=(*rgb,1);ma.use_nodes=True;nt=ma.node_tree;p=nt.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*rgb,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 if texture:
  no=nt.nodes.new('ShaderNodeTexNoise');no.inputs['Scale'].default_value=texture;no.inputs['Detail'].default_value=2
  ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*[x*.72 for x in rgb],1);ramp.color_ramp.elements[1].color=(*[min(1,x*1.18) for x in rgb],1);nt.links.new(no.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],p.inputs['Base Color'])
  bu=nt.nodes.new('ShaderNodeBump');bu.inputs['Strength'].default_value=.19;bu.inputs['Distance'].default_value=.035;nt.links.new(no.outputs['Fac'],bu.inputs['Height']);nt.links.new(bu.outputs[0],p.inputs['Normal'])
 return ma
