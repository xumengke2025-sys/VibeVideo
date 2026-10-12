"""Synthetic negative cases for evidence validation; never an actual AV review."""
from copy import deepcopy
from pathlib import Path
import importlib.util, json, tempfile

spec = importlib.util.spec_from_file_location('avcheck', 'D:/Codex/skills/vibe-video/scripts/check_av_review.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
results = []
with tempfile.TemporaryDirectory(prefix='vibe-av-consistency-') as folder:
    base = Path(folder)
    video, evidence, audio_evidence = base / 'synthetic-media.bin', base / 'synthetic-observation.png', base / 'synthetic-audio.wav'
    video.write_bytes(b'test-only-media')
    evidence.write_text('Synthetic test fixture, not a real observation.', encoding='utf-8')
    audio_evidence.write_text('Synthetic audio fixture, not heard.', encoding='utf-8')
    def observation(start, end, visual=True):
        file = evidence if visual else audio_evidence
        return {('start_frame' if visual else 'start'): start,
                ('end_frame' if visual else 'end'): end,
                'evidence': [str(file)], 'method': 'synthetic visual test' if visual else 'audio_input', 'observation': 'fixture only',
                'source_video_sha256': module.digest(video), 'evidence_sha256': {str(file): module.digest(file)}}
    valid = {'video_path': str(video), 'video_sha256': module.digest(video),
             'reviewer': {'mode': 'independent_agent', 'id': 'synthetic-fixture'},
             'coverage': {'decoded_frames': 10, 'visual_ranges': [observation(0, 9)],
                          'audio_listened_ranges_seconds': [observation(0, 1, False)], 'audio_status': 'complete',
                          'audio_perception': {'status': 'available', 'tool': 'synthetic fixture only'}},
             'findings': [], 'verdict': 'pass'}
    def trial(name, mutate, expected, audio=True, silent=False):
        review = deepcopy(valid)
        mutate(review)
        result = module.check(video, review, 10, 1.0, audio, silent)
        assert result['evidence_consistent'] == expected, (name, result)
        results.append({'case': name, 'passed': True, 'validator_accepts': expected, 'detected': result['errors']})
    trial('complete declared ranges', lambda r: None, True)
    trial('single missing frame', lambda r: r['coverage'].update(visual_ranges=[observation(0, 3), observation(5, 9)]), False)
    trial('overlap merges without false gap', lambda r: r['coverage'].update(visual_ranges=[observation(0, 5), observation(4, 9)]), True)
    trial('stale media hash', lambda r: r.update(video_sha256='0' * 64), False)
    trial('audio has small gap', lambda r: r['coverage'].update(audio_listened_ranges_seconds=[observation(0, .49, False), observation(.5, 1, False)]), False)
    trial('ASR without listening range', lambda r: r['coverage'].update(audio_listened_ranges_seconds=[]), False)
    trial('audio present marked inapplicable', lambda r: r['coverage'].update(audio_status='not_applicable'), False)
    trial('unresolved major', lambda r: r.update(findings=[{'severity': 'major', 'recheck_status': 'pending'}]), False)
    trial('resolved major', lambda r: r.update(findings=[{'severity': 'major', 'recheck_status': 'resolved'}]), True)
    trial('out of range frame', lambda r: r['coverage'].update(visual_ranges=[observation(0, 10)]), False)
    trial('missing evidence file', lambda r: r['coverage']['visual_ranges'][0].update(evidence=[str(base / 'missing.png')]), False)
    trial('count mismatch', lambda r: r['coverage'].update(decoded_frames=11), False)
    trial('honest incomplete is consistent', lambda r: (r.update(verdict='incomplete'), r['coverage'].update(visual_ranges=[], audio_listened_ranges_seconds=[], audio_status='pending')), True)
    trial('silent without brief authorization', lambda r: r['coverage'].update(audio_status='not_applicable', audio_listened_ranges_seconds=[]), False, audio=False)
    trial('intentional silent', lambda r: r['coverage'].update(audio_status='not_applicable', audio_listened_ranges_seconds=[]), True, audio=False, silent=True)
    trial('ASR-only falsely declared complete', lambda r: r['coverage']['audio_listened_ranges_seconds'][0].update(method='ASR transcription only; no listening tool'), False)
    trial('audio perception unavailable', lambda r: r['coverage'].update(audio_perception={'status': 'unavailable', 'tool': ''}), False)
    trial('old unrelated evidence binding', lambda r: r['coverage']['visual_ranges'][0].update(source_video_sha256='0' * 64), False)
    trial('changed evidence hash', lambda r: r['coverage']['visual_ranges'][0].update(evidence_sha256={str(evidence): '0' * 64}), False)
    text_file = base / 'old-unrelated.txt'
    text_file.write_text('Synthetic unrelated text', encoding='utf-8')
    trial('text evidence cannot be hearing', lambda r: r['coverage']['audio_listened_ranges_seconds'][0].update(evidence=[str(text_file)], evidence_sha256={str(text_file): module.digest(text_file)}), False)
out = Path(__file__).with_name('av-validator-tests.json')
out.write_text(json.dumps({'kind': 'synthetic validation tests, not video acceptance', 'cases': results}, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'{len(results)} meaningful consistency cases passed; no actual viewing/hearing was performed.')
