from pathlib import Path
import json,hashlib,wave
ROOT=Path(__file__).resolve().parent
plan=json.loads((ROOT/'plan.json').read_text(encoding='utf8'))
timeline=json.loads((ROOT/'v8-timeline.json').read_text(encoding='utf8'))
freeze=json.loads((ROOT/'render/frozen-v8-manifest.json').read_text(encoding='utf8'))
assert plan['version']=='v8' and (plan['width'],plan['height'])==(1080,1920)
assert plan['delivery_mode']=='ai_review_once'
assert len(plan['shots'])==len(timeline['shots'])==7
for i,s in enumerate(plan['shots']):
 a,b=timeline['shots'][i][:2];assert (s['start'],s['end'])==(a,b)
 assert s['camera']['path']==timeline['shots'][i][2:]
 assert all(a<=v<=b for v in s['states'].values())
for key,path in [('model_sha256','model/babylon-city-v8.blend'),('renderer_sha256','render_city_v8.py'),('timeline_sha256','v8-timeline.json')]:
 assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==freeze['sample'][key],path
with wave.open(str(ROOT/'audio/final-mix-v8.wav'),'rb') as w:
 audio={'rate':w.getframerate(),'channels':w.getnchannels(),'duration':w.getnframes()/w.getframerate()}
 assert audio=={'rate':48000,'channels':2,'duration':56.0}
report={'plan_and_renderer':'7 matching shots, continuous 0–56s timeline','format':'1080x1920 / 24fps','source_hashes':'unchanged since verified sample','audio':audio,'actual_audio_perception':False,'scope':'mechanical consistency, not an aesthetic or listening approval'}
(ROOT/'qa/v8/frozen-consistency.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report))
