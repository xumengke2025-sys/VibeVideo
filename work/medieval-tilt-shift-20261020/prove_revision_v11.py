from pathlib import Path
import json, os, subprocess, time, sys, hashlib
import numpy as np

ROOT=Path(__file__).resolve().parent
QA=ROOT/'qa/v11'
BLENDER=ROOT.parents[1]/'tools/blender-portable/blender-4.5.3-windows-x64/blender.exe'
data=np.load(ROOT/'traffic-v11.npz');s=data['state'];names=[str(n) for n in data['names']]
minimum=1e9;worst=None;substantial=[];minimum_clearance=1e9
radii=data['radii'];wanted=radii[:,None]+radii[None,:]
for f in range(len(s)):
    xy=s[f,:,:2];delta=xy[:,None,:]-xy[None,:,:]
    d=np.linalg.norm(delta,axis=2)
    d[np.abs(s[f,:,2,None]-s[f,None,:,2])>1]=1e9
    d[np.eye(len(names),dtype=bool)]=1e9
    a,b=np.unravel_index(np.argmin(d),d.shape)
    minimum_clearance=min(minimum_clearance,float((d-wanted).min()))
    if d[a,b]<minimum:minimum=float(d[a,b]);worst={'seconds':f/8,'names':[names[a],names[b]],'distance':minimum}
    for a,b in zip(*np.where(np.triu(d<.29,k=1))):substantial.append({'seconds':f/8,'pair':[names[a],names[b]],'distance':float(d[a,b])})
assert np.all(np.isfinite(s)), 'Nonfinite traffic data'
assert not substantial, f'Visible-body overlap candidate(s): {substantial[:3]}'
assert minimum_clearance>=.025, f'Personal space constraint failed: {minimum_clearance}'
report={'cache_shape':list(s.shape),'fixed_hz':8,'sample_interval_seconds':.125,'minimum_center_distance_metres':minimum,'minimum_clearance_beyond_body_radii_metres':minimum_clearance,'worst_pair':worst,'body_overlap_candidates_below_029m':substantial,'limits':'All cached 8Hz states checked. Numerical center/radius checks do not establish natural-looking traffic or prove all detailed mesh collisions absent.'}
(QA/'traffic-check.json').write_text(json.dumps(report,indent=2),encoding='utf8')
proofs=[('CYCLES',[168,288,504,576,756,972,1176,1392,1560,1752])]
if '--compare' in sys.argv:proofs.append(('EEVEE',[504,1176]))
for engine,frames in proofs:
    record={'engine':engine,'frames':frames,'hashes':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['model/babylon-city-v11.blend','render_city_v11.py','traffic-v11.npz','v11-timeline.json']}}
    signature=hashlib.sha256(json.dumps(record['hashes'],sort_keys=True).encode()).hexdigest()[:10]
    folder='proof-v11-'+signature+'-'+engine.lower();record['folder']='render/'+folder
    (QA/f'proof-source-{engine.lower()}.json').write_text(json.dumps(record,indent=2),encoding='utf8')
    env=os.environ.copy();env.update(CITY_DEVICE='OPTIX',CITY_DENOISER='OPENIMAGEDENOISE',CITY_DENOISE_GPU='1',CITY_COMPOSITOR='GPU',CITY_TILING='0',CITY_FRAME_DIR=folder)
    if engine=='EEVEE':env['CITY_ENGINE']='EEVEE'
    else:env.pop('CITY_ENGINE',None)
    start=time.time()
    with (QA/f'proof-{engine.lower()}.log').open('w',encoding='utf8') as log:
        p=subprocess.run([str(BLENDER),'--background','--python-exit-code','1','--python',str(ROOT/'render_city_v11.py'),'--','stills',*[str(f) for f in frames]],env=env,stdout=log,stderr=subprocess.STDOUT)
    if p.returncode:raise SystemExit(f'{engine} proof failed; see log')
    assert all((ROOT/f'render/{folder}'/f'{f:05d}.png').exists() for f in frames),f'{engine} did not produce requested proof frames'
    print(json.dumps({'engine':engine,'frames':frames,'elapsed_seconds':time.time()-start}),flush=True)
print('V11_PROOFS_READY',flush=True)
