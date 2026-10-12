# 原创数据能力片段

入口：[style-studio](../../../assets/style-studio/)，时间轴 `clips/dataviz-proof.json`，绘制函数 `dataviz(t)`。10 秒：八个演示值落定 → 折线沿点生长 → 标注最大值 → 点向零基线延伸成柱 → 同一数值关系落定。

数据为 `[18,28,22,47,39,64,74,62]`，显著标明无现实统计含义；坐标、顺序、基线与最大值保持一致。没有科学/商业结论，也没有任意轮廓 morph。

```text
node check.mjs
node render.mjs --clip=dataviz-proof --out=out/dataviz-proof --chrome=/path/to/chrome --ffmpeg=/path/to/ffmpeg
python score.py --clip=dataviz-proof --out=out/dataviz-proof --ffmpeg=/path/to/ffmpeg
```

依赖、外部模块参数、输出隔离同 [蓝图重建](../blueprint/DEMO.md)。使用新值时先确认范围和纵轴，再渲染检查标注、极值和留白；不沿用示例中硬编码的极值标注。验证状态见共享 `capabilities.json`。
