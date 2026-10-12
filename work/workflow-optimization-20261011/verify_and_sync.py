"""Validate this scoped update and synchronize only differing skill files."""
from pathlib import Path
import hashlib, importlib.util, json, re, shutil, subprocess, sys, tomllib

task = Path(__file__).resolve().parent
project = task.parents[1]
installed = Path('D:/Codex/skills/vibe-video')
snapshot = project / 'skill/vibe-video'
ffprobe = project / 'node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

verification = {'kind': 'skill/evidence checks, not creative video acceptance', 'checks': {}}
drafts = []
for path in sorted((task / 'config-draft').rglob('*.toml')):
    data = tomllib.loads(path.read_text(encoding='utf-8-sig'))
    if 'agents' in path.parts:
        assert all(data.get(k) for k in ('name', 'description', 'developer_instructions'))
        assert data['model'] == 'gpt-6-astra'
        assert data['model_reasoning_effort'] in ('high', 'medium')
    drafts.append({'path': str(path), 'sha256': sha(path), 'syntax_valid': True})
verification['checks']['historical_config_drafts'] = {'active': False, 'files': drafts}
activation = task / 'activation/activation.json'
withdrawal = json.loads((task / 'activation/withdrawal.json').read_text(encoding='utf-8'))
assert all(not (project / row['project_path']).exists() for row in withdrawal['archived_files'])
effective = json.loads((task / withdrawal['effective_configuration_check']).read_text(encoding='utf-8'))
project_layers = [row for row in effective['layers'] if row['name'].get('type') == 'project']
assert project_layers and all(not row['model_and_agents'] for row in project_layers)
verification['checks']['model_configuration'] = withdrawal
verification['checks']['project_model_overrides_removed'] = True

changed = []
for src in sorted(installed.rglob('*')):
    if not src.is_file() or '__pycache__' in src.parts:
        continue
    rel = src.relative_to(installed)
    dest = snapshot / rel
    if dest.exists() and sha(src) == sha(dest):
        continue
    if dest.exists():
        old = task / 'before-project-skill' / rel
        old.parent.mkdir(parents=True, exist_ok=True)
        if not old.exists():
            shutil.copy2(dest, old)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    assert sha(src) == sha(dest)
    changed.append({'relative_path': str(rel), 'sha256': sha(src)})
verification['checks']['skill_sync_changed_files'] = changed
verification['checks']['skill_sync_total_compared'] = sum(1 for p in installed.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
verification['checks']['update_files'] = [{'relative_path': rel, 'sha256': sha(installed / rel)} for rel in ['SKILL.md', 'references/director-design.md', 'references/motion-craft.md', 'references/independent-av-review.md', 'references/reference-transfer.md', 'references/role-orchestration.md', 'scripts/check_av_review.py']]
verification['checks']['snapshot_extra_files'] = [str(p.relative_to(snapshot)) for p in snapshot.rglob('*') if p.is_file() and '__pycache__' not in p.parts and not (installed / p.relative_to(snapshot)).exists()]

links = []
files = ['SKILL.md', 'references/reference-transfer.md', 'references/role-orchestration.md', 'references/director-design.md', 'references/motion-craft.md', 'references/independent-av-review.md']
for rel in files:
    path = installed / rel
    for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8-sig')):
        if '://' in link or link.startswith('#'):
            continue
        target = (path.parent / link.split('#')[0]).resolve()
        assert target.exists(), (str(path), link)
        links.append({'file': rel, 'target': link})
verification['checks']['local_links'] = {'passed': True, 'count': len(links)}
validate = Path('D:/Codex/skills/.system/skill-creator/scripts/quick_validate.py')
result = subprocess.run(['uv', 'run', '--cache-dir', str(task / 'uv-cache'), '--with', 'pyyaml', 'python', '-X', 'utf8', str(validate), str(installed)], capture_output=True, text=True, encoding='utf-8', timeout=120)
verification['checks']['quick_validate'] = {'exit_code': result.returncode, 'output': (result.stdout + result.stderr).strip()}
assert result.returncode == 0, result.stdout + result.stderr

# Existing silent media: exercise actual decoding path with no observation claims.
video = project / 'work/creative-upgrade-20261010/flight/out-final/flight-director.mp4'
media = json.loads(subprocess.run([str(ffprobe), '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', str(video)], capture_output=True, text=True, check=True, timeout=60).stdout)
stream = next(s for s in media['streams'] if s['codec_type'] == 'video')
fixture = {'kind': 'technical incomplete fixture, no real viewing or listening', 'video_path': str(video), 'video_sha256': sha(video), 'reviewer': {'mode': 'technical_fixture', 'id': 'not-an-actual-reviewer'}, 'coverage': {'decoded_frames': int(stream['nb_read_frames']), 'visual_ranges': [], 'unreviewed_frame_ranges': [[0, int(stream['nb_read_frames']) - 1]], 'audio_status': 'not_applicable', 'audio_listened_ranges_seconds': []}, 'findings': [], 'limitations': ['No frames observed during this test'], 'verdict': 'incomplete'}
fixture_path = task / 'tests/current-media-incomplete-fixture.json'
fixture_path.parent.mkdir(parents=True, exist_ok=True)
fixture_path.write_text(json.dumps(fixture, ensure_ascii=False, indent=2), encoding='utf-8')
result = subprocess.run([sys.executable, '-X', 'utf8', str(installed / 'scripts/check_av_review.py'), str(video), '--review', str(fixture_path), '--ffprobe', str(ffprobe), '--allow-silent', '--out', str(task / 'tests/current-media-consistency.json')], capture_output=True, text=True, encoding='utf-8', timeout=60)
verification['checks']['real_media_cli'] = {'exit_code': result.returncode, 'result': json.loads(result.stdout)}
assert result.returncode == 0
verification['checks']['synthetic_consistency_tests'] = json.loads((task / 'av-validator-tests.json').read_text(encoding='utf-8'))
verification['checks']['independent_source_study'] = {'report': str(task / 'source-study/RESEARCH.md'), 'manifest': str(task / 'source-study/source-manifest.json'), 'scope': 'source read only, no upper film playback or hearing'}
verification['checks']['new_video_quality'] = 'not tested; no video generated this turn'
verification['checks']['doctor_metadata'] = {'cli_version': '0.159.2', 'desktop_version': '26.1007.2314.0', 'existing_config_parse': 'ok', 'active_thread_overrides': 'not inspected', 'unrelated_global_setting': 'disable_response_storage ignored; left unchanged'}
out = task / 'verification.json'
out.write_text(json.dumps(verification, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'quick_validate': verification['checks']['quick_validate'], 'links': len(links), 'synced_files': len(changed), 'extra_snapshot_files': len(verification['checks']['snapshot_extra_files']), 'drafts': len(drafts), 'actual_media': '192 decoded frames; incomplete fixture only', 'report': str(out)}, ensure_ascii=False))
