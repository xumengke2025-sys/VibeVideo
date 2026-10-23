"""Restartable bounded-memory asset processing; one material per child process."""
from pathlib import Path
import json,sys,subprocess
R=Path(__file__).resolve().parent;Q=R/'qa/v21'
for kind,ids in [('scene',range(20)),('bridge',range(1,19))]:
    for i in ids:
        expected=(41 if i==0 else 25 if i==18 else 32 if i==19 else 33) if kind=='scene' else 17
        p=Q/f'{kind}-{i:02d}.json'
        if p.exists() and json.loads(p.read_text())['output_frames']==expected:
            print(f'{kind} {i}: existing completed asset',flush=True);continue
        with (Q/f'{kind}-{i:02d}-build.log').open('w') as log:
            proc=subprocess.run([sys.executable,'-u','build_motion_v21.py','--'+kind+'s',str(i)],cwd=R,stdout=log,stderr=subprocess.STDOUT,timeout=600)
        if proc.returncode:raise RuntimeError(f'{kind} {i}: see build log')
        print(f'{kind} {i}: completed',flush=True)
# Refresh full manifest even when every individual material was already ready.
subprocess.run([sys.executable,'build_motion_v21.py'],cwd=R,check=True,timeout=30)
print('All 39 assets completed; handover bridge retained.',flush=True)
