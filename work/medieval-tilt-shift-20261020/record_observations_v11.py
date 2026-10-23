"""Save actual producer observations, then finalize this delivered revision."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import subprocess
import sys

root = Path(__file__).resolve().parent
evidence = json.loads((root / 'qa/v11/producer-evidence-v11.json').read_text(encoding='utf8'))
video = Path(evidence['video'])
digest = hashlib.sha256(video.read_bytes()).hexdigest()
assert digest == evidence['video_sha256'] == 'ea895e3b1fa3dc6af62bc8aa7f24e92f2d4e243938c56668c4fe2f2ead6630e7'
viewed = [0, 12, 48, 96, 168, 288, 384, 504, 576, 647, 648, 756, 875, 876, 972, 1067, 1068, 1176, 1283, 1284, 1392, 1492, 1493, 1560, 1622, 1623, 1752, 1800, 1823]
assert [f['frame'] for f in evidence['extracted_frames']] == viewed
report = {
    'video': str(video),
    'video_sha256': digest,
    'created_at': datetime.now().isoformat(timespec='seconds'),
    'reviewer': 'production agent /root; non-independent producer verification',
    'actual_viewed_encoded_frames': viewed,
    'original_resolution_frames': [576, 1176, 1752],
    'contact_sheets': evidence['contact_sheets'],
    'method': 'Actually viewed all five labeled contact sheets (29 representative encoded frames, 270x480 cells), and full-resolution encoded frames 576, 1176 and 1752. No realtime playback or full-frame review.',
    'prior_continuous_sample': {
        'record': 'qa/v11/sample-encoded-evidence.json',
        'frames': [588, 659],
        'method': 'Existing producer record documents viewing all 72 consecutive encoded sample images. Reused as prior short-sample evidence, not claimed as a new full-film review.',
    },
    'actual_listened_ranges_seconds': [],
    'audio_perceived': False,
    'new_independent_review': False,
    'observations': [
        {'frames': [0, 12, 48, 96, 168], 'observation': 'Opening progresses from black through low horizon views into an elevated city view; the sampled later states show a narrow readable region with foreground and distance blur.'},
        {'frames': [288, 384, 504, 576, 647], 'observation': 'Blue glazed gate and street panels, gold royal sculpture, stalls, irregularly spaced residents and dispersed pack animals are visible. Full-size frame 576 shows separate small human groups and a laden donkey rather than a regular livestock line.'},
        {'frames': [648, 756, 875], 'observation': 'Loaded barges and sailing boats remain inside the canal; the sampled images show cargo and seats within their hulls.'},
        {'frames': [876, 972, 1067], 'observation': 'Garden terraces, steps and palms remain legible within the focused region.'},
        {'frames': [1068, 1176, 1283], 'observation': 'The two principal statues show faces and front or three-quarter bodies, distinct crowns and materials. Offering vessels, smaller figure, stela and guardian sculpture enrich the forecourt. The full-size frame retains focus on both main figures.'},
        {'frames': [1284, 1392, 1492], 'observation': 'New temple courtyard has a continuous open ground plane and accessible dais; no inherited cross-wall divides the court in these inspected views.'},
        {'frames': [1493, 1560, 1622], 'observation': 'Grain courtyard contains a blue canopy, goods, residents and separated pack animals; its setting differs from the processional avenue and temple forecourt.'},
        {'frames': [1623, 1752, 1800, 1823], 'observation': 'Final city view includes the new sites, canal, bridges, connected cross streets and repeated distant courtyard blocks. Full-size frame 1752 has a clear central band and progressive front/back defocus. Final inspected frame is black after the intended fade.'},
        {'frames': [647, 648, 875, 876, 1067, 1068, 1283, 1284, 1492, 1493, 1622, 1623], 'observation': 'The exact sampled frames immediately before and after these cuts contain complete scene images without intervening blanks among the inspected frames.'},
    ],
    'verification_limits': [
        '29 representative encoded frames and three full-size stills checked; no new full-film independent review.',
        'The 72-frame continuous sample is prior producer evidence and covers only a short street-to-canal passage.',
        'Actual listening unavailable; subjective musical timing, balance and listening quality remain unverified.',
        'Human and animal geometry and gait remain stylized for a miniature city; sampled views cannot establish all detailed collisions absent.',
        'Babylon-inspired fantasy city, not an archaeological reconstruction.',
    ],
}
path = root / 'qa/v11/producer-observations-v11.json'
path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
subprocess.run([sys.executable, '-X', 'utf8', str(root / 'finalize_delivery_v11.py')], check=True)
