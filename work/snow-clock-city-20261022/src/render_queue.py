"""Serialize project Blender jobs on the single 8 GB GPU.
Usage: python src/render_queue.py --log render/name.log -- blender.exe ...
"""
import os,sys,time,json,argparse,subprocess,ctypes
from pathlib import Path
R=Path(__file__).resolve().parents[1];LOCK=R/'render/.gpu-job.lock'
parser=argparse.ArgumentParser();parser.add_argument('--log',required=True);parser.add_argument('command',nargs=argparse.REMAINDER);args=parser.parse_args()
cmd=args.command[1:] if args.command[:1]==['--'] else args.command
if not cmd:raise SystemExit('Missing child command')
LOCK.parent.mkdir(exist_ok=True)
def alive(pid):
    if os.name=='nt':
        kernel=ctypes.windll.kernel32;handle=kernel.OpenProcess(0x100000,False,pid)
        if not handle:return False
        running=kernel.WaitForSingleObject(handle,0)==258;kernel.CloseHandle(handle);return running
    try:os.kill(pid,0);return True
    except OSError:return False
last=0
while True:
    try:
        with LOCK.open('x',encoding='utf8') as f:json.dump({'pid':os.getpid(),'started':time.time(),'log':args.log},f)
        break
    except FileExistsError:
        try:
            owner=json.loads(LOCK.read_text())
            if not alive(owner['pid']):LOCK.unlink();continue
        except (ValueError,KeyError,OSError):pass
        if time.monotonic()-last>30:print('Waiting for project GPU queue',flush=True);last=time.monotonic()
        time.sleep(3)
try:
    # This workstation also hosts other independent film jobs. Do not stop them
    # or launch an 8 GB scene while another Blender is holding the machine.
    if os.name=='nt':
        last=0
        while True:
            inventory=subprocess.run(['tasklist','/FI','IMAGENAME eq blender.exe','/FO','CSV','/NH'],capture_output=True,text=True,encoding='oem',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW).stdout
            if 'blender.exe' not in inventory.lower():break
            if time.monotonic()-last>30:print('Waiting for existing Blender process on this workstation',flush=True);last=time.monotonic()
            time.sleep(5)
    logfile=R/args.log;logfile.parent.mkdir(parents=True,exist_ok=True)
    with logfile.open('w',encoding='utf8') as out:
        child=subprocess.Popen(cmd,cwd=R,stdout=out,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        print('Blender started; log:',logfile,flush=True)
        code=child.wait()
    print('Blender finished:',code,flush=True)
finally:
    try:
        if json.loads(LOCK.read_text())['pid']==os.getpid():LOCK.unlink()
    except (OSError,ValueError):pass
raise SystemExit(code)
