from pathlib import Path
import json,zipfile,hashlib
R=Path(__file__).resolve().parent;B=R.parent;O=B/'out/final-v11-opportunity-cards';Z=B/'FirmBuddy-source-v11-opportunity-cards.zip'
files=list(R.rglob('*'))+[B/'server.mjs',B/'CHECKPOINT.md']+list((B/'concepts/v11').glob('*'))+list(O.glob('*.json'))+list(O.glob('*.jpg'))+[B/'out/layout-v11.json',B/'out/motion-v11.json']
exclude={'prepare_v11.py','update_tools.py','collect_delivery.py','package_delivery.py','premix.wav','music.wav','foley.wav'}
entries=[]
with zipfile.ZipFile(Z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in files:
  if not f.is_file() or f.name in exclude or '__pycache__' in f.parts:continue
  b=f.read_bytes();name=f.relative_to(B).as_posix();z.writestr(name,b);entries.append(dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 z.writestr('MANIFEST-v11.json',json.dumps(entries,ensure_ascii=False,indent=2))
with zipfile.ZipFile(Z) as z:assert z.testzip() is None
result=dict(zip=str(Z),files=len(entries),bytes=Z.stat().st_size,sha256=hashlib.sha256(Z.read_bytes()).hexdigest())
(O/'source-package.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
