from pathlib import Path
import subprocess,shutil,json,hashlib,time,os
R=Path(__file__).resolve().parent
T=R/'out/source-runtime-v19'
logs=[]
env=os.environ.copy()
cached=R/'node_modules/.remotion/chrome-headless-shell/win64/chrome-headless-shell-win64/chrome-headless-shell.exe'
if cached.exists():env['CHROME_EXECUTABLE']=str(cached)
for mode in ['check','transitioncheck']:
    start=time.monotonic()
    p=subprocess.run([shutil.which('node'),'render-v19.mjs',mode],cwd=T,env=env,capture_output=True,text=True,timeout=180,creationflags=subprocess.CREATE_NO_WINDOW)
    (R/f'qa/v19/source-runtime-{mode}.log').write_text(p.stdout+p.stderr,encoding='utf8')
    if p.returncode:raise RuntimeError(f'Extracted source {mode}: {p.returncode}')
    logs.append({'command':f'node render-v19.mjs {mode}','exit':p.returncode,'seconds':round(time.monotonic()-start,2)})
m=json.loads((T/'SOURCE-PACKAGE.json').read_text());check=json.loads((T/'qa/v19/mechanical-check.json').read_text());trans=json.loads((T/'qa/v19/transition-check.json').read_text())
assert check['era_count']==20 and check['frames']==960 and not check['issues'] and check['pixel_determinism']
assert len(check['continuity']['endpoints'])==19 and not check['continuity']['issues']
assert trans['cuts']==19 and not trans['issues'] and trans['transition_seek_determinism']
names=[n for n in m['sha256'] if n.startswith(('film/','assets/')) or n.endswith('.mjs') or n=='package.json']
for n in names:
    assert hashlib.sha256((R/n).read_bytes()).hexdigest()==m['sha256'][n],n
    assert hashlib.sha256((T/n).read_bytes()).hexdigest()==m['sha256'][n],n
report={'version':19,'extracted_runtime':'out/source-runtime-v19','commands':logs,'era_count':20,'frames':960,'runtime_assets':m['runtime_assets'],'runtime_files_matched':len(names),'actor_connections':19,'room_transitions':19,'issues':0,'pixel_determinism':True,'source_and_extracted_runtime_hashes_match':True,'dependencies':'Reused existing project Node modules and cached Chromium; no clean-machine installation test','scope':'Source runtime, dimensions, endpoint pixels and random access; no new independent or whole-film aesthetic review'}
(R/'qa/v19/source-runtime-check.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report))
