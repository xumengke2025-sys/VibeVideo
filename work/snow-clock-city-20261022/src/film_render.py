import bpy,math,os,sys,json,time
import numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['stills','2064']
bpy.ops.wm.open_mainfile(filepath=os.environ.get('SNOW_MODEL',str(R/'model/clock-city-production-v5.blend')))
if not json.loads(bpy.context.scene.get('carriage_data','{}')):
 import film_world
 film_world.build()
S=bpy.context.scene;S.render.engine='CYCLES';S.cycles.samples=int(os.environ.get('SNOW_SAMPLES','32'));S.cycles.adaptive_threshold=.04;S.cycles.use_denoising=True;S.cycles.denoiser='OPENIMAGEDENOISE';S.cycles.denoising_use_gpu=False
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
S.cycles.device='GPU';S.cycles.seed=221022;S.cycles.use_animated_seed=False;S.cycles.max_bounces=5;S.cycles.diffuse_bounces=3;S.cycles.glossy_bounces=3;S.cycles.volume_bounces=1;S.render.use_persistent_data=True
S.render.threads_mode='FIXED';S.render.threads=4;S.render.compositor_device='CPU';S.render.resolution_percentage=int(os.environ.get('SNOW_SCALE','100'))
if os.environ.get('SNOW_ENGINE')=='EEVEE':
 S.render.engine='BLENDER_EEVEE_NEXT';S.eevee.taa_render_samples=64;S.eevee.use_raytracing=True;S.eevee.shadow_ray_count=2;S.eevee.shadow_step_count=8
S.render.image_settings.file_format='PNG';S.render.image_settings.color_mode='RGB';S.render.image_settings.color_depth='8';S.render.image_settings.compression=12
S.view_layers[0].use_pass_z=True;S.view_layers[0].use_pass_mist=True;S.world.mist_settings.start=75;S.world.mist_settings.depth=350
S.use_nodes=True;nt=S.node_tree;nt.nodes.clear();lk=nt.links;rl=nt.nodes.new('CompositorNodeRLayers')
def mn(op,a=None,b=None):
 n=nt.nodes.new('CompositorNodeMath');n.operation=op
 for i,val in enumerate([a,b]):
  if val is None:continue
  if isinstance(val,(float,int)):n.inputs[i].default_value=val
  else:lk.new(val,n.inputs[i])
 return n.outputs[0]
focus=nt.nodes.new('CompositorNodeValue');focus.name='Focus reciprocal';physical=mn('MULTIPLY',mn('ABSOLUTE',mn('SUBTRACT',focus.outputs[0],mn('DIVIDE',1,mn('MAXIMUM',rl.outputs['Depth'],.1)))),22)
W=round(S.render.resolution_x*S.render.resolution_percentage/100);H=round(S.render.resolution_y*S.render.resolution_percentage/100);yy,xx=np.mgrid[0:H,0:W]
for name,half in [('Narrow focus band',.13),('Wide focus band',.27)]:
 band=np.clip(np.maximum(0,np.abs(yy/(H-1)+.06*(xx/(W-1)-.5)-.5)-half)/.26,0,1)**1.6
 pixels=np.ones((H,W,4),np.float32);pixels[:,:,:3]=band[:,:,None];im=bpy.data.images.new(name,W,H,float_buffer=True);im.colorspace_settings.name='Non-Color';im.pixels.foreach_set(pixels.ravel());im.pack()
bn=nt.nodes.new('CompositorNodeImage');bn.name='Focus band image';bn.image=bpy.data.images['Narrow focus band'];strength=nt.nodes.new('CompositorNodeValue');strength.name='Tilt strength';strength.outputs[0].default_value=.7
coc=mn('MULTIPLY',mn('MINIMUM',mn('ADD',mn('MULTIPLY',physical,.3),mn('MULTIPLY',bn.outputs[0],.7)),1),strength.outputs[0]);previous=rl.outputs['Image'];lower=0
scale=S.render.resolution_percentage/100
for rad in [2,5,11,22,32]:
 upper=rad/32;blur=nt.nodes.new('CompositorNodeBlur');blur.filter_type='FAST_GAUSS';blur.size_x=max(1,round(rad*scale));blur.size_y=max(1,round(rad*scale));lk.new(rl.outputs['Image'],blur.inputs['Image'])
 w=mn('MINIMUM',mn('MAXIMUM',mn('DIVIDE',mn('SUBTRACT',coc,lower),upper-lower),0),1);w=mn('MULTIPLY',mn('MULTIPLY',w,w),mn('SUBTRACT',3,mn('MULTIPLY',w,2)))
 mix=nt.nodes.new('CompositorNodeMixRGB');lk.new(w,mix.inputs[0]);lk.new(previous,mix.inputs[1]);lk.new(blur.outputs[0],mix.inputs[2]);previous=mix.outputs[0];lower=upper
mix=nt.nodes.new('CompositorNodeMixRGB');lk.new(mn('MULTIPLY',rl.outputs['Mist'],.65),mix.inputs[0]);lk.new(previous,mix.inputs[1]);mix.inputs[2].default_value=(.50,.60,.70,1)
out=nt.nodes.new('CompositorNodeComposite');lk.new(mix.outputs[0],out.inputs[0])
import film_animation as animate
folder=R/os.environ.get('SNOW_OUTPUT','render/film-proof-v1');folder.mkdir(parents=True,exist_ok=True)
frames=list(range(int(args[1]),int(args[2]))) if args[0]=='range' else [int(f) for f in args[1:]]
if S.render.engine=='BLENDER_EEVEE_NEXT':
 # One animation render keeps the render engine alive between adjacent frames.
 # Repeated still renders recreated all GPU resources and crashed the driver.
 missing=[f for f in frames if not (folder/f'{f:05d}.png').exists()]
 runs=[]
 for f in missing:
  if runs and runs[-1][-1]+1==f:runs[-1].append(f)
  else:runs.append([f])
 state={};last=[time.time()]
 def prepare(scene,*_):
  state.clear();state.update(animate.at((scene.frame_current-1)/24))
 def written(scene,*_):
  f=scene.frame_current-1;src=Path(scene.render.frame_path(frame=scene.frame_current))
  src.replace(folder/f'{f:05d}.png')
  state['render_seconds']=round(time.time()-last[0],2);last[0]=time.time()
  (folder/'progress.json').write_text(json.dumps(state,indent=2),encoding='utf8');print('FRAME_READY',f,state['render_seconds'],flush=True)
 bpy.app.handlers.frame_change_post.append(prepare);bpy.app.handlers.render_write.append(written)
 try:
  for run in runs:
   S.frame_start=run[0]+1;S.frame_end=run[-1]+1;S.frame_step=1;S.render.filepath=str(folder/'anim-partial-')
   last[0]=time.time();S.frame_set(S.frame_start);bpy.ops.render.render(animation=True)
 finally:
  bpy.app.handlers.frame_change_post.remove(prepare);bpy.app.handlers.render_write.remove(written)
else:
 for f in frames:
  path=folder/f'{f:05d}.png'
  if path.exists():continue
  S.frame_set(f+1);state=animate.at(f/24);S.render.filepath=str(folder/f'{f:05d}.partial.png');t0=time.time();bpy.ops.render.render(write_still=True);Path(S.render.filepath).replace(path)
  state['render_seconds']=round(time.time()-t0,2);(folder/'progress.json').write_text(json.dumps(state,indent=2),encoding='utf8');print('FRAME_READY',f,state['render_seconds'],flush=True)
if args[0]=='concept':bpy.ops.wm.save_as_mainfile(filepath=str(R/'model/clock-city-film-preview.blend'))
