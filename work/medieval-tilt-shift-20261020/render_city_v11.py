"""Deterministic 76s Blender city film, original camera path.
Reference adoption: Lemo tilt-shift demo's physical-depth + screen-band CoC,
absolute-time camera, independently quantized world motion. Blender compositor
Defocus replaces its WebGL spiral gather; this is not the identical shader.
"""
import bpy,math,json,sys,time,os
import numpy as np
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'render';OUT.mkdir(exist_ok=True)
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['proof']
mode=args[0]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'model/babylon-city-v11.blend'))
scene=bpy.context.scene;cam=scene.camera
scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.adaptive_threshold=.065;scene.cycles.use_denoising=True;scene.render.use_persistent_data=True
scene.render.threads_mode='FIXED';scene.render.threads=4
scene.cycles.max_bounces=6;scene.cycles.diffuse_bounces=3;scene.cycles.glossy_bounces=3;scene.cycles.transparent_max_bounces=4
device_type=os.environ.get('CITY_DEVICE','CUDA')
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type=device_type;prefs.get_devices()
for d in prefs.devices:d.use=d.type==device_type
scene.cycles.device='GPU';scene.cycles.seed=4409;scene.cycles.use_animated_seed=False
# Bound GPU render buffers while preserving final resolution and all city geometry.
scene.cycles.use_auto_tile=os.environ.get('CITY_TILING','0')=='1';scene.cycles.tile_size=256
scene.cycles.denoiser=os.environ.get('CITY_DENOISER','OPENIMAGEDENOISE');scene.cycles.denoising_use_gpu=os.environ.get('CITY_DENOISE_GPU','1')=='1';scene.render.compositor_device=os.environ.get('CITY_COMPOSITOR','GPU')
if mode=='eevee' or os.environ.get('CITY_ENGINE')=='EEVEE':
 scene.render.engine='BLENDER_EEVEE_NEXT';scene.eevee.taa_render_samples=64;scene.eevee.use_raytracing=True;scene.eevee.shadow_ray_count=2;scene.eevee.shadow_step_count=8
scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.render.resolution_percentage=100
if mode=='preview':scene.render.resolution_percentage=50;scene.cycles.samples=20
scene.render.fps=24;scene.frame_start=1;scene.frame_end=1824
if mode=='stills':scene.cycles.samples=24
if 'CITY_SAMPLES' in os.environ:scene.cycles.samples=int(os.environ['CITY_SAMPLES'])
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.color_depth='8';scene.render.image_settings.compression=15
cam.data.dof.use_dof=False;cam.data.clip_end=5000
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
def tilt_band(name,tilt,half):
 v=yy/(H-1)+tilt*(xx/(W-1)-.5)
 band=np.clip(np.maximum(0,np.abs(v-.49)-half)/.23,0,1)**1.45
 pixels=np.ones((H,W,4),np.float32);pixels[:,:,:3]=band[:,:,None]
 im=bpy.data.images.new(name,W,H,float_buffer=True);im.colorspace_settings.name='Non-Color';im.pixels.foreach_set(pixels.ravel());im.pack()
 return im
im=tilt_band('Street focus band',.07,.075)
statue_band=tilt_band('Diagonal focus through both divine figures',-.45,.145)
bn=nt.nodes.new('CompositorNodeImage');bn.image=im
pb=mathnode('MULTIPLY',physical.outputs[0],.30);bb=mathnode('MULTIPLY',bn.outputs[0],.70);added=mathnode('ADD',pb.outputs[0],bb.outputs[0]);clamp=mathnode('MINIMUM',added.outputs[0],1)
blur=nt.nodes.new('CompositorNodeDefocus');blur.name='Depth plus tilt band';blur.use_zbuffer=False;blur.z_scale=38;blur.blur_max=38;blur.bokeh='OCTAGON';lk.new(rl.outputs['Image'],blur.inputs['Image']);lk.new(clamp.outputs[0],blur.inputs['Z'])
mist=mathnode('MULTIPLY',rl.outputs['Mist'],1.0)
mix=nt.nodes.new('CompositorNodeMixRGB');mix.blend_type='MIX';mix.inputs[2].default_value=(.31,.36,.38,1);lk.new(mist.outputs[0],mix.inputs[0]);lk.new(blur.outputs[0],mix.inputs[1])
glare=nt.nodes.new('CompositorNodeGlare');glare.glare_type='FOG_GLOW';glare.quality='MEDIUM';glare.threshold=1.6;glare.mix=-.95;lk.new(mix.outputs[0],glare.inputs[0])
fade=nt.nodes.new('CompositorNodeMixRGB');fade.blend_type='MULTIPLY';fade.inputs[0].default_value=1;fade.inputs[2].default_value=(1,1,1,1);lk.new(glare.outputs[0],fade.inputs[1]);out=nt.nodes.new('CompositorNodeComposite');lk.new(fade.outputs[0],out.inputs[0])
def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)
def lerp(a,b,u):return tuple(x+(y-x)*u for x,y in zip(a,b))
shots=json.loads((ROOT/'v11-timeline.json').read_text(encoding='utf8'))['shots']
actors=[bpy.data.objects[n] for n in json.loads(scene['actor_names'])]
for actor in actors:
 head=next((o for o in actor.children if o.name.startswith('Resident sculpted head')),None)
 actor['safe_x_shift']=max(-2.7,min(2.7,head.location.x))-head.location.x if head and actor['base_y']<10 else 0
