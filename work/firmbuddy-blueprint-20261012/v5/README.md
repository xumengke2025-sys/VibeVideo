# FirmBuddy V5 · 机械行动蓝图

52秒，1920×1080横屏，30fps，H264/AAC。三个独立入口：查商机、问业务、备拜访；专业齿轮解释协作，剖切资料仓解释知识引用，导轨滑块把缺项变成提问。结尾为六类业务端口与工程标题栏，没有上市前／中／后矩阵。

本目录独立于V4及产品应用。所有业务记录为流程示例；专家数量与知识范围参见根目录product-reassessment-20261013.json。机械为产品机制的视觉比喻，非产品实时操作或物理仿真。

## 预览和编辑

从源码包根目录执行 `node server.mjs --serve`，打开 http://127.0.0.1:8768/v5/index.html 。原生浏览器Canvas/WebGL2，无需前端打包依赖。可用播放按钮及时间滑块，音轨已包含。

- `film.js`：世界几何、啮合齿轮、剖切、滑块、相机轨道、字幕。所有状态根据绝对秒数求值。
- `plan.json`：场景时长、旁白与产品边界。
- `vendor/draw.js`、`vendor/paper.js`：制图引擎及固定世界坐标的蓝晒纸纹。
- `audio/`：旁白分段、原创拨弦和机械音效、混音、字幕与实际时长。

## 渲染

已安装本机路径可直接执行 `node v5/render.mjs --mode=final --version=v5-final-build --duration=52`。迁移机器需安装 `playwright-core` 并提供Chrome及FFmpeg/ffprobe，支持以下环境变量：FIRMBUDDY_PLAYWRIGHT（index.mjs绝对路径）、FIRMBUDDY_CHROME、FIRMBUDDY_FFMPEG、FIRMBUDDY_FFPROBE。FFmpeg需支持libx264和AAC。修改源文件、计划或混音后使用新version，不能混用旧帧。

低清预演：`node v5/render.mjs --mode=preview --version=custom-preview --width=960 --fps=12 --duration=52`；真实960×540像素缓冲。

旁白重新生成：Windows PowerShell执行v5/make_voice.ps1，使用中文SAPI Huihui。随后Python（numpy、imageio-ffmpeg）运行v5/make_audio.py；可自行替换分段voice WAV。包装交付已包含最终音轨，不必重做旁白。

## 来源与验证范围

沿用项目vibe-video技能；Lemo blueprint参考commit e3cb16f63768c68693ff0e15171d6e755457cc32，保留vendor/LICENSE-Lemo。迁移范围见source-transfer.json和根REVISION-V5.md。分段特写、传动追踪、剖切、爆炸偏移和标题栏收束按FirmBuddy内容重新编排；没有复制捕云剧情或人物。

完整MP4做全量视频/音频解码、尺寸、帧数、时长和AAC音轨检查。131个文字阅读时刻检查安全区与字幕交叠；代表帧、核心连续窗由主制作角色实际观察。不是新一轮独立审核，旧独立审核结论不自动覆盖V5；未完成完整实际听音。详见out/final-v5-final-build/delivery-checks.json。
