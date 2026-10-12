"""Inspect current deliverables; does not evaluate images or fill observation logs."""
import hashlib,json,re,subprocess,shutil
from pathlib import Path
BASE=Path(__file__).resolve().parent;SKILL=Path('D:/Codex/skills/vibe-video');DEST=BASE.parents[1]/'skill/vibe-video'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
links=[]
for md in [SKILL/'SKILL.md',*[SKILL/'references'/n for n in ['director-design.md','motion-craft.md','visual-review.md','opus-methodology.md']]]:
    for target in re.findall(r'\]\(([^)]+)\)',md.read_text(encoding='utf-8')):
        if re.match(r'^[a-z]+://',target) or target.startswith('#'):continue
        p=(md.parent/target.split('#')[0]).resolve();links.append({'from':str(md),'target':target,'exists':p.exists()})
changed=[]
for p in (BASE/'before-skill').rglob('*'):
    if p.is_file() and p.name!='manifest.json':
        rel=p.relative_to(BASE/'before-skill');now=SKILL/rel
        if not now.exists() or digest(p)!=digest(now):changed.append(rel.as_posix())
added=['assets/mechanical.mjs','assets/test-motion.mjs','scripts/creative_review.py']
for rel in added:assert (SKILL/rel).is_file()
media=[]
for case,video in [('flight','flight-director.mp4'),('valve','valve-director.mp4')]:
    folder=BASE/case/'out-final';p=folder/video;meta=read(folder/'qa/media/media-evidence.json');render=read(folder/'render-evidence.json');review=read(folder/'qa/review.json')
    sha=digest(p);assert sha==render['render']['sha256']==review['video_sha256'];assert not meta['technical_failures'] and meta['full_decode']=='passed';assert meta['width']==1080 and meta['height']==1920 and meta['fps']==24;assert not render['errors'] and render['seek']['identical']
    media.append({'case':case,'video':str(p),'sha256':sha,'duration':meta['duration'],'size':[meta['width'],meta['height']],'fps':meta['fps'],'full_decode':meta['full_decode'],'visual_review':'user_preview_pending; no autonomous final approval'})
review_tests=read(BASE/'forward-test/review-test-results.json');assert all(c['exit_code']==(2 if c['expected']=='reject' else 0) for c in review_tests['cases'])
cache=read(BASE/'other-regression/cache-test-results.json');assert all(c['pass'] for c in cache['cases'])
library=read(SKILL/'references/opus-methods.json');operating=[c['id'] for c in library['cards'] if c.get('operating')]
tests=[]
for name,args in [('skill-frontmatter',['C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe','-X','utf8','D:/Codex/skills/.system/skill-creator/scripts/quick_validate.py',str(SKILL)]),('method-index',['C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe','-X','utf8',str(SKILL/'scripts/opus_methodology.py'),'validate']),('motion',['D:/docker/node.exe','--test',str(SKILL/'assets/test-motion.mjs')]),('event-contract',['D:/docker/node.exe',str(SKILL/'assets/style-studio/test-contract.mjs')])]:
    r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',timeout=120);tests.append({'name':name,'exit_code':r.returncode,'output':r.stdout[-2200:],'stderr':r.stderr[-500:]});assert r.returncode==0
sync=[]
for p in SKILL.rglob('*'):
    if p.is_file() and '__pycache__' not in p.parts:
        rel=p.relative_to(SKILL);dst=DEST/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst);sync.append({'path':rel.as_posix(),'sha256':digest(p),'match':digest(p)==digest(dst)})
save(BASE/'skill-sync-manifest.json',{'version':'0.10.1','source':str(SKILL),'destination':str(DEST),'files':sync,'all_match':all(x['match'] for x in sync)})
assert all(x['exists'] for x in links)
save(BASE/'delivery-audit.json',{'version':'0.10.1','links':links,'changed_existing_files':changed,'added_files':added,'cards_with_operating_metadata':operating,'tests':tests,'review_regression_cases':len(review_tests['cases']),'cache_regression_cases':len(cache['cases']),'media':media,'sync_files':len(sync),'all_match':True,'user_override':'Every generated video is shown first; no autonomous aesthetic calibration before user feedback. Final review logs remain pending.'})
print(json.dumps({'links':len(links),'changed_existing_files':changed,'operating_cards':len(operating),'tests':len(tests),'sync_files':len(sync),'media_verified':len(media)},ensure_ascii=False))
