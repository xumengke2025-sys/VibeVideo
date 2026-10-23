"""Snow-clock valley: editable mountain terrain and instanced Alpine firs.

Public API: build_environment(seed=2217, tree_density=1, terrain_step=1.0).
The central rectangle [-32,32] x [-30,45] exactly follows ground(x,y).
All objects are parented to the returned root. No scene, camera, or palette is
cleared by the API. Running this module directly makes a separate scale study.
"""
import bpy, math, json, time, os, sys, hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector, Matrix

R=Path(__file__).resolve().parents[1]
SEED=2217

def smooth(v):
    v=max(0.0,min(1.0,float(v)))
    return v*v*(3-2*v)

def ground(x,y):
    return max(0,.12*(y+20))+2*smooth((y-12)/10)+.12*math.sin(x*.18)*math.sin(y*.12)

def _ss(x):
    a=np.clip(x,0,1)
    return a*a*(3-2*a)

def _noise(x,y,seed=0):
    """Deterministic smooth 2D value noise; independent of render ordering."""
    ix=np.floor(x);iy=np.floor(y);fx=_ss(x-ix);fy=_ss(y-iy)
    def h(a,b):
        v=np.sin(a*127.1+b*311.7+seed*57.13)*43758.5453123
        return 2*(v-np.floor(v))-1
    a=h(ix,iy)*(1-fx)+h(ix+1,iy)*fx
    b=h(ix,iy+1)*(1-fx)+h(ix+1,iy+1)*fx
    return a*(1-fy)+b*fy

def _fbm(x,y,seed=SEED,octaves=5):
    s=np.zeros_like(np.asarray(x,dtype=float));amp=1.0;norm=0
    for i in range(octaves):
        s+=amp*_noise(x,y,seed+i*13);norm+=amp
        x=x*2.03+13.2;y=y*2.03-7.1;amp*=.48
    return s/norm

def _ridge(x,y,points,width):
    """Irregular branching crest, heights interpolated along its segments."""
    out=np.zeros_like(x,dtype=float)
    for a,b in zip(points,points[1:]):
        ax,ay,az=a;bx,by,bz=b;dx=bx-ax;dy=by-ay
        t=np.clip(((x-ax)*dx+(y-ay)*dy)/(dx*dx+dy*dy),0,1)
        dist=np.sqrt((x-(ax+dx*t))**2+(y-(ay+dy*t))**2)
        out=np.maximum(out,(az*(1-t)+bz*t)*np.exp(-(dist/width)**1.23))
    return out

def landscape_height(x,y,seed=SEED):
    """Continuous valley + connected ribbed massifs, never isolated cones."""
    x=np.asarray(x,dtype=float);y=np.asarray(y,dtype=float)
    central=np.maximum(0,.12*(y+20))+2*_ss((y-12)/10)+.12*np.sin(x*.18)*np.sin(y*.12)
    # Warped drainage coordinates prevent straight symmetrical ridge lines.
    wx=x+5.2*_fbm(x*.025,y*.025,seed+12,3)
    wy=y+5.6*_fbm(x*.027+4,y*.027,seed+32,3)
    systems=[
      ([(-178,162,48),(-142,160,72),(-111,145,92),(-78,157,100),(-50,135,108),(-20,146,76),(7,157,114),(32,139,86),(64,152,99),(96,136,78),(132,161,88),(180,169,50)],53),
      ([(-150,218,58),(-116,222,99),(-69,209,93),(-33,235,109),(18,220,106),(69,226,110),(116,218,94),(165,235,78)],62),
      ([(-78,157,96),(-75,122,75),(-91,96,52),(-76,69,25),(-66,40,10)],36),
      ([(-50,135,103),(-34,109,62),(-48,84,35),(-42,64,13)],32),
      ([(7,157,110),(18,128,74),(36,103,43),(43,81,15)],35),
      ([(64,152,95),(78,113,66),(73,87,42),(80,55,26),(65,27,8)],38),
      ([(-111,145,89),(-127,111,63),(-116,70,35),(-110,22,19),(-81,-10,4)],39),
      ([(96,136,77),(120,108,57),(113,67,31),(122,21,12)],40),
    ]
    field=np.zeros_like(x)
    for points,width in systems:field=np.maximum(field,_ridge(wx,wy,points,width))
    # Folded strata and fine ravines, tapered to avoid spiky lowland terrain.
    detail=_fbm(wx*.075,wy*.075,seed+3,5)
    cross=_fbm(wx*.12+wy*.045,wy*.025,seed+8,4)
    ridge_noise=1-np.abs(_fbm(wx*.055,wy*.055,seed+20,5))
    field=field*(.96+.12*detail)+np.minimum(field/45,1)*(5.5*detail+3.5*cross+2.2*ridge_noise)
    # Lower snowbanks keep a protected continuous town surface and road space.
    border=np.maximum(np.maximum((np.abs(x)-32)/23,(y-45)/23),(-30-y)/25)
    blend=_ss(border)
    valley=central+1.7*_fbm(x*.04,y*.04,seed+51,4)
    field=np.maximum(field,valley)
    z=central*(1-blend)+field*blend
    return z

