"""Prepare bounded review packets and merge actual reports; never infer perception."""
from __future__ import annotations
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from check_av_review import check, digest, gaps


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(path)


def now():
    return datetime.now(timezone.utc).isoformat()


def sheets(index_path, video_hash, frames):
    """Accept explicit ranges, or the known 30-frame frame_audit atlas layout."""
    source = read(index_path)
    base = Path(index_path).resolve().parent
    if source.get('video_sha256', source.get('sha256')) != video_hash:
        raise ValueError('Evidence index hash differs from current video')
    if source.get('source_frame_count', source.get('count')) != frames:
        raise ValueError('Evidence index frame count differs from current media')
    if 'sheets' in source:
        rows = source['sheets']
    else:
        entries = source['frames']
        if [e['frame'] for e in entries] != list(range(frames)):
            raise ValueError('Partial or non-contiguous frame index cannot cover the film')
        per_page = source.get('atlas_frames_per_page', 30)
        if len(source['atlases']) != (frames + per_page - 1) // per_page:
            raise ValueError('Unknown atlas layout; provide explicit sheet ranges')
        rows = [{'start': i * per_page, 'end': min(frames - 1, (i + 1) * per_page - 1),
                 'path': p} for i, p in enumerate(source['atlases'])]
        for entry in entries:
            if not (base / entry['image']).is_file():
                raise ValueError('Missing decoded frame: ' + entry['image'])
    normalized = []
    for row in rows:
        start, end = row['start'], row['end']
        if type(start) is not int or type(end) is not int or not 0 <= start <= end < frames:
            raise ValueError('Invalid sheet range')
        path = Path(row['path'])
        path = path if path.is_absolute() else base / path
        path = path.resolve()
        actual = digest(path)
        if row.get('sha256') and row['sha256'] != actual:
            raise ValueError('Changed evidence sheet: ' + str(path))
        normalized.append({'start': start, 'end': end, 'path': str(path), 'sha256': actual})
    if gaps([(r['start'], r['end']) for r in normalized], frames, True):
        raise ValueError('Evidence sheets leave frame gaps')
    return normalized, source


def prepare(video, index, out, frames, duration, has_audio, batch_frames=150,
            repair_round=0, brief=(), no_progress_minutes=10):
    video, index, out = Path(video).resolve(), Path(index).resolve(), Path(out).resolve()
    if frames <= 0 or duration <= 0 or batch_frames <= 0 or no_progress_minutes <= 0:
        raise ValueError('Positive media, batch and deadline values required')
    if repair_round not in (0, 1, 2):
        raise ValueError('Preserve the existing repair round (0..2); never reset it')
    sha = digest(video)
    pages, source = sheets(index, sha, frames)
    packet_path = out / 'packet.json'
    if packet_path.exists():
        raise ValueError('Use a new packet directory; existing review records are immutable inputs')
    batches = []
    for start in range(0, frames, batch_frames):
        end = min(frames - 1, start + batch_frames - 1)
        relevant = [p for p in pages if p['end'] >= max(0, start - 1) and p['start'] <= min(frames - 1, end + 1)]
        batch = {'id': f'{start:06d}-{end:06d}', 'assigned_range': [start, end],
                 'boundary_range': [max(0, start - 1), min(frames - 1, end + 1)], 'sheets': relevant}
        batches.append(batch)
        write(out / ('batch-' + batch['id'] + '.json'), batch)
    brief_paths = [str(Path(p).resolve()) for p in brief]
    if any(not Path(p).is_file() for p in brief_paths):
        raise ValueError('Brief input missing')
    packet = {'created_at': now(), 'video_path': str(video), 'video_sha256': sha,
              'decoded_frames': frames, 'duration_seconds': duration, 'has_audio': has_audio,
              'repair_round': repair_round, 'index_path': str(index), 'index_sha256': digest(index),
              'decoded_frame_directory': source.get('decoded_dir', str(index.parent / 'frames')),
              'audio_path': source.get('audio', str(video)), 'brief_after_blind': brief_paths,
              'no_progress_minutes': no_progress_minutes, 'batches': batches,
              'coverage_status': 'pending', 'note': 'Exported files are not observed coverage.'}
    write(packet_path, packet)
    (out / 'REVIEW.md').write_text(
        '# 有限上下文独立审核\n\n'
        '先读技能 independent-av-review.md、review-performance.md。继承用户当前模型。'
        '首次先看指定batch图片并保存实际理解/困惑，再打开packet的brief_after_blind做符合性核对。'
        '材料已在本地，不等待制作方第二次交接。\n\n'
        '每个batch最多加载它的分页图和必要原尺寸细节；只读其他batch的简短已确认发现和待审范围。'
        '累计图片较多时保存当前报告并用新上下文续接剩余batch，不能把首次盲看重置。'
        '边界图用于连续性；只把实际可辨认且已观察的帧登记为已审。\n\n'
        '只在本目录reports/写check_av_review兼容JSON；附batch_id、reviewer身份、当前视频哈希、'
        '观察方式/具体发现及证据文件哈希。未听音保持pending。机器合并不授予pass。'
        '修复轮数取packet，不因换上下文/审片者重置。\n', encoding='utf-8')
    return packet


