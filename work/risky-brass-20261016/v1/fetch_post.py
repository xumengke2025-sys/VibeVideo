import pathlib,urllib.request,re,posixpath
R=pathlib.Path(__file__).resolve().parent/'vendor'
seen=set()
def pull(name):
    name=posixpath.normpath(name)
    if name in seen:return
    seen.add(name); target=R/name;target.parent.mkdir(exist_ok=True,parents=True)
    if not target.exists():
        with urllib.request.urlopen('https://unpkg.com/three@0.186.0/examples/jsm/'+name,timeout=35) as response: target.write_bytes(response.read())
    text=target.read_text(encoding='utf-8')
    for dep in re.findall(r"from\s+['\"]([^'\"]+)['\"]",text):
        if dep.startswith('.'):pull(posixpath.join(posixpath.dirname(name),dep))
    print(name,flush=True)
for name in ['postprocessing/EffectComposer.js','postprocessing/RenderPass.js','postprocessing/SSAOPass.js','postprocessing/OutputPass.js']:pull(name)
