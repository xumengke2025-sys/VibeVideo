// Reads every scene's sound cues and writes assets/audio/cues.json.
//
// Loads each scene the way the render does (its <template> into one page, with
// the kit), then reads K.events and offsets each cue by the scene's start in
// index.html. The sound effects are laid from this file, so they land on the
// same beats as the picture.
//
//   CHROME=<chromium binary> node tools/extract-cues.mjs
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const require = createRequire(import.meta.url);
const puppeteer = require(process.env.PUPPETEER_CORE || "puppeteer-core");

// INDEX picks another root (a preview cut); OUT another cue file.
const index = fs.readFileSync(path.join(root, process.env.INDEX || "index.html"), "utf8");
const scenes = [...index.matchAll(/data-composition-id="([^"]+)" data-composition-src="([^"]+)"\s+data-start="([\d.]+)" data-duration="([\d.]+)"/g)]
  .map(([, id, src, start, duration]) => ({ id, src, start: +start, duration: +duration }));

const harness = `<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="kit/kit.css"><script src="assets/vendor/gsap.min.js"></script>
<script>window.__timelines = {}; window.__hyperframes = { getVariables: () => ({}) };</script>
<script src="kit/kit.js"></script></head><body></body></html>`;

const types = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".woff2": "font/woff2" };
const server = http.createServer((req, res) => {
  const url = decodeURIComponent(req.url.split("?")[0]);
  if (url === "/__cues.html") return res.end(harness);
  const file = path.join(root, url);
  if (!file.startsWith(root) || !fs.existsSync(file)) return res.writeHead(404).end();
  res.writeHead(200, { "content-type": types[path.extname(file)] || "application/octet-stream" }).end(fs.readFileSync(file));
});
await new Promise((ok) => server.listen(0, ok));
const base = `http://127.0.0.1:${server.address().port}`;

const browser = await puppeteer.launch({ executablePath: process.env.CHROME, channel: process.env.CHROME ? undefined : "chrome", args: ["--no-sandbox"] });
const page = await browser.newPage();
const errors = [];
page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
page.on("pageerror", (e) => errors.push(String(e)));
await page.setViewport({ width: 1920, height: 1080 });
await page.goto(`${base}/__cues.html`);

const cues = await page.evaluate(async (scenes) => {
  for (const s of scenes) {
    const html = await (await fetch(s.src)).text();
    const tpl = new DOMParser().parseFromString(html, "text/html").querySelector("template");
    const host = document.createElement("div");
    host.style.cssText = "position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:hidden";
    document.body.appendChild(host);
    for (const node of [...tpl.content.childNodes]) {
      if (node.nodeName === "SCRIPT") {
        const sc = document.createElement("script");
        sc.textContent = node.textContent;
        host.appendChild(sc);
      } else host.appendChild(document.importNode(node, true));
    }
  }
  const out = [];
  for (const s of scenes) {
    const tl = window.__timelines[s.id];
    if (!tl) continue;
    for (const e of window.K.events.filter((e) => e.tl === tl)) {
      out.push({ t: +(s.start + e.t).toFixed(4), type: e.type, scene: s.id, ...(e.dur ? { dur: e.dur } : {}), ...(e.n ? { n: e.n } : {}) });
    }
  }
  return out.sort((a, b) => a.t - b.t);
}, scenes);

await browser.close();
server.close();
const missing = scenes.filter((s) => !cues.some((c) => c.scene === s.id)).map((s) => s.id);
fs.writeFileSync(path.join(root, process.env.OUT || "assets/audio/cues.json"), JSON.stringify({ scenes, cues }, null, 1));
console.log(`${cues.length} cues from ${scenes.length - missing.length}/${scenes.length} scenes${missing.length ? `; missing ${missing.join(", ")}` : ""}`);
if (errors.length) console.log("page errors:\n  " + errors.slice(0, 10).join("\n  "));