def _mesh(name,vertices,faces,parent,material):
    me=bpy.data.meshes.new(name);me.from_pydata(vertices,[],faces);me.update()
    ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);ob.parent=parent
    me.materials.append(material)
    for p in me.polygons:p.use_smooth=True
    return ob

def _terrain_material():
    m=bpy.data.materials.new('ENV | crystalline snow and exposed layered granite');m.use_nodes=True
    n=m.node_tree.nodes;l=m.node_tree.links;n.clear()
    out=n.new('ShaderNodeOutputMaterial');p=n.new('ShaderNodeBsdfPrincipled');l.new(p.outputs[0],out.inputs[0])
    p.inputs['Roughness'].default_value=.84;p.inputs['Subsurface Weight'].default_value=.025
    geo=n.new('ShaderNodeNewGeometry');tex=n.new('ShaderNodeTexCoord')
    sep=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Normal'],sep.inputs[0])
    at=n.new('ShaderNodeAttribute');at.attribute_name='snow_cover'
    noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=2.3;noise.inputs['Detail'].default_value=5;noise.inputs['Roughness'].default_value=.7
    l.new(tex.outputs['Object'],noise.inputs[0])
    rock=n.new('ShaderNodeTexImage');rock.image=bpy.data.images.load(str(R/'assets/pbr/rock_boulder_dry/rock_boulder_dry_diff_2k.jpg'),check_existing=True);rock.projection='BOX';rock.projection_blend=.35
    mapping=n.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=.22;l.new(tex.outputs['Object'],mapping.inputs[0]);l.new(mapping.outputs[0],rock.inputs[0])
    rocktint=n.new('ShaderNodeMixRGB');rocktint.blend_type='MULTIPLY';rocktint.inputs[0].default_value=.8;rocktint.inputs[2].default_value=(.50,.59,.66,1);l.new(rock.outputs[0],rocktint.inputs[1])
    # Discontinuous sediment bands are only exposed on bare cliff faces.
    pos=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Position'],pos.inputs[0])
    strataheight=n.new('ShaderNodeMath');strataheight.operation='MULTIPLY';strataheight.inputs[1].default_value=1.3;l.new(pos.outputs['Z'],strataheight.inputs[0])
    stratanoise=n.new('ShaderNodeMath');stratanoise.operation='MULTIPLY_ADD';stratanoise.inputs[1].default_value=3.1;l.new(noise.outputs['Fac'],stratanoise.inputs[0]);l.new(strataheight.outputs[0],stratanoise.inputs[2])
    stratawave=n.new('ShaderNodeMath');stratawave.operation='SINE';l.new(stratanoise.outputs[0],stratawave.inputs[0])
    strataamount=n.new('ShaderNodeMath');strataamount.operation='MULTIPLY_ADD';strataamount.inputs[1].default_value=.055;strataamount.inputs[2].default_value=.055;l.new(stratawave.outputs[0],strataamount.inputs[0])
    strata=n.new('ShaderNodeMixRGB');strata.blend_type='MULTIPLY';strata.inputs[2].default_value=(.36,.39,.42,1);l.new(strataamount.outputs[0],strata.inputs[0]);l.new(rocktint.outputs[0],strata.inputs[1])
    # Vertex cover is slope/wind/elevation based. Noise only breaks soft edges.
    mult=n.new('ShaderNodeMath');mult.operation='MULTIPLY_ADD';mult.inputs[1].default_value=.20;mult.inputs[2].default_value=-.10;l.new(noise.outputs['Fac'],mult.inputs[0])
    add=n.new('ShaderNodeMath');add.operation='ADD';l.new(at.outputs['Fac'],add.inputs[0]);l.new(mult.outputs[0],add.inputs[1])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.32;ramp.color_ramp.elements[1].position=.62;l.new(add.outputs[0],ramp.inputs[0])
    mix=n.new('ShaderNodeMixRGB');l.new(ramp.outputs[0],mix.inputs[0]);l.new(strata.outputs[0],mix.inputs[1]);mix.inputs[2].default_value=(.79,.835,.875,1)
    air=n.new('ShaderNodeAttribute');air.attribute_name='air_depth'
    haze=n.new('ShaderNodeMixRGB');l.new(air.outputs['Fac'],haze.inputs[0]);l.new(mix.outputs[0],haze.inputs[1]);haze.inputs[2].default_value=(.39,.50,.65,1);l.new(haze.outputs[0],p.inputs['Base Color'])
    bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.17;bump.inputs['Distance'].default_value=.055;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
    return m

