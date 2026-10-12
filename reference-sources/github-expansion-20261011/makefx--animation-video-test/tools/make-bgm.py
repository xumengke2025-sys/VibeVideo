# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy"]
# ///
"""The soundtrack for "how makefx works": 120 BPM, one bar per scene, synthesized.

Deterministic and license-free. Two layers, mixed into one file:

- **music** follows the chapters: each has its own chords and drum density, a
  riser and a fill lead into every new chapter, a crash lands on its first beat,
  and a lead melody carries the middle and the finale.
- **sound effects** come from assets/audio/cues.json (tools/extract-cues.mjs): one
  per on-screen event, on its beat, pitched to the bar's chord so the effects
  play along with the music.

    uv run tools/make-bgm.py --cues assets/audio/cues.json --out assets/audio/soundtrack.wav
"""
import argparse
import json
import wave

import numpy as np

SR = 48000
BPM = 120
BEAT = 60 / BPM  # 0.5 s
BAR = 4 * BEAT  # 2 s, one scene
BARS = 20  # 18 scenes, the finale holds three bars
rng = np.random.default_rng(120)

# One chord per bar (root MIDI for the bass, triad for everything else). Key of F.
CH = {
    "F": (41, [65, 69, 72]), "Dm": (38, [62, 65, 69]), "Bb": (46, [65, 70, 74]),
    "Gm": (43, [62, 67, 70]), "C": (48, [64, 67, 72]),
}
PROG = ["F", "Dm", "Bb", "Gm", "C", "Dm", "Bb", "C", "F", "C", "Dm", "Bb", "F", "C", "Dm", "Bb", "C", "F", "Bb", "F"]
# Chapter of each bar, from the ring: ask, price, generate, land, continue, cut, share, finale.
CHAPTER = [1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 7, 8, 8, 8]


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def env(n, attack, decay):
    t = np.arange(n) / SR
    return np.clip(t / max(attack, 1e-4), 0, 1) * np.exp(-t / decay)


def place(buf, sig, at, gain=1.0):
    i = int(round(at * SR))
    j = min(len(buf), i + len(sig))
    if 0 <= i < len(buf):
        buf[i:j] += gain * sig[: j - i]


def lp(x, cutoff):
    """One-pole low-pass; cutoff may be a scalar or a per-sample array."""
    c = np.broadcast_to(np.asarray(cutoff, dtype=float), x.shape)
    a = np.exp(-2 * np.pi * c / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc
        y[i] = acc
    return y


def hp(x, cutoff):
    return x - lp(x, cutoff)


def noise(seconds):
    return rng.standard_normal(int(seconds * SR))


def sweep(f0, f1, seconds, shape=1.0):
    n = int(seconds * SR)
    u = np.linspace(0, 1, n) ** shape
    f = f0 * (f1 / f0) ** u
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


# ---------------------------------------------------------------- instruments
def kick(strength=1.0):
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 45 + 95 * np.exp(-t / 0.035)
    return strength * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.12)


def clap(g=0.3):
    n = int(0.22 * SR)
    x = lp(hp(noise(0.22), 900), 5000)
    e = env(n, 0.001, 0.05)
    e[int(0.012 * SR):] += 0.6 * env(n - int(0.012 * SR), 0.001, 0.03)
    return g * x * e


def snare(g=0.25):
    n = int(0.18 * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 190 * t) * env(n, 0.001, 0.04)
    return g * (0.5 * body + lp(hp(noise(0.18), 1200), 7000) * env(n, 0.001, 0.06))


def hat(g):
    n = int(0.05 * SR)
    return g * hp(noise(0.05), 7000) * env(n, 0.0005, 0.012)


def crash(g=0.16):
    n = int(1.6 * SR)
    return g * hp(noise(1.6), 5000) * env(n, 0.002, 0.45)


def riser(seconds, g=0.12):
    n = int(seconds * SR)
    u = np.linspace(0, 1, n)
    x = lp(hp(noise(seconds), 400), 600 + 7000 * u**2)
    return g * x * u**1.5


def marimba(midi, vel=1.0):
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    f = hz(midi)
    return 0.16 * vel * (np.sin(2 * np.pi * f * t) * env(n, 0.002, 0.22) + 0.3 * np.sin(2 * np.pi * f * 3.93 * t) * env(n, 0.001, 0.03))


def bell(midi, g=0.10, length=1.6):
    n = int(length * SR)
    t = np.arange(n) / SR
    f = hz(midi)
    parts = [(1, 1.0, 0.9), (2.76, 0.4, 0.35), (5.4, 0.2, 0.15), (8.9, 0.1, 0.08)]
    return g * sum(a * np.sin(2 * np.pi * f * m * t) * env(n, 0.001, d) for m, a, d in parts)


def bass(midi, length, g=0.30):
    n = int(length * SR)
    t = np.arange(n) / SR
    f = hz(midi)
    saw = 2 * ((f * t) % 1) - 1
    return g * (0.6 * np.sin(2 * np.pi * f * t) + 0.25 * lp(saw, 600)) * env(n, 0.004, 0.25)


