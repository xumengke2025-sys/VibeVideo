"""Read-only lightweight status, without starting PowerShell/CIM."""
from pathlib import Path
from datetime import datetime
import json

root = Path(__file__).resolve().parent
pipeline = json.loads((root / 'render/pipeline-status-v16.json').read_text(encoding='utf8'))
checkpoint = json.loads((root / 'CHECKPOINT-v16.json').read_text(encoding='utf8'))
progress = json.loads((root / 'render/frames-v16/render-progress.json').read_text(encoding='utf8'))
print(json.dumps({'frames': sum(p.name[:5].isdigit() and len(p.name) == 9 for p in (root / 'render/frames-v16').glob('*.png')),
                  'last': progress['last_frame'], 'stage': pipeline['stage'],
                  'checkpoint': checkpoint['status'], 'time': datetime.now().strftime('%H:%M:%S')}))
