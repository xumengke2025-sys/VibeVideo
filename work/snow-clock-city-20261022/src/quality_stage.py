"""Actual Blender quality study after rejection of the primitive city.
Run: blender --background --python src/quality_stage.py
"""
import bpy,sys,math,random,json,time,os
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.noise import noise_vector
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
import craft as C
import actors
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for datablocks in [bpy.data.materials,bpy.data.meshes,bpy.data.curves]:
    for data in list(datablocks):
        if data.users==0:datablocks.remove(data)
C.palette();rng=random.Random(811)
hero=C.chalet('Bakery | reconstructed hero architecture',(-2.7,1.6,.12))
station=C.station('Uphill cable loading station',(3.65,-1.25,.10))
station.rotation_euler.z=-.08

def ground(x,y):
    n=noise_vector(Vector((x*.25,y*.25,1))).x
    return .05+.045*n+.015*math.sin(x*2+y)

# Ground continues beyond the frame. No floating display plinth.
C.drift('Snow-covered continuous hillside',(-40,40),(-40,40),lambda x,y:ground(x,y)+.07,None,.40)
road=C.Mesh();gravel=C.Mesh()
roadmats=[C.material('Wet granite sett '+str(i),(.205+i*.009,.22+i*.009,.23+i*.009),.52,texture='rock_boulder_dry',tint=(.55+i*.035,.60+i*.035,.64+i*.035)) for i in range(7)]
for row in range(29):
    y=-7.9+row*.27
    for col in range(95):
        x=-16+col*.34+(row%2)*.17
        # A clearing broadens at the loading station and meets the front door.
        if y>-.8 and not (-6.5<x<6.1):continue
        if y>-.4:continue
        road.box((x,y,.16+rng.uniform(-.006,.006)),(.323+rng.uniform(-.012,.012),.255,.15),rng.choice(roadmats),jitter=.014,seed=row*100+col)
road.box((0,-4.2,.10),(32,7.7,.10),C.MO)
road.obj('Individually laid irregular wet setts',None,.021)
# Accumulations feather into the cleared edge; no solid white tube border.
for sign in [-1,1]:
    lo,hi=(-8.8,-7.7) if sign<0 else (-.55,.45)
    C.drift('Shovelled edge '+str(sign),(-16,16),(lo,hi),lambda x,y,lo=lo,hi=hi:.13+.25*math.sin(math.pi*(y-lo)/(hi-lo))**2*(.75+.2*math.sin(x*1.4)+.12*math.sin(x*3.1)),None,.12)
# Clear wooden station approach and low stone edging.
edge=C.Mesh()
for i in range(34):
    x=-12+i*.67
    edge.box((x,.25,.23),(.64,.43,.37),C.ST,jitter=.028,seed=i)
edge.obj('Street gutter stones',None,.024)

# A retaining terrace behind the bakery, with a stair, never on the carriage road.
wall=C.Mesh();wall.box((0,6.9,1.4),(28,.80,2.8),C.ST)
for i in range(45):wall.box((-14+i*.64,6.65,2.84),(.61,1.02,.17),C.ST,jitter=.02,seed=i)
wall.obj('Rear terrace masonry',None,.025)
C.drift('Terrace snow',(-22,22),(6.3,24),lambda x,y:3.09+.05*noise_vector(Vector((x*.5,y*.5,0))).x,None,.3)
stairs=C.Mesh()
for i in range(18):stairs.box((-8.5,2.6+i*.23,i*.155/2), (2,.25,i*.155),C.ST,jitter=.008,seed=i)
stairs.obj('Pedestrian stone stairs to upper lane',None,.02)

# A smaller rear wing makes the silhouette an ensemble, not cloned cubes.
wing=C.chalet('Neighbouring clockmaker',(-8.4,9.3,2.95),seed=135,variant='workshop')
wing.scale=(.65,.69,.72);wing.rotation_euler.z=.12

def fir(name,p,h,seed):
    ra=random.Random(seed);r=C.root(name,p);trunk=C.Mesh();branch=C.Mesh();snow=C.Mesh()
    trunk.rod((0,0,0),(0,0,h),.12,C.DK,18,.025)
    for layer in range(14):
        z=.7+layer*(h-.9)/14;radius=(1-z/h)*h*.26
        for j in range(7):
            a=j*math.tau/7+layer*.73;length=radius*ra.uniform(.75,1.15)
            end=Vector((math.cos(a)*length,math.sin(a)*length,z-.12));start=Vector((0,0,z))
            branch.rod(start,end,.025,C.DK,8,.007)
            for k in range(7):
                u=.15+k*.12;center=start.lerp(end,u);span=length*(1-u)*.25
                for side in [-1,1]:
                    aa=a+side*.65;tip=center+Vector((math.cos(aa)*span,math.sin(aa)*span,.07))
                    branch.rod(center,tip,.011,C.DK,6,.003)
                    # Needle fans stay small and irregular; no cone tiers.
                    for q in range(6):
                        t=q/6;pos=center.lerp(tip,t)
                        for s in [-1,1]:
                            an=aa+s*.95
                            branch.rod(pos,pos+Vector((math.cos(an)*.10,math.sin(an)*.10,.03)),.013,C.GR,5,.002)
                if k%2==0 and j%2==0:snow.ellipsoid(center+Vector((0,0,.045)),(.13,.09,.035),C.SN,12,6)
    trunk.obj(name+' trunk',r,.005);branch.obj(name+' branches and needles',r,0);snow.obj(name+' settled dusting',r,0)
