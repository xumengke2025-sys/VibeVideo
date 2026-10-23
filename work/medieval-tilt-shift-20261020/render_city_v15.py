"""Deterministic 76s Blender city film, original camera path.
Reference adoption: Lemo tilt-shift demo's physical-depth + screen-band CoC,
absolute-time camera, independently quantized world motion. Blender compositor
Multi-level Gaussian replaces its WebGL gather; this is an approximation.
"""
import bpy,math,json,sys,time,os
import numpy as np
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'render';OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT))
import v14_motion
import v15_motion
from bpy_extras.object_utils import world_to_camera_view
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['proof']
mode=args[0]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'model/babylon-city-v15-detail.blend'))
scene=bpy.context.scene;cam=scene.camera
v14data=v14_motion.setup(scene)
rider_data=v15_motion.setup(scene)
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.adaptive_threshold=.035;scene.cycles.use_denoising=True;scene.render.use_persistent_data=True
scene.render.threads_mode='FIXED';scene.render.threads=4
scene.cycles.max_bounces=6;scene.cycles.diffuse_bounces=3;scene.cycles.glossy_bounces=3;scene.cycles.transparent_max_bounces=4
device_type=os.environ.get('CITY_DEVICE','CUDA')
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type=device_type;prefs.get_devices()
for d in prefs.devices:d.use=d.type==device_type
scene.cycles.device='GPU';scene.cycles.seed=4409;scene.cycles.use_animated_seed=False
# Bound GPU render buffers while preserving final resolution and all city geometry.
scene.cycles.use_auto_tile=os.environ.get('CITY_TILING','0')=='1';scene.cycles.tile_size=256
scene.cycles.denoiser=os.environ.get('CITY_DENOISER','OPENIMAGEDENOISE');scene.cycles.denoising_use_gpu=os.environ.get('CITY_DENOISE_GPU','0')=='1';scene.render.compositor_device=os.environ.get('CITY_COMPOSITOR','CPU')
if mode=='eevee' or os.environ.get('CITY_ENGINE')=='EEVEE':
 scene.render.engine='BLENDER_EEVEE_NEXT';scene.eevee.taa_render_samples=64;scene.eevee.use_raytracing=True;scene.eevee.shadow_ray_count=2;scene.eevee.shadow_step_count=8
scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.render.resolution_percentage=100
if mode=='preview':scene.render.resolution_percentage=35;scene.cycles.samples=12
if 'CITY_SCALE' in os.environ:scene.render.resolution_percentage=int(os.environ['CITY_SCALE'])
scene.render.fps=24;scene.frame_start=1;scene.frame_end=2160
if mode in ['stills','character']:scene.cycles.samples=32
if 'CITY_SAMPLES' in os.environ:scene.cycles.samples=int(os.environ['CITY_SAMPLES'])
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.color_depth='8';scene.render.image_settings.compression=15
scene.render.filter_size=1.25;cam.data.dof.use_dof=False;cam.data.clip_end=5000
scene.view_layers[0].use_pass_z=True;scene.view_layers[0].use_pass_mist=True
scene.world.mist_settings.start=400;scene.world.mist_settings.depth=2200;scene.world.mist_settings.falloff='LINEAR'

# Signed contributions do not cancel: mix their magnitudes, as in corrected study.
scene.use_nodes=True;nt=scene.node_tree;nt.nodes.clear();lk=nt.links
rl=nt.nodes.new('CompositorNodeRLayers')
def mathnode(op,a=None,b=None):
 n=nt.nodes.new('CompositorNodeMath');n.operation=op
 if a is not None:
  if isinstance(a,(float,int)):n.inputs[0].default_value=a
  else:lk.new(a,n.inputs[0])
 if b is not None:
  if isinstance(b,(float,int)):n.inputs[1].default_value=b
  else:lk.new(b,n.inputs[1])
 return n
