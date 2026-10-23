from pathlib import Path
import json
P=Path(__file__).resolve().parent
s=(P/'render_city_v13.py').read_text(encoding='utf8')
s=s.replace('v13','v14')
s=s.replace('Defocus replaces its WebGL spiral gather; this is not the identical shader.','Multi-level Gaussian replaces its WebGL gather; this is an approximation.')
s=s.replace("ROOT=Path(__file__).resolve().parent;OUT=ROOT/'render';OUT.mkdir(exist_ok=True)","ROOT=Path(__file__).resolve().parent;OUT=ROOT/'render';OUT.mkdir(exist_ok=True)\nsys.path.insert(0,str(ROOT))\nimport v14_motion\nfrom bpy_extras.object_utils import world_to_camera_view")
s=s.replace('scene=bpy.context.scene;cam=scene.camera','scene=bpy.context.scene;cam=scene.camera\nv14data=v14_motion.setup(scene)')
s=s.replace("p=d['base'];ph=d['phase'];ob.location=(p[0]+.09*math.sin(wt*.19+ph),p[1]+.42*math.sin(wt*.23+ph)", "p=d['base'];ph=d['phase'];amp=.10 if d.get('grouped') else 1.0;ob.location=(p[0]+amp*.09*math.sin(wt*.19+ph),p[1]+amp*.42*math.sin(wt*.23+ph)")
start=s.index('W=1080;H=1920;');end=s.index('# Stable separable',start)
s=s[:start]+'''W=1080;H=1920;yy,xx=np.mgrid[0:H,0:W]
def coord_image(name,values):
 pixels=np.ones((H,W,4),np.float32);pixels[:,:,:3]=values[:,:,None]
 image=bpy.data.images.new(name,W,H,float_buffer=True);image.colorspace_settings.name='Non-Color';image.pixels.foreach_set(pixels.ravel());image.pack()
 ob=nt.nodes.new('CompositorNodeImage');ob.image=image;return ob.outputs['Image']
cx=coord_image('V14 screen x',xx/(W-1));cy=coord_image('V14 screen y',yy/(H-1))
def val(name,value):
 n=nt.nodes.new('CompositorNodeValue');n.name=name;n.outputs[0].default_value=value;return n
band_center=val('V14 tracked focus center',.49);band_half=val('V14 adaptive focus width',.09);band_tilt=val('V14 shot focus tilt',.07)
dx=mathnode('SUBTRACT',cx,.5);slant=mathnode('MULTIPLY',dx.outputs[0],band_tilt.outputs[0]);ytilt=mathnode('ADD',cy,slant.outputs[0]);offset=mathnode('SUBTRACT',ytilt.outputs[0],band_center.outputs[0]);mag=mathnode('ABSOLUTE',offset.outputs[0]);outside=mathnode('SUBTRACT',mag.outputs[0],band_half.outputs[0]);outside=mathnode('MAXIMUM',outside.outputs[0],0);outside=mathnode('DIVIDE',outside.outputs[0],.23);outside=mathnode('MINIMUM',outside.outputs[0],1);band=mathnode('POWER',outside.outputs[0],1.45)
pb=mathnode('MULTIPLY',physical.outputs[0],.30);bb=mathnode('MULTIPLY',band.outputs[0],.70);added=mathnode('ADD',pb.outputs[0],bb.outputs[0]);clamp=mathnode('MINIMUM',added.outputs[0],1)
''' +s[end:]
s=s.replace("desired_band=statue_band if si==5 else canal_band if si==3 else im\n\tif bn.image!=desired_band:bn.image=desired_band",'') if False else s
old=" desired_band=statue_band if si==5 else canal_band if si==3 else im\n if bn.image!=desired_band:bn.image=desired_band"
assert old in s;s=s.replace(old,'')
s=s.replace("u=smooth((t-a)/(b-a))","raw=(t-a)/(b-a);u=(.72*raw+.28*smooth(raw)) if si in [2,3,4,8] else smooth(raw)")
needle=" noise.inputs['W'].default_value=t*.09"
assert needle in s
s=s.replace(needle,''' detail=v14_motion.update(v14data,t)
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
 noise.inputs['W'].default_value=t*.09''')
s=s.replace("'world_time':wt}","'world_time':wt,'focus_band_center':center,'focus_band_half':half,'action':detail}")
# Small evaluation mode validates contacts and absolute-time seeking without rendering.
needle="if mode=='proof':frames="
at=s.index(needle)
s=s[:at]+'''if mode=='audit':
 report=[]
 for seconds in [53.5,55,56.3,57.2,58.2,59.5,60.4,61.2,61.8,31.5,73,57.2]:report.append(at(seconds))
 (ROOT/'qa/v14/action-state-audit.json').write_text(json.dumps(report,indent=2),encoding='utf8')
 print('V14_STATE_AUDIT',max(r['action']['offering_max_reach'] for r in report),flush=True)
 sys.exit(0)
''' +s[at:]
s=s.replace("def blend_pose(keys,phase):", "# Free unlinked stride source collections after baking their shape keys.\ndel v14poses,v14meshes,pose_coordinates,meshes\nprint('V14_ORPHANS_PURGED',bpy.data.orphans_purge(do_local_ids=True,do_linked_ids=False,do_recursive=True),flush=True)\nimport gc;gc.collect()\ndef blend_pose(keys,phase):")
(P/'render_city_v14.py').write_text(s,encoding='utf8')
t=json.loads((P/'v13-timeline.json').read_text(encoding='utf8'))
t['shots'][0][2]=[-43,-126,6.6]
t['shots'][0][4]=[14,67,9]
t['shots'][6][2]=[-38,123,26];t['shots'][6][3]=[-39,126,25]
t['shots'][6][4]=[-48.2,147.3,2.7];t['shots'][6][5]=[-48.0,147.45,2.6]
t['shots'][6][6]=48;t['shots'][6][7]=50
for ev in t['events']:ev['id']=ev['id'].replace('v12','v14')
t['events'][6]['reads']=['Two priests and a shared offering dish','Receiver takes dish, turns toward altar','Dish rests on altar before hands withdraw']
t['music']['note']='Existing excerpt/cut timing preserved; scene ambience revised. Actual listening not claimed.'
(P/'v14-timeline.json').write_text(json.dumps(t,ensure_ascii=False,indent=2),encoding='utf8')
a=(P/'assemble_city_v13.py').read_text(encoding='utf8').replace('v13','v14').replace('final-mix-v11.wav','final-mix-v14.wav')
(P/'assemble_city_v14.py').write_text(a,encoding='utf8')
print('V14_RENDERER_PREPARED')
