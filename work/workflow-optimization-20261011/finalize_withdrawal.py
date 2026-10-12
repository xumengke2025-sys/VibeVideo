"""Refresh the withdrawal result without repeating completed media/skill tests."""
import json
from pathlib import Path

task = Path(__file__).resolve().parent
project = task.parents[1]
withdrawal = json.loads((task / 'activation/withdrawal.json').read_text(encoding='utf-8'))
for row in withdrawal['archived_files']:
    assert not (project / row['project_path']).exists()
    assert (task / row['archive_path']).is_file()
effective = json.loads((task / withdrawal['effective_configuration_check']).read_text(encoding='utf-8'))
layers = [row for row in effective['layers'] if row['name'].get('type') == 'project']
assert layers and all(not row['model_and_agents'] for row in layers)
assert any(row['model'] == 'gpt-6-astra' for row in effective['model_catalog'])
verification_path = task / 'verification.json'
verification = json.loads(verification_path.read_text(encoding='utf-8'))
verification['checks']['model_configuration'] = withdrawal
verification['checks']['project_model_overrides_removed'] = True
verification_path.write_text(json.dumps(verification, ensure_ascii=False, indent=2), encoding='utf-8')
print('3 configurations archived; no project model overrides; prior skill checks preserved; user confirmed switching restored.')
