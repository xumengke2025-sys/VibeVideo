import bpy,json,math,os,time
import numpy as np
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parent
source=(ROOT/'render_city_v13.py').read_text(encoding='utf8').split("if mode=='proof':frames=")[0]
exec(compile(source,str(ROOT/'render_city_v13.py'),'exec'),globals())
records=[]
for t in [16,16.5,22,26.5,27.5,31,36,73]:
    state=at(t);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();items=[]
    for ob,ev in zip(special_objects,special):
        if ev['kind'] not in ['tow','patrol']:continue
        q=ob.matrix_world@Vector((0,0,1.3));v=world_to_camera_view(scene,cam,q)
        delta=q-cam.location
        hit,point,normal,index,blocker,matrix=scene.ray_cast(dg,cam.location,delta.normalized(),distance=delta.length-.25)
        ground_hit,ground,_,_,groundob,_=scene.ray_cast(dg,Vector((ob.location.x,ob.location.y,4)),Vector((0,0,-1)),distance=4)
        items.append({'name':ob.name,'kind':ev['kind'],'world':list(ob.location),'screen':[v.x,1-v.y,v.z],'inside':0<v.x<1 and 0<v.y<1,'blocker':blocker.name if hit and blocker.name!=ob.name else None,'surface_z':ground.z if ground_hit else None,'surface':groundob.name if ground_hit else None})
    records.append({'time':t,'items':items})
    relevant=[d for d in items if d['kind']==('patrol' if t<27 else 'tow')]
    print('V13_LAYOUT',t,[(i['kind'],[round(x,2) for x in i['screen'][:2]],i['blocker'],i['surface_z']) for i in relevant],flush=True)
collisions=[]
for row in range(16*8,27*8):
    t=row/8
    for ev in special:
        if ev['kind']!='patrol':continue
        xy=np.array(ev['base'][:2])+np.array([0,t*ev['speed']])
        d=np.linalg.norm(traffic['state'][row,:,:2]-xy,axis=1)
        for i in np.where(d<.72)[0]:collisions.append({'t':t,'soldier':ev['name'],'actor':str(traffic['names'][i]),'distance':float(d[i])})
(ROOT/'qa/v13/layout-evidence.json').write_text(json.dumps({'records':records,'patrol_civilian_close_approaches':collisions},indent=2),encoding='utf8')
print('PATROL_NEAR_APPROACHES',len(collisions),collisions[:6],flush=True)
dest=ROOT/'render/proof-v13';dest.mkdir(exist_ok=True)
for f in [396,528,636,660,744,864]:
    at(f/24);scene.render.filepath=str(dest/f'{f:05d}.png');bpy.ops.render.render(write_still=True)
    print('V13_PROOF',f,flush=True)
