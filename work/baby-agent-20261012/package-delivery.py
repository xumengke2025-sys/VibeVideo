"""Collect the actual film inputs and editable sources; exclude large frame caches."""
from pathlib import Path
import hashlib,json,zipfile,sys
root=Path(__file__).resolve().parent
version=sys.argv[1] if len(sys.argv)>1 else 'final-v1'
output=root/'out'/version
files=['README.md','index.html','film.mjs','server.mjs','render.mjs','make_audio.py','brief.json','plan.json','events.json','assets/head-atlas.png','assets/LICENSE-lemo.txt','audio/mix.wav','audio/audio-info.json']
manifest={'title':'代号：小小读者','version':version,'files':{}}
for name in files:
    p=root/name
    manifest['files'][name]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
manifest['video']={'path':str(output/'video.mp4'),'sha256':hashlib.sha256((output/'video.mp4').read_bytes()).hexdigest()}
(output/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
with zipfile.ZipFile(output/'小小读者-源码与素材.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in files:z.write(root/name,'小小读者/'+name)
    z.write(output/'source-manifest.json','小小读者/source-manifest.json')
print(json.dumps({'archive':str(output/'小小读者-源码与素材.zip'),'video_sha256':manifest['video']['sha256']},ensure_ascii=False))
