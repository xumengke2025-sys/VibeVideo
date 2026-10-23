"""Actual corrected-cel evidence. Measurements are a contour proxy, not anatomy."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;Q=R/'qa/v19';D=R/'assets/motion-v19'
M=json.loads((D/'manifest.json').read_text())
def cel(atlas,f):
    return atlas.crop((f%6*700,f//6*560,f%6*700+700,f//6*560+560))
def tile(a,size=(280,224)):
    bg=Image.new('RGBA',(700,560),'#ad7194');bg.alpha_composite(a)
    return bg.convert('RGB').resize(size)
for page in range(4):
    board=Image.new('RGB',(1400,1260),'#ad7194');d=ImageDraw.Draw(board)
    for row,r in enumerate(M['scenes'][page*5:page*5+5]):
        atlas=Image.open(D/r['file'])
        for col,f in enumerate([0,12,24,35,47]):
            board.paste(tile(cel(atlas,f)),(col*280,row*252+24))
            d.text((col*280+5,row*252+5),f'Scene {r["era"]} F{f}',fill='white')
    board.save(Q/f'infant-overview-{page}.jpg',quality=94)
for name,ids in [('scene-16',range(24,40)),('scene-18',range(24,40)),('bridge-18',range(17)),('bridge-19',range(25))]:
    atlas=Image.open(D/(name+'.png'));board=Image.new('RGB',(1400,304*((len(ids)+3)//4)),'#ad7194');d=ImageDraw.Draw(board)
    for k,f in enumerate(ids):
        board.paste(tile(cel(atlas,f),(350,280)),(k%4*350,k//4*304+24))
        d.text((k%4*350+4,k//4*304+4),f'{name} F{f}',fill='white')
    board.save(Q/f'continuous-{name}.jpg',quality=94)
records=json.loads((Q/'infant-registration.json').read_text());summary=[]
for r in records:
    a=np.array(r['after_diameters']);b=np.array(r['before_diameters'])
    summary.append({'file':r['file'],'before_min':round(float(b.min()),2),'before_max':round(float(b.max()),2),'after_min':round(float(a.min()),2),'after_max':round(float(a.max()),2),'after_largest_adjacent_proxy_change':round(float(abs(np.diff(a)).max()),2),'before_span':round(float(np.ptp(b)),2),'after_span':round(float(np.ptp(a)),2)})
b=np.concatenate([r['before_diameters'] for r in records]);a=np.concatenate([r['after_diameters'] for r in records])
report={'target_skull_arc_diameter_px':130,'baked_cels':len(a),'before_percentiles_5_50_95':np.percentile(b,[5,50,95]).tolist(),'after_percentiles_5_50_95':np.percentile(a,[5,50,95]).tolist(),'scope':'Exterior hair-arc proxy; changing pose/style and rasterization affect readings. Not a claim of anatomical precision or viewing.','records':summary}
(Q/'infant-size-check.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='records'}))
print(json.dumps(sorted(summary,key=lambda r:r['after_span'],reverse=True)[:8]))
