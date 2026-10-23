from pathlib import Path
R=Path(__file__).resolve().parent
for name in ['film/index-v17.html','film/sequences-v17.js','render-v17.mjs','render-batched-v17.mjs','preview-v17.mjs','finalize_v17.py','inspect_transitions_v17.py','inspect_bridges_v17.py','check_assets_v17.py','verify_source_runtime_v17.py']:
    text=(R/name).read_text(encoding='utf8').replace('v17','v18')
    (R/name.replace('v17','v18')).write_text(text,encoding='utf8')
print('v18 render and checking entries ready')
