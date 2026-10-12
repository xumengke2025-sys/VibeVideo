# Independent forward test: mechanical / data request

Objective: create a 9:16 mechanical/data animation while preserving facts, choosing different creative events, observing dynamics, and keeping the video rebuildable. This fixture tests workflow behaviour; it is not a professional visual-quality demonstration.

Three event candidates:
1. Cutaway reveal: start at the sealed contact, pull back to reveal the fixed spring end, and then apply pressure. Viewer discovers the structure. Cost: camera and annotation re-layout; local cutaway geometry sufficient.
2. Threshold and response: pressure and travel share a data state; input crosses preload, disc opens to a stop, pressure reverses, disc reseats. Viewer reads cause and constraint. Cost: lowest; quasi-static schematic is enough, no impact/flow claim.
3. Counterfactual comparison: same pressure applied to two preload settings produces different opening thresholds on stable axes; join both traces at the final contact. Viewer compares mechanism parameters. Cost: two systems and longer reading time; avoid inventing real valve specifications.

Selection: candidate 2 directly tests correct seat contact, stroke clamp, fixed spring end and stable data scale in one short window. The other choices reveal structure or compare parameters; they are different event logics, not palette/angle changes.

Fact boundary: arbitrary dimensionless illustrative parameters; force = pressure * area; equilibrium travel = clamp((force - preload) / stiffness, 0, stroke). No damping, inertia, fluid particles, impact or transient flow claim. Negative pressure leaves the valve seated. Spring compression and disc travel share one state.

Timeline: 0–0.4s seated; 0.4–1.0s raise pressure past threshold; 1.0–1.25s stop-limited; 1.25–1.8s reduce through reseating; 1.8–2.0s seated under reverse pressure. Silent fixture. One fixed camera is purposeful at critical contact.

Rebuild: run `node check_tools.mjs`, then bundled Python `build_fixture.py`, then `creative_review.py prepare plan.json fixture.mp4 --out qa --width 360 --type mechanical-data --ffmpeg ... --ffprobe ...`. All source and states are local; these scripts preserve the fixture's parameter/state relation.
