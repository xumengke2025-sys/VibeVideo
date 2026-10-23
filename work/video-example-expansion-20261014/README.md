# 成套参考扩展 · 2026-10-14

本轮新增下载21个作者效果视频，统一目录加入22个条目（另1个复用已有三维预告），总计98个视频与源码条目。保留作者原片，没有把本地重制冒充原作。

入口：[播放、搜索与源码目录](../github-reference-expansion-20261011/index.html)。运行项目根目录 `npm run preview:references` 后访问 `http://127.0.0.1:8176/work/github-reference-expansion-20261011/index.html`。

- Shotcraft：20段产品运镜、连续布局、CSS空间摄影、数据叙事镜头样段，Apache-2.0代码/文档，音频素材许可分别保留。
- [Chaoqi31/opus-paints](https://github.com/Chaoqi31/opus-paints)：59.6秒《The Claude Glass》作者解释片及完整257文件工程。代码MIT，画作/墙面/影片CC BY 4.0。引用署名按plates/LICENSE：The Claude Glass, works by Claude (Opus 5.5), https://github.com/Chaoqi31/opus-paints。
- [ishuagrawal/particle-beach](https://github.com/ishuagrawal/particle-beach)：复用已有60秒Three三维预告及完整cinematic runtime，MIT。

技能调用：`node skill/vibe-video/scripts/video_examples.mjs search --query "数据叙事"`，`card shotcraft/mosaic-reframe`或`card opus-paints/_timeline`返回准确本地视频、绘制入口、许可及证据。搬迁项目可指定 `--root`。

新增来源及筛选记录：`reference-sources/video-examples-20261014/manifest.json`。固定源码、原许可、Git blob及SHA256分别保留；Shotcraft用已有固定源码快照，实际预览下载URL和源码入口哈希在每个MP4旁的.source.json。

工程验证与边界见[检查点](CHECKPOINT.md)和[验证](verification.json)。仅做解码、入口和浏览器功能检查，没有把它们写成全片动态/听音通过。上游制作方式与模型属于作者声明；不继承其固定模型、音乐先行、审片轮数或推广要求。

实施脚本：discover.mjs保存候选版本/许可，acquire.mjs保存固定工程与作者媒体，verify-media.mjs记录解码和封面，build-skill-index.mjs构建技能索引，final-verification.mjs验证旧目录保留、检索、同步及HTTP入口。update-catalog.mjs是一次性改造脚本，已执行，不应重复应用。
