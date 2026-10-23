"""Keep a complete baseline and replace explicitly scoped picture ranges.

Scope is a production decision, not an automatic visibility/shadow solver.
The tool refuses missing or changed reusable frames instead of silently mixing them.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess

from PIL import Image


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf8')


def digest(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def register(args):
    assert not Path(args.out).exists(), 'Baseline indices are immutable; use a new index path'
    report = read(args.report)
    assert report['decode_exit'] == 0, 'Baseline must have passed decoding'
    count, fps = int(report['frames']), float(report['frame_rate'].split('/')[0]) / float(report['frame_rate'].split('/')[1])
    video = Path(report['video'])
    assert digest(video) == report['sha256'], 'Baseline video changed'
    folder = Path(args.frames).resolve()
    paths = [folder / f'{i:05d}.png' for i in range(count)]
    missing = [i for i, path in enumerate(paths) if not path.is_file()]
    assert not missing, f'Incomplete baseline: missing {len(missing)} frames'
    cuts = [0] + [round(float(s) * fps) for s in args.cuts.split(',') if s] + [count]
    assert cuts == sorted(set(cuts)) and cuts[-2] < count
    index = {'video': str(video), 'video_sha256': report['sha256'],
             'frames_dir': str(folder), 'frames': count, 'fps': fps,
             'width': report['width'], 'height': report['height'],
             'shots': [{'id': i, 'start': a, 'end': b} for i, (a, b) in enumerate(zip(cuts, cuts[1:]))],
             'frame_sha256': [digest(path) for path in paths]}
    write(args.out, index)
    print(json.dumps({'registered_frames': count, 'shots': len(index['shots']), 'index': str(Path(args.out).resolve())}))


def plan(args):
    baseline = read(args.baseline)
    selected = set(int(i) for i in args.shots.split(',') if i) if args.shots is not None else set()
    known = {shot['id'] for shot in baseline['shots']}
    assert selected <= known, f'Unknown shots: {selected - known}'
    if args.global_visual:
        selected = known
    if args.audio_only:
        assert not selected and not args.global_visual
    assert args.audio_only or selected, 'Declare an actual visual scope or audio-only change'
    changed = set()
    for shot in baseline['shots']:
        if shot['id'] in selected:
            changed.update(range(max(0, shot['start'] - args.handles), min(baseline['frames'], shot['end'] + args.handles)))
    result = {'baseline': str(Path(args.baseline).resolve()),
              'baseline_index_sha256': digest(args.baseline), 'reason': args.reason,
              'scope_source': 'Explicit operator declaration; not automatic visibility certification.',
              'impact_checks_required': [] if args.audio_only else ['direct visibility', 'cast shadows', 'reflections and indirect light', 'motion continuity and adjacent cuts'],
              'affected_shots': sorted(selected), 'render_frames': sorted(changed),
              'reuse_frames': [i for i in range(baseline['frames']) if i not in changed],
              'audio_only': args.audio_only, 'handles': args.handles}
    write(args.out, result)
    print(json.dumps({'render': len(changed), 'reuse': baseline['frames'] - len(changed), 'total': baseline['frames']}))


def materialize(args):
    change = read(args.plan)
    assert digest(change['baseline']) == change['baseline_index_sha256'], 'Baseline index changed'
    baseline = read(change['baseline'])
    target = Path(args.out).resolve()
    assert not target.exists(), 'Use a new staging directory; never overwrite a baseline'
    source = Path(baseline['frames_dir'])
    patches = Path(args.patches).resolve() if args.patches else None
    changed = set(change['render_frames'])
    assert not changed or patches is not None, 'Visual changes require rendered patch frames'
    items = []
    for i in range(baseline['frames']):
        patch = i in changed
        path = (patches if patch else source) / f'{i:05d}.png'
        assert path.is_file(), f'Missing frame {i}: {path}'
        sha = digest(path)
        if not patch:
            assert sha == baseline['frame_sha256'][i], f'Reusable frame {i} changed'
        with Image.open(path) as image:
            assert image.size == (baseline['width'], baseline['height']), f'Wrong dimensions at {i}'
        items.append({'frame': i, 'source': str(path), 'sha256': sha, 'kind': 'patch' if patch else 'baseline'})
    target.mkdir(parents=True)
    for item in items:
        os.link(item['source'], target / f"{item['frame']:05d}.png")
    write(target / 'provenance.json', {'plan': str(Path(args.plan).resolve()), 'frames': items,
                                     'staging_policy': 'Read-only encode input. Do not modify hard-linked frames in place.'})
    print(json.dumps({'staged_frames': len(items), 'patched': len(changed), 'out': str(target)}))


def remux_audio(args):
    baseline = read(args.baseline)
    assert digest(baseline['video']) == baseline['video_sha256'], 'Baseline video changed'
    output = Path(args.out).resolve()
    assert not output.exists(), 'Keep historical videos; use a new output path'
    audio = Path(args.audio).resolve()
    assert audio.is_file()
    ff = Path('D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')
    duration = baseline['frames'] / baseline['fps']
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(ff), '-hide_banner', '-loglevel', 'warning',
                    '-i', baseline['video'], '-i', str(audio),
                    '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy',
                    '-af', f'apad,atrim=duration={duration}', '-c:a', 'aac',
                    '-b:a', '256k', '-ar', '48000', '-ac', '2',
                    '-t', str(duration), '-movflags', '+faststart', str(output)], check=True)
    subprocess.run([str(ff), '-v', 'error', '-i', str(output), '-vn',
                    '-c:a', 'pcm_s16le', '-f', 'null', 'NUL'], check=True)
    write(output.with_suffix('.provenance.json'),
          {'video': str(output), 'sha256': digest(output), 'picture_mode': 'stream copy',
           'baseline_video_sha256': baseline['video_sha256'], 'new_audio': str(audio),
           'new_audio_sha256': digest(audio), 'rendered_3d_frames': 0,
           'actual_listening': False})
    print(json.dumps({'video': str(output), 'rendered_3d_frames': 0, 'picture_mode': 'stream copy'}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    command = commands.add_parser('register')
    for key in ['report', 'frames', 'out']:
        command.add_argument('--' + key, required=True)
    command.add_argument('--cuts', required=True, help='Interior shot boundaries in seconds')
    command.set_defaults(run=register)
    command = commands.add_parser('plan')
    command.add_argument('--baseline', required=True)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument('--audio-only', action='store_true')
    mode.add_argument('--shots')
    mode.add_argument('--global-visual', action='store_true')
    command.add_argument('--handles', type=int, default=2)
    command.add_argument('--reason', required=True)
    command.add_argument('--out', required=True)
    command.set_defaults(run=plan)
    command = commands.add_parser('materialize')
    command.add_argument('--plan', required=True)
    command.add_argument('--patches')
    command.add_argument('--out', required=True)
    command.set_defaults(run=materialize)
    command = commands.add_parser('remux-audio')
    command.add_argument('--baseline', required=True)
    command.add_argument('--audio', required=True)
    command.add_argument('--out', required=True)
    command.set_defaults(run=remux_audio)
    args = parser.parse_args()
    assert getattr(args, 'handles', 0) >= 0
    args.run(args)


if __name__ == '__main__':
    main()
