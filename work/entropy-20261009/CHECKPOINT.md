# 检查点 — 熵增 66 秒中文科普动画《熵增：为什么“混乱”更容易出现？》

## 需求
用户点题：约 60 秒中文科普动画，面向无统计物理基础的观众，说清“接近均匀分布的宏观状态对应更多微观排列，因此更容易被观察到；熵增是统计结论”。规格由用户逐条明确：1920×1080、30fps；深蓝黑底、米白线条、青色粒子、暖黄强调；编号全程可辨；中线先为可移除隔板（暖黄）后为虚线统计边界；柱状图纵轴从 0 开始、高度与真实计数成比例；画面文字尽量少。
时长说明：旁白实测 56.47s，为不加速、按自然语速排布，整片延长至 66.0s 并在此声明（用户允许适度延长并说明）。

## 能力边界（用户明示）
不能直接生成图片；粒子、容器、计数阵列（8 格归属编码）、柱图与文字全部用 Canvas 2D 代码绘制，零外部素材、零生成图像。渲染链：playwright-core 逐帧截图 + ffmpeg 编码。

## 科学模型（全部运行时计算，无硬编码数值）
- 8 个可区分粒子、只记录左右归属；总排列 2^8 = 256；C(8,k) = 1, 8, 28, 56, 70, 56, 28, 8, 1。
- 4:4 = 70 种 ≈ 27.3%（明确不占多数）；近均匀 k=3,4,5 = 182 种 ≈ 71.1%；“全部在左”= 1 种、“全部在任意一侧”合计 = 2 种（两者严格区分）。
- 禁区遵守：未称 256 为位置/速度总数；未称排列数是运动路线；未把熵定为“视觉乱不乱”；未称 4:4 占绝大多数；随机轨迹非单调上升（含回落与波动）；画面注明“对称随机模型 · 非真实气体轨迹”；不虚构音频；不称“熵每时每刻在任何系统只能增加”（片尾改为“统计意义 / 局部熵降低可伴随环境熵增加”）。
- A/B 排列：A = 左{1,2,3,4}（枚举索引 0），B = 左{1,3,5,7}（索引 20），由独立脚本 verify_counts.py 复算一致。

## 六段结构（契约 shots；旁白与字幕同源）
S1 0–8.5s 提出矛盾（八粒子全在左、隔板移除、一个粒子反向返回又被强调）→ S2 8.5–18.9s 两个尺度（同一 4:4 下成员 A→B 切换，计数恒定；“微观：具体是谁 / 宏观：左右各几个”）→ S3 18.9–31.2s 排列数量（8:0 一行 vs 4:4 七十行 8 格归属编码，互不重复）→ S4 31.2–43.4s 概率分布（9 柱按真实计数升起→突出两端各 1 种→中心 70/256≈27.3%→近均匀三组合并 182/256≈71.1%）→ S5 43.4–55.4s 统计含义（固定种子对称随机模型、每步等概率翻转一个粒子、三条 8 步短轨迹、极端值标记环随步显示）→ S6 55.4–66.0s 纠误收尾（保留迷你分布与 S = k_B ln Ω，停留结论句“更容易出现，因为对应的微观排列更多。”）。

## 旁白与字幕全文（entropy.srt 同源导出）
1. 粒子可以向右走，也可以向左走。那为什么，它们散开以后，却很少全部回到一边？
2. 我们用八个可区分的粒子，只记录它们在哪一侧。同样是左四、右四，具体是哪四个，可以完全不同。
3. 全部在左，只有一种归属排列。但左右各四，有七十种。宏观看起来一样，背后能对应的微观排列，却多得多。
4. 如果这些归属排列等可能，接近均匀的状态，就占了大多数。不过，恰好四比四只占百分之二十七左右。平衡附近，仍然会有波动。
5. 这里的规则没有偏爱左右，但从少见的集中状态出发，系统更容易进入排列更多的状态。它仍会波动，也并非绝不能回去。
6. 熵不只是看起来乱不乱。粒子数量巨大时，整体回到集中状态的机会极小，这就是熵增的统计含义。

## 制作链
`timeline.mjs`（事件时间轴/字幕窗口/C(n,k) 核算）→ `clips/entropy.json`（24 事件、6 镜头、6 字幕、6 旁白、随机游走参数）→ `film.mjs`（Canvas 绘制引擎，全部状态为时间的纯函数）→ `render.mjs`（确定性逐帧渲染 1980 帧 + seek 三重一致性校验）→ `make_narration.py`（edge-tts 合成旁白）→ `score.py`（合成拟音 + 底噪床 + 旁白混音 + 两遍 loudnorm 混流）。

