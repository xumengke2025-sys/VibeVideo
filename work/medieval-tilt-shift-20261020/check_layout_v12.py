import json,sys
from pathlib import Path
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parent
source=(ROOT/'render_city_v12.py').read_text(encoding='utf8').split("if mode=='proof':frames=")[0]
exec(compile(source,str(ROOT/'render_city_v12.py'),'exec'),globals())
records=[]
for t in [16.5,22,26.5,27.5,31.5,36]:
 at(t);bpy.context.view_layer.update();items=[]
 for ob,ev in zip(special_objects,special):
  if ev['kind'] not in ['patrol','tow']:continue
  p=ob.matrix_world@Vector((0,0,1.25));v=world_to_camera_view(scene,cam,p)
  items.append({'name':ob.name,'kind':ev['kind'],'world':list(p),'screen':[v.x,1-v.y,v.z],'inside':0<v.x<1 and 0<v.y<1})
 records.append({'time':t,'items':items})
(ROOT/'qa/v12/layout-evidence.json').write_text(json.dumps(records,indent=2),encoding='utf8')
for r in records:
 relevant=[d for d in r['items'] if d['kind']==('patrol' if r['time']<27 else 'tow')]
 print('LAYOUT',r['time'],sum(d['inside'] for d in relevant),'/',len(relevant),[(d['name'],[round(x,2) for x in d['screen'][:2]]) for d in relevant],flush=True)