depth=mathnode('MAXIMUM',rl.outputs['Depth'],.1)
inv=mathnode('DIVIDE',1,depth.outputs[0]);focus=nt.nodes.new('CompositorNodeValue');focus.name='Reciprocal focus distance'
diff=mathnode('SUBTRACT',focus.outputs[0],inv.outputs[0]);ab=mathnode('ABSOLUTE',diff.outputs[0]);physical=mathnode('MULTIPLY',ab.outputs[0],27)
W=1080;H=1920;yy,xx=np.mgrid[0:H,0:W]
def coord_image(name,values):
 pixels=np.ones((H,W,4),np.float32);pixels[:,:,:3]=values[:,:,None]
 image=bpy.data.images.new(name,W,H,float_buffer=True);image.colorspace_settings.name='Non-Color';image.pixels.foreach_set(pixels.ravel());image.pack()
 ob=nt.nodes.new('CompositorNodeImage');ob.image=image;return ob.outputs['Image']
cx=coord_image('V15 screen x',xx/(W-1));cy=coord_image('V15 screen y',yy/(H-1))
def val(name,value):
 n=nt.nodes.new('CompositorNodeValue');n.name=name;n.outputs[0].default_value=value;return n
band_center=val('V15 tracked focus center',.49);band_half=val('V15 adaptive focus width',.09);band_tilt=val('V15 shot focus tilt',.07)
dx=mathnode('SUBTRACT',cx,.5);slant=mathnode('MULTIPLY',dx.outputs[0],band_tilt.outputs[0]);ytilt=mathnode('ADD',cy,slant.outputs[0]);offset=mathnode('SUBTRACT',ytilt.outputs[0],band_center.outputs[0]);mag=mathnode('ABSOLUTE',offset.outputs[0]);outside=mathnode('SUBTRACT',mag.outputs[0],band_half.outputs[0]);outside=mathnode('MAXIMUM',outside.outputs[0],0);outside=mathnode('DIVIDE',outside.outputs[0],.23);outside=mathnode('MINIMUM',outside.outputs[0],1);band=mathnode('POWER',outside.outputs[0],1.45)
pb=mathnode('MULTIPLY',physical.outputs[0],.30);bb=mathnode('MULTIPLY',band.outputs[0],.70);added=mathnode('ADD',pb.outputs[0],bb.outputs[0]);clamp=mathnode('MINIMUM',added.outputs[0],1)
# Stable separable Gaussian CoC integration avoids the GPU Defocus/result
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

mist=mathnode('MULTIPLY',rl.outputs['Mist'],1.0)
mix=nt.nodes.new('CompositorNodeMixRGB');mix.blend_type='MIX';mix.inputs[2].default_value=(.31,.36,.38,1);lk.new(mist.outputs[0],mix.inputs[0]);lk.new(blur.outputs[0],mix.inputs[1])
glare=nt.nodes.new('CompositorNodeGlare');glare.glare_type='FOG_GLOW';glare.quality='MEDIUM';glare.threshold=1.6;glare.mix=-.95;lk.new(mix.outputs[0],glare.inputs[0])
fade=nt.nodes.new('CompositorNodeMixRGB');fade.blend_type='MULTIPLY';fade.inputs[0].default_value=1;fade.inputs[2].default_value=(1,1,1,1);lk.new(glare.outputs[0],fade.inputs[1]);out=nt.nodes.new('CompositorNodeComposite');lk.new(fade.outputs[0],out.inputs[0])
def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)
def lerp(a,b,u):return tuple(x+(y-x)*u for x,y in zip(a,b))
shots=json.loads((ROOT/'v14-timeline.json').read_text(encoding='utf8'))['shots']
actors=[bpy.data.objects[n] for n in json.loads(scene['actor_names'])]
for actor in actors:
 head=next((o for o in actor.children if o.name.startswith('Resident sculpted head')),None)
 actor['safe_x_shift']=max(-2.7,min(2.7,head.location.x))-head.location.x if head and actor['base_y']<10 else 0
boat=bpy.data.objects['Animated canal boat']
water=bpy.data.materials['Canal water / rippled reflection'];noise=next(n for n in water.node_tree.nodes if n.type=='TEX_NOISE');noise.noise_dimensions='4D'
v8crowd=[bpy.data.objects[n] for n in json.loads(scene['v8_crowd'])]
v8animals=[bpy.data.objects[n] for n in json.loads(scene['v8_animals'])]
v8boats=[bpy.data.objects[n] for n in json.loads(scene['v8_boats'])]

