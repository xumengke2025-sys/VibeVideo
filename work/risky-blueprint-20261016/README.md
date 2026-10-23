# Risky 风险视角 · V3

80 秒，1920×1080，16:9，30 fps。代码绘制的二维机械蓝图、浅挤出和连续纸面摄影；原创程序合成配乐与机械音效，无旁白。

## 使用与交付

- 成片：`out/video-v3-final/video.mp4`；`v3-full` 为修复前审核留档。
- 正式效果图：`out/stills-v3-delivery-concept/60.png`。
- 可编辑源码：`v3/scene-body.js`；基础绘制：`v3/primitives.js.txt`；合成后的运行入口：`v3/film.js`。
- 时间线与字幕：`build-v3.mjs`，构建后得到 `v3/plan.json`。
- 音乐源码：`v3/make_audio.py`；混音及独立音轨：`v3/audio/`。
- 工程检查：成片目录的 `evidence.json`、`ffprobe.json`、`config.json`；静帧目录的 `checks.json` 记录重复定位一致性。审核范围见 `qa/`。

## 本机重新生成

从项目根目录运行：

```powershell
D:\docker\node.exe build-v3.mjs
D:\docker\node.exe v3/render.mjs --mode=stills --version=my-concept --times=60 --concept=1
D:\docker\node.exe v3/render.mjs --mode=video --version=my-render
```

改动源码后使用新的 `--version`，渲染器拒绝混用旧输入帧。默认完整渲染 80 秒；局部预演可使用 `--start=40 --duration=22 --width=960`。

其他机器需要 Node.js、Playwright Core、Chrome、FFmpeg/FFprobe。设置 `RISKY_PLAYWRIGHT` 为 playwright-core 的 index.mjs 绝对路径、`RISKY_CHROME` 为浏览器路径、`RISKY_FFMPEG` 为 ffmpeg.exe 路径（ffprobe.exe 放在同目录）。现有默认值为制作工作区的安装位置。配乐重建另需 Python 3、numpy，并按本机安装位置配置 make_audio.py 中 FF 路径。已有 WAV 可直接渲染，无需重建。

内部播放器需要 HTTP 服务，例如在 v3 目录运行 `python -m http.server 8080`，访问 http://localhost:8080 。它是源码预览工具；MP4 是主要交付。

## 内容与实现边界

最终版完成工程检查。一轮独立审核在修复前查看全2400帧连续图集，发现并修复返回镜头出画；同一审片者对最终版61–68秒210帧做了局部复核，问题已解决。正常速度观看和实际听音未完成，因此不宣称完整视听验收通过。报告在 `qa/v3-final/`，保留修复前记录。

合成企业 A、案件 A-001、快照 S-001 用于说明流程。三种情景曲线由动画代码构造，不是 Risky 引擎实际运行结果，不表示概率、评级或损失估计。Risky 业务源码只读，未修改、未宣称完成其运行验收。

V3 沿用 FirmBuddy V10 实际绘制原语与纸面摄影路线。V2 生成图为已放弃的探索，不属于成片实现承诺。保留 V1、V2 历史材料，不混入当前交付源码。

## 来源与许可

上游蓝图绘制参考：lemomo-ai/lemo-opuscar，commit `e3cb16f63768c68693ff0e15171d6e755457cc32`；使用经过本地 FirmBuddy V10 整合的 draw.js / paper.js，原许可保留在 `v3/vendor/LICENSE-Lemo`。Risky 场景、时间线、路径、配乐由本项目源码生成。详情见 `evidence/SOURCES.md`。
