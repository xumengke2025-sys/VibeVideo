import hashlib, json, shutil
from pathlib import Path

TASK = Path(__file__).parent
DEST = Path('D:/Codex/skills/vibe-video/assets/code-studies')
TEXT_SUFFIX = {'.js','.mjs','.cjs','.ts','.tsx','.html','.py','.json','.md','.glsl','.wgsl','.css','.yaml','.yml','.sh','.txt'}

def install(name, repo, commit, root, include, excluded, inspected):
    dest = DEST / name
    if dest.exists():
        raise RuntimeError('Refusing to overwrite: ' + str(dest))
    rows = []
    for p in sorted(root.rglob('*')):
        if not p.is_file(): continue
        rel = p.relative_to(root).as_posix()
        if any(x in p.relative_to(root).parts for x in ('.git','node_modules','out','.github')): continue
        if p.name == 'RESEARCH_SOURCE.json': continue
        if not include(rel): continue
        if p.suffix.lower() not in TEXT_SUFFIX and p.name not in ('LICENSE','NOTICE'): continue
        target = dest / rel
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(p,target)
        rows.append({'source_path':rel,'local_path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
    info = {'repository':'https://github.com/'+repo,'commit':commit,'checked':'2026-10-09','license':'MIT; original LICENSE retained',
            'scope':'Pinned source reference archive; not a reproduced film or complete offline asset/dependency bundle',
            'excluded':excluded,'inspected':inspected,'runtime_verification':'not run in this study','files':rows}
    (dest/'SOURCE.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
    print(name,len(rows),sum(x['bytes'] for x in rows))

install('mg-styles-15','Vincentwei1021/mg-styles-15','49052d80bfaf9fa8412cc9710530e5e95a3b8d8c',TASK/'source-text/mg-styles-15',lambda p:True,
        ['media, raster/mesh assets, fonts, audio samples, installed dependencies, site, output logs; selected text files only'],
        ['demos/08-morph/index.html:50-134,273-372','demos/07-liquid/js/shaders.js:1-200','demos/05-cel-boil/js/engine.js:1-231','demos/03-isometric/js/render.js:1-203','demos/20-pixel/film.js:1-105'])
install('papermotion','francozanardi/papermotion','aafddbe2dbc2b594bcd57c19c4a5a75c5c271be8',TASK/'source-text/papermotion',lambda p:True,
        ['media, installed dependencies, site, output logs; selected text files only'],
        ['examples/light/main.ts:1-162','examples/kite/main.ts:1-168','examples/cast/Child.ts:1-95','src/stage/Stage.ts:1-167','src/direction/Beats.ts:1-101'])
install('three-avbd','sbobyn/three-avbd','9b9c27b6b65a1212896e4d90e7e3d154c06e428a',Path('C:/CodexTemp/vibe-methodology-20261009/three-avbd'),
        lambda p:p.startswith(('src/','examples/')) or '/' not in p,
        ['media, installed dependencies, unrelated tooling and outputs'],['examples/basic.ts:1-85','src/app3d/renderer3d.ts:1-170'])
install('water-opus','AiondaDotCom/ai-sim-benchmark','680f87e6d54984199525dd12005bd95711bb47bb',Path('C:/CodexTemp/vibe-methodology-20261009/ai-sim-benchmark'),
        lambda p:p.startswith('runs/claude-code-opus-5-5/') or p in ('LICENSE','README.md'),
        ['other model runs, lobby, media, installed dependencies, output logs'],
        ['runs/claude-code-opus-5-5/src/main.ts:1-55','runs/claude-code-opus-5-5/src/sim/water.ts:1-320','runs/claude-code-opus-5-5/src/sim/world.ts:1-108','runs/claude-code-opus-5-5/src/render/waterMesh.ts:1-212','runs/claude-code-opus-5-5/src/render/cameraRig.ts:1-30'])
