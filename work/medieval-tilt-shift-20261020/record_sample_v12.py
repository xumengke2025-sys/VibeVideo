from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent;QA=ROOT/'qa/v12';FOLDER=ROOT/'render/sample-v12'
sheet=Image.new('RGB',(1080,1380),'#202020');draw=ImageDraw.Draw(sheet)
for i,f in enumerate(range(732,756)):
 with Image.open(FOLDER/f'{f:05d}.png') as im:
  im.thumbnail((180,320));x=i%6*180;y=i//6*345;sheet.paste(im,(x,y+25));draw.text((x+5,y+5),f'f{f} | {f/24:.3f}s',fill='white')
sheet.save(QA/'final-tow-continuous.jpg',quality=94)
record={'manifest':'render/frozen-v12-manifest.json','manifest_sha256':hashlib.sha256((ROOT/'render/frozen-v12-manifest.json').read_bytes()).hexdigest(),'producer':True,'independent_review':False,'actual_viewed_final_source_frames':[744],'previous_diagnostic_source_frames_actually_viewed':[288,528,744,1176,1752],'continuous_sheet':'qa/v12/final-tow-continuous.jpg','continuous_sheet_actually_viewed':False,'observations':['Final-model frame 744 shows eight towmen on the raised waterside path with two connected ropes and painted cargo boats. No intervening building occlusion is visible at this inspected frame.','Previous diagnostic source frames show Egyptian gifts/fan bearers and guards at the gate, distinct armed patrol in the market, white-robed priests before the divine statues, and citizens extending along the avenue into the distance. These observations predate the local towpath update.'],'limits':['No full-film viewing claim.','No new independent review or subjective listening.']}
(QA/'production-sample-observations.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
print('CONTINUOUS_SHEET_READY')
