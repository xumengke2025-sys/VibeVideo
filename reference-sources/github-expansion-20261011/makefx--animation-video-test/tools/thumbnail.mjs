// The YouTube thumbnail, built with the video's own kit so it matches the film.
//
//   CHROME=<chromium binary> node tools/thumbnail.mjs
// VARIANT=prompt|recipe|chain; writes renders/thumbnail-<variant>.png (3840 × 2160).
// Scale it to 1280 × 720 for upload.
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const puppeteer = createRequire(import.meta.url)(process.env.PUPPETEER_CORE || "puppeteer-core");

const VARIANT = process.env.VARIANT || "recipe";
const page = `<!doctype html><html><head><meta charset="utf-8">
<style>
  @font-face { font-family: "Space Grotesk"; src: url("assets/fonts/SpaceGrotesk-600.woff2") format("woff2"); font-weight: 600; }
  @font-face { font-family: "JetBrains Mono"; src: url("assets/fonts/JetBrainsMono-500.woff2") format("woff2"); font-weight: 500; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 1920px; height: 1080px; overflow: hidden; background: #08080a; }
  .t-h { font: 600 132px/0.95 var(--k-display); letter-spacing: -0.045em; color: var(--k-ink); white-space: pre; }
  .t-h b { color: var(--k-accent); font-weight: 600; }
  .t-glow { position: absolute; border-radius: 50%; background: radial-gradient(closest-side, rgba(242,193,78,.28), rgba(242,193,78,0)); pointer-events: none; }
  .t-term { font: 500 46px/1.5 var(--k-mono); color: var(--k-ink-2); padding: 34px 44px; }
  .t-term b { color: var(--k-ink); font-weight: 500; }
  .t-row { display: flex; gap: 34px; font: 500 38px/1.75 var(--k-mono); color: var(--k-ink); white-space: nowrap; }
  .t-row > span:first-child { width: 210px; font: 500 24px/2.8 var(--k-display); letter-spacing: .16em; text-transform: uppercase; color: var(--k-ink-3); }
  .t-mark { font: 600 44px/1 var(--k-display); letter-spacing: -0.025em; color: var(--k-ink); }
  .t-mark b { color: var(--k-accent); font-weight: 600; }
</style>
<link rel="stylesheet" href="kit/kit.css"><script src="assets/vendor/gsap.min.js"></script><script src="kit/kit.js"></script>
</head><body><div id="scene" class="k-scene"></div>
<script>
  const scene = document.getElementById("scene"), V = ${JSON.stringify(VARIANT)};
  const el = (tag, cls, style, html) => K.el(scene, tag, { class: "k-abs " + cls, style }, html);
  const glow = (x, y, r) => el("div", "t-glow", { left: x - r + "px", top: y - r + "px", width: 2 * r + "px", height: 2 * r + "px" });

  if (V === "timeline") {
    // The chain of assets above, the cut below: every card is material for the timeline.
    el("div", "t-h", { left: "80px", top: "54px", fontSize: "104px" }, "Every asset is <b>material</b>");
    el("div", "t-mark", { left: "1700px", top: "80px" }, "make<b>fx</b>");
    glow(740, 430, 420);
    const still = K.card(scene, { id: "a", left: 90, top: 380, scale: 1.2, art: K.harbourArt({ boat: -20 }), name: "quay at low tide", cr: "3 cr" });
    const flight = K.card(scene, { id: "b", left: 510, top: 250, scale: 1.9, art: K.harbourArt({ boat: 12 }), name: "harbour flight", cr: "80 cr", state: "selected" });
    const frame = K.card(scene, { id: "c", left: 1080, top: 300, scale: 1.2, art: K.harbourArt({ boat: 40 }), name: "frame 4.8 s", cr: "0 cr" });
    const next = K.card(scene, { id: "d", left: 1520, top: 330, scale: 1.5, art: K.harbourArt({ boat: 30, mood: "dusk" }), name: "next clip", cr: "40 cr" });
    const amber = (d, w = 3, dash) => { const p = K.edge(scene, d); p.setAttribute("stroke", "rgba(242,193,78,.75)"); p.setAttribute("stroke-width", w); if (dash) p.setAttribute("stroke-dasharray", dash); return p; };
    amber("M378 470 C 440 470, 450 420, 510 420");
    amber("M966 420 C 1020 420, 1030 400, 1080 400");
    amber("M1368 400 C 1440 400, 1450 460, 1520 460");
    const tag = (x, y, t) => el("div", "k-chip", { left: x + "px", top: y + "px", fontSize: "18px" }, t);
    tag(382, 486, "start_frame"); tag(984, 446, "frame"); tag(1374, 476, "start_frame");
    // The timeline: a ruler, a clips track cut from the two videos, voice under it.
    const P = { l: 80, t: 740, w: 1760, h: 280 }, X0 = P.l + 130, PX = 135; // 135 px per second
    el("div", "k-panel", { left: P.l + "px", top: P.t + "px", width: P.w + "px", height: P.h + "px" });
    el("div", "k-micro", { left: P.l + 26 + "px", top: P.t + 22 + "px", fontSize: "20px" }, "video/timeline · harbour cut · 0 cr");
    for (let s = 0; s <= 12; s++) el("div", "k-mono", { left: X0 + s * PX - 10 + "px", top: P.t + 58 + "px", fontSize: "18px", color: "rgba(245,245,244,.5)" }, s % 2 ? "" : s + "s");
    [["clips", 104], ["voice", 206]].forEach(([n, y]) => el("div", "k-micro", { left: P.l + 26 + "px", top: P.t + y + 18 + "px", fontSize: "18px" }, n));
    for (let s = 0; s < 12; s++) {
      const dusk = s >= 8;
      el("div", "", { left: X0 + s * PX + 2 + "px", top: P.t + 96 + "px", width: PX - 4 + "px", height: "76px", borderRadius: "6px", overflow: "hidden",
        boxShadow: "0 0 0 1.5px " + (dusk ? "rgba(255,255,255,.2)" : "rgba(242,193,78,.8)") }, K.harbourArt({ boat: dusk ? 20 + (s - 8) * 12 : -40 + s * 11, mood: dusk ? "dusk" : "day" }));
    }
    el("div", "", { left: X0 + "px", top: P.t + 206 + "px", width: 12 * PX + "px", height: "44px", borderRadius: "6px", background: "rgba(245,245,244,.06)",
      backgroundImage: "repeating-linear-gradient(90deg, rgba(245,245,244,.55) 0 3px, transparent 3px 9px)", WebkitMaskImage: "linear-gradient(transparent 18%, #000 18% 82%, transparent 82%)" });
    el("div", "", { left: X0 + 8 * PX - 2 + "px", top: P.t + 50 + "px", width: "4px", height: "210px", background: "#f2c14e", borderRadius: "2px" });
    // Each video drops into its place on the track.
    amber("M" + flight.k.cx + " " + flight.k.bottom + " C " + flight.k.cx + " 700, " + (X0 + 4 * PX) + " 690, " + (X0 + 4 * PX) + " " + (P.t + 94), 3, "4 10");
    amber("M" + next.k.cx + " " + next.k.bottom + " C " + next.k.cx + " 700, " + (X0 + 10 * PX) + " 690, " + (X0 + 10 * PX) + " " + (P.t + 94), 3, "4 10");
  } else if (V === "prompt") {
    // One sentence to the agent, one card on the canvas: the whole product in a glance.
    const term = el("div", "k-panel t-term", { left: "80px", top: "150px", width: "1000px", height: "250px" },
      "<div>$ claude</div><div>&gt; <b>make a camera flight</b></div><div>&nbsp;&nbsp;<b>over the harbour</b></div>");
    glow(1390, 640, 560);
    const card = K.card(scene, { id: "c", left: 1000, top: 420, scale: 3.1, art: K.harbourArt({ boat: 12 }), name: "harbour flight", cr: "80 cr", state: "selected" });
    const arc = K.edge(scene, "M760 420 C 820 560, 900 600, 1000 620", { alpha: 0.0 });
    arc.setAttribute("stroke", "#f2c14e"); arc.setAttribute("stroke-width", "5"); arc.setAttribute("stroke-dasharray", "2 16");
    el("div", "k-pill k-amber", { left: "560px", top: "450px", fontSize: "34px", padding: "12px 26px", transform: "rotate(-6deg)" }, "create_asset");
    el("div", "t-h", { left: "80px", top: "700px", fontSize: "108px" }, "Your agent<br>makes the <b>media</b>.");
    el("div", "t-mark", { left: "1690px", top: "60px" }, "make<b>fx</b>");
  } else if (V === "recipe") {
    // The difference in one frame: the media, and next to it how it was made and what it cost.
    glow(560, 560, 520);
    const card = K.card(scene, { id: "c", left: 70, top: 300, scale: 2.95, art: K.harbourArt({ boat: 12 }), name: "harbour flight", cr: "80 cr", state: "selected" });
    const panel = el("div", "k-panel", { left: "860px", top: "300px", width: "990px", height: "520px", padding: "40px 48px" });
    panel.innerHTML = '<div class="k-micro" style="font-size:24px;margin-bottom:22px">recipe</div>' +
      [["provider", "fal"], ["model", "video/h3-max"], ["prompt", "camera flight over the harbour"], ["params", "8 s · 480p"], ["price", '<span style="color:#f2c14e">80 cr</span>']]
        .map(([k, v]) => '<div class="t-row"><span>' + k + '</span><span>' + v + '</span></div>').join("");
    el("div", "t-h", { left: "70px", top: "70px", fontSize: "118px" }, "Every asset keeps its <b>recipe</b>");
    el("div", "t-mark", { left: "1690px", top: "930px" }, "make<b>fx</b>");
  } else {
    // The story as one lit chain: ask, generate, pull a frame, continue, cut.
    const Y = 600, cards = [["quay at low tide", "3 cr", { boat: -20 }], ["harbour flight", "80 cr", { boat: 12 }], ["frame 4.8 s", "0 cr", { boat: 40 }], ["next clip", "40 cr", { boat: 40, mood: "dusk" }], ["harbour cut", "0 cr", { boat: 20, mood: "night" }]];
    glow(640, Y + 60, 420);
    cards.forEach(([name, cr, art], i) => {
      const s = i === 1 ? 2.2 : 1.35, x = [60, 360, 960, 1300, 1620][i], y = i === 1 ? Y - 180 : i % 2 ? Y - 60 : Y + 40;
      K.card(scene, { id: "c" + i, left: x, top: y, scale: s, art: K.harbourArt(art), name, cr, state: i === 1 ? "selected" : "rest" });
    });
    ["M384 700 C 400 700, 330 640, 360 640", "M888 560 C 930 560, 920 700, 960 700", "M1284 700 C 1300 700, 1270 600, 1300 600", "M1624 600 C 1640 600, 1600 700, 1620 700"]
      .forEach((d) => { const p = K.edge(scene, d, { alpha: 0.6 }); p.setAttribute("stroke", "#f2c14e"); p.setAttribute("stroke-width", "4"); });
    el("div", "t-h", { left: "70px", top: "90px", fontSize: "150px" }, "How make<b>fx</b> works");
    el("div", "k-pill", { left: "76px", top: "270px", fontSize: "38px", padding: "12px 26px", color: "#f5f5f4" }, "in 40 seconds");
  }
  document.fonts.ready.then(() => (window.__ready = true));
</script></body></html>`;

const types = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".woff2": "font/woff2" };
const server = http.createServer((req, res) => {
  const url = decodeURIComponent(req.url.split("?")[0]);
  if (url === "/__thumb.html") return res.end(page);
  const file = path.join(root, url);
  if (!file.startsWith(root) || !fs.existsSync(file)) return res.writeHead(404).end();
  res.writeHead(200, { "content-type": types[path.extname(file)] || "application/octet-stream" }).end(fs.readFileSync(file));
});
await new Promise((ok) => server.listen(0, ok));
const browser = await puppeteer.launch({ executablePath: process.env.CHROME, channel: process.env.CHROME ? undefined : "chrome", args: ["--no-sandbox"] });
const tab = await browser.newPage();
tab.on("pageerror", (e) => console.error("page error:", String(e)));
await tab.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 2 });
await tab.goto(`http://127.0.0.1:${server.address().port}/__thumb.html`);
await tab.waitForFunction("window.__ready === true");
await tab.screenshot({ path: path.join(root, `renders/thumbnail-${VARIANT}.png`) });
await browser.close();
server.close();
console.log(`renders/thumbnail-${VARIANT}.png`);
