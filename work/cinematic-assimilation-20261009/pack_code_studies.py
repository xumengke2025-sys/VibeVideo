"""Preserve MIT runtime sources byte-for-byte, with fixed source identity and file hashes."""
from pathlib import Path
import shutil,json,hashlib
base=Path('C:/CodexTemp/vibe-github-20261009')
out=Path('D:/Codex/skills/vibe-video/assets/code-studies')
specs=[
 ('particle-beach','ishuagrawal/particle-beach','92db82255b962acf2930f19bf6e5e7790174a790',['index.html','record.mjs','js/**/*.js','LICENSE']),
 ('work-reel-26','tuzhechen2005/opus-video-skills','59744a69c7b916cfbe4c4ec84006b0c2f5e2fde1',['skills/kinetic-reel/examples/work-reel-26/reel.js','skills/kinetic-reel/examples/work-reel-26/cues.js','skills/kinetic-reel/template/reel/index.html','LICENSE'])
]
result=[]
for name,repo,commit,patterns in specs:
    src=base/('opus-video-skills' if name=='work-reel-26' else name);dst=out/name;dst.mkdir(parents=True,exist_ok=True);files=[]
    for pat in patterns:
        for p in src.glob(pat):
            rel=p.relative_to(src); target=dst/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
            files.append({'path':rel.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
    manifest={'repo':'https://github.com/'+repo,'commit':commit,'license':'MIT','scope':'complete cinematic runtime (not unrelated site/build/docs)','files':files}
    (dst/'SOURCE.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');result.append({'study':name,'files':len(files),'bytes':sum(x['bytes'] for x in files)})
print(json.dumps(result))
