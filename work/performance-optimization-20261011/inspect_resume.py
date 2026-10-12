"""Read a bounded tail of existing production sessions; do not alter chat state."""
import json
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

OUT = Path(__file__).resolve().parent
BASE = OUT.parent / 'performance-diagnosis-20261011'
prior = json.loads((BASE / 'session-timings.json').read_text(encoding='utf-8'))
logs = Path('C:/Users/67236/.codex/sessions/2026/10/11')
targets = ['matcha-morph-20261011', 'wastewater-isometric-20261011', 'napoleon-egypt-ink-20261009']
result = {'snapshot_utc': datetime.now(timezone.utc).isoformat(), 'projects': []}
db = sqlite3.connect(Path('C:/Users/67236/.codex/state_5.sqlite').as_uri() + '?mode=ro', uri=True, timeout=5)
db.execute('PRAGMA query_only=ON')
for target in targets:
    candidates = [r for r in prior if r.get('source') == 'user' and list(r.get('project_tool_hits', {})) == [target]]
    if not candidates:
        result['projects'].append({'project': target, 'limitation': 'No unique parent session mapping'})
        continue
    selected = max(candidates, key=lambda r: r['project_tool_hits'][target])
    path = logs / selected['file']
    # Resuming/changing settings can roll over to a new transcript with the same thread ID.
    thread_id = selected['file'][-42:-6]
    state = db.execute('select rollout_path,model,reasoning_effort from threads where id=?', (thread_id,)).fetchone()
    if state:
        path = Path(state[0])
    with path.open('rb') as stream:
        stream.seek(max(0, path.stat().st_size - 2*1024*1024))
        raw = stream.read().decode('utf-8', errors='replace').splitlines()
    rows = []
    for line in raw:
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    entry = {'project': target, 'session_file': path.name, 'file_mtime_utc': datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
             'last_record': rows[-1].get('timestamp') if rows else None, 'recent_events': [], 'last_usage': None}
    if state:
        entry['selected_model'] = {'model': state[1], 'effort': state[2]}
    for row in rows:
        p = row.get('payload', {})
        kind = p.get('type', row.get('type'))
        if kind in ('task_started', 'task_complete', 'turn_aborted', 'function_call', 'custom_tool_call', 'function_call_output', 'custom_tool_call_output', 'compacted'):
            entry['recent_events'].append({'time': row.get('timestamp'), 'kind': kind, 'tool': p.get('name'), 'call_id': p.get('call_id')})
        elif kind == 'message' and p.get('role') in ('user', 'assistant'):
            text = '\n'.join(x.get('text', '') for x in p.get('content', []) if isinstance(x, dict))
            if p.get('channel') != 'analysis' and not text.startswith(('# AGENTS.md', '<environment', '<external')):
                entry['recent_events'].append({'time': row.get('timestamp'), 'kind': 'message', 'role': p.get('role'), 'channel': p.get('channel'), 'text': text[:320]})
        elif kind == 'token_count':
            entry['last_usage'] = {'time': row.get('timestamp'), 'usage': p.get('info', {}).get('last_token_usage')}
        elif row.get('type') == 'turn_context':
            entry['model'] = {k: p.get(k) for k in ('model', 'effort', 'reasoning_effort') if p.get(k)}
    entry['recent_events'] = entry['recent_events'][-12:]
    result['projects'].append(entry)
(OUT / 'resume-status.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
db.close()
