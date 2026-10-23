from pathlib import Path
import shutil,json,hashlib
p=Path(__file__).parent
r=json.loads((p/'out/verification.json').read_text(encoding='utf-8'))
assert r['allPassed']
dest=p.parents[1]/'动画成品/宝宝和太阳的晚安-蜡笔绘本-v3.mp4'
shutil.copy2(p/'out/宝宝和太阳的晚安-v3.mp4',dest)
assert hashlib.sha256(dest.read_bytes()).hexdigest()==r['sha256']
r['deliveryCopy']=str(dest)
(p/'out/verification.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
j=json.loads((p/'assets/prompts.json').read_text(encoding='utf-8'))
j['savedOutputs']=[str(p/'assets'/f'head-{name}.png') for name in ['front','quarter','profile','yawn']]
(p/'assets/prompts.json').write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
(p/'CHECKPOINT.md').write_text(f"""# 宝宝绘本 v3 checkpoint

delivery_mode: user_feedback
aspect_ratio: 9:16
width: 1080
height: 1920

已完成：内置imagegen简化粗蜡笔透明头部（正面、右转、侧面、哈欠），左右肩、坐姿躯干和手掌朝向改造，固定骨长短胖身体和爬行，40秒共享连续速度时钟，音乐及拟音同步。保持无字家→院子→院外花园→日夜→回书页。
概念帧：out/still-0.00.png、out/still-4.00.png、out/still-32.20.png；坐姿已在会话展示。沿用连续执行授权。
提示词与素材：assets/prompts.json；四张RGBA素材均有真实透明区域。

交付：{dest}
源码：{p}
SHA256：{r['sha256']}

基本工程检查全部通过：完整视频/音频解码、1080×1920、24fps、40秒、960帧、H.264/AAC立体声48kHz；交付副本哈希相同。

制作观察：代表帧、2—6.75秒20个连续时间采样；源码/素材哈希已记录。未作独立审片、全帧审核或完整音轨听审；沿用用户选定直接生成模式。

下一步：用户观看并反馈画风、相似度、头部与手臂动作。v1/v2完整保留，无其他项目自动恢复。
""",encoding='utf-8')
print(dest)
