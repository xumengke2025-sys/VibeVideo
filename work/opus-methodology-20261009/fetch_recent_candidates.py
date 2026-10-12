"""Read recent film candidates and their license; do not fetch media or execute code."""
import concurrent.futures
import json
import subprocess
import urllib.request
from pathlib import Path

OUT = Path('C:/CodexTemp/vibe-more-sources-20261009')
REPOS = ['JohnnyWang8802/songbie', 'Aureliengmz/clearwater', 'lemomo-ai/lemo-opuscar',
         '20q2/i-like-ur-look-lyric-video', 'neelnanda-io/dont-go-quiet-on-me']

def gh(endpoint):
    return json.loads(subprocess.check_output(['gh','api',endpoint],encoding='utf-8',timeout=40))

def read(repo):
    meta = gh('repos/'+repo)
    c = gh('repos/'+repo+'/commits/'+meta['default_branch'])
    commit = c['sha']
    tree = gh('repos/'+repo+'/git/trees/'+commit+'?recursive=1')
    if tree.get('truncated'): raise RuntimeError('truncated tree')
    root = OUT/repo.split('/')[-1]
    root.mkdir(parents=True,exist_ok=True)
    (root/'TREE.json').write_text(json.dumps(tree),encoding='utf-8')
    license_files = [x['path'] for x in tree['tree'] if x['type']=='blob' and
                     ('LICENSE' in Path(x['path']).name.upper() or x['path'] in ('README.md','README.zh-CN.md'))]
    for p in license_files:
        with urllib.request.urlopen('https://raw.githubusercontent.com/'+repo+'/'+commit+'/'+p,timeout=30) as r:
            raw=r.read(600_001)
        if len(raw)>600_000: raise RuntimeError('too large')
        raw.decode('utf-8')
        (root/p).parent.mkdir(parents=True,exist_ok=True)
        (root/p).write_bytes(raw)
    record={'repository':repo,'commit':commit,'created':meta['created_at'],
            'commit_date':c['commit']['committer']['date'],'license':(meta.get('license') or {}).get('spdx_id'),
            'description':meta['description'],'homepage':meta.get('homepage'),
            'license_files':license_files,'files':[x['path'] for x in tree['tree'] if x['type']=='blob'],
            'scope':'metadata/readme/license only; scene implementations not yet read'}
    (root/'CANDIDATE.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({**{k:v for k,v in record.items() if k!='files'},'file_count':len(record['files']),
                      'source_candidates':[p for p in record['files'] if Path(p).suffix.lower() in
                        ('.js','.mjs','.ts','.tsx','.html','.py','.glsl')][:65]},ensure_ascii=False),flush=True)
    return record

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    records=list(pool.map(read,REPOS))
(OUT/'recent-candidates.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
