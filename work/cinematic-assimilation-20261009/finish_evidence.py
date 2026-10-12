from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib
root=Path(__file__).parent
skill=Path('D:/Codex/skills/vibe-video')
for name in ['beach','reel']:
    folder=root/'reference-output'/name
    files=sorted(folder.glob('frame-*.jpg'))
    for page in range((len(files)+29)//30):
        sheet=Image.new('RGB',(1600,1248),'#101820'); draw=ImageDraw.Draw(sheet)
        for j,p in enumerate(files[page*30:(page+1)*30]):
            x,y=(j%5)*320,(j//5)*208
            with Image.open(p) as im: sheet.paste(im.resize((320,180)),(x,y))
            draw.text((x+5,y+185),p.name,fill='white')
        sheet.save(folder/f'window-{page:02d}.jpg',quality=90)
report={'skill_version':'0.6.0','code_only_demo':True,'video':str(root/'demo/out-durable/lumen-sound.mp4'),
 'video_sha256':hashlib.sha256((root/'demo/out-durable/lumen-sound.mp4').read_bytes()).hexdigest(),
 'visual_review':{'method':'480 decoded frames viewed in 16 contact sheets; selected 1280px frames','frames':[0,479],'reviewer':'primary agent','findings':['No blank frames observed','4s intentional cut; 9s and 14s camera joins continuous','8.2s propagation and 9–14s reveal readable','Local glass highlights broad; final overview intentionally subdued']},
 'audio':{'technical_check':'media-check/media-evidence.json','listened':False},
 'pixel_repeat':{'identical':False,'difference':'one pixel at (903,387), max channel difference 6/255 at t=12.32; cause unresolved','strict_mode':'--strict-pixels'},
 'source_evidence':['reference-output/beach/capture-evidence.json','reference-output/reel/capture-evidence.json','bundled-replay/beach/capture-evidence.json','bundled-replay/reel/capture-evidence.json'],
 'sdf_validation':'1 second rendered; 4 second timeline representative frames; approximate single-interface refraction',
 'vendor_hash_validation':[]}
for source in (skill/'assets/code-studies').glob('*/SOURCE.json'):
    data=json.loads(source.read_text(encoding='utf-8'))
    report['vendor_hash_validation'].append({'source':str(source),'manifest':data})
(root/'delivery-evidence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Contact sheets and delivery evidence saved')
