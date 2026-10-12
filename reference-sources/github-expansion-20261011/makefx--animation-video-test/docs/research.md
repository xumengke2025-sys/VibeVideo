# What the reference video does

The reference is Addy Osmani's 40-second "how browsers work" animation
(Claude Opus 5.5 drew each frame in JavaScript). These are measurements of it,
made with ffmpeg and a few lines of numpy, and they became the rules this
video follows.

| | Measured |
|-|-|
| Format | 1920×1080, 24 fps, 40 s, a music track |
| Tempo | 120 BPM: audio onsets repeat every 0.50 s, bars every 2.0 s |
| Cuts | 17 hard cuts, on the bar lines (2.0, 4.0, 6.0 … s); one scene per bar |
| Events | about one new event per eighth note (250 ms), 6–8 per scene, the last beat often a hold |
| Motion | median 0.64% of pixels change per frame (p90 3.6%); about 15 small moving regions per frame |
| Focus | each event starts where the previous one ended; nothing else moves |
| Chrome | a fixed title top left and a chapter ring top right in every scene |
| Styles | two looks alternate: illustrated metaphor scenes and blueprint mechanism scenes |

The same measures on this video: median 0.21% of pixels change per frame,
about 4 moving regions, cuts on every bar.

## Ways people make videos like this

| Approach | How | Suits |
|-|-|-|
| Canvas/WebGL, `frame = f(t)` | a pure draw function per scene, stepped frame by frame in a headless browser, joined with ffmpeg | full control, custom character |
| Remotion | React components reading the current frame | templated, data-driven video (company license above three people) |
| Motion Canvas / Revideo | generator timelines on a scene graph | step-by-step explainers |
| HyperFrames | plain HTML/CSS/GSAP; the renderer owns the clock and seeks each frame | agent-written video; used here |
| Manim | Python scenes | math and geometry |
| After Effects / Rive / Lottie | keyframes by hand | the most polish, the least automation |
