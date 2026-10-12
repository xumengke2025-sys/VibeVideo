// how makefx works: the shared kit, in the makefx look (DESIGN.md).
//
// The grammar, measured from the reference video:
//   - 120 BPM. A scene is one 2 s bar; a new event lands on each eighth note (0.25 s).
//   - One focus. Each event starts where the previous one ended; nothing else moves.
//   - The chrome settles in the first beat and then stays still.
//
// The look, from DESIGN.md: a void where media is the only colour, chrome is quiet
// ink, rings instead of borders, and amber only on the thing being acted on, which
// makes amber the viewer's focus too.
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
  K.ease = "expo.out"; // DESIGN --e-out-strong, entrances
  K.easeMove = "power3.inOut"; // DESIGN --e-in-out, between two known places

  // ---------- deterministic noise ----------
  K.hash = function (a, b, c) {
    let h = (a * 374761393 + b * 668265263 + c * 2147483647) | 0;
    h = Math.imul(h ^ (h >>> 13), 1274126177);
    return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
  };

  // ---------- markup ----------
  const SVGNS = "http://www.w3.org/2000/svg";
  const SVG_TAGS = ["svg", "g", "path", "rect", "circle", "ellipse", "line", "polyline", "polygon", "text", "clipPath", "defs", "mask", "linearGradient", "radialGradient", "stop"];
  K.el = function (parent, tag, attrs = {}, html) {
    const e = SVG_TAGS.includes(tag) ? document.createElementNS(SVGNS, tag) : document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "style" && typeof v === "object") Object.assign(e.style, v);
      else e.setAttribute(k, v);
    }
    if (html != null) e.innerHTML = html;
    parent.appendChild(e);
    return e;
  };

  // ---------- media ----------
  // Stand-in media for the Salt Harbour space, 16:9 (viewBox 320 × 180). Media is the
  // only colour on screen, so it is rich; `boat` moves the boat so frames differ.
  const MOODS = {
    day: { sky: ["#8ec5e6", "#d8ecf5"], sea: ["#3a7fb0", "#1f4f78"], sun: "#ffd66b", glow: "rgba(255,214,107,.45)", sunY: 58, land: "#2f4a5a", beam: false },
    dusk: { sky: ["#f59a6b", "#f7cf94"], sea: ["#6b5a8e", "#3a2f5a"], sun: "#ffcf6b", glow: "rgba(255,160,90,.55)", sunY: 112, land: "#4a3350", beam: false },
    night: { sky: ["#141d33", "#2a3a5e"], sea: ["#16223a", "#0b1222"], sun: "#f5f1e0", glow: "rgba(245,241,224,.25)", sunY: 44, land: "#0f1626", beam: true },
  };
  K.harbourArt = function ({ boat = 0, mood = "day" } = {}) {
    const m = MOODS[mood] || MOODS.day, id = `hb-${mood}`, bx = 150 + boat * 1.8;
    return `<svg viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" data-layout-allow-overflow>
      <defs>
        <linearGradient id="${id}-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${m.sky[0]}"/><stop offset="1" stop-color="${m.sky[1]}"/></linearGradient>
        <linearGradient id="${id}-sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${m.sea[0]}"/><stop offset="1" stop-color="${m.sea[1]}"/></linearGradient>
        <radialGradient id="${id}-glow"><stop offset="0" stop-color="${m.glow}"/><stop offset="1" stop-color="rgba(0,0,0,0)"/></radialGradient>
      </defs>
      <rect width="320" height="120" fill="url(#${id}-sky)"/>
      <circle cx="248" cy="${m.sunY}" r="60" fill="url(#${id}-glow)"/>
      <circle cx="248" cy="${m.sunY}" r="15" fill="${m.sun}"/>
      <path d="M0 112 Q40 92 80 104 T170 100 L170 120 L0 120 Z" fill="${m.land}" opacity=".85"/>
      <rect y="118" width="320" height="62" fill="url(#${id}-sea)"/>
      ${m.beam ? '<path d="M78 58 L320 22 L320 84 Z" fill="#ffd66b" opacity=".18"/>' : ""}
      <path d="M68 118 L72 56 L86 56 L90 118 Z" fill="#f4efe6"/><rect x="70" y="72" width="18" height="10" fill="#e0574a"/><rect x="70" y="94" width="18" height="10" fill="#e0574a"/>
      <path d="M66 56 H92 L86 46 H72 Z" fill="#2b2b33"/><circle cx="79" cy="44" r="5" fill="${m.beam ? "#ffd66b" : "#f4efe6"}"/>
      <path d="M${bx} 132 h54 l-9 11 h-36 z" fill="#e0574a"/><path d="M${bx + 26} 131 V100 l20 29 z" fill="#f4efe6"/>
      <path d="M${bx - 6} 146 q12 -3 24 0 t24 0 t24 0" stroke="rgba(255,255,255,.35)" stroke-width="2" fill="none"/>
      <path d="M20 150 q14 -4 28 0 t28 0 M214 164 q14 -4 28 0 t28 0 M120 170 q12 -3 24 0" stroke="rgba(255,255,255,.22)" stroke-width="2" fill="none"/>
      <rect x="${bx + 8}" y="146" width="40" height="3" fill="rgba(0,0,0,.18)"/></svg>`;
  };

  // ---------- the asset card ----------
  // Media on a matte, a meta row (name, credits), the ring on top. State lives only in
  // the ring: rest, hover, wait (queued), generating, selected, failed. Nothing touches
  // the media.
  const RING = {
    rest: (w) => `inset 0 0 0 ${w}px rgba(255,255,255,.12)`,
    hover: (w) => `inset 0 0 0 ${w}px rgba(255,255,255,.24)`,
    wait: (w) => `inset 0 0 0 ${w}px rgba(245,245,244,.35)`,
    generating: (w) => `inset 0 0 0 ${w}px rgba(242,193,78,.55)`,
    selected: (w) => `inset 0 0 0 ${w * 1.8}px #f2c14e`,
    failed: (w) => `inset 0 0 0 ${w}px #f0655a`,
  };
  K.card = function (parent, { id, left, top, scale = 1, art = "", name = "", cr = "", state = "rest" }) {
    const s = scale, W = 240 * s, m = 2 * s, mw = W - 2 * m, mh = Math.round((mw * 9) / 16), meta = 40 * s, H = m + mh + meta;
    const wrap = K.el(parent, "div", { id, class: "k-card", style: { left: left + "px", top: top + "px", width: W + "px", height: H + "px" } });
    wrap.innerHTML = `
      <div class="k-media" style="left:${m}px;top:${m}px;width:${mw}px;height:${mh}px"><div class="k-thumb">${art}</div><div class="k-bar"></div></div>
      <div class="k-meta" style="left:${12 * s}px;right:${12 * s}px;top:${m + mh}px;height:${meta}px">
        <span class="k-name" style="font-size:${15 * s}px">${name}</span><span class="k-cr" style="font-size:${14 * s}px">${cr}</span></div>
      <div class="k-ring" style="box-shadow:${RING[state](1.5 * s)}"></div>`;
    gsap.set(wrap.querySelector(".k-bar"), { scaleX: 0 });
    // Geometry in scene pixels, for focus points and lines.
    wrap.k = { s, W, H, mh, left, top, cx: left + W / 2, mediaCy: top + m + mh / 2, bottom: top + H };
    return wrap;
  };
  K.part = (wrap, cls) => wrap.querySelector("." + cls);
  K.ringShadow = (state, scale = 1) => RING[state](1.5 * scale);
  // Change a card's state: the ring changes in --t-micro.
  K.ring = function (tl, card, state, at, { dur = 0.12, follow = false } = {}) {
    tl.to(K.part(card, "k-ring"), { boxShadow: RING[state](1.5 * card.k.s), duration: dur, ease: "power1.out", data: follow ? "follow" : undefined }, at);
  };
  // The progress bar along the bottom inside edge of the media.
  // Chain later fills with { chain: true } so they do not paint their start at frame 0.
  K.progress = function (tl, card, from, to, at, dur, { follow = false, chain = false } = {}) {
    tl.fromTo(K.part(card, "k-bar"), { scaleX: from }, { scaleX: to, duration: dur, ease: "none", immediateRender: !chain, data: follow ? "follow" : undefined }, at);
  };
  // Media fades in over the placeholder, opacity only; the bar completes and fades.
  K.reveal = function (tl, card, b, { dur = 0.3 } = {}) {
    K.sound(tl, "reveal", K.t(b));
    tl.fromTo(K.part(card, "k-thumb"), { opacity: 0 }, { opacity: 1, duration: dur, ease: "power1.out" }, K.t(b));
    tl.to(K.part(card, "k-bar"), { opacity: 0, duration: 0.16, data: "follow" }, K.t(b));
  };
  // The ring pulses once to amber and back: "this one".
  K.pulse = function (tl, card, at, { back = "rest" } = {}) {
    K.sound(tl, "sparkle", at);
    const r = K.part(card, "k-ring");
    tl.to(r, { boxShadow: RING.selected(1.5 * card.k.s), duration: 0.08, ease: "power1.out", data: "follow" }, at);
    tl.to(r, { boxShadow: RING[back](1.5 * card.k.s), duration: 0.2, ease: "power1.in", data: "follow" }, at + 0.1);
  };

  // ---------- chrome ----------
  // Four corners, nothing in the middle. Settles inside the first beat, then holds.
  //   top left: chapter micro label and the title; top right: chapter progress;
  //   bottom left: the wordmark; bottom right: the balance.
  const CHAPTERS = ["ask", "price", "generate", "land", "continue", "cut", "share"];
  K.chrome = function (scene, tl, { title, step, balance = "2,000 cr", held = "", animateStep = true }) {
    const label = K.el(scene, "div", { class: "k-abs k-micro k-chapter" });
    label.textContent = `${String(step).padStart(2, "0")} · ${CHAPTERS[step - 1]}`;
    const t = K.el(scene, "div", { class: "k-abs k-title" });
    t.textContent = title.charAt(0).toUpperCase() + title.slice(1);
    const prog = K.el(scene, "div", { class: "k-abs k-pill k-progress" },
      CHAPTERS.map((_, i) => `<i class="${i < step - 1 ? "k-done" : ""}"></i>`).join(""));
    const slot = prog.children[step - 1];
    slot.style.position = "relative";
    const cur = K.el(slot, "i", { style: { position: "absolute", inset: "0", background: "#f2c14e", transformOrigin: "0 50%" } });
    K.el(scene, "div", { class: "k-abs k-wordmark" }, "make<b>fx</b>");
    const bal = K.el(scene, "div", { class: "k-abs k-pill k-balance" });
    bal.innerHTML = `<span class="k-bal-v">${balance}</span><span class="k-held">${held}</span>`;
    scene.k = { balance: bal };
    K.sound(tl, "title", 0);
    tl.fromTo([label, t], { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.4, ease: K.ease }, 0);
    tl.fromTo(cur, { scaleX: animateStep ? 0 : 1 }, { scaleX: 1, duration: 0.3, ease: "power2.out" }, 0);
  };
  // The balance changes (DESIGN §7.2): the old figure leaves upward, the new one
  // arrives from below. `held` is the lighter suffix ("−80") a hold shows until it
  // settles. Text follows the tween's position, so any seek lands on the right figure.
  K.balance = function (tl, scene, at, { balance, held = "" }) {
    const v = scene.k.balance.querySelector(".k-bal-v"), h = scene.k.balance.querySelector(".k-held");
    const was = { v: v.textContent, h: h.textContent }, o = { p: 0 };
    const show = () => { const now = o.p >= 0.5; v.textContent = now ? balance : was.v; h.textContent = now ? held : was.h; };
    tl.fromTo(o, { p: 0 }, { p: 1, duration: 0.2, ease: "none", onUpdate: show }, at);
    tl.fromTo([v, h], { y: 0, opacity: 1 }, { y: -8, opacity: 0, duration: 0.1, ease: "power1.in", data: "follow" }, at);
    tl.fromTo([v, h], { y: 8, opacity: 0 }, { y: 0, opacity: 1, duration: 0.14, ease: K.ease, immediateRender: false, data: "follow" }, at + 0.1);
  };

  // ---------- props and annotations ----------
  // A collaborator's cursor: white arrow with a name chip. Returns the element to move.
  K.cursor = function (scene, x, y, label) {
    return K.el(scene, "div", { class: "k-abs", style: { left: x + "px", top: y + "px", width: "150px", height: "80px" } },
      `<svg width="34" height="42" viewBox="0 0 34 42"><path d="M3 2 L3 32 L11 25 L17 38 L23 35 L17 22 L29 22 Z" fill="#f5f5f4" stroke="#08080a" stroke-width="2.5" stroke-linejoin="round"/></svg>` +
      (label ? `<div class="k-chip" style="left:26px;top:34px;background:#f5f5f4;color:#08080a;box-shadow:none">${label}</div>` : ""));
  };
  // Annotation: a hairline with a dot and a micro label.
  K.leader = function (scene, x1, y1, x2, y2, label, { align = "start" } = {}) {
    K.el(scene, "svg", { class: "k-abs", width: 1920, height: 1080, style: { pointerEvents: "none" } },
      `<path d="M${x1} ${y1} L${x2} ${y2}" stroke="rgba(255,255,255,.18)" stroke-width="1.5" fill="none"/><circle cx="${x1}" cy="${y1}" r="3.5" fill="rgba(245,245,244,.5)"/>`);
    const l = K.el(scene, "div", { class: "k-abs k-micro", style: { left: (align === "end" ? x2 - 600 : x2 + 12) + "px", width: align === "end" ? "588px" : "auto", textAlign: align === "end" ? "right" : "left", top: y2 - 10 + "px" } });
    l.textContent = label;
    return l;
  };
  // An edge between cards: white alpha for references (DESIGN §8). Returns the path.
  K.edge = function (scene, d, { alpha = 0.2, id } = {}) {
    const svg = K.el(scene, "svg", { class: "k-abs", width: 1920, height: 1080, style: { pointerEvents: "none" } });
    return K.el(svg, "path", Object.assign({ d, stroke: `rgba(255,255,255,${alpha})`, "stroke-width": 2, fill: "none", "stroke-linecap": "round" }, id ? { id } : {}));
  };

  // ---------- sound cues ----------
  // Every event can make a sound. The kit's own motions cue themselves; K.check
  // classifies the rest. tools/extract-cues.mjs reads K.events after the scenes
  // load, and tools/make-bgm.py lays a sound effect on each one.
  K.events = [];
  K.sound = function (tl, type, at, extra = {}) {
    K.events.push(Object.assign({ tl, t: at, type }, extra));
  };

  // ---------- motion vocabulary (DESIGN §7) ----------
  // Enter: fade-up, opacity and 12 px, --t-enter, strong ease-out. No overshoot.
  K.pop = function (tl, el, b, { from = 0.97, dur = 0.4, origin = "50% 50%", y = 12 } = {}) {
    K.sound(tl, "pop", K.t(b));
    tl.fromTo(el, { opacity: 0, y, scale: from, transformOrigin: origin }, { opacity: 1, y: 0, scale: 1, duration: dur, ease: K.ease }, K.t(b));
  };
  K.enter = K.pop;
  // Arrive: something reached its place. A short settle, no bounce.
  K.land = function (tl, el, at, { follow = false } = {}) {
    K.sound(tl, "land", at);
    tl.fromTo(el, { scale: 1.025 }, { scale: 1, duration: 0.2, ease: K.ease, data: follow ? "follow" : undefined }, at);
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
  // Move an element's centre along an SVG path (path in scene pixels), through gsap's
  // x/y so scale on the same element still composes.
  K.travel = function (tl, el, path, b, dur = 0.25, ease = K.easeMove, w = 0, h = 0) {
    K.sound(tl, "whoosh", K.t(b), { dur });
    const L = path.getTotalLength();
    const p = { u: 0 };
    const place = () => {
      const q = path.getPointAtLength(L * p.u);
      gsap.set(el, { x: q.x - w / 2, y: q.y - h / 2 });
    };
    place();
    tl.fromTo(p, { u: 0 }, { u: 1, duration: dur, ease, onUpdate: place }, K.t(b));
  };
  // A ping: one thin amber ring widening and fading where the focus is.
  K.sparkle = function (tl, scene, x, y, at, { r = 44 } = {}) {
    K.sound(tl, "sparkle", at);
    const e = K.el(scene, "div", { class: "k-abs", style: { left: x - r + "px", top: y - r + "px", width: 2 * r + "px", height: 2 * r + "px", borderRadius: "50%", boxShadow: "inset 0 0 0 2px #f2c14e" } });
    tl.fromTo(e, { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.12, ease: "power1.out", data: "follow" }, at);
    tl.to(e, { scale: 1.3, opacity: 0, duration: 0.22, ease: "power1.in", data: "follow" }, at + 0.12);
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

  // One focus per beat: [[beat, x, y], ...]. A jump over 620 px is an error, so check
  // reports it; in debug renders the focus ring is drawn so a reviewer can follow it.
  K.focus = function (scene, tl, name, points) {
    for (let i = 1; i < points.length; i++) {
      const [, x0, y0] = points[i - 1], [b, x1, y1] = points[i];
      const d = Math.hypot(x1 - x0, y1 - y0);
      if (d > 620) console.error(`[kit] ${name}: focus jumps ${Math.round(d)}px at beat ${b}`);
    }
    let debug = false;
    try { debug = !!(window.__hyperframes && window.__hyperframes.getVariables().debug); } catch (e) { debug = false; }
    if (!debug) return;
    const ring = K.el(scene, "div", { class: "k-abs k-focus" });
    points.forEach(([b, x, y]) => tl.set(ring, { x, y }, K.t(b)));
  };
})();
