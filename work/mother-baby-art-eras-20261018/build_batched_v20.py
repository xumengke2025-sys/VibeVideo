from pathlib import Path
import subprocess,sys,time,json,argparse
R=Path(__file__).resolve().parent
log=R/'out/build-v20.log'
p=argparse.ArgumentParser()
p.add_argument('--scene-start',type=int,default=0)
p.add_argument('--bridge-start',type=int,default=1)
args=p.parse_args()
with log.open('a',encoding='utf8') as f:
    for flag,ids in [('--only',range(args.scene_start,20)),('--bridges',range(args.bridge_start,20))]:
        for i in ids:
            started=time.monotonic();p=subprocess.run([sys.executable,str(R/'build_cushions_v20.py'),flag,str(i)],cwd=R,stdout=f,stderr=subprocess.STDOUT)
            entry={'stage':flag,'id':i,'seconds':round(time.monotonic()-started,2),'exit':p.returncode};print(json.dumps(entry),flush=True);f.write(json.dumps(entry)+'\n');f.flush()
            if p.returncode:raise SystemExit(p.returncode)
