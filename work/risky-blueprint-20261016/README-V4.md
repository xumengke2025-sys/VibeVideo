# Risky 风险视角 · V4

80 秒，1920×1080，16:9，30 fps。完整 MP4：`out/video-v4-final/video.mp4`。整体效果图：`out/stills-v4-final-overall/60.png`；阶段图：`out/stills-v4-final-look/`。

本版按用户反馈重做运动与音乐：相机共享端点速度、连续绘图、三次时间采样；120 BPM 原创音乐与机械接触声共用动作事件表。唯一主案件 A-001 贯穿全片，三组接收同源快照 S-001 的试验副本，三份条件记录归回原案件。

## 编辑与重建

权威场景源文件为 `v4/scene-body.js`；绘制原语为 `v4/primitives.js.txt`；时间线和事件表在 `build-v4.mjs`。构建产物为 `v4/film.js` 与 `v4/plan.json`。配乐源文件为 `v4/make_audio.py`，混音与分轨在 `v4/audio/`。

从解压后的工程根目录执行：

```powershell
node build-v4.mjs
node v4/render.mjs --mode=stills --version=new-concept --times=60 --concept=1
node v4/render.mjs --mode=video --version=new-render --shutter=1
```

修改输入后必须使用新的 version。局部预演可加 `--start=46 --duration=22 --width=960`。正式输出默认 1920×1080、80秒、30fps。

需要 Node.js、Playwright Core、Chrome、FFmpeg/FFprobe。跨机器设置 `RISKY_PLAYWRIGHT` 为 playwright-core/index.mjs 绝对路径、`RISKY_CHROME` 为 Chrome 路径、`RISKY_FFMPEG` 为 ffmpeg.exe 路径（同目录放 ffprobe.exe）。默认安装路径属于制作工作区。重新合成配乐需要 Python 3、numpy，并调整 make_audio.py 的 FF 路径；交付 WAV 可直接参与渲染。内部预览可在 v4 目录启动 `python -m http.server 8080` 后访问 localhost:8080。

## 验证与表达边界

工程证据在成片目录的 evidence.json、ffprobe.json、config.json；静帧 checks.json 记录运行错误和重复定位一致性；qa/v4 保存运动测量与本次制作检查范围。V3 的一次独立审核预算已经结束，V4 是主制作角色依用户反馈修改，并未新增独立审片。实际听音和正常速度观看未完成，不宣称完整视听验收。

三种情景曲线均为合成机制示意，不是 Risky 引擎运行结果，不表示概率、评级或损失估计。Risky 业务源码只读。本片保留二维蓝图、浅挤出与纸面摄影的现有能力边界。

## 来源与许可

蓝图绘制参考 lemomo-ai/lemo-opuscar，commit `e3cb16f63768c68693ff0e15171d6e755457cc32`，经本地 FirmBuddy V10 整合；许可见 `v4/vendor/LICENSE-Lemo`。事实来源见 `evidence/SOURCES.md`。场景、时间线与原创程序合成音乐均附源码。