traffic=np.load(ROOT/'traffic-v14.npz')
v15actors=[bpy.data.objects[str(n)] for n in traffic['names']]
v15poses=[[bpy.data.collections[n] for n in json.loads(o['stride_modules'])] for o in v15actors]
# Keep stable render topology for every actor. Shape keys carry exactly the
# baked stride vertices without replacing collection or mesh datablocks.
# This lets Cycles refit moving bodies instead of caching a new instance graph.
v15meshes=[[next(o.data for o in col.objects if o.type=='MESH') for col in poses] for poses in v15poses]
direct_actors=[];v15keys=[];pose_coordinates={}
for original,meshes in zip(v15actors,v15meshes):
 name=original.name;transform=original.matrix_world.copy()
 bpy.data.objects.remove(original,do_unlink=True)
 actor=bpy.data.objects.new(name,meshes[0].copy());scene.collection.objects.link(actor)
 actor.matrix_world=transform;direct_actors.append(actor)
 actor.shape_key_add(name='Basis')
 keys=[]
 for index,mesh in enumerate(meshes[1:],1):
  if mesh.name not in pose_coordinates:
   coords=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('co',coords);pose_coordinates[mesh.name]=coords
  key=actor.shape_key_add(name='Baked stride '+str(index));key.data.foreach_set('co',pose_coordinates[mesh.name]);keys.append(key)
 v15keys.append(keys)
v15actors=direct_actors

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
# Free unlinked stride source collections after baking their shape keys.
del v15poses,v15meshes,pose_coordinates,meshes
print('V15_ORPHANS_PURGED',bpy.data.orphans_purge(do_local_ids=True,do_linked_ids=False,do_recursive=True),flush=True)
import gc;gc.collect()
def blend_pose(keys,phase):
 count=len(keys)+1;p=(phase%math.tau)/math.tau*count;i=int(p);f=p-i
 for k,key in enumerate(keys,1):key.value=(1-f if k==i else 0)+(f if k==(i+1)%count else 0)

def city_at(t):
 scene.frame_set(round(t*24)+1)
 si=next((i for i,s in enumerate(shots) if s[0]<=t<s[1]),len(shots)-1);a,b,p0,p1,q0,q1,l0,l1=shots[si];raw=(t-a)/(b-a);u=(.72*raw+.28*smooth(raw)) if si in [2,3,4,8] else smooth(raw)
 pos=lerp(p0,p1,u);target=lerp(q0,q1,u);cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=l0+(l1-l0)*u

 focus.outputs[0].default_value=1/(Vector(target)-cam.location).length
 # Blend in miniature depth gently as the horizon opens, retaining the reveal.
 blur_strength.outputs[0].default_value=smooth(t/3)
 wt=math.floor(t*8)/8;mt=wt*2.4
 for actor in actors:
  if actor['walk']:
   d=mt*actor['speed'];actor.location.y=d;actor.location.x=actor['safe_x_shift'];actor.location.z=.018*math.sin(mt*8+actor['phase'])
 boat.location.y=12-.58*wt;boat.location.z=.025*math.sin(t*1.3)
 # Deterministic lane motion; no wrapping or teleportation in the shot window.
 for ob in v8crowd:
  base=Vector(ob['base']);speed=ob['speed']
  if base.x>40:base.x=21.1
  # New pedestrian paths occupy open main avenue and unobstructed quay sections.
  phase=mt*.14+ob['phase'];dy=math.sin(phase)*speed*10 if ob['span'] else 0
  if ob['span']==78 and base.y+dy<8:dy=8-(base.y+dy)+8-base.y
  ob.location=base+Vector((0,dy,.025*math.sin(mt*9+ob['phase'])))
  if ob['span']:ob.rotation_euler.z=0 if speed*math.cos(phase)>=0 else math.pi
 for ob in v8animals:
  ob.location=Vector(ob['base'])+Vector((0,math.sin(mt*.14)*ob['speed']*8,.018*math.sin(mt*8+ob['phase'])))
  ob.rotation_euler.z=math.pi if math.cos(mt*.14)>=0 else 0
 for ob in v8boats:
  ob.location=Vector(ob['base'])+Vector((0,math.sin(wt*.04)*ob['speed']*12,.018*math.sin(t*1.3+ob['phase'])))
 row=min(len(traffic['state'])-1,int(math.floor(t*8)))
 for ob,keys,s in zip(v15actors,v15keys,traffic['state'][row]):
  ob.location=(float(s[0]),float(s[1]),float(s[2]));ob.rotation_euler.z=float(s[3])
  pose=int(s[4])
  for index,key in enumerate(keys,1):
   value=float(index==pose)
   if key.value!=value:key.value=value

 bpy.context.view_layer.update()
 for ob,ev,keys in zip(special_objects,special,special_keys):
  p=list(ev['base']);yaw=ev['yaw'];phase=ev['phase'];kind=ev['kind']
  if kind=='patrol':
   p[1]+=t*ev['speed'];phase+=math.tau*t*ev['speed']/ev['stride_length']
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
  p=d['base'];ph=d['phase'];amp=.10 if d.get('grouped') else 1.0;ob.location=(p[0]+amp*.09*math.sin(wt*.19+ph),p[1]+amp*.42*math.sin(wt*.23+ph),p[2]+.015*math.sin(wt*3.9+ph))
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

 detail=v14_motion.update(v14data,t)
 tilt=-.45 if si==5 else -.08 if si==6 else .07
 half=.145 if si==5 else .12 if si==3 else .115 if si==6 else .09
 center=.49
 subject=None
 if si==2:subject=Vector((1.99,24.1+t*1.05-3.2,1.1))
 elif si==3:
  w=v14data['wakes'][-1];subject=bpy.data.objects[w['boat']].matrix_world@Vector(w['center']);subject.z=.65
 elif si==6:subject=Vector(detail['offering_dish'])
 if subject is not None:
  projection=world_to_camera_view(scene,cam,subject);desired=projection.y+tilt*(projection.x-.5)
  center=max(.40,min(.59,.49*.25+desired*.75));focus.outputs[0].default_value=1/(subject-cam.location).length
 if si==8:half=.125+.065*smooth(raw);blur_strength.outputs[0].default_value=.92-.20*smooth(raw)
 band_center.outputs[0].default_value=center;band_half.outputs[0].default_value=half;band_tilt.outputs[0].default_value=tilt
 noise.inputs['W'].default_value=t*.09
 f=smooth(t/.18)*(1-smooth((t-74.5)/1.5));fade.inputs[2].default_value=(f,f,f,1)
 return {'time':t,'shot':si,'position':list(pos),'target':list(target),'lens':cam.data.lens,'focus':1/focus.outputs[0].default_value,'world_time':wt,'focus_band_center':center,'focus_band_half':half,'action':detail}


