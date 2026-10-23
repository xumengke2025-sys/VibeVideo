"""Inspect current choreography against real freight and worker rigs on CPU."""
import ast,sys,json,math,hashlib
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import craft as C
import actors
import freight_assets as F
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);C.palette()
source=(ROOT/'src/film_animation.py').read_text(encoding='utf8')
meta=json.loads((ROOT/'render/world-build.json').read_text());A,B=map(Vector,meta['stations'])
CA=A+Vector((0,0,3.62));CB=B+Vector((0,0,3.62));S=bpy.context.scene;O=bpy.data.objects
F.station('Hill freight station',A);F.station('Square freight station',B);F.basket();F.crate()
actors.human('Baker',baker=True);actors.human('Porter')
module=ast.parse(source)
keep={'sm','ramp','cable','progress','carrier_position','crate_position','child','person_pose','grip_hands','worker_position','worker_feet','worker_pose'}
nodes=[n for n in module.body if isinstance(n,ast.FunctionDef) and n.name in keep]
anim=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='at')
cut=next(i for i,n in enumerate(anim.body) if isinstance(n,ast.For) and 'residents' in ast.unparse(n.iter))
anim.body=anim.body[:cut];nodes.append(anim)
exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),'choreography_subset','exec'),globals())
def sample(t):
    at(t);bpy.context.view_layer.update();out={'t':t,'crate':list(O['One persistent bread crate'].location),'workers':{}}
    for name in ['Baker','Porter']:
        root=O[name];rig=next(o for o in root.children if o.type=='ARMATURE');rec={'root':list(root.location),'hands':{},'ankles':{}}
        cp=Vector(out['crate'])
        for side,sign in [('L',1),('R',-1)]:
            actual=rig.matrix_world@rig.pose.bones['finger3-1.'+side].head
            target=next(o for o in root.children_recursive if o.name.endswith('hand target '+side)).matrix_world.translation
            desired=cp+Vector((-sign*.51,-.12,.23))
            rec['hands'][side]={'point':list(actual),'target_error_m':(actual-target).length,'crate_grip_error_m':(actual-desired).length}
            target=next(o for o in root.children_recursive if o.name.endswith('foot target '+side)).matrix_world.translation
            ankle=rig.matrix_world@rig.pose.bones['foot.'+side].head
            rec['ankles'][side]={'target_error_m':(ankle-target).length}
        out['workers'][name]=rec
    return out
report={'scope':'real freight geometry and two worker rigs, CPU dependency graph only; no city or rendering',
        'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'samples':[],'boundary_changes':[]}
for t in [19.39,19.41,20,20.5,21,21.25,21.5,21.75,22,22.25,22.49,22.51,23,23.49,23.51,24.01,25,26,47.6,48,48.01,48.25,48.5,48.6,49.0,49.39,49.41,49.49,49.51,50,50.5,51,51.5,52,52.25,52.5,53,54,55,55.5,56,56.5,56.79,56.81,57,57.25,57.5,58]:
    report['samples'].append(sample(t))
for t in [19.4,20,21,22.5,23.5,24,48,49.4,49.5,50,52,55,56,56.8]:
    before=sample(t-.0001);after=sample(t+.0001)
    for name in ['Baker','Porter']:
        a=before['workers'][name];b=after['workers'][name]
        change={'t':t,'worker':name,'root_jump_m':(Vector(a['root'])-Vector(b['root'])).length}
        for side in ['L','R']:change['hand_'+side+'_jump_m']=(Vector(a['hands'][side]['point'])-Vector(b['hands'][side]['point'])).length
        if max(v for k,v in change.items() if k.endswith('_m'))>.01:report['boundary_changes'].append(change)
# Actual lid latch and instructed left palm at the same time: there is a
# visible brass latch at x=0, y=-.91, z=.02 in hinge coordinates.
report['lid_contacts']=[]
for t in [48.01,48.25,48.5,49,49.49]:
    state=sample(t);latch=O['Freight lid hinge'].matrix_world@Vector((0,-.91,.02))
    hand=Vector(state['workers']['Porter']['hands']['L']['point'])
    report['lid_contacts'].append({'t':t,'latch_world':list(latch),'hand_world':list(hand),'hand_to_latch_center_m':(hand-latch).length,
        'IK_target_error_m':state['workers']['Porter']['hands']['L']['target_error_m']})
report['geometry']={'platform_top_station_z':.4,'table_top_station_z':1.35,'basket_base_station_z':1.2,
 'basket_plank_top_station_z':1.2+.57+.147/2,'crate_lateral_transfer_bottom_station_z':2.1,
 'lateral_transfer_plank_clearance_m':2.1-(1.2+.57+.147/2),
 'initial_crate_handle_station_z':1.28+.23,'work_tread_top_station_z':.65}
report['maximum_hand_target_error_m']=max(h['target_error_m'] for s in report['samples'] for w in s['workers'].values() for h in w['hands'].values())
report['maximum_ankle_target_error_m']=max(h['target_error_m'] for s in report['samples'] for w in s['workers'].values() for h in w['ankles'].values())
report['dense_coverage']={'fps':24,'windows':[[19.3,26.1],[47.5,58.5]],'samples':0,'maximum_hand_target_error_m':0,'maximum_ankle_target_error_m':0,'worst_hand':None,'worst_ankle':None}
for begin,end in report['dense_coverage']['windows']:
    for frame in range(math.floor(begin*24),math.ceil(end*24)+1):
        state=sample(frame/24);report['dense_coverage']['samples']+=1
        for name,w in state['workers'].items():
            for kind in ['hands','ankles']:
                key='maximum_'+('hand' if kind=='hands' else 'ankle')+'_target_error_m'
                for side,d in w[kind].items():
                    if d['target_error_m']>report['dense_coverage'][key]:
                        report['dense_coverage'][key]=d['target_error_m'];report['dense_coverage']['worst_'+('hand' if kind=='hands' else 'ankle')]=[frame/24,name,side]
out=ROOT/'render/actor-transfer-audit.json';out.write_text(json.dumps(report,indent=2),encoding='utf8')
print('TRANSFER_AUDIT',out)
print('BOUNDARY_CHANGES',json.dumps(report['boundary_changes']))
print('LID_CONTACTS',json.dumps(report['lid_contacts']))
print('MAXIMUM_ERRORS',report['maximum_hand_target_error_m'],report['maximum_ankle_target_error_m'])
print('DENSE_COVERAGE',json.dumps(report['dense_coverage']))