## 视觉迭代（静帧审 → 修复 → 复验）
- **5 秒片段先行**（members-5s）：A→B 成员切换、编号可读、计数不变、高亮节奏通过后才扩展全片。
- **全片 v1 审片发现三类问题**：① 长字幕溢出画布两侧被裁切（c3 49 字 ≈ 2058px > 1920px）；② S4 “70 种·单个最多”黄字压在米白柱上不可见、27.3% 与轴标签拥挤；③ S5 轨迹极端值空环在轨迹到达前提前显示（未发生的数据先亮相）。
- **修复**：字幕自动折行（>1700px 按中点标点断两行、避头尾）；S4 删压柱文字并将 27.3% 重定位；空环加时间条件随步显示。
- **r2 审片再发现**：S3→S4 转场存在 3 帧纯空档 + 硬切（其余转场均为交叉淡化）。
- **r3 修复与复验**：S3 淡出延至 31.2s、S4 自 30.6s 渐入、交叠 0.6s；转场帧 918/927/936 直接查看通过（30.9s 两者同屏交叠）。**42 张静帧 r2 与 r3 逐比特相同**——证明修复零回归、只影响过渡带。

## 声音
- 6 条中文旁白：edge-tts 合成音 zh-CN-YunxiNeural（+12%，声明于 narration.json），实测总长 56.47s，按实际时长排布，不加速。非真人录音、非克隆语音。
- 18 条合成音效事件（whoosh/tick/pluck/chime/sub）+ 全片底噪床；无音乐、无外部录音。
- 两遍 loudnorm（I=-16, TP=-1.5, LRA=11）→ 成片实测 60s 采样 peak −1.28 dBFS / RMS −17.21 dBFS；母版前峰值 −1.55 dBFS 无削波。

## 交付物与证据（out/entropy-r3/）
- 成片 `entropy.mp4`：1920×1080 / 30fps / 66.000s / 1980 帧 / h264 + AAC 48kHz 单声道；5.19 MB；SHA256 `eb305f373176476861518e702e5c90c70af417428ba870ff975dc13872e45e64`。
- 契约检查 check.mjs：24 事件 / 6 镜头 / 0 错误。
- 渲染确定性：seek 三重校验（顺序、逆序、新页面像素哈希两两一致）、0 页面错误（`render-evidence.json`）。
- 帧级审计 `frame-audit.json`：265 采样点（每 0.25s）左右记账一致（每帧恰 8 粒子）、3 条随机游走 Node 端独立复算一致、分镜状态抽检通过。
- 独立计数核验 `verify-counts-output.json`：256 / 70 / 182 / 27.34% / 71.09% / A=0 / B=20。
- 全解码 + 接触表 + 电平：`evidence/media-evidence.json`（technical_failures 空）。
- 汇总证据：`delivery-evidence.json`；审片静帧 42 张（still-*.png）。

## 重建命令（绝对路径）
```powershell
cd "d:\ai项目\ai动画\VibeVideo项目\work\entropy-20261009"
# 渲染（1980 帧，含 seek 校验；同源可断点续渲）
& "D:/docker/node.exe" render.mjs --clip=entropy --out=out/entropy-r3 "--ffmpeg=D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe" "--chrome=C:/Program Files/Google/Chrome/Application/chrome.exe" "--playwright=C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core/index.js"
# 声音与混流
& "C:/Users/67236/AppData/Local/Programs/Python/Python312/python.exe" score.py --clip=entropy --out=out/entropy-r3 "--ffmpeg=D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe"
# 验证
& "D:/docker/node.exe" verify_entropy.mjs "--chrome=C:/Program Files/Google/Chrome/Application/chrome.exe" "--playwright=C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core/index.js"
& "C:/Users/67236/AppData/Local/Programs/Python/Python312/python.exe" verify_counts.py
& "D:/docker/node.exe" check.mjs
```

## 验证边界
- 未实时播放观看、未实际听音；已完成逐帧图检（含静帧、转场邻域帧、编码后关键帧、接触表）、全解码校验与波形/响度分析——这些不能替代播放与听音。
- “更容易理解”为主观判断，由制作者评审给出；未见真实观众数据。
- 模型为粗粒化统计计数示意（8 粒子），非真实气体动力学；“对称随机模型 · 非真实气体轨迹”已上屏。
- out/entropy（v1）与 out/entropy-r2 为审片过程目录，保留作迭代痕迹；正式交付以 out/entropy-r3 为准。
