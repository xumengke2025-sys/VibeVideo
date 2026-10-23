"""Fetch public CC0 surfaces and version-matched Three.js helper, retaining provenance."""
import json, pathlib, urllib.request, hashlib
R=pathlib.Path(__file__).resolve().parent
def get(url,path):
    if not path.exists():
        req=urllib.request.Request(url,headers={'User-Agent':'Risky instrument animation / local production'})
        with urllib.request.urlopen(req,timeout=50) as response: path.write_bytes(response.read())
    return {'url':url,'file':str(path.relative_to(R)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
assets=[]
for name,fields in [('brown_photostudio_02',['hdri']),('dark_wood',['Diffuse','nor_gl','Rough'])]:
    d=json.loads((R/'assets'/('polyhaven-'+name+'.json')).read_text())
    for key in fields:
        data=d[key]['1k']['hdr' if key=='hdri' else 'jpg']
        item=get(data['url'],R/'assets'/data['url'].split('/')[-1]); item.update(authority='Poly Haven',license='CC0',source='https://polyhaven.com/a/'+name)
        assets.append(item); print(item['file'],flush=True)
for name in ['HDRLoader.js']:
    item=get('https://unpkg.com/three@0.186.0/examples/jsm/loaders/'+name,R/'vendor'/name); item.update(license='MIT',authority='Three.js r186');assets.append(item)
get('https://unpkg.com/three@0.186.0/LICENSE',R/'vendor'/'LICENSE-Three.txt')
(R/'assets'/'provenance.json').write_text(json.dumps(assets,indent=2),encoding='utf-8')
