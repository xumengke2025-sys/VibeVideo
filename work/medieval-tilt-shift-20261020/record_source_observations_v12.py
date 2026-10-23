"""Record only the final-source stills actually inspected by the producer."""
from pathlib import Path
import datetime, hashlib, json

ROOT = Path(__file__).resolve().parent
manifest_path = ROOT / 'render/frozen-v12-manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf8'))
for name, expected in manifest['files'].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
observations = [
    (288, 'Blue glazed gate, royal statue, blue-clad shield guards and white-clad gift/fan bearers are readable in the focused middle area. The small scene conveys a diplomatic reception; it is an artistic interpretation.'),
    (528, 'Ten armed patrol members have a purposeful formation while civilians remain scattered around the market. Spears, shields and helmets distinguish the patrol from the surrounding residents.'),
    (744, 'Two groups of towmen are visible on the quay. Ropes connect toward colored cargo boats. Painted gunwales, loads, canopy and people aboard are visible. Foreground and far boats are intentionally blurred.'),
    (1176, 'White-robed priests and acolytes stand before distinct statues and offering vessels. The two principal statues face the forecourt; the narrow focus gives the architecture a miniature appearance.'),
    (1752, 'Citizens continue along the central avenue into the distance and across cross streets and bridges. The focused middle retains readable buildings and people; farther detail is progressively blurred.'),
]
report = {
    'created_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'producer': '/root', 'independent_review': False,
    'manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
    'frozen_inputs_verified': True,
    'method': 'Actual original-resolution visual inspection of five final-source PNGs; still inspection does not establish continuous action or whole-film temporal stability.',
    'frames': [
        {'frame': f, 'seconds': f / 24, 'path': str(ROOT / f'render/frames-v12/{f:05d}.png'),
         'sha256': hashlib.sha256((ROOT / f'render/frames-v12/{f:05d}.png').read_bytes()).hexdigest(),
         'observation': note} for f, note in observations
    ],
    'audio_perceived': False,
    'pending': ['Complete 1824-frame sequence', 'All-frame technical temporal scans', 'Encoded-film representative and continuous-window visual checks'],
}
(ROOT / 'qa/v12/final-source-still-observations.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
p = ROOT / 'CHECKPOINT.json'
d = json.loads(p.read_text(encoding='utf8'))
d['status'] = 'v12_full_rendering'
d['updated_at'] = report['created_at']
d['next_action'] = 'Continue the existing renderer; validate and assemble the full v12, then inspect the encoded output and deliver.'
d['v12_revision']['source_still_observations'] = 'qa/v12/final-source-still-observations.json'
d['v12_revision']['active_pipeline_pid'] = 26024
d['v12_revision']['actual_viewed_final_source_stills'] = [f for f, _ in observations]
p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')
print('Frozen inputs verified; five actually viewed final-source stills recorded.')
