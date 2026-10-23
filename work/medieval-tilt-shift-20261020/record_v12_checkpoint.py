"""Keep the existing film handoff current; no review claims are inferred."""
import json, sys, datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'CHECKPOINT.json'
d=json.loads(p.read_text(encoding='utf8'))
d['status']=sys.argv[1] if len(sys.argv)>1 else 'v12_final_quality_sample_rendering'
d['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=d['v12_revision']
r.update({
 'model':'model/babylon-city-v12.blend',
 'renderer':'render_city_v12.py',
 'pipeline':'render_pipeline_v12.py',
 'timeline':'v12-timeline.json',
 'traffic':'traffic-v12.npz',
 'revision_plan':'v12-修复计划.md',
 'model_evidence':'qa/v12/model-evidence.json',
 'layout_evidence':'qa/v12/layout-evidence.json',
 'frozen_manifest':'render/frozen-v12-manifest.json',
 'screen_layout_checked':{'patrol':{'times':[16.5,22,26.5],'inside_frame':'10/10'},'tow_teams':{'times':[27.5,31.5,36],'inside_frame':'8/8'}},
 'completed':['v11 isolated green/bright frames 24 and 1115 diagnosed',
  'Replaced unstable Defocus with multi-level Gaussian CoC; GPU compositing avoids CPU memory allocation failures in final-model samples',
  'priest, acolyte, Babylonian guard/patrol, Egyptian envoy and attendant role meshes built',
  '8582 additional solid street citizens including 936 independently moving mid-distance actors',
  '180 additional nearby citizens with cached avoidance',
  '4 painted square-sail merchant craft with 8 additional aboard crew; existing barges painted and cargo accented',
  '2 tow teams with 8 modeled workers and animated connected ropes',
  'layout projections place 10 patrol members and 8 tow workers within their shot windows',
  'excluded livestock from human profession reassignment; rebuilt final model',
  'raised continuous towpath with two passing lanes removes house occlusion; feet rest on real quay height',
  '37 final-model formal-size sample frames rendered and passed strong-green corruption scan',
  'producer viewed final-model canal frame 744: both teams and connected ropes clearly visible'],
 'verification_limits':['No new independent review round. Previous review remains bound to its historical output.',
  'Full encoded-film visual and temporal checks pending; final-model canal frame 744 viewed.',
  'Audio excerpt unchanged; actual subjective listening is not claimed.'],
 'full_render_session':44518,
 'render_status':'render/pipeline-status-v12.json',
 'next_action':'Continue full 1824-frame render; scan temporal faults; encode and check current output.'
})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print(d['status'])
