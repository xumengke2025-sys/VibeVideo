from pathlib import Path
import json,zipfile,hashlib
R=Path(__file__).resolve().parent;B=R.parent;out=B/'FirmBuddy-source-v18-business-story.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,6) as z:
 for f in sorted(R.rglob('*')):
  if f.is_file() and f.suffix not in ['.log'] and '__pycache__' not in str(f):z.write(f,Path('v18')/f.relative_to(R))
 z.write(B/'server.mjs','server.mjs')
 for name in ['evidence.json','delivery-checks.json','ffprobe.json','final-overview.jpg','observations.json']:
  p=B/'out/final-v18-business-story'/name
  if p.exists():z.write(p,Path('evidence')/name)
with zipfile.ZipFile(out) as z:assert z.testzip() is None; count=len(z.infolist())
data={'path':str(out),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'files':count}
(B/'out/final-v18-business-story/source-package.json').write_text(json.dumps(data,indent=2),encoding='utf-8');print(json.dumps(data))
