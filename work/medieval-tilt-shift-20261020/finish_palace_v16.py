"""Run the authorized complete film; persist exact state even across chat turns."""
from pathlib import Path
import sys,subprocess,json,datetime,traceback
P=Path(__file__).resolve().parent;cp=P/'CHECKPOINT-v16.json'
def update(status,next_action,**extra):
 c=json.loads(cp.read_text(encoding='utf8'));c.update(status=status,next_action=next_action,updated_at=datetime.datetime.now().astimezone().isoformat(),**extra)
 cp.write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf8')
update('full_render_running','Render frozen v16, with 27-29s palace excerpt first; then full 2160 frames, temporal scan, encode and decode. Actual final picture observations remain pending.')
try:
 subprocess.run([sys.executable,'-X','utf8',str(P/'render_pipeline_v16.py'),'full'],cwd=P,check=True)
 report=json.loads((P/'delivery/engineering-check-v16.json').read_text(encoding='utf8'))
 assert report['decode_exit']==0 and report['frames']==2160
 subprocess.run([sys.executable,'-X','utf8',str(P/'prepare_final_evidence_v16.py')],cwd=P,check=True)
 update('candidate_encoded_pending_final_view','Full shot-cache baseline and encoded representative images are ready. View qa/v16/final-encoded/index.json and the necessary adjacent windows, then display the final file with the actual producer-only verification scope.',final_candidate=report['video'],final_sha256=report['sha256'],unresolved=['Final encoded picture inspection pending','Actual listening unavailable'])
 marker=P.parent/'mist-gold-city-20261022/render/PAUSED-FOR-BABYLON.json'
 if marker.exists():
  saved=json.loads(marker.read_text(encoding='utf8'))
  if saved.get('authorization')=='允许，优先完成巴比伦':
   (P/'render/released-mist-gold-priority-after-v16.json').write_text(json.dumps({'released_at':datetime.datetime.now().astimezone().isoformat(),'prior_marker':saved,'reason':'v16 encoded and fully decoded. No other renderer started.'},ensure_ascii=False,indent=2),encoding='utf8');marker.unlink()
 print('V16_PALACE_FILM_READY',report['video'],flush=True)
except Exception:
 update('render_requires_attention','Inspect render/palace-v16.stderr.log and render/pipeline-status-v16.json; preserve finished frames and resume missing targets.')
 traceback.print_exc();raise
