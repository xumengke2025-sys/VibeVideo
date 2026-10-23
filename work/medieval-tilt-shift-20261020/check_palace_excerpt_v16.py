"""Bounded contact sheets and a technical scan of the new two-second shot."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;F=P/'render/frames-v16';Q=P/'qa/v16/excerpt';Q.mkdir(exist_ok=True)
rows=[];prev=None;imgs=[]
for f in range(648,696):
 with Image.open(F/f'{f:05d}.png') as im:
  assert im.size==(1080,1920);im.load();a=np.asarray(im.resize((135,240)),np.float32)
  rows.append({'frame':f,'mean':float(a.mean()),'difference_from_previous':float(np.abs(a-prev).mean()) if prev is not None else None})
  imgs.append(im.resize((225,400)));prev=a
for k in range(3):
 sheet=Image.new('RGB',(900,1704),(28,28,28));d=ImageDraw.Draw(sheet)
 for j in range(16):
  index=k*16+j;x=(j%4)*225;y=(j//4)*426;sheet.paste(imgs[index],(x,y));d.text((x+8,y+405),f'{648+index} / {(648+index)/24:.3f}s',fill='white')
 sheet.save(Q/f'continuous-{k+1}.jpg',quality=91)
report={'frames':[648,695],'count':48,'dimensions':[1080,1920],'frame_stats':rows,'max_adjacent_mean_difference':max(r['difference_from_previous'] or 0 for r in rows),'method':'Downsampled RGB differences and full-range contact sheets. Does not prove absence of subtle shimmer or aesthetic quality.','frozen_manifest_sha256':hashlib.sha256((P/'render/frozen-v16-manifest.json').read_bytes()).hexdigest()}
(Q/'technical-scan.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('EXCERPT_SHEETS_READY',report['max_adjacent_mean_difference'])
