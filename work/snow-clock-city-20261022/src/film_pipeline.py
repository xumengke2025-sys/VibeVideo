"""Bounded, resumable production rendering. No Blender starts on import or plan/status.

Every Blender child goes through render_queue.py. A version owns immutable input
hashes; changed inputs require another --version rather than mixing old PNGs.
This is engineering validation, not the project's one audiovisual review.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import time
import wave
import zlib
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[1]
MODEL = ROOT / 'model/clock-city-production-v5.blend'
AUDIO = ROOT / 'audio/final-mix.wav'
BLENDER = PROJECT / 'tools/blender-portable/blender-4.5.3-windows-x64/blender.exe'
FFMPEG = PROJECT / 'work/firmbuddy-blueprint-20261012/tools/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
FFPROBE = PROJECT.parent / 'node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
FPS, WIDTH, HEIGHT, TOTAL = 24, 1080, 1920, 2160
PROOF = [0, 240, 480, 648, 888, 1032, 1104, 1152, 1200, 1248, 1320, 1416, 1536, 1776, 2064, 2159]
FLAGS = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f'.{os.getpid()}.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf8')
    temporary.replace(path)


def alive(pid):
    if os.name == 'nt':
        import ctypes
        kernel = ctypes.windll.kernel32
        handle = kernel.OpenProcess(0x100000, False, int(pid))
        if not handle:
            return False
        try:
            return kernel.WaitForSingleObject(handle, 0) == 258
        finally:
            kernel.CloseHandle(handle)
    try:
        os.kill(int(pid), 0)
        return True
    except OSError:
        return False


def blender_pids():
    if os.name != 'nt':
        return []
    result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq blender.exe', '/FO', 'CSV', '/NH'],
                            capture_output=True, text=True, encoding='oem', errors='replace', creationflags=FLAGS, timeout=15)
    return [int(row[1]) for row in csv.reader(io.StringIO(result.stdout))
            if len(row) > 1 and row[0].lower() == 'blender.exe']


def valid_png(path):
    """Check complete chunks, CRC and actual production dimensions before reuse."""
    try:
        with path.open('rb') as f:
            if f.read(8) != b'\x89PNG\r\n\x1a\n':
                return False
            first = True
            while True:
                head = f.read(8)
                if len(head) != 8:
                    return False
                length, kind = struct.unpack('>I4s', head)
                if length > 128 * 1024 * 1024:
                    return False
                data, crc = f.read(length), f.read(4)
                if len(data) != length or len(crc) != 4:
                    return False
                if zlib.crc32(kind + data) & 0xffffffff != struct.unpack('>I', crc)[0]:
                    return False
                if first:
                    if kind != b'IHDR' or struct.unpack('>II', data[:8]) != (WIDTH, HEIGHT):
                        return False
                    first = False
                if kind == b'IEND':
                    return length == 0 and f.read(1) == b''
    except (OSError, ValueError, struct.error):
        return False


class Pipeline:
    def __init__(self, args):
        self.args = args
        self.base = ROOT / 'render' / args.version
        self.status_path = self.base / 'status.json'
        self.state = dict(pipeline_pid=os.getpid(), mode=args.mode, version=args.version,
                          delivery_mode='ai_review_once', width=WIDTH, height=HEIGHT,
                          fps=FPS, film_duration=90, updated=time.time())
        self.manifest = None
        self.model_stat = None

    def save(self, **updates):
        self.state.update(updates, updated=time.time())
        write_json(self.status_path, self.state)

    def source_files(self):
        return sorted((ROOT / 'src').glob('*.py'))

    def freeze(self, build=False):
        paths = self.source_files()
        if build:
            paths += sorted(p for p in (ROOT / 'assets').rglob('*') if p.is_file())
            environment = ROOT / 'model/environment-assets-v2.blend'
            if environment.exists():
                paths.append(environment)
        else:
            paths += [MODEL, AUDIO]
        missing = [str(p) for p in paths if not p.is_file()]
        if missing:
            raise RuntimeError('Missing inputs: ' + ', '.join(missing))
        manifest = dict(schema=1, files={p.relative_to(ROOT).as_posix(): digest(p) for p in paths},
                        width=WIDTH, height=HEIGHT, fps=FPS, duration=90, frames=TOTAL,
                        delivery_mode='ai_review_once', samples=self.args.samples,
                        engine=self.args.engine, resolution_percentage=100)
        path = self.base / ('build-inputs.json' if build else 'frozen-manifest.json')
        if path.exists() and json.loads(path.read_text(encoding='utf8')) != manifest:
            raise RuntimeError(f'Frozen inputs changed: {path}. Use a new --version; old PNGs are preserved.')
        write_json(path, manifest)
        snapshot = self.base / ('build-source' if build else 'source')
        for src in self.source_files():
            dest = snapshot / src.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists():
                shutil.copy2(src, dest)
            elif digest(src) != digest(dest):
                raise RuntimeError(f'Source snapshot differs: {dest}')
        self.manifest = manifest
        if not build:
            self.model_stat = (MODEL.stat().st_size, MODEL.stat().st_mtime_ns)
        return manifest

    def unchanged(self, final=False):
        for relative, expected in self.manifest['files'].items():
            path = ROOT / relative
            # The large .blend is fully hashed at freeze and after completion;
            # detect any replacement/edits cheaply between bounded processes.
            if path == MODEL and not final:
                if (path.stat().st_size, path.stat().st_mtime_ns) != self.model_stat:
                    raise RuntimeError('Production model changed during rendering; use a new version.')
            elif digest(path) != expected:
                raise RuntimeError(f'Frozen input changed during rendering: {relative}')

    def run_logged(self, command, log, env=None, frames=None, folder=None):
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open('w', encoding='utf8') as output:
            child = subprocess.Popen([str(c) for c in command], cwd=ROOT, env=env,
                                     stdout=output, stderr=subprocess.STDOUT, creationflags=FLAGS)
            try:
                while child.poll() is None:
                    done = sum((folder / f'{f:05d}.png').exists() for f in frames) if frames else None
                    self.save(child_pid=child.pid, log=str(log), completed_frames=done,
                              requested_frames=len(frames) if frames else None,
                              blender_pids=blender_pids())
                    time.sleep(5)
                if child.returncode:
                    raise RuntimeError(f'Process failed ({child.returncode}); see {log}. No automatic retry.')
            except BaseException:
                # Do not terminate legitimate Blender work just because the
                # launcher was interrupted. A resumed launcher waits on queue.
                self.save(stage='interrupted_or_failed', child_pid=child.pid,
                          child_still_alive=child.poll() is None, log=str(log))
                raise
        self.save(child_pid=None, blender_pids=blender_pids())

    def queued_blender(self, script, args, label, env=None, frames=None, folder=None):
        stamp = time.strftime('%Y%m%d-%H%M%S') + f'-{os.getpid()}'
        blender_log = self.base / 'logs' / f'{label}-{stamp}.blender.log'
        queue_log = blender_log.with_suffix('.queue.log')
        command = [sys.executable, ROOT / 'src/render_queue.py', '--log', blender_log,
                   '--', BLENDER, '--background', '--python-exit-code', '1', '--python', script]
        if args:
            command += ['--'] + args
        self.save(stage='queued_or_rendering', blender_log=str(blender_log), batch=label)
        self.run_logged(command, queue_log, env=env, frames=frames, folder=folder)

    def build(self):
        self.freeze(build=True)
        build_report = self.base / 'build-result.json'
        if build_report.exists():
            expected = json.loads(build_report.read_text(encoding='utf8'))['model_sha256']
            if MODEL.exists() and digest(MODEL) == expected:
                self.save(stage='build_already_complete', model=str(MODEL))
                return
            raise RuntimeError('Build output changed or missing; select a new version to rebuild.')
        if MODEL.exists():
            archive = self.base / 'previous-model' / MODEL.name
            archive.parent.mkdir(parents=True, exist_ok=True)
            if not archive.exists():
                shutil.copy2(MODEL, archive)
        MODEL.parent.mkdir(parents=True, exist_ok=True)
        self.queued_blender(ROOT / 'src/film_world.py', [], 'build')
        self.queued_blender(ROOT / 'src/optimize_production.py', [], 'forest-lod')
        self.queued_blender(ROOT / 'src/bake_static_geometry.py', [], 'static-geometry')
        self.queued_blender(ROOT / 'src/finish_foreground.py', [], 'foreground-bank')
        self.unchanged(final=True)
        if not MODEL.is_file():
            raise RuntimeError('Builder exited without production-v2.blend')
        write_json(build_report, dict(model=str(MODEL), model_sha256=digest(MODEL), completed=time.time()))
        self.save(stage='build_complete', model=str(MODEL))

    def render(self):
        self.freeze()
        mode = self.args.mode
        frames = (sorted(set(self.args.frames or PROOF)) if mode == 'proof'
                  else list(range(43 * FPS, 60 * FPS)) if mode == 'sample'
                  else list(range(TOTAL)))
        if not frames or min(frames) < 0 or max(frames) >= TOTAL:
            raise ValueError('Frames must be in 0..2159')
        folder = self.base / mode
        folder.mkdir(parents=True, exist_ok=True)
        write_json(folder / 'frozen-manifest.json', self.manifest)
        write_json(folder / 'requested-frames.json', dict(frames=frames, start_seconds=frames[0] / FPS,
                                                        continuous=mode != 'proof'))
        # An invalid existing PNG must not be skipped by film_render.py.
        for f in frames:
            path = folder / f'{f:05d}.png'
            if path.exists() and not valid_png(path):
                rejected = folder / 'rejected'
                rejected.mkdir(exist_ok=True)
                path.replace(rejected / f'{f:05d}-{time.time_ns()}.png')
        if mode == 'full':
            self.reuse_checked_frames(folder, frames)
        env = os.environ.copy()
        env['SNOW_ENGINE'] = self.args.engine
        env.update(SNOW_SAMPLES=str(self.args.samples), SNOW_SCALE='100',
                   SNOW_OUTPUT=str(folder), SNOW_MODEL=str(MODEL))
        renderer = (ROOT / 'src/film_render.py').read_text(encoding='utf8')
        if 'SNOW_MODEL' not in renderer and "model/clock-city-production-v1.blend" in renderer:
            raise RuntimeError('film_render.py still hardcodes v1; update its model loading to SNOW_MODEL or v2 before rendering.')
        for offset in range(0, len(frames), self.args.batch_size):
            batch = frames[offset:offset + self.args.batch_size]
            missing = [f for f in batch if not (folder / f'{f:05d}.png').exists()]
            if not missing:
                continue
            self.unchanged()
            args = ['stills'] + [str(f) for f in missing]
            self.queued_blender(ROOT / 'src/film_render.py', args,
                                f'{mode}-{batch[0]:05d}-{batch[-1]:05d}', env, frames, folder)
            for f in missing:
                if not valid_png(folder / f'{f:05d}.png'):
                    raise RuntimeError(f'Missing or invalid rendered PNG {f}; inspect batch log and resume explicitly.')
            self.save(stage='batch_complete', completed_frames=sum((folder / f'{f:05d}.png').exists() for f in frames))
        self.unchanged(final=True)
        if mode != 'proof':
            self.encode(folder, frames)
        else:
            self.save(stage='proof_complete', completed_frames=len(frames), folder=str(folder))

    def reuse_checked_frames(self, folder, frames):
        """Reuse only this version's exact frozen sample/proof, never other films."""
        report_path = folder / 'frame-provenance.json'
        previous = json.loads(report_path.read_text(encoding='utf8')) if report_path.exists() else {}
        reused = {item['frame']: item for item in previous.get('reused', [])
                  if (folder / f'{item["frame"]:05d}.png').exists()}
        sources = []
        for mode in ['sample', 'proof']:
            source = self.base / mode
            manifest_path = source / 'frozen-manifest.json'
            try:
                matches = json.loads(manifest_path.read_text(encoding='utf8')) == self.manifest
            except (OSError, ValueError):
                matches = False
            sources.append(dict(folder=str(source), frozen_manifest_matches=matches))
            if not matches:
                continue
            for frame in frames:
                target = folder / f'{frame:05d}.png'
                candidate = source / target.name
                if target.exists() or not valid_png(candidate):
                    continue
                try:
                    os.link(candidate, target)
                    method = 'hardlink'
                except OSError:
                    shutil.copy2(candidate, target)
                    method = 'copy2'
                reused[frame] = dict(frame=frame, source=str(candidate), method=method,
                                     crc_checked=True)
        write_json(report_path, dict(sources=sources, reused=[reused[f] for f in sorted(reused)],
                                     reused_count=len(reused), frozen_manifest_matches_required=True))
        self.save(stage='reused_checked_frames', reused_frames=len(reused))

    def encode(self, folder, frames):
        self.save(stage='encoding')
        duration, start = len(frames) / FPS, frames[0] / FPS
        with wave.open(str(AUDIO), 'rb') as track:
            if track.getnframes() / track.getframerate() + 0.001 < start + duration:
                raise RuntimeError('final-mix.wav is shorter than required timeline')
        delivery = ROOT / 'delivery' / self.args.version
        delivery.mkdir(parents=True, exist_ok=True)
        video = delivery / ('雪山钟城-第一篮面包-' + self.args.mode + '.mp4')
        temporary = video.with_suffix('.partial.mp4')
        command = [FFMPEG, '-y', '-hide_banner', '-loglevel', 'warning', '-framerate', str(FPS),
                   '-start_number', str(frames[0]), '-i', folder / '%05d.png',
                   '-ss', str(start), '-i', AUDIO, '-map', '0:v:0', '-map', '1:a:0',
                   '-frames:v', str(len(frames)), '-t', str(duration), '-c:v', 'libx264',
                   '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-threads:v', '2',
                   '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-ac', '2',
                   '-movflags', '+faststart', temporary]
        self.run_logged(command, self.base / 'logs' / f'{self.args.mode}-encode.log')
        self.save(stage='engineering_checks')
        probe = json.loads(subprocess.check_output([str(FFPROBE), '-v', 'error', '-count_frames',
                    '-show_streams', '-show_format', '-of', 'json', str(temporary)],
                    text=True, encoding='utf8', creationflags=FLAGS))
        vs = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        au = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
        if ((vs['width'], vs['height'], int(vs['nb_read_frames'])) != (WIDTH, HEIGHT, len(frames))
                or Fraction(vs['r_frame_rate']) != FPS
                or abs(float(probe['format']['duration']) - duration) > 0.08
                or int(au['sample_rate']) != 48000 or au['channels'] != 2):
            raise RuntimeError('Encoded dimensions/frame count/duration/audio mismatch')
        self.run_logged([FFMPEG, '-hide_banner', '-v', 'error', '-xerror', '-i', temporary,
                         '-map', '0:v:0', '-map', '0:a:0', '-c:v', 'rawvideo', '-c:a', 'pcm_s16le',
                         '-f', 'null', os.devnull], self.base / 'logs' / f'{self.args.mode}-decode.log')
        self.unchanged(final=True)
        temporary.replace(video)
        report = dict(video=str(video), sha256=digest(video), width=WIDTH, height=HEIGHT,
                      fps=FPS, frames=len(frames), duration=duration, source_start_seconds=start,
                      audio_source=str(AUDIO), audio_sha256=self.manifest['files']['audio/final-mix.wav'],
                      complete_audio_video_decode=True, actual_viewing=False, actual_listening=False,
                      independent_ai_review='pending; engineering checks do not consume the one review',
                      frozen_manifest=str(self.base / 'frozen-manifest.json'), ffmpeg=str(FFMPEG), ffprobe=str(FFPROBE))
        write_json(delivery / f'{self.args.mode}-ffprobe.json', probe)
        write_json(delivery / f'{self.args.mode}-engineering-check.json', report)
        write_json(delivery / 'frozen-manifest.json', self.manifest)
        self.save(stage='candidate_ready_for_review' if self.args.mode == 'full' else 'sample_complete',
                  video=str(video), sha256=report['sha256'], completed_frames=len(frames))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['plan', 'status', 'build', 'build-proof', 'proof', 'sample', 'full'])
    parser.add_argument('--version', default='film-v2')
    parser.add_argument('--frames', nargs='+', type=int, help='proof frame indices (zero-based)')
    parser.add_argument('--batch-size', type=int, default=24, help='bounded frames per Blender process')
    parser.add_argument('--samples', type=int, default=32)
    parser.add_argument('--engine', choices=['CYCLES','EEVEE'], default='CYCLES')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', args.version) or args.version in ('.', '..'):
        parser.error('Use a simple version name without directory separators')
    if not 1 <= args.batch_size <= 48 or args.samples < 1:
        parser.error('batch-size must be 1..48 and samples positive')
    pipeline = Pipeline(args)
    if args.mode == 'status':
        state = json.loads(pipeline.status_path.read_text(encoding='utf8')) if pipeline.status_path.exists() else {'stage': 'not_started'}
        state['pipeline_alive'] = alive(state['pipeline_pid']) if state.get('pipeline_pid') else False
        state['blender_pids_now'] = blender_pids()
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return
    if args.mode == 'plan':
        print(json.dumps(dict(root=str(ROOT), blender=str(BLENDER), ffmpeg=str(FFMPEG),
                              ffprobe=str(FFPROBE), model=str(MODEL), audio=str(AUDIO),
                              tools_exist={str(p): p.is_file() for p in [BLENDER, FFMPEG, FFPROBE]},
                              version=args.version, batch_size=args.batch_size, samples=args.samples,
                              proof_frames=PROOF, sample_frames=[1032, 1439], full_frames=[0, 2159],
                              dimensions=[WIDTH, HEIGHT], fps=FPS, delivery_mode='ai_review_once'), ensure_ascii=False, indent=2))
        return
    for tool in [BLENDER, FFMPEG, FFPROBE]:
        if not tool.is_file():
            raise FileNotFoundError(tool)
    pipeline.base.mkdir(parents=True, exist_ok=True)
    lock = pipeline.base / '.pipeline.lock'
    try:
        with lock.open('x', encoding='utf8') as f:
            json.dump(dict(pid=os.getpid(), started=time.time()), f)
    except FileExistsError:
        owner = json.loads(lock.read_text(encoding='utf8'))
        if alive(owner['pid']):
            raise RuntimeError(f'Version already owned by live pipeline PID {owner["pid"]}')
        lock.unlink()
        with lock.open('x', encoding='utf8') as f:
            json.dump(dict(pid=os.getpid(), started=time.time()), f)
    try:
        pipeline.save(stage='starting')
        if args.mode in ('build', 'build-proof'):
            pipeline.build()
            if args.mode == 'build-proof':
                args.mode = 'proof'
                args.frames = args.frames if args.frames is not None else [1320, 2064]
                pipeline.save(mode='proof', requested_mode='build-proof')
                pipeline.render()
        else:
            pipeline.render()
    except BaseException as error:
        pipeline.save(stage='failed', error=str(error), retry='No automatic retry; inspect logs, then resume this exact version.')
        raise
    finally:
        if lock.exists() and json.loads(lock.read_text(encoding='utf8'))['pid'] == os.getpid():
            lock.unlink()


if __name__ == '__main__':
    main()
