import bpy,math,random,json,time
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'out';R=random.Random(19042)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'babylon-city-v2.blend'))
scene=bpy.context.scene
# Eliminate the deliberately crude distant cubes: background uses real courtyard modules.
for o in list(scene.objects):
 if o.name.startswith(('Distant adobe city','Distant roof cornice')):bpy.data.objects.remove(o,do_unlink=True)
modules=[bpy.data.collections.get('Courtyard house module '+str(i)) for i in range(3)]
for j in range(16):
 for k in range(23):
  x=-113+k*10.2+R.uniform(-1.3,1.3);y=145+j*10.5+R.uniform(-1.4,1.4)
  if 24<x<43:continue
  ob=bpy.data.objects.new('Distant inhabited courtyard',None);ob.instance_type='COLLECTION';ob.instance_collection=R.choice(modules);scene.collection.objects.link(ob);ob.location=(x,y,0);ob.rotation_euler[2]=R.choice([0,math.pi/2,math.pi,math.pi*1.5])+R.uniform(-.025,.025);s=R.uniform(.92,1.25);ob.scale=(s,s,R.uniform(.75,1.5))
# Break uniform rows with scale and facade orientation; retain the canal and processional axis.
for ob in scene.objects:
 if ob.name.startswith(('Courtyard neighbourhood','East bank courtyard')):
  ob.rotation_euler[2]+=R.choice([0,math.pi/2,math.pi,math.pi*1.5]);ob.scale.z*=R.uniform(.88,1.25)
# Give terrace cypress an actual serrated needle canopy rather than a smooth oval primitive.
verts=[];faces=[]
for j in range(23):
 z=-.95+j/22*1.9;radius=.91*(1-abs(z)**1.8)**.5
 for k in range(17):
  a=k*math.tau/17+j*.47;r=radius*R.uniform(.72,1.08);base=Vector((math.cos(a)*r*.55,math.sin(a)*r*.55,z));tip=Vector((math.cos(a)*r,math.sin(a)*r,z+R.uniform(.03,.13)));off=Vector((-math.sin(a)*.11,math.cos(a)*.11,0));n=len(verts);verts.extend([tuple(base-off),tuple(tip),tuple(base+off),tuple(base+Vector((0,0,.09)))]);faces.extend([(n,n+1,n+3),(n+1,n+2,n+3)])
me=bpy.data.meshes.new('Layered cypress needle sprays');me.from_pydata(verts,[],faces);me.materials.append(bpy.data.materials['Palm leaf'])
for ob in scene.objects:
 if ob.name.startswith('Cypress crown'):ob.data=me
# Duplicate frond silhouettes with a small azimuth offset to create a full crown, using actual leaves.
for ob in list(scene.objects):
 if ob.name.startswith('Hundreds of individual palm leaflets'):
  vv=[v.co.copy() for v in ob.data.vertices];center=sum(vv,Vector())/len(vv);rot=Matrix.Rotation(.21,3,'Z');copy=ob.copy();copy.data=ob.data.copy();copy.name='Secondary palm frond whorl';scene.collection.objects.link(copy)
  for v in copy.data.vertices:v.co=center+rot@(v.co-center)+Vector((0,0,.18))
# Shared lighting stays coherent across all camera angles. Reduced sky fill makes shadows legible.
bg=scene.world.node_tree.nodes.get('Background');bg.inputs['Strength'].default_value=.075
sun=bpy.data.objects['Warm late afternoon key'];sun.data.energy=3.5;sun.data.angle=math.radians(.8);sun.data.color=(1,.75,.46);sun.rotation_euler=(math.radians(66),math.radians(-12),math.radians(-30))
scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.15
for name in ['Palm leaf','Palm young leaf']:
 mat=bpy.data.materials[name];p=mat.node_tree.nodes.get('Principled BSDF');c=p.inputs['Base Color'].default_value;p.inputs['Base Color'].default_value=(c[0]*.65,c[1]*.8,c[2]*.6,1)
# Dense foreground market clusters are assembled from existing geometry, with enough room for camera travel.
for x,y in [(-34,-8),(-27,-22),(-16,-28),(15,-25),(25,-24),(51,-17),(-42,13),(-38,30),(-50,5)]:
 ob=bpy.data.objects.new('Foreground street block',None);ob.instance_type='COLLECTION';ob.instance_collection=R.choice(modules);scene.collection.objects.link(ob);ob.location=(x,y,0);ob.rotation_euler[2]=R.choice([0,math.pi/2,math.pi]);ob.scale=(R.uniform(.85,1.1),R.uniform(.85,1.1),R.uniform(.8,1.2))
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
scene.cycles.device='GPU';scene.cycles.samples=96;scene.render.resolution_percentage=100
cam=scene.camera;cam.data.dof.use_dof=False
def camera(pos,target,lens):cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
camera((-48,-104,83),(19,45,9),58)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'babylon-city-v3.blend'))
for label,pos,target,lens in [('city-overview',(-48,-104,83),(19,45,9),58),('gate-street',(29,-40,25),(0,4,8),45),('canal-temple',(13,13,29),(52,77,13),42)]:
 camera(pos,target,lens);scene.render.filepath=str(OUT/(label+'-v3.png'));bpy.ops.render.render(write_still=True);print('PROOF_READY',label,flush=True)
e={'version':'v3','model':str(ROOT/'babylon-city-v3.blend'),'dof':False,'resolution':[1080,1920],'adjustments':['removed distant cubes; linked courtyard houses','less uniform neighbourhoods','needle cypress and fuller palms','lower-angle sun and lower sky fill','denser foreground street blocks'],'scope':'model proofs, not a finished film','audio':'not created'}
(OUT/'model-v3-evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2),encoding='utf8')
