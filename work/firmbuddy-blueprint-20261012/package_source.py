from pathlib import Path
import json
import zipfile

root = Path(__file__).resolve().parent
data = json.loads((root / 'audio/timing.json').read_text(encoding='utf-8'))
def stamp(t):
    ms = round(t * 1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
subs = '\n\n'.join(f'{i+1}\n{stamp(e["start"])} --> {stamp(e["end"])}\n{e["text"]}' for i, e in enumerate(data['entries']))
(root / 'audio/narration.srt').write_text(subs+'\n', encoding='utf-8-sig')
with zipfile.ZipFile(root / 'FirmBuddy-source.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    files = [p for p in root.iterdir() if p.suffix in {'.js','.mjs','.html','.ps1','.py','.md'}]
    for folder in ['assets/reference','vendor','audio']:
        files.extend(p for p in (root/folder).rglob('*') if p.is_file())
    for file in files:
        archive.write(file, file.relative_to(root))
print('Source package and SRT written')
