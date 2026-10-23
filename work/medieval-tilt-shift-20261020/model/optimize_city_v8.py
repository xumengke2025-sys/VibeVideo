"""Distance-appropriate true courtyard meshes; preserve near geometry and city extent."""
import bpy,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'babylon-city-v8.blend'))
sc=bpy.context.scene
if not sc.get('v8_reliefs_face_street'):
    for ob in sc.objects:
        if ob.name.startswith('V8 processional lion wall'):ob.rotation_euler.z=-ob.rotation_euler.z
    sc['v8_reliefs_face_street']=True
mats=[bpy.data.materials['Sun dried brick '+str(i)] for i in range(6)]+[bpy.data.materials['Worn limestone'],bpy.data.materials['Interior shade']]
cols=[]
for i in range(12):
    v=[];f=[];mi=[];h=5.2+(i%3)*.8;w=7.5+(i%3)*.6;d=7.5+(i%3)*.5
    def block(x,y,z,sx,sy,sz,m):
        k=len(v);sx/=2;sy/=2;sz/=2
        v.extend([(x+a*sx,y+b*sy,z+c*sz) for a,b,c in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]])
        f.extend([tuple(k+q for q in p) for p in [(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]]);mi.extend([m]*6)
    for side in [-1,1]:
        block(side*w*.38,0,h/2,w*.24,d,h,i%6)
        block(side*w*.3,-d*.4,h/2,w*.36,d*.2,h,i%6)
        block(side*w/2,0,h+.25,.22,d,.5,(i+1)%6)
        block(0,side*d/2,h+.25,w,.22,.5,(i+1)%6)
        block(side*w*.29,-d/2-.02,h*.62,.6,.04,.8,7)
    block(0,d*.36,h/2,w,d*.28,h,i%6)
    block(0,-d*.4,(h+3)/2,w*.25,d*.2,h-3,i%6)
    block(0,-d*.4,2.8,w*.26,d*.21,.25,6)
    if i%4 in [0,1]:block(-w*.26,d*.22,h+1.1,w*.39,d*.39,2.2,(i+2)%6)
    me=bpy.data.meshes.new('V8 distant courtyard silhouette');me.from_pydata(v,[],f)
    for m in mats:me.materials.append(m)
    for p,m in zip(me.polygons,mi):p.material_index=m
    col=bpy.data.collections.new('V8 distant courtyard '+str(i));ob=bpy.data.objects.new('V8 single-mesh courtyard',me);col.objects.link(ob);cols.append(col)
count=0
for ob in sc.objects:
    if ob.instance_type=='COLLECTION' and ob.instance_collection and ob.location.y>300:
        old=ob.instance_collection.name
        if 'inhabited block' in old.lower() or 'courtyard house module' in old.lower():
            ob.instance_collection=cols[count%12];count+=1
sc['v8_distance_lod']=count
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'babylon-city-v8.blend'))
(ROOT/'out/lod-v8-evidence.json').write_text(json.dumps({'distant_courtyards_optimized':count,'boundary_y_metres':300,'city_extent_preserved':True,'geometry':'single-mesh open courtyards with four wings, door, parapets, upper chambers and window recesses','near_geometry':'unchanged','reliefs':'turned to face the street'}),encoding='utf8')
print('V8_LOD_READY',count,flush=True)
