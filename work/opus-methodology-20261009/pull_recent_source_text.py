import concurrent.futures
import hashlib
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path('C:/CodexTemp/vibe-more-sources-20261009')
REPOS = ['songbie','clearwater','lemo-opuscar','i-like-ur-look-lyric-video']
STYLES = ('art-deco','ink-wash','blueprint','hologram-hud')
SUFFIX = {'.js','.mjs','.ts','.tsx','.html','.py','.md','.json','.glsl','.swift','.txt','.css'}

def select(name,p):
    if any(x in Path(p).parts for x in ('node_modules','vendor','out','.github')): return False
    if Path(p).suffix.lower() not in SUFFIX and Path(p).name!='LICENSE': return False
    if 'lock' in Path(p).name.lower(): return False
    if name=='songbie': return not p.startswith(('media/','out/'))
    if name=='clearwater': return p in ('index.html','tools/make_pebbles.py','LICENSE','README.md')
    if name=='lemo-opuscar':
        return p in ('LICENSE','README.md','DIRECTOR.md','TECHNIQUE.md','core/lib.js') or p.startswith('core/render/') or any(p.startswith('styles/'+s+'/') for s in STYLES)
    if name=='i-like-ur-look-lyric-video':
        return p in ('LICENSE','README.md','docs/ENGINE.md','docs/TREATMENT.md') or p.startswith(('app/src/','app/scripts/')) or p in ('app/package.json','app/LICENSE','app/index.html','app/tsconfig.json','app/vite.config.ts')
    return False

def fetch(job):
    url,p=job
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url,timeout=25) as r: raw=r.read(1_500_001)
            if len(raw)>1_500_000: raise ValueError('source file exceeds limit')
            raw.decode('utf-8')
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes(raw)
            return {'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
        except Exception:
            if attempt==2: raise
            time.sleep(1)

for name in REPOS:
    r=ROOT/name
    meta=json.loads((r/'CANDIDATE.json').read_text(encoding='utf-8'))
    tree=json.loads((r/'TREE.json').read_text(encoding='utf-8'))
    jobs=[('https://raw.githubusercontent.com/'+meta['repository']+'/'+meta['commit']+'/'+x['path'],r/'source'/x['path'])
          for x in tree['tree'] if x['type']=='blob' and select(name,x['path'])]
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures={pool.submit(fetch,j):j for j in jobs}
        for f in concurrent.futures.as_completed(futures):
            try: results.append(f.result())
            except Exception as e: results.append({'path':str(futures[f][1]),'error':str(e)})
    (r/'TEXT_SOURCE.json').write_text(json.dumps({**meta,'selected_styles':list(STYLES) if name=='lemo-opuscar' else [],'retrieval':results},ensure_ascii=False,indent=2),encoding='utf-8')
    print(name,'text files',len(results),'errors',sum('error' in x for x in results),flush=True)
