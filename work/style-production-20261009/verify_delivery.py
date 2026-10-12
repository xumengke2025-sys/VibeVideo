import hashlib,json,re
from pathlib import Path
work=Path(__file__).resolve().parent
installed=Path('D:/Codex/skills/vibe-video')
files=[installed/'SKILL.md',installed/'references/style-production.md',installed/'references/event-timeline.md',installed/'references/capability-evidence.md',*installed.glob('references/style-packs/*/*.md')]
broken=[];checked=0
for p in files:
    for rel in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if '://' in rel or rel.startswith('#'):continue
        checked+=1
        if not (p.parent/rel.split('#')[0]).exists():broken.append({'file':str(p),'link':rel})
assert not broken,broken
e=json.loads((work/'installed-portability/render-evidence.json').read_text(encoding='utf-8'))
assert e['seek']['identical'] and not e['errors']
frame=work/'installed-portability/still-4.400.png'
projectframe=work/'studio/out-approved/dataviz-variant/still-4.400.png'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(frame)==sha(projectframe)
report={'local_links_checked':checked,'broken_links':broken,'installed_and_snapshot_skill_format':'passed','installed_toolkit_contract_checks':'passed','installed_toolkit_still_rebuild':'passed','installed_vs_project_still_pixels_sha256':sha(frame),'portability_scope':'Same machine and runtimes; no clean-machine installation tested.'}
(work/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
p=work/'CHECKPOINT.md';p.write_text(p.read_text(encoding='utf-8')+'\n技能格式与链接检查通过；安装工具源码的契约检查和代表帧重建通过，重建 PNG 与项目输出 SHA256 相同。同机运行验证不等于全新机器安装验证，见 verification.json。\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
