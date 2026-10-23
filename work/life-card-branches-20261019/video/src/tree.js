// The graph is a real rooted five-ary tree.  The engraved reference image is
// atmosphere; these stable IDs and edges drive every reveal and the rewind.
export const WIDTH = 1080;
export const HEIGHT = 1920;
export const LEVEL_X = [90, 310, 515, 690, 840, 980];
export const MAIN_IDS = ['r', 'r.2', 'r.2.2', 'r.2.2.2', 'r.2.2.2.2', 'r.2.2.2.2.2'];
export const FIRST_CHOICES = ['留在原城', '先去短住', '搬去新城', '两城往返', '暂缓决定'];

const hash = (s) => {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619);
  return (h >>> 0) / 4294967295;
};

export function makeTree() {
  const nodes = [{id: 'r', parentId: null, depth: 0, x: LEVEL_X[0], y: 960, lo: 54, hi: 1866}];
  const edges = [];
  const byId = new Map([['r', nodes[0]]]);
  for (let depth = 1; depth <= 5; depth++) {
    const parents = nodes.filter((n) => n.depth === depth - 1);
    for (const parent of parents) {
      const span = (parent.hi - parent.lo) / 5;
      for (let slot = 0; slot < 5; slot++) {
        const lo = parent.lo + span * slot;
        const hi = lo + span;
        const id = `${parent.id}.${slot}`;
        const main = MAIN_IDS.includes(id);
        const wobble = main ? 0 : (hash(id) - 0.5) * Math.min(22, span * 0.14);
        const child = {
          id, parentId: parent.id, depth, slot,
          x: LEVEL_X[depth] + (main ? 0 : (hash(`${id}:x`) - 0.5) * (depth < 3 ? 20 : 12)),
          y: (lo + hi) / 2 + wobble, lo, hi, main,
          cardType: main ? ['','move','lovers','career','tower','star'][depth] :
            ['plain','money','career','tarot','plain'][Math.floor(hash(`${id}:type`) * 5)]
        };
        nodes.push(child);
        byId.set(id, child);
        edges.push({id, from: parent, to: child, depth, main});
      }
    }
  }
  return {nodes, edges, byId};
}

export const TREE = makeTree();
export const COUNTS = [1, 5, 25, 125, 625, 3125];

export function edgePath(edge) {
  const {from, to, depth} = edge;
  const sx = from.x + (depth < 3 ? 20 : 6);
  const ex = to.x - (depth < 3 ? 22 : 4);
  const dx = ex - sx;
  const bend = (hash(`${edge.id}:bend`) - 0.5) * Math.min(33, 70 / depth);
  return `M${sx.toFixed(2)} ${from.y.toFixed(2)} C${(sx + dx * 0.34).toFixed(2)} ${(from.y + bend).toFixed(2)} ${(sx + dx * 0.64).toFixed(2)} ${(to.y - bend).toFixed(2)} ${ex.toFixed(2)} ${to.y.toFixed(2)}`;
}

export function cardPath(node) {
  const size = [56, 44, 24, 12, 5.2, 1.9][node.depth];
  const h = size * 1.36;
  const x = node.x - size / 2;
  const y = node.y - h / 2;
  return `M${x.toFixed(2)} ${y.toFixed(2)}h${size.toFixed(2)}v${h.toFixed(2)}h${(-size).toFixed(2)}z`;
}

export const LEVEL_PATHS = Array.from({length: 5}, (_, i) => {
  const depth = i + 1;
  return {
    depth,
    edges: TREE.edges.filter((e) => e.depth === depth).map(edgePath).join(' '),
    cards: TREE.nodes.filter((n) => n.depth === depth).map(cardPath).join(' '),
  };
});

export const ORGANIC_LEAVES = TREE.edges.filter((e) => e.depth <= 3 && !e.main && hash(`${e.id}:leaf`) > 0.56)
  .map((e) => {
    const x = e.from.x + (e.to.x - e.from.x) * 0.52;
    const y = e.from.y + (e.to.y - e.from.y) * 0.52;
    const flip = hash(`${e.id}:flip`) > 0.5 ? 1 : -1;
    const r = e.depth === 1 ? 11 : e.depth === 2 ? 6 : 3;
    return `M${x.toFixed(1)} ${y.toFixed(1)}q${(r * 0.5).toFixed(1)} ${(-flip * r).toFixed(1)} ${(r * 1.7).toFixed(1)} ${(-flip * r * 0.7).toFixed(1)}q${(-r * 0.4).toFixed(1)} ${(flip * r * 0.8).toFixed(1)} ${(-r * 1.7).toFixed(1)} ${(flip * r * 0.7).toFixed(1)}z`;
  }).join(' ');
