import json,zipfile,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
final=ROOT/'out/final-v5-final-build';video=final/'video.mp4'
evidence=json.loads((final/'evidence.json').read_text(encoding='utf-8'))
assert hashlib.sha256(video.read_bytes()).hexdigest()==evidence['sha256']
assert evidence['width']==1920 and evidence['height']==1080 and evidence['count']==1560 and evidence['decoded'] and evidence['audio']
stills=json.loads((ROOT/'out/stills-v5-final-build/checks.json').read_text(encoding='utf-8'));assert not stills['errors'] and all(s['identical'] for s in stills['seeks'])
layout=json.loads((ROOT/'out/layout-v5.json').read_text(encoding='utf-8'));assert not layout['issues']
observations=json.loads((final/'observations.json').read_text(encoding='utf-8'));assert observations['sha256']==evidence['sha256']
checks={'video':str(video),'sha256':evidence['sha256'],'duration':52,'width':1920,'height':1080,'fps':30,'frames':1560,'full_decode':True,'video_codec':'H264','audio_codec':'AAC','deterministic_seeks':stills['seeks'],'layout':{'samples':layout['samples'],'issues':0,'scope':layout['scope']},'visual_observations':observations,'full_listening_completed':False,'independent_review':'Previous round used; this user-requested V5 revision has production observations, no new independent review.'}
(final/'delivery-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
files=[p for p in (ROOT/'v5').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
files+=[ROOT/f for f in ['server.mjs','REVISION-V5.md','product-reassessment-20261013.json']]
files+=[p for p in (ROOT/'assets/reference').rglob('*') if p.is_file()]
files+=[final/f for f in ['evidence.json','delivery-checks.json','observations.json','ffprobe.json']]
files+=[ROOT/'out/layout-v5.json',ROOT/'out/stills-v5-final-build/checks.json']
archive=ROOT/'FirmBuddy-source-v5.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for f in files:z.write(f,f.relative_to(ROOT))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps({'video':str(video),'megabytes':round(video.stat().st_size/1048576,2),'source':str(archive),'source_megabytes':round(archive.stat().st_size/1048576,2)},ensure_ascii=False))
