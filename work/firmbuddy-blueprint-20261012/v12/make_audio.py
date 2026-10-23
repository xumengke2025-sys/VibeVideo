"""Retain the approved score, add quiet cues for business material handoffs."""
from pathlib import Path
import json,wave,hashlib
import numpy as np
R=Path(__file__).resolve().parent
SR=48000
with wave.open(str(R/'audio/base-v11.wav'),'rb') as w:
    a=np.frombuffer(w.readframes(w.getnframes()),'<i2').reshape(-1,2).astype(np.float32)/32768
events=[]
for t,note,kind in [(15,74,'announcement-merge'),(15.2,77,'shareholder-merge'),(15.4,81,'client-dossier-ready'),(39.1,74,'visit-material-assembled'),(39.35,77,'talking-points-assembled'),(39.6,81,'followup-plan-assembled'),(40.2,86,'preparation-output')]:
    z=np.arange(int(.28*SR))/SR;f=440*2**((note-69)/12)
    s=(np.sin(2*np.pi*f*z)+.16*np.sin(4*np.pi*f*z))*np.exp(-z*20)*(1-np.exp(-z/.002))*.035
    k=round(t*SR);a[k:k+len(s)]+=s[:,None]
    events.append(dict(time=t,sample=k,kind=kind))
assert np.max(np.abs(a))<.99
with wave.open(str(R/'audio/mix.wav'),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.rint(a*32767).astype('<i2').tobytes())
timing=json.loads((R/'audio/base-v11-timing.json').read_text(encoding='utf-8'))
timing.update(revision='V12',business_action_cues=events,actual_listening=False,mix_sha256=hashlib.sha256((R/'audio/mix.wav').read_bytes()).hexdigest())
(R/'audio/timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(duration=60,peak=float(np.max(np.abs(a))),new_events=len(events))))