def at(t):
 state=city_at(min(75.95,t*76/90))
 pose=v15_motion.camera(t);action=v15_motion.update(rider_data,t)
 cam.location=pose['position'];target=Vector(pose['target']);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=pose['lens']
 if mode=='character':
  base=Vector(action['position']);cam.location=base+Vector((3.2,3.8,2.8));target=base+Vector((0,0,1.08));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=60
 bpy.context.view_layer.update();subject=Vector(action['position'])+Vector((0,0,1.15));projected=world_to_camera_view(scene,cam,subject)
 focus.outputs[0].default_value=1/max(.1,(subject-cam.location).length)
 # Smoothly open a small corridor around this persistent moving protagonist.
 forward=Vector((-math.sin(action['yaw']),math.cos(action['yaw']),0));normal=Vector((forward.y,-forward.x,0));rp=Vector(action['position'])
 for ob in v15actors+mid_objects+v8crowd:
  delta=ob.location-rp;along=delta.dot(forward);across=delta.dot(normal)
  if abs(along)<3.8 and abs(across)<1.15 and ob.location.z<2:
   weight=smooth((3.8-abs(along))/1.5);shift=(1.15-abs(across))*weight*(1 if across>=0 else -1);ob.location+=normal*shift
 for ob,ev,keys in zip(special_objects,special,special_keys):
  role=ev['role'];response=0
  if role in ['envoy','attendant']:response=v15_motion.route.pulse(t,12.7,13.4,15.2,16)
  elif role=='crew':response=v15_motion.route.pulse(t,35.8,36.5,38,39)
  if response:
   delta=rp-ob.location;look=math.atan2(delta.x,-delta.y);difference=(look-ob.rotation_euler.z+math.pi)%math.tau-math.pi;ob.rotation_euler.z+=difference*.7*response;blend_pose(keys,.5+.35*response*math.sin(t*3))
 # West-bank team stays on its paved towpath while passing the cyclist.
 for tow in tows:
  if tow.get('bank_side')=='west':
   for name in tow['team']:
    man=special_objects[special_index[name]];gap=abs(man.location.y-rp.y);man.location.x+=.45*smooth((4-gap)/2) if gap<4 and abs(rp.x-22.8)<1 else 0
 bpy.context.view_layer.update()
 for tow in tows:
  par=bpy.data.objects[tow['boat']];anchor=par.matrix_world@Vector(tow['attachment']);points=bpy.data.objects[tow['rope']].data.splines[0].points
  lead=special_objects[special_index[tow['team'][0]]];end=lead.matrix_world@Vector((0,-.2,1.16))
  for j,point in enumerate(points[:9]):
   u=j/8;v=anchor.lerp(end,u);v.z-=.27*math.sin(math.pi*u);point.co=(*v,1)
  for j,name in enumerate(tow['team'][1:],9):
   man=special_objects[special_index[name]];v=man.matrix_world@Vector((0,-.2,1.16));points[j].co=(*v,1)
 half=.13 if pose['shot'] in [3,6] else .095
 if mode=='character':half=.44
 if pose['shot']==8:half=.12+.075*pose['progress']
 band_center.outputs[0].default_value=max(.22,min(.76,projected.y));band_half.outputs[0].default_value=half;band_tilt.outputs[0].default_value=.035
 blur_strength.outputs[0].default_value=smooth(t/3)*(.9-.18*pose['progress'] if pose['shot']==8 else 1)
 if mode=='character':blur_strength.outputs[0].default_value=.12
 f=smooth(t/.18)*(1-smooth((t-88.5)/1.5));fade.inputs[2].default_value=(f,f,f,1)
 state.update(time=t,shot=pose['shot'],position=list(cam.location),target=list(target),lens=cam.data.lens,rider=action,rider_projection=list(projected))
 return state

