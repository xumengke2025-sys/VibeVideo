#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const skill = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const option = (name, fallback) => {const i = args.indexOf(`--${name}`); return i < 0 ? fallback : args[i + 1];};
const provenance = JSON.parse(fs.readFileSync(path.join(skill, 'references/shotcraft-source.json'), 'utf8'));
const sibling = path.resolve(skill, '../video-shotcraft');
const restored = path.resolve(skill, '../../reference-sources/video-shotcraft-20261014');
const root = path.resolve(option('root', process.env.VIDEO_SHOTCRAFT_ROOT ?? ([sibling,restored].find(p=>fs.existsSync(path.join(p,'gallery/api/library.json'))) ?? provenance.local_install)));
const library = JSON.parse(fs.readFileSync(path.join(root, 'gallery/api/library.json'), 'utf8'));
const normalize = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, '');
// Explicit aliases checked against the fixed commit's recipe references.
const aliases = {
  'brand-ink-open': 'demos/typography/brand-ink-open/BrandInkOpen.tsx',
  'document-typewriter-reveal': 'demos/ui-entrance/document-typewriter-reveal/DocumentTypewriterReveal.tsx',
  'panel-to-canvas': 'demos/interaction/canvas-materialize-moves/PanelToCanvasMaterialize.tsx',
  'diagram-cascade': 'demos/interaction/canvas-materialize-moves/DiagramCascadeBuild.tsx',
  'oscilloscope-stream': 'demos/data/chart-live-moves/OscilloscopeStreamV2.tsx',
  'unit-dot-swarm-regroup': 'demos/data/chart-live-moves/UnitDotSwarmRegroupV2.tsx',
  'axis-rescale-shock': 'demos/data/chart-live-moves/AxisRescaleShockV2.tsx',
  'crash-zoom-punch': 'demos/camera/crash-zoom-punch/CrashZoomReal.tsx',
  'spotlight-sweep': 'demos/effects/light-play-moves/SpotlightSweepReveal.tsx',
  'sheen-sweep': 'demos/effects/light-play-moves/SheenSweepRetry.tsx',
  'flash-cut': 'assets/lib/FlashCut.tsx',
  'whip-pan': 'demos/transition/shot-transitions/WhipBrakeReal.tsx',
  'mask-wipe': 'demos/transition/shot-transitions/PortalWipeV2.tsx',
  'drift-assembly': 'demos/typography/type-assembly-moves/LetterformDriftAssembly.tsx',
  'icon-flip-bloom': 'demos/outro/ui-to-brand-morph/IconFlipBloomLogo.tsx',
  'input-morph-assemble': 'demos/outro/ui-to-brand-morph/InputMorphsIntoLogo.tsx',
};
const within = (relative) => {
  const p = path.resolve(root, relative);
  if (!p.startsWith(root + path.sep)) throw new Error(`Source path outside library: ${relative}`);
  return p;
};
const absoluteStyle = s => ({...s,source:s.source?within(s.source):null,demo:s.demo?within(s.demo):null,alternatives:s.alternatives?.map(within),candidates:s.candidates?.map(within)});
const cards = library.cards.map(card => {
  const dir = `demos/${card.category}/${card.name}`;
  const candidates = fs.existsSync(within(dir)) ? fs.readdirSync(within(dir)).filter(p => p.endsWith('.tsx')).map(p => `${dir}/${p}`) : [];
  const styles = card.styles.map(style => {
    const exact = candidates.filter(p => normalize(path.basename(p, '.tsx')) === normalize(style.key));
    const source = aliases[style.key] ?? (exact.length === 1 ? exact[0] : candidates.length === 1 && card.styles.length === 1 ? candidates[0] : null);
    const sourceKind = source?.startsWith('assets/') ? 'component' : source ? 'active-demo' : 'unresolved';
    const demo = sourceKind === 'active-demo' ? source : null;
    return {key: style.key, label: style.label, description: style.description, source, sourceKind, demo, alternatives: style.key === 'crash-zoom-punch' ? ['demos/camera/crash-zoom-punch/CrashImpactReal.tsx'] : undefined, candidates: source ? undefined : candidates, preview: `https://vincentwei1021.github.io/video-shotcraft/${style.media.url.replace(/^\.\//, '')}`};
  });
  return {name: card.name, category: card.category, summary: card.summary, use: card.use, energy: card.energy, duration: card.duration, card: card.source, styles};
});
const command = args[0] ?? 'search';
const result = (value) => console.log(JSON.stringify(value, null, 2));
if (command === 'search') {
  const query = option('query', '').toLowerCase();
  const category = option('category', '');
  const limit = Math.max(1, Math.min(30, Number(option('limit', '5'))));
  if (!Number.isInteger(limit)) throw new Error('limit must be an integer');
  const words = query.split(/\s+/).filter(Boolean);
  const found = cards.map(c => ({c, score: words.reduce((n, w) => n + (JSON.stringify(c).toLowerCase().includes(w) ? 1 : 0), 0)}))
    .filter(x => (!category || x.c.category === category) && (!words.length || x.score > 0))
    .sort((a, b) => b.score - a.score || a.c.name.localeCompare(b.c.name))
    .slice(0, limit).map(x => ({...x.c, card: within(x.c.card), styles: x.c.styles.map(absoluteStyle)}));
  result({commit: provenance.commit, root, results: found});
} else if (command === 'card') {
  const name = args[1];
  if (!name) throw new Error('card requires a card name or style key');
  const matches = cards.filter(c => c.name === name || c.styles.some(s => s.key === name));
  if (matches.length !== 1) throw new Error(`Expected one exact card/style match for ${name}; got ${matches.length}`);
  const c = matches[0];
  const allStyles = c.name === name ? c.styles : c.styles.filter(s => s.key === name);
  result({commit: provenance.commit, root, ...c, card: within(c.card), styles: allStyles.map(absoluteStyle), note: 'Read the complete card and exact source before adapting; preview correspondence and dynamic quality require separate checks.'});
} else if (command === 'verify' || command === 'index') {
  const missing = [];
  const unresolved = [];
  const names = new Set();
  const keys = new Set();
  for (const c of cards) {
    if (names.has(c.name)) missing.push(`duplicate card: ${c.name}`);
    names.add(c.name);
    if (!fs.existsSync(within(c.card))) missing.push(c.card);
    for (const s of c.styles) {
      if (keys.has(s.key)) missing.push(`duplicate style: ${s.key}`);
      keys.add(s.key);
      if (!s.source) unresolved.push({card: c.name, style: s.key, candidates: s.candidates});
      else if (!fs.existsSync(within(s.source))) missing.push(s.source);
      for (const other of s.alternatives ?? []) if (!fs.existsSync(within(other))) missing.push(other);
    }
  }
  const summary = {commit: provenance.commit, cards: cards.length, styles: keys.size, mappedDemos: cards.flatMap(c => c.styles).filter(s => s.demo).length, mappedComponents: cards.flatMap(c => c.styles).filter(s => s.sourceKind === 'component').length, missing, unresolved};
  if (command === 'index') {
    const out = option('out', path.join(skill, 'references/shotcraft-library.json'));
    fs.writeFileSync(out, JSON.stringify({source: provenance, summary, cards}, null, 2) + '\n');
  }
  result(summary);
  if (missing.length || unresolved.length) process.exitCode = 1;
} else throw new Error(`Unknown command: ${command}`);
