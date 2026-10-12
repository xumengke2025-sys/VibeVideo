# How makefx works: the brief

A 40 s explainer in the manner of Addy Osmani's "how browsers work": 18 scenes,
one 2 s bar each at 120 BPM (scene 18 holds for 3 bars), cut on the bar line.
The protagonist is one asset card: asked for, priced, generated, landed,
reused, cut, shared. Audience: developers who work with an agent.

Reference scenes in the current look: `compositions/s01-ask.html`,
`s09-lands.html`, `s13-frame.html`. Read all three before writing a scene.

## The grammar (measured from the reference video; the kit enforces it)

1. **One bar per scene.** Scene time 0–2 s. Eight beats: `K.t(b)` = b × 0.25 s.
2. **One event per beat, on the beat.** Each beat b0..b7 starts one small
   event. A tween that finishes an earlier event passes `data: "follow"` and
   may start anywhere; everything else must start on a 1/8 s grid or
   `K.check` fails the render. b7 may be a hold or a small flourish.
3. **One focus.** Each event starts where the previous one ended. List the
   focus per beat in `K.focus(scene, tl, id, [[beat, x, y], ...])`; a jump
   over 620 px fails check. Consecutive points should normally be < 400 px.
4. **Nothing else moves.** The ground, cards at rest, labels and edges are
   still. The only ambient motion allowed is on the focus.
5. **Every event makes a sound.** The kit cues its own motions (`K.pop`,
   `K.land`, `K.type`, `K.draw`, `K.travel`, `K.reveal`, `K.pulse`,
   `K.sparkle`); `K.check` names the rest from what they animate. Prefer kit
   motions so the sound matches what is seen; call `K.sound(tl, type, at)`
   for anything special (types: pop, land, type, draw, whoosh, reveal,
   sparkle, stamp, tick).
6. **Chrome.** `K.chrome(scene, tl, { title, step, balance, held,
   animateStep })` owns the four corners: chapter label and title top left,
   chapter progress top right, wordmark bottom left, balance bottom right.
   Keep content between y 190 and y 960 and 90 px from the side edges.
7. **Big and legible.** This is watched on phones. Focal cards at scale
   1.6–2.2, secondary cards 1.2–1.4, mono text ≥ 20 px, micro labels are
   decoration only.

## The look (DESIGN.md, the product's own)

A dark void where media is the only colour; chrome is quiet ink; amber is
the one thing being acted on.

- **Ground:** the scene (`class="k-scene"`) is the canvas: `#08080a` with a
  dot grid. No paper, stripes, grain, illustrations, props, characters or
  faces. Nothing decorative on the ground.
- **Surfaces:** `k-panel` (panels, terminals, editors: translucent near-black,
  1.5 px white-alpha ring, radius 16), `k-pill` and `k-chip` (mono, ringed),
  `k-button` (the one amber primary per panel), `k-micro` (uppercase label).
  Rings are `box-shadow`, never borders. No drop shadows on media.
- **Cards** are real product cards: `K.card(...)` media on a matte, a meta row
  (name, credits in mono), and the ring. State lives only in the ring:
  `rest`, `hover`, `wait` (queued), `generating` (amber, half strength, with
  the progress bar), `selected` (solid amber), `failed` (danger). Ready says
  nothing: no badge, no check. Nothing ever sits on top of media except the
  progress bar and a slot chip.
- **Colour:** media has all of it (`K.harbourArt({ boat, mood })`, day, dusk,
  night; draw other media in the same rich, flat, gradient style). Chrome is
  ink: `--k-ink`, `--k-ink-2`, `--k-ink-3`. Amber `--k-accent` only for the
  thing acted on now, the progress fill, the primary button, a credit amount
  moving. Danger `--k-danger` only for failure. Edges are white alpha
  (`K.edge`), reference edges brighten to .5 when picked.
- **Type:** `var(--k-display)` (Space Grotesk 600) for names, titles, buttons;
  `var(--k-mono)` (JetBrains Mono) for credits, times, ids, code, JSON.
  Sentence case everywhere except micro labels.
- **Motion (DESIGN §7):** things enter with a fade-up (`K.pop`: opacity, 12 px,
  strong ease-out, no overshoot); media fades in over its placeholder
  (`K.reveal`); rings change state fast (`K.ring`); a picked thing pulses
  amber once (`K.pulse`); moves between two known places use `K.easeMove`;
  exits are short and never bounce. No squash, no stretch, no wobble.
- **Metaphors become the product.** Where the old scene drew a house, a jar,
  a printer, a pipe or a magnifier, show the real thing instead: panels, cards,
  rings, the balance pill, labelled nodes joined by edges, a stream of dots.

## The kit (`kit/kit.js`, global `K`; read it, don't edit it)

- `K.card(parent, { id, left, top, scale, art, name, cr, state })` returns the
  card; `card.k` holds its geometry in scene pixels (`W, H, cx, mediaCy,
  bottom, left, top, s`). Parts by class via `K.part(card, "k-thumb" |
  "k-bar" | "k-ring" | "k-meta" | "k-name" | "k-cr" | "k-media")`.
