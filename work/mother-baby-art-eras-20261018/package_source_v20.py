from pathlib import Path
import json,hashlib,zipfile,re
R=Path(__file__).resolve().parent
(R/'README.md').write_text((R/'README-v20.md').read_text(encoding='utf8'),encoding='utf8')
(R/'requirements-build-v20.txt').write_text('numpy\nPillow\nopencv-python\n',encoding='utf8')
p=json.loads((R/'package.json').read_text(encoding='utf8'));p['version']='20.0.0';p['scripts']={'render':'node render-batched-v20.mjs','stills':'node render-v20.mjs stills','sample':'node render-v20.mjs sample','check':'node render-v20.mjs check','check:transitions':'node render-v20.mjs transitioncheck','check:environment':'node render-v20.mjs environmentcheck','preview':'node preview-v20.mjs'}
(R/'package.json').write_text(json.dumps(p,indent=2),encoding='utf8')
b=json.loads((R/'brief.json').read_text(encoding='utf8'));b.update(version=20,entry='film/index-v20.html',source='out/mother-baby-v20-source-and-assets.zip',video='out/mother-baby-20-eras-portrait-v20-40s.mp4',production_route='Fixed cushion independent of v19-size actor layer; registered local indoor animation; preserved outdoor action and shared actor connections')
(R/'brief.json').write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf8')
names=['README.md','README-v20.md','CHECKPOINT.md','brief.json','package.json','THIRD_PARTY_NOTICES.md','REFERENCE-LICENSE.txt','requirements-build-v20.txt','render-v20.mjs','render-batched-v20.mjs','preview-v20.mjs','build_cushions_v20.py','build_batched_v20.py','prepare_cushion_atlas_v20.py','check_fixed_layers_v20.py','inspect_cushions_v20.py','finalize_v20.py','inspect_encoded_infant_v20.py','package_source_v20.py','verify_source_runtime_v20.py','film/index-v20.html','film/sequences-v20.js','film/environment-life-v20.js','film/environment-stopmotion-v15.js','film/chase-scenes-v9.js','film/eras.js','film/transitions-v16.js']
names.extend(['inspect_environment_encoded_v20.py','record_review_v20.py'])
files={R/n for n in names};scenes=json.loads((R/'film/chase-scenes-v9.js').read_text(encoding='utf8').split('=',1)[1].strip().rstrip(';'))
runtime={(R/'film'/s['background']).resolve() for s in scenes}
m=json.loads((R/'assets/motion-v20/manifest.json').read_text());runtime.update(R/'assets/motion-v20'/r['file'] for r in m['scenes']+m['bridges']);runtime.update({R/'assets/motion-v20/cushions-atlas.png',R/'assets/motion-v20/manifest.json',R/'assets/environment-v15/animals-atlas.png'});files.update(runtime)
for pattern in ['assets/motion-v19/*.png','assets/motion-v19/manifest.json','assets/motion-v20/cushions-generated.png','assets/motion-v20/cushion-prompt.txt','qa/v20/*.json','qa/v20/cushion-input-*.jpg','qa/v20/fixed-cushions-*.jpg','qa/v20/final/*.json','qa/v20/final/*.txt','qa/v20/final/*.png']:
    files.update(f for f in R.glob(pattern) if f.is_file())
assert all(f.is_file() for f in files)
manifest={'version':20,'video_included':False,'photos_included':False,'runtime_assets':len(runtime),'sha256':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}}
dest=R/'out/mother-baby-v20-source-and-assets.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=2) as z:
    for p in sorted(files):z.write(p,p.relative_to(R))
    z.writestr('SOURCE-PACKAGE.json',json.dumps(manifest,indent=2))
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    for n,h in manifest['sha256'].items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
    for s in re.findall(r'<script src="([^"]+)"',(R/'film/index-v20.html').read_text(encoding='utf8')):assert 'film/'+s in z.namelist(),s
    target=R/'out/source-runtime-v20';target.mkdir(exist_ok=True);z.extractall(target)
result={'archive':str(dest),'files':len(files),'runtime_assets':len(runtime),'zip_integrity':True,'all_hashes_match':True,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'extracted_to':str(target)}
(R/'out/source-package-v20-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
