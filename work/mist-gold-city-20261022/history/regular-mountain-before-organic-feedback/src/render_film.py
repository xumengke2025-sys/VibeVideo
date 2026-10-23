"""Frozen-world render entry: stills N... / range A B. Atomic frames, absolute time."""
import bpy,math,sys,os,json,time
import numpy as np
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));from timeline import *
from geometry import Mesh
from terrain import ground_z
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['stills','2064'];mode=args[0]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'model/fog-gold-city.blend'));scene=bpy.context.scene;cam=scene.camera
scene.render.engine=os.environ.get('FOG_ENGINE','CYCLES');scene.render.threads_mode='FIXED';scene.render.threads=6
scene.cycles.samples=int(os.environ.get('FOG_SAMPLES','32'));scene.cycles.adaptive_threshold=.05;scene.cycles.use_denoising=True;scene.cycles.denoiser='OPENIMAGEDENOISE';scene.cycles.denoising_use_gpu=True;scene.cycles.seed=221018;scene.cycles.use_animated_seed=False
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
scene.cycles.device='GPU';scene.cycles.max_bounces=5;scene.cycles.diffuse_bounces=2;scene.cycles.glossy_bounces=2;scene.cycles.transparent_max_bounces=4;scene.cycles.volume_bounces=0;scene.render.use_persistent_data=True
if scene.render.engine=='BLENDER_EEVEE_NEXT':scene.eevee.taa_render_samples=32;scene.eevee.use_raytracing=False
percent=int(os.environ.get('FOG_PERCENT','100'));scene.render.resolution_percentage=percent
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.compression=15;scene.render.filter_size=1.25
scene.render.compositor_device='GPU';scene.view_layers[0].use_pass_z=True;scene.view_layers[0].use_pass_mist=True;scene.world.mist_settings.start=250;scene.world.mist_settings.depth=1900;scene.world.mist_settings.falloff='LINEAR'
scene.use_nodes=True;nt=scene.node_tree;nt.nodes.clear();lk=nt.links;rl=nt.nodes.new('CompositorNodeRLayers')
def mn(op,a=None,b=None):
 n=nt.nodes.new('CompositorNodeMath');n.operation=op
 for i,v in enumerate([a,b]):
  if v is None:continue
  if isinstance(v,(float,int)):n.inputs[i].default_value=v
  else:lk.new(v,n.inputs[i])
 return n.outputs[0]
depth=mn('MAXIMUM',rl.outputs['Depth'],.1);focus=nt.nodes.new('CompositorNodeValue');strength=nt.nodes.new('CompositorNodeValue');physical=mn('MULTIPLY',mn('ABSOLUTE',mn('SUBTRACT',focus.outputs[0],mn('DIVIDE',1,depth))),34)
# Low resolution analytical CoC texture is interpolated; output blur radii scale with pixels.
W,H=round(1080*percent/100),round(1920*percent/100);grid_y,grid_x=np.mgrid[0:H,0:W];bandimg=bpy.data.images.new('Animated tilted focus band',W,H,float_buffer=True);bandimg.colorspace_settings.name='Non-Color';bn=nt.nodes.new('CompositorNodeImage');bn.image=bandimg
coc=mn('MULTIPLY',mn('MINIMUM',mn('ADD',mn('MULTIPLY',physical,.42),mn('MULTIPLY',bn.outputs[0],.58)),1),strength.outputs[0]);previous=rl.outputs['Image'];lower=0
for r in [2,5,11,22,38]:
 upper=r/38;blur=nt.nodes.new('CompositorNodeBlur');blur.filter_type='FAST_GAUSS';blur.size_x=round(r*percent/100);blur.size_y=round(r*percent/100);lk.new(rl.outputs['Image'],blur.inputs['Image']);weight=mn('MINIMUM',mn('MAXIMUM',mn('DIVIDE',mn('SUBTRACT',coc,lower),upper-lower),0),1);weight=mn('MULTIPLY',mn('MULTIPLY',weight,weight),mn('SUBTRACT',3,mn('MULTIPLY',weight,2)));mix=nt.nodes.new('CompositorNodeMixRGB');lk.new(weight,mix.inputs[0]);lk.new(previous,mix.inputs[1]);lk.new(blur.outputs[0],mix.inputs[2]);previous=mix.outputs[0];lower=upper
