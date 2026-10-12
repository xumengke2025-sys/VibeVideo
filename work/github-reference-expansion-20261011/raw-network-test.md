# The Vietnam War — Explained (2-min animated explainer)

Videos (2:22, 30 fps, voiceover + music + SFX + subtitles):
- `out/vietnam-war-explained-web.mp4` — landscape 16:9 (1920×1080)
- `out/vietnam-war-explained-vertical-web.mp4` — vertical 9:16 (1080×1920) for Shorts / Reels / TikTok

Made as an experiment with Claude Opus 5.5.

Everything is procedural — HTML canvas + JS for visuals, OpenAI `gpt-4o-mini-tts` narration (falls back to macOS `say`), numpy for music + SFX.
Put `OPENAI_API_KEY=...` in a `.env` file (never committed) to use the OpenAI voice.

## Files
- `narration.json` — script: scenes, sentences, sound-effect cues
- `scripts/build_audio.py` — TTS narration, music bed, SFX → `audio/final_mix.wav` + `src/timings.js`
- `src/` — animation engine (`core.js`, `map.js`, `assets.js`, `scenes.js`, `main.js`) and `index.html` player
- `scripts/render.mjs` — renders frames with Playwright and pipes them to ffmpeg

## Rebuild
```bash
.venv/bin/python scripts/build_audio.py   # after editing narration.json
node scripts/render.mjs                    # full MP4 (16:9)
node scripts/render.mjs --vertical         # 9:16 MP4
node scripts/render.mjs --stills 5,30,60   # preview frames into build/
```
Open `src/index.html` (or `src/index.html?vertical`) in a browser to play or scrub it live (Space = play/pause, ←/→ = seek).
