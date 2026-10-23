from pathlib import Path
from datetime import datetime, timezone
import json
P=Path(__file__).resolve().parent
s=(P/'finalize_delivery_v13.py').read_text(encoding='utf8').replace('v13','v14')
s=s.replace('1176,1392,1560','1176,1320,1356,1373,1392,1428,1464,1476,1492,1560')
s=s.replace("('opening-old-flash',12)","('opening',36)")
s=s.replace("('garden-repaired-flash',922)","('garden',922)")
s=s.replace("('statue-old-flash',1103)","('statue',1103)")
s=s.replace("('avenue-panorama',1740)","('offering-transfer',1362),('offering-placement',1452),('ritual-next-cut',1482),('avenue-panorama',1740)")
(P/'finalize_delivery_v14.py').write_text(s,encoding='utf8')
cp=json.loads((P/'CHECKPOINT-v14.json').read_text(encoding='utf8'))
cp.update(status='production_samples_rendering',updated_at=datetime.now(timezone.utc).isoformat(),completed=['Built independent v14 Blender model; v13 preserved','119 grouped citizens have >1.10m placement clearance and reduced idle motion','New continuous offering handover and altar placement; sampled arm reach 0.469m','Added roof/garden props, subtle building variation and cedar sanctuary doors','Changed water noise to world scale and added 5 boat wake systems','Dynamic focus band follows patrol, boat and offering; final panorama opens focus','Created 76-second scene-specific original ambience mix with unchanged music excerpt','Viewed formal proof frames 756 and 1373 after water/door fixes'],verification=['Actual viewed final-model proof images: render/proof-v14-final/00756.png and 01373.png','Audio technical measurements: -17.30 LUFS, -2.29 dBTP, 48kHz stereo; not listened','Initial GPU memory/driver failures occurred under shared-machine pressure; final proof process completed successfully'],unresolved=['Continuous action and shimmer samples still rendering','Full 1824-frame render and encoded output checks pending','Actual listening unavailable'],next_action='Inspect canal and complete offering sample; freeze accepted input hashes and render full sequence; encode and verify v14.')
(P/'CHECKPOINT-v14.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2),encoding='utf8')
main=json.loads((P/'CHECKPOINT.json').read_text(encoding='utf8'))
main.update(status='v14_user_authorized_revision_in_progress',updated_at=cp['updated_at'],active_revision_checkpoint='CHECKPOINT-v14.json',next_action=cp['next_action'])
main['v14_revision']={'authorized':'User: 好执行以上优化','checkpoint':'CHECKPOINT-v14.json','protected_prior_delivery':main.get('final_candidate'),'delivery_mode':'ai_review_once','review_scope':'Existing round exhausted; producer verification only'}
(P/'CHECKPOINT.json').write_text(json.dumps(main,ensure_ascii=False,indent=2),encoding='utf8')
print('V14_CHECKPOINT_AND_FINALIZER_READY')
