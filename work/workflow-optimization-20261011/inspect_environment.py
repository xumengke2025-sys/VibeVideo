"""Read only configuration metadata; never print credentials or MCP values."""
from pathlib import Path
import json, os, tomllib

root = Path(__file__).resolve().parents[2]
codex_dir = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex')
paths = [codex_dir / 'config.toml', root / '.codex/config.toml']
result = {'project': str(root), 'config_layers': [], 'custom_agents': []}
for path in paths:
    item = {'path': str(path), 'exists': path.exists()}
    if path.exists():
        data = tomllib.loads(path.read_text(encoding='utf-8-sig'))
        item['model_settings'] = {k: data[k] for k in ('model', 'model_reasoning_effort') if k in data}
        item['agent_settings'] = {k: v for k, v in data.get('agents', {}).items() if k in ('enabled', 'max_concurrent_threads_per_session', 'max_threads', 'default_subagent_model', 'default_subagent_reasoning_effort')}
        item['project_trust'] = [v.get('trust_level') for k, v in data.get('projects', {}).items() if Path(k).resolve() == root]
    result['config_layers'].append(item)
for folder in (codex_dir / 'agents', root / '.codex/agents'):
    for path in sorted(folder.glob('*.toml')):
        data = tomllib.loads(path.read_text(encoding='utf-8-sig'))
        result['custom_agents'].append({'path': str(path), **{k: data[k] for k in ('name', 'model', 'model_reasoning_effort') if k in data}})
out = Path(__file__).with_name('environment.json')
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