mist=nt.nodes.new('CompositorNodeMixRGB');mist.inputs[2].default_value=(.39,.48,.52,1);lk.new(mn('MULTIPLY',rl.outputs['Mist'],.48),mist.inputs[0]);lk.new(previous,mist.inputs[1]);output=nt.nodes.new('CompositorNodeComposite');lk.new(mist.outputs[0],output.inputs[0])
traffic=json.loads(scene['traffic']);cars=json.loads(scene['carriages']);boats=json.loads(scene['boats']);steam=json.loads(scene['steam']);O=bpy.data.objects
flag=O['Deep blue small flag'];flagbase=np.array([v.co[:] for v in flag.data.vertices]);crew=O['Navy flag bell barge crew']
def pose(ob,phase,wave=0):
 if not ob.data.shape_keys:return
 keys=ob.data.shape_keys.key_blocks;count=6;p=phase/math.tau%1*count;i=int(p);f=p-i
 for k in range(1,count):keys[k].value=(1-wave)*((1-f if k==i else 0)+(f if k==(i+1)%count else 0))
 if 'Wave' in keys:
  sway=.5+.5*math.sin(phase*3);keys['Wave'].value=wave*sway;keys['Wave alternate'].value=wave*(1-sway)
def animate_car(root,distance,speed):
 for child in root.children:
  if ' wheel' in child.name:child.rotation_euler.x=-distance/.69
  if child.name.startswith('Horse body'):
   child.location.z=0
   if root.name=='Burgundy Royal Mail coach':child.location.z=road_z(root.location.x+child.location.y)-road_z(root.location.x)-math.tan(root.rotation_euler.x)*child.location.y
   for leg in child.children:
    if leg.name.startswith('Horse leg '):
     phase=distance*math.tau/1.5+(.0 if leg['side']*leg['fore']==1 else math.pi)
     if root.name=='Burgundy Royal Mail coach':
      # Two-link leg geometry, planted stance and lifted recovery; no topology swapping.
      u=(phase/math.tau)%1
      if u<.62:fy=.465-.93*u/.62;lift=0
      else:v=(u-.62)/.38;fy=-.465+.93*smooth(v);lift=.18*math.sin(math.pi*v)
      fy*=min(1,speed/.4);lift*=min(1,speed/.4)
      foot=Vector((0,fy,-1.25+lift));d=foot.length;mid=foot*.5;normal=Vector((0,-foot.z,foot.y)).normalized();knee=mid+normal*math.sqrt(max(0,.68**2-(d*.5)**2));mat=O[child.children[0].name].data.materials[0] if child.children[0].type=='MESH' else bpy.data.materials['wood'];mm=Mesh();mm.rod((0,0,0),knee,.10,mat,.063,10);mm.rod(knee,foot,.063,mat,.045,10);mm.box((0,fy+.06,-1.28+lift),(.16,.23,.13),bpy.data.materials['dark']);mesh=next(c.data for c in leg.children if c.type=='MESH');mesh.vertices.foreach_set('co',[x for p in mm.v for x in p]);mesh.update()
     else:leg.rotation_euler.x=.39*math.sin(phase)*min(speed,1)
