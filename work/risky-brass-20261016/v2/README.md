# Risky 风险视角 · 黄铜机械完整版

成片：`Risky-黄铜机械-完整版.mp4`，80秒、1920×1080、30fps、H264/AAC。

`scene.js` 为实际三维场景、文字和可寻址时间轴；`window.renderAt(seconds)` 在0至80秒确定性求值。`index.html` 仅是内部绘制入口，正式交付为MP4。

`render.cjs` 使用Chrome/Playwright逐帧导出；`make_audio.py` 生成原创合成音乐和接触拟音；`finalize.py` 合成并检查完整视频。`BRIEF.md` 保存完整镜头表，`../BUSINESS-MAPPING.md` 保存实际产品来源与机械解释的对应关系。

在本机PowerShell重新导出：

```powershell
& 'D:/docker/node.exe' './render.cjs' --mode=render --duration=80 --output=risky-full-silent.mp4
& 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' './make_audio.py'
& 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' './finalize.py'
```

运行时路径在render.cjs和finalize.py顶部，可按实际安装调整。Three模块与素材随vendor、assets保留，来源/许可继承assets内清单。重编整套场景可运行build_full.py（读取保留的v1场景）；通常直接编辑scene.js即可。

内容为合成A17案例及机制示意，没有调用Risky业务引擎，不是实际预测或真实新闻。无中文旁白；声音为数学合成器乐，非声学乐器录音。音轨解码和电平检查不代表实际听审。

旧版v1样段保留。审核覆盖、媒体哈希及剩余限制记录于qa和上级CHECKPOINT.md。
