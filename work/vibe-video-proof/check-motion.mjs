import assert from 'node:assert/strict';
import {clamp, progress, seeded, rotate3, project3, worldToScreen} from './motion.mjs';

// Arbitrary frame/time access must not depend on previous evaluations.
const evaluate = time => project3(rotate3({x: 350, y: 80, z: -120}, time * 0.27, -0.2), {cx: 960, cy: 540});
const reference = evaluate(7.2);
evaluate(0); evaluate(11.9); evaluate(3.4);
assert.deepEqual(evaluate(7.2), reference);

// Camera focal point remains at viewport center for every zoom.
for (const zoom of [0.5, 1, 2.5]) {
  assert.deepEqual(worldToScreen({x: 1200, y: 700}, {x: 1200, y: 700, zoom}, {width: 1920, height: 1080}), {x: 960, y: 540});
}
assert.equal(project3({x: 0, y: 0, z: -1400}, {cx: 0, cy: 0}), null);
const a = seeded(731), b = seeded(731);
for (let i = 0; i < 560; i++) assert.equal(a(), b());
assert.equal(progress(-1, 0, 2), 0);
assert.equal(progress(5, 0, 2), 1);
assert.equal(clamp(-0.5), 0);
assert.equal(clamp(1.5), 1);
console.log('Passed: frame-order independence, camera focal-point invariance, safe projection, fixed-seed particles, timing bounds.');
