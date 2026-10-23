"""Bounded functional checks; fixtures are not delivered media or review evidence."""
from pathlib import Path
from types import SimpleNamespace as Args
import json
import tempfile

from PIL import Image
import shot_cache as cache

ROOT = Path(__file__).resolve().parent
QA = ROOT / 'qa/incremental-cache'
QA.mkdir(parents=True, exist_ok=True)
index = QA / 'baseline-v13.json'
timeline = cache.read(ROOT / 'v13-timeline.json')
if not index.exists():
    cache.register(Args(report=ROOT / 'delivery/engineering-check-v13.json',
                        frames=ROOT / 'render/frames-v13',
                        cuts=','.join(str(shot[0]) for shot in timeline['shots'][1:]), out=index))
cache.plan(Args(baseline=index, audio_only=True, shots=None, global_visual=False,
                handles=2, reason='Verify audio-only change reuses all existing picture frames',
                out=QA / 'audio-only-v13.json'))
actual = cache.read(QA / 'audio-only-v13.json')
assert actual['render_frames'] == [] and len(actual['reuse_frames']) == 1824
checks = ['real complete v13 registered with 1824 per-frame hashes', 'audio-only plan requests zero 3D frames']
with tempfile.TemporaryDirectory(prefix='fixture-', dir=QA) as folder:
    temp = Path(folder).resolve()
    assert temp.is_relative_to(QA.resolve())
    original, patches = temp / 'original', temp / 'patches'
    original.mkdir(); patches.mkdir()
    for i in range(10):
        Image.new('RGB', (8, 8), (i * 20, 20, 30)).save(original / f'{i:05d}.png')
        Image.new('RGB', (8, 8), (i * 20, 150, 30)).save(patches / f'{i:05d}.png')
    fixture = {'frames_dir': str(original), 'frames': 10, 'width': 8, 'height': 8,
               'shots': [{'id': 0, 'start': 0, 'end': 3}, {'id': 1, 'start': 3, 'end': 7},
                         {'id': 2, 'start': 7, 'end': 10}],
               'frame_sha256': [cache.digest(original / f'{i:05d}.png') for i in range(10)]}
    baseline = temp / 'baseline.json'
    cache.write(baseline, fixture)
    plan = temp / 'plan.json'
    cache.plan(Args(baseline=baseline, audio_only=False, shots='1', global_visual=False,
                    handles=1, reason='Labeled fixture: one changed shot', out=plan))
    result = cache.read(plan)
    assert result['render_frames'] == list(range(2, 8))
    assert result['reuse_frames'] == [0, 1, 8, 9]
    cache.materialize(Args(plan=plan, patches=patches, out=temp / 'staged'))
    for i in range(10):
        expected = (patches if 2 <= i < 8 else original) / f'{i:05d}.png'
        assert cache.digest(temp / 'staged' / expected.name) == cache.digest(expected)
    checks += ['local shot plus boundary handles only', 'assembled frames use correct baseline or patch hashes']
    (patches / '00002.png').unlink()
    try:
        cache.materialize(Args(plan=plan, patches=patches, out=temp / 'missing-patch'))
    except AssertionError as error:
        assert 'Missing frame 2' in str(error)
    else:
        raise AssertionError('Missing patch was accepted')
    assert not (temp / 'missing-patch').exists()
    checks.append('missing replacement frame rejected before staging')
    Image.new('RGB', (8, 8), 'red').save(original / '00000.png')
    try:
        cache.materialize(Args(plan=plan, patches=patches, out=temp / 'tampered'))
    except AssertionError as error:
        assert 'Reusable frame 0 changed' in str(error)
    else:
        raise AssertionError('Changed reusable frame was accepted')
    checks.append('tampered baseline frame rejected')
cache.write(QA / 'verification.json', {'passed': checks,
                                      'v16_baseline_ready': False,
                                      'visual_scope_solver': False,
                                      'actual_listening': False,
                                      'remux_audio_executed': False})
print(json.dumps({'passed_checks': len(checks), 'evidence': str(QA / 'verification.json')}))