treepath=R/'assets/models/fir_sapling_medium/fir_sapling_medium_1k.gltf'
if treepath.exists() and (treepath.parent/'fir_sapling_medium.bin').exists():
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(treepath));imported=set(bpy.data.objects)-before
    tr=C.root('CC0 fir | Poly Haven',(-9.7,4.7,.1))
    for o in imported:
        if not o.parent:o.parent=tr
    bpy.context.view_layer.update()
    coords=[o.matrix_world@Vector(v) for o in imported if o.type=='MESH' for v in o.bound_box]
    height=max(v.z for v in coords)-min(v.z for v in coords);sc=7.8/max(height,.01);tr.scale=(sc,sc,sc)
else:
    fir('Old fir at upper stair',(-10.5,5.2,.12),8.1,83)

# Small joinery and props at credible human scale.
props=C.Mesh()
for j in range(11):props.box((-.65+j*.165,-4.0,.82),(.154,.72,.055),C.WO,wood=True,seed=j)
for x in [-.45,.80]:
    for y in [-4.25,-3.75]:props.box((x,y,.46),(.075,.075,.72),C.DK,wood=True)
props.box((.18,-4.0,.87),(1.45,.60,.05),C.CL)
for j in range(6):
    x=-.40+j*.23
    props.ellipsoid((x,-4.0,.97),(.13,.19,.09),C.BD,24,10)
    for k in [-1,0,1]:C.curve('Scored bread crust',[(x-.06,-4.09+k*.08,1.035),(x,-4.05+k*.08,1.06),(x+.05,-4.02+k*.08,1.03)],.006,C.CL)
props.obj('Bakery trestle and bread',None,.008)
baker=actors.human('Baker in linen apron',(.7,-3.45,.22),True);baker.rotation_euler.z=-.5
porter=actors.human('Freight station porter',(5.15,-2.20,.55));porter.rotation_euler.z=1.2
horse=actors.horse('Chestnut carriage horse',(-3.0,-6.3,.22),math.pi/2)
C.lantern((-5.75,-1.62,2.38))
C.lantern((.35,-1.62,2.38))
# Wall-mounted forged brackets.
for x in [-5.75,.35]:C.curve('Lantern scroll bracket',[(x,-1.25,2.85),(x,-1.50,2.85),(x,-1.73,2.77),(x,-1.73,2.68)],.019,C.IR)

# Carrying cable extends through the composition toward the eventual town.
for shift in [0,.09]:
    pts=[]
    for i in range(100):
        u=i/99;pts.append((3.65+shift+u*7,-1.25-u*27,4.15-u*.5-1.2*4*u*(1-u)))
    C.curve('Suspended freight cable '+str(shift),pts,.017,C.IR)

# Lighting: winter blue fill, warm oblique dawn with large soft shadows.
world=bpy.data.worlds.new('Cold clear winter morning');world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.36,.48,.68,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.40;bpy.context.scene.world=world
def light(name,typ,loc,energy,color,target,size=1):
    ld=bpy.data.lights.new(name,typ);ld.energy=energy;ld.color=color
    if typ=='AREA':ld.shape='DISK';ld.size=size
    elif typ=='SUN':ld.angle=.12
    ob=bpy.data.objects.new(name,ld);bpy.context.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();return ob
light('Morning sun','SUN',(-15,-10,13),2.5,(1,.78,.53),(0,0,0))
light('Soft sky reflection','AREA',(0,-6,18),1100,(.62,.76,1),(0,0,0),18)
light('Bakery reflected warmth','AREA',(-2.7,-2.0,2.1),38,(1,.52,.19),(-2.7,-7,0),3)

scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=int(os.environ.get('CRAFT_SAMPLES','96'))
scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.02;scene.cycles.max_bounces=7
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
scene.cycles.device='GPU';scene.cycles.seed=811;scene.cycles.use_animated_seed=False
scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.render.resolution_percentage=int(os.environ.get('CRAFT_SCALE','100'))
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.fps=24
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.65
scene.render.threads_mode='FIXED';scene.render.threads=4
camdata=bpy.data.cameras.new('Portrait model quality camera');cam=bpy.data.objects.new('Portrait model quality camera',camdata);bpy.context.collection.objects.link(cam);scene.camera=cam
def camera(loc,target,lens):
    cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();camdata.lens=lens
    camdata.dof.use_dof=True;camdata.dof.focus_distance=(Vector(target)-cam.location).length;camdata.dof.aperture_fstop=11
camera((18,-29,21),(-1.2,1.3,3.1),60)
scene.use_nodes=True;n=scene.node_tree.nodes;n.clear();l=scene.node_tree.links
rl=n.new('CompositorNodeRLayers');gl=n.new('CompositorNodeGlare');gl.glare_type='FOG_GLOW';gl.quality='HIGH';gl.threshold=3;gl.mix=-.96
l.new(rl.outputs['Image'],gl.inputs['Image']);out=n.new('CompositorNodeComposite');l.new(gl.outputs['Image'],out.inputs[0])
folder=R/'render/quality-rebuild-v3';folder.mkdir(parents=True,exist_ok=True)
# Bundle maps and make a separate, fully editable model before rendering.
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(R/'model/bakery-quality-v3.blend'))
scene.render.filepath=str(folder/'bakery-station-portrait.png');t=time.time();bpy.ops.render.render(write_still=True)
(folder/'render-info.json').write_text(json.dumps({'size':[1080,1920],'samples':scene.cycles.samples,'seconds':time.time()-t,'source':'src/quality_stage.py','model':'model/bakery-quality-v1.blend','status':'actual 3D work in progress; not complete film'},indent=2),encoding='utf8')
camera((9.5,-16,10.5),(-2.2,-.5,3.6),62)
scene.render.filepath=str(folder/'joinery-detail.png');bpy.ops.render.render(write_still=True)
print('QUALITY_STAGE_READY',flush=True)
