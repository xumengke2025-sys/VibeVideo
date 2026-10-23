from pathlib import Path
import json,hashlib,zipfile,re
R=Path(__file__).resolve().parent
p=json.loads((R/'package.json').read_text(encoding='utf8'));p['version']='21.0.0';p['scripts']={'render':'node render-batched-v21.mjs','stills':'node render-v21.mjs stills','sample':'node render-v21.mjs sample','check':'node render-v21.mjs check','check:transitions':'node render-v21.mjs transitioncheck','preview':'node preview-v21.mjs'}
(R/'package.json').write_text(json.dumps(p,indent=2),encoding='utf8');(R/'README.md').write_text((R/'README-v21.md').read_text(encoding='utf8'),encoding='utf8')
b=json.loads((R/'brief.json').read_text(encoding='utf8'));b.update(version=21,entry='film/index-v21.html',source='out/mother-baby-v21-source-and-assets.zip',video='out/mother-baby-20-eras-portrait-v21-40s-music.mp4',silent=False,audio='assets/audio-v21/warm-family-40s.wav',text_overlay=False,production_route='Text-free; exact-clock actor resampling, local hand/prop matte repair, four newly generated handover poses; stationary cushion and background details retained; original 40s family score')
(R/'brief.json').write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf8')
names=['README.md','README-v21.md','CHECKPOINT.md','brief.json','package.json','THIRD_PARTY_NOTICES.md','REFERENCE-LICENSE.txt','render-v21.mjs','render-batched-v21.mjs','preview-v21.mjs','build_motion_v21.py','build_batched_v21.py','build_handover_v21.py','check_assets_v21.py','clean_matte_v21.py','verify_source_runtime_v21.py','finalize_v21.py','package_source_v21.py','film/index-v21.html','film/sequences-v21.js','film/environment-life-v20.js','film/environment-stopmotion-v15.js','film/chase-scenes-v9.js','film/eras.js','film/transitions-v16.js']
files={R/n for n in names};files.update({R/'compose_music_v21.py',R/'add_music_v21.py',R/'record_review_v21.py'});files.update((R/'assets/audio-v21').glob('*'));scenes=json.loads((R/'film/chase-scenes-v9.js').read_text(encoding='utf8').split('=',1)[1].strip().rstrip(';'))
runtime={(R/'film'/s['background']).resolve() for s in scenes};runtime.add(R/'assets/audio-v21/warm-family-40s.wav')
m=json.loads((R/'assets/motion-v21/manifest.json').read_text());runtime.update(R/'assets/motion-v21'/r['file'] for r in m['scenes']+m['bridges']);runtime.update({R/'assets/motion-v20/cushions-atlas.png',R/'assets/motion-v21/manifest.json',R/'assets/environment-v15/animals-atlas.png'});files.update(runtime)
for pattern in ['assets/motion-v20/scene-*.png','assets/motion-v20/bridge-*.png','assets/motion-v20/manifest.json','assets/motion-v21/handover-*','qa/v21/*.json','qa/v21/*comparison.jpg','qa/v21/handover-keys.jpg','qa/v21/final/*.json','qa/v21/final/*.png']:
    files.update(f for f in R.glob(pattern) if f.is_file())
assert all(f.is_file() for f in files)
manifest={'version':21,'video_included':False,'photos_included':False,'runtime_assets':len(runtime),'sha256':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}}
dest=R/'out/mother-baby-v21-source-and-assets.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
    for p in sorted(files):z.write(p,p.relative_to(R))
    z.writestr('SOURCE-PACKAGE.json',json.dumps(manifest,indent=2))
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    for n,h in manifest['sha256'].items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
    for s in re.findall(r'<script src="([^"]+)"',(R/'film/index-v21.html').read_text(encoding='utf8')):assert 'film/'+s in z.namelist(),s
    target=R/'out/source-runtime-v21';target.mkdir(exist_ok=True);z.extractall(target)
result={'archive':str(dest),'files':len(files),'runtime_assets':len(runtime),'zip_integrity':True,'all_hashes_match':True,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'extracted_to':str(target)}
(R/'out/source-package-v21-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
