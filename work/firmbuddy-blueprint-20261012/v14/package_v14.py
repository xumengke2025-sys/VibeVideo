from pathlib import Path
import json,zipfile,hashlib
R=Path(__file__).resolve().parent;B=R.parent;O=B/'out/final-v14-burden-journey';Z=B/'FirmBuddy-source-v14-burden-journey.zip'
names=['README.md','brief.md','film.js','intro.js','scene-body.js','journey.js','index.html','setup.py','render.mjs','plan.json','make_audio.py','verify_delivery.py','check_journey.mjs','opportunity-logic-evidence.json','original-video-continuity.json','professional-ai-content-evidence.json','reduction-content-evidence.json','source-transfer.json','package.json','requirements.txt','package_v14.py']
files=[R/n for n in names]+list((R/'vendor').rglob('*'))+[R/'audio'/n for n in ['mix.wav','music.wav','foley.wav','timing.json']]+[B/'server.mjs',B/'CHECKPOINT.md',B/'out/journey-v14-checks.json']
files+=list(O.glob('*.json'))+[O/'final-overview.jpg']
files+=[B/'out/stills-v14-checked'/n for n in ['5.png','39.5.png','89.5.png','checks.json','six-unloads.jpg']]
files+=[B/'out/sample-v14-unload-transfer'/n for n in ['evidence.json','transfer-contact.jpg']]
required=[O/'video.mp4',O/'delivery-checks.json',O/'completion-audit.json',B/'out/journey-v14-checks.json']
assert all(p.is_file() for p in required),'Missing delivery evidence'
entries=[]
with zipfile.ZipFile(Z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in files:
  if not f.is_file() or '__pycache__' in f.parts:continue
  b=f.read_bytes();name=f.relative_to(B).as_posix();z.writestr(name,b);entries.append(dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 z.writestr('MANIFEST-v14.json',json.dumps(entries,ensure_ascii=False,indent=2))
with zipfile.ZipFile(Z) as z:
 assert z.testzip() is None
 assert all(f'v14/{n}' in z.namelist() for n in ['film.js','journey.js','audio/mix.wav','vendor/draw.js','vendor/paper.js'])
result=dict(zip=str(Z),files=len(entries),bytes=Z.stat().st_size,sha256=hashlib.sha256(Z.read_bytes()).hexdigest())
(O/'source-package.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
