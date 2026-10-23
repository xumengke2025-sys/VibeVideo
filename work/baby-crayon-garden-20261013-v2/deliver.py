from pathlib import Path
import shutil,json,hashlib
p=Path(__file__).parent
r=json.loads((p/'out/verification.json').read_text(encoding='utf-8'))
assert r['allPassed']
dest=p.parents[1]/'动画成品/宝宝和太阳的晚安-蜡笔绘本-v2.mp4'
shutil.copy2(p/'out/宝宝和太阳的晚安-v2.mp4',dest)
assert hashlib.sha256(dest.read_bytes()).hexdigest()==r['sha256']
r['deliveryCopy']=str(dest)
(p/'out/verification.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
j=json.loads((p/'assets/prompts.json').read_text(encoding='utf-8'))
j['savedOutputs']=[str(p/'assets'/f'head-{name}.png') for name in ['smile','blink','yawn']]
(p/'assets/prompts.json').write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
(p/'CHECKPOINT.md').write_text(f"""# 宝宝绘本 v2 checkpoint

delivery_mode: user_feedback

已完成：照片参照的内置imagegen透明头部（闭嘴、眨眼、哈欠），固定骨长短胖身体和爬行，40秒共享连续速度时钟，音乐及拟音同步。保持无字家→院子→院外花园→日夜→回书页。

交付：{dest}
源码：{p}
SHA256：{r['sha256']}

基本工程检查全部通过：完整视频/音频解码、1080×1920、24fps、40秒、960帧、H.264/AAC立体声48kHz；交付副本哈希相同。

制作观察：代表帧、2—6.75秒20个连续时间采样；IK骨长和时间单调性检查。未作独立审片、全帧审核或完整音轨听审；沿用用户选定直接生成模式。

下一步：用户观看并反馈相似度、动作和节奏。v1完整保留，无其他项目自动恢复。
""",encoding='utf-8')
print(dest)
