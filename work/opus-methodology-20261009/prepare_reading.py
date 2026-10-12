from pathlib import Path
import json, re, hashlib
root=Path(__file__).parent; root.mkdir(parents=True,exist_ok=True)
data=json.loads(Path('D:/Codex/skills/vibe-video/assets/opus-gallery.json').read_text(encoding='utf-8'))
entries=data['entries']; seen=set(); groups={k:[] for k in ['motion','explainer','3d','interactive']};long=[]
for x in entries:
    h=hashlib.sha256(x['prompt'].encode()).hexdigest()
    if h in seen: continue
    seen.add(h)
    if len(x['prompt'])<=1000:groups[x['category']].append(x)
    else:long.append(x)
for category,items in groups.items():
    lines=[]
    for x in items:
        lines.append(f"[{x['slug']}] partial={x['prompt_partial']}\n{x['prompt']}\n")
    (root/f'read-{category}.txt').write_text('\n'.join(lines),encoding='utf-8')
lines=[]
for x in long:
    p=x['prompt']; paragraphs=re.split(r'\n\s*\n',p)
    selected=[v for v in paragraphs if re.search(r'camera|morph|mask|light|material|transit|shader|timeline|spring|geometry|particle|layout|scene|render|seed|lens|type|rhythm|sound|audio|flow|simulat|physical',v,re.I)]
    excerpt='\n'.join(selected) if selected else p
    lines.append(f"[{x['slug']}] {x['category']} partial={x['prompt_partial']} original_chars={len(p)}\n{excerpt[:1800]}\n[excerpt end; full prompt retained in catalogue]\n")
(root/'read-long.txt').write_text('\n'.join(lines),encoding='utf-8')
(root/'checkpoint.md').write_text('''# 方法论吸收 checkpoint
目标：广泛覆盖513条资料，提炼导演/摄影/美术/动作方法与代码实现关系；本轮不制作样片。
已完成：读取现有skill/图库/既有源码研究，生成去重短文本与长文本研究摘录。
待完成：阅读分类材料，增加机制卡与需求检索、证据分级、制作质量对标，接入skill并验证。
约束：原作代码来源未知不得标为已证实；重制标签只作线索；本项目9:16竖屏1080×1920，保留历史横版。
''',encoding='utf-8')
print({k:len(v) for k,v in groups.items()},'long',len(long),'unique',len(seen))
