"""Opposite-bank tow teams and coordinated patrol with planted-foot gait."""
import ast
import bpy
import json
import math
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
QA = BASE / 'qa/v13'
QA.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT / 'babylon-city-v12.blend'))
scene = bpy.context.scene
tree = ast.parse((ROOT / 'revise_city_v12.py').read_text(encoding='utf8'))
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Mesh'], type_ignores=[]), 'v12 Mesh helper', 'exec'))
M = bpy.data.materials
skin = M['Sunlit warm skin']; navy = M['Indigo handwoven cloth']
red = M['Madder dyed fabric']; gold = M['V12 chased warm bronze']
lapis = M['V12 indigo painted timber']; leather = M['V12 dark leather']
wood = M['Dark date palm timber']; dark = M['Interior shade']

def soldier(phase, officer=False):
    m = Mesh()
    m.ring((0,0,.59),[(.27,0),(.245,.37),(.20,.71)],navy,20,.79)
    m.ball((0,0,1.18),(.225,.14,.24),navy,16)
    for j in range(6):
        for k in range(5):
            m.ball(((k-2)*.077,-.139-(2-abs(k-2))*.006,1.32-j*.064),(.043,.027,.045),gold,8,4)
    m.box((0,.145,1.02),(.37,.045,.65),red)
    # Foot travel during the 62% stance interval matches the root advance.
    # Local -Y is forward. Opposite legs alternate; stance feet stay low.
    for side in [-1,1]:
        u=(phase/math.tau+(0 if side<0 else .5))%1
        if u<.62:
            foot_y=-.285+.57*(u/.62); lift=0
        else:
            s=(u-.62)/.38
            foot_y=.285-.57*(s*s*(3-2*s)); lift=.105*math.sin(math.pi*s)
        hip=(side*.105,0,.76)
        knee=(side*.112,foot_y*.49-.07-lift*.7,.43+lift*.45)
        ankle=(side*.12,foot_y,.085+lift)
        m.rod(hip,knee,.058,skin);m.rod(knee,ankle,.046,skin)
        m.ball((ankle[0],ankle[1]-.055,ankle[2]-.025),(.078,.145,.05),leather,10,5)
    # Hands, shield grip and spear shaft use the same explicit coordinates.
    for side in [-1,1]:
        shoulder=(side*.22,0,1.31)
        elbow=(side*.30,-.075,1.10)
        hand=(side*.34,-.20,1.065)
        m.rod(shoulder,elbow,.063,skin);m.rod(elbow,hand,.049,skin)
        m.ball(hand,(.055,.055,.07),skin,10,5)
    m.rod((-.34,-.20,1.065),(-.40,-.255,1.065),.027,leather)
    m.ball((-.40,-.29,1.055),(.255,.047,.35),gold,16,8)
    m.ball((-.40,-.337,1.055),(.215,.015,.30),lapis,16,8)
    m.ball((-.40,-.358,1.055),(.065,.029,.065),gold,12,6)
    m.rod((.34,-.20,.12),(.34,-.20,2.43),.019,wood)
    m.add([(.34,-.20,2.68),(.265,-.20,2.42),(.415,-.20,2.42),(.34,-.155,2.42)],[(0,1,2),(0,3,1),(0,2,3),(1,3,2)],gold)
    m.rod((0,0,1.32),(0,0,1.49),.07,skin)
    m.ball((0,-.01,1.58),(.13,.12,.17),skin,16,8)
    m.ball((0,-.127,1.58),(.028,.045,.052),skin,8,4)
    for side in [-1,1]:
        m.ball((side*.052,-.119,1.625),(.018,.01,.012),dark,8,4)
        m.ball((side*.13,0,1.58),(.025,.04,.045),skin,8,4)
    m.ring((0,0,1.63),[(.15,0),(.152,.12),(.11,.25),(.012,.38)],gold,20)
    if officer:
        m.ring((0,0,1.74),[(.15,0),(.15,.032)],red,20)
    return m

cols={}
for role in ['soldier','officer']:
    names=[]
    for k in range(12):
        col=bpy.data.collections.new(f'V13 coordinated {role} stride {k}')
        col.use_fake_user=True
        ob=soldier(k*math.tau/12,role=='officer').bake(col.name,False)
        col.objects.link(ob);names.append(col.name)
    cols[role]=names

special=json.loads(scene['v12_special'])
patrol=[ev for ev in special if ev['kind']=='patrol']
for i,ev in enumerate(patrol):
    row=i//2;column=i%2
    ev['base']=[1.35+column*1.28,24.10-row*1.60,.04]
    ev['speed']=1.05
    ev['yaw']=math.pi
    ev['phase']=.02*(row%2)
    ev['stride_length']=.57/.62
    ev['role']='officer' if i==0 else 'soldier'
    ob=bpy.data.objects[ev['name']]
    ob.instance_collection=bpy.data.collections[cols[ev['role']][0]]
    ob['stride_modules']=json.dumps(cols[ev['role']])
    ob.location=ev['base'];ob.rotation_euler.z=math.pi

tows=json.loads(scene['v12_tows'])
by_name={ev['name']:ev for ev in special}
for index,tow in enumerate(tows):
    bank=23.35 if index==0 else 40.50
    tow['bank']=bank
    tow['bank_side']='west' if index==0 else 'east'
    for j,name in enumerate(tow['team']):
        ev=by_name[name]
        ev['base'][0]=bank+(.045 if j%2 else -.045)
        ev['base'][2]=1.17
        ev['offset']=5.0+j*1.16
        bpy.data.objects[name].location=ev['base']

# Matching paved east towpath lies on the existing retaining bank.
quay=bpy.data.objects['Continuous quay cap'].data.materials[0]
m=Mesh();m.box((41.10,68,.965),(2.80,164,.38),quay)
east=m.bake('V13 east-bank raised paved towpath')
east['v13_added_path']=True
scene['v12_special']=json.dumps(special)
scene['v12_tows']=json.dumps(tows)
scene['city_version']='v13'
scene['v13_scope']='Opposite riverbank tow teams and 12-pose phase-coordinated planted-foot patrol.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'babylon-city-v13.blend'))
(QA/'model-evidence.json').write_text(json.dumps({'tow_banks':[{k:t[k] for k in ['bank','bank_side','boat','team']} for t in tows],'patrol':patrol,'stride_pose_count':12,'stance_fraction':.62,'stride_length':.57/.62,'patrol_speed':1.05,'model':'model/babylon-city-v13.blend','appearance_pending':True},ensure_ascii=False,indent=2),encoding='utf8')
print('V13_MODEL_READY',len(patrol),[t['bank'] for t in tows],flush=True)
