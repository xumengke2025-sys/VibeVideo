"""Attach the seven deferred-batch seats to their existing animated hull."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'babylon-city-v9.blend'))
scene=bpy.context.scene
seats=bpy.data.objects['Boat crossbench.001']
hull=bpy.data.objects['Carvel wooden river boat.003']
parent=bpy.data.objects['Animated canal boat']
assert seats.parent is None and hull.parent==parent
assert len(seats.data.vertices)==392
before=seats.matrix_world.copy()
seats.parent=parent
seats.matrix_world=before
scene.view_layers.update()
checks=[]
for frame in [852,0,744,203,1343,639,168,1224,852]:
    wt=math.floor((frame/24)*8)/8
    parent.location.y=-.58*wt
    parent.location.z=.025*math.sin((frame/24)*1.3)
    bpy.context.view_layer.update()
    def center(ob):
        points=[ob.matrix_world@v.co for v in ob.data.vertices]
        return Vector([(min(p[i] for p in points)+max(p[i] for p in points))/2 for i in range(3)])
    a,b=center(seats),center(hull)
    assert abs(a.x-b.x)<1e-5 and abs(a.y-b.y)<1e-5,(frame,list(a),list(b))
    checks.append({'frame':frame,'seat_hull_xy_offset':[a.x-b.x,a.y-b.y],'parent':seats.parent.name})
parent.location=(0,0,0)
bpy.context.view_layer.update()
scene['city_version']='v10'
scene['v10_scope']='Seven legacy crossbenches attached to their animated hull; all photography, materials, world scale and music retained.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'babylon-city-v10.blend'))
report={'before':{'object':seats.name,'parent':None,'vertices':392},'after':{'object':seats.name,'parent':parent.name,'same_parent_as_hull':seats.parent==hull.parent},'cause':'Deferred brick-batch seats were flushed after the legacy boat children were grouped in finish_city.py, lines 144–147.','changed_objects':[seats.name],'pose_checks':checks,'rendering':'required; source relationship check alone is not visual verification'}
(ROOT.parent/'qa/v10/boat-parenting-fix.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('MODEL_V10_READY; seven seats follow hull at all checked unordered times',flush=True)
