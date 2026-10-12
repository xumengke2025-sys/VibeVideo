"""Exercise local retrieval and preserve bounded verification evidence."""
import json
import subprocess
import sys
from pathlib import Path

SKILL = Path('D:/Codex/skills/vibe-video')
OUT = Path(__file__).resolve().parent
CLI = SKILL / 'scripts/opus_methodology.py'
results = {}

def run(label, *args, expected=0):
    proc = subprocess.run([sys.executable, '-X', 'utf8', str(CLI), *args],
                          capture_output=True, text=True, encoding='utf-8', timeout=30)
    assert proc.returncode == expected, (label, proc.returncode, proc.stderr)
    result = json.loads(proc.stdout) if proc.returncode == 0 else {'error': proc.stderr.strip()}
    results[label] = {'args': list(args), 'exit_code': proc.returncode, 'output': result}
    return result

v = run('validate', 'validate')
assert v['ok'] and v['cards'] == 35 and v['indexed_rows'] == 513 and v['source_hashes_checked'] == 688
s = run('stats', 'stats')
assert len(s['local_archives']) == 10 and len(s['source_read_only']) == 9
assert all(s['reference_roles'][sid] == 'component' for sid in ('water','rigid','clearwater'))
mechanical = run('mechanical_query', 'recommend', '--query', '竖屏 弹簧止回阀 剖面 流体', '--limit', '4')
assert mechanical['cards'][0]['id'] == 'mechanical-section'
assert mechanical['cards'][0]['status'] == 'design_inference_from_public_brief'
assert not mechanical['cards'][0]['sources']
code = run('code_query', 'recommend', '--query', '点云 长焦 运镜 水流 碰撞', '--code-only', '--limit', '8')
assert code['cards'] and all(c['sources'] for c in code['cards'])
index = json.loads((SKILL / 'references/opus-source-index.json').read_text(encoding='utf-8'))
rows = {r['slug']: r for r in index['entries']}
for card in code['cards']:
    for case in card['reference_leads']:
        row = rows[case['slug']]
        assert row['source_id'] and row['original_visual_provenance'] not in (
            'generated_video_required_in_prompt', 'generated_image_required_in_prompt', 'video_asset_origin_unknown')
unknown = run('unknown_query', 'recommend', '--query', 'zzzzunknownrequest9876')
assert unknown['cards'] == [] and unknown['unresolved']
card = run('morph_card', 'card', 'outline-morph')
assert len(card['source_details']) == 2
for ref in card['source_details']:
    assert Path(ref['local']).is_file() and '#L' + str(ref['line']) in ref['url']
for sid in s['local_archives']:
    src = run('source_' + sid, 'source', sid)
    assert Path(src['local']).is_absolute() and (Path(src['local']) / 'SOURCE.json').is_file()
    assert src['commit_date'].endswith('Z') and src['quality_evidence']
film = run('film_query', 'recommend', '--query', '产品 全息 标注 摄影 水面 焦散 流体', '--code-only', '--film-only', '--limit', '8')
assert any(c['id'] == 'world-anchor-callout' for c in film['cards'])
assert all(any(r['reference_role'] in ('film','film_engine') for r in c['sources']) for c in film['cards'])
assert all(c['id'] not in ('shallow-water','gpu-rigid','refracted-caustic-grid') for c in film['cards'])
for cid in ('performance-handoff','world-anchor-callout','curved-page-handoff','refracted-caustic-grid'):
    c = run('new_card_' + cid, 'card', cid)
    assert c['gallery_slugs'] == []
    for ref in c['source_details']:
        assert Path(ref['local']).is_file() and ref['quality_evidence'] == 'source_inspected_video_unreviewed'
trace = run('mixed_provenance', 'trace', 'koldo2k-778767')
assert trace['original_visual_provenance'] == 'generated_video_required_in_prompt'
assert trace['source'] is None and not trace['pixel_match_verified']
run('invalid_card', 'card', 'does-not-exist', expected=2)

# Check document routes changed in this iteration, including directory links.
import re
for rel in ('SKILL.md', 'references/opus-methodology.md', 'references/opus-gallery.md', 'references/code-cinema.md','references/recent-film-selection.md'):
    path = SKILL / rel
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
        if '://' in target or target.startswith('#'):
            continue
        assert (path.parent / target.split('#')[0]).exists(), (rel, target)

(OUT / 'retrieval-verification.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
summary = {'ok': True, 'commands_exercised': len(results), **v,
           'local_source_roots': 10, 'new_upstream_files': 231,
           'new_archives_runtime_verified': False, 'new_video_rendered': False,
           'checks': ['CLI errors and unknown query', 'Chinese requirement matching',
                      'code-only source provenance', 'mixed-source trace',
                      'absolute source paths and line anchors', 'relative documentation links',
                      'film-only filtering and source role/quality/date evidence']}
(OUT / 'verification-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
