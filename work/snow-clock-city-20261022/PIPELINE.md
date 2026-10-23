# 雪山钟城制作流水线

`run-film.ps1` 默认只打印计划，不启动 Blender。使用项目便携 Blender 内置的独立 Python，无需系统 Python。画幅固定 1080×1920、24fps，整片 2160 帧 / 90 秒。AI 审核一轮尚需对当前成片另行实际执行；本入口只负责工程检查。

```powershell
.\run-film.ps1 plan -Version film-v2
.\run-film.ps1 build -Version film-v2
.\run-film.ps1 build-proof -Version film-v2
.\run-film.ps1 proof -Version film-v2 -Frames 1032,1104,1200,1320,1416,2064
.\run-film.ps1 sample -Version film-v2
.\run-film.ps1 full -Version film-v2
.\run-film.ps1 status -Version film-v2
```

`build` 调用 `film_world.py` 生成 `model/clock-city-production-v2.blend`；已有同名模型先保存在该输出版本的 `previous-model`。成功的 build 可按生成模型哈希跳过。渲染入口必须读取环境变量 `SNOW_MODEL`，或使用 v2 模型；流水线拒绝仍硬编码 v1 的旧 renderer。

`build-proof` 将建模与两张正式样帧串行执行，默认只渲染 1320（55秒）和 2064（86秒），可用 `-Frames` 覆盖。完成后即停止，供主制作实际看样帧；不自动启动关键样段或整片。

`proof` 默认为 16 张跨全片和装卸关键阶段的正式样帧，可指定零起算帧号。`sample` 为原片 43–60 秒：1032–1439 共 408 帧，音轨同样从 43 秒截取 17 秒。`full` 为 0–2159 共 2160 帧。

每个 Blender 都经过现有 `render_queue.py`：项目 GPU 串行，并等全机已有 Blender 退出。默认每进程 24 帧，可用 `-BatchSize 1` 至 `48` 调整；帧数不改变正式像素或 samples。已有 PNG 经完整 chunk CRC、尺寸及结尾检查后复用，损坏帧移入 `rejected`。失败立即退出，不自动循环重试；修复环境后以同一命令显式续渲。输入代码、模型或音轨发生变化时必须换 `-Version`，不能混用旧帧。`full` 自动复用同版本 `sample` / `proof` 中完整冻结 manifest 与当前完全相同且 PNG CRC 校验通过的帧，优先硬链接、失败则 `copy2`，来源保存在 `full/frame-provenance.json`。不跨版本或借用未核验目录。

`render/<Version>/frozen-manifest.json` 冻结当前源码、模型与音轨 SHA256，`source` 保存源码快照；每批前复核源码/音轨和模型大小及修改时间，结束时重核全部哈希。实际执行当前工作源码，期间变更会令该次工作失败；需要重建快照时使用新版本。渲染期间请勿继续编辑已冻结源码。`build-inputs.json` 另外冻结建模输入与环境模型缓存。输出 `status.json` 记录流水线/队列 PID、全机 Blender PID、阶段、帧进度和当前日志。中断启动器不会为了状态更新而杀死正在运行的 Blender；恢复时仍会排队等待旧任务。

样段和完整片写入 `delivery/<Version>`，以完整 imageio FFmpeg 编码 H.264/AAC，并将 `audio/final-mix.wav` 混入。结束后做 ffprobe 帧数、尺寸、时长、24fps 和 48kHz 双声道检查，再完整解码音视频；成功后原子替换正式 MP4，保留成片哈希、probe 和工程报告。工程报告明确标记未实际观看/听音，不把解码通过记作视听审核。

完整 FFmpeg 路径：`../firmbuddy-blueprint-20261012/tools/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe`。ffprobe 路径：`D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe`。便携 Blender 路径：`../../tools/blender-portable/blender-4.5.3-windows-x64/blender.exe`。移机须同时迁移这些依赖或调整入口常量；未宣称工程已脱离本机依赖。

本次继续制作补充：最终候选使用 `-Engine EEVEE -Samples 64`；EEVEE通过连续动画区间渲染复用GPU场景，`film_animation.at(seconds)` 不再自行设置场景帧。渲染入口负责帧号，frame_change_post负责绝对时间求值。模型构建链依次为 `film_world.py`（保留 production-v2）→ `optimize_production.py`（远景扫描树LOD，production-v3）→ `bake_static_geometry.py`（静态倒角缓存，production-v4）→ `finish_foreground.py`（封闭近景雪坡，production-v5）。角色骨架与机构父子层级保留。当前生产入口读取 production-v5，历史v2/v3/v4和样帧均保留。

注意：`-Version` 与 `-Engine`、`-Samples` 要保持一致才能续渲和复用；当前工作源码更改后需新版本。帧输出以0起算，Blender场景帧以1起算，二者通过渲染回调明确映射。
