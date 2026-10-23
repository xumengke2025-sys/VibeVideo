from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parent;B=R.parent;out=B/'FirmBuddy-source-v6.zip'
files=list(R.rglob('*'))+[B/'server.mjs',B/'product-reassessment-20261013.json',B/'CHECKPOINT.md',B/'v5/film.js']
files+=list((B/'assets/reference').glob('*'))
files+=list((B/'concepts/v6-stages').glob('*.json'))
files+=[B/'concepts/v6-stages'/f for f in ['01-input.png','02-signal.png','03-experts.png','04-knowledge.png','05-output.png','06-feedback.png','07-reveal-corrected.png']]
files+=[B/'out/motion-v6.json',B/'out/layout-v6.json',B/'out/stills-v6-release/checks.json']
files+=list((B/'out/final-v6-delivery').glob('*.json'))
files+=list((B/'out/final-v6-delivery').glob('*.jpg'))
entries=[]
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for f in files:
        if not f.is_file() or '__pycache__' in f.parts:continue
        data=f.read_bytes();name=f.relative_to(B).as_posix();z.writestr(name,data);entries.append({'path':name,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
    z.writestr('MANIFEST-v6.json',json.dumps(entries,ensure_ascii=False,indent=2))
with zipfile.ZipFile(out) as z:
    bad=z.testzip();assert bad is None,bad
print(json.dumps({'zip':str(out),'files':len(entries),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},ensure_ascii=False))
