"""One bounded repair: pier-and-timber bridges and mastless cargo barges.

The city remains an interpretive Babylon-inspired fantasy. Bridge dimensions,
traffic, gardens and sculpture are artistic reconstruction, not a site survey.
"""
import bpy,math,json,random
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'babylon-city-v8.blend'))
sc=bpy.context.scene;R=random.Random(202610219)
wood=bpy.data.materials['Dark date palm timber']
stone=bpy.data.materials['Worn limestone']
clay=[bpy.data.materials['Sun dried brick '+str(i)] for i in range(6)]
linen=bpy.data.materials['Natural flax canvas']
cloth=bpy.data.materials['Indigo handwoven cloth']
removed=[];added=[];bridge_y=[32.,108.]
for ob in list(sc.objects):
    if ob.name.startswith('Distant connected arched bridge'):
        pts=[ob.matrix_world@Vector(v) for v in ob.bound_box]
        bridge_y.append((min(p.y for p in pts)+max(p.y for p in pts))/2)
    if ob.name.startswith(('Masonry arch bridge','Bridge deck slabs','Bridge stone parapet','Bridge handrail coping','Distant connected arched bridge','Cream lateen','Sail edge rope')) or (ob.name.startswith('Boat mast') and (not ob.parent or ob.parent.name=='Animated canal boat')):
        removed.append(ob.name);bpy.data.objects.remove(ob,do_unlink=True)

def mesh(name,vs,fs,mat):
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(mat);me.update()
    ob=bpy.data.objects.new(name,me);sc.collection.objects.link(ob);added.append(ob.name);return ob

def box(name,pos,size,mat,bevel=.025):
    sx,sy,sz=[s/2 for s in size]
    vs=[(-sx,-sy,-sz),(sx,-sy,-sz),(sx,sy,-sz),(-sx,sy,-sz),(-sx,-sy,sz),(sx,-sy,sz),(sx,sy,sz),(-sx,sy,sz)]
    ob=mesh(name,vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat);ob.location=pos
    if bevel:
        m=ob.modifiers.new('Worn timber arris','BEVEL');m.width=bevel;m.segments=2
        ob.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    return ob

def rod(name,a,b,r,mat):
    a,b=Vector(a),Vector(b);d=b-a;N=10
    vs=[(r*math.cos(i/N*math.tau),r*math.sin(i/N*math.tau),z) for z in [-d.length/2,d.length/2] for i in range(N)]
    fs=[tuple(reversed(range(N))),tuple(range(N,N*2))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
    ob=mesh(name,vs,fs,mat);ob.location=(a+b)/2;ob.rotation_euler=d.to_track_quat('Z','Y').to_euler();return ob

def rope(name,points,r=.022):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=2
    sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
    for p,co in zip(sp.bezier_points,points):p.co=co;p.handle_left_type=p.handle_right_type='AUTO'
    ob=bpy.data.objects.new(name,cu);cu.materials.append(linen);sc.collection.objects.link(ob);added.append(ob.name);return ob

for yy in sorted(bridge_y):
    near=yy<150;width=4.2 if near else 5.2;top=1.45
    # Open piers leave the two river lanes free; no solid wall beneath the span.
    for xx in [24.8,33.,41.2]:
        if near:
            box('V9 bridge pier core',(xx,yy,.04),(1.35,width+.8,2.1),clay[2],.04)
            for side in [-1,1]:
                vs=[(xx-.675,yy+side*(width/2+.35),-.5),(xx+.675,yy+side*(width/2+.35),-.5),(xx,yy+side*(width/2+1.2),-.5),
                    (xx-.675,yy+side*(width/2+.35),1.08),(xx+.675,yy+side*(width/2+.35),1.08),(xx,yy+side*(width/2+1.2),1.08)]
                mesh('V9 pointed brick cutwater',vs,[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],clay[3])
            for iz in range(7):
                zz=-.42+iz*.21
                for side in [-1,1]:
                    for j in range(8):
                        box('V9 pier visible fired brick',(xx+side*.686,yy-width/2-.25+(j+.5)*(width+.5)/8,zz),(.075,(width+.5)/8-.018,.19),clay[(j+iz)%6],.012)
            box('V9 pier limestone bearing',(xx,yy,1.04),(1.6,width+.65,.18),stone,.025)
        else:
            box('V9 distant masonry pier',(xx,yy,.12),(1.35,width+.65,1.95),clay[2],0)
    for dy in [-width*.36,0,width*.36]:
        box('V9 longitudinal timber girder',(33,yy+dy,1.14),(20.4,.22,.32),wood,.025 if near else 0)
    if near:
        for j in range(68):
            xx=22.8+(j+.5)*20.4/68
            box('V9 individual bridge deck plank',(xx,yy,1.365),(.292,width,.17),wood,.016)
        for side in [-1,1]:
            for xx in [23.,25.,29.,33.,37.,41.,43.]:
                rod('V9 timber bridge rail post',(xx,yy+side*(width/2-.1),1.4),(xx,yy+side*(width/2-.1),2.12),.055,wood)
            for xa,xb in zip([23.,25.,29.,33.,37.,41.],[25.,29.,33.,37.,41.,43.]):
                rope('V9 bridge flax handrope',[(xa,yy+side*(width/2-.1),2.04),((xa+xb)/2,yy+side*(width/2-.1),1.92),(xb,yy+side*(width/2-.1),2.04)])
    else:box('V9 distant flat wooden deck',(33,yy,1.365),(20.4,width,.17),wood,0)
    # Full solid ramps connect the deck to both existing transverse streets.
    for xa,xb,za,zb in [(20.8,22.8,.06,top),(43.2,45.2,top,.06)]:
        vs=[(xa,yy-width/2,-.05),(xb,yy-width/2,-.05),(xb,yy+width/2,-.05),(xa,yy+width/2,-.05),
            (xa,yy-width/2,za),(xb,yy-width/2,zb),(xb,yy+width/2,zb),(xa,yy+width/2,za)]
        mesh('V9 continuous bridge approach',vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],stone)

