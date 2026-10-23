from pathlib import Path
import json,hashlib,sys,re
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;Q=R/'qa/v21';D=R/'assets/motion-v21'
M=json.loads((D/'manifest.json').read_text());issues=[];rows=[];ends={}
assert len(M['scenes'])==20 and len(M['bridges'])==19
for r in M['scenes']+M['bridges']:
    p=D/r['file'];a=np.array(Image.open(p).convert('RGBA'))
    if hashlib.sha256(p.read_bytes()).hexdigest()!=r['sha256']:issues.append(r['file']+' hash')
    if a.shape[:2]!=(r['rows']*560,4200):issues.append(r['file']+' dimensions')
    frames=[a[f//6*560:f//6*560+560,f%6*700:f%6*700+700] for f in range(r['frames'])]
    border=0
    for frame in frames:
        border+=int(np.count_nonzero(np.concatenate([frame[0,:,3],frame[-1,:,3],frame[:,0,3],frame[:,-1,3]])>12))
    if border:issues.append(r['file']+f' border {border}')
    ends[r['file']]=(frames[0].copy(),frames[-1].copy())
    rows.append({'file':r['file'],'frames':r['frames'],'border_pixels':border})
for r in M['bridges']:
    if not np.array_equal(ends[f'scene-{r["from"]:02d}.png'][1],ends[r['file']][0]):issues.append(r['file']+' start')
    if not np.array_equal(ends[f'scene-{r["to"]:02d}.png'][0],ends[r['file']][1]):issues.append(r['file']+' end')
scripts=['sequences-v21.js','environment-life-v20.js','environment-stopmotion-v15.js','transitions-v16.js','eras.js','chase-scenes-v9.js']
text_calls=[name for name in scripts if re.search(r'\.(fillText|strokeText)\s*\(', (R/'film'/name).read_text(encoding='utf8'))]
if text_calls:issues.append('Text drawing call: '+str(text_calls))
result={'version':21,'assets':39,'poses':sum(r['frames'] for r in rows),'rows':rows,'issues':issues,'text_drawing_calls':text_calls,'exact_endpoints':not any('start' in v or 'end' in v for v in issues),'scope':'Runtime script text-drawing scan; all atlas hashes, edges, dimensions, 38 identical endpoint pixel pairs. No anatomy or aesthetic certification.'}
(Q/'asset-check.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='rows'}));assert not issues
for page in range(4):
    sheet=Image.new('RGB',(1400,1250),'#b9afb0');draw=ImageDraw.Draw(sheet)
    for j,r in enumerate(M['scenes'][page*5:page*5+5]):
        atlas=Image.open(D/r['file']).convert('RGBA')
        for col,f in enumerate(np.linspace(0,r['frames']-1,5).round().astype(int)):
            im=Image.new('RGBA',(700,560),'#b9afb0');im.alpha_composite(atlas.crop((f%6*700,f//6*560,f%6*700+700,f//6*560+560)));x=col*280;y=j*250;sheet.paste(im.convert('RGB').resize((280,224)),(x,y+24));draw.text((x+4,y+4),f'{r["file"]} pose {f}',fill='black')
    sheet.save(Q/f'all-eras-{page}.jpg',quality=94)
for name in ['scene-16.png','scene-18.png','bridge-19.png']:
    r=next(r for r in M['scenes']+M['bridges'] if r['file']==name);atlas=Image.open(D/name).convert('RGBA');sheet=Image.new('RGB',(1400,300*((r['frames']+3)//4)),'#b9afb0');draw=ImageDraw.Draw(sheet)
    for f in range(r['frames']):
        im=Image.new('RGBA',(700,560),'#b9afb0');im.alpha_composite(atlas.crop((f%6*700,f//6*560,f%6*700+700,f//6*560+560)));x=f%4*350;y=f//4*300;sheet.paste(im.convert('RGB').resize((350,280)),(x,y+20));draw.text((x+4,y+3),f'{name} pose {f}',fill='black')
    sheet.save(Q/(name[:-4]+'-continuous.jpg'),quality=95)
