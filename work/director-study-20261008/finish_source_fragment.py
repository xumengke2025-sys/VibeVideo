"""Acquire a public pinned image + isolate an authored image/code action.
This is a normalized local study, never claimed as the full original MV.
"""
import urllib.request,json,pathlib,hashlib
R=pathlib.Path(__file__).parent/'source-snapshots/Lugia123';R.mkdir(exist_ok=True)
base='https://raw.githubusercontent.com/Lugia123/ai-video/1c22f4384f1ed42045666ea47f7b9b0946a9df16/'
entries=[]
for name in ['episodes/cast-cyber-girl/closeup/c3v7/k4.png','episodes/mv-pdoom/kits/comic.js','episodes/mv-pdoom/engine/palette.js','LICENSE']:
    try:
        d=urllib.request.urlopen(base+name,timeout=30).read();p=R/pathlib.Path(name).name;p.write_bytes(d);entries.append({'url':base+name,'file':str(p),'sha256':hashlib.sha256(d).hexdigest(),'bytes':len(d)});print(name,len(d),flush=True)
    except Exception as e:print('unavailable',name,str(e),flush=True)
(R/'fragment-assets.json').write_text(json.dumps(entries,indent=2),encoding='utf-8')
src=(R/'c3-v7.final.js').read_text(encoding='utf-8').splitlines()
# Exact p4 layer draw closure, with two external generic helpers rendered locally.
fragment='\n'.join(src[375:397])
fragment=fragment[fragment.index('draw: ')+6:]
fragment=fragment.removesuffix(' },') if fragment.endswith(' },') else fragment
# The original line ends "c.restore(); } },"; take only the function expression.
fragment=fragment[:fragment.rfind(' } },')+2] if ' } },' in fragment else fragment
(R/'p4-action-fragment.txt').write_text(fragment,encoding='utf-8')
