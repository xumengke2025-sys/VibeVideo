"""Production contact sheets of the actual baked actor handoffs."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parent
Q=R/'qa/v17'; manifest=json.loads((R/'assets/motion-v17/manifest.json').read_text())
for page in range(4):
    rows=manifest['bridges'][page*5:(page+1)*5]
    board=Image.new('RGB',(1400,320*len(rows)),'#eee4d3');draw=ImageDraw.Draw(board)
    for row,r in enumerate(rows):
        with Image.open(R/'assets/motion-v17'/r['file']) as atlas:
            for col,f in enumerate([0,round((r['frames']-1)*.25),round((r['frames']-1)*.5),round((r['frames']-1)*.75),r['frames']-1]):
                x=f%r['columns']*r['width'];y=f//r['columns']*r['height']
                cell=atlas.crop((x,y,x+r['width'],y+r['height']))
                bg=Image.new('RGBA',cell.size,'#eee4d3');bg.alpha_composite(cell);bg.thumbnail((280,280))
                px=col*280;py=row*320;board.paste(bg.convert('RGB'),(px,py+34))
                draw.text((px+4,py+8),f"cut {r['cut_seconds']}s | F{f}",fill='#342a20')
    board.save(Q/f'bridge-overview-{page}.jpg',quality=94)
print('4 actual-actor contact sheets ready')
