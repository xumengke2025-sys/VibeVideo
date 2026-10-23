"""Original 40-second family miniature; editable score and licensed instruments."""
from pathlib import Path
import sys, json, wave, struct, hashlib
import numpy as np
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'.tools/python-libs'))
from tinysoundfont import Synth
O=R/'assets/audio-v21';O.mkdir(exist_ok=True)
SR=48000;N=SR*40;BEAT=.5;BAR=2;notes=[];events=[]
def note(t,d,ch,p,v):
    if t>=39:return
    notes.append([round(t,4),round(d,4),ch,p,v])
    events.extend([(round(t*SR),False,ch,p,v),(min(N,round((t+d)*SR)),True,ch,p,0)])
# F major. The harmony spans eras in four-bar phrases, with a final tonic at 38s.
chords=[(41,[57,60,64]),(40,[55,60,64]),(38,[57,60,65]),(34,[53,57,62]),
        (43,[55,58,62]),(36,[55,58,64]),(41,[57,60,65]),(36,[55,60,64]),
        (38,[57,60,65]),(45,[55,60,64]),(34,[53,57,60]),(36,[55,58,64]),
        (41,[57,60,65]),(40,[55,60,64]),(38,[57,60,65]),(34,[53,57,62]),
        (43,[55,58,62]),(36,[55,58,64]),(36,[55,58,64]),(41,[57,60,65])]
# (beat offset, MIDI pitch, duration in beats): a new four-bar call and answer.
melodies=[[(0,72,1),(1,77,.5),(1.5,76,.5),(2,72,1),(3,69,.75)],
 [(0,67,1),(1.25,72,.5),(2,76,1),(3,74,.75)],
 [(0,77,1.5),(1.5,76,.5),(2,74,1),(3,72,.75)],
 [(0,69,1),(1,70,.5),(1.5,72,.5),(2,74,1.5)],
 [(0,74,1),(1,77,.75),(2,79,1),(3,77,.75)],
 [(0,76,1.5),(1.5,74,.5),(2,72,1.75)],
 [(0,69,1),(1,72,1),(2,77,1.75)],
 [(0,76,1),(1,74,1),(2,72,1.5)],
 [(0,77,.75),(1,76,.75),(2,74,1.5)],
 [(0,72,1.5),(1.5,69,.5),(2,67,1.75)],
 [(0,65,1),(1,69,.75),(2,72,1),(3,74,.75)],
 [(0,76,1),(1,74,.75),(2,72,1.5)],
 [(0,72,1),(1,77,.5),(1.5,76,.5),(2,72,1),(3,69,.75)],
 [(0,67,1),(1.25,72,.5),(2,76,1),(3,79,.75)],
 [(0,81,1.5),(1.5,79,.5),(2,77,1.75)],
 [(0,74,1),(1,72,1),(2,69,1.5)],
 [(0,70,1),(1,74,1),(2,77,1.75)],
 [(0,76,1),(1,74,1),(2,72,1.5)],
 [(0,70,.75),(1,69,.75),(2,67,1.5)],
 [(0,77,2.6)]]
for b,(bass,chord) in enumerate(chords):
    t=b*BAR;ending=b==19;vel=43 if b<4 else 47 if b<12 else 50
    note(t,1.65 if not ending else 1.2,3,bass,vel)
    for k,p in enumerate(chord):note(t+k*.023,1.72 if not ending else 1.3,0,p,vel-6)
    if not ending:
        for j in range(8):
            p=chord[[0,1,2,1,0,1,2,1][j]]+(12 if j==6 and b%4==2 else 0)
            note(t+j*.25,.34,2,p,vel-4+(3 if j%4==0 else -2))
        if 4<=b<=17:
            for j in [1,3]:note(t+j*.5,.22,4,chord[j%3],32)
    for off,p,d in melodies[b]:note(t+off*BEAT,d*BEAT*.95,1,p,55+(3 if off==0 else 0))
    # Sparse sparkle at phrase openings; never a heavy accent at every cut.
    if b in [4,8,12,16]:note(t+.04,1.0,5,84 if b%8==4 else 81,27)
programs={0:0,1:8,2:24,3:32,4:45,5:10}
s=Synth(gain=-9,samplerate=SR);sf=s.sfload((O/'GeneralUser-GS.sf2').read_bytes(),max_voices=96)
for ch,p in programs.items():s.program_select(ch,sf,0,p)
for ch,pan in [(0,48),(1,68),(2,83),(3,64),(4,38),(5,56)]:s.control_change(ch,10,pan)
audio=np.zeros((N,2),np.float32);cursor=0
for at,off,ch,p,v in sorted(events,key=lambda e:(e[0],not e[1])):
    if at>cursor:audio[cursor:at]=np.frombuffer(s.generate(at-cursor),np.float32).reshape(-1,2);cursor=at
    if off:s.noteoff(ch,p)
    else:s.noteon(ch,p,v)
if cursor<N:audio[cursor:]=np.frombuffer(s.generate(N-cursor),np.float32).reshape(-1,2)
dry=audio.copy()
for delay,gain in [(.067,.10),(.113,.085),(.197,.055),(.311,.035),(.439,.02)]:
    n=round(delay*SR);audio[n:]+=dry[:-n,::-1]*gain
t=np.arange(N)/SR;audio*=np.interp(t,[0,.32,37.9,38.7,40],[0,1,1,.85,0])[:,None]
rms=float(np.sqrt(np.mean(audio**2)));peak=float(np.abs(audio).max());gain=min(.13/max(rms,1e-9),.82/max(peak,1e-9));audio*=gain
with wave.open(str(O/'warm-family-40s.wav'),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(audio,-1,1)*32767).astype('<i2').tobytes())
def vlq(n):
    b=[n&127];n>>=7
    while n:b.insert(0,(n&127)|128);n>>=7
    return bytes(b)
ev=[(0,b'\xff\x51\x03\x07\xa1\x20'),(0,b'\xff\x58\x04\x04\x02\x18\x08')]
for ch,p in programs.items():ev.append((0,bytes([0xc0+ch,p])))
for at,d,ch,p,v in notes:ev.extend([(round(at/BEAT*480),bytes([0x90+ch,p,v])),(round((at+d)/BEAT*480),bytes([0x80+ch,p,0]))])
data=b'';last=0
for tick,msg in sorted(ev,key=lambda e:e[0]):data+=vlq(tick-last)+msg;last=tick
data+=b'\x00\xff\x2f\x00';(O/'warm-family.mid').write_bytes(b'MThd'+struct.pack('>IHHH',6,0,1,480)+b'MTrk'+struct.pack('>I',len(data))+data)
report={'duration':40,'sample_rate':SR,'channels':2,'tempo':120,'meter':'4/4','key':'F major','notes':notes,'programs':programs,'composition':'New original family miniature; piano, celesta, nylon guitar, acoustic bass, pizzicato','instrument_license':'LICENSE-GeneralUser.txt','rms_dbfs':round(20*np.log10(np.sqrt(np.mean(audio**2))),2),'peak_dbfs':round(20*np.log10(np.abs(audio).max()),2),'clipped_samples':int(np.count_nonzero(np.abs(audio)>=1)),'actual_listening':False,'listening_limitation':'No enabled audio-perception tool; waveform and mux checks do not establish listening','wav_sha256':hashlib.sha256((O/'warm-family-40s.wav').read_bytes()).hexdigest()}
(O/'score.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=float),encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k!='notes'},ensure_ascii=True,default=float))
