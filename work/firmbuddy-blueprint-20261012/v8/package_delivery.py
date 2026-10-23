from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parent; B=R.parent; out=B/'FirmBuddy-source-v8-reduction.zip'
files=list(R.rglob('*'))+[B/'server.mjs',B/'product-reassessment-20261013.json',B/'CHECKPOINT.md',B/'v7/scene-body.js',B/'v7/audio/mix.wav',B/'out/layout-v8.json',B/'out/stills-v8-content/checks.json']
files+=list((B/'assets/reference').glob('*'))
files+=list((B/'assets/reduction-reference').glob('*'))
files+=list((B/'concepts/v6-stages').glob('*.json'))
files+=[B/'concepts/v6-stages'/f for f in ['01-input.png','02-signal.png','03-experts.png','04-knowledge.png','05-output.png','06-feedback.png','07-reveal-corrected.png']]
files+=list((B/'out/final-v8-reduction').glob('*.json'))+list((B/'out/final-v8-reduction').glob('*.jpg'))
entries=[]
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for f in files:
        if not f.is_file() or '__pycache__' in f.parts or f.name in ['premix.wav','revise_content.py','source-package.json']:continue
        data=f.read_bytes();name=f.relative_to(B).as_posix();z.writestr(name,data)
        entries.append({'path':name,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
    z.writestr('MANIFEST-v8-reduction.json',json.dumps(entries,ensure_ascii=False,indent=2))
with zipfile.ZipFile(out) as z: assert z.testzip() is None
result={'zip':str(out),'files':len(entries),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(B/'out/final-v8-reduction/source-package.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
