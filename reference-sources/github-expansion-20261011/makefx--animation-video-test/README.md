# How makefx works: an animation video test

A 40-second explainer for [makefx](https://makefx.app), written as code and
rendered to video. It follows the rhythm of Addy Osmani's "how browsers work"
animation, and is drawn in makefx's own design language.

**Watch:** https://youtu.be/k28tsX6h_Jg · files in [`renders/`](renders/)

![Thumbnail](renders/thumbnail.jpg)

Every file used to make it is here: the brief, the kit, the 18 scenes, the
sound tools, the renders, the thumbnail, and the earlier versions it grew out
of.

## The recipe

| | |
|-|-|
| Picture | 18 HTML scenes rendered with [HyperFrames](https://github.com/heygen-com/hyperframes) (Apache-2.0), 3840×2160 and 1920×1080, 24 fps, 40 s |
| Made by | Claude (Opus 5.5) in Claude Code. The kit and three reference scenes were written first; five agents then wrote the other fifteen scenes in parallel from one brief, [SCENES.md](SCENES.md) |
| Look | makefx's design system: the canvas void and dot grid, real product cards, rings for state, amber only on the thing being acted on |
| Rhythm | 120 BPM. One 2 s bar per scene, one event per eighth note, one place to look at a time |
| Sound | Synthesized by [tools/make-bgm.py](tools/make-bgm.py): music that follows the chapters, plus 169 sound effects placed on the on-screen events |
| Media | The harbour pictures are drawn stand-ins; credits and balances follow makefx's price sheet |

## How it works

**The grammar is enforced in code.** [kit/kit.js](kit/kit.js) turns beats into
time (`K.t(b)` = b × 0.25 s). `K.check` fails the render when an event starts
off the beat grid. `K.focus` fails it when attention would jump more than
620 px between beats, and in a debug render it draws the focus ring so a
reviewer can follow it.

**Every event makes a sound.** The kit's motions (pop, land, type, draw,
travel, reveal, pulse) record a cue as they are scheduled. `K.check` names
any event nobody cued by what it animates.
[tools/extract-cues.mjs](tools/extract-cues.mjs) loads all scenes in a headless
browser and writes [assets/audio/cues.json](assets/audio/cues.json).
`make-bgm.py` then lays one sound effect on each cue, pitched to that bar's
chord, over music whose chords, drums, risers and fills follow the chapters.

**One scene is one file.** Each `compositions/sNN-*.html` is a HyperFrames
sub-composition with its own paused GSAP timeline, 2 s long (the finale 6 s).
[index.html](index.html) places them on the bar lines and adds the soundtrack.

**Review was visual.** Each scene was checked on a sheet of one still per
beat, taken 0.2 s after the beat ([tools/beat-sheet.sh](tools/beat-sheet.sh)),
with and without the focus ring.

The full process, including the brief the agents worked from, is in
[docs/process.md](docs/process.md). What was measured in the reference video
is in [docs/research.md](docs/research.md).

## Layout

```
index.html              the 40 s cut: 18 scenes on bar lines, soundtrack
compositions/           one file per scene
kit/                    the shared look (kit.css) and grammar, motions, cues (kit.js)
SCENES.md               the brief: grammar, look, facts, storyboard, review loop
tools/                  cue extractor, soundtrack synth, thumbnail, beat sheets
assets/                 fonts (OFL), GSAP, soundtrack and cues
renders/                1080p and 4K renders, thumbnails, a still per scene
history/spike/          the first HyperFrames test scene
history/v1-illustrated/ the first full cut, in an illustrated style
YOUTUBE.md              title and description as published
```

## Render it

Needs Node 22+, FFmpeg, [uv](https://docs.astral.sh/uv/) for the soundtrack,
and Chrome or Chromium for the cue and thumbnail tools (set `CHROME` to its
path if it is not the system Chrome).

```bash
npm install                 # puppeteer-core, for the tools
npm run check               # lint, runtime, layout, motion, contrast
npm run cues                # scenes → assets/audio/cues.json
npm run soundtrack          # cues → assets/audio/soundtrack.wav
npx --yes hyperframes@0.8.71 render -f 24 -q high -o renders/how-makefx-works.mp4
npm run render:4k
VARIANT=timeline npm run thumbnail
```

Add `--variables '{"debug":true}'` to a render to see the focus ring.

## Licenses

The code in this repository is Apache-2.0 ([LICENSE](LICENSE)). Space Grotesk
and JetBrains Mono are under the SIL Open Font License 1.1
([assets/fonts](assets/fonts)). GSAP is under GreenSock's
[standard license](https://gsap.com/standard-license). makefx and its wordmark
belong to makefx.
