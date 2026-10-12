import copy,hashlib,json,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent;SKILL=Path('D:/Codex/skills/vibe-video');QA=BASE/'qa'
def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def invoke(args):
    r=subprocess.run([sys.executable,'-X','utf8',*map(str,args)],capture_output=True,text=True,encoding='utf-8',timeout=120)
    try:out=json.loads(r.stdout)
    except ValueError:out={'stdout':r.stdout,'stderr':r.stderr}
    return {'exit_code':r.returncode,'result':out}
pending=json.loads((QA/'review.json').read_text(encoding='utf-8'))
observed=copy.deepcopy(pending);observed['status']='observed'
notes={'establish':'Viewed full-size frame: disc overlays gold seat, travel zero, drive 0.60 below preload; spring far end stays fixed.','action':'Viewed full-size frame: disc separated right from gold seat, travel clamped 1.00 and spring compressed.','result':'Viewed full-size frame: reverse drive -0.50, disc returned to seat and travel zero; pressure-axis extent unchanged.'}
for o in observed['observations']:o['note']=notes[o['state']]
window_notes=['Viewed all 25 frames on atlas 000, source 12–36: disc remains at seat through frame 16, separates at 17, travel reaches stop at 26 then holds; fixed spring end does not move.','Viewed all 13 frames on atlas 000, source 45–57: disc reaches seat by 46 and stays there under increasingly negative drive; no visible pass through seat.']
for w,note in zip(observed['continuous'],window_notes):w.update(viewed_pages=w['required_pages'],method='continuous frame contact sheet inspection',note=note)
findings={'idea':'A single pressure crossing is a readable test event, but this is a schematic fixture without a developed visual surprise.','reveal':'Source 12–36 builds pressure then opens/clamps; source 45–57 lowers through reseating.','motion':'Travel changes with the input; spring compresses while the far end stays fixed, and closing stops at seat.','camera':'Fixed schematic camera holds threshold/contact readable; no follow camera was required or tested.','composition':'Full-size frame preserves portrait margins, but sparse layout and the chart without a y-axis label limit educational delivery.','correctness':'Seat/stop constraints agree with shared state; spring-disc drawing has a small attachment gap. Diagram is marked quasi-static, not a fluid solver.'}
for d in observed['dimensions']:d.update(start=.4,end=1.9,evidence='window-00/atlas-000.jpg',finding=findings[d['dimension']])
observed['limits']=['Only three representative full-size images and the two stated continuous windows were observed. No realtime playback or audio review.','This fixture is a tool workflow test, not delivery-quality visual proof.','The spring attachment gap and missing y-axis label would need fixing before an educational delivery.']
save(QA/'observed-review.json',observed)
cases=[]
def case(name,review,plan=None,expect_reject=False):
    rp=QA/(name+'.json');save(rp,review)
    pp=BASE/'plan.json'
    if plan is not None:pp=BASE/(name+'-plan.json');save(pp,plan)
    got=invoke([SKILL/'scripts/creative_review.py','check',pp,BASE/'fixture.mp4','--review',rp,'--out',QA/(name+'-result.json')]);cases.append({'name':name,'expected':'reject' if expect_reject else 'accept consistency only',**got})
case('pending',pending,expect_reject=True)
case('observed',observed)
for w in observed['continuous']:
    audit=json.loads((QA/w['report']).read_text(encoding='utf-8'))
    w['viewed_pages']=[str(Path(w['report']).parent/n) for n in audit['atlases']]
case('observed-native-paths',observed)
old=copy.deepcopy(observed);old['video_sha256']='0'*64;case('old-hash',old,expect_reject=True)
missing=copy.deepcopy(observed);missing['continuous']=[];case('missing-continuous',missing,expect_reject=True)
pages=copy.deepcopy(observed)
for w in pages['continuous']:w['viewed_pages']=[]
case('unviewed-pages',pages,expect_reject=True)
plan=json.loads((BASE/'plan.json').read_text(encoding='utf-8'));plan['shots'][0]['risks']=[]
static=copy.deepcopy(observed);static['continuous']=[]
case('no-risks-static-only',static,plan=plan,expect_reject=True)
dim=copy.deepcopy(observed);dim['dimensions']=[{**observed['dimensions'][0],'weight':100}]
case('idea-only-no-correctness',dim,expect_reject=True)
weights=copy.deepcopy(observed);weights['dimensions'][0]['weight']=0
case('invalid-weights',weights,expect_reject=True)
stale=copy.deepcopy(observed)
audit=json.loads((QA/'window-00/frame-audit.json').read_text(encoding='utf-8'));audit['video_sha256']='0'*64
save(QA/'window-00/stale-frame-audit.json',audit)
stale['continuous'][0]['report']='window-00/stale-frame-audit.json'
case('stale-dynamic-hash',stale,expect_reject=True)
index={}
for name,args in {'validate':['validate'],'recommend':['recommend','--query','竖屏 弹簧止回阀 剖面 数据','--code-only','--limit','3'],'mechanical-card':['card','load-regulated-valve'],'mixed-source':['trace','koldo2k-778767'],'film-only':['recommend','--query','全息 弹簧 数据 水 焦散','--code-only','--film-only','--limit','8']}.items():
    index[name]=invoke([SKILL/'scripts/opus_methodology.py',*args]);save(BASE/('index-'+name+'.json'),index[name])
source_hashes={str(p.relative_to(SKILL)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [SKILL/'SKILL.md',SKILL/'scripts/creative_review.py',SKILL/'scripts/shot_contract.py',SKILL/'assets/mechanical.mjs',SKILL/'assets/motion.mjs']}
save(BASE/'review-test-results.json',{'cases':cases,'index':{k:{'exit_code':v['exit_code']} for k,v in index.items()},'skill_hashes_at_test':source_hashes,'scope':'Exit status is evidence consistency, never proof of visual or motion quality.'})
print(json.dumps([{k:c[k] for k in ['name','expected','exit_code']} for c in cases],indent=2))
