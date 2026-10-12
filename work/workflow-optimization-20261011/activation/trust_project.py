"""Add only the project's necessary trust entry; preserve user defaults."""
from pathlib import Path
import hashlib, json, os, shutil, tempfile, tomllib

project = Path(__file__).resolve().parents[3]
user_dir = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex')
config = user_dir / 'config.toml'
raw = config.read_bytes()
data = tomllib.loads(raw.decode('utf-8-sig'))
key = str(project.resolve()).lower()
existing = {k.lower(): v for k, v in data.get('projects', {}).items()}
if key in existing:
    assert existing[key].get('trust_level') == 'trusted', 'Existing project trust requires a scoped edit, not a duplicate table'
    print('Project already trusted; no user config change')
else:
    ending = '\r\n' if b'\r\n' in raw else '\n'
    suffix = ending + '# VibeVideo project configuration activation, 2026-10-11' + ending + "[projects.'" + key + "']" + ending + 'trust_level = "trusted"' + ending
    updated = raw + suffix.encode('utf-8')
    candidate = tomllib.loads(updated.decode('utf-8-sig'))
    assert candidate.get('model') == data.get('model')
    assert candidate.get('model_reasoning_effort') == data.get('model_reasoning_effort')
    assert candidate['projects'][key]['trust_level'] == 'trusted'
    backup = user_dir / 'config.toml.vibe-before-trust-20261011'
    if not backup.exists():
        shutil.copy2(config, backup)
    with tempfile.NamedTemporaryFile(dir=user_dir, delete=False, suffix='.tmp') as stream:
        temp = Path(stream.name)
        stream.write(updated)
    assert config.read_bytes() == raw, 'User config changed concurrently'
    os.replace(temp, config)
    result = {'change': 'one project trust entry only', 'project': key,
              'user_default_model_unchanged': True, 'user_default_effort_unchanged': True,
              'backup_path': str(backup), 'before_sha256': hashlib.sha256(raw).hexdigest(), 'after_sha256': hashlib.sha256(updated).hexdigest()}
    Path(__file__).with_name('trust-change.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))
