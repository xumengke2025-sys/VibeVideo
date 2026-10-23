# FirmBuddy V12 · 原视频业务表达增强版

60秒 / 1920×1080 / 30fps / H264+AAC / 纯音乐。

本版基于V11原视频制作，保留原来的抽卡开场、机械世界、专家会场、知识仓、连续运镜与配乐。业务表达贯穿每个段落：资料分散与搜集慢、线索缺少切入点、跨领域专业支持、跟进准备重复及客户经营接续。

源码：`intro.js` 为开场与业务旁注；`scene-body.js` 为原机械世界及本轮局部材料动作；`film.js` 是合并后的实际入口；`plan.json` 为业务叙事与原声音时间轴。修改后运行 `python v12/setup.py`。

从压缩包根目录运行（需Node、Python/numpy、Chrome及playwright-core）：

```powershell
python v12/setup.py
python v12/make_audio.py
$env:FIRMBUDDY_PLAYWRIGHT='C:/absolute/path/to/playwright-core/index.mjs'
$env:FIRMBUDDY_FFMPEG='C:/absolute/path/to/ffmpeg.exe'
$env:FIRMBUDDY_FFPROBE='C:/absolute/path/to/ffprobe.exe'
node v12/render.mjs --mode=final --version=my-v12 --duration=60 --width=1920 --fps=30
```

也可运行`node server.mjs --serve`后打开`http://127.0.0.1:8768/v12/index.html`交互预览。默认本机路径仅是本项目现有配置，可通过以上环境变量替换。

配乐：`audio/base-v11.wav`为原视频60秒纯音乐；`make_audio.py`从此底轨添加7个轻量材料交接提示音，生成`audio/mix.wav`，无需旧版目录。开场保持150BPM，原主体音乐起点保持第8秒。`audio/timing.json`记录新增视觉动作与声音采样位置。旧`make_opening_audio.py`仅为历史制作记录。

视频时间：0–4业务痛点；4–11多场景抽卡入机；11–18资料归集与线索筛选；18–27需求、时机与切入点研判；27–37专业知识支撑；37–45跟进准备；45–53客户记录与持续经营；53–60整机价值呈现。商机查询是通用入口，减持仅为示例。九业务分类、六知识槽、专家专业培养与AI作用保留。

制作：正式代码效果图与12.8–20.8秒样段验证后输出整片。检查必要文字、相机连续性、寻址、完整解码、规格、音轨与AAC对齐。实际画面观察范围记录在成片目录`delivery-checks.json`；本轮不新增独立审核，不声称完整实际听音。

参考：用户截图仅用于卡牌形式和空间关系，不采纳截图公司、动态数字作为事实；原蓝图引擎固定来源与许可见`source-transfer.json`与`vendor`。
