import React from 'react';
import {AbsoluteFill, Audio, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp, lerp, smooth, progress, seeded, rotate3, project3} from './motion.mjs';

const BG = '#131715';
const INK = '#f1ebdf';
const ACCENT = '#ff7748';
const MUTED = '#95998e';
const COUNT = 560;
const rng = seeded(731);
const POINTS = Array.from({length: COUNT}, (_, i) => {
  const y = 1 - 2 * (i + 0.5) / COUNT;
  const phi = i * Math.PI * (3 - Math.sqrt(5));
  const r = Math.sqrt(1 - y * y);
  return {
    id: i, x: r * Math.cos(phi), y, z: r * Math.sin(phi),
    sx: (rng() - 0.5) * 1650, sy: (rng() - 0.5) * 850,
    phase: rng() * Math.PI * 2, delay: rng() * 0.38,
  };
});

// Four monoline glyphs built as geometry, rather than extracted font bitmaps.
const glyphPoint = (id) => {
  const letter = Math.floor(id / 140);
  const p = (id % 140) / 139;
  let x = 0, y = 0;
  if (letter === 0) {
    const angle = 0.24 * Math.PI + p * 1.52 * Math.PI;
    x = 95 * Math.cos(angle); y = 142 * Math.sin(angle);
  } else if (letter === 1) {
    const angle = p * Math.PI * 2;
    x = 95 * Math.cos(angle); y = 142 * Math.sin(angle);
  } else if (letter === 2) {
    if (p < 0.35) {x = -82; y = lerp(-142, 142, p / 0.35);}
    else {const angle = Math.PI / 2 - (p - 0.35) / 0.65 * Math.PI; x = -82 + 177 * Math.cos(angle); y = 142 * Math.sin(angle);}
  } else {
    if (p < 0.4) {x = -82; y = lerp(-142, 142, p / 0.4);}
    else if (p < 0.6) {x = lerp(-82, 90, (p - 0.4) / 0.2); y = -142;}
    else if (p < 0.8) {x = lerp(-82, 62, (p - 0.6) / 0.2); y = 0;}
    else {x = lerp(-82, 90, (p - 0.8) / 0.2); y = 142;}
  }
  return {x: 960 + (letter - 1.5) * 240 + x, y: 495 + y, letter};
};

const curvePath = (points) => points.map((p, i) => `${i ? 'L' : 'M'}${p.x.toFixed(2)},${p.y.toFixed(2)}`).join(' ');
const tracking = (s) => ({letterSpacing: s});

