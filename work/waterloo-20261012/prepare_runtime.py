from pathlib import Path
import json, urllib.request, shutil, sys
ROOT=Path(__file__).resolve().parent
STUDIO=ROOT/'studio'
for p in ['assets','vendor','audio-assets','out']:(STUDIO/p).mkdir(parents=True,exist_ok=True)
SOURCE=ROOT.parents[1]/'reference-sources/github-expansion-20261011/lemomo-ai--lemo-opuscar'
for f in ['paper.js','lib.js']:shutil.copy2(SOURCE/'styles/paper-lantern/demo/src'/f,STUDIO/'vendor'/f)
shutil.copy2(SOURCE/'LICENSE',STUDIO/'vendor/LICENSE-Lemo-MIT.txt')
shutil.copy2(Path('C:/Users/67236/.codex/generated_images/01a12fda-7b5e-7ff3-913c-c8f79fb2ccc7/exec-955417d0-e2a5-485e-95fd-00449fb4121d.png'),STUDIO/'assets/style-triptych.png')
url='https://api.github.com/repos/mrbumpy409/GeneralUser-GS/git/trees/main?recursive=1'
req=urllib.request.Request(url,headers={'User-Agent':'Waterloo-film-local-production'})
data=json.load(urllib.request.urlopen(req,timeout=45))
items=[x for x in data.get('tree',[]) if x['path'].lower().endswith(('.sf2','.txt','.md')) and ('sf2' in x['path'].lower() or 'license' in x['path'].lower())]
print(json.dumps(items,indent=2))
(STUDIO/'audio-assets/source-tree.json').write_text(json.dumps({'url':url,'items':items},indent=2))
