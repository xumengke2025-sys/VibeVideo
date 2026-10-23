# FirmBuddy V6 · 连续机械蓝图

52 秒，1920×1080，30 fps。入口 `index.html`；确定性绘制 `film.js`。

依据已确认的七阶段概念，重建同一张图纸上的独立代码部件：三入口、筛选传动、四排阶梯专家会场、六类资料仓、成果滑台、确认锁扣和外围反馈轨道。概念图不作为平移或切换背景使用。

九业务席区沿用 FirmBuddy 系统分类；产业链洞察、财务诊断、拜访策略是参与会商的个别专家名。知识库预先装配，运行时在可见范围内检索；扩产披露仅为待核实线索。用户确认控制任务创建，实际用户记录再进入反馈。成果按需生成。

摄影采用一条绝对时间轨迹：五次 Hermite 插值，连接处共享速度、加速度为零，缩放在对数空间中进行。停机对应阅读窗口；其他过渡经长导轨和弧形支路承接。纸纹固定在世界坐标。

## 复现

在本工程根目录运行 `node server.mjs --serve`，浏览器访问 `http://127.0.0.1:8768/v6/index.html`。Node 需可导入 playwright-core，Chrome 默认使用本机已安装版本。`render.mjs` 支持环境变量 FIRMBUDDY_PLAYWRIGHT、FIRMBUDDY_CHROME、FIRMBUDDY_FFMPEG、FIRMBUDDY_FFPROBE。

正式导出：`node v6/render.mjs --mode=final --version=v6-final-build --width=1920 --fps=30`。

`scene-body.js` 是主体可编辑来源；`setup.py` 将 V5 的基础制图辅助函数与主体合为 `film.js`，并生成计划。正式入口直接使用 `film.js`，无需先运行 setup。重新运行 setup 不会生成配音；改旁白后依次执行 `make_voice.ps1`、`make_audio.py`。已提供最终混音和分轨。

渲染保持串行。真实低清预演可传 `--width=960`，会降低全部像素缓冲。工具不控制或结束其他项目进程。

## 来源与检查边界

依据本项目 `skill/vibe-video/SKILL.md` v0.15.0。制图引擎及蓝图材料参考 Lemo blueprint，固定 commit `e3cb16f63768c68693ff0e15171d6e755457cc32`，许可见 `vendor/LICENSE-Lemo`；原作相机硬切未沿用。原始系统截图和生成概念仅作为形态与内容依据。

本版是用户反馈修改，沿用 `delivery_mode: ai_review_once` 已用审核预算，没有新增独立审片角色。工程检查和主制作抽样观察范围见交付 evidence/observations；数值连续不等于全片感知审核。离线 SAPI Huihui 旁白与原创合成配乐、音效；没有声称完整实际听音通过。