# The four legacy hulls become loaded, mastless local river barges. New V8
# square-sail traders retain their form and their deterministic lane movement.
cargo=[]
for i,(x,y,s,parent) in enumerate([(32,10,.9,None),(31,69,1,None),(36,118,.75,None),(34,87,.82,bpy.data.objects['Animated canal boat'])]):
    before=set(sc.objects)
    for j in range(5):
        py=y+(-1.9+j*.74)*s
        ob=box('V9 bound woven cargo bale',(x-.21*s,py,1.09*s),(.95*s,.62*s,.58*s),linen,.06*s)
        for dx in [-.27,.27]:
            rope('V9 cargo lashing',[(x+(dx-.21)*s,py-.33*s,.86*s),(x+(dx-.21)*s,py-.33*s,1.39*s),(x+(dx-.21)*s,py+.33*s,1.39*s),(x+(dx-.21)*s,py+.33*s,.86*s)],.014*s)
    # One boatman and steering pole make the unrigged cargo vessel legible.
    col=bpy.data.collections.get('V8 resident module '+str(i))
    ob=bpy.data.objects.new('V9 river boatman',None);ob.instance_type='COLLECTION';ob.instance_collection=col;sc.collection.objects.link(ob);added.append(ob.name)
    ob.location=(x,y+2.65*s,.75);ob.scale=(.8*s,)*3;ob.rotation_euler.z=math.pi
    rod('V9 barge steering pole',(x+.3*s,y+2.6*s,1.6*s),(x+1.55*s,y+3.6*s,-.2),.028*s,wood)
    for o in set(sc.objects)-before:
        if parent:o.parent=parent
    cargo.append({'origin':[x,y],'scale':s,'parent':parent.name if parent else None})

assert not any(o.name.startswith(('Cream lateen','Masonry arch bridge','Distant connected arched bridge')) for o in sc.objects)
assert len(bridge_y)==24,len(bridge_y)
sc['city_version']='v9';sc['v9_scope']='One repair: 24 connected pier/timber bridges, 4 unrigged cargo barges; camera/music/tilt shift retained'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'babylon-city-v9.blend'))
e={'removed_objects':removed,'new_objects':len(added),'crossings_y':sorted(bridge_y),'bridge_type':'brick piers, timber girders and flat plank decks, continuous solid approaches','cargo_barges':cargo,'retained_square_sail_boats':4,'camera_and_audio':'unchanged','scope':'Geometry built; rendered evidence still required','sources':[{'url':'https://sourcebooks.web.fordham.edu/ancient/herodotus-history.asp','basis':'Herodotus 1.186, piers joined by squared wooden timbers; literary account, not dimension evidence'},{'url':'https://www.iranicaonline.org/articles/bridges/','basis':'Babylon Euphrates bridge and pier/timber construction discussion'}]}
(ROOT/'out/model-v9-evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2),encoding='utf8')
print('MODEL_V9_READY',len(added),'objects,',len(bridge_y),'crossings',flush=True)
