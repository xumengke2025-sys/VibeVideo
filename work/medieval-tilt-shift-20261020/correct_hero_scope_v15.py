"""Apply explicit user scope: no facial anatomy; precision serves cycling."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
path=P/'model/refine_rider_v15.py';s=path.read_text(encoding='utf8')
a=s.index('# Face:');b=s.index('# Felt fedora',a)
s=s[:a]+'''# Face: intentionally featureless miniature head per explicit user direction.
m=Mesh();rows=[]
profile=[(1.731,.047,.047,.053),(1.751,.065,.060,.055),(1.785,.084,.077,.058),(1.823,.102,.090,.063),(1.858,.115,.099,.068),(1.900,.118,.099,.068),(1.943,.111,.094,.063),(1.979,.098,.084,.056),(2.010,.071,.066,.051),(2.024,.001,.001,.048)]
for z,rx,ry,cy in profile:
 rows.append([(rx*math.cos(a),cy+ry*math.sin(a),z) for a in [i*math.tau/48 for i in range(49)]])
strip(m,rows,skin)
# Hair is a quiet back-of-head silhouette below the hat, without facial features.
rows=[]
for z,r in [(1.954,.113),(1.976,.105),(2.008,.078)]:
 rows.append([(r*math.cos(a),.055+r*.86*math.sin(a),z) for a in [math.pi+math.pi*i/32 for i in range(33)]])
strip(m,rows,hair);replace('face and moustache',m)
''' +s[b:]
s=s.replace("data['detail_revision']=2","data['detail_revision']=4").replace("'revision':2","'revision':4")
s=s.replace('shaped face and eyelids; sculpted fedora','featureless miniature head per user; sculpted fedora')
path.write_text(s,encoding='utf8')
cp=P/'CHECKPOINT-v15.json';d=json.loads(cp.read_text(encoding='utf8'));d['user_correction']='No facial features or eyeballs. Precision means coat silhouette, riding posture, contacts, bicycle structure and interactions.';d['status']='applying_featureless_hero_scope';d['next_action']='Rebuild detail model without facial features; validate hero silhouette and cycling actions, then full production.';cp.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print('V15_USER_SCOPE_CORRECTED')
