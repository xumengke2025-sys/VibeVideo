export const clamp = (v, lo = 0, hi = 1) => Math.max(lo, Math.min(hi, v));
export const lerp = (a, b, t) => a + (b - a) * t;
export const smooth = (v) => { const t = clamp(v); return t * t * (3 - 2 * t); };
export const progress = (time, start, end) => end > start ? clamp((time - start) / (end - start)) : Number(time >= end);

export const seeded = (seed) => {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6D2B79F5) >>> 0;
    let n = Math.imul(state ^ (state >>> 15), 1 | state);
    n ^= n + Math.imul(n ^ (n >>> 7), 61 | n);
    return ((n ^ (n >>> 14)) >>> 0) / 4294967296;
  };
};

// Pure analytical rotation; no simulation state or wall-clock dependency.
export const rotate3 = ({x, y, z}, yaw = 0, pitch = 0) => {
  const rx = x * Math.cos(yaw) + z * Math.sin(yaw);
  const rz = -x * Math.sin(yaw) + z * Math.cos(yaw);
  return {x: rx, y: y * Math.cos(pitch) - rz * Math.sin(pitch), z: y * Math.sin(pitch) + rz * Math.cos(pitch)};
};

export const project3 = (point, {cx, cy, focal = 1100, distance = 1400, near = 20}) => {
  const depth = distance + point.z;
  if (depth <= near) return null;
  const scale = focal / depth;
  return {x: cx + point.x * scale, y: cy + point.y * scale, z: point.z, scale};
};

export const worldToScreen = ({x, y}, {x: cameraX, y: cameraY, zoom}, {width, height}) => ({
  x: width / 2 + (x - cameraX) * zoom,
  y: height / 2 + (y - cameraY) * zoom,
});

// Suitable for a DOM layer with transform-origin: 0 0.
export const cameraTransform = ({x, y, zoom}, {width, height}) =>
  `translate(${width / 2}px, ${height / 2}px) scale(${zoom}) translate(${-x}px, ${-y}px)`;
