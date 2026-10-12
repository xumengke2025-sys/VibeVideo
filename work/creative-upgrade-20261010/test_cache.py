"""Renderer cache regression; uses a tiny engineering fixture, no visual judgement."""
import hashlib,json,subprocess,shutil
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE/'other-regression/cache-fixture'
ROOT.mkdir(parents=True,exist_ok=True)
RENDER=BASE/'other-regression/cache-render.mjs'
shutil.copy2(BASE/'render.mjs',RENDER)
(ROOT/'package.json').write_text('{"type":"module"}',encoding='utf-8')
(ROOT/'data.json').write_text('{"label":"fixture"}',encoding='utf-8')
(ROOT/'palette.mjs').write_text('export const color="#197ca5";',encoding='utf-8')
(ROOT/'index.html').write_text('''<!doctype html><html><body><script type="module">
import {color} from './palette.mjs';
const c=document.createElement('canvas');c.width=64;c.height=96;document.body.append(c);
window.__film={duration:.25,fps:24,width:64,height:96,cuts:[]};
window.renderAt=(t,type='image/png',q=.96)=>{const g=c.getContext('2d');g.fillStyle=color;g.fillRect(0,0,64,96);g.fillStyle='#fff';g.fillRect(5+80*t,40,10,10);return c.toDataURL(type,q);};window.ready=true;
</script></body></html>''',encoding='utf-8')
OUT=ROOT/'out-cache'
cmd=['D:/docker/node.exe',str(RENDER),'--project='+str(ROOT),'--out='+str(OUT),'--name=cache.mp4','--stills=.1','--playwright=C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core/index.js','--three=D:/ai项目/ai动画/node_modules/three','--ffmpeg=D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe']
cases=[]
def invoke(name,args=cmd,reject=False):
    r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',timeout=180)
    okay=(r.returncode!=0 and 'Frame configuration changed' in r.stderr) if reject else r.returncode==0
    cases.append({'name':name,'exit_code':r.returncode,'expected_reject':reject,'pass':okay,'stdout':r.stdout[-500:],'stderr':r.stderr[-700:]})
    if not okay:raise AssertionError(cases[-1])
def hashes():
    return {p.relative_to(OUT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.rglob('*') if p.is_file() and (p.suffix in ('.png','.jpg','.mp4') or p.name=='frame-config.json')}
invoke('baseline')
initial=hashes()
invoke('unchanged-cache-reuse')
assert hashes()==initial
palette=ROOT/'palette.mjs';original=palette.read_text(encoding='utf-8')
palette.write_text('export const color="#aa3344";',encoding='utf-8');invoke('import-module-change',reject=True);assert hashes()==initial;palette.write_text(original,encoding='utf-8')
data=ROOT/'data.json';original=data.read_text(encoding='utf-8')
data.write_text('{"label":"changed"}',encoding='utf-8');invoke('event-json-change',reject=True);assert hashes()==initial;data.write_text(original,encoding='utf-8')
original=RENDER.read_text(encoding='utf-8');RENDER.write_text(original+'\n// cache identity test\n',encoding='utf-8');invoke('renderer-change',reject=True);assert hashes()==initial;RENDER.write_text(original,encoding='utf-8')
invoke('preview-scale-change',[*cmd,'--scale=.5'],reject=True);assert hashes()==initial
manifest=OUT/'frame-config.json';original=manifest.read_text(encoding='utf-8');value=json.loads(original);value['toolchain']['browser']='different-version';manifest.write_text(json.dumps(value),encoding='utf-8');invoke('toolchain-mismatch',reject=True);manifest.write_text(original,encoding='utf-8');assert hashes()==initial
(BASE/'other-regression/cache-test-results.json').write_text(json.dumps({'cases':cases,'cached_outputs_unchanged_on_rejection':True,'baseline_hashes':initial,'scope':'Engineering cache regression only; no aesthetic review.'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':len(cases),'video':str(OUT/'cache.mp4'),'scope':'engineering fixture'},ensure_ascii=False))
