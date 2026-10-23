from pathlib import Path
from PIL import Image
import hashlib, json
p = Path(__file__).resolve().parent
items = []
for name in ['01-character.png', '02-connected-workshop.png', '03-expert-conversation.png', '04-abstract-character.png', '05-abstract-conversation.png']:
    f = p / name
    with Image.open(f) as im:
        im.load()
        items.append({'file':name,'width':im.width,'height':im.height,'mode':im.mode,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
report={'stage':'concept_only','generation':'built_in_image_gen','video_target':[1920,1080], 'images':items,'observed':'角色设定、修订后连通空间、专家会商关键帧已实际查看；概念不等同于可动资产。','next':'用户反馈方向后制作连续动作样段。'}
(p/'assets.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(items,ensure_ascii=False))
