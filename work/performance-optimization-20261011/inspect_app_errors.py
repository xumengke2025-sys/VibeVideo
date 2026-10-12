"""Inspect SQLite schemas read-only, then bounded project-scoped diagnostic logs."""
import json
from pathlib import Path
import sqlite3
from datetime import datetime, timezone
import re

base = Path('C:/Users/67236/.codex')
ids = ['01a1281a-0df8-7473-a697-489f61e2dccf', '01a1294e-2c8b-78b0-9771-95b2e949020e', '01a12958-186a-7ca3-8186-e232c238898d']
collected = {}
for file in ('state_5.sqlite', 'logs_2.sqlite'):
    con = sqlite3.connect((base / file).as_uri() + '?mode=ro', uri=True, timeout=5)
    con.execute('PRAGMA query_only=ON')
    names = [r[0] for r in con.execute("select name from sqlite_master where type='table'")]
    result = {'file': file, 'tables': {name: [r[1] for r in con.execute('pragma table_info("' + name.replace('"', '""') + '")')]
                                       for name in names if name in ('threads', 'logs')}}
    con.row_factory = sqlite3.Row
    if file.startswith('state'):
        collected['threads'] = [dict(r) for r in con.execute('select id,title,model,reasoning_effort,updated_at_ms,rollout_path,archived from threads where id in (?,?,?)', ids)]
    else:
        cutoff = int(datetime.fromisoformat('2026-10-11T08:24:00+00:00').timestamp())
        scoped = con.execute("select ts,level,target,thread_id,feedback_log_body from logs where ts >= ? and thread_id in (?,?,?) and level in ('WARN','ERROR') order by id desc limit 12", [cutoff, *ids])
        general = con.execute("select ts,level,target,thread_id,feedback_log_body from logs where ts >= ? and thread_id is null and level in ('WARN','ERROR') and target not like '%state_db%' and feedback_log_body not like '%rollout path%' order by id desc limit 4", [cutoff])
        collected['logs'] = []
        for row in list(scoped) + list(general):
            entry = dict(row)
            body = entry.pop('feedback_log_body') or ''
            # HTTP header dumps are neither needed nor safe diagnostic output.
            body = re.split(r'(?i)headers\s*[:=]', body, maxsplit=1)[0]
            body = re.sub(r'(?im)^.*(?:authorization|set-cookie|cookie|__cf_bm|api[_-]?key).*$','[secret-bearing line omitted]', body)
            body = re.sub(r'(?i)bearer\s+\S+', 'Bearer [redacted]', body)
            body = re.sub(r'https?://[^\s]+', '[URL omitted]', body)
            entry['body_excerpt'] = body[-700:]
            collected['logs'].append(entry)
    con.close()
destination = Path(__file__).resolve().parent / 'resume-app-errors.json'
destination.write_text(json.dumps(collected, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'logs': [r for r in collected.get('logs', []) if r['target'] == 'codex_core::responses_retry']}, ensure_ascii=False))
