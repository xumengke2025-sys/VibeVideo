from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
s=(ROOT/'render_city_v11.py').read_text(encoding='utf8').replace('v11','v12')
s=s.replace("scene.cycles.samples=24;scene.cycles.adaptive_threshold=.065", "scene.cycles.samples=32;scene.cycles.adaptive_threshold=.035")
s=s.replace("os.environ.get('CITY_DENOISE_GPU','1')=='1'", "os.environ.get('CITY_DENOISE_GPU','0')=='1'").replace("os.environ.get('CITY_COMPOSITOR','GPU')", "os.environ.get('CITY_COMPOSITOR','CPU')")
s=s.replace("cam.data.dof.use_dof=False", "scene.render.filter_size=1.25;cam.data.dof.use_dof=False")
old_blur=next(line for line in s.splitlines() if line.startswith("blur=nt.nodes.new('CompositorNodeDefocus')"))
new_blur='''# Stable separable Gaussian CoC integration avoids the GPU Defocus/result
# buffer failure diagnosed in v11. Optical depth + tilted band are retained.
blur_strength=nt.nodes.new('CompositorNodeValue');blur_strength.outputs[0].default_value=1
coc=mathnode('MULTIPLY',clamp.outputs[0],blur_strength.outputs[0])
previous=rl.outputs['Image'];lower=0
for radius in [2,5,11,22,38]:
 upper=radius/38
 fixed=nt.nodes.new('CompositorNodeBlur');fixed.filter_type='FAST_GAUSS';fixed.size_x=radius;fixed.size_y=radius;lk.new(rl.outputs['Image'],fixed.inputs['Image'])
 weight=mathnode('SUBTRACT',coc.outputs[0],lower)
 weight=mathnode('DIVIDE',weight.outputs[0],upper-lower)
 weight=mathnode('MAXIMUM',weight.outputs[0],0);weight=mathnode('MINIMUM',weight.outputs[0],1)
 squared=mathnode('MULTIPLY',weight.outputs[0],weight.outputs[0]);twice=mathnode('MULTIPLY',weight.outputs[0],2);complement=mathnode('SUBTRACT',3,twice.outputs[0]);weight=mathnode('MULTIPLY',squared.outputs[0],complement.outputs[0])
 blended=nt.nodes.new('CompositorNodeMixRGB');blended.blend_type='MIX';lk.new(weight.outputs[0],blended.inputs[0]);lk.new(previous,blended.inputs[1]);lk.new(fixed.outputs[0],blended.inputs[2]);previous=blended.outputs[0];lower=upper
blur=blended
'''
s=s.replace(old_blur,new_blur)
s=s.replace('blur.z_scale=38*smooth(t/3);blur.blur_max=38','blur_strength.outputs[0].default_value=smooth(t/3)')
s=s.replace("if mode=='stills':scene.cycles.samples=24", "if mode=='stills':scene.cycles.samples=32")
s=s.replace("bn=nt.nodes.new('CompositorNodeImage')", "canal_band=tilt_band('Canal boats and towpath focus band',.07,.115)\nbn=nt.nodes.new('CompositorNodeImage')")
s=s.replace('desired_band=statue_band if si==5 else im','desired_band=statue_band if si==5 else canal_band if si==3 else im')
s=s.replace("v12poses=[[bpy.data.collections[n] for n in json.loads(o['stride_modules'])] for o in v12actors]", "v12poses=[[bpy.data.collections[n] for n in json.loads(o['stride_modules'])] for o in v12actors]")
anchor='v12actors=direct_actors\n'
addition='''
special=json.loads(scene['v12_special']);special_objects=[];special_keys=[]
for ev in special:
 original=bpy.data.objects[ev['name']];basis=original.matrix_basis.copy();parent=original.parent;inverse=original.matrix_parent_inverse.copy()
 meshes=[next(o.data for o in bpy.data.collections[n].objects if o.type=='MESH') for n in json.loads(original['stride_modules'])]
 scale=original.scale.copy();bpy.data.objects.remove(original,do_unlink=True)
 ob=bpy.data.objects.new(ev['name'],meshes[0].copy());scene.collection.objects.link(ob);ob.parent=parent;ob.matrix_parent_inverse=inverse;ob.matrix_basis=basis
 ob.shape_key_add(name='Basis');keys=[]
 for index,mesh in enumerate(meshes[1:],1):
  coords=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('co',coords)
  key=ob.shape_key_add(name='Gesture '+str(index));key.data.foreach_set('co',coords);keys.append(key)
 special_objects.append(ob);special_keys.append(keys)
mid=json.loads(scene['v12_mid_crowd']);mid_objects=[bpy.data.objects[d['name']] for d in mid]
tows=json.loads(scene['v12_tows']);special_index={d['name']:i for i,d in enumerate(special)}
def blend_pose(keys,phase):
 p=(phase%math.tau)/math.tau*6;i=int(p);f=p-i
 for k,key in enumerate(keys,1):key.value=(1-f if k==i else 0)+(f if k==(i+1)%6 else 0)
'''
s=s.replace(anchor,anchor+addition)
s=s.replace("scene.frame_set(round(t*24)+1)\n return", "return")
s=s.replace(" si=next", " scene.frame_set(round(t*24)+1)\n si=next",1)
add_at='''
 bpy.context.view_layer.update()
 for ob,ev,keys in zip(special_objects,special,special_keys):
  p=list(ev['base']);yaw=ev['yaw'];phase=ev['phase'];kind=ev['kind']
  if kind=='patrol':p[1]+=wt*ev['speed'];phase+=wt*ev['speed']*4.6
  elif kind=='tow':
   tow=tows[ev['tow_index']];par=bpy.data.objects[tow['boat']]
   # Local attachment and moving crew share the same parent transform.
   attach=par.matrix_world@Vector(tow['attachment'])
   p[1]=attach.y+tow['direction']*ev['offset'];phase+=attach.y*4.5
   ob.rotation_euler.x=.20
  elif kind=='aboard':phase+=wt*.5;p[2]+=.012*math.sin(t*1.3+phase)
  elif ev['role'] in ['priest','acolyte','envoy','attendant']:
   phase=.25+.22*math.sin(wt*.65+phase);yaw+=.09*math.sin(wt*.35+ev['phase'])
  else:phase=0
  ob.location=p;ob.rotation_euler.z=yaw
  blend_pose(keys,phase)
 for ob,d in zip(mid_objects,mid):
  p=d['base'];ph=d['phase'];ob.location=(p[0]+.09*math.sin(wt*.19+ph),p[1]+.42*math.sin(wt*.23+ph),p[2]+.015*math.sin(wt*3.9+ph))
  ob.rotation_euler.z=d['yaw']+.075*math.sin(wt*.15+ph)
 # Updating the dependency graph before querying the attachment prevents stale
 # tow ropes in random-order evaluation or on the first frame of each process.
 bpy.context.view_layer.update()
 for tow in tows:
  par=bpy.data.objects[tow['boat']];a=par.matrix_world@Vector(tow['attachment'])
  lead=special_objects[special_index[tow['team'][0]]];b=lead.matrix_world@Vector((0,-.2,1.16))
  points=bpy.data.objects[tow['rope']].data.splines[0].points
  for j,point in enumerate(points[:9]):
   u=j/8;v=a.lerp(b,u);v.z-=.27*math.sin(math.pi*u);point.co=(*v,1)
  for j,name in enumerate(tow['team'][1:],9):
   man=special_objects[special_index[name]];v=man.matrix_world@Vector((0,-.2,1.16));points[j].co=(*v,1)
'''
s=s.replace(" noise.inputs['W'].default_value=t*.09",add_at+"\n noise.inputs['W'].default_value=t*.09")
s=s.replace("if mode=='proof':frames=[168,288,504,756,972,1176,1392,1560,1752]", "if mode=='proof':frames=[24,288,528,756,1115,1392,1752]")
(ROOT/'render_city_v12.py').write_text(s,encoding='utf8')
timeline=json.loads((ROOT/'v11-timeline.json').read_text(encoding='utf8'))
for ev in timeline['events']:ev['id']=ev['id'].replace('v11','v12')
timeline['shots'][1][4]=[-1.8,-8.5,2.8];timeline['shots'][1][5]=[-1.8,-8.5,2.8]
timeline['shots'][3][2]=[56,39,50];timeline['shots'][3][3]=[54,34,49]
timeline['shots'][3][4]=[27.5,68,0];timeline['shots'][3][5]=[27.5,62.5,1];timeline['shots'][3][6:]=[45,45]
for i,name in [(1,'蓝釉门楼与埃及使团'),(2,'市集、居民与巴比伦巡逻军队'),(3,'彩绘商船、船员与纤夫'),(5,'神像与祭司供奉'),(6,'庭院神庙仪式'),(8,'全长大道繁华巨城')]:timeline['events'][i]['name']=name
(ROOT/'v12-timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf8')
print('V12_RENDERER_READY')
