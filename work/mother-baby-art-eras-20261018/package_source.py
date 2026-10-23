"""Package the editable film, license and review summary without runtime deps."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json
root=Path(__file__).resolve().parent
files=['film/index.html','film/film.js','film/eras.js','render.mjs','validate.mjs','prepare_evidence.py','package_source.py','README.md','THIRD_PARTY_NOTICES.md','REFERENCE-LICENSE.txt','brief.json','CHECKPOINT.md','research/REFERENCE-TRANSFER.md','out/mechanical-check.json','out/determinism-and-reach.json']
for rel in ['qa/v1/engineering-check.json','qa/v1/av-review.json','qa/v1/report.md','qa/v1/blind-observation.md','qa/v2/av-review.json','qa/v2/report.md','qa/v2/recheck.md']:
    if (root/rel).is_file():files.append(rel)
manifest={rel:{'sha256':hashlib.sha256((root/rel).read_bytes()).hexdigest(),'bytes':(root/rel).stat().st_size} for rel in files}
(root/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
dest=root/'out/mother-baby-editable-source.zip'
with ZipFile(dest,'w',ZIP_DEFLATED) as z:
    for rel in files+['source-manifest.json']:z.write(root/rel,'mother-baby-35-eras/'+rel)
print(json.dumps({'zip':str(dest),'files':len(files)+1,'bytes':dest.stat().st_size},ensure_ascii=False))