if mode=='audit':
 report=[]
 for seconds in [0,8,13.5,22,29,36,50.5,64,67.8,70,76,86,13.5]:report.append(at(seconds))
 (ROOT/'qa/v15/action-state-audit.json').write_text(json.dumps(report,indent=2),encoding='utf8')
 print('V15_STATE_AUDIT',max(r['rider']['max_arm_reach'] for r in report),flush=True)
 sys.exit(0)
if mode=='character':frames=[528,1632]
elif mode=='proof':frames=[96,324,552,864,1212,1536,1632,1872,2064]
elif mode=='stills':frames=[int(x) for x in args[1:]]
elif mode=='benchmark':
 scene.cycles.samples=24;frames=[192,624,720,1248]
elif mode=='eevee':frames=[192,720,1248]
elif mode=='preview':frames=list(range(0,193,3))+list(range(408,481,3))
elif mode=='sample':frames=list(range(612,684))
elif mode=='range':frames=list(range(int(args[1]),int(args[2])))
else:frames=list(range(2160))
folder=OUT/os.environ.get('CITY_FRAME_DIR',('sample-v15' if mode=='sample' else 'proof-v15' if mode=='stills' else 'proof-v15' if mode=='proof' else 'benchmark-v15' if mode=='benchmark' else 'eevee-test-v15' if mode=='eevee' else 'preview-v15' if mode=='preview' else 'frames-v15'));folder.mkdir(exist_ok=True)
evidence=[];start=time.time()
for f in frames:
 path=folder/(f'{f:05d}.png')
 if mode not in ['proof','preview'] and path.exists():continue
 state=at(f/24);temporary=folder/(f'{f:05d}.partial.png');scene.render.filepath=str(temporary);t0=time.time();bpy.ops.render.render(write_still=True);temporary.replace(path);state['seconds']=time.time()-t0;evidence.append(state)
 print('FRAME_READY',f,round(state['seconds'],2),'elapsed',round(time.time()-start,1),flush=True)
 (folder/'render-progress.json').write_text(json.dumps({'last_frame':f,'target_frames':len(frames),'elapsed':time.time()-start,'latest':state},indent=2),encoding='utf8')
(folder/('camera-evidence-'+str(frames[0])+'-'+str(frames[-1])+'.json')).write_text(json.dumps(evidence,indent=2),encoding='utf8')
if mode=='proof':bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'model/babylon-film-v15.blend'))
