# Independent forward test

Test performed in a dedicated task directory without editing the skill or the main agent's production examples. The tested request was a portrait mechanical/data animation that must preserve facts, develop different creative events, actually inspect continuous motion, and remain rebuildable.

## What was exercised

- Read the current main skill plus director-design, motion-craft, visual-review, opus-methodology, mechanical/motion tools, and the executable review scripts.
- Recorded three different event candidates (structure reveal, force threshold, parameter counterfactual), selected the threshold mechanism, and stated the fact boundary.
- Generated a two-second 1080×1920 / 30 fps silent MP4 from shared analytical valve states. The MP4 is 79,476 bytes, SHA256 `b7d5f84612f1e891ef185b0b4488650e9011db9e22d87ef5fb98b2c07090f748`. Full decode passed in media-evidence.json. This is a workflow fixture, not a quality benchmark.
- Ran creative_review prepare with bundled FFmpeg/ffprobe; it extracted all representative states and two risk windows.
- Actually inspected the three representative full-size images and both atlas pages (source frames 12–36 and 45–57). Method: continuous-frame contact sheets, not realtime playback. No audio was present or reviewed. There were no aesthetic scores.
- Observed opening after preload, travel saturation, spring compression at a fixed far end, and reseating without going through the seat. Found a small spring/disc attachment gap and missing y-axis label in the fixture; these are visible fixture defects, so no educational delivery-quality claim is made.
- Ran eight independent constraint/determinism assertions, then two fresh Node processes with identical analytical-state SHA256. Ran the skill's test-motion.mjs: three tests passed. Ran style-studio/test-contract.mjs: passed.
- Ran index validate: 37 cards, 513 indexed entries, 688 source hashes, no errors. Checked code-only mechanical/data retrieval, mechanical card operation fields, generated-video provenance trace, and film-only exclusion of component references. Exact index outputs are local JSON files.

## Initial failures and reproduction

1. Windows path separators rejected genuinely filled continuous-page records. Initial `prepare` emits `window-00/atlas-000.jpg`; initial `check` used `str(Path(report).parent / page)`, yielding native `window-00\\atlas-000.jpg`. Copying the supplied required_pages to viewed_pages, after actually inspecting those pages, failed with both windows marked unobserved. Changing only the path strings to native separators made the same log pass. Original case results are in before-fix/observed-result.json and before-fix/observed-native-paths-result.json. Minimum fix: normalize compared page paths on both sides, such as Path(...).as_posix().
2. A valid single-shot plan with risks=[] and an observed log with continuous=[] returned success despite only static evidence. Reproduce with no-risks-static-only-plan.json and qa/no-risks-static-only.json. Original success is preserved in before-fix/no-risks-static-only-result.json. Minimum fix: generate a default action window for no-window plans in both prepare and check, or explicitly require continuous evidence in creative_review without breaking the older shot_contract interface.
3. A log reduced to one dimension, idea with weight 100, returned success without any motion/composition/correctness dimension. Original success is preserved in before-fix/idea-only-no-correctness-result.json. Minimum fix: require those three evidence dimensions with positive adjustable weights; correctness cannot be removed for mechanical/data work.

The parent agent implemented those fixes in the production skill. This tester did not edit production files.

## Post-fix regression

Ten cases now produce the expected result. qa/*-result.json and review-test-results.json retain exact output and the tested script hashes:

|Case|Expected|Observed exit|
|---|---|---|
|prepare paths observed|accept consistency only|0|
|native Windows paths observed|accept consistency only|0|
|pending review|reject|2|
|old top-level video hash|reject|2|
|missing continuous evidence|reject|2|
|continuous pages not viewed|reject|2|
|single shot, no declared risks, static-only review|reject|2|
|idea only, no motion/composition/correctness|reject|2|
|invalid weights|reject|2|
|stale continuous audit hash|reject|2|

Also reran prepare on the no-risk plan in a fresh qa-fallback directory. It successfully extracted a real fallback window covering source frames 15–36 and kept the log pending. This verifies extraction, not a new observation claim. The fallback has finite coverage; plans must still declare mechanism/contact risks rather than assume this one window covers every transition.

## Operational metadata limitation

All three distinct minimum_verification entry files exist and their CLI flags are real. The motion and contract commands actually pass. The reveal-path minimum command, run from the skill directory with its output redirected to this test directory, fails immediately at cinematic-starter/render.mjs:5 with `MODULE_NOT_FOUND: playwright-core`. The renderer explicitly requires package dependencies; they are not installed beneath the archived skill project. There is no invalid entry path. The card should tell the next agent to use a task copy with installed dependencies, or provide explicit existing --playwright and --three paths. No dependencies were installed and no third-party renderer was claimed to have run.

## Rebuild and evidence

Sources: check_tools.mjs -> states.json -> build_fixture.py -> fixture.mp4. See creative-direction.md for selection and fact boundary. Build uses the bundled Python supplied in the task and bundled Remotion FFmpeg. Run_review_tests.py reconstructs review negative cases and the index output; observations are explicit records of this tester's actual image inspection, never automatically inferred from extraction.

The consistency checker accepts observation records, not visual quality. It cannot prove that an agent truly watched the stated pages, that aesthetic judgement is correct, or that this minimal fixture matches a high-quality external film.
