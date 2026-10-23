from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parent;B=R.parent;O=B/'out/final-v19-mechanical-relief';target=B/'FirmBuddy-source-v19-mechanical-relief.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,6) as z:
 for f in sorted(R.rglob('*')):
  if f.is_file() and f.suffix!='.log' and '__pycache__' not in str(f):z.write(f,Path('v19')/f.relative_to(R))
 z.write(B/'server.mjs','server.mjs')
 for name in ['evidence.json','delivery-checks.json','ffprobe.json','final-overview.jpg','observations.json']:
  f=O/name
  if f.exists():z.write(f,Path('evidence')/name)
with zipfile.ZipFile(target) as z:assert z.testzip() is None;count=len(z.infolist())
report=dict(path=str(target),bytes=target.stat().st_size,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),files=count)
(O/'source-package.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
