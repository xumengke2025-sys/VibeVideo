# FirmBuddy V16：同一个客户案例

104秒 / 1920×1080 / 30fps / H264 + AAC立体声 / 纯音乐无配音。

影片在原版V11/V13的机械蓝图框架上继续制作。同一个A01示例客户档案贯穿：商机查询、资料归集、股东服务研判、专家会商、半导体产业研究、知识依据、沟通准备和经营接续。

## 可编辑源

- `helpers.js`：原机械绘图函数。
- `intro.js`：原版抽卡、痛点开场及业务说明。
- `scene-body.js`：原版机械世界、会场、知识仓、输出与反馈。
- `story.js`：本轮时间映射、业务研判工位、产业图谱、同一案例连续运镜。
- `plan.json`：104秒时间轴、主要文字和配乐事件。
- `make_audio.py`：原创合成音乐与机械声，无语音素材。
- `vendor/`：原Lemo绘图与纸张合成器及原有许可。
- `assets/industry-roundtable-reference.png`：用户提供的会商图谱参考。

`setup.py`只拼接上述源文件，不重置计划或音乐。`film.js`是构建输出，不建议直接改动。

## 运行与重建

需要Node.js、Chrome、Python（numpy、Pillow、imageio-ffmpeg）、Playwright Core、FFmpeg与FFprobe。原工作区已有运行环境。独立使用可在v16安装`npm install playwright-core`，并把Chrome、FFmpeg、FFprobe绝对路径分别设置为`FIRMBUDDY_CHROME`、`FIRMBUDDY_FFMPEG`、`FIRMBUDDY_FFPROBE`环境变量。

在交付包根目录运行：

```text
python v16/setup.py
python v16/make_audio.py
node server.mjs --serve
```

浏览器打开 `http://127.0.0.1:8768/v16/index.html`。

正式渲染（有源码改动时使用新的version名称）：

```text
node v16/render.mjs --mode=final --version=custom --duration=104 --fps=30 --width=1920
```

关键样段和检查：

```text
node v16/check_motion.mjs
node v16/check_layout.mjs
node v16/render.mjs --mode=sample --version=custom --start=58 --duration=20 --fps=30 --width=1920
```

出图按绝对时间计算，支持任意时间寻址；配乐与最终视频均104秒。源资料全部是流程示例，不代表真实企业业务判断。产品FirmBuddy源码未改动。

## 检查范围

交付时保存布局、运镜、媒体解码、规格、AAC音频对齐及实际查看的代表帧记录。不把数值检查表述为完整听音或独立审片。当前交付模式沿用历史ai_review_once，历史预算已用，本轮无新增独立角色。
