import json
from pathlib import Path
root=Path(__file__).resolve().parent
dest=root/'assets/run-v6';dest.mkdir(exist_ok=True)
old=json.loads((root/'assets/run-v4/prompts-all.json').read_text('utf8'))
prompts=[]
for item in old:
 n=item['era'];avian=n in [3,5,6,7,9,10,15,16]
 anatomy=('Keep the entire bill a clean rigid anatomically correct shape in EVERY drawing, CLOSED throughout. Express surprise with round alert eyes and a lifted head, never by bending or stretching the bill. Natural neck curves, no knots. Wings stay folded.' if avian else 'Keep muzzle, nose and jaw anatomically correct in EVERY drawing. Mouth mostly closed; surprise through round alert eyes, ears and lifted head. No huge open mouth, no stretched lips, no human teeth. Paws stay planted.')
 prompt=f'''Use case: illustration-story. Create ONE finished animation sprite sheet of the SAME animal in NINE hand-redrawn successive reaction poses. Reference image is the exact character/style reference, not something to warp. Redraw the poses carefully.
Subject: {item['owner']}
Style/medium: {item['medium']} Match the reference palette, pigment, outline and detail density EXACTLY. Do not make a generic modern cartoon.
Format: a SQUARE image, exact 3 columns x 3 rows of equal SQUARE cells, 9 cells in reading order. Truly TRANSPARENT alpha background. No grid, no captions/numbers, no shadows, no ground, no fish or other props. Each cell contains ONE complete animal facing LEFT. Keep full beak, tail and feet inside with 8% padding. Same scale and body registration in all cells: feet at 87% cell height, torso center at x59%; body, paws and tail nearly stationary, only head/neck/eye/ear gestures change. Leave head motion room above and left.
Nine successive drawings in reading order:
1 relaxed neutral, looking left at its fish spot;
2 notices the missing fish, alert eye and small head recoil;
3 recoil apex, a puzzled pause, clean face;
4 head lowers halfway to look at the empty spot in front of its feet;
5 head fully lowered inspecting the empty spot, readable comic disbelief;
6 head begins lifting again, puzzled;
7 surprised upright double-take, eyes wide, head slightly tipped backward;
8 holds the funny surprised pose, small ear/neck emphasis;
9 settles slightly while still looking astonished, does not return to neutral.
{anatomy}
Humor comes from timing and the double-take, not disfigurement. No aggression, fighting or pursuit. No extra body parts, duplicate heads, bent beaks, twisted mouths, stretched face, melting anatomy, detached parts or motion blur. All nine are genuine finished distinct pose drawings, not a deformed mesh.'''
 prompts.append({'era':n,'prompt':prompt,'reference':str(root/f'assets/run-v4/era-{n:02}/owner-neutral.png'),'output':f'owner-{n:02}-sheet.png'})
(dest/'prompts.json').write_text(json.dumps(prompts,ensure_ascii=False,indent=2),encoding='utf8')
for source,target in [('run-v5.html','run-v6.html'),('render-run-v5.mjs','render-run-v6.mjs'),('src/run-v5.js','src/run-v6.js'),('production-plan-run-v5.json','production-plan-run-v6.json'),('package-run-v5.py','package-run-v6.py')]:
 text=(root/source).read_text('utf8').replace('run-v5.html','run-v6.html').replace('src/run-v5.js','src/run-v6.js').replace('production-plan-run-v5.json','production-plan-run-v6.json').replace('render-run-v5.mjs','render-run-v6.mjs')
 if target=='render-run-v6.mjs':text=text.replace("...walk('assets/run-v5')","...walk('assets/run-v5'),...walk('assets/run-v6')")
 (root/target).write_text(text,encoding='utf8')
print('Prepared v6 files and 16 redraw prompts')
