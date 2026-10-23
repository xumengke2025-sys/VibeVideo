# FirmBuddy V4 · 把问题展开成行动

1920×1080横屏，30fps，68秒。三种独立输入：查商机、问业务、备拜访；记忆点为专业分工、知识有据、持续经营。所有业务资料与回答均标明流程示例。

## 预览

在源码包根目录启动任意静态HTTP服务，例如 `python -m http.server 8768`，浏览器打开 `http://localhost:8768/v4/index.html`。播放按钮控制画面与现成音轨，时间滑杆可定位任意时刻。不要直接双击HTML（模块与JSON需HTTP加载）。本项目内也可执行 `node server.mjs --serve`，访问同一路径。

低清预演地址可加 `?width=960`，会真实改变输出、墨线、声音效果层和字幕层的像素缓冲。完整视频使用1920×1080。

## 修改与导出

场景和动作在 `film.js`；镜头与旁白在 `plan.json`；共享绘图与纸面引擎在 `vendor/`。预览使用 `audio/mix.wav`，旁白、配乐和音效保留独立WAV。随机纸纹固定种子19，全部画面由绝对秒时钟计算；`window.renderAt(seconds)`可以寻址导出。

渲染需要Node.js、Chrome、playwright-core和FFmpeg/ffprobe。工程已使用已有依赖导出，源码包不包含浏览器与大型依赖。包外部署可在根目录安装 `npm install playwright-core`，通过环境变量指定二进制：

```powershell
$env:FIRMBUDDY_CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
$env:FIRMBUDDY_FFMPEG = 'C:/ffmpeg/bin/ffmpeg.exe'
$env:FIRMBUDDY_FFPROBE = 'C:/ffmpeg/bin/ffprobe.exe'
node v4/render.mjs --mode=final --version=my-edit
```

已有项目的路径自动回退到本项目依赖。导出代码会检查源文件签名，修改源文件后需采用新的version，避免混用旧帧。`--reuse=../out/sample-v4-execution`只在源码签名、分辨率和fps完全一致时复用样段。

配音为Windows SAPI的Microsoft Huihui离线合成，中文旁白中AI读作“人工智能”。开场作1.084倍时长适配，其余段未做速度压缩。配乐和音效为原创合成，未使用外部录音。需要重新配音时运行 `make_voice.ps1`，混音脚本需Python、numpy、imageio-ffmpeg。

## 参考与检查范围

绘图和纸面合成迁移自本项目归档Lemo blueprint，commit `e3cb16f63768c68693ff0e15171d6e755457cc32`；MIT许可在 `vendor/LICENSE-Lemo`。中文字体使用Windows现有Microsoft YaHei，不在源码包分发字体。四张用户截图作为会场、档案、商机卡和生命周期形态参考，保留在包内 `assets/reference/`。

本轮完成内部样段、代表帧、指定动作的采样序列检查及工程检查。此前独立审核预算已使用，本次没有新增独立审片；不声称逐帧完整视听验收通过，完整音轨尚未实际听音。