def pad(midis, length, g=0.025, cutoff=900):
    n = int(length * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for m in midis:
        for det in (-0.08, 0.08):
            s += 2 * ((hz(m + det) * t) % 1) - 1
    a = np.clip(t / 0.4, 0, 1) * np.clip((length - t) / 0.4, 0, 1)
    return g * lp(s, cutoff) * a


def lead(midi, length, g=0.075):
    """A soft plucked square with a little vibrato: the melody."""
    n = int(length * SR)
    t = np.arange(n) / SR
    f = hz(midi) * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * t) * np.clip(t / 0.15, 0, 1))
    sq = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR))
    return g * lp(sq, 2400) * env(n, 0.006, 0.35 + length * 0.4)


# --------------------------------------------------------------------- music
# The hook: (beat offset, scale step over the chord, length in beats). Steps index the
# triad upward across octaves (0 root, 1 third, 2 fifth, 3 octave...).
HOOK = [(0, 2, 0.5), (0.5, 3, 0.5), (1, 4, 1), (2, 3, 0.5), (2.5, 2, 0.5), (3, 1, 1)]
ANSWER = [(0, 4, 0.5), (0.5, 3, 0.5), (1, 2, 0.5), (1.5, 1, 0.5), (2, 2, 2)]


def step_note(triad, step):
    return triad[step % 3] + 12 * (step // 3)


def music():
    total = BARS * BAR + 2.5
    drums, tonal = np.zeros(int(total * SR)), np.zeros(int(total * SR))
    for b in range(BARS):
        t0, ch = b * BAR, CHAPTER[b]
        root, triad = CH[PROG[b]]
        first = b == 0 or CHAPTER[b - 1] != ch
        last_of_chapter = b + 1 < BARS and CHAPTER[b + 1] != ch
        finale, end = ch == 8, b == BARS - 1

        place(tonal, bell(triad[0] + 12, g=0.07), t0)  # the cut
        place(tonal, pad(triad, BAR + 0.3, g=0.03 if finale else 0.022, cutoff=1400 if finale else 900), t0)
        if first and b > 0:
            place(drums, crash(0.12 if not finale else 0.16), t0)
        if end:
            place(tonal, pad(triad, 2.4, g=0.04, cutoff=1600), t0)
            place(tonal, bell(triad[0] + 24, g=0.12, length=2.4), t0)
            place(drums, kick(1.1), t0)
            place(tonal, bass(root, 2.0), t0)
            continue

        # Arpeggio on the quarters; the sound effects carry the eighths.
        for q in range(4):
            place(tonal, marimba(step_note(triad, [0, 2, 1, 3][q] + (3 if q == 3 else 0)), 0.8 if q else 1.0), t0 + q * BEAT)

        # Melody: the hook through landing and continuing, answered in the finale.
        if ch in (4, 5) or (finale and b == 17):
            for off, st, ln in HOOK if (b % 2 == 0 or finale) else ANSWER:
                place(tonal, lead(step_note(triad, st + 3), ln * BEAT), t0 + off * BEAT)
        if finale and b == 18:
            for off, st, ln in ANSWER:
                place(tonal, lead(step_note(triad, st + 3), ln * BEAT, g=0.06), t0 + off * BEAT)

        # Drums grow with the story: sparse asking, driving generation, full landing.
        if b == 0 or finale:
            pass
        else:
            kicks = {1: [0, 2], 2: [0, 2, 2.5], 3: [0, 1, 2, 3], 4: [0, 2, 2.5], 5: [0, 2, 3.5], 6: [0, 2.5], 7: [0, 2, 3]}[ch]
            for k in kicks:
                place(drums, kick(1.0 if k == 0 else 0.75), t0 + k * BEAT)
            if ch >= 2:
                for k in (1, 3):
                    place(drums, clap(), t0 + k * BEAT)
            sub = 16 if ch == 3 else 8
            for e in range(sub):
                place(drums, hat(0.07 if e % 2 else 0.045), t0 + e * BAR / sub)
            bl = {3: [(0, 0.45), (0.5, 0.2), (1, 0.45), (1.5, 0.2), (2, 0.45), (2.5, 0.2), (3, 0.45), (3.5, 0.2)]}.get(
                ch, [(0, 0.45), (1.5, 0.2), (2, 0.45), (3.5, 0.2)])
            for at, ln in bl:
                place(tonal, bass(root + (12 if at % 1 else 0), ln), t0 + at * BEAT)

        # Into the next chapter: a riser over the last beat and a snare fill on its sixteenths.
        if last_of_chapter:
            place(drums, riser(BEAT * 1.5), t0 + BAR - BEAT * 1.5)
            if not finale and ch != 7:
                for k in range(4):
                    place(drums, snare(0.12 + 0.05 * k), t0 + 3 * BEAT + k * BEAT / 4)
    return tonal, drums


# ------------------------------------------------------------- sound effects
def chord_at(t):
    return CH[PROG[min(int(t // BAR), BARS - 1)]]


def fx_click(pitch, g=0.07):
    n = int(0.03 * SR)
    x = lp(hp(noise(0.03), 1500), 6000) * env(n, 0.0003, 0.004)
    tone = np.sin(2 * np.pi * hz(pitch) * np.arange(n) / SR) * env(n, 0.0005, 0.01)
    return g * (x + 0.6 * tone)


def fx_pop(pitch):
    s = sweep(hz(pitch) * 0.6, hz(pitch) * 1.25, 0.09, 0.5)
    return 0.16 * s * env(len(s), 0.001, 0.035)


def fx_land():
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    f = 50 + 70 * np.exp(-t / 0.02)
    thud = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.07)
    knock = lp(noise(0.3), 1800) * env(n, 0.0005, 0.018)
    return 0.42 * thud + 0.12 * knock


def fx_whoosh(seconds):
    seconds = max(seconds, 0.18)
    n = int(seconds * SR)
    u = np.linspace(0, 1, n)
    x = lp(hp(noise(seconds), 300), 500 + 5000 * np.sin(np.pi * u) ** 2)
    return 0.16 * x * np.sin(np.pi * u) ** 1.5


def fx_draw(seconds, pitch):
    seconds = max(seconds, 0.12)
    z = sweep(hz(pitch), hz(pitch) * 2, seconds, 0.7)
    n = len(z)
    u = np.linspace(0, 1, n)
    return 0.05 * z * np.sin(np.pi * u) + 0.4 * fx_whoosh(seconds)[:n]


def fx_reveal(triad):
    out = np.zeros(int(0.5 * SR))
    for k, m in enumerate([triad[0] + 24, triad[1] + 24, triad[2] + 24]):
        s = bell(m, g=0.06, length=0.4)
        place(out, s, k * BEAT / 4)
    sh = lp(hp(noise(0.5), 6000), 12000) * env(int(0.5 * SR), 0.05, 0.12)
    return out + 0.03 * sh


def fx_sparkle(triad):
    out = np.zeros(int(0.5 * SR))
    place(out, bell(triad[2] + 24, g=0.07, length=0.4), 0)
    place(out, bell(triad[0] + 36, g=0.05, length=0.4), 0.06)
    return out


def fx_stamp():
    out = 1.3 * fx_land()
    place(out, fx_click(84, 0.12), 0)
    return out


def sound_effects(cues, length):
    fx = np.zeros(length)
    tick_i = 0
    for c in cues:
        t, kind = c["t"], c["type"]
        root, triad = chord_at(t)
        if kind == "title":
            for k in range(3):
                place(fx, fx_click(96 + 2 * k, 0.03), t + k * 0.08)
        elif kind == "type":
            steps = max(2, round(c.get("dur", 0.3) / (BEAT / 4)))  # sixteenths
            for k in range(steps):
                place(fx, fx_click(88 + (k * 5) % 12, 0.05), t + k * BEAT / 4)
        elif kind == "tick":
            place(fx, fx_click(step_note(triad, 6 + tick_i % 3), 0.08), t)
            tick_i += 1
        elif kind == "pop":
            place(fx, fx_pop(step_note(triad, 6 + tick_i % 3)), t)
            tick_i += 1
        elif kind == "land":
            place(fx, fx_land(), t)
        elif kind == "whoosh":
            place(fx, fx_whoosh(c.get("dur", 0.25)), t)
        elif kind == "draw":
            place(fx, fx_draw(c.get("dur", 0.25), step_note(triad, 6)), t)
        elif kind == "reveal":
            place(fx, fx_reveal(triad), t)
        elif kind == "sparkle":
            place(fx, fx_sparkle(triad), t)
        elif kind == "stamp":
            place(fx, fx_stamp(), t)
    return fx


def reverb(x, seconds=1.1, mix=0.18):
    n = int(seconds * SR)
    ir = lp(rng.standard_normal(n) * np.exp(-np.arange(n) / SR / (seconds / 5)), 4000)
    ir /= np.sqrt(np.sum(ir**2))
    size = 1 << (len(x) + n - 1).bit_length()
    return x + mix * np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]


def write(path, mix):
    pcm = (np.clip(mix, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cues", default="assets/audio/cues.json")
    ap.add_argument("--out", default="assets/audio/soundtrack.wav")
    args = ap.parse_args()
    tonal, drums = music()
    cues = json.load(open(args.cues))["cues"]
    fx = sound_effects(cues, len(tonal))
    mix = reverb(tonal) + drums + reverb(fx, 0.6, 0.12)
    total = len(mix) / SR
    mix *= np.clip((total - np.arange(len(mix)) / SR) / 1.2, 0, 1)
    mix = np.tanh(1.3 * mix) / np.tanh(1.3)
    mix *= 0.89 / np.max(np.abs(mix))
    write(args.out, mix)
    print(f"{args.out}: {total:.1f}s, {len(cues)} sound effects")


if __name__ == "__main__":
    main()
