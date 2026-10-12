"""Original deterministic electronic ambience and timed sound events, no external audio."""
import math, wave, array, random
from pathlib import Path
RATE=48000; DURATION=32; random.seed(62136)
N=RATE*DURATION
left=array.array('f',[0.0])*N;right=array.array('f',[0.0])*N
def add_note(start,duration,freq,gain,pan=.5,kind='pad'):
    begin=int(start*RATE);end=min(N,int((start+duration)*RATE))
    pl=math.cos(pan*math.pi/2);pr=math.sin(pan*math.pi/2)
    for i in range(begin,end):
        t=(i-begin)/RATE
        if kind=='pad':
            env=min(1,t/1.8)*min(1,max(0,(duration-t)/2.4))
            s=math.sin(2*math.pi*freq*t+.15*math.sin(2*math.pi*.11*t))+.24*math.sin(2*math.pi*freq*2.003*t)+.1*math.sin(2*math.pi*freq*3.999*t)
            s*=env*(.85+.15*math.sin(2*math.pi*.13*t))
        else:
            env=(1-math.exp(-t*90))*math.exp(-t*(1.4 if kind=='bell' else 3.0))
            s=(math.sin(2*math.pi*freq*t+1.7*math.sin(2*math.pi*freq*2.01*t)*math.exp(-t*3))+.25*math.sin(2*math.pi*freq*3.98*t))*env
        value=s*gain
        left[i]+=value*pl;right[i]+=value*pr
for start,dur,frequencies in [(0,18,[73.416,146.832,220.,293.665,329.628]),(13.5,12,[58.27,116.541,174.614,220,261.626,349.228]),(23,9,[73.416,146.832,220,293.665,440])]:
    for j,f in enumerate(frequencies):add_note(start,dur,f,.035 if j>0 else .046,(j+.5)/len(frequencies))
events=[(0.35,587.33),(4.25,440),(8.5,659.25),(9.7,783.99),(11.1,880),(12.7,1174.66),(15.25,587.33),(20.2,440),(23,523.25),(26.3,587.33)]
for j,(t,f) in enumerate(events):add_note(t,3.2,f,.065,.3+.4*(j%2),'bell')
for k in range(22):
    t=15.5+k*.5
    add_note(t,.9,[146.83,220,293.66,329.63,440,293.66,220,329.63][k%8],.027,.25+.5*(k%3)/2,'pluck')
    if k%4==0:
        for i in range(int(t*RATE),min(N,int((t+.35)*RATE))):
            x=(i-int(t*RATE))/RATE;s=math.sin(2*math.pi*(49*x+27*.055*(1-math.exp(-x/.055))))*math.exp(-x*15)*.055
            left[i]+=s;right[i]+=s
# Modest deterministic stereo reflections, then fade at the film's settled ending.
for delay,gain in [(.137,.12),(.233,.11),(.389,.09),(.617,.06)]:
    d=int(delay*RATE)
    for i in range(d,N):
        left[i]+=right[i-d]*gain;right[i]+=left[i-d]*gain
peak=max(max(abs(x) for x in left),max(abs(x) for x in right));scale=.68/max(peak,.001)
pcm=array.array('h')
for i in range(N):
    t=i/RATE;env=min(1,t/.15)*min(1,max(0,(32-t)/2.3));pcm.extend((int(left[i]*scale*env*32767),int(right[i]*scale*env*32767)))
out=Path(__file__).parent/'soundtrack.wav'
with wave.open(str(out),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(RATE);f.writeframes(pcm.tobytes())
print(f'{out}: {DURATION}s, stereo, {RATE}Hz; original synthesized electronic ambience; peak target 0.68')
