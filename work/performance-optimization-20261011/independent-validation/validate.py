"""Bounded independent forward test. Text fixtures are not actual media."""
from pathlib import Path
import sys
import copy
from datetime import datetime, timezone

sys.path.insert(0, 'D:/Codex/skills/vibe-video/scripts')
import review_batches as rb
from check_av_review import digest

ROOT = Path(__file__).resolve().parent
RUN = ROOT / ('run-' + datetime.now(timezone.utc).strftime('%H%M%S%f'))
RUN.mkdir()
results = []


def record(case, actual, expected):
    results.append(dict(case=case, actual=actual, expected=expected, passed=actual == expected))


def rejected(call):
    try:
        call()
        return False
    except ValueError:
        return True


v, s, a = [RUN / name for name in ('fixture.mp4', 'fixture.jpg', 'fixture.wav')]
for path in (v, s, a):
    path.write_text('TEXTUAL SYNTHETIC FIXTURE; NOT DECODABLE MEDIA; NO PERCEPTION CLAIM.', encoding='utf-8')
h = digest(v)
index = RUN / 'index.json'
rb.write(index, {'sha256': h, 'count': 6, 'sheets': [dict(start=0, end=5, path=str(s), sha256=digest(s))]})
packet = rb.prepare(v, index, RUN / 'packet', 6, 6, True, batch_frames=3, repair_round=1)
pp = RUN / 'packet/packet.json'


def report(batch, start, end, reviewer):
    return dict(video_path=str(v), video_sha256=h, reviewer=dict(id=reviewer), batch_id=batch,
                coverage=dict(decoded_frames=6, visual_ranges=[dict(start_frame=start, end_frame=end,
                    evidence=[str(s)], evidence_sha256={str(s): digest(s)}, source_video_sha256=h,
                    method='synthetic_visual_declaration', observation='Synthetic declaration only; not actual perception')],
                    audio_listened_ranges_seconds=[], audio_status='pending'), findings=[], verdict='incomplete')


r1, r2 = RUN / 'r1.json', RUN / 'r2.json'
rb.write(r1, report(packet['batches'][0]['id'], 0, 2, 'fixture-observer-1'))
rb.write(r2, report(packet['batches'][1]['id'], 3, 5, 'fixture-observer-2'))
t0, t1, t11, t12, t13, t60 = ['2026-10-11T' + t + '+00:00' for t in ('00:00:00', '00:01:00', '00:11:00', '00:12:00', '00:13:00', '01:00:00')]
state = rb.merge(pp, [], RUN / 'unobserved', run_started_at=t0, at=t0)
record('export_is_pending', state['visual_gaps'], [[0, 5]])
state = rb.merge(pp, [r1], RUN / 'coverage', at=t0)
record('partial_visual_gaps', state['visual_gaps'], [[3, 5]])
state = rb.merge(pp, [r1, r2], RUN / 'coverage', at=t1)
record('full_visual_does_not_grant_AV_pass', [state['visual_gaps'], state['audio_gaps'], state['delivery_verdict']], [[], [[0, 6]], 'incomplete'])
record('accepted_reports_cannot_be_dropped', rejected(lambda: rb.merge(pp, [r1], RUN / 'coverage', at=t11)), True)
record('repair_round_preserved', rb.read(RUN / 'coverage/av-review.json')['repair_round'], 1)
bad = rb.read(r1)
bad['video_sha256'] = '0' * 64
badp = RUN / 'bad-hash.json'
rb.write(badp, bad)
record('wrong_hash_rejected', rejected(lambda: rb.merge(pp, [badp], RUN / 'bad-hash')), True)
bad = rb.read(r1)
bad['coverage']['visual_ranges'][0]['end_frame'] = 5
rb.write(badp, bad)
record('out_of_batch_coverage_rejected', rejected(lambda: rb.merge(pp, [badp], RUN / 'bad-boundary')), True)
out = RUN / 'pause'
rb.merge(pp, [r1], out, run_started_at=t0, at=t0)
state = rb.merge(pp, [r1], out, paused=True, at=t1)
record('paused_no_delivery', state['delivery_due'], False)
state = rb.merge(pp, [r1], out, at=t60)
record('paused_without_explicit_resume_stays_paused', [state['paused'], state['delivery_due']], [True, False])
# Explicitly restore pause for old code so remaining checks stay meaningful.
rb.merge(pp, [r1], out, paused=True, at=t60)
state = rb.merge(pp, [r1], out, run_started_at=t60, at=t60)
record('resume_starts_fresh_wait', [state['delivery_due'], state['no_progress_minutes']], [False, 0])
record('active_cannot_restart_clock', rejected(lambda: rb.merge(pp, [r1], out, run_started_at='2026-10-11T02:00:00+00:00', at='2026-10-11T02:00:00+00:00')), True)
out = RUN / 'repeat'
rb.merge(pp, [r1, r2], out, run_started_at=t0, at=t0)
state = rb.merge(pp, [r1, r2], out, at=t11)
record('poll_no_reset', state['delivery_due'], True)
state = rb.merge(pp, [r2, r1], out, at=t12)
record('reorder_no_reset', state['delivery_due'], True)
state = rb.merge(pp, [r2, r1, r1], out, at=t13)
record('duplicate_report_no_reset', state['delivery_due'], True)
false = rb.read(r1)
false['coverage']['audio_listened_ranges_seconds'] = [dict(start=0, end=6, evidence=[str(a)],
    evidence_sha256={str(a): digest(a)}, source_video_sha256=h, method='waveform', observation='Synthetic declaration only')]
falsep = RUN / 'false-audio.json'
rb.write(falsep, false)
record('waveform_not_hearing', rejected(lambda: rb.merge(pp, [falsep], RUN / 'false-audio')), True)
false['coverage']['audio_listened_ranges_seconds'][0]['method'] = 'audio_input'
false['coverage']['audio_perception'] = {'status': 'available'}
rb.write(falsep, false)
try:
    rb.merge(pp, [falsep], RUN / 'missing-tool')
    actual = rb.read(RUN / 'missing-tool/av-review.json')['coverage']['audio_status']
except ValueError:
    actual = 'rejected'
record('missing_audio_tool_cannot_count_complete', actual in ('pending', 'rejected'), True)
rb.write(RUN / 'results.json', dict(scope='Textual isolated fixtures; no real media generated, decoded, watched or heard.', results=results))
rb.write(ROOT / 'latest-results.json', dict(run_directory=str(RUN), passed=sum(x['passed'] for x in results), total=len(results), results=results))
print(str(RUN))
for result in results:
    print(('PASS ' if result['passed'] else 'FAIL ') + result['case'] + ': ' + str(result['actual']))
