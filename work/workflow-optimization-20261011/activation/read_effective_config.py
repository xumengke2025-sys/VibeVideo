"""Initialize a local protocol client and read config; no chats or model turns."""
import argparse, json, os, queue, subprocess, threading, time
from pathlib import Path

project = Path(__file__).resolve().parents[3]
parser = argparse.ArgumentParser()
parser.add_argument('--out', type=Path, default=Path(__file__).with_name('effective-config.json'))
parser.add_argument('--models', action='store_true', help='Also read the picker model catalog; no model invocation.')
args = parser.parse_args()
exe = Path('D:/npm-global/node_modules/@openai/codex/node_modules/@openai/codex-win32-x64/vendor/x86_64-pc-windows-msvc/bin/codex.exe')
proc = subprocess.Popen([str(exe), 'app-server'], cwd=project, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
messages = queue.Queue()
def read():
    for line in proc.stdout:
        try:
            messages.put(json.loads(line))
        except json.JSONDecodeError:
            pass
threading.Thread(target=read, daemon=True).start()
def send(value):
    proc.stdin.write(json.dumps(value) + '\n')
    proc.stdin.flush()
def response(id):
    end = time.monotonic() + 25
    while time.monotonic() < end:
        item = messages.get(timeout=max(.1, end - time.monotonic()))
        if item.get('id') == id:
            return item
    raise TimeoutError('Local app-server response timeout')
out = {'kind': 'read-only runtime configuration check; no thread created or model call'}
try:
    send({'id': 1, 'method': 'initialize', 'params': {'clientInfo': {'name': 'vibe_workflow_config_check', 'version': '1'}, 'capabilities': {'experimentalApi': True}}})
    init = response(1)
    out['initialize_ok'] = 'result' in init
    send({'method': 'initialized'})
    send({'id': 2, 'method': 'config/read', 'params': {'cwd': str(project), 'includeLayers': True}})
    result = response(2)
    if 'error' in result:
        out['error'] = {'code': result['error'].get('code'), 'message': result['error'].get('message')}
    else:
        data = result['result']
        config = data.get('config', {})
        out['effective'] = {k: config[k] for k in ('model', 'model_reasoning_effort', 'agents') if k in config}
        out['layers'] = []
        for layer in data.get('layers') or []:
            row = {k: layer[k] for k in ('name', 'origin', 'disabledReason', 'version') if k in layer}
            layer_config = layer.get('config') or {}
            row['model_and_agents'] = {k: layer_config[k] for k in ('model', 'model_reasoning_effort', 'agents') if k in layer_config}
            out['layers'].append(row)
        out['returned_fields'] = list(data)
    if args.models:
        catalog = []
        cursor = None
        for page in range(5):
            request_id = 3 + page
            send({'id': request_id, 'method': 'model/list', 'params': {'includeHidden': False, 'limit': 100, 'cursor': cursor}})
            reply = response(request_id)
            if 'error' in reply:
                out['model_list_error'] = reply['error']
                break
            payload = reply['result']
            for row in payload.get('data', []):
                catalog.append({key: row[key] for key in ('id', 'model', 'hidden', 'isDefault', 'supportedReasoningEfforts') if key in row})
            cursor = payload.get('nextCursor')
            if not cursor:
                break
        out['model_catalog'] = catalog
        out['model_catalog_next_cursor'] = cursor
        out['model_catalog_scope'] = 'Standalone local app-server catalog; not a UI reproduction or successful model invocation.'
finally:
    proc.stdin.close()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.terminate()
        proc.wait(timeout=5)
args.out.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(out, ensure_ascii=False))