def _make_terrain(parent,step=1.0,seed=SEED):
    xs=np.linspace(-210,210,round(420/step)+1);ys=np.linspace(-100,270,round(370/step)+1)
    X,Y=np.meshgrid(xs,ys);Z=landscape_height(X,Y,seed)
    nx=len(xs);ny=len(ys)
    vertices=np.stack([X.ravel(),Y.ravel(),Z.ravel()],axis=1).tolist()
    faces=[(j*nx+i,j*nx+i+1,(j+1)*nx+i+1,(j+1)*nx+i) for j in range(ny-1) for i in range(nx-1)]
    ob=_mesh('ENV | continuous Alpine valley and branched mountain ridges',vertices,faces,parent,_terrain_material())
    gy,gx=np.gradient(Z,ys,xs);normalz=1/np.sqrt(1+gx*gx+gy*gy)
    # Wind scours east/south faces, while shallow gullies retain snow.
    cover=np.clip((normalz-.24)/.46-.11*gx+.14*_fbm(X*.11,Y*.11,seed+18,3),0,1)
    cover=np.maximum(cover,1-_ss((Z-14)/20))
    air=.015+.38*_ss((Y-45)/170)
    for name,values in [('snow_cover',cover),('air_depth',air)]:
        attr=ob.data.attributes.new(name,'FLOAT','POINT');attr.data.foreach_set('value',values.ravel().astype(np.float32))
    ob['height_function']='alpine_environment.landscape_height';ob['town_surface']='exact ground(x,y) for x[-32,32], y[-30,45]'
    return ob

def _snow_fir_material(mat):
    """Light dusting on upward needle surfaces; alpha silhouette is preserved."""
    if not mat.use_nodes or mat.get('ENV_snow_dusting'):return
    n=mat.node_tree.nodes;l=mat.node_tree.links;p=next((q for q in n if q.type=='BSDF_PRINCIPLED'),None)
    if p is None:return
    sock=p.inputs['Base Color'];links=list(sock.links)
    original=links[0].from_socket if links else None;color=tuple(sock.default_value)
    if links:l.remove(links[0])
    geo=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Normal'],sep.inputs[0])
    ramp=n.new('ShaderNodeMapRange');ramp.inputs['From Min'].default_value=.48;ramp.inputs['From Max'].default_value=.96;ramp.inputs['To Min'].default_value=0;ramp.inputs['To Max'].default_value=.62;l.new(sep.outputs['Z'],ramp.inputs[0])
    mix=n.new('ShaderNodeMixRGB');l.new(ramp.outputs[0],mix.inputs[0]);mix.inputs[1].default_value=color;mix.inputs[2].default_value=(.81,.86,.90,1)
    if original:l.new(original,mix.inputs[1])
    l.new(mix.outputs[0],sock);p.inputs['Roughness'].default_value=.83;mat['ENV_snow_dusting']=True

