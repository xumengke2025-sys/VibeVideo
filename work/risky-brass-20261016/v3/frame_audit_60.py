#!/usr/bin/env python3
"""Export every decoded frame, timestamped atlases and a local frame viewer. No aesthetic scoring."""
import argparse
import hashlib
import html
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, 'D:\\Codex\\skills\\vibe-video\\scripts')
from video_evidence import run, tool_path


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--start-frame', type=int, default=0)
    parser.add_argument('--end-frame', type=int)
    parser.add_argument('--width', type=int, default=960)
    parser.add_argument('--cuts', default='', help='Known hard-cut source frame numbers')
    parser.add_argument('--ffmpeg')
    parser.add_argument('--ffprobe')
    args = parser.parse_args()
    from PIL import Image, ImageDraw, ImageFont
    video = args.video.resolve()
    if not video.is_file() or video.stat().st_size == 0:
        raise ValueError('Video missing or empty')
    if args.start_frame < 0 or args.width < 64 or args.width > 7680:
        raise ValueError('Invalid start frame or review image width (64–7680)')
    ffmpeg = tool_path('ffmpeg', args.ffmpeg, video)
    sibling = Path(ffmpeg).with_name('ffprobe.exe' if sys.platform == 'win32' else 'ffprobe')
    ffprobe = tool_path('ffprobe', args.ffprobe or (str(sibling) if sibling.is_file() else None), video)
    meta = json.loads(run([ffprobe, '-v', 'error', '-select_streams', 'v:0', '-show_streams', '-show_frames',
                          '-show_entries', 'stream=width,height,avg_frame_rate:frame=best_effort_timestamp_time',
                          '-of', 'json', str(video)]).stdout)
    streams = meta.get('streams', [])
    if not streams:
        raise ValueError('No video stream')
    timestamps = [float(f['best_effort_timestamp_time']) for f in meta.get('frames', [])]
    if not timestamps or any(not math.isfinite(t) for t in timestamps):
        raise ValueError('No valid decoded frame timestamps')
    if any(b <= a for a, b in zip(timestamps, timestamps[1:])):
        raise ValueError('Frame timestamps must be strictly increasing')
    last = len(timestamps) - 1
    start, end = args.start_frame, last if args.end_frame is None else args.end_frame
    if not 0 <= start <= end <= last:
        raise ValueError(f'Frame window must be within 0–{last}, inclusive')
    cuts = set(int(v) for v in args.cuts.split(',') if v.strip())
    if any(c < 0 or c > last for c in cuts):
        raise ValueError('Declared cut outside source frame range')
    output = args.out.resolve()
    frames_dir = output / 'frames'
    # Dedicated evidence output only; never overwrite source assets or a stale run.
    if output.exists() and any(output.iterdir()):
        raise ValueError('Evidence directory must be new or empty; use a versioned --out')
    frames_dir.mkdir(parents=True, exist_ok=True)
    width = min(args.width, streams[0]['width'])
    width -= width % 2
    # Remotion's lean FFmpeg omits select/trim filters. Output seeking discards decoded
    # frames before the timestamp; a midpoint avoids rounding onto the wrong boundary.
    seek = 0 if start == 0 else (timestamps[start-1]+timestamps[start])/2-timestamps[0]
    run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-xerror', '-threads', '1', '-i', str(video),
         '-ss', f'{seek:.9f}', '-frames:v', str(end-start+1), '-vf', f'scale={width}:-2',
         '-fps_mode', 'passthrough', '-start_number', str(start),
         '-q:v', '2', '-threads:v', '1', str(frames_dir / 'frame-%06d.jpg')])
    files = sorted(frames_dir.glob('frame-*.jpg'))
    expected = end - start + 1
    if len(files) != expected:
        raise ValueError(f'Expected {expected} frames, extracted {len(files)}')
    font = ImageFont.load_default(size=16)
    cols, rows, tile_w, label_h = 6, 10, 320, 28
    tile_h = round(tile_w * streams[0]['height'] / streams[0]['width'])
    per_page = cols * rows
    entries, sheets, previous, sheet = [], [], None, None
    for index, file in enumerate(files):
        frame = start + index
        stamp = timestamps[frame]
        with Image.open(file) as picture:
            gray = picture.convert('L').resize((64, 36)).tobytes()
            mean = sum(gray) / len(gray)
            diff = None if previous is None else sum(abs(a-b) for a, b in zip(gray, previous)) / len(gray)
            flags = []
            if mean < 2:
                flags.append('near_black_candidate')
            if diff is not None and diff < 0.025:
                flags.append('near_static_candidate')
            if diff is not None and diff > 24:
                flags.append('large_change_declared_cut' if frame in cuts else 'large_change_candidate')
            entries.append({'frame': frame, 'seconds': stamp, 'image': file.relative_to(output).as_posix(),
                            'mean_luma_0_255': round(mean, 3),
                            'adjacent_luma_diff_0_255': None if diff is None else round(diff, 3), 'candidates': flags})
            previous = gray
            if index % per_page == 0:
                count = min(per_page, expected-index)
                sheet = Image.new('RGB', (cols*tile_w, math.ceil(count/cols)*(tile_h+label_h)), '#10131b')
            slot = index % per_page
            x, y = (slot % cols)*tile_w, (slot // cols)*(tile_h+label_h)
            sheet.paste(picture.convert('RGB').resize((tile_w, tile_h)), (x, y))
            ImageDraw.Draw(sheet).text((x+6, y+tile_h+5), f'F{frame:06d}   {stamp:.3f}s', fill='#e1e8f0', font=font)
        if slot == per_page-1 or index == expected-1:
            path = output / f'atlas-{index//per_page:03d}.jpg'
            sheet.save(path, quality=93)
            sheets.append(path.name)
    report = {'video': str(video), 'video_sha256': sha256(video), 'source_frame_count': len(timestamps),
              'window_inclusive': [start, end], 'exported_frame_count': len(entries),
              'export_width': width, 'source_width': streams[0]['width'], 'source_height': streams[0]['height'],
              'declared_cuts': sorted(cuts), 'atlases': sheets, 'atlas_frames_per_page': per_page, 'frames': entries,
              'interpretation': 'Candidate metrics are diagnostic only; intentional holds and cuts may be correct.',
              'visual_review': {'status': 'pending', 'reviewed_ranges': [], 'method': '', 'issues': []}}
    (output/'frame-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    title = html.escape(video.name)
    data = json.dumps(entries, ensure_ascii=False).replace('<', '\\u003c')
    viewer = '''<!doctype html><meta charset="utf-8"><title>Frame audit</title>
<style>body{margin:24px;background:#10131b;color:#e1e8f0;font:16px system-ui}img{display:block;max-width:100%;max-height:76vh;margin:12px auto}input{width:100%}button{margin-right:10px;padding:8px}pre{white-space:pre-wrap}a{color:#91c5e8}</style>
<h1>TITLE</h1><p>Source frames, not a re-render. Arrow keys step one frame. Full-size source details require an original-resolution extraction.</p>
<button id="prev">Previous frame</button><button id="next">Next frame</button><label id="label"></label>
<input id="seek" type="range" min="0" max="MAX" step="1" value="0"><img id="picture"><pre id="detail"></pre>
<p><a href="frame-audit.json">Frame report</a></p><script>
const frames=DATA;const seek=document.getElementById('seek');const picture=document.getElementById('picture');
function show(){const f=frames[Number(seek.value)];picture.src=f.image;document.getElementById('label').textContent=`Frame ${f.frame} | ${f.seconds.toFixed(3)} s`;document.getElementById('detail').textContent=JSON.stringify(f,null,2)}
function step(n){seek.value=Math.max(0,Math.min(frames.length-1,Number(seek.value)+n));show()}
seek.oninput=show;document.getElementById('prev').onclick=()=>step(-1);document.getElementById('next').onclick=()=>step(1);
document.onkeydown=e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();step(e.key==='ArrowRight'?1:-1)}};show();
</script>'''.replace('<h1>TITLE</h1>', '<h1>'+title+'</h1>').replace('max="MAX"', 'max="'+str(len(entries)-1)+'"').replace('const frames=DATA;', 'const frames='+data+';')
    (output/'review.html').write_text(viewer, encoding='utf-8')
    print(json.dumps({'frames': len(entries), 'source_frames': len(timestamps), 'atlases': len(sheets),
                      'report': str(output/'frame-audit.json'), 'viewer': str(output/'review.html'),
                      'visual_review': 'pending'}, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError, ImportError, KeyError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(2)
