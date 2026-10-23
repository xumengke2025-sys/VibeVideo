"""Deterministic 56s Blender city film, original camera path.
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
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'model/babylon-city-v6.blend'))
scene=bpy.context.scene;cam=scene.camera
scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.adaptive_threshold=.065;scene.cycles.use_denoising=True;scene.cycles.use_persistent_data=True
scene.render.threads_mode='FIXED';scene.render.threads=4
scene.cycles.max_bounces=6;scene.cycles.diffuse_bounces=3;scene.cycles.glossy_bounces=3;scene.cycles.transparent_max_bounces=4
device_type=os.environ.get('CITY_DEVICE','OPTIX')
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type=device_type;prefs.get_devices()
for d in prefs.devices:d.use=d.type==device_type
scene.cycles.device='GPU';scene.cycles.seed=4409;scene.cycles.use_animated_seed=False
# Bound GPU render buffers while preserving final resolution and all city geometry.
scene.cycles.use_auto_tile=True;scene.cycles.tile_size=256
scene.cycles.denoiser='OPTIX';scene.cycles.denoising_use_gpu=True;scene.render.compositor_device=os.environ.get('CITY_COMPOSITOR','GPU')
if mode=='eevee':
 scene.render.engine='BLENDER_EEVEE_NEXT';scene.eevee.taa_render_samples=32;scene.eevee.use_raytracing=True;scene.eevee.shadow_ray_count=2;scene.eevee.shadow_step_count=8
scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.render.resolution_percentage=100
if mode=='preview':scene.render.resolution_percentage=50;scene.cycles.samples=20
scene.render.fps=24;scene.frame_start=1;scene.frame_end=1344
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.color_depth='8';scene.render.image_settings.compression=15
cam.data.dof.use_dof=False;cam.data.clip_end=2000
scene.view_layers[0].use_pass_z=True;scene.view_layers[0].use_pass_mist=True
scene.world.mist_settings.start=130;scene.world.mist_settings.depth=1200;scene.world.mist_settings.falloff='LINEAR'

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
W=1080;H=1920;yy,xx=np.mgrid[0:H,0:W];v=yy/(H-1)+.07*(xx/(W-1)-.5)
band=np.clip(np.maximum(0,np.abs(v-.49)-.17)/.5,0,1)**1.45
pixels=np.ones((H,W,4),np.float32);pixels[:,:,:3]=band[:,:,None]
im=bpy.data.images.new('Tilt band magnitude',W,H,float_buffer=True);im.colorspace_settings.name='Non-Color';im.pixels.foreach_set(pixels.ravel());im.pack()
bn=nt.nodes.new('CompositorNodeImage');bn.image=im
pb=mathnode('MULTIPLY',physical.outputs[0],.58);bb=mathnode('MULTIPLY',bn.outputs[0],.42);added=mathnode('ADD',pb.outputs[0],bb.outputs[0]);clamp=mathnode('MINIMUM',added.outputs[0],1)
blur=nt.nodes.new('CompositorNodeDefocus');blur.name='Depth plus tilt band';blur.use_zbuffer=False;blur.z_scale=22;blur.blur_max=22;blur.bokeh='OCTAGON';lk.new(rl.outputs['Image'],blur.inputs['Image']);lk.new(clamp.outputs[0],blur.inputs['Z'])
mist=mathnode('MULTIPLY',rl.outputs['Mist'],1.0)
mix=nt.nodes.new('CompositorNodeMixRGB');mix.blend_type='MIX';mix.inputs[2].default_value=(.31,.36,.38,1);lk.new(mist.outputs[0],mix.inputs[0]);lk.new(blur.outputs[0],mix.inputs[1])
glare=nt.nodes.new('CompositorNodeGlare');glare.glare_type='FOG_GLOW';glare.quality='MEDIUM';glare.threshold=1.6;glare.mix=-.95;lk.new(mix.outputs[0],glare.inputs[0])
fade=nt.nodes.new('CompositorNodeMixRGB');fade.blend_type='MULTIPLY';fade.inputs[0].default_value=1;fade.inputs[2].default_value=(1,1,1,1);lk.new(glare.outputs[0],fade.inputs[1]);out=nt.nodes.new('CompositorNodeComposite');lk.new(fade.outputs[0],out.inputs[0])
def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)
def lerp(a,b,u):return tuple(x+(y-x)*u for x,y in zip(a,b))
shots=[
 (0,8,(-48,-153,1.5),(-48,-104,83),(28,120,18),(24,49,11),48,52),
 (8,18,(-48,-104,83),(-28,-68,55),(24,49,11),(6,20,7),52,55),
 (18,28,(24,2,27),(23,18,27),(-2,26,2),(-2,42,2),45,45),
 (28,38,(0,26,34),(4,47,36),(35,63,3),(40,88,9),45,48),
 (38,48,(16,28,51),(29,34,57),(64,82,21),(64,82,22),48,52),
 (48,56,(-72,-128,110),(-155,-220,205),(20,90,8),(20,130,5),45,45)]
actors=[bpy.data.objects[n] for n in json.loads(scene['actor_names'])]
for actor in actors:
 head=next((o for o in actor.children if o.name.startswith('Resident sculpted head')),None)
 actor['safe_x_shift']=max(-2.7,min(2.7,head.location.x))-head.location.x if head and actor['base_y']<10 else 0
boat=bpy.data.objects['Animated canal boat']
water=bpy.data.materials['Canal water / rippled reflection'];noise=next(n for n in water.node_tree.nodes if n.type=='TEX_NOISE');noise.noise_dimensions='4D'
def at(t):
 si=next((i for i,s in enumerate(shots) if s[0]<=t<s[1]),5);a,b,p0,p1,q0,q1,l0,l1=shots[si];u=smooth((t-a)/(4 if si==5 else b-a))
 pos=lerp(p0,p1,u);target=lerp(q0,q1,u);cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=l0+(l1-l0)*u
 focus.outputs[0].default_value=1/(Vector(target)-cam.location).length
 # Blend in miniature depth gently as the horizon opens, retaining the reveal.
 blur.z_scale=22*smooth(t/6);blur.blur_max=22
 wt=math.floor(t*10)/10
 for actor in actors:
  if actor['walk']:
   d=wt*actor['speed'];actor.location.y=d;actor.location.x=actor['safe_x_shift'];actor.location.z=.018*math.sin(wt*8+actor['phase'])
 boat.location.y=-.58*wt;boat.location.z=.025*math.sin(t*1.3)
 noise.inputs['W'].default_value=t*.055
 f=smooth(t/.65)*(1-smooth((t-54.5)/1.5));fade.inputs[2].default_value=(f,f,f,1)
 scene.frame_set(round(t*24)+1)
 return {'time':t,'shot':si,'position':list(pos),'target':list(target),'lens':cam.data.lens,'focus':1/focus.outputs[0].default_value,'world_time':wt}

if mode=='proof':frames=[24,96,192,480,624,720,960,1248]
elif mode=='benchmark':
 scene.cycles.samples=24;frames=[192,624,720,1248]
elif mode=='eevee':frames=[192,720,1248]
elif mode=='preview':frames=list(range(0,193,3))+list(range(408,481,3))
elif mode=='range':frames=list(range(int(args[1]),int(args[2])))
else:frames=list(range(1344))
folder=OUT/('proof-v6' if mode=='proof' else 'benchmark-v6' if mode=='benchmark' else 'eevee-test-v6' if mode=='eevee' else 'preview-v6' if mode=='preview' else 'frames-v6');folder.mkdir(exist_ok=True)
evidence=[];start=time.time()
for f in frames:
 path=folder/(f'{f:05d}.png')
 if mode not in ['proof','preview'] and path.exists():continue
 state=at(f/24);temporary=folder/(f'{f:05d}.partial.png');scene.render.filepath=str(temporary);t0=time.time();bpy.ops.render.render(write_still=True);temporary.replace(path);state['seconds']=time.time()-t0;evidence.append(state)
 print('FRAME_READY',f,round(state['seconds'],2),'elapsed',round(time.time()-start,1),flush=True)
 (folder/'render-progress.json').write_text(json.dumps({'last_frame':f,'target_frames':len(frames),'elapsed':time.time()-start,'latest':state},indent=2),encoding='utf8')
(folder/('camera-evidence-'+str(frames[0])+'-'+str(frames[-1])+'.json')).write_text(json.dumps(evidence,indent=2),encoding='utf8')
if mode=='proof':bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'model/babylon-film-v6.blend'))
