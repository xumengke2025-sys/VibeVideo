import json,sys,subprocess,zipfile,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools/python'))
import imageio_ffmpeg
ff=imageio_ffmpeg.get_ffmpeg_exe()
final=ROOT/'out/final-v4-execution';video=final/'video.mp4';qa=final/'delivery-frames';qa.mkdir(exist_ok=True)
times=[4.5,12.8,20.5,34.5,43.5,53.5,59.3,66.5]
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
board=Image.new('RGB',(1920,590),'#0b1830');draw=ImageDraw.Draw(board)
for i,t in enumerate(times):
    target=qa/f'{t}.png'
    if not target.exists():subprocess.run([ff,'-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(target)],check=True)
    im=Image.open(target);im.thumbnail((480,270));x=i%4*480;y=i//4*295;board.paste(im,(x,y+25));draw.text((x+8,y+3),f'{t:.1f}s / decoded MP4',font=font,fill='#dceaf7')
board.save(qa/'contact.jpg',quality=93)
evidence=json.loads((final/'evidence.json').read_text(encoding='utf-8'))
assert hashlib.sha256(video.read_bytes()).hexdigest()==evidence['sha256']
observations_file=final/'observations.json'
observations=json.loads(observations_file.read_text(encoding='utf-8')) if observations_file.exists() else None
observed=bool(observations and observations['sha256']==evidence['sha256'] and observations['decoded_final_contact_actually_viewed'])
checks=json.loads((ROOT/'out/stills-v4-execution/checks.json').read_text(encoding='utf-8'))
assert not checks['errors'] and all(x['identical'] for x in checks['seeks'])
layout=json.loads((ROOT/'out/layout-v4.json').read_text(encoding='utf-8'));assert not layout['issues']
result={
    'video':str(video),'sha256':evidence['sha256'],'width':1920,'height':1080,'fps':30,'duration':68,'frames':2040,
    'full_decode':True,'audio_codec':'AAC','video_codec':'H264','deterministic_seek_samples':checks['seeks'],
    'layout':{'samples':layout['samples'],'issues':0,'scope':layout['scope']},
    'actual_visual_observations':[
        'Initial full-size scene images: 20.5,34.5,43.5,66.5s.',
        'Preview overview sampled at 24–46s in one-second steps; gap-to-question sequence sampled at12fps,39.333–40.25s.',
        'Final-quality sample evidence-return sequence:32.8–33.7s sampled at12fps. Production observations, not independent review.',
    ],
    'decoded_final_frames_exported':times,'decoded_final_frames_viewing_status':'8-frame contact actually viewed; see observations.json' if observed else 'awaiting_actual_visual_inspection',
    'full_listening_completed':False,'independent_review':'prior round used; no new independent review for V4',
}
(final/'delivery-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
archive=ROOT/'FirmBuddy-source-v4.zip'
files=[p for p in (ROOT/'v4').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
files+=[ROOT/f for f in ['server.mjs','ANIMATION-PLAN-V4.md','plan-v4.json','product-reassessment-20261013.json','plan-v4-verification.json']]
files+=[p for p in (ROOT/'assets/reference').rglob('*') if p.is_file()]
files+=[final/'evidence.json',final/'delivery-checks.json',ROOT/'out/layout-v4.json']
if observed:files.append(observations_file)
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for file in files:z.write(file,file.relative_to(ROOT))
print(json.dumps({'video':str(video),'megabytes':round(video.stat().st_size/1048576,2),'source':str(archive),'source_megabytes':round(archive.stat().st_size/1048576,2),'decoded_frame_contact':str(qa/'contact.jpg')},ensure_ascii=False))
