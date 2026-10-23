from pathlib import Path
import json,re,sys
root=Path(__file__).resolve().parent
version=sys.argv[1]
voice=json.loads((root/'audio/timing.json').read_text(encoding='utf-8'))
film=(root/'film.js').read_text(encoding='utf-8')
block=film.split('export const captions=[')[1].split('function subtitle()')[0]
caps=[(float(a)/1.25,float(b)/1.25) for a,b in re.findall(r'\[([\d.]+),([\d.]+),',block)]
checks=[dict(id=e['id'],caption_start=c[0],caption_end=c[1],voice_start=e['start'],voice_end=e['end'],covered=c[0]<=e['start']+.001 and c[1]+.001>=e['end']) for c,e in zip(caps,voice['entries'])]
stills=json.loads((root/f'out/stills-{version}/checks.json').read_text(encoding='utf-8'))
report={'version':version,'duration':voice['duration'],'audio_peak':voice['peak'],'caption_checks':checks,'caption_count_matches':len(caps)==len(voice['entries']),'runtime_errors':stills['errors'],'seeks':stills['seeks'],'production_visual_observation':'Actual full-size frames viewed at 20.4s expert hall, 28.4s knowledge, 36.4s outputs; clear main labels and visible quantity/category structure. Not all-frame or independent review.','audio_perception':'not_completed','independent_review':'not_repeated; V1 review not valid for this version'}
(root/f'qa/{version}-production-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
assert report['caption_count_matches'] and all(c['covered'] for c in checks)
assert not stills['errors'] and all(c['identical'] for c in stills['seeks'])
print(json.dumps({'caption_timing':'passed','determinism':'passed','duration':voice['duration'],'peak':voice['peak']}))
