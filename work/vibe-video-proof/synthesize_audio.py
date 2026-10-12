"""Original restrained audio cues for the 12s analytical motion study."""
from array import array
from math import sin, pi, exp, tanh
from pathlib import Path
import random
import sys
import wave

rate = 48000
duration = 12
audio = [0.0] * (rate * duration)
rng = random.Random(731)

def tone(start, length, frequency, gain, glide=0):
    phase = 0.0
    for n in range(int(length * rate)):
        k = int(start * rate) + n
        if k >= len(audio):
            break
        t = n / rate
        envelope = min(1, t / 0.025) * exp(-t * 3.5 / length)
        envelope *= min(1, max(0, (length - t) / 0.1))
        phase += 2 * pi * (frequency + glide * exp(-t * 10)) / rate
        audio[k] += gain * envelope * (sin(phase) + 0.18 * sin(2 * phase))

# Quiet harmonic foundation; no external recordings or media provider.
for frequency in [130.8128, 195.9977, 261.6256]:
    for n in range(len(audio)):
        t = n / rate
        fade = min(1, t / 1.4) * min(1, max(0, (duration - t) / 1.4))
        audio[n] += 0.022 * fade * sin(2 * pi * frequency * t + 0.17 * sin(t * 0.5))

for start in [0.2, 3.2, 6.5, 9.4]:
    tone(start, 1.1, 58, 0.21, 85)
    tone(start + 0.025, 0.8, 392, 0.05)
for start, f in [(0.7, 523.25), (1.45, 587.33), (2.2, 659.25), (3.6, 783.99), (4.35, 659.25), (5.1, 587.33), (6.9, 523.25), (7.65, 659.25), (8.4, 783.99), (9.45, 1046.5)]:
    tone(start, 0.9, f, 0.055)
for start in [2.65, 5.95, 8.85]:
    for n in range(int(0.7 * rate)):
        k = int(start * rate) + n
        if k >= len(audio):
            break
        t = n / rate / 0.7
        audio[k] += 0.014 * sin(pi * t) ** 2 * rng.uniform(-1, 1)

peak = max(abs(v) for v in audio)
pcm = array('h', (int(tanh(v) / max(1, peak) * 27000) for v in audio))
if sys.byteorder != 'little':
    pcm.byteswap()
target = Path(__file__).parent / 'public' / 'proof-score.wav'
target.parent.mkdir(parents=True, exist_ok=True)
with wave.open(str(target), 'wb') as stream:
    stream.setnchannels(1)
    stream.setsampwidth(2)
    stream.setframerate(rate)
    stream.writeframes(pcm.tobytes())
print(target)
