from pathlib import Path
import json, hashlib, shutil

R = Path(__file__).resolve().parent
B = R.parent
camera = lambda s: s[s.index('const keys='):s.index('function pathPoint')]
previous = camera((B/'v12/scene-body.js').read_text(encoding='utf-8'))
current = camera((R/'scene-body.js').read_text(encoding='utf-8'))
assert previous == current
assert (R/'audio/mix.wav').read_bytes() == (B/'v12/audio/mix.wav').read_bytes()
motion = json.loads((B/'out/motion-v12.json').read_text(encoding='utf-8'))
motion['reuse_provenance'] = {
    'source': 'out/motion-v12.json',
    'reason': 'V13 camera code identical to V12; narrative text changed only.',
    'camera_sha256': hashlib.sha256(current.encode()).hexdigest(),
    'new_perceptual_review': False,
}
(B/'out/motion-v13.json').write_text(json.dumps(motion,ensure_ascii=False,indent=2),encoding='utf-8')
stills=B/'out/stills-v13-business-first-check'
checks=json.loads((stills/'checks.json').read_text(encoding='utf-8'))
assert not checks['errors'] and all(s['identical'] for s in checks['seeks'])
dest=B/'concepts/v13'
dest.mkdir(exist_ok=True,parents=True)
for f in stills.glob('*.png'): shutil.copy2(f,dest/f.name)
shutil.copy2(stills/'checks.json',dest/'checks.json')
print(json.dumps({'camera_identical':True,'audio_identical':True,'deterministic_seeks':len(checks['seeks']),'concept_frames':len(list(dest.glob('*.png')))}))
