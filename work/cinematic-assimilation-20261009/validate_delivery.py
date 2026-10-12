from pathlib import Path
import json,hashlib,re
root=Path(__file__).parent; skill=Path('D:/Codex/skills/vibe-video'); count=0
for source in (skill/'assets/code-studies').glob('*/SOURCE.json'):
    data=json.loads(source.read_text(encoding='utf-8'))
    for f in data['files']:
        p=source.parent/f['path']
        assert p.is_file(),str(p)
        assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'],str(p)
        count+=1
for doc in [skill/'SKILL.md',skill/'references/code-cinema.md']:
    for link in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
        if '://' not in link: assert (doc.parent/link.split('#')[0]).exists(),link
report=json.loads((root/'delivery-evidence.json').read_text(encoding='utf-8'))
report['packaging_validation']={'vendor_files_verified':count,'local_links':'pass','renderer_sdf_stills':'pass'}
(root/'delivery-evidence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'checkpoint.md').write_text('''# 完成 checkpoint

目标：吸收可证明由代码绘制的开源成果到 vibe-video。
完成：两套MIT完整运行源码和离线回放器，摄影/美术/转场配方，原创16秒代码片、声音、480帧接触表审片，独立SDF实验，skill0.6主入口与可运行模板。
验证：原作两模式回放通过；新renderer SDF出图通过；成片完整解码和媒体技术通过；源码哈希与本地路由通过。详细证据见delivery-evidence.json。
边界：未复现513全库；原海滩局部黑帧未定位；原创重复帧有单像素差；声音未实际听音；玻璃非完整焦散。
下一步：交付已完成资源，后续具体题材从可执行工程和配方开始。
''',encoding='utf-8')
print(f'Verified {count} vendor files; local links pass')
