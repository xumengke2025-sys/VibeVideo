"""Preserve the v5 city and extend transverse paving to the western canal edge."""
from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'babylon-city-v5.blend'))
changed=[]
for ob in bpy.context.scene.objects:
    if ob.name.startswith('West connected cross street'):
        # These mesh vertices are authored directly in world coordinates.
        before=max(v.co.x for v in ob.data.vertices)
        for v in ob.data.vertices:
            if v.co.x>0: v.co.x=23
        changed.append({'name':ob.name,'old_east_edge':before,'new_east_edge':23,'street_y':sum(v.co.y for v in ob.data.vertices)/len(ob.data.vertices)})
assert len(changed)>10 and all(abs(x['old_east_edge']-12)<.01 for x in changed)
bpy.context.scene['street_connection_revision']='v6: cross streets reach western canal edge x=23; original continuous avenue preserved'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'babylon-city-v6.blend'))
(ROOT/'out/street-connections-v6.json').write_text(json.dumps({'changed':changed,'visual_status':'pending revised frame','central_avenue':'unchanged, continuous stone courses to y=180 then shader pavement to y=1800'},indent=2),encoding='utf8')
