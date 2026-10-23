from pathlib import Path
R=Path(__file__).resolve().parent
for name in ['film/index-v16.html','render-v16.mjs','render-batched-v16.mjs','finalize_v16.py','inspect_encoded_v16.py','inspect_transitions_v16.py','package_source_v16.py']:
    src=(R/name).read_text(encoding='utf8');dest=name.replace('v16','v17')
    if name.endswith('.html'):src=src.replace('sequences-v16.js','sequences-v17.js')
    elif name.endswith('.mjs'):src=src.replace('v16','v17').replace('SCENE_TRANSITIONS_V17','SCENE_TRANSITIONS_V16')
    else:src=src.replace('v16','v17')
    if name=='render-v16.mjs':
        src=src.replace("state.era+':'+state.actor_frame+':env'+state.cel","state.actor_key+':'+state.actor_frame+':env'+state.era+':'+state.cel")
        src=src.replace("const evidence=await page.evaluate(()=>window.__auditAll());","const evidence=await page.evaluate(async()=>({...window.__auditAll(),continuity:await window.__continuityQA()}));if(evidence.continuity.issues.length)evidence.issues.push(...evidence.continuity.issues);")
    (R/dest).write_text(src,encoding='utf8')
print('v17 entry and render tools ready')
