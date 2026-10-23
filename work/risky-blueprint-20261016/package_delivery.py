from pathlib import Path
import hashlib, json, zipfile, sys

root=Path(__file__).resolve().parent
version=sys.argv[1] if len(sys.argv)>1 else 'v3-final'
video_dir=root/'out'/('video-'+version)
dest=root/'delivery'
dest.mkdir(exist_ok=True)
files=[]
for folder in ['v3','evidence']:
    files.extend(p for p in (root/folder).rglob('*') if p.is_file())
files.extend(root/p for p in ['build-v3.mjs','README.md','CHECKPOINT.md','package_delivery.py'])
files.extend(p for p in video_dir.iterdir() if p.is_file() and p.suffix in ['.json','.mp4'])
files.extend(p for p in (root/'out/stills-v3-delivery-concept').iterdir() if p.is_file())
if (root/'qa').exists():
    files.extend(p for p in (root/'qa').rglob('*') if p.is_file() and 'frames-evidence' not in p.parts and p.suffix in ['.json','.md'])
    files.extend((root/'qa').glob('*/frames-evidence/atlas-*.jpg'))
    files.extend((root/'qa').glob('*/frames-evidence/frame-audit.json'))
manifest={str(p.relative_to(root)).replace('\\','/'):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
(dest/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
target=dest/'Risky-V3-source-and-video.zip'
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
    for p in files:z.write(p,p.relative_to(root))
    z.write(dest/'manifest.json','manifest.json')
with zipfile.ZipFile(target) as z:
    bad=z.testzip()
    if bad:raise RuntimeError('Corrupt archive member: '+bad)
print(json.dumps({'archive':str(target),'bytes':target.stat().st_size,'files':len(files),'zip_crc_verified':True},ensure_ascii=False))
