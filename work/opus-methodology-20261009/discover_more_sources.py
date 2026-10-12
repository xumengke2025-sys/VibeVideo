import concurrent.futures
import json
import re
import subprocess
import urllib.request
from pathlib import Path

OUT = Path('C:/CodexTemp/vibe-more-sources-20261009')
OUT.mkdir(parents=True, exist_ok=True)
REPOS = ['guanmo-ai/awesome-ai-motion', 'PavelDoGreat/WebGL-Fluid-Simulation',
         'gkjohnson/three-gpu-pathtracer', 'motion-canvas/examples']

def gh(endpoint):
    return json.loads(subprocess.check_output(['gh', 'api', endpoint], encoding='utf-8', timeout=40))

def investigate(repo):
    meta = gh('repos/' + repo)
    commit = gh('repos/' + repo + '/commits/' + meta['default_branch'])['sha']
    tree = gh('repos/' + repo + '/git/trees/' + commit + '?recursive=1')
    if tree.get('truncated'): raise RuntimeError('truncated tree')
    name = repo.split('/')[-1]
    (OUT / (name + '-tree.json')).write_text(json.dumps(tree), encoding='utf-8')
    record = {'repository':repo,'commit':commit,'license':(meta.get('license') or {}).get('spdx_id'),
              'tree_files':sum(x['type']=='blob' for x in tree['tree'])}
    if repo.startswith('guanmo'):
        paths = ['README.md','browse/discoveries.md']
        text = ''
        for p in paths:
            with urllib.request.urlopen('https://raw.githubusercontent.com/'+repo+'/'+commit+'/'+p,timeout=30) as r:
                data = r.read().decode('utf-8')
            (OUT / (name + '-' + Path(p).name)).write_text(data,encoding='utf-8')
            text += data
        record['github_leads'] = sorted(set(re.findall(r'https://github.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)',text)))
    else:
        record['entry_candidates'] = [x['path'] for x in tree['tree'] if x['type']=='blob' and
            (x['path'].startswith(('examples/','src/')) or '/' not in x['path']) and
            Path(x['path']).suffix in ('.ts','.tsx','.glsl','.js','.md')][:90]
    return record

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records = list(pool.map(investigate, REPOS))
(OUT/'discovery.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(records,ensure_ascii=False,indent=2))
