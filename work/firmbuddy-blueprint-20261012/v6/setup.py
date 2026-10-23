import json
from pathlib import Path
R=Path(__file__).resolve().parent
old=(R.parent/'v5/film.js').read_text(encoding='utf-8')
helpers=old[:old.index('const centers=')]
(R/'film.js').write_text(helpers+(R/'scene-body.js').read_text(encoding='utf-8'),encoding='utf-8')
for f in ['render.mjs','index.html']:
    p=R/f;p.write_text(p.read_text(encoding='utf-8').replace('v5','v6').replace('V5','V6'),encoding='utf-8')
p=R/'vendor/paper.js'
p.write_text(p.read_text(encoding='utf-8').replace('vec3(.094,.200,.420), light = vec3(.165,.345,.650)','vec3(.025,.120,.232), light = vec3(.065,.252,.426)'),encoding='utf-8')
concept=json.loads((R.parent/'concepts/v6-stages/plan.json').read_text(encoding='utf-8'))
voices=[
'查商机、问业务、备拜访，一句业务问题，随时进入。',
'市场信息和客户名单，筛出待核实线索，并保留来源。',
'数十位专家，覆盖九类业务。按议题匹配、互补会商，让问题得到多角度研判。',
'专家从已装配的知识库查证。比如扩产计划没有资金安排，就先核实来源和缺口，不把信号当成确定需求。',
'信息缺项，变成具体拜访提问。还可按需生成商机诊断、销售陪练报告和客户经营计划。',
'用户确认后，创建跟进任务。实际记录再反馈给专家，更新商机判断。',
'从线索、答疑到拜访和持续经营。FirmBuddy，把业务问题，变成有依据的行动。'
]
shots=[]
for i,s in enumerate(concept['stages']):
    shots.append({k:s[k] for k in ['id','name','start','end','action','camera','handoff','anchor']})
    shots[-1].update(voiceover=voices[i],establish='Discover existing station in one continuous world',change=s['action'],result=s['handoff'])
plan={k:concept[k] for k in ['duration','fps','width','height','world','delivery_mode','review_budget','source_categories','camera_rules']}
plan.update(revision='V6',shots=shots,reading_windows=[[.6,2.9],[6.6,8.25],[14,16.1],[23.7,25.6],[32.7,34.7],[39.5,40.1],[48.4,51.9]],concepts='concepts/v6-stages/production-handoff.json',source_reference={'repository':'lemomo-ai/lemo-opuscar','commit':'e3cb16f63768c68693ff0e15171d6e755457cc32'},truth_limits=['Illustrative workflow, not live system execution','Nine business domains; individual selected experts are not domain names','Knowledge preconfigured; retrieval does not imply automatic training','Confirmation only gates task creation','Outputs are available by need, not all automatically generated'])
(R/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
p=R/'make_audio.py';s=p.read_text(encoding='utf-8')
s=s.replace('for t in [.5,.7,.9,2.3,5,7.3,8,9,11,11.35,11.65,14.3,15.7,16.3,19,20.5,22.6,23.2,24.2,26.6,29,30.3,32.4,33,33.4,34.6,37.8,38.2,39.7,41.2,44,45.1,49.6]:','for t in [.2,.36,.52,1.2,5.1,6.1,6.3,12.1,12.5,12.9,14,14.4,14.8,21.4,22.5,23.4,29.4,31.2,31.8,32.8,33,33.2,37.9,38.3,39.2,44,46.8]:')
s=s.replace('[(5.3,7.2),(10.1,11),(18.1,19),(20.5,22.6),(22.7,24.2),(25,26.6),(30.3,32.4),(36.2,37),(43.8,45.1),(47.5,49.6)]','[(3,6),(8.4,12),(16.3,21),(21.4,22.5),(25.8,29.1),(29.4,31.2),(35,38),(40.3,47.5)]')
s=s.replace('np.arange(11,18.2,.25)','np.arange(5.1,7.9,.375)')
p.write_text(s,encoding='utf-8')
print('V6 scene, plan and tools prepared')
