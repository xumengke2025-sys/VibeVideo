# 长长巴士的相遇谜案

儿童数学讲解动画，竖屏1080×1920，24fps，当前版本30秒。仅原创趣味音乐，无旁白。当前交付方式：直接生成，由用户反馈修改。

- 当前成片：`out/bus-math-story-30s-v2.mp4`，修正物品缩放、人物动作和转场。旧30秒版与152秒版保留。
- 动画：`scene-stable.cjs`，复用`scene.cjs`的巴士与已认可五官；可寻址 `renderAt(seconds, timeline)`，SVG图层、Sharp栅格化、FFmpeg编码。修订原因见`motion-fix-record.md`。
- 文案与配乐：`make-music-only.py` 生成 `timeline.json`、`captions.srt`、`audio/music-only.wav`，配乐源自本地原创合成。
- 30秒版准备：`python make-short.py`，生成 `timeline-short.json` 与 `audio/music-only-30s.wav`。保留全题条件与核心算式，动作加速示意。
- 当前输出：`node render.cjs --plan timeline-short.json --scene scene-stable.cjs --out out/bus-math-story-30s-v2.mp4`。
- 工程检查：`node verify-output.cjs --v2`，结果 `verification-30s-v2.json`。
- 参考阅读、来源和范围见 `reference-study/README.md`；沿用用户认可的 `concept-v2.png` 的暖绘本、黄巴士、蓝甲和珊瑚乙，五官以代码重新绘制便于动画。

计算：车速5米/秒；甲速5−15÷6＝2.5米/秒；乙速15÷2−5＝2.5米/秒。车尾离甲后32秒车尾离乙，车尾从起点走160米、甲走80米，剩80米。两人每秒合拢5米，80÷5＝16秒。

历史含旁白素材、旧样段和旧字幕保留，成片仅引用 `audio/music-only.wav`。
