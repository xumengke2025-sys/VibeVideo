# FirmBuddy V19 · 机械减负工作流

120秒 / 1920×1080 / 30fps / 纯音乐无配音。

保留工程蓝图纸张、原式阶梯专家座谈、系统九类专家、同一家A01半导体衬底企业与知识库分类。用滚轮归集、专家多路接力、丝杠定位、知识抽屉、连杆压头、人工开闸与记录回流解释业务减负；取消长段说明与上下双字幕。无虚构绩效数值，机构是解释性隐喻。

```text
python v19/setup.py
node server.mjs --serve
```

访问 http://localhost:8768/v19/index.html 。任意时间寻址，支持乱序渲染。

```text
python v19/make_audio.py
node v19/render.mjs --mode=final --version=v19-mechanical-relief --duration=120 --fps=30 --width=1920
```

依赖Node、Python（numpy、Pillow、imageio-ffmpeg）、Chrome、Playwright Core、FFmpeg/ffprobe。FIRMBUDDY_PLAYWRIGHT、FIRMBUDDY_CHROME、FIRMBUDDY_FFMPEG、FIRMBUDDY_FFPROBE可指定运行时位置，render.mjs保留原工程默认路径。

helpers.js / geometry.js：原Lemo制图引擎的适配与原版基础机构。mechanisms.js：七站机构与持续客户档案。conductor.js：连续相机、任意时间求值及预览。plan.json：业务含义、共享动作/声音锚点。film.js由setup.py生成。

实际检查范围、成片哈希与限制见CHECKPOINT、交付evidence。沿用本片历史已使用的审核预算，没有新开独立审片。完整解码、音乐对齐、静帧和连续抽样分别记录，不代替完整正常速度观看与听音。
