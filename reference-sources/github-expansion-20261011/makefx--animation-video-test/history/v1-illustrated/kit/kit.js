// how makefx works: the shared kit.
//
// The grammar, measured from the reference video:
//   - 120 BPM. A scene is one 2 s bar; a new event lands on each eighth note (0.25 s).
//   - One focus. Each event starts where the previous one ended; nothing else moves.
//   - The chrome (title, chapter ring) settles in the first beat and then stays still.
//
// K.t(b) turns a beat index into scene time. K.check() refuses events that start off
// the grid; a tween that only finishes an earlier motion passes `data: "follow"`.
(function () {
  const BEAT = 0.25;
  const GRID = BEAT / 2; // sixteenths allowed for accents
  const K = (window.K = {});
  K.BEAT = BEAT;
  K.t = (b) => b * BEAT;
  K.accent = "#f2c14e";

  // ---------- deterministic noise ----------
  K.hash = function (a, b, c) {
    let h = (a * 374761393 + b * 668265263 + c * 2147483647) | 0;
    h = Math.imul(h ^ (h >>> 13), 1274126177);
    return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
  };

  // ---------- markup ----------
  const SVGNS = "http://www.w3.org/2000/svg";
  K.el = function (parent, tag, attrs = {}, html) {
    const isSvg = ["svg", "g", "path", "rect", "circle", "ellipse", "line", "polyline", "text", "clipPath", "defs", "filter", "feTurbulence", "feColorMatrix"].includes(tag);
    const e = isSvg ? document.createElementNS(SVGNS, tag) : document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "style" && typeof v === "object") Object.assign(e.style, v);
      else e.setAttribute(k, v);
    }
    if (html != null) e.innerHTML = html;
    parent.appendChild(e);
    return e;
  };

  K.grain = function (scene, seed) {
    K.el(scene, "div", { class: "k-abs k-grain", style: { width: "1920px", height: "1080px" } },
      `<svg width="1920" height="1080"><filter id="${seed}-grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="${seed.length}"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .9 0"/></filter><rect width="1920" height="1080" filter="url(#${seed}-grain)"/></svg>`);
  };

  // The mascot. Thumbnail on top, face strip below, legs under.
  // Returns the wrapper; parts are found by class.
  // `scale` sizes the whole card; part coordinates stay in the 220 × 210 box.
  K.card = function (parent, { id, theme = "warm", left, top, thumb = "", scale = 1 }) {
    const W = 220 * scale, H = 210 * scale;
    const wrap = K.el(parent, "div", { id, class: "k-card-wrap", style: { left: left + "px", top: top + "px", width: W + "px", height: H + "px" } });
    wrap.innerHTML = `
      <svg class="k-card k-${theme}-card" width="${W}" height="${H}" viewBox="0 0 220 210">
        <defs><clipPath id="${id}-clip"><rect x="24" y="24" width="172" height="104" rx="12"/></clipPath></defs>
        <g class="k-legs"><rect x="76" y="172" width="14" height="30" rx="6"/><rect x="130" y="172" width="14" height="30" rx="6"/></g>
        <rect class="k-ring" x="3" y="3" width="214" height="184" rx="27" fill="none" stroke="#f2c14e" stroke-width="6" opacity="0"/>
        <rect class="k-body" x="10" y="10" width="200" height="170" rx="22"/>
        <rect class="k-thumb-bg" x="24" y="24" width="172" height="104" rx="12"/>
        <g clip-path="url(#${id}-clip)"><g class="k-thumb">${thumb}</g>
          <rect class="k-bar" x="24" y="122" width="172" height="6" fill="#f2c14e"/></g>
        <g class="k-face">
          <g class="k-eyes">
            <ellipse class="k-eye" cx="92" cy="151" rx="5.5" ry="7"/>
            <ellipse class="k-eye" cx="128" cy="151" rx="5.5" ry="7"/>
            <circle class="k-glint" cx="94" cy="148" r="1.8"/><circle class="k-glint" cx="130" cy="148" r="1.8"/>
          </g>
          <ellipse class="k-cheek" cx="76" cy="161" rx="8" ry="4.5"/><ellipse class="k-cheek" cx="144" cy="161" rx="8" ry="4.5"/>
          <path class="k-mouth" d="M103 162 q7 6 14 0" fill="none" stroke-width="3.5" stroke-linecap="round"/>
        </g>
      </svg>`;
    return wrap;
  };
  K.part = (wrap, cls) => wrap.querySelector("." + cls);

  // Harbour art for thumbnails, in the card's thumb box (24..196 × 24..128).
  // `boat` shifts the boat so filmstrip frames differ; `mood` varies the palette
  // so a canvas of cards reads as different takes, not copies.
  const MOODS = {
    day: { sky: "#a9d3e8", sea: "#3e7ca6", sun: "#f2c14e", wave: "#cfe6f1", beam: false },
    dusk: { sky: "#f4b183", sea: "#6b5a8e", sun: "#f2c14e", wave: "#c9b6d8", beam: false },
    night: { sky: "#26324a", sea: "#16223a", sun: "#fffaf0", wave: "#3a4d6e", beam: true },
  };
  K.harbourArt = function ({ boat = 0, line = false, mood = "day" } = {}) {
    if (line) {
      const s = 'stroke="rgba(245,245,244,.8)" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"';
      return `<path ${s} d="M24 92 H196"/><circle ${s} cx="160" cy="52" r="10"/>
        <path ${s} d="M52 92 L56 54 H66 L70 92 M54 70 H68 M58 54 L61 46 L64 54"/>
        <path ${s} d="M${84 + boat} 88 h34 l-6 8 h-22 z M${100 + boat} 88 V70 l12 14"/>
        <path stroke="rgba(245,245,244,.35)" stroke-width="2" fill="none" d="M34 106 q10 -4 20 0 t20 0 M120 114 q10 -4 20 0 t20 0"/>`;
    }
    const m = MOODS[mood];
    return `<rect x="24" y="24" width="172" height="70" fill="${m.sky}"/><rect x="24" y="94" width="172" height="40" fill="${m.sea}"/>
      ${m.beam ? '<path d="M64 60 L196 36 V70 Z" fill="#f2c14e" opacity=".35"/>' : ""}
      <circle cx="160" cy="${mood === "dusk" ? 84 : 52}" r="11" fill="${m.sun}"/>
      <path d="M52 94 L56 56 H66 L70 94 Z" fill="#fffaf0" stroke="#2a2118" stroke-width="3"/><rect x="55" y="66" width="12" height="7" fill="#f0655a"/>
      <path d="M${84 + boat} 90 h34 l-6 8 h-22 z" fill="#f0655a" stroke="#2a2118" stroke-width="3"/>
      <path d="M${100 + boat} 90 V72 l12 14 z" fill="#fffaf0" stroke="#2a2118" stroke-width="2.5"/>
      <path stroke="${m.wave}" stroke-width="2.5" fill="none" d="M34 110 q10 -4 20 0 t20 0 M120 118 q10 -4 20 0 t20 0"/>`;
  };

  // ---------- props: still detail, never animated ----------
  K.cloud = function (scene, x, y, s = 1) {
    K.el(scene, "div", { class: "k-abs", style: { left: x + "px", top: y + "px" } },
      `<svg width="${170 * s}" height="${80 * s}" viewBox="0 0 170 80"><path d="M20 70 Q2 70 6 54 Q10 40 28 44 Q30 18 58 22 Q72 4 96 16 Q120 8 128 32 Q152 28 158 48 Q168 70 146 70 Z" fill="#fffaf0" stroke="#2a2118" stroke-width="4" stroke-linejoin="round"/><path d="M40 58 Q60 64 82 58" stroke="#e8dcc0" stroke-width="4" fill="none" stroke-linecap="round"/></svg>`);
  };
  K.plant = function (scene, x, y, s = 1) {
    K.el(scene, "div", { class: "k-abs", style: { left: x + "px", top: y + "px" } },
      `<svg width="${120 * s}" height="${170 * s}" viewBox="0 0 120 170">
        <path d="M60 110 C 40 80, 18 70, 10 40 C 34 44, 52 66, 60 100" fill="#7fae5a" stroke="#2a2118" stroke-width="4" stroke-linejoin="round"/>
        <path d="M60 104 C 76 70, 98 58, 112 30 C 88 36, 66 60, 60 96" fill="#6a9c4a" stroke="#2a2118" stroke-width="4" stroke-linejoin="round"/>
        <path d="M60 110 C 58 70, 56 40, 64 8 C 76 40, 70 76, 62 108" fill="#8cbc63" stroke="#2a2118" stroke-width="4" stroke-linejoin="round"/>
        <path d="M28 108 H92 L84 166 H36 Z" fill="#e07a5f" stroke="#2a2118" stroke-width="4" stroke-linejoin="round"/>
        <rect x="22" y="100" width="76" height="18" rx="5" fill="#e98e74" stroke="#2a2118" stroke-width="4"/></svg>`);
  };
  K.mug = function (scene, x, y) {
    K.el(scene, "div", { class: "k-abs", style: { left: x + "px", top: y + "px" } },
      `<svg width="110" height="100" viewBox="0 0 110 100"><path d="M74 36 q26 0 26 22 t-26 22" fill="none" stroke="#2a2118" stroke-width="7"/>
        <rect x="8" y="22" width="70" height="74" rx="12" fill="#f2c14e" stroke="#2a2118" stroke-width="4"/>
        <rect x="8" y="22" width="70" height="14" rx="7" fill="#6e4527" stroke="#2a2118" stroke-width="4"/>
        <text x="43" y="74" text-anchor="middle" font-family="Space Grotesk" font-weight="600" font-size="20" fill="#1a1300">fx</text></svg>`);
  };
  K.cursor = function (scene, x, y, label) {
    K.el(scene, "div", { class: "k-abs", style: { left: x + "px", top: y + "px", width: "110px", height: "80px" } },
      `<svg width="40" height="48" viewBox="0 0 40 48"><path d="M4 3 L4 38 L14 29 L21 44 L28 41 L21 26 L34 26 Z" fill="#fffaf0" stroke="#2a2118" stroke-width="3.5" stroke-linejoin="round"/></svg>` +
      (label ? `<div class="k-pill" style="left:30px;top:40px;font-size:16px;padding:3px 10px">${label}</div>` : ""));
  };
  // Blueprint annotation: a thin leader with a dot and a mono label.
  K.leader = function (scene, x1, y1, x2, y2, label, { align = "start" } = {}) {
    const g = K.el(scene, "svg", { class: "k-abs", width: 1920, height: 1080, style: { pointerEvents: "none" } },
      `<path d="M${x1} ${y1} L${x2} ${y2}" stroke="rgba(245,245,244,.35)" stroke-width="1.5" fill="none"/><circle cx="${x1}" cy="${y1}" r="4" fill="rgba(245,245,244,.6)"/>`);
    K.el(scene, "div", { class: "k-abs k-mono", style: { left: (align === "end" ? x2 - 400 : x2 + 10) + "px", width: align === "end" ? "390px" : "auto", textAlign: align === "end" ? "right" : "left", top: y2 - 12 + "px", fontSize: "18px", color: "#a8a8a3", whiteSpace: "nowrap" } }).textContent = label;
    return g;
  };
  // Blueprint crosshair registration mark.
  K.cross = function (scene, x, y) {
    K.el(scene, "svg", { class: "k-abs", width: 30, height: 30, style: { left: x - 15 + "px", top: y - 15 + "px" } },
      '<path d="M15 2 V28 M2 15 H28" stroke="rgba(245,245,244,.3)" stroke-width="1.5"/><circle cx="15" cy="15" r="6" fill="none" stroke="rgba(245,245,244,.3)" stroke-width="1.5"/>');
  };

  // ---------- chrome ----------
  // Settles inside the first beat, then holds.
  K.chrome = function (scene, tl, { title, chapter, step, of = 7 }) {
    const t = K.el(scene, "div", { class: "k-abs k-title" });
    const u = K.el(scene, "div", { class: "k-abs k-underline", style: { width: Math.round(title.length * 15.5) + "px" } });
    const R = 24, C = 2 * Math.PI * R;
    const ring = K.el(scene, "div", { class: "k-abs k-ring" },
      `<svg width="64" height="64" viewBox="0 0 64 64">
        <circle cx="32" cy="32" r="${R}" fill="none" stroke="currentColor" stroke-opacity=".18" stroke-width="5"/>
        <circle class="k-arc" cx="32" cy="32" r="${R}" fill="none" stroke="#f2c14e" stroke-width="5" stroke-linecap="round" transform="rotate(-90 32 32)" stroke-dasharray="${C}"/>
        <rect x="26" y="26" width="12" height="12" rx="3" fill="#f2c14e"/></svg>`);
    K.el(scene, "div", { class: "k-abs k-chapter" }).textContent = chapter;
    const typed = { n: 0 };
    K.sound(tl, "title", 0);
    t.textContent = "";
    tl.fromTo(typed, { n: 0 }, { n: title.length, duration: 0.3, ease: "none", onUpdate: () => (t.textContent = title.slice(0, Math.round(typed.n))) }, 0);
    tl.fromTo(u, { scaleX: 0 }, { scaleX: 1, duration: 0.25, ease: "power2.out" }, K.t(1));
    tl.fromTo(ring.querySelector(".k-arc"), { attr: { "stroke-dashoffset": C * (1 - (step - 1) / of) } },
      { attr: { "stroke-dashoffset": C * (1 - step / of) }, duration: 0.3, ease: "power2.out" }, 0);
  };

  // ---------- sound cues ----------
  // Every event can make a sound. The kit's own motions cue themselves; K.check
  // classifies the rest. tools/extract-cues.mjs reads K.events after the scenes
  // load, and tools/make-bgm.py lays a sound effect on each one.
  K.events = [];
  K.sound = function (tl, type, at, extra = {}) {
    K.events.push(Object.assign({ tl, t: at, type }, extra));
  };

  // ---------- motion vocabulary ----------
  K.pop = function (tl, el, b, { from = 0, ease = "back.out(2.2)", dur = 0.28, origin = "50% 50%" } = {}) {
    K.sound(tl, "pop", K.t(b));
    tl.fromTo(el, { scale: from, opacity: 0, transformOrigin: origin }, { scale: 1, opacity: 1, duration: dur, ease }, K.t(b));
  };
  // Squash on contact, then an elastic settle that belongs to the same event.
  // Pass follow when the contact ends a fall that already started on the beat.
  K.land = function (tl, el, at, { follow = false } = {}) {
    K.sound(tl, "land", at);
    tl.fromTo(el, { scaleX: 1, scaleY: 1 }, { scaleX: 1.16, scaleY: 0.82, duration: 0.07, ease: "power1.out", transformOrigin: "50% 100%", data: follow ? "follow" : undefined }, at);
    tl.to(el, { scaleX: 1, scaleY: 1, duration: 0.42, ease: "elastic.out(1.1, 0.45)", data: "follow" }, at + 0.07);
  };
  K.blink = function (tl, eyes, at) {
    tl.fromTo(eyes, { scaleY: 1 }, { scaleY: 0.1, duration: 0.06, yoyo: true, repeat: 1, transformOrigin: "50% 50%", data: "follow" }, at);
  };
  K.type = function (tl, el, text, b, dur) {
    K.sound(tl, "type", K.t(b), { dur, n: text.length });
    const s = { n: 0 };
    el.textContent = "";
    tl.fromTo(s, { n: 0 }, { n: text.length, duration: dur, ease: "none", onUpdate: () => (el.textContent = text.slice(0, Math.round(s.n))) }, K.t(b));
  };
  K.draw = function (tl, path, b, dur = 0.25, ease = "power2.out") {
    K.sound(tl, "draw", K.t(b), { dur });
    const L = path.getTotalLength();
    path.setAttribute("stroke-dasharray", `${L} ${L}`);
    tl.fromTo(path, { attr: { "stroke-dashoffset": L } }, { attr: { "stroke-dashoffset": 0 }, duration: dur, ease }, K.t(b));
  };
  // Move an element's centre along an SVG path (path in scene pixels).
  K.travel = function (tl, el, path, b, dur = 0.25, ease = "power2.inOut", w = 0, h = 0) {
    K.sound(tl, "whoosh", K.t(b), { dur });
    const L = path.getTotalLength();
    const p = { u: 0 };
    // Through gsap's x/y, so scale, rotation or K.land on the same element still compose.
    const place = () => {
      const q = path.getPointAtLength(L * p.u);
      gsap.set(el, { x: q.x - w / 2, y: q.y - h / 2 });
    };
    place();
    tl.fromTo(p, { u: 0 }, { u: 1, duration: dur, ease, onUpdate: place }, K.t(b));
  };

  // ---------- accents ----------
  // Small secondary motion that belongs to an event already on the beat: it happens
  // where the focus already is, so it adds detail without splitting attention.
  K.puff = function (tl, scene, x, y, at, { theme = "warm", spread = 70 } = {}) {
    const fill = theme === "warm" ? "#fffaf0" : "rgba(245,245,244,.12)";
    const stroke = theme === "warm" ? "#2a2118" : "rgba(245,245,244,.6)";
    [-1, -0.45, 0.45, 1].forEach((d, i) => {
      const r = 13 - Math.abs(d) * 3;
      const p = K.el(scene, "div", { class: "k-abs", style: { width: r * 2 + "px", height: r * 2 + "px", borderRadius: "50%", background: fill, border: `3px solid ${stroke}`, left: x - r + "px", top: y - r + "px" } });
      tl.fromTo(p, { x: 0, y: 0, scale: 0.3, opacity: 0 }, { x: d * spread, y: -10 - (1 - Math.abs(d)) * 12, scale: 1, opacity: 1, duration: 0.14, ease: "power2.out", data: "follow" }, at);
      tl.to(p, { scale: 0.2, opacity: 0, duration: 0.2, ease: "power1.in", data: "follow" }, at + 0.14 + i * 0.01);
    });
  };
  K.sparkle = function (tl, scene, x, y, at, { r = 70, n = 3, seed = 1, color = "#f2c14e", stroke = "#2a2118" } = {}) {
    K.sound(tl, "sparkle", at);
    for (let i = 0; i < n; i++) {
      const a = -Math.PI / 2 + (i - (n - 1) / 2) * 0.9 + (K.hash(seed, i, 3) - 0.5) * 0.4;
      const d = r * (0.8 + K.hash(seed, i, 7) * 0.4), size = 22 + K.hash(seed, i, 9) * 12;
      const s = K.el(scene, "div", { class: "k-abs", style: { left: x + Math.cos(a) * d - size / 2 + "px", top: y + Math.sin(a) * d - size / 2 + "px", width: size + "px", height: size + "px" } },
        `<svg width="${size}" height="${size}" viewBox="-12 -12 24 24"><path d="M0 -11 Q2 -2 11 0 Q2 2 0 11 Q-2 2 -11 0 Q-2 -2 0 -11Z" fill="${color}" stroke="${stroke}" stroke-width="2" stroke-linejoin="round"/></svg>`);
      tl.fromTo(s, { scale: 0, rotation: -40, opacity: 1 }, { scale: 1, rotation: 0, duration: 0.14, ease: "back.out(3)", data: "follow" }, at + i * 0.03);
      tl.to(s, { scale: 0, rotation: 30, duration: 0.16, ease: "power2.in", data: "follow" }, at + 0.2 + i * 0.03);
    }
  };

  // ---------- the rules, enforced ----------
  K.check = function (tl, name) {
    const bad = [];
    tl.getChildren(false, true, true).forEach((c) => {
      if (c.data === "follow") return;
      const st = c.startTime();
      if (Math.abs(st / GRID - Math.round(st / GRID)) > 1e-6) bad.push(st.toFixed(3));
    });
    if (bad.length) console.error(`[kit] ${name}: events off the beat grid at ${bad.join(", ")}s`);

    // Events nobody cued: name them by what they do, so each still makes a sound.
    const cued = K.events.filter((e) => e.tl === tl).map((e) => e.t);
    const seen = new Set();
    tl.getChildren(false, true, true).forEach((c) => {
      if (c.data === "follow") return;
      const st = Math.round(c.startTime() / GRID) * GRID;
      if (seen.has(st) || cued.some((t) => Math.abs(t - st) < 0.03)) return;
      seen.add(st);
      K.sound(tl, K.classify(c), st);
    });
  };
  K.classify = function (c) {
    const v = c.vars || {}, f = v.startAt || {};
    const moved = (k) => typeof v[k] === "number" && typeof f[k] === "number" && Math.abs(v[k] - f[k]) > 150;
    if (v.clipPath || f.clipPath) return "reveal";
    if (typeof f.scale === "number" && f.scale > 1.2) return "stamp";
    if (v.attr && "stroke-dashoffset" in v.attr) return "draw";
    if (moved("x") || moved("y")) return "whoosh";
    if ((typeof f.scale === "number" && f.scale < 0.8) || f.opacity === 0) return "pop";
    return "tick";
  };

  // One focus per beat: [[beat, x, y], ...]. Warns when attention would jump, and in
  // debug renders draws the focus ring so a reviewer can follow it.
  K.focus = function (scene, tl, name, points) {
    for (let i = 1; i < points.length; i++) {
      const [, x0, y0] = points[i - 1], [b, x1, y1] = points[i];
      const d = Math.hypot(x1 - x0, y1 - y0);
      if (d > 620) console.warn(`[kit] ${name}: focus jumps ${Math.round(d)}px at beat ${b}`);
    }
    let debug = false;
    try { debug = !!(window.__hyperframes && window.__hyperframes.getVariables().debug); } catch (e) { debug = false; }
    if (!debug) return;
    const ring = K.el(scene, "div", { class: "k-abs k-focus" });
    points.forEach(([b, x, y]) => tl.set(ring, { x, y }, K.t(b)));
  };
})();
