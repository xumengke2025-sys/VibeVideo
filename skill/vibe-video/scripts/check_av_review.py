"""Check AV review evidence consistency. Does not watch, listen, or score art."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def gaps(intervals, end, discrete=False):
    cursor = 0
    missing = []
    for start, stop in sorted(intervals):
        if start > cursor + (0 if discrete else 1e-6):
            missing.append([cursor, start - 1 if discrete else start])
        cursor = max(cursor, stop + 1 if discrete else stop)
    if cursor < end - (0 if discrete else 1e-6):
        missing.append([cursor, end - 1 if discrete else end])
    return missing


def check(video, review, frames, duration, has_audio, allow_silent=False):
    errors = []
    coverage = review.get('coverage', {})
    verdict = review.get('verdict')
    if verdict not in ('pass', 'needs_revision', 'incomplete'):
        errors.append('Unknown review verdict')
    if review.get('video_sha256') != digest(video):
        errors.append('Review hash does not match current video')
    if not review.get('video_path') or Path(review['video_path']).resolve() != Path(video).resolve():
        errors.append('Review video path does not match current video')
    if coverage.get('decoded_frames') != frames:
        errors.append('Declared frame count does not match decoded frame count')
    if not review.get('reviewer', {}).get('id'):
        errors.append('Missing reviewer identity')
    if frames <= 0 or duration <= 0:
        errors.append('Media must have a positive decoded frame count and timeline duration')

    def ranges(key, visual):
        accepted = []
        for index, row in enumerate(coverage.get(key, [])):
            label = f'{key}[{index}]'
            if not isinstance(row, dict):
                errors.append(f'{label}: use an object with range and observation evidence')
                continue
            start, stop = row.get('start_frame' if visual else 'start'), row.get('end_frame' if visual else 'end')
            numeric = isinstance(start, (int, float)) and not isinstance(start, bool) and isinstance(stop, (int, float)) and not isinstance(stop, bool)
            valid = numeric and 0 <= start <= stop and stop < frames if visual else numeric and 0 <= start < stop <= duration + 1e-6
            if visual:
                valid = valid and type(start) is int and type(stop) is int
            if not valid:
                errors.append(f'{label}: invalid or out-of-bounds range')
                continue
            evidence = row.get('evidence', [])
            if not isinstance(evidence, list) or not evidence:
                errors.append(f'{label}: missing evidence files')
                continue
            if any(not isinstance(p, str) or not Path(p).is_absolute() or not Path(p).is_file() for p in evidence):
                errors.append(f'{label}: evidence must name existing absolute file paths')
                continue
            if row.get('source_video_sha256') != review.get('video_sha256'):
                errors.append(f'{label}: evidence is not bound to the current media hash')
                continue
            hashes = row.get('evidence_sha256', {})
            if not isinstance(hashes, dict) or any(hashes.get(p) != digest(p) for p in evidence):
                errors.append(f'{label}: evidence hashes missing or changed')
                continue
            extensions = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'} if visual else {'.wav', '.mp3', '.flac', '.m4a', '.aac', '.ogg', '.opus', '.mp4', '.mov', '.webm', '.mkv'}
            if any(Path(p).suffix.lower() not in extensions for p in evidence):
                errors.append(f'{label}: evidence files have the wrong modality')
                continue
            if not visual and row.get('method') not in ('audio_input', 'perceptible_av_playback'):
                errors.append(f'{label}: ASR/waveform/link/unknown methods cannot count as actual hearing')
                continue
            if not row.get('method') or not row.get('observation'):
                errors.append(f'{label}: missing actual observation method or finding')
                continue
            accepted.append((start, stop))
        return accepted

    visual = ranges('visual_ranges', True)
    visual_gaps = gaps(visual, frames, True)
    audio = ranges('audio_listened_ranges_seconds', False)
    audio_gaps = gaps(audio, duration) if has_audio else []
    if not has_audio and not allow_silent:
        errors.append('No audio track: explicit brief-based --allow-silent is required')
    if has_audio and coverage.get('audio_status') == 'not_applicable':
        errors.append('Audio track exists; cannot mark hearing not_applicable')
    if not has_audio and coverage.get('audio_status') != 'not_applicable':
        errors.append('Intentionally silent film must mark hearing not_applicable')
    if verdict == 'pass':
        if visual_gaps:
            errors.append('Pass declared with unreviewed frames')
        if has_audio and (audio_gaps or coverage.get('audio_status') != 'complete'):
            errors.append('Pass declared without complete actual audio listening coverage')
        perception = coverage.get('audio_perception', {})
        if has_audio and (perception.get('status') != 'available' or not perception.get('tool')):
            errors.append('Pass declared without an identified actual audio perception tool')
        if coverage.get('unreviewed_frame_ranges'):
            errors.append('Pass declared with explicitly pending frame ranges')
        if any(f.get('severity') in ('blocker', 'major') and f.get('recheck_status') != 'resolved' for f in review.get('findings', [])):
            errors.append('Pass declared with unresolved blocker/major finding')
    return {'evidence_consistent': not errors, 'review_verdict': verdict,
            'visual_gaps': visual_gaps, 'audio_gaps': audio_gaps, 'errors': errors,
            'limitation': 'Checks declared records and files only; cannot prove viewing, hearing, creative quality, or scientific correctness.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('--review', required=True, type=Path)
    parser.add_argument('--ffprobe', default='ffprobe')
    parser.add_argument('--allow-silent', action='store_true', help='Only for a brief that intentionally specifies no audio')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    try:
        probe = subprocess.run([args.ffprobe, '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', str(args.video)], capture_output=True, text=True, check=True, timeout=120)
        media = json.loads(probe.stdout)
        stream = next(s for s in media['streams'] if s.get('codec_type') == 'video')
        frames = int(stream['nb_read_frames'])
        has_audio = any(s.get('codec_type') == 'audio' for s in media['streams'])
        # Hearing must cover the audio timeline even when it extends past video.
        timelines = [s for s in media['streams'] if s.get('codec_type') == 'audio'] if has_audio else [stream]
        origin = float(media.get('format', {}).get('start_time') or 0)
        duration = max(
            max(0.0, float(s.get('start_time') or 0) - origin) + float(s['duration'])
            if s.get('duration') is not None else float(media['format']['duration'])
            for s in timelines
        )
        result = check(args.video, json.loads(args.review.read_text(encoding='utf-8-sig')), frames, duration, has_audio, args.allow_silent)
    except (OSError, ValueError, KeyError, StopIteration, subprocess.SubprocessError, TypeError) as exc:
        result = {'evidence_consistent': False, 'errors': [str(exc)]}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding='utf-8')
    print(text)
    raise SystemExit(0 if result['evidence_consistent'] else 1)


if __name__ == '__main__':
    main()
