"""CPU-only, isolated rig/contact verification. No production world is loaded."""
import sys, json, math
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import craft as C
import actors
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
C.palette()
root=actors.human('Contact worker',baker=True)
rig=next(o for o in root.children if o.type=='ARMATURE')
report={'scope':'isolated CPU dependency-graph rig verification; no image render or full mesh collision test',
        'target_semantics':'hand target is middle-finger base/palm grip point, not wrist',
        'recommended_interface':{'holding_root_offset_y':-.47,'grip_world_offset_y':-.12,'grip_x_abs':.51,'grip_height_above_crate_bottom':.23},
        'contact_samples':[],'accessories':[]}
root.rotation_euler.z=math.pi
for bottom in [1.28,1.35,1.45,1.6,1.8]:
    crate=Vector((8.4,3.2,7.0+bottom));root.location=(crate.x,crate.y-.47,7.4)
    bpy.context.view_layer.update()
    target_points={}
    for side,sign in [('L',1),('R',-1)]:
        point=crate+Vector((-sign*.51,-.12,.23));target_points[side]=point
        target=next(o for o in root.children_recursive if o.name.endswith('hand target '+side))
        target.location=root.matrix_world.inverted()@point
    bpy.context.view_layer.update()
    for side in ['L','R']:
        actual=rig.matrix_world@rig.pose.bones['finger3-1.'+side].head
        palm=rig.matrix_world@rig.pose.bones['grip.'+side].tail
        stretch=max(abs(rig.pose.bones[bn+side].length-rig.data.bones[bn+side].length) for bn in ['upperarm01.','upperarm02.','lowerarm01.','lowerarm02.'])
        report['contact_samples'].append({'crate_bottom_above_station':bottom,'side':side,
              'grip_point':list(actual),'expected':list(target_points[side]),'contact_error_m':(actual-target_points[side]).length,
              'palm_marker_to_finger_base_m':(actual-palm).length,'maximum_arm_bone_stretch_m':stretch})
for ob in root.children_recursive:
    if ob.type=='MESH' and any(key in ob.name for key in ['wool cap','buckled shoe','coat skirts','linen apron','coat buttons','neck strap']):
        modifiers=[m.type for m in ob.modifiers]
        item={'name':ob.name,'rig_bound':any(m.type=='ARMATURE' and m.object==rig for m in ob.modifiers),'vertex_count':len(ob.data.vertices)}
        if 'buckled shoe' in ob.name:
            evaluated=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=evaluated.to_mesh()
            item['sole_above_platform_m']=min((evaluated.matrix_world@v.co).z for v in mesh.vertices)-7.4
            evaluated.to_mesh_clear()
        report['accessories'].append(item)
def vertex_world(ob,index=0):
    evaluated=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=evaluated.to_mesh()
    result=evaluated.matrix_world@mesh.vertices[index].co;evaluated.to_mesh_clear();return result
cap=next(o for o in root.children_recursive if 'period wool cap' in o.name)
shoe=next(o for o in root.children_recursive if 'buckled shoe L' in o.name)
skirt=next(o for o in root.children_recursive if 'coat skirts' in o.name)
before={o.name:vertex_world(o) for o in [cap,shoe,skirt]}
rig.pose.bones['head'].rotation_mode='XYZ';rig.pose.bones['head'].rotation_euler.x=.15
rig.pose.bones['upperleg01.L'].rotation_mode='XYZ';rig.pose.bones['upperleg01.L'].rotation_euler.x=.2
rig.pose.bones['root'].rotation_mode='XYZ';rig.pose.bones['root'].rotation_euler.x=.04
bpy.context.view_layer.update()
report['accessory_deformation_probe']={o.name:(vertex_world(o)-before[o.name]).length for o in [cap,shoe,skirt]}
report['maximum_contact_error_m']=max(x['contact_error_m'] for x in report['contact_samples'])
report['passed']=report['maximum_contact_error_m']<.002 and all(x['rig_bound'] for x in report['accessories']) and all(abs(x.get('sole_above_platform_m',0))<.003 for x in report['accessories'])
out=ROOT/'render/actor-contact-report.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print('CONTACT_REPORT',str(out),'pass',report['passed'],'max error m',report['maximum_contact_error_m'])
assert report['passed'],report
