"""Read project-related session evidence; summarize timings without copying prompts."""
import json, re
from pathlib import Path
from datetime import datetime
from collections import Counter

root = Path(__file__).resolve().parent
logs = Path('C:/Users/67236/.codex/sessions/2026/10/11')
targets = ['matcha-morph-20261011', 'wastewater-isometric-20261011', 'napoleon-egypt-ink-20261009']
results = []
for path in sorted(logs.glob('*.jsonl')):
    rows = []
    with path.open(encoding='utf-8') as f:
        for line in f:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    if not rows:
        continue
    meta = rows[0].get('payload', {})
    if 'VibeVideo' not in meta.get('cwd', ''):
        continue
    calls = {}
    completed = []
    markers = []
    roles = []
    models = []
    events = Counter()
    for row in rows:
        p = row.get('payload', {})
        kind = p.get('type', row.get('type'))
        ts = row.get('timestamp', '')
        events[kind] += 1
        if row.get('type') == 'turn_context':
            choice = {k: p.get(k) for k in ('model', 'effort', 'reasoning_effort') if p.get(k)}
            if choice not in models:
                models.append(choice)
        if kind in ('function_call', 'custom_tool_call'):
            args = p.get('arguments', p.get('input', ''))
            projects = [x for x in targets if x in args]
            tag = p.get('name', '')
            for word in ('imagegen', 'render', 'frame_audit', 'view_image', 'inspect_local_file', 'wait_agent', 'spawn_agent', 'audio', 'ffmpeg'):
                if word in args:
                    tag += ':' + word
            calls[p.get('call_id')] = {'start': ts, 'tool': tag, 'projects': projects}
        elif kind in ('function_call_output', 'custom_tool_call_output'):
            call = calls.get(p.get('call_id'))
            if call:
                result = dict(call, end=ts)
                result['elapsed_seconds'] = round((datetime.fromisoformat(ts.replace('Z', '+00:00')) - datetime.fromisoformat(call['start'].replace('Z', '+00:00'))).total_seconds(), 3)
                text = str(p.get('output', ''))
                match = re.search(r'Wall time:\s*([\d.]+)', text)
                if match:
                    result['reported_wall_seconds'] = float(match.group(1))
                # Output flags only, never echo raw command text or credentials.
                result['flags'] = [x for x in ('Script running', 'session_id', 'exit_code', 'timeout', 'Error', 'COMPLETE', 'incomplete') if x in text]
                completed.append(result)
        elif kind == 'message':
            role = p.get('role')
            content = p.get('content', [])
            text = '\n'.join(x.get('text', '') for x in content if isinstance(x, dict))
            if role == 'assistant':
                markers.append({'time': ts, 'channel': p.get('channel'), 'text': text[:360]})
            if role == 'user' and not text.startswith(('# AGENTS.md', '<environment', '<external')):
                roles.append({'time': ts, 'text': text[:240]})
    project_hits = Counter(x for row in rows if row.get('payload', {}).get('type') in ('function_call', 'custom_tool_call') for x in targets if x in row['payload'].get('arguments', row['payload'].get('input', '')))
    results.append({'file': path.name, 'source': meta.get('thread_source'), 'first': rows[0]['timestamp'], 'last': rows[-1]['timestamp'], 'project_tool_hits': dict(project_hits), 'models': models, 'events': dict(events), 'last_user_messages': roles[-3:], 'last_updates': markers[-5:], 'slowest_calls': sorted(completed, key=lambda x: x['elapsed_seconds'], reverse=True)[:12], 'project_calls': [x for x in completed if x['projects']], 'pending_calls': [x for k, x in calls.items() if not any(c.get('start') == x['start'] and c.get('tool') == x['tool'] for c in completed)]})
(root / 'session-timings.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
for row in results:
    if row['project_tool_hits']:
        compact = {k: row[k] for k in ('file', 'source', 'last', 'project_tool_hits', 'models', 'last_user_messages', 'last_updates', 'slowest_calls')}
        print(json.dumps(compact, ensure_ascii=False))
