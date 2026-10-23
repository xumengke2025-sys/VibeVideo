from pathlib import Path
import json
root=Path(__file__).resolve().parent
p=root/'brief.json';b=json.loads(p.read_text(encoding='utf-8'))
b['review'].update(status='incomplete: v1 full-frame visual review; v2 local recheck completed; actual audio and realtime playback unavailable',current_version='final-v2',current_sha256='52199ecd265b6a08426153ed94ff40fe91e3b08c4419f19706412bac3e4c7e83',resolved=['V1-01','V1-02','V1-03'],remaining=['V2-01 minor: point approach amplitude weak'],v2_visual_ranges=[[60,389],[750,839]])
p.write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf-8')
