"""Original 80-second synthesized chamber motif and timed mechanical Foley.
Not a recording of acoustic instruments. Deterministic, editable, no remote API.
"""
from pathlib import Path
import json
import wave
import numpy as np

ROOT = Path(__file__).parent
SR = 48000
DURATION = 80
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

# Thirty composed bars: presentation, inquiry, trials, return and cadence.
# A continuous composition with changing voicings and density, not a looped sample.
progression = [(50,57,62,65),(46,58,62,65),(43,55,58,62),(45,57,61,64),
               (50,57,62,65),(48,55,60,64),(46,58,62,65),(45,57,61,64),
               (43,55,58,62),(50,57,62,65),(46,58,62,65),(45,57,61,64),
               (50,57,62,65),(43,55,58,62),(45,57,61,64),(50,57,62,65),
               (46,58,62,65),(43,55,58,62),(45,57,61,64),(50,57,62,65),
               (46,58,62,65),(48,55,60,64),(43,55,58,62),(45,57,61,64),
               (50,57,62,65),(46,58,62,65),(43,55,58,62),(45,57,61,64),
               (50,57,62,65),(38,50,57,62)]
phrases = [(74,77,76,74),(77,81,79,77),(79,77,74,70),(73,76,81,79),
           (77,74,69,74),(76,79,81,79),(77,82,81,77),(76,73,69,73)]
for bar,chord in enumerate(progression):
    origin=bar*4*BEAT
    section=0 if bar<8 else 1 if bar<12 else 2 if bar<21 else 3
    density=[.85,.74,.90,.72][section]
    add(note(chord[0],2.7,'bow'),origin,.030*density,-.13)
    pattern=[1,2,3,2,1,3,2,3] if bar%2==0 else [1,3,2,3,1,2,3,2]
    for step,degree in enumerate(pattern):
        if bar==29 and step>1:continue
        add(note(chord[degree],1.10),origin+step*BEAT/2,.047*density,-.34)
    phrase=phrases[(bar+section*2)%len(phrases)]
    for step,pitch in enumerate(phrase):
        if bar==29:continue
        # Rest in alternate phrases lets mechanical actions remain audible.
        if section==1 and step==2:continue
        pitch += -12 if bar in [10,11,24,25] else 0
        add(note(pitch,1.35),origin+step*BEAT,.043*density,.33)
    if bar>=12 and bar<21:
        add(note(chord[2]+12,2.4,'bow'),origin,.012,.16)
    if bar==29:
        for pitch in [38,50,57,62,65,74]:add(note(pitch,2.55),origin,.033,0)

def contact(when, strength=.09, label='contact'):
    t = np.arange(round(.34 * SR)) / SR
    noise = rng.standard_normal(len(t))
    click = noise * np.exp(-t*170) * .14
    body = sum(np.sin(2*np.pi*f*t)*np.exp(-t*decay)*gain
               for f, decay, gain in [(480,28,.65),(923,37,.3),(1731,48,.16)])
    add(click+body, when, strength)
    events.append({'time':when,'kind':label})

for when,strength,label in [(3.5, 0.07, 'company-card'), (5.0, 0.07, 'event-card'), (8.5, 0.06, 'evidence-arrival'), (10.2, 0.035, 'evidence-open'), (12, 0.04, 'source-1-saved'), (12.8, 0.04, 'source-2-saved'), (13.1, 0.045, 'pending-card'), (18.3, 0.04, 'guarantee-link'), (18.9, 0.04, 'group-link'), (24.5, 0.06, 'council-arrival'), (26.2, 0.035, 'expert-card'), (28.6, 0.04, 'opinion-return'), (29.1, 0.04, 'question-return'), (34.35, 0.07, 'case-arrives'), (35.45, 0.09, 'clamp-closed'), (35.65, 0.09, 'seal-contact'), (36.5, 0.04, 'trial-1-dispatch'), (37.55, 0.04, 'trial-2-dispatch'), (38.6, 0.04, 'trial-3-dispatch'), (38.7, 0.05, 'trial-1-dock'), (39.75, 0.05, 'trial-2-dock'), (40.8, 0.05, 'trial-3-dock'), (46.3, 0.055, 'pressure-change'), (47.3, 0.035, 'B-response'), (48.1, 0.035, 'C-response'), (50.5, 0.055, 'mitigation-assumption'), (59, 0.06, 'recorder-arrival'), (59.7, 0.025, 'record-line-1'), (61, 0.025, 'record-line-2'), (62.3, 0.025, 'record-line-3'), (65.7, 0.045, 'bundle-loaded'), (72, 0.055, 'return-arrival'), (73.5, 0.03, 'review-1'), (73.8, 0.03, 'review-2'), (74.1, 0.03, 'review-3'), (75.6, 0.045, 'pending-filed')]:
    contact(when,strength,label)

# A light room response, followed by one deterministic peak-safe gain.
dry = mix.copy()
for delay, amount in [(.041,.11),(.073,.07),(.113,.045)]:
    n = round(delay*SR)
    mix[n:] += dry[:-n, ::-1] * amount
timeline = np.arange(len(mix))/SR
mix *= (np.minimum(1, timeline/.45)*np.minimum(1,(DURATION-timeline)/1.1))[:,None]
peak = float(np.max(np.abs(mix)))
if peak > 0:
    mix *= .50/peak
pcm = np.int16(np.clip(mix,-1,1)*32767)
with wave.open(str(ROOT/'full-audio.wav'), 'wb') as wav:
    wav.setnchannels(2)
    wav.setsampwidth(2)
    wav.setframerate(SR)
    wav.writeframes(pcm.tobytes())
(ROOT/'qa'/'audio-events.json').write_text(json.dumps({
    'duration':DURATION,'sample_rate':SR,'original_synthesis':True,
    'auditioned':False,'events':events,'peak':float(np.max(np.abs(mix)))
},ensure_ascii=False,indent=2),encoding='utf-8')
print('Created full-audio.wav (original synthesis; listening review pending)')
