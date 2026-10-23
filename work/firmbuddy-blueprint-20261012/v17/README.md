# FirmBuddy V17

1920×1080，30fps，124秒，纯音乐。根据用户反馈统一工程蓝图风格，细化业务痛点及来源抽卡，重建贴近原图的阶梯专家座谈。

在父目录运行：

```text
python v17/setup.py
node server.mjs --serve
```

预览 `http://localhost:8768/v17/index.html`。

```text
node v17/render.mjs --mode=final --version=v17-blueprint-sources --duration=124 --fps=30 --width=1920
```

可设置 `FIRMBUDDY_PLAYWRIGHT`、`FIRMBUDDY_CHROME`、`FIRMBUDDY_FFMPEG`、`FIRMBUDDY_FFPROBE` 指向本机依赖。默认使用本项目已有 Playwright、Chrome 与 FFmpeg。

活跃绘制源码：`helpers.js`、`opening.js`、`scene-body.js`、`hall.js`、`story.js`。`setup.py` 将 hall.js 同步到 scene-body.js 后生成 film.js。`plan.json` 管理镜头、业务字幕和音乐事件。修改配乐后运行 `make_audio.py`。所有时间均可直接寻址，无墙上时钟随机状态。

`assets/expert-hall-reference.png` 为用户提供的原始座谈参考，仅用作结构参考。画面使用线几何、专业字体和程序纸纹重新绘制。九大业务目录与专家名来自 FirmBuddy 工程，业务来源记录在 content-evidence.json。

历史成片与产品工程未修改。one-time revise.py / prepare_checks.py 为本轮迁移记录，不是运行入口。使用已有一轮审核预算，未新增独立审核；实际检查范围见 CHECKPOINT.md 和成片 delivery-checks.json。
