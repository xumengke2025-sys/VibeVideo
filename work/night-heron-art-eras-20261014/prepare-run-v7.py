from pathlib import Path
import json
root=Path(__file__).resolve().parent
assets=root/'assets/run-v7';assets.mkdir(exist_ok=True)
jobs=json.loads((root/'assets/run-v6/prompts.json').read_text('utf8'))
for j in jobs:
 old=j['prompt'];subject=old.split('Subject: ')[1].split('\nStyle/medium: ')[0];style=old.split('Style/medium: ')[1].split('\nFormat: ')[0]
 j['reference']=str(root/f"assets/run-v6/era-{j['era']:02}/pose-0.png")
 j['output']=f"owner-{j['era']:02}-sheet.png"
 j['prompt']=f'''Use case: illustration-story. Create a transparent 3x3 animation sprite sheet, NINE complete drawings of the exact reference animal, same scale, palette and medium.
Subject: {subject}
Style: {style}
CRITICAL animation change: the animal stands STILL. Its torso, wings, tail, legs and planted feet are IDENTICAL and identically positioned in ALL nine cells. Only HEAD, eyes and neck turn to follow a small bird running past from screen LEFT to screen RIGHT. Never turn or mirror the body. The fish theft surprises this animal. Wide alert eyes, raised ears/neck, anatomically normal closed muzzle or rigid closed beak. No aggression or chase. No face warping.
Format: square image, exactly 3 columns x 3 rows equal cells. Truly transparent alpha background, no grid, labels, props, fish, ground, shadow. Complete animal in every cell, 10% padding all sides, feet at 86% cell height. Keep room on BOTH sides for head/bill to turn. Fixed body registration.
Nine pose keys in reading order:
1 body facing LEFT, relaxed head and gaze down-left toward its fish.
2 SAME BODY, startled head facing LEFT, eyes wide and gaze down-left at approaching thief, slight head lift.
3 SAME BODY, surprised head faces LEFT and slightly down, eyes clearly tracking thief at lower-left.
4 SAME BODY, head turns toward viewer in a three-quarter LEFT front view, still looking slightly down at moving thief.
5 SAME BODY, head looking straight toward VIEWER, BOTH eyes visible, surprised wide eyes looking down, muzzle/beak correctly foreshortened.
6 SAME BODY, head turns three-quarter RIGHT toward the moving thief, surprised gaze down-right.
7 SAME BODY, head now points RIGHT over shoulder, looking down-right after thief. Beak or nose visibly points RIGHT.
8 SAME BODY, head points RIGHT, gaze right toward escaping thief, astonished hold.
9 SAME BODY, head lifted slightly to RIGHT, eyes following thief upward-right, mouth/beak still closed.
Important: rows 2 and 3 MUST genuinely turn the HEAD from left THROUGH FRONT to right while the body remains absolutely stationary facing left. Natural neck joint, no upside-down head. No walking or paw lift. Do not repeat all-left poses. No drawn arrows or textual labels.'''
(assets/'prompts.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf8')
for src,dst in [('run-v6.html','run-v7.html'),('src/run-v6.js','src/run-v7.js'),('render-run-v6.mjs','render-run-v7.mjs'),('package-run-v6.py','package-run-v7.py')]:
 text=(root/src).read_text('utf8').replace('run-v6','run-v7')
 (root/dst).write_text(text,encoding='utf8')
plan=json.loads((root/'production-plan-run-v6.json').read_text('utf8'));plan['version']='run-v7-bank-locked-head-tracking'
plan['userLatest']+=['被抢动物相对岸边静止','失鱼后惊讶，目光和头跟随夜鹭的行迹']
plan['direction']['ownerReaction']='脚底与岸边共享世界摄影位移；身体固定；惊讶后依据夜鹭相对位置由左经正面转向右，目光随头跟踪；保持嘴喙正常，不网格变形'
(root/'production-plan-run-v7.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
with (root/'CHECKPOINT.md').open('a',encoding='utf8') as f:f.write('''\n## run-v7 用户反馈继续制作（2026-10-15）\n- objective: 动物相对岸边静止，失鱼后惊讶，头与目光跟踪夜鹭由左向右跑过。\n- aspect_ratio: 9:16；width: 1080；height: 1920；delivery_mode: ai_review_once（既有预算已用，不新增审片者）。\n- cause: v6动物按世界相机每秒约600–850px横移，背景却仅按镜头进度缓移约50px/秒；两者摄影位移不一致，造成沿岸滑动。九姿势也均朝左，缺少追踪朝向。\n- implementation_plan: 背景岸线和固定动物共用同一摄影位移；16时代分别生成身体固定的头眼左→正面→右转动姿势，按夜鹭相对位置驱动。旧v6与历史版本保留。\n- next: 生成真实转头姿势，困难样段验证岸边固定与头眼跟随，再导出31秒48fps整片。\n''')
print('Prepared isolated v7 entry, plan and 16 prompts')
