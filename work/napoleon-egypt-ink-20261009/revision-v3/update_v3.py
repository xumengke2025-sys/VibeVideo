from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parent
inputs=json.loads((R/'assets/generated-inputs.json').read_text(encoding='utf8'))
if not any(x['id']=='boot2' for x in inputs):
 inputs.append(dict(id='boot2',cols=4,rows=3,source='C:/Users/67236/.codex/generated_images/01a12958-186a-7ca3-8186-e232c238898d/exec-2cc2c563-9534-455c-9cb9-49ec2757a2a8.png',prompt="Use case historical-scene. Reference image is costume and ink style reference ONLY. Generate a corrected TWELVE-frame sprite sheet, strict FOUR columns by THREE rows, transparent background. Each isolated drawing takes at most 65 percent of its cell width and 75 percent of cell height, generous transparent gutters on ALL sides, no touching other cells. SAME pair of Napoleon's black riding boots, pale breeches, coat hem, cut off at thigh, facing RIGHT side view. No upper body, no boat, no ground. Fixed scale. ONE smooth step down from low boat to sand: frame1 both feet on raised step; 2 right knee lifts; 3 right foot reaches forward; 4 right heel lowers; 5 heel approaches sand; 6 right heel contacts sand 12cm lower than rear boot; 7 right sole settles; 8 weight onto right boot rear heel lifts; 9 rear foot airborne moving toward right; 10 rear boot lowers beside right; 11 both feet on same lower ground; 12 settled both feet planted. Preserve same leg lengths and boot size. Right foot front, left rear. Draw ACTUAL different natural ankle/knee poses. Traditional gray black ink wash, dry broken contours, wet gray folds, no color, no numbers, no labels or text, no shadows. CRITICAL never let an extended shoe touch the neighboring figure. Full feet in every cell.",method='Codex built-in imagegen',selected=True))
 (R/'assets/generated-inputs.json').write_text(json.dumps(inputs,ensure_ascii=False,indent=2),encoding='utf8')
if not (R/'plan-history.json').exists():shutil.copy2(R/'plan.json',R/'plan-history.json')
if not (R/'score-history.py').exists():shutil.copy2(R/'score.py',R/'score-history.py')
plan=json.loads((R/'plan.json').read_text(encoding='utf-8-sig'))
plan['status']='v3_implemented_pending_actual_av_review';plan['entry']='index-v3.html'
events=[]
def event(t,kind,target,gain=.12):events.append(dict(id=f'v3-{len(events):03}',at=round(t,4),target=target,sound=dict(kind=kind,offset=0,gain=gain)))
event(1.625,'footstep','landing-boots');event(2.975,'footstep','landing-boots')
for start,end,period,target in [(4,9,.625,'general'),(9,14,.575,'march'),(14,16.7,.65,'formation'),(24,26.4,.6,'general-result')]:
 t=start
 while t<end:event(t,'footstep',target,.065);t+=period
event(19.8,'齐射','firing-line',.17)
for i in range(16):event(18+i*.29,'hoof','cavalry',.07)
event(30,'远炮','fleet',.15);event(33.55,'帆和木材受击','mainmast',.16);event(34.05,'木断','mainmast',.18);event(35.7,'水面闷响','mast-water',.17)
for t in [43.15,44.25,45.35]:event(t,'刷石','brush-hand',.11)
for t in [46.1,47.3]:event(t,'笔端接触记录','writing-hand',.10)
for t in [49.5,50.77,51.4,52.03]:event(t,'footstep','boarding-general',.07)
event(52.65,'纸边落定','bench-contact',.07);event(54.1,'划桨','launch',.09);event(56,'浅浪覆盖','footprints',.12)
plan['events']=sorted(events,key=lambda e:e['at'])
for shot in plan['shots']:
 shot['implementation']='film-v3.mjs / generated full-pose assets, uniform group scale'
 shot['reads']=[{'at':shot['states'][k],'meaning':k} for k in ['establish','action','result']]
(R/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
# Preserve render.mjs: the new entry adds still-only capture before any movie is made.
src=(R/'render.mjs').read_text(encoding='utf8').replace("?'index.html'","?'index-v3.html'")
src=src.replace('if(args.check){',"if(args.stills){for(const t of String(args.stills).split(',').map(Number))fs.writeFileSync(path.join(out,'still-'+t+'.png'),await capture(t,true));fs.writeFileSync(path.join(out,'still-evidence.json'),JSON.stringify(evidence,null,2));console.log('stills complete')} else if(args.check){")
(R/'render-v3.mjs').write_text(src,encoding='utf8')
print('v3 manifest, timeline and rendering entry updated')
