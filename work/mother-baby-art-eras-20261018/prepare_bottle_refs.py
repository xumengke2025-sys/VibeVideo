from pathlib import Path
from PIL import Image
import json
R=Path(__file__).resolve().parent
A=R/'assets/generated-v2'
O=R/'assets/bottle-v3';O.mkdir(exist_ok=True)
jobs=json.loads((R/'assets/generation-catalog-v3.json').read_text(encoding='utf8'))
jobs.append({'index':34,'mode':'modern','name':'现代扁平插画','medium':'Warm modern flat 2D children book cartoon, textured solid pastel colors','costume':'cream romper with coral sleeves'})
batches=[]
for start in range(0,35,5):
 group=jobs[start:start+5]
 if not all((A/'layers'/f"{x['index']:02d}-{x['mode']}"/'baby-0.png').exists() for x in group):continue
 sheet=Image.new('RGBA',(2000,1550))
 for row,x in enumerate(group):
  for col in range(4):
   im=Image.open(A/'layers'/f"{x['index']:02d}-{x['mode']}"/f'baby-{col}.png').convert('RGBA')
   sheet.alpha_composite(im,(col*500,row*310))
 dest=O/f'reference-{start:02d}.png';sheet.save(dest)
 prompt='Edit this 4-column by 5-row transparent sprite atlas. Preserve EXACT grid, each cell 500x310 on a 2000x1550 sheet, no borders or labels. Each row is a different historical cartoon medium; maintain the SAME baby identity, head, round cheeks, short dark hair, facing right, body proportions and exact seated hip and floor registration in ALL cells. Change the yellow star toy and ALL arm poses to a baby lifting and drinking from a milk feeding bottle held with BOTH hands. Remove ALL stars completely. One baby and exactly ONE feeding bottle in each cell. The bottle has white milk and a clearly readable soft nipple. The bottle is deliberately a recognizable feeding bottle in every historical art medium, not a cup or vase. Four action columns left to right: (1) seated baby bends slightly, reaches BOTH hands toward the upright milk bottle immediately beside the feet on the floor; (2) baby hugs bottle in BOTH hands at chest; (3) baby drinks happily, bottle nipple touching mouth, head slightly tipped back, bottle angled upward with bottom higher than nipple, BOTH hands firmly hugging bottle; (4) baby lowers bottle to lap still held with BOTH hands. Make arm movements readable; bottle must stay attached to hands after lifting. Keep the fixed head and hips similar across columns. No separate floating hands. Every row STRICTLY 2D CARTOON with flat colored shapes; cute and warm, no realistic skin, no 3D. Keep clear gaps between all cells and rows, TRUE transparent background. Preserve each row art medium and costume described below. Do not draw environment, furniture, text, grids, numbers, mother or extra people. Output exact same aspect ratio and registration as reference.\n'
 for row,x in enumerate(group):prompt+=f"ROW {row+1} ONLY: {x['medium']}. Costume: {x['costume']}.\n"
 (O/f'batch-{start:02d}-prompt.txt').write_text(prompt,encoding='utf8')
 batches.append({'start':start,'reference':str(dest),'prompt':prompt,'rows':group})
(O/'batches.json').write_text(json.dumps(batches,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'batches':len(batches),'rows':sum(len(x['rows']) for x in batches)}))
