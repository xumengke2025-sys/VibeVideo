"""Restrained original test sound design; not a commissioned music score or narration."""
import math
import random
import struct
import wave
from pathlib import Path
random.seed(21)
rate=44100
with wave.open(str(Path(__file__).parent/'public'/'study-sound.wav'),'wb') as out:
    out.setnchannels(2)
    out.setsampwidth(2)
    out.setframerate(rate)
    block=bytearray()
    for n in range(rate*10):
        t=n/rate
        envelope=min(1,t/.45)*min(1,max(0,(10-t)/1.2))
        base=sum(math.sin(2*math.pi*f*t)*a for f,a in [(65.406,.055),(130.813,.025),(196,.018),(261.626,.009)])*envelope
        for at in [3,6,8.9]:
            d=t-at
            if 0<=d<1.2:
                base+=.075*math.exp(-d*5)*math.sin(2*math.pi*(180*d+22*(1-math.exp(-8*d))))
        d=t-6
        if 0<d<2.5:
            base+=random.uniform(-1,1)*.015*math.sin(math.pi*d/2.5)**2
        sample=round(max(-1,min(1,base))*32767)
        block.extend(struct.pack('<hh',sample,sample))
    out.writeframes(block)