boat=bpy.data.objects['Animated canal boat']
water=bpy.data.materials['Canal water / rippled reflection'];noise=next(n for n in water.node_tree.nodes if n.type=='TEX_NOISE');noise.noise_dimensions='4D'
v8crowd=[bpy.data.objects[n] for n in json.loads(scene['v8_crowd'])]
v8animals=[bpy.data.objects[n] for n in json.loads(scene['v8_animals'])]
v8boats=[bpy.data.objects[n] for n in json.loads(scene['v8_boats'])]

traffic=np.load(ROOT/'traffic-v11.npz')
v11actors=[bpy.data.objects[str(n)] for n in traffic['names']]
v11poses=[[bpy.data.collections[n] for n in json.loads(o['stride_modules'])] for o in v11actors]
# Keep stable render topology for every actor. Shape keys carry exactly the
# baked stride vertices without replacing collection or mesh datablocks.
# This lets Cycles refit moving bodies instead of caching a new instance graph.
v11meshes=[[next(o.data for o in col.objects if o.type=='MESH') for col in poses] for poses in v11poses]
direct_actors=[];v11keys=[];pose_coordinates={}
for original,meshes in zip(v11actors,v11meshes):
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
 v11keys.append(keys)
v11actors=direct_actors

def at(t):
 si=next((i for i,s in enumerate(shots) if s[0]<=t<s[1]),len(shots)-1);a,b,p0,p1,q0,q1,l0,l1=shots[si];u=smooth((t-a)/(b-a))
 pos=lerp(p0,p1,u);target=lerp(q0,q1,u);cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=l0+(l1-l0)*u
 desired_band=statue_band if si==5 else im
 if bn.image!=desired_band:bn.image=desired_band
 focus.outputs[0].default_value=1/(Vector(target)-cam.location).length
 # Blend in miniature depth gently as the horizon opens, retaining the reveal.
 blur.z_scale=38*smooth(t/3);blur.blur_max=38
 wt=math.floor(t*8)/8;mt=wt*2.4
 for actor in actors:
  if actor['walk']:
   d=mt*actor['speed'];actor.location.y=d;actor.location.x=actor['safe_x_shift'];actor.location.z=.018*math.sin(mt*8+actor['phase'])
 boat.location.y=-.58*wt;boat.location.z=.025*math.sin(t*1.3)
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
 for ob,keys,s in zip(v11actors,v11keys,traffic['state'][row]):
  ob.location=(float(s[0]),float(s[1]),float(s[2]));ob.rotation_euler.z=float(s[3])
  pose=int(s[4])
  for index,key in enumerate(keys,1):
   value=float(index==pose)
   if key.value!=value:key.value=value
 noise.inputs['W'].default_value=t*.09
 f=smooth(t/.18)*(1-smooth((t-74.5)/1.5));fade.inputs[2].default_value=(f,f,f,1)
 scene.frame_set(round(t*24)+1)
 return {'time':t,'shot':si,'position':list(pos),'target':list(target),'lens':cam.data.lens,'focus':1/focus.outputs[0].default_value,'world_time':wt}

if mode=='proof':frames=[168,288,504,756,972,1176,1392,1560,1752]
elif mode=='stills':frames=[int(x) for x in args[1:]]
elif mode=='benchmark':
 scene.cycles.samples=24;frames=[192,624,720,1248]
elif mode=='eevee':frames=[192,720,1248]
elif mode=='preview':frames=list(range(0,193,3))+list(range(408,481,3))
elif mode=='sample':frames=list(range(612,684))
elif mode=='range':frames=list(range(int(args[1]),int(args[2])))
else:frames=list(range(1824))
folder=OUT/os.environ.get('CITY_FRAME_DIR',('sample-v11' if mode=='sample' else 'proof-v11' if mode=='stills' else 'proof-v11' if mode=='proof' else 'benchmark-v11' if mode=='benchmark' else 'eevee-test-v11' if mode=='eevee' else 'preview-v11' if mode=='preview' else 'frames-v11'));folder.mkdir(exist_ok=True)
evidence=[];start=time.time()
for f in frames:
 path=folder/(f'{f:05d}.png')
 if mode not in ['proof','preview'] and path.exists():continue
 state=at(f/24);temporary=folder/(f'{f:05d}.partial.png');scene.render.filepath=str(temporary);t0=time.time();bpy.ops.render.render(write_still=True);temporary.replace(path);state['seconds']=time.time()-t0;evidence.append(state)
 print('FRAME_READY',f,round(state['seconds'],2),'elapsed',round(time.time()-start,1),flush=True)
 (folder/'render-progress.json').write_text(json.dumps({'last_frame':f,'target_frames':len(frames),'elapsed':time.time()-start,'latest':state},indent=2),encoding='utf8')
(folder/('camera-evidence-'+str(frames[0])+'-'+str(frames[-1])+'.json')).write_text(json.dumps(evidence,indent=2),encoding='utf8')
if mode=='proof':bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'model/babylon-film-v11.blend'))
