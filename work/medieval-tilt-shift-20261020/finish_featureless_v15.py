"""Finish the authorized film and record exact completion/failure, without new agents."""
from pathlib import Path
import subprocess,sys,json,datetime,traceback
P=Path(__file__).resolve().parent
cp=P/'CHECKPOINT-v15.json'
def update(status,next_action,**extra):
    c=json.loads(cp.read_text(encoding='utf8'));c.update(status=status,next_action=next_action,updated_at=datetime.datetime.now().astimezone().isoformat(),**extra)
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf8')
update('full_render_running','Continue frozen v15 bounded render, temporal scan, encode and decode checks. Producer final observations remain pending.')
try:
    subprocess.run([sys.executable,'-X','utf8',str(P/'render_pipeline_v15.py'),'full'],cwd=P,check=True)
    report=json.loads((P/'delivery/engineering-check-v15.json').read_text(encoding='utf8'))
    assert report['decode_exit']==0 and report['frames']==2160
    update('candidate_encoded_pending_final_view','View current final film and necessary adjacent windows. Deliver current film with producer-only visual scope and actual-listening limitation. No new independent review round.',final_candidate=report['video'],final_sha256=report['sha256'],unresolved=['Final encoded picture inspection pending','Actual listening unavailable'])
    # Release only the explicit Babylon-priority marker. Do not launch another film.
    marker=P.parent/'mist-gold-city-20261022/render/PAUSED-FOR-BABYLON.json'
    if marker.exists():
        saved=json.loads(marker.read_text(encoding='utf8'))
        if saved.get('authorization')=='允许，优先完成巴比伦':
            history=P/'render/released-mist-gold-priority-after-v15.json'
            history.write_text(json.dumps({'released_at':datetime.datetime.now().astimezone().isoformat(),'reason':'Superseding v15 film rendered, encoded and decoded successfully. No renderer auto-started.','prior_marker':saved},ensure_ascii=False,indent=2),encoding='utf8')
            marker.unlink()
    print('FEATURELESS_V15_CANDIDATE_READY',report['video'],flush=True)
except Exception:
    update('render_requires_attention','Inspect render/featureless-v15.stderr.log and render/pipeline-status-v15.json; preserve completed frames and resume missing targets.')
    traceback.print_exc();raise
