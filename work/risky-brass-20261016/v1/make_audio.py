"""Original 24-second synthesized chamber motif and timed mechanical Foley.
Not a recording of acoustic instruments. Deterministic, editable, no remote API.
"""
from pathlib import Path
import json
import wave
import numpy as np

ROOT = Path(__file__).parent
SR = 48000
DURATION = 24
BEAT = 2 / 3  # 90 BPM, nine four-beat bars
rng = np.random.default_rng(171)
mix = np.zeros((SR * DURATION, 2), dtype=np.float64)
events = []

def add(sound, when, gain=1, pan=0):
    start = round(when * SR)
    length = min(len(sound), len(mix) - start)
    if length <= 0:
        return
    stereo = np.array([np.sqrt((1-pan)/2), np.sqrt((1+pan)/2)])
    mix[start:start+length] += sound[:length, None] * stereo * gain

def note(midi, length, kind='pluck'):
    t = np.arange(round(length * SR)) / SR
    f = 440 * 2 ** ((midi - 69)/12)
    out = np.zeros_like(t)
    if kind == 'pluck':
        for h in range(1, 12):
            out += np.sin(2*np.pi*f*h*t + .03*h) / h**1.42 * np.exp(-t*(1.7+h*.34))
        env = np.minimum(1, t/.003) * np.minimum(1, (length-t)/.08)
    else:
        for h in range(1, 6):
            out += np.sin(2*np.pi*f*h*t + .006*np.sin(2*np.pi*4.3*t)) / h**2
        env = np.minimum(1, t/.15) * np.minimum(1, (length-t)/.23) * np.exp(-t*.13)
    return out * env

# D minor / G minor / A major / D minor / B flat / G minor / A / D minor / cadence.
chords = [(50,57,62,65),(43,55,58,62),(45,57,61,64),(50,57,62,65),
          (46,58,62,65),(43,55,58,62),(45,57,61,64),(50,57,62,65),(38,50,57,62)]
melody = [(74,76,77,74),(79,77,76,74),(73,76,81,79),(77,76,74,69),
          (74,77,82,81),(79,77,76,74),(73,76,81,73),(74,77,76,74),(74,69,62,62)]
for bar, (chord, phrase) in enumerate(zip(chords, melody)):
    origin = bar * 4 * BEAT
    add(note(chord[0], 2.5, 'bow'), origin, .035, -.15)
    for step, degree in enumerate([1,2,3,2,1,2,3,2]):
        if bar == 8 and step > 3:
            continue
        add(note(chord[degree], .90), origin + step * BEAT/2, .050, -.35)
    for step, pitch in enumerate(phrase):
        if bar == 8 and step > 1:
            continue
        add(note(pitch, 1.35), origin + step * BEAT, .053, .32)
    if bar == 8:
        for n in [50,57,62,65,74]:
            add(note(n, 2.3), origin, .040, 0)

def contact(when, strength=.09, label='contact'):
    t = np.arange(round(.34 * SR)) / SR
    noise = rng.standard_normal(len(t))
    click = noise * np.exp(-t*170) * .14
    body = sum(np.sin(2*np.pi*f*t)*np.exp(-t*decay)*gain
               for f, decay, gain in [(480,28,.65),(923,37,.3),(1731,48,.16)])
    add(click+body, when, strength)
    events.append({'time':when,'kind':label})

for when, strength, label in [(2.35,.07,'case-arrives'),(3.45,.10,'clamp-closed'),
                              (3.65,.09,'seal-contact'),(4.50,.045,'trial-1'),
                              (5.55,.045,'trial-2'),(6.60,.045,'trial-3'),
                              (6.7,.055,'trial-1-dock'),(7.75,.055,'trial-2-dock'),
                              (8.8,.055,'trial-3-dock'),(14.3,.06,'pressure-change'),
                              (15.3,.035,'B-response'),(16.1,.035,'C-response'),
                              (18.5,.055,'mitigation-assumption')]:
    contact(when,strength,label)

# A light room response, followed by one deterministic peak-safe gain.
dry = mix.copy()
for delay, amount in [(.041,.11),(.073,.07),(.113,.045)]:
    n = round(delay*SR)
    mix[n:] += dry[:-n, ::-1] * amount
timeline = np.arange(len(mix))/SR
mix *= (np.minimum(1, timeline/.45)*np.minimum(1,(DURATION-timeline)/1.1))[:,None]
peak = float(np.max(np.abs(mix)))
if peak > .65:
    mix *= .65/peak
pcm = np.int16(np.clip(mix,-1,1)*32767)
with wave.open(str(ROOT/'sample-audio.wav'), 'wb') as wav:
    wav.setnchannels(2)
    wav.setsampwidth(2)
    wav.setframerate(SR)
    wav.writeframes(pcm.tobytes())
(ROOT/'qa'/'audio-events.json').write_text(json.dumps({
    'duration':DURATION,'sample_rate':SR,'original_synthesis':True,
    'auditioned':False,'events':events,'peak':float(np.max(np.abs(mix)))
},ensure_ascii=False,indent=2),encoding='utf-8')
print('Created sample-audio.wav (original synthesis; listening review pending)')
