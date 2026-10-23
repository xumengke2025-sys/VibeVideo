from pathlib import Path
import json,zipfile,hashlib
R=Path(__file__).resolve().parent;B=R.parent;O=B/'out/final-v12-business-value';Z=B/'FirmBuddy-source-v12-business-value.zip'
files=list(R.rglob('*'))+[B/'server.mjs',B/'CHECKPOINT.md']+list((B/'concepts/v12').glob('*'))+list(O.glob('*.json'))+list(O.glob('*.jpg'))+[B/'out/layout-v12.json',B/'out/motion-v12.json',B/'out/sample-v12-business-handoff/handoff-contact.jpg',B/'out/sample-v12-business-handoff/evidence.json']
exclude={'prepare_delivery.py','make_opening_audio.py','premix.wav','music.wav','foley.wav','retained-v10.wav'}
entries=[]
with zipfile.ZipFile(Z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in files:
  if not f.is_file() or f.name in exclude or '__pycache__' in f.parts:continue
  b=f.read_bytes();name=f.relative_to(B).as_posix();z.writestr(name,b);entries.append(dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 z.writestr('MANIFEST-v12.json',json.dumps(entries,ensure_ascii=False,indent=2))
with zipfile.ZipFile(Z) as z:assert z.testzip() is None
result=dict(zip=str(Z),files=len(entries),bytes=Z.stat().st_size,sha256=hashlib.sha256(Z.read_bytes()).hexdigest())
(O/'source-package.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
