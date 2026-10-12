"""Fetch pinned text source only; never fetch media or run upstream code."""
import concurrent.futures, json, subprocess, urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
REPOS = ['Vincentwei1021/mg-styles-15', 'francozanardi/papermotion']

def gh(*args):
    return json.loads(subprocess.check_output(['gh', 'api', *args], text=True, encoding='utf-8', timeout=40))

def fetch_one(job):
    url, target = job
    with urllib.request.urlopen(url, timeout=30) as r:
        raw = r.read(3_000_001)
    if len(raw) > 3_000_000:
        return {'path': str(target), 'error': 'text-size limit'}
    raw.decode('utf-8')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    return {'path': str(target), 'bytes': len(raw)}

for repo in REPOS:
    meta = gh('repos/' + repo)
    commit = gh('repos/' + repo + '/commits/' + meta['default_branch'])['sha']
    tree = gh('repos/' + repo + '/git/trees/' + commit + '?recursive=1')
    if tree.get('truncated'):
        raise RuntimeError('truncated tree: ' + repo)
    dest = ROOT / 'source-text' / repo.split('/')[-1]
    jobs = []
    for entry in tree['tree']:
        p = entry['path']
        if entry['type'] != 'blob' or p.startswith(('.github/', 'site/', 'videos/', 'node_modules/')):
            continue
        if Path(p).suffix.lower() not in ('.html', '.js', '.mjs', '.ts', '.tsx', '.py', '.md', '.json', '.glsl') and Path(p).name not in ('LICENSE', 'NOTICE'):
            continue
        if 'lock' in Path(p).name or entry.get('size', 0) > 3_000_000:
            continue
        jobs.append(('https://raw.githubusercontent.com/' + repo + '/' + commit + '/' + p, dest / p))
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(fetch_one, j): j for j in jobs}
        for f in concurrent.futures.as_completed(futures):
            try:
                results.append(f.result())
            except Exception as e:
                results.append({'path': str(futures[f][1]), 'error': str(e)})
    record = {'repository': repo, 'commit': commit, 'license': meta.get('license'), 'checked': '2026-10-09', 'scope': 'text retrieval only; no media or execution', 'files': results}
    dest.mkdir(parents=True, exist_ok=True)
    (dest / 'RESEARCH_SOURCE.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    print(repo, commit, 'text files', len(results), 'errors', sum('error' in x for x in results), flush=True)
