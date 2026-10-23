from pathlib import Path
import hashlib, json, zipfile

root = Path(__file__).resolve().parent
dest = root / 'delivery'
dest.mkdir(exist_ok=True)
files = []
for folder in ['v4', 'evidence', 'qa/v4', 'out/stills-v4-final-look', 'out/stills-v4-final-overall']:
    files.extend(p for p in (root/folder).rglob('*') if p.is_file() and p.name != 'body-template.js' and '__pycache__' not in p.parts)
for name in ['build-v4.mjs', 'verify-v4-motion.mjs', 'README-V4.md', 'V4-DIRECTION.md', 'CHECKPOINT.md', 'package_v4.py']:
    files.append(root/name)
files.extend(p for p in (root/'out/video-v4-final').iterdir() if p.is_file() and p.suffix in ['.json', '.mp4'])
manifest = {p.relative_to(root).as_posix(): {'bytes':p.stat().st_size, 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
manifest_path = dest/'manifest-v4.json'
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
target = dest/'Risky-V4-source-and-video.zip'
with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=5) as z:
    for p in files: z.write(p, p.relative_to(root))
    z.write(manifest_path, 'manifest-v4.json')
with zipfile.ZipFile(target) as z:
    bad = z.testzip()
    if bad: raise RuntimeError(bad)
print(json.dumps({'archive':str(target), 'bytes':target.stat().st_size, 'files':len(files), 'zip_crc_verified':True}, ensure_ascii=False))
