import urllib.request,pathlib,json,hashlib
ROOT=pathlib.Path(__file__).parent
items=[('Liamrjohnston','examples/openmontage-claude-pipeline.mp4'),('Liamrjohnston','examples/openmontage-hook.mp4'),('Liamrjohnston','examples/openmontage-tool-chaos.mp4'),('Liamrjohnston','docs/prompt-threads.md'),('Lugia123','episodes/ep03-paired-estimate/index.html'),('Lugia123','README.md')]
records=[]
for author,remote in items:
    source=json.loads((ROOT/'source-snapshots'/author/'repo.json').read_text(encoding='utf-8'))
    url=f'https://raw.githubusercontent.com/{source["repo"]}/{source["commit"]["sha"]}/{remote}'
    dest=ROOT/'source-snapshots'/author/remote;dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Codex-public-reference-study'}),timeout=40) as r:dest.write_bytes(r.read())
    records.append({'url':url,'path':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'bytes':dest.stat().st_size})
    print('SAVED',author,remote,dest.stat().st_size,flush=True)
(ROOT/'source-downloads.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
