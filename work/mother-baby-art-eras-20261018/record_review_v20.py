from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;Q=R/'qa/v20'
read=lambda p:json.loads((Q/p).read_text(encoding='utf8'))
eng=read('final/engineering-check.json');actor=read('final/infant-capture.json');env=read('final/environment-capture.json')
assert eng['sha256']==actor['video_sha256']==env['video_sha256']
for n in ['mechanical-check.json','transition-check.json','fixed-layer-check.json']:assert not read(n)['issues'],n
assert read('environment-check.json')['outside_mask_pixels']==0
files=['film/sequences-v20.js','film/environment-life-v20.js','film/environment-stopmotion-v15.js','film/transitions-v16.js','render-v20.mjs','render-batched-v20.mjs','assets/motion-v20/manifest.json','assets/motion-v20/cushions-atlas.png']
report={
 'version':20,'date':'2026-10-23','video_sha256':eng['sha256'],
 'reviewer':'production agent; non-independent targeted verification',
 'delivery_mode':'ai_review_once','historical_independent_round_exhausted':True,'new_independent_review':False,
 'changes':['Stationary cushion layer with fixed rectangle [310,1435,290,87]; era material blends only.','Original deforming cushion removed through local alpha masks; no new actor coordinate mapping or scale.','Rooted local foliage, lantern and textile motion in 19 applicable eras; existing outdoor motion retained.'],
 'engineering':eng,
 'mechanical':['39 atlases / 1291 cels: retained RGB unchanged, upper-body alpha unchanged, no solid canvas-border pixels, hashes match.','19 actor bridge endpoints and routing match.','20 isolated cushion layers identical at three times per era.','19 room-transition endpoints and random-access results match.','19 applicable indoor-motion eras have changing detail pixels; 0 outside-mask pixels exceed 3 RGB levels.'],
 'actually_viewed':{
   'method':'Ordered time-labelled contact sheets and cropped detail pairs; no claim of normal-speed full-film playback.',
   'preencode':'20 eras x 5 final actor/fixed-cushion samples: fixed-cushions-0.jpg through -3.jpg.',
   'encoded_actor_frames':actor['era_sample_frames'],'encoded_consecutive_frames':actor['continuous_frames'],'encoded_unique_actor_frames':actor['captured_frames'],
   'encoded_full_frames_seconds':[.8,18.8,36.9,39.2],
   'encoded_background_pairs':env['background_pairs'],'encoded_join_35_frames':env['join_35_frames'],
   'encoded_room_transition_seconds':[37.75+j/24 for j in range(12)]},
 'findings':['Viewed samples retain a fixed support while the infant changes pose. Cushion material changes during era bridges without position or size changes.','Inspected contact and handoff windows preserve the original v19 interactions; 35-second render-batch join shows consecutive action.','Encoded lantern/tassel and hanging-vine pairs show localized movement; curtain movement is subtle.'],
 'remaining_limits':['Original RIFE inbetweens retain translucent/soft hands and props, costume morphing and a few small dark flecks. These were not regenerated in v20.','No new independent or full-film aesthetic approval. Silent output has no listening coverage requirement.'],
 'runtime_sha256':{n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in files}
}
(Q/'production-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'video_sha256':eng['sha256'],'encoded_actor_frames_viewed':actor['captured_frames'],'new_independent_review':False}))
