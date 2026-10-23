# 雾金之城

- Objective: 90-second editable 18th-century fantasy miniature city film.
- aspect_ratio: 9:16; width: 1080; height: 1920; fps: 24; frames: 2160.
- delivery_mode: ai_review_once. Independent review used: 0; repair rounds used: 0.
- User authorized continuous progress after concept presentation; no repeated approval.
- Completed: read AGENTS, vibe-video and miniature-city reference; inspected Babylon v13 render/compositor/traffic/geometry/pipeline code; verified Blender 4.5.3 and Python 3.12/numpy/Pillow.
- Old project stays intact. New geometry, roads, actors, camera and score are independently generated here. No runtime dependency on Babylon models/caches.
- Music directory contains only previous Babylon music. Original score will use locally available GeneralUser GS sampled instruments; license permits music creation. Soundfont copied with license.
- Visual direction: warm limestone/old brick/copper, canal as continuous north-south spine; cathedral west, working quays east; single east-west counterweight bascule bridge.
- Next: implement shared world and actual-resolution concept render, then full bridge sample, extend film, engineering checks and one independent review.
- Audio perception: no tool found that exposes actual audio to model; do not claim listening completed. This does not prevent producing/mixing audio.

## User feedback / 2026-10-22
- User saw concept/v3/02064.png: city looks too flat; requests mountain-city character and stronger real height/depth.
- Supersedes flat city visual layout. Retain valley canal and bridge event, rebuild terrain and elevated districts before sample/full render.
- Preserve prior model/source in history/flat-city-before-mountain-feedback. No full-film/sample render has been started. Review budget still unused (0).
- Completed before feedback: city models, original 90s sampled score + separate foley stems, absolute-time animation, concept renders. Corrected submerged hull, CoC texture dimensions, counterweight length/height, roadway footprints and horse stance.
- Next: terraced high ground, cathedral acropolis, connecting stairs/ramps, elevated residential tiers, stronger occlusion/parallax; show new 9:16 concept. Continue under user's standing authorization.

## Mountain implementation / latest steering
- User further requests grandeur, architectural diversity and eighteenth-century beauty; may reference period oil paintings.
- Actually viewed Met public-domain Canaletto, Piazza San Marco (late 1720s), object 435839, and Hubert Robert, The Portico of a Country Mansion (1773), object 437468. Local reference images in references/. Adopting facade rhythm, small human scale, porticoes, stone stairs, warm illuminated masonry and layered depth; no painting texture pasted into film.
- New src/terrain.py shared relief model; src/mountain_city.py varied mansard/hip/gable houses, courtyard palazzi, ridge rotundas and connected roads; src/ceremonial_terrace.py cathedral raised to 32m with ceremonial stairs. Flat history preserved.
- Camera updated for mountain composition; focus band broadened and strength reduced to preserve architectural depth.
- Mountain build and concepts completed, subsequently superseded by organic-city correction below.
- Still no sample/full render or independent review. Latest static .blend may be overwritten only after build succeeds.

## Organic city correction / latest user feedback
- User rejected regular mountain-v3 layout: still too orderly and not convincing as an eighteenth-century fantasy steam city. Do NOT expand that version into film.
- Saved regular mountain source/model/brief under history/regular-mountain-before-organic-feedback/.
- Actually viewed references/Prague-historical-aerial-55819439.jpg (historic aerial, ETH via Commons) and Prague-St-Nicholas-aerial.jpg. Metadata saved in prague-aerial-metadata.json. These reference later photographs, not evidence of an unaltered 18th-century city; adopt street fabric only, exclude modern objects.
- Read UNESCO Edinburgh urban heritage atlas for ridge spine, narrow branching closes and dense perimeter frontages. https://whc.unesco.org/en/urban-heritage-atlas/edinburgh/
- Implemented generate_layout.py with local vendor/urban SciPy+Shapely. Generates model/urban-layout.json: 613 irregular blocks, 1426 road segments and curved arteries, reserved landmarks/industry/plazas.
- New organic_city.py maps connected perimeter parcels to actual irregular quadrilateral building footprints; creates winding roads, internal courtyards and gardens. mountain_city.py now keeps architecture helpers and executes organic_city.py; old grid generator removed from active source.
- Organic builds and concept/organic-v1 succeeded. Actually inspected final overview frame 2064 and bridge frame 1200; showed overview to user. Street fabric is now visibly irregular and elevation layered. New actor routes follow urban-layout roads.
- Fixed arterial/landmark intersections, moved western quay lane out of cathedral podium, moved stairs to the west with terrain clearance, moved street trees and crates out of vehicle lanes, separated background carriages. Organic build v3 succeeded (render/organic-build-v3.log); 1438 road segments. Rendering concept/organic-v2 opening, bridge and finale states before formal continuous sample.
- Final pre-sample build v4 succeeded; ships moved to ±6m side lanes so the bell barge has 1.24m lateral clearance; spectator positions corrected. Opening hill now includes fixed grass and limestone outcrops. Cool skylight increased modestly to retain readable shadow detail.
- src/verify_constraints.py passed: no roads overlap reserved footprints; minimum open-leaf side clearance 4.63m; stern clear of bridge by 0.948m when lowering starts; horse nose stays 4.05m from gate while waiting. Evidence qa/constraints.json; this is envelope checking, not complete mesh collision proof.
- Formal sample v1 was stopped during production after discovering puff hide-at-lifetime-end could pop. Existing frames preserved. Added independent per-puff density with continuous emergence/dissipation; started version organic-final-v2, frames 960–1727, 1080×1920, 32-sample Cycles. Log render/sample-organic-final-v2.log; authoritative progress render/status.json. Current render session 40814 (Blender PID comes from status.json). Do not modify frozen rendering inputs while this version is running.
- src/open_editable.py successfully loaded model and calculated frame 1201 in Blender; evidence qa/editor-smoke.log. README and PowerShell production/editing launchers created. No sample/full MP4 completed yet; independent reviewer count remains 0. Full delivery objective remains active.

## User-authorized resource pause / 2026-10-23
- User in Babylon task explicitly authorized: 允许，优先完成巴比伦. Mist Gold render queue paused; existing frames and frozen inputs preserved.
- Pause marker: render/PAUSED-FOR-BABYLON.json. src/pipeline.py waits while this marker exists. Do not restart a direct Blender render while Babylon v14 is active.
- Resume existing sample version organic-final-v2 after Babylon releases the GPU; missing-frame resume is supported.