def _fir_collections():
    existing=[bpy.data.collections.get('ENV Fir variant '+str(i)+' LOD0') for i in range(3)]
    if all(existing):return existing,[bpy.data.collections['ENV Fir variant '+str(i)+' LOD1'] for i in range(3)]
    path=R/'assets/models/fir_sapling_medium/fir_sapling_medium_1k.gltf'
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(path));created=set(bpy.data.objects)-before
    source=sorted([o for o in created if o.type=='MESH'],key=lambda o:o.name)
    high=[];low=[]
    for i,o in enumerate(source):
        bpy.context.view_layer.update();pts=[o.matrix_world@Vector(c) for c in o.bound_box]
        xmin=min(p.x for p in pts);xmax=max(p.x for p in pts);ymin=min(p.y for p in pts);ymax=max(p.y for p in pts);zmin=min(p.z for p in pts);h=max(p.z for p in pts)-zmin
        transform=Matrix.Scale(1/h,4)@Matrix.Translation(Vector((-(xmin+xmax)/2,-(ymin+ymax)/2,-zmin)))@o.matrix_world
        o.parent=None;o.matrix_world=transform
        for col in list(o.users_collection):col.objects.unlink(o)
        hc=bpy.data.collections.new('ENV Fir variant '+str(i)+' LOD0');hc.objects.link(o);high.append(hc)
        for mat in o.data.materials:_snow_fir_material(mat)
        # Decimate a separate mesh once; every distant instance shares it.
        lo=o.copy();lo.data=o.data.copy();lo.name='ENV Fir reduced mesh '+str(i);bpy.context.collection.objects.link(lo)
        bpy.context.view_layer.objects.active=lo;lo.select_set(True)
        mod=lo.modifiers.new('Distant branch simplification','DECIMATE');mod.ratio=.22
        bpy.ops.object.modifier_apply(modifier=mod.name);lo.select_set(False)
        for col in list(lo.users_collection):col.objects.unlink(lo)
        lc=bpy.data.collections.new('ENV Fir variant '+str(i)+' LOD1');lc.objects.link(lo);low.append(lc)
    for ob in created:
        if ob.type!='MESH':bpy.data.objects.remove(ob,do_unlink=True)
    return high,low

def _plant_trees(root,seed,density):
    import random
    ra=random.Random(seed);high,low=_fir_collections();placed=[];objects=[]
    # Forest groups outside the town reserve: all principal routes remain clear.
    groups=[(-47,-7,14,21,22),(-50,41,16,24,26),(45,11,13,27,30),(53,66,20,20,32),(-67,84,21,27,25),(71,110,30,18,25),(-105,44,19,28,20)]
    for cx,cy,sx,sy,count in groups:
        for _ in range(round(count*density)):
            x=ra.gauss(cx,sx*.56);y=ra.gauss(cy,sy*.56)
            if -36<x<36 and -35<y<51:continue
            if abs(x)<40 and y<65:continue
            if any((x-px)**2+(y-py)**2<9 for px,py in placed):continue
            z=float(landscape_height(x,y,seed));dx=float(landscape_height(x+.5,y,seed)-landscape_height(x-.5,y,seed));dy=float(landscape_height(x,y+.5,seed)-landscape_height(x,y-.5,seed))
            if z>62 or math.hypot(dx,dy)>1.0:continue
            h=ra.uniform(5.5,11.5)*(1-.25*max(0,(z-25)/40));variant=ra.randrange(3)
            col=high[variant] if y<8 and abs(x)<65 else low[variant]
            ob=bpy.data.objects.new('ENV | snow-dusted fir %03d'%len(placed),None);bpy.context.collection.objects.link(ob);ob.parent=root
            ob.instance_type='COLLECTION';ob.instance_collection=col;ob.location=(x,y,z-.04);width=ra.uniform(.8,1.13);ob.scale=(h*width,h*width,h);ob.rotation_euler.z=ra.random()*math.tau
            ob['tree_height_m']=h;ob['asset']='Poly Haven fir_sapling_medium CC0';objects.append(ob);placed.append((x,y))
    return objects

