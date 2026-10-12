"""Original synthesized sound bed and lens-contact chimes; no downloaded audio or model API."""
import math, wave, array
from pathlib import Path
SR=48000;DUR=16;TAU=math.tau
def arrival(z):
    lo,hi=0.,1.
    for _ in range(40):
        u=(lo+hi)/2
        if u*u*(3-2*u)<(8-z)/18: lo=u
        else: hi=u
    return 1+7.2*(lo+hi)/2
events=list(zip([arrival(z) for z in [6,2,-2,-6,-10]],[293.665,349.228,440,587.33,698.456]))
events += [(9.2,880),(10.4,1174.66),(13.6,440)]
channels=[array.array('f'),array.array('f')]
for i in range(SR*DUR):
    t=i/SR;fade=min(1,t/1.4,(DUR-t)/1.4)
    pulse=.75+.25*math.sin(TAU*.4*t)
    for c in (0,1):
        pad=sum(math.sin(TAU*f*(1+c*.0009)*t+.12*k)*a for k,(f,a) in enumerate([(73.416,.03),(146.832,.02),(220,.012),(293.664,.008)]))*pulse
        val=pad
        for at,f in events:
            dt=t-at
            if 0<=dt<2.7:
                env=min(1,dt/.015)*math.exp(-3.2*dt)
                val+=env*(math.sin(TAU*f*dt)*.095+math.sin(TAU*f*2.003*dt)*.024+math.sin(TAU*f*3.99*dt)*.009)*(1 if c==0 else .82)
                echo=dt-.18
                if echo>0:val+=math.sin(TAU*f*echo)*.012*math.exp(-3.4*echo)
        channels[c].append(val*max(0,fade))
peak=max(max(abs(v) for v in ch) for ch in channels);gain=.68/peak
pcm=array.array('h')
for a,b in zip(*channels):pcm.extend((int(max(-1,min(1,a*gain))*32767),int(max(-1,min(1,b*gain))*32767)))
out=Path(__file__).parent/'score.wav'
with wave.open(str(out),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
print(f'{out} | 48000Hz stereo | {DUR}s | peak 0.68 | lens cues {[(round(a,3),f) for a,f in events[:5]]}')
