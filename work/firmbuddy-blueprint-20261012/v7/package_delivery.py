from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parent; B=R.parent; out=B/'FirmBuddy-source-v7-music.zip'
files=list(R.rglob('*'))+[B/'server.mjs',B/'product-reassessment-20261013.json',B/'CHECKPOINT.md',B/'v6/scene-body.js']
files+=list((B/'assets/reference').glob('*'))
files+=list((B/'concepts/v6-stages').glob('*.json'))
files+=[B/'concepts/v6-stages'/f for f in ['01-input.png','02-signal.png','03-experts.png','04-knowledge.png','05-output.png','06-feedback.png','07-reveal-corrected.png']]
files+=list((B/'out/final-v7-music').glob('*.json'))+list((B/'out/final-v7-music').glob('*.jpg'))
entries=[]
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for f in files:
        if not f.is_file() or '__pycache__' in f.parts or f.name=='premix.wav':continue
        data=f.read_bytes();name=f.relative_to(B).as_posix();z.writestr(name,data)
        entries.append({'path':name,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
    z.writestr('MANIFEST-v7-music.json',json.dumps(entries,ensure_ascii=False,indent=2))
with zipfile.ZipFile(out) as z: assert z.testzip() is None
result={'zip':str(out),'files':len(entries),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(B/'out/final-v7-music/source-package.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
