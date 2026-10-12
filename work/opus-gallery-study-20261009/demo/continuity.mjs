// Original helpers for deterministic, seekable motion. Times are seconds.
// frequency is the natural frequency in Hz; damping is the damping ratio.
function parameters(frequency, damping) {
  if (!Number.isFinite(frequency) || frequency <= 0 || !Number.isFinite(damping) || damping <= 0)
    throw new RangeError('frequency and damping must be finite and positive');
  return {w: 2 * Math.PI * frequency, z: damping};
}

export function springFrom(time, {from, to, velocity = 0, frequency = 3, damping = 1}) {
  const {w, z} = parameters(frequency, damping);
  if (![time, from, to, velocity].every(Number.isFinite)) throw new RangeError('Nonfinite spring input');
  if (time <= 0) return from;
  const y = from - to;
  if (Math.abs(z - 1) < 1e-7) return to + Math.exp(-w * time) * (y + (velocity + w * y) * time);
  if (z < 1) {
    const wd = w * Math.sqrt(1 - z * z);
    return to + Math.exp(-z * w * time) * (y * Math.cos(wd * time) + (velocity + z * w * y) / wd * Math.sin(wd * time));
  }
  const q = Math.sqrt(z * z - 1), r1 = -w / (z + q), r2 = -w * (z + q);
  const a = (velocity - r2 * y) / (r1 - r2), b = y - a;
  return to + a * Math.exp(r1 * time) + b * Math.exp(r2 * time);
}

export const springStep = (time, options = {}) => springFrom(time, {...options, from: 0, to: 1, velocity: 0});

// Superposition preserves position and velocity through repeated target changes.
// Events must be sorted; each is {time, value}. No previous rendered frame is read.
export function springTrack(time, initial, events, options = {}) {
  if (![time, initial].every(Number.isFinite)) throw new RangeError('Nonfinite track input');
  let result = initial, previous = initial, previousTime = -Infinity;
  for (const event of events) {
    if (![event.time, event.value].every(Number.isFinite) || event.time < previousTime)
      throw new RangeError('Spring events must be finite and sorted');
    result += (event.value - previous) * springStep(time - event.time, options);
    previous = event.value; previousTime = event.time;
  }
  return result;
}

// Constant speed in logarithmic scale for a portal zoom; progress in [0,1].
export function logZoom(start, end, progress) {
  if (![start, end, progress].every(Number.isFinite) || start <= 0 || end <= 0)
    throw new RangeError('Zoom scales must be finite and positive');
  const p = Math.max(0, Math.min(1, progress));
  return Math.exp(Math.log(start) + p * Math.log(end / start));
}

// Explicit point correspondence only: equal topology and winding are caller responsibilities.
export function morphPoints(a, b, progress) {
  if (a.length !== b.length || !Number.isFinite(progress)) throw new RangeError('Point topology must match');
  const p = Math.max(0, Math.min(1, progress));
  return a.map((point, i) => {
    if (![point.x, point.y, b[i].x, b[i].y].every(Number.isFinite)) throw new RangeError('Nonfinite point');
    return {x: point.x + (b[i].x - point.x) * p, y: point.y + (b[i].y - point.y) * p};
  });
}
