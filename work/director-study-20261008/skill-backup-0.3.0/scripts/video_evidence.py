#!/usr/bin/env python3
"""Extract media evidence with Python stdlib + FFmpeg; no aesthetic scoring."""
import argparse
from array import array
import io
import json
import math
import shutil
import subprocess
import sys
import wave
from pathlib import Path


def tool_path(name, explicit, video):
    if explicit:
        candidate = Path(explicit).expanduser().resolve()
        if not candidate.is_file():
            raise ValueError(f"Missing {name}: {candidate}")
        return str(candidate)
    system = shutil.which(name)
    if system:
        return system
    filename = name + (".exe" if sys.platform == "win32" else "")
    roots = [Path.cwd(), *video.parents]
    for root in dict.fromkeys(roots):
        base = root / "node_modules" / "@remotion"
        if base.is_dir():
            for candidate in sorted(base.glob(f"compositor-*/{filename}")):
                if candidate.is_file():
                    return str(candidate)
    raise ValueError(f"{name} unavailable; supply --{name} or use an installed media tool")


def run(command, binary=False):
    options = {} if binary else {"text": True, "encoding": "utf-8", "errors": "replace"}
    result = subprocess.run(command, capture_output=True, **options)
    if result.returncode:
        error = result.stderr.decode("utf-8", errors="replace") if binary else result.stderr
        raise RuntimeError(f"Command failed ({result.returncode}): {error[-3500:]}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--duration", type=float)
    parser.add_argument("--fps", type=float)
    parser.add_argument("--size", help="Expected WIDTHxHEIGHT")
    parser.add_argument("--times", help="Comma-separated seconds; clamped to final decodable frame")
    parser.add_argument("--require-audio", action="store_true")
    parser.add_argument("--ffmpeg")
    parser.add_argument("--ffprobe")
    args = parser.parse_args()
    video = args.video.resolve()
    if not video.is_file() or video.stat().st_size == 0:
        raise ValueError(f"Missing or empty video: {video}")
    ffmpeg = tool_path("ffmpeg", args.ffmpeg, video)
    probe_hint = args.ffprobe
    sibling = Path(ffmpeg).with_name("ffprobe.exe" if sys.platform == "win32" else "ffprobe")
    if not probe_hint and sibling.is_file():
        probe_hint = str(sibling)
    ffprobe = tool_path("ffprobe", probe_hint, video)
    metadata = json.loads(run([ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video)]).stdout)
    visual = next((s for s in metadata["streams"] if s["codec_type"] == "video"), None)
    if not visual:
        raise ValueError("No video stream")
    audio = [s for s in metadata["streams"] if s["codec_type"] == "audio"]
    duration = float(visual.get("duration") or metadata["format"]["duration"])
    numerator, denominator = map(float, visual["avg_frame_rate"].split("/"))
    fps = numerator / denominator if denominator else 0
    if not math.isfinite(duration) or duration <= 0 or fps <= 0:
        raise ValueError("Invalid duration or frame rate")
    failures = []
    if args.duration is not None and abs(duration - args.duration) > max(0.06, 1.1 / fps):
        failures.append(f"Duration {duration} != expected {args.duration}")
    if args.fps is not None and abs(fps - args.fps) > 0.01:
        failures.append(f"FPS {fps} != expected {args.fps}")
    if args.size:
        width, height = map(int, args.size.lower().split("x"))
        if (visual["width"], visual["height"]) != (width, height):
            failures.append(f"Size {visual['width']}x{visual['height']} != expected {args.size}")
    if args.require_audio and not audio:
        failures.append("Expected an audio stream")
    requested = list(map(float, args.times.split(","))) if args.times else [duration * n / 5 for n in range(6)]
    if not 1 <= len(requested) <= 24 or any(not math.isfinite(t) for t in requested):
        raise ValueError("Provide 1–24 finite keyframe times")
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=True)
    frames = []
    times = [max(0, min(duration - 1 / fps, t)) for t in requested]
    for i, t in enumerate(times):
        destination = output / f"keyframe-{i:02d}-{t:.3f}s.png"
        run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t:.6f}", "-i", str(video), "-frames:v", "1", str(destination)])
        if not destination.is_file() or destination.stat().st_size == 0:
            raise ValueError(f"Could not decode keyframe at {t}s")
        frames.append(destination)
    # Remotion's lean FFmpeg does not necessarily include xstack/volumedetect.
    try:
        from PIL import Image
        columns = min(3, len(frames))
        tile_w = 480
        tile_h = round(tile_w * visual["height"] / visual["width"])
        canvas = Image.new("RGB", (columns * tile_w, math.ceil(len(frames) / columns) * tile_h))
        for i, frame in enumerate(frames):
            with Image.open(frame) as image:
                canvas.paste(image.convert("RGB").resize((tile_w, tile_h)), ((i % columns) * tile_w, (i // columns) * tile_h))
        sheet = output / "contact-sheet.jpg"
        canvas.save(sheet, quality=94)
    except ImportError:
        import html
        sheet = output / "contact-sheet.html"
        items = "".join(f'<figure><img src="{html.escape(frame.name)}"><figcaption>{t:.3f}s</figcaption></figure>' for frame, t in zip(frames, times))
        sheet.write_text('<!doctype html><meta charset="utf-8"><title>Video keyframes</title><style>body{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px}figure{margin:0}img{width:100%}</style>' + items, encoding="utf-8")
    # Decode the entire candidate: metadata alone does not establish decodability.
    run([ffmpeg, "-hide_banner", "-loglevel", "error", "-xerror", "-threads", "1", "-i", str(video), "-c:v", "rawvideo", "-threads:v", "1", "-c:a", "pcm_s16le", "-f", "null", "-"])
    audio_info = None
    if audio:
        sample_duration = min(duration, 60)
        decoded = run([ffmpeg, "-hide_banner", "-loglevel", "error", "-threads", "1", "-i", str(video), "-t", str(sample_duration), "-vn", "-ac", "1", "-ar", "8000", "-c:a", "pcm_s16le", "-f", "wav", "-"], binary=True).stdout
        with wave.open(io.BytesIO(decoded), "rb") as stream:
            samples = array("h", stream.readframes(math.ceil(sample_duration * 8000)))
        if sys.byteorder != "little":
            samples.byteswap()
        peak = max((abs(v) / 32768 for v in samples), default=0)
        rms = math.sqrt(sum((v / 32768) ** 2 for v in samples) / max(1, len(samples)))
        audio_info = {"sampled_seconds": sample_duration, "peak_dbfs": round(20 * math.log10(peak), 2) if peak else None, "rms_dbfs": round(20 * math.log10(rms), 2) if rms else None}
        if args.require_audio and not peak:
            failures.append("Audio stream is silent")
    report = {
        "video": str(video), "bytes": video.stat().st_size, "duration": duration,
        "fps": fps, "width": visual["width"], "height": visual["height"],
        "codec": visual["codec_name"], "audio_streams": len(audio), "audio_levels": audio_info,
        "full_decode": "passed", "keyframe_times": times, "keyframes": [str(p) for p in frames],
        "contact_sheet": str(sheet), "technical_failures": failures,
        "visual_review": "pending human or agent image inspection; this script does not score aesthetics",
    }
    (output / "media-evidence.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"technical_pass": not failures, "duration": duration, "fps": fps, "audio_streams": len(audio), "failures": failures, "report": str(output / "media-evidence.json"), "contact_sheet": str(sheet)}, ensure_ascii=False))
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, RuntimeError, OSError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(2)
