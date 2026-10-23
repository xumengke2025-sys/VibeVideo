# FirmBuddy V11 · 商机痛点与抽卡入机

60秒 / 1920×1080 / 30fps / H264+AAC / 纯音乐。

源码：`intro.js` 为新增痛点、五张独立场景卡、抽卡和载纸交接；`scene-body.js` 保留原机械世界；`film.js` 是合并后的实际入口。修改后运行 `python v11/setup.py`，保留plan/音乐。

从压缩包根目录运行（需Node、Python/numpy、Chrome及playwright-core）：

```powershell
python v11/setup.py
python v11/make_opening_audio.py
$env:FIRMBUDDY_PLAYWRIGHT='C:/absolute/path/to/playwright-core/index.mjs'
$env:FIRMBUDDY_FFMPEG='C:/absolute/path/to/ffmpeg.exe'
$env:FIRMBUDDY_FFPROBE='C:/absolute/path/to/ffprobe.exe'
node v11/render.mjs --mode=final --version=my-v11 --duration=60 --width=1920 --fps=30
```

也可运行`node server.mjs --serve`后打开`http://127.0.0.1:8768/v11/index.html`交互预览。默认本机路径仅是本项目现有配置，可通过以上环境变量替换。

配乐：`audio/retained-v10.wav`为原片原创52秒纯音乐；新增开头8秒150BPM，原主体52秒在第8秒开始，旧动作音点统一后移8秒。`make_opening_audio.py`是可重建的最终混音来源，其他保留分轨为历史素材，非60秒最终分轨。

视频时间：0–4痛点；4–8多场景抽卡；8–11卡片图纸化入机；11–60沿用原片后续。开头表达商机查询，股东减持只是选择的业务示例。正式九分类、专家会场、知识装备和AI作用保留。

制作：已用最终代码输出概念帧、6–12秒正式品质样段后导出整片。工程检查与实际观察分开记录。沿用历史一次审核预算，本轮无新增独立审核，不声称完整实际听音。

参考：用户截图仅用于卡牌形式和空间关系，不采纳截图公司、动态数字作为事实；原蓝图引擎固定来源与许可见`source-transfer.json`与`vendor`。
