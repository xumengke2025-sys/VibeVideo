import importlib.util
import json
from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parent
script=Path('D:/Codex/skills/vibe-video/scripts/opus_gallery.py')
raw=json.loads((root.parents[1]/'reference-sources/awesome-opus5-5-videos-20261009/data/videos.json').read_text(encoding='utf-8'))
packed=json.loads(script.parents[1].joinpath('assets/opus-gallery.json').read_text(encoding='utf-8'))
assert packed['entries']==raw
assert len(raw)==513
slugs={x['slug'] for x in raw}
prompt_slugs={x.stem for x in (root.parents[1]/'reference-sources/awesome-opus5-5-videos-20261009/prompts').glob('*.md')}
assert slugs==prompt_slugs
by_slug={x['slug']:x for x in raw}

def run(*args):
    result=subprocess.run([sys.executable,str(script),*args],capture_output=True,text=True,encoding='utf-8',check=True)
    return json.loads(result.stdout)

stats=run('stats')
assert stats['partial_prompts']==234
assert stats['categories']=={'motion':317,'explainer':67,'interactive':70,'3d':59}
for query in [
    ['--category','explainer','--query','photon','--limit','3'],
    ['--mechanism','continuity','--complete','--limit','5'],
    ['--tag','svg','--tag','gsap','--limit','4'],
]:
    data=run('search',*query)
    assert 0<len(data['results'])<=int(query[-1])
    for result in data['results']:
        source=by_slug[result['slug']]
        if '--complete' in query:assert not source['prompt_partial']
        if '--category' in query:assert source['category']=='explainer' and 'photon' in source['prompt'].lower()
        if '--tag' in query:assert {'svg','gsap'}.issubset(source['tech_tags'])
        assert result['remake_tech_tags']==source['tech_tags']
        assert packed['provenance']['commit'] in result['prompt_file']

result=run('search','--slug','twoclipping-402193','--prompt')['results'][0]
assert result['prompt']==by_slug['twoclipping-402193']['prompt']
assert run('search','--query','nonexistent-fdf7c2-unique')['matches']==0
assert run('search','--slug','voxyz-ai-345550')['results'][0]['prompt_partial'] is True
assert run('search','--slug','voxyz-ai-345550','--complete')['matches']==0

roundtrip=root/'verification-catalog.json'
run('import',str(root.parents[1]/'reference-sources/awesome-opus5-5-videos-20261009/data/videos.json'),'--out',str(roundtrip),'--commit',packed['provenance']['commit'],'--checked','2026-10-09')
assert json.loads(roundtrip.read_text(encoding='utf-8'))==packed
spec=importlib.util.spec_from_file_location('gallery',script);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
try:module.validate(raw+[raw[0]])
except ValueError:pass
else:raise AssertionError('Duplicate slug was accepted')

report={'status':'passed','entries_preserved':len(raw),'all_prompt_files_correspond':True,'checked':['full data fidelity','bounded category/query/AND tag search','partial/full filtering','single prompt equality','pinned source URLs','import roundtrip','duplicate slug rejection']}
(root/'gallery-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