- `K.ring(tl, card, state, at, { follow })`, `K.progress(tl, card, from, to,
  at, dur)`, `K.reveal(tl, card, b)`, `K.pulse(tl, card, at, { back })`.
- `K.balance(tl, scene, at, { balance, held })` changes the balance pill (the
  held suffix is the lighter "−80").
- Motion: `K.pop` (= `K.enter`), `K.land` (a short settle), `K.type`,
  `K.draw(tl, path, b, dur)`, `K.travel(tl, el, path, b, dur, ease, w, h)`,
  `K.sparkle` (one amber ping ring).
- Layout: `K.edge(scene, d, { alpha })` returns a path; `K.leader(scene, x1,
  y1, x2, y2, label)`; `K.cursor(scene, x, y, label)` returns the element.
- Rules: `K.check(tl, id)` and `K.focus(...)` at the end of every scene.
- Pitfalls: `K.pop` animates `y`, so place popped elements with left/top, not
  a transform. Elements written in the template sit under cards the script
  adds later: `scene.appendChild(el)` anything that must travel above cards.
  Text mid-fade can fail the contrast check; slide or clip instead.

If you need a helper the kit lacks, write it inside your scene's script.

## Scene file contract

`compositions/sNN-slug.html`, a `<template>` sub-composition like the
references: styles and script inside the template, root `#sNN-root` with
`data-composition-id="sNN-slug"`, every id prefixed `sNN-`, one paused
timeline registered as `window.__timelines["sNN-slug"]`, `gsap.fromTo` for
entrances (no CSS transforms on tweened elements), no `<br>`, no
`Math.random`/`Date.now`.

## Facts (use these exactly; do not invent product behaviour)

- Space `alv/salt-harbour` (the "Salt Harbour, Low Tide" demo space).
- Connect: `claude mcp add --transport http makefx https://makefx.app/mcp`.
  OAuth 2.1; the person signs in with Google once; no provider keys.
- The protagonist: an 8 s video, model `video/h3-max`, 480p, 10 cr/s = 80 cr.
  Its call: `create_asset {"space_id":"alv/salt-harbour","kind":"video",
  "model":"video/h3-max","prompt":"camera flight over the harbour at low tide",
  "references":[{"asset_id":"as_s02","slot":"start_frame"}],
  "params":{"duration_seconds":8,"resolution":"480p"}}`.
  Balance 2,000 cr before, 1,920 cr after it lands. 1 credit = €0.01.
- Other prices: `image/flux-2` still 3 cr; a 4 s 480p clip 40 cr;
  `image/frame` 0 cr; `video/timeline` 0 cr (renders in the browser);
  Describe 2 cr.
- Every change to a space goes through one writer (a per-space durable
  object), in order: it validates, checks the balance, writes the card as
  `queued` with its recipe and the credits held, then broadcasts to every
  open canvas over a socket.
- Price: quoted and held before anything runs; charged when it lands;
  released (refunded) if it fails. A failed generation costs nothing. In
  on-screen text never say hold/held/settle/release (ledger words stay in the
  ledger); say "priced before it runs", "charged when it lands", "refunded if it
  fails". The balance pill's lighter "−80" suffix is the product's own UI.
- One durable workflow per asset. Steps in order: mark running → prepare
  references → submit → poll & persist → inspect → poster (video) →
  complete. `submit` is never retried, so a retry can never pay twice;
  polling retries with growing waits (5 s, 10 s, 20 s …). No step returns
  bytes: media streams from the provider straight into storage (R2) at
  `media/{account}/{space}/{asset}.mp4`.
- Statuses: `queued` → `generating` → `ready` (or `failed`, with a short
  error like `provider_timeout`).
- Recipe: provider, model, prompt, settings (params), references with their
  slots, price. Immutable once generated. "continue", never "reproduce".
- Reference slots differ per model and each takes certain kinds. The
  protagonist's model `video/h3-max` has only `start_frame` and `end_frame`,
  one image each (no `reference` slot). Other models have `reference`
  (images), `reference_video`, `reference_audio`. A card fills a slot of a
  later card when its kind fits; a video reaches an image slot through
  `image/frame`.
- Describe: reads an image and writes an editable traits text onto the
  asset (e.g. "red scarf, round glasses"), for later prompts. 2 cr.
- Timeline: `video/timeline`, a browser model; tracks for clips, voice,
  music, captions; renders in your browser, free. The finished cut is a
  card with its own recipe listing the clips it was cut from.
- Sharing: demo spaces open to anyone without signing in, recipes and
  prices included.
- Words: agent (never assistant), canvas (the view), space (the thing),
  credits with the unit (`80 cr`). "recipe" is the only metaphor in text.
  Titles in sentence case, ≤ 6 words.

## Storyboard

