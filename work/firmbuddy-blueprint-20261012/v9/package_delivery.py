from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parent; B=R.parent; out=B/'FirmBuddy-source-v9-expert-ai.zip'
files=list(R.rglob('*'))+[B/'server.mjs',B/'product-reassessment-20261013.json',B/'CHECKPOINT.md',B/'v8/scene-body.js',B/'v8/audio/mix.wav',B/'out/layout-v9.json',B/'out/stills-v9-content/checks.json']
files+=list((B/'assets/reference').glob('*'))
files+=list((B/'assets/reduction-reference').glob('*'))
files+=list((B/'concepts/v6-stages').glob('*.json'))
files+=[B/'concepts/v6-stages'/f for f in ['01-input.png','02-signal.png','03-experts.png','04-knowledge.png','05-output.png','06-feedback.png','07-reveal-corrected.png']]
files+=list((B/'out/final-v9-expert-ai').glob('*.json'))+list((B/'out/final-v9-expert-ai').glob('*.jpg'))
files+=[B/'out/sample-v9-expert-ai/evidence.json',B/'out/sample-v9-expert-ai/knowledge-to-experts.jpg']
entries=[]
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for f in files:
        if not f.is_file() or '__pycache__' in f.parts or f.name in ['premix.wav','revise_content.py','source-package.json','reduction-content-evidence.json']:continue
        data=f.read_bytes();name=f.relative_to(B).as_posix();z.writestr(name,data)
        entries.append({'path':name,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
    z.writestr('MANIFEST-v9-expert-ai.json',json.dumps(entries,ensure_ascii=False,indent=2))
with zipfile.ZipFile(out) as z: assert z.testzip() is None
result={'zip':str(out),'files':len(entries),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(B/'out/final-v9-expert-ai/source-package.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