export const CodeMotionStudy = ({soundSrc = null, accent = ACCENT}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const frozenT = Math.min(t, 10.4);
  const gather = smooth(progress(t, 0.2, 3.2));
  const reveal = smooth(progress(t, 3.0, 4.3));
  const morph = smooth(progress(t, 6.5, 9.4));
  const cx = lerp(1280, 960, reveal);
  const cy = 520;
  const radius = lerp(330, 450, reveal);
  const yaw = frozenT * 0.27;
  const pitch = -0.25 + Math.sin(frozenT * 0.22) * 0.13;
  const project = (p) => project3(rotate3(p, yaw, pitch), {cx, cy, focal: 1320, distance: 1500});
  const particles = POINTS.map(p => {
    const sphere = project({x: p.x * radius, y: p.y * radius, z: p.z * radius});
    const q = smooth(progress(t, 0.2 + p.delay, 2.9 + p.delay));
    const swirl = (1 - q) * t * 0.28;
    const scatterX = cx + p.sx * Math.cos(swirl) - p.sy * Math.sin(swirl);
    const scatterY = cy + p.sx * Math.sin(swirl) * 0.45 + p.sy * Math.cos(swirl);
    const target = glyphPoint(p.id);
    const shift = smooth(progress(t, 6.5 + p.delay * 0.7, 9.05 + p.delay * 0.7));
    return {
      id: p.id, z: sphere.z * (1 - shift),
      x: lerp(lerp(scatterX, sphere.x, q), target.x, shift),
      y: lerp(lerp(scatterY, sphere.y, q), target.y, shift),
      radius: lerp(lerp(1.25, 4.1, clamp((sphere.z + radius) / (radius * 2))), 3.6, shift),
      alpha: lerp(lerp(0.16, 0.96, clamp((sphere.z + radius) / (radius * 2))), 1, shift),
      color: shift > 0.55 ? (target.letter % 2 ? accent : INK) : (p.id % 7 === 0 ? accent : INK),
    };
  }).sort((a, b) => b.z - a.z);
  const wireOpacity = smooth(progress(t, 2.6, 4.0)) * (1 - smooth(progress(t, 6.6, 7.8)));
  const wires = [];
  for (let k = -2; k <= 2; k++) {
    const lat = k * Math.PI / 8;
    const pts = Array.from({length: 121}, (_, i) => {
      const a = i / 120 * Math.PI * 2;
      return project({x: radius * Math.cos(lat) * Math.cos(a), y: radius * Math.sin(lat), z: radius * Math.cos(lat) * Math.sin(a)});
    });
    wires.push(<path key={`lat${k}`} d={curvePath(pts)} fill="none" stroke={INK} strokeWidth="1" opacity="0.15"/>);
  }
  for (let k = 0; k < 7; k++) {
    const lon = k / 7 * Math.PI;
    const pts = Array.from({length: 121}, (_, i) => {
      const a = i / 120 * Math.PI * 2;
      return project({x: radius * Math.cos(a) * Math.cos(lon), y: radius * Math.sin(a), z: radius * Math.cos(a) * Math.sin(lon)});
    });
    wires.push(<path key={`lon${k}`} d={curvePath(pts)} fill="none" stroke={INK} strokeWidth="1" opacity="0.12"/>);
  }
  const orbitAlpha = smooth(progress(t, 3.0, 4.1)) * (1 - smooth(progress(t, 6.1, 7.1)));
  const orbitPts = Array.from({length: 180}, (_, i) => {
    const a = i / 179 * Math.PI * 2;
    return project(rotate3({x: Math.cos(a) * radius * 1.18, y: 0, z: Math.sin(a) * radius * 1.18}, 0.25, 0.65));
  });
  const satellite = project(rotate3({x: Math.cos(t * 1.2) * radius * 1.18, y: 0, z: Math.sin(t * 1.2) * radius * 1.18}, 0.25, 0.65));
  const firstTextAlpha = 1 - smooth(progress(t, 2.9, 3.5));
  const finalAlpha = smooth(progress(t, 9.2, 10.1));
  const topLabel = t < 3.3 ? '01 / 规则' : t < 6.6 ? '02 / 空间' : '03 / 表达';
  const margin = 94;
  return <AbsoluteFill style={{backgroundColor: BG, color: INK, fontFamily: 'Microsoft YaHei, sans-serif'}}>
    {soundSrc ? <Audio src={soundSrc} volume={0.8}/> : null}
    <svg width="1920" height="1080" viewBox="0 0 1920 1080" style={{position: 'absolute', inset: 0}}>
      <defs><pattern id="study-grain" width="31" height="29" patternUnits="userSpaceOnUse"><circle cx="2" cy="3" r="0.65" fill={INK} opacity="0.07"/><circle cx="17" cy="21" r="0.5" fill={INK} opacity="0.04"/></pattern></defs>
      <rect width="1920" height="1080" fill="url(#study-grain)"/>
      <text x="92" y="595" fill={INK} opacity={0.035 * reveal * (1 - morph)} fontFamily="Arial, sans-serif" fontSize="300" fontWeight="700" letterSpacing="-12">MOTION</text>
      <g opacity={wireOpacity}>{wires}</g>
      <g opacity={orbitAlpha}>
        <path d={curvePath(orbitPts)} fill="none" stroke={accent} strokeWidth="1.4" opacity="0.55"/>
        <circle cx={satellite.x} cy={satellite.y} r="8" fill={accent}/>
      </g>
      {particles.map(p => <circle key={p.id} cx={p.x} cy={p.y} r={p.radius} opacity={p.alpha} fill={p.color}/>)}
      <line x1={margin} y1="957" x2="1826" y2="957" stroke={INK} opacity="0.15"/>
      <line x1={margin} y1="957" x2={margin + 1732 * clamp(t / 10.4)} y2="957" stroke={accent} strokeWidth="2"/>
    </svg>
    <div style={{position: 'absolute', top: 61, left: margin, fontSize: 23, ...tracking(3), color: MUTED}}>CODE / MOTION STUDY</div>
    <div style={{position: 'absolute', top: 61, right: margin, fontSize: 23, color: MUTED, fontVariantNumeric: 'tabular-nums'}}>{topLabel}</div>
    <div style={{position: 'absolute', top: 330, left: margin, opacity: firstTextAlpha, transform: `translateY(${lerp(38, 0, smooth(progress(t, 0, 0.9)))}px)`}}>
      <div style={{fontSize: 105, lineHeight: 1.3, fontWeight: 600, letterSpacing: -5}}>一条规则<br/>一个世界<span style={{color: accent}}>。</span></div>
      <div style={{fontSize: 25, marginTop: 30, color: MUTED}}>从粒子，到空间，再到表达。</div>
    </div>
    <div style={{position: 'absolute', top: 770, left: 0, width: 1920, textAlign: 'center', opacity: finalAlpha, transform: `translateY(${lerp(30, 0, finalAlpha)}px)`}}>
      <div style={{fontSize: 60, fontWeight: 500, letterSpacing: 4}}>把想法，变成运动。</div>
      <div style={{fontSize: 23, marginTop: 20, color: MUTED, ...tracking(4)}}>VIBE VIDEO / PURE CODE STUDY</div>
    </div>
    <div style={{position: 'absolute', left: margin, bottom: 67, fontSize: 21, color: MUTED}}>{t < 3.3 ? '轨迹由规则定义' : t < 6.6 ? '旋转 · 透视 · 深度' : '同一组粒子，组成新的形态'}</div>
    <div style={{position: 'absolute', right: margin, bottom: 67, fontSize: 21, color: MUTED}}>SVG × ANALYTICAL 3D</div>
  </AbsoluteFill>;
};
