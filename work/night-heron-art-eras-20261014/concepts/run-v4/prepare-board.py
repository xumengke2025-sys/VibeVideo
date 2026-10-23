from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib
root=Path(__file__).resolve().parent
names=['01-cave-bear.png','03-black-figure-pelican.png','09-ink-cormorant.png','09-ink-swallow.png']
manifest=[]
board=Image.new('RGB',(1290,650),'#e9e6de')
d=ImageDraw.Draw(board)
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',19)
labels=['史前 · 棕熊','古希腊 · 白鹈鹕','清初 · 叼鱼后','清初 · 仰头吞鱼']
for i,(name,label) in enumerate(zip(names,labels)):
    path=root/name
    im=Image.open(path)
    manifest.append({'file':name,'width':im.width,'height':im.height,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'inspection':'主制作已在生成结果实际查看，非独立动态审核'})
    im=im.convert('RGB')
    im.thumbnail((306,592))
    x=12+i*320+(306-im.width)//2
    board.paste(im,(x,42))
    d.text((12+i*320,12),label,fill='#302b26',font=font)
board.save(root/'concept-board.jpg',quality=93)
(root/'manifest.json').write_text(json.dumps({'status':'static_concepts_only','assets':manifest},ensure_ascii=False,indent=2),encoding='utf-8')
plan=json.loads((root.parents[1]/'production-plan-run-v4.json').read_text(encoding='utf-8'))
shots=plan['timeline']['shots']
assert len(shots)==16 and sum(s['frames'] for s in shots)==702
assert shots[0]['startFrame']==24 and shots[-1]['endFrameExclusive']==726
assert all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(shots,shots[1:]))
assert all(s['events']['grab'] < s['events']['headUp'] < s['events']['swallowStart'] < s['events']['fishGone'] < s['events']['neckTucked'] < s['events']['safeCutStart'] < s['frames'] for s in shots)
assert plan['brief']['frames']==744 and plan['brief']['duration']==31
print(json.dumps({'concepts':len(manifest),'sizes':[(x['width'],x['height']) for x in manifest],'shots':len(shots),'frames':744,'seconds':31,'event_order':'pass','dynamic_validation':'not_done'},ensure_ascii=False))