def at(t):
 scene.frame_set(round(t*24)+1);pos,target,lens=sample_camera(t);cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
 focus.outputs[0].default_value=1/(Vector(target)-cam.location).length;strength.outputs[0].default_value=.65*smooth((t-2)/6)
 bridgefocus=smooth((t-35)/6)*(1-smooth((t-68)/7));half=.17+.10*bridgefocus;tilt=.10-.23*bridgefocus;center=.49+.025*math.sin(t*.05)
 band=np.clip(np.maximum(0,np.abs(grid_y/(H-1)+tilt*(grid_x/(W-1)-.5)-center)-half)/.27,0,1)**1.5;pixels=np.ones((H,W,4),np.float32);pixels[:,:,:3]=band[:,:,None];bandimg.pixels.foreach_set(pixels.ravel());bandimg.update()
 for side in [-1,1]:
  angle=bridge_angle(t);O['Bridge pivot '+str(side)].rotation_euler.y=side*angle
  for yy in [-3.7,3.7]:
   # Cable length is conserved between deck attachment, fixed pulley and weight.
   a=Vector((side*9.25-side*5*math.cos(angle),18+yy*.8,3.1+5*math.sin(angle)));b=Vector((side*11.3,18+yy,12.6));base=Vector((side*4.25,18+yy*.8,3.1));L0=(base-b).length+math.sqrt(1.7**2+1.6**2);remain=L0-(a-b).length;z=b.z-math.sqrt(max(0,remain**2-1.7**2));c=Vector((side*13,18+yy,z));pts=O['Lift chain %s %s'%(side,yy)].data.splines[0].points
   for point,v in zip(pts,[a,b,c]):point.co=(*v,1)
   O['Counterweight %s %s'%(side,yy)].location.z=z-.8
  gate=O['Gate arm '+str(side)];gate.rotation_euler.x=(1-smooth((t-41)/2)+smooth((t-64)/1.2))*math.pi/2
 barge=O['Navy flag bell barge'];barge.location=(0,boat_y(t),.025*math.sin(t*1.3));barge.rotation_euler.y=.003*math.sin(t*1.1)
 wave=smooth((t-51)/1.1)*(1-smooth((t-58)/1.2));pose(crew,t*1.3,wave);pose(O['Bridge traffic foreman'],t*.9,smooth((t-40.5)/.8)*(1-smooth((t-43.5)/1)))
 coords=flagbase.copy();coords[:,1]+=.12*np.sin(coords[:,0]*5-t*3.1)*(coords[:,0]-1.5);flag.data.vertices.foreach_set('co',coords.ravel())
 coach=O['Burgundy Royal Mail coach'];cx=coach_x(t);coach.location=(cx,18,road_z(cx));coach.rotation_euler.x=math.atan2(road_z(cx+1.2)-road_z(cx-1.2),2.4);animate_car(coach,cx+140,coach_speed(t))
 for data in traffic:
  ob=O[data['name']];p=list(data['base']);phase=data['phase'];distance=t*data['speed']
  if data.get('watcher'):
   distance=max(0,t-65.7)*data['speed'];p[0 if data['crossing'] else 1]+=distance;p[2]=road_z(p[0]) if data['crossing'] else 2.27;ob.rotation_euler.z=-math.pi/2 if data['crossing'] or t<65.7 else 0
  else:
   pause=data['pause'];distance-=data['speed']*max(0,min(data['duration'],t-pause));axis=0 if data['axis']=='x' else 1;p[axis]+=data['direction']*distance
   # Pedestrians travelling cross streets stay on their bank unless on a bridge.
   reflected=False
   if axis==0 and not data.get('stone_bridge'):
    if data['base'][0]<0 and p[0]>-20:p[0]=-40-p[0];reflected=True
    elif data['base'][0]>0 and p[0]<20:p[0]=40-p[0];reflected=True
   if data.get('stone_bridge'):
    ax=abs(p[0]);p[2]=2.85+4.5*math.sqrt(max(0,1-(p[0]/9.2)**2)) if ax<9.25 else 2.2+.9*max(0,1-(ax-9)/8)
   ob.rotation_euler.z=(-math.pi/2 if data['direction']>0 else math.pi/2) if axis==0 else (0 if data['direction']>0 else math.pi)
   if reflected:ob.rotation_euler.z+=math.pi
  if not data.get('stone_bridge') and not data.get('watcher'):p[2]=ground_z(p[0],p[1])+.07
  ob.location=p
  if data['close']:pose(ob,phase+distance*math.tau/.72)
 for i in range(12):pose(O['Hidden shared distant actor '+str(i)],t*(4.2+i*.1)+i*.63)
 for d in cars:
  ob=O[d['name']];distance=d['speed']*t*d['direction'];xx=d['x']+d['direction']*1.5;yy=d['y']+distance;ob.location=(xx,yy,ground_z(xx,yy));ob.rotation_euler.z=0 if d['direction']>0 else math.pi;ob.rotation_euler.x=math.atan2(ground_z(xx,yy+1)-ground_z(xx,yy-1),2)*d['direction'];animate_car(ob,distance,d['speed'])
 for d in boats:
  ob=O[d['name']];ob.location=(d['x'],d['y']+(0 if d['moored'] else .28*t),.025*math.sin(t*1.2+d['phase']));ob.rotation_euler.y=.006*math.sin(t*.8+d['phase'])
 O['Waterwheel hub'].rotation_euler.x=t*.46
 for d in steam:
  age=(t*.13+d['phase'])%1;ob=O[d['name']];x,y,z=d['origin'];ob.location=(x+age*6,y+age*1.7,z+age*7);s=.18+age*1.5;ob.scale=(s*1.25,s*.85,s);ob.hide_render=age>.94
 bpy.context.view_layer.update()
 return {'t':t,'camera':pos,'target':target,'lens':lens,'bridge_degrees':math.degrees(bridge_angle(t)),'boat_y':boat_y(t),'coach_x':cx,'coach_speed':coach_speed(t),'focus_distance':1/focus.outputs[0].default_value}
frames=list(range(int(args[1]),int(args[2]))) if mode=='range' else [int(a) for a in args[1:]]
folder=ROOT/os.environ.get('FOG_OUTPUT','concept');folder.mkdir(parents=True,exist_ok=True);states=[]
for f in frames:
 path=folder/f'{f:05d}.png'
 if path.exists() and os.environ.get('FOG_OVERWRITE')!='1':continue
 state=at(f/24);temp=folder/f'{f:05d}.partial.png';scene.render.filepath=str(temp);start=time.time();bpy.ops.render.render(write_still=True);temp.replace(path);state['render_seconds']=time.time()-start;states.append(state);print('FRAME_READY',f,round(state['render_seconds'],2),flush=True);(folder/'progress.json').write_text(json.dumps(state,indent=2),encoding='utf8')
(folder/('states-%s-%s.json'%(frames[0],frames[-1]))).write_text(json.dumps(states,indent=2),encoding='utf8')
if os.environ.get('FOG_SAVE_FILM')=='1':bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'model/fog-gold-film.blend'))