def build_environment(seed=SEED,tree_density=1.0,terrain_step=1.0):
    root=bpy.data.objects.new('ENV | Snow-clock Alpine valley',None);bpy.context.collection.objects.link(root)
    root['seed']=seed;root['version']='environment-v2';root['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();t=time.time()
    terrain=_make_terrain(root,terrain_step,seed)
    trees=_plant_trees(root,seed,tree_density) if tree_density>0 else []
    info={'root':root.name,'terrain':terrain.name,'seed':seed,'town_bounds':[-32,32,-30,45],'town_height':'ground(x,y)',
          'tree_count':len(trees),'terrain_vertices':len(terrain.data.vertices),'terrain_faces':len(terrain.data.polygons),
          'build_seconds':time.time()-t,'mountain_extent':[-210,210,48,270],
          'protected_clear_rectangle':[-36,36,-35,51], 'tree_assets':'Poly Haven fir_sapling_medium CC0; linked meshes and LOD1 at 22%'}
    root['environment_info']=json.dumps(info)
    return {'root':root,'terrain':terrain,'trees':trees,'ground':ground,'height':landscape_height,'info':info}

def save_environment_cache(environment,path=None):
    """Save just environment datablocks, with packed texture dependencies."""
    path=Path(path or R/'model/environment-assets-v2.blend')
    bpy.ops.file.pack_all()
    blocks={environment['root'],environment['terrain'],*environment['trees']}
    bpy.data.libraries.write(str(path),blocks,path_remap='RELATIVE',fake_user=True,compress=True)
    return str(path)

def load_environment_cache(path=None,check_source=True):
    """Append the packed shared assets without changing camera/world/palette."""
    path=Path(path or R/'model/environment-assets-v2.blend')
    with bpy.data.libraries.load(str(path),link=False) as (available,loaded):
        loaded.objects=[name for name in available.objects if name.startswith('ENV |')]
    for ob in loaded.objects:
        if ob and not ob.users_collection:bpy.context.collection.objects.link(ob)
    root=next(ob for ob in loaded.objects if ob and ob.get('environment_info'))
    if check_source and root.get('source_sha256')!=hashlib.sha256(Path(__file__).read_bytes()).hexdigest():
        raise ValueError('Environment cache predates current source; rebuild the cache before reuse.')
    info=json.loads(root['environment_info']);terrain=next(ob for ob in loaded.objects if ob and ob.type=='MESH' and ob.get('town_surface'))
    trees=[ob for ob in loaded.objects if ob and ob.get('tree_height_m')]
    return {'root':root,'terrain':terrain,'trees':trees,'ground':ground,'height':landscape_height,'info':info}

def _demo():
    bpy.ops.wm.read_factory_settings(use_empty=True);sys.path.insert(0,str(R/'src'));import craft as C
    C.palette();t=time.time();env=build_environment(tree_density=float(os.environ.get('ENV_TREES','1')));save_environment_cache(env)
    hero=C.chalet('Scale reference | approved bakery',(-5,-2,ground(-5,-2)),seed=71)
    # One reference house only. The vacant reserved town area is intentional.
    world=bpy.data.worlds.new('Winter valley morning');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.36,.48,.68,1);world.node_tree.nodes['Background'].inputs[1].default_value=.40;bpy.context.scene.world=world
    sun=bpy.data.lights.new('Low dawn from the valley pass','SUN');sun.energy=2.5;sun.color=(1,.79,.57);sun.angle=.10
    ob=bpy.data.objects.new(sun.name,sun);bpy.context.collection.objects.link(ob);ob.rotation_euler=Vector((.65,.32,-.7)).to_track_quat('-Z','Y').to_euler()
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=int(os.environ.get('ENV_SAMPLES','64'));scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.025;scene.cycles.max_bounces=7
    scene.cycles.transparent_max_bounces=12
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
    for d in prefs.devices:d.use=d.type=='OPTIX'
    scene.cycles.device='GPU';scene.cycles.seed=SEED;scene.cycles.use_animated_seed=False
    scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.render.resolution_percentage=int(os.environ.get('ENV_SCALE','100'));scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.threads_mode='FIXED';scene.render.threads=4
    scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.65
    camd=bpy.data.cameras.new('Environment scale portrait');cam=bpy.data.objects.new(camd.name,camd);bpy.context.collection.objects.link(cam);scene.camera=cam
    cam.location=(59,-126,99);target=Vector((0,42,27));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();camd.lens=37;camd.clip_end=1800
    camd.dof.use_dof=False
    folder=R/'render/alpine-environment';folder.mkdir(parents=True,exist_ok=True)
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(R/'model/environment-v2.blend'))
    scene.render.filepath=str(folder/'environment-portrait.png');rt=time.time();bpy.ops.render.render(write_still=True)
    info=env['info'];info.update({'render_seconds':time.time()-rt,'total_seconds':time.time()-t,'size':[1080,1920],'samples':scene.cycles.samples,'scene_mesh_polygons':sum(len(m.polygons) for m in bpy.data.meshes),'scene_mesh_vertices':sum(len(m.vertices) for m in bpy.data.meshes),'review':'producer actual still inspection pending; environment model only'})
    (folder/'environment-info.json').write_text(json.dumps(info,indent=2),encoding='utf8');print('ENVIRONMENT_READY',json.dumps(info),flush=True)

if __name__=='__main__':_demo()
