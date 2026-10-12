import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
INSTALLED = Path('D:/Codex/skills/vibe-video')
LOCAL = ROOT / 'skill/vibe-video'
NODE = 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
UV = 'C:/Users/67236/.local/bin/uv.exe'
CHECK = 'D:/Codex/skills/.system/skill-creator/scripts/quick_validate.py'
changed = ['SKILL.md', 'references/independent-av-review.md', 'references/review-performance.md',
           'scripts/review_batches.py', 'scripts/render_phase_timer.mjs', 'scripts/frame_audit.py']
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
result = {'skill_version': '0.14.0', 'sync': [], 'syntax': [], 'skill_validation': [], 'reference_errors': [],
          'new_movies_generated': False, 'models_changed': False}
for name in changed:
    a, b = INSTALLED / name, LOCAL / name
    result['sync'].append({'path': name, 'sha256': sha(a), 'equal': sha(a) == sha(b)})
    if a.suffix == '.py':
        compile(a.read_text(encoding='utf-8-sig'), str(a), 'exec')
        result['syntax'].append({'path': str(a), 'ok': True})
for name in ['work/matcha-morph-20261011/render.mjs', 'work/wastewater-isometric-20261011/render.mjs',
             'work/wastewater-isometric-20261011/js/main.js', 'work/napoleon-egypt-ink-20261009/revision-v3/render-v3.mjs',
             'work/napoleon-egypt-ink-20261009/revision-v3/film-v3.mjs',
             'work/napoleon-egypt-ink-20261009/revision-v3/vendor/claude-ink-comp.mjs',
             'skill/vibe-video/scripts/render_phase_timer.mjs']:
    p = ROOT / name
    check = subprocess.run([NODE, '--check', str(p)], capture_output=True, text=True, timeout=60)
    result['syntax'].append({'path': str(p), 'ok': check.returncode == 0, 'error': check.stderr[-1000:], 'sha256': sha(p)})
for folder in (INSTALLED, LOCAL):
    check = subprocess.run([UV, 'run', '--cache-dir', str(OUT / 'uv-cache'), '--with', 'pyyaml', 'python', '-X', 'utf8', CHECK, str(folder)],
                           capture_output=True, text=True, encoding='utf-8', timeout=120)
    result['skill_validation'].append({'path': str(folder), 'ok': check.returncode == 0, 'output': (check.stdout + check.stderr)[-1500:]})
for name in ['SKILL.md', 'references/independent-av-review.md', 'references/review-performance.md']:
    p = INSTALLED / name
    for link in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
        if not re.match(r'\w+://', link) and not (p.parent / link.split('#')[0]).exists():
            result['reference_errors'].append({'file': name, 'link': link})
independent = json.loads((OUT / 'independent-validation/latest-results.json').read_text(encoding='utf-8'))
result['independent_forward_test'] = {'passed': independent['passed'], 'total': independent['total'],
                                    'source_hashes_match': all(sha(p) == h for p, h in independent['tested_source_sha256'].items())}
result['ok'] = (all(x['equal'] for x in result['sync']) and all(x['ok'] for x in result['syntax'])
                and all(x['ok'] for x in result['skill_validation']) and not result['reference_errors']
                and result['independent_forward_test']['source_hashes_match'])
(OUT / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'ok': result['ok'], 'sync_files': len(result['sync']), 'syntax_checks': len(result['syntax']),
                  'independent_tests': result['independent_forward_test'], 'skill_validation': result['skill_validation']}, ensure_ascii=False))
raise SystemExit(0 if result['ok'] else 1)