def merge(packet_path, reports, out, run_started_at=None, paused=None, at=None):
    packet = read(packet_path)
    video = Path(packet['video_path'])
    if digest(video) != packet['video_sha256'] or digest(packet['index_path']) != packet['index_sha256']:
        raise ValueError('Packet media/index changed; do not reuse old observations')
    clock = at or now()
    state_path = Path(out) / 'progress-state.json'
    prior = read(state_path) if state_path.exists() else {}
    if prior and prior.get('video_sha256') != packet['video_sha256']:
        raise ValueError('Progress state belongs to another video')
    paused = bool(paused or (prior.get('paused') and not run_started_at))
    supplied = {str(Path(p).resolve()): digest(p) for p in reports}
    for source in prior.get('accepted_reports', []):
        if supplied.get(source['path']) != source['sha256']:
            raise ValueError('Keep previously accepted reports unchanged in every merge')
    if (run_started_at and prior.get('run_started_at') and run_started_at != prior['run_started_at']
            and not prior.get('paused')):
        raise ValueError('Do not restart the wait clock without a recorded pause')
    result = {'video_path': str(video), 'video_sha256': packet['video_sha256'],
              'reviewer': {'id': 'batch-report-merge', 'mode': 'report_aggregation'},
              'coverage': {'decoded_frames': packet['decoded_frames'], 'visual_ranges': [],
                           'audio_listened_ranges_seconds': [], 'realtime_viewed_ranges_seconds': [],
                           'audio_status': 'pending' if packet['has_audio'] else 'not_applicable'},
              'findings': [], 'limitations': ['Aggregate is not final creative/AV acceptance.'],
              'verdict': 'incomplete', 'repair_round': packet['repair_round'], 'report_sources': []}
    blind = []
    for path in reports:
        report = read(path)
        validation = check(video, report, packet['decoded_frames'], packet['duration_seconds'], packet['has_audio'], not packet['has_audio'])
        if not validation['evidence_consistent']:
            raise ValueError(str(path) + ': ' + '; '.join(validation['errors']))
        batch = next((b for b in packet['batches'] if b['id'] == report.get('batch_id')), None)
        if batch is None:
            raise ValueError('Missing/unknown batch_id: ' + str(path))
        for row in report.get('coverage', {}).get('visual_ranges', []):
            if not batch['boundary_range'][0] <= row['start_frame'] <= row['end_frame'] <= batch['boundary_range'][1]:
                raise ValueError('Report claims visual coverage outside assigned batch boundaries')
        identity = report['reviewer']['id']
        result['report_sources'].append({'path': str(Path(path).resolve()), 'sha256': digest(path), 'reviewer': report['reviewer'], 'batch_id': batch['id']})
        for key in ('visual_ranges', 'audio_listened_ranges_seconds'):
            result['coverage'][key].extend({**r, 'reviewer_id': identity} for r in report.get('coverage', {}).get(key, []))
        # Playback declarations are kept as claims; final reviewer must verify them.
        result['coverage']['realtime_viewed_ranges_seconds'].extend(report.get('coverage', {}).get('realtime_viewed_ranges_seconds', []))
        if report.get('coverage', {}).get('audio_perception', {}).get('status') == 'available':
            result['coverage']['audio_perception'] = report['coverage']['audio_perception']
        result['findings'].extend({**f, 'reviewer_id': identity} for f in report.get('findings', []))
        result['limitations'].extend(report.get('limitations', []))
        if report.get('blind_observation'):
            blind.append({'reviewer_id': identity, 'batch_id': batch['id'], 'observation': report['blind_observation']})
    cov = result['coverage']
    cov['unreviewed_frame_ranges'] = gaps([(r['start_frame'], r['end_frame']) for r in cov['visual_ranges']], packet['decoded_frames'], True)
    audio_gaps = gaps([(r['start'], r['end']) for r in cov['audio_listened_ranges_seconds']], packet['duration_seconds']) if packet['has_audio'] else []
    if (packet['has_audio'] and not audio_gaps and cov.get('audio_perception', {}).get('status') == 'available'
            and cov.get('audio_perception', {}).get('tool')):
        cov['audio_status'] = 'complete'
    if any(f.get('severity') in ('blocker', 'major') and f.get('recheck_status') != 'resolved' for f in result['findings']):
        result['verdict'] = 'needs_revision'
    result['blind_observations'] = blind
    # Only accepted observations/findings advance the clock, never polling or file mtime.
    def canonical(rows):
        # Reordering, reimporting or copying the same declaration is not progress.
        return sorted({json.dumps({k: v for k, v in row.items() if k not in ('reviewer_id', 'batch_id')},
                                  sort_keys=True, ensure_ascii=False) for row in rows})
    progress = {'visual': canonical(cov['visual_ranges']), 'audio': canonical(cov['audio_listened_ranges_seconds']),
                'findings': canonical(result['findings']), 'blind': canonical(blind)}
    fingerprint = hashlib.sha256(json.dumps(progress, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    started = run_started_at or prior.get('run_started_at')
    last = prior.get('last_actual_progress_at')
    if fingerprint != prior.get('progress_fingerprint') and (cov['visual_ranges'] or cov['audio_listened_ranges_seconds'] or result['findings'] or blind):
        last = clock
    origins = [datetime.fromisoformat(x) for x in (last, started) if x]
    origin = max(origins) if origins else None
    elapsed = max(0, (datetime.fromisoformat(clock) - origin).total_seconds()) if origin else 0
    stalled = bool(origin and elapsed >= packet['no_progress_minutes'] * 60 and not paused)
    state = {'video_sha256': packet['video_sha256'], 'run_started_at': started, 'last_actual_progress_at': last,
             'progress_fingerprint': fingerprint, 'paused': paused, 'no_progress_minutes': round(elapsed / 60, 2),
             'accepted_reports': [{'path': p, 'sha256': sha} for p, sha in sorted(supplied.items())],
             'delivery_due': stalled, 'delivery_verdict': result['verdict'],
             'next_action': 'deliver_current_with_incomplete_review; retain late reports' if stalled else 'paused' if paused else 'continue_remaining_batches' if origin else 'review_not_started',
             'visual_gaps': cov['unreviewed_frame_ranges'], 'audio_gaps': audio_gaps}
    write(Path(out) / 'av-review.json', result)
    write(state_path, state)
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('prepare')
    p.add_argument('--video', required=True); p.add_argument('--index', required=True); p.add_argument('--out', required=True)
    p.add_argument('--frames', type=int, required=True); p.add_argument('--duration', type=float, required=True)
    p.add_argument('--has-audio', action='store_true'); p.add_argument('--batch-frames', type=int, default=150)
    p.add_argument('--repair-round', type=int, required=True); p.add_argument('--brief', action='append', default=[])
    p.add_argument('--no-progress-minutes', type=float, default=10)
    p = sub.add_parser('merge')
    p.add_argument('--packet', required=True); p.add_argument('--reports', nargs='*', default=[]); p.add_argument('--out', required=True)
    p.add_argument('--run-started-at'); p.add_argument('--paused', action='store_true', default=None)
    args = parser.parse_args()
    if args.command == 'prepare':
        result = prepare(args.video, args.index, args.out, args.frames, args.duration, args.has_audio, args.batch_frames, args.repair_round, args.brief, args.no_progress_minutes)
        print(json.dumps({'packet': str(Path(args.out).resolve() / 'packet.json'), 'batches': len(result['batches']), 'coverage': 'pending'}, ensure_ascii=False))
    else:
        print(json.dumps(merge(args.packet, args.reports, args.out, args.run_started_at, args.paused), ensure_ascii=False))


if __name__ == '__main__':
    main()