Chapters (progress pill): 1 ask · 2 price · 3 generate · 4 land · 5 continue ·
6 cut · 7 share. `animateStep` is true only on a chapter's first scene. Balance
column is what the pill shows at the scene's start → where it ends.

| # | file | title | step | animateStep | balance | beats |
|-|-|-|-|-|-|-|
| 1 | s01-ask | Ask your agent | 1 | yes | 2,000 cr | done |
| 2 | s02-connect | One command connects | 1 | no | 2,000 cr | the add command types in the agent's terminal → a line runs from the agent to a makefx node → "Sign in with Google" is pressed, a check → an empty provider-keys field is marked "none needed" |
| 3 | s03-toolcall | A tool call, not a form | 1 | no | 2,000 cr | the create_asset JSON builds field by field in a panel → it leaves as a pill into the space's canvas |
| 4 | s04-writer | One space, one writer | 2 | yes | 2,000 cr (the hold shows inside the writer; it reaches the pill in s05) | three request pills queue at one "space · alv/salt-harbour" writer node → it takes one at a time → validate, balance, write ticks → a card fades up `queued` (wait ring) → broadcast edges to two canvases |
| 5 | s05-price | Price first, charged on landing | 2 | no | 2,000 cr → 2,000 cr −80 | the estimate pill computes 8 s × 10 cr/s = 80 cr → the 80 cr travels from the card to the balance pill and shows as the held "−80" → three short rules: held before it runs · charged when it lands · refunded if it fails |
| 6 | s06-workflow | One workflow per asset | 3 | yes | 2,000 cr −80 | a track of seven step nodes; the card rides it; each lights as it passes; ring and bar follow the state |
| 7 | s07-submit | Submit once, poll many | 3 | no | 2,000 cr −80 | submit fires once with a lock ("never retried") → polls return on a time axis at growing intervals (5 s, 10 s, 20 s) → done |
| 8 | s08-stream | Bytes go straight to storage | 3 | no | 2,000 cr −80 | provider node → storage node (r2) with the workflow node between; a stream of dots flows provider → r2 past the workflow, which holds none → the media path `media/{account}/{space}/{asset}.mp4` |
| 9 | s09-lands | It lands, live | 4 | yes | 2,000 cr −80 → 1,920 cr | done |
| 10 | s10-failure | A failure costs nothing | 4 | no | 1,920 cr −40 → 1,920 cr | a sibling clip (4 s, 40 cr) generating → bar stalls → ring snaps to danger, meta row tints, `provider_timeout` → the held −40 leaves the balance: refunded |
| 11 | s11-recipe | Every asset keeps its recipe | 4 | no | 1,920 cr | the card opens its recipe panel → fields fill: provider fal, model, prompt, params, references, price → a lock: immutable once generated |
| 12 | s12-material | Every asset is material | 5 | yes | 1,920 cr | a still fills the next clip's `start_frame`, a pulled frame fills `end_frame` (video/h3-max has only these two) → reference edges draw → the next clip's price shows 40 cr |
| 13 | s13-frame | Pull a frame, free | 5 | no | 1,920 cr | done |
| 14 | s14-describe | Describe keeps the traits | 5 | no | 1,920 cr → 1,918 cr | a character still (draw it: harbour keeper, red scarf, round glasses) → Describe runs (2 cr, balance ticks) → traits text writes onto the asset, editable → the text goes into the next prompt |
| 15 | s15-timeline | The cut happens in your browser | 6 | yes | 1,918 cr | an editor panel with a ruler and four tracks: clips snap in, voice, music, captions → render in your browser fills → free · 0 cr |
| 16 | s16-cut | A cut is a card too | 6 | no | 1,918 cr | the finished film card fades up on the canvas → reference edges from its clips → its recipe lists video/timeline, 0 cr, and the clips it was cut from |
| 17 | s17-share | Anyone can open the space | 7 | yes | 1,918 cr | the space's link opens signed out → visitors' cursors arrive → each card they point at shows its recipe and price |
| 18 | s18-finale | How makefx works | 7 | no | 1,918 cr | 6 s: the chain of cards builds one per beat with its edges → zoom out to the whole space with its notes → all chrome fades; the closing block (POSITIONING §2) arrives a beat at a time: the wordmark, "Your agent makes the media. You keep the canvas.", "Open a demo space. Send your agent when you're ready.", makefx.app; still to 6 s |

## Review loop (every scene)

1. `npx --yes hyperframes@0.8.71 check` → 0 errors, 0 warnings.
2. Render the debug pass (`--variables '{"debug":true}'`, draft, `-f 24`) and
   a clean pass, then `tools/beat-sheet.sh <video> 24 <first scene start>
   <scene count> <out.jpg>`: one still per beat, 0.2 s after it. Look at
   every beat: is there exactly one place to look, is it where the pink ring
   is, is anything moving elsewhere, does it look like makefx?
3. Fix and repeat. Set `DO_NOT_TRACK=1` on every hyperframes command. Keep
   only one root HTML with `data-composition-id` in the project (a second one
   doubles the audio); render other roots with `-c`.
