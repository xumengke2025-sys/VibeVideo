"""Bind the actual review coverage to the final rendered artifacts."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
skill = Path('D:/Codex/skills/vibe-video')


def read(relative):
    return json.loads((root / relative).read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


video = root / 'demo/out/continuity-study.mp4'
audit = read('demo/out/frame-audit-final/frame-audit.json')
media = read('demo/out/evidence/media-evidence.json')
render = read('demo/out/render-check.json')
assert digest(video) == audit['video_sha256']
assert media['full_decode'] == 'passed' and not media['technical_failures']
assert audit['source_frame_count'] == audit['exported_frame_count'] == 240
assert render['out_of_order_seek'] == render['loop_endpoints'] == 'passed'

review = {
    'method': 'Agent visual inspection of continuous-frame contact sheets and selected full-size frames',
    'inspected_atlases': [f'demo/out/frame-audit-final/atlas-{i:03d}.jpg' for i in range(8)],
    'thumbnail_frame_coverage_inclusive': [0, 239],
    'full_size_frames_inspected': ['demo/out/frame-audit-final/frames/frame-000173.jpg'],
    'observations': [
        'One container persists through button, loading, slider, graph, check and button.',
        'One point-corresponded line persists through slider, graph and check.',
        'The final 5.767-second frame keeps both curve endpoints inside the rounded mask.',
        'First and final contact-sheet states agree; both ends hold still.',
    ],
    'repair': {
        'issue': 'Container shrink outpaced line morph; endpoints touched the rounded clipping mask.',
        'before': 'demo/out/evidence/line-clipping-before.jpg',
        'after': 'demo/out/frame-audit-final/frames/frame-000173.jpg',
        'change': 'Curve-to-check morph duration adjusted from 0.42 to 0.36 seconds.',
    },
    'realtime_playback': False,
    'audio_listened': False,
    'all_full_size_frames_inspected': False,
    'independent_reviewer': False,
}

sources = []
for name in ['twoclipping-original', 'twoclipping-remake', 'koldo2k-original', 'ror-fly-original']:
    item = read(f'evidence/{name}/media-evidence.json')
    source_video = Path(item['video'])
    sources.append({
        'id': name,
        'video_sha256': digest(source_video),
        'media_report': f'evidence/{name}/media-evidence.json',
        'duration': item['duration'],
        'fps': item['fps'],
        'audio_streams': item['audio_streams'],
        'full_decode': item['full_decode'],
        'inspected_sparse_times_seconds': item['keyframe_times'],
        'contact_sheet_inspected': f'evidence/{name}/contact-sheet.jpg',
    })

windows = []
for name in ['ui-handoff', 'portal-handoff', 'portal-crossing', 'portal-exit']:
    item = read(f'evidence/{name}/frame-audit.json')
    windows.append({
        'id': name,
        'video_sha256': item['video_sha256'],
        'inspected_window_frames_inclusive': item['window_inclusive'],
        'inspected_atlases': [f'evidence/{name}/{atlas}' for atlas in item['atlases']],
        'coverage': 'All thumbnail states in the listed continuous windows were visually inspected.',
    })

evidence = {
    'checked_date': '2026-10-09',
    'objective': 'Study the public gallery, migrate reusable mechanisms into vibe-video and verify a local Codex implementation path.',
    'status': 'complete',
    'upstream': {
        'repository': 'https://github.com/yihui-dev/awesome-opus5-5-videos',
        'commit': '756290289742535eb0ac3817548f152e9759cc70',
        'entries': 513,
        'partial_prompts': 234,
        'unique_raw_prompt_texts': 459,
        'technology_tags_describe': 'Skillry remakes, not verified original engines',
    },
    'skill': {
        'path': str(skill),
        'version': '0.5.0',
        'format_validation': 'quick_validate.py passed in the earlier task execution',
        'sha256': {name: digest(skill / name) for name in [
            'SKILL.md', 'agents/openai.yaml', 'scripts/opus_gallery.py',
            'assets/opus-gallery.json', 'assets/opus-gallery-LICENSE.txt',
            'assets/continuity.mjs', 'references/opus-gallery.md',
            'references/verified-experience.md', 'references/sources.md',
        ]},
    },
    'gallery_verification': read('gallery-verification.json'),
    'motion_verification': read('continuity-verification.json'),
    'source_media_observation': sources,
    'source_continuous_windows': windows,
    'final_demo': {
        'video': str(video),
        'sha256': digest(video),
        'media_report': 'demo/out/evidence/media-evidence.json',
        'frame_report': 'demo/out/frame-audit-final/frame-audit.json',
        'render_report': 'demo/out/render-check.json',
        'source_sha256': {name: digest(root / 'demo' / name) for name in ['index.html', 'continuity.mjs', 'render.mjs']},
        'duration_seconds': media['duration'],
        'size': [media['width'], media['height']],
        'fps': media['fps'],
        'frames': audit['source_frame_count'],
        'audio': False,
        'full_decode': media['full_decode'],
        'review': review,
    },
    'limits': [
        'No complete original-author animation project was obtained.',
        'Most gallery entries were indexed or read as public text rather than watched.',
        'No equivalent-budget cross-model comparison was performed.',
        'Glass, physical refraction/caustics, arbitrary glyph morphing and complex 3D were not implemented in this demo.',
        'Logarithmic zoom was numerically tested; a complete portal scene was not rendered in this demo.',
        'Source videos were decoded and inspected as sampled or continuous frame images, without realtime playback or listening.',
        'The final demo validates specific continuity mechanisms and export, not parity with every gallery work.',
    ],
}
(root / 'research-evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': 'complete', 'evidence': str(root / 'research-evidence.json'), 'final_video_sha256': digest(video)}, ensure_ascii=False))
