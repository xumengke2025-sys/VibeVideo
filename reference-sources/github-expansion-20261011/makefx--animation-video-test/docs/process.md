# How the video was made

All of it happened in one Claude Code session on 2026-09-24, with a person
reviewing each stage.

1. **Research.** The reference video was measured frame by frame and its audio
   analysed ([research.md](research.md)): 120 BPM, one scene per bar, one event
   per eighth note, one place to look.
2. **Spike.** One scene rebuilt in HyperFrames to test canvas drawing,
   determinism and render speed ([history/spike](../history/spike)): a 6 s scene
   renders in about 5 s; two renders with different worker counts match to
   48 dB PSNR.
3. **Kit and three reference scenes.** The grammar went into code (`K.t`,
   `K.check`, `K.focus`), plus the chrome, a card, motion helpers, and scenes 1,
   9 and 13. They were rendered, reviewed as beat sheets, and fixed until each
   beat had one place to look.
4. **Fifteen scenes in parallel.** Five agents took three scenes each, working
   in separate copies of the project from one brief ([SCENES.md](../SCENES.md)),
   each running its own check → render → beat sheet → fix loop. Their reports
   were read and their sheets reviewed before merging; two factual errors were
   caught this way (a slot the model does not have, a label repeating it).
5. **First cut** ([history/v1-illustrated](../history/v1-illustrated)): an
   illustrated style close to the reference, with a first synthesized track.
6. **Sound.** The kit started recording a cue for every event; the soundtrack
   script was rewritten to follow the chapters and put a sound effect on each
   cue.
7. **makefx's own look.** The kit was rebuilt from makefx's DESIGN.md (void,
   rings, product cards, amber on the focus, corner chrome). Three reference
   scenes were redone and approved, then five agents ported the other fifteen.
8. **Polish.** Off-position labels fixed, on-screen copy checked against
   makefx's positioning (ledger words out, the closing block on the end card),
   a 4K render, a thumbnail, the YouTube upload.

## The agent brief

Each scene agent got a workspace of its own and this prompt, with its three
scene names filled in:

> Read first, fully: SCENES.md (the brief: grammar, the look, kit API, facts,
> storyboard with per-scene chrome and balance, review loop), kit/kit.js,
> kit/kit.css, and the three reference scenes. Then read the old versions of
> your scenes; keep their story, facts and beat rhythm where they still fit,
> and rebuild them in the new look.
>
> 1. Replace this workspace's index.html with a preview root that mounts only
>    your three scenes.
> 2. Rewrite each scene file. Plan the 8 beats and the focus path first: one
>    event per beat, each starting where the last ended, everything else still.
>    Use kit motions so every event gets its sound. Every fact from SCENES.md.
> 3. Review loop: `hyperframes check` to 0 errors and 0 warnings, then a debug
>    render and a clean render, `tools/beat-sheet.sh`, and look at every beat.
>    At least two rounds. Ask of every frame: one place to look, nothing else
>    moving, does it look like the makefx product?
> 4. Do not edit kit/ files.
>
> Reply with the files you wrote, one line per beat, the final check line, the
> render and sheet paths, and anything in the brief or kit that was wrong or
> missing.

The "wrong or missing" answers fed back into the kit: `K.travel` composing with
scale, chained progress fills, media art marked for layout checks, focus jumps
reported as errors.
