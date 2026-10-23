# FirmBuddy V18 · 从业务问题走到客户行动

154秒，1920×1080，30fps，H264/AAC，纯音乐无配音。

保留V17原机器、来源抽卡、专家座谈与产业研究。新增客户经理任务开场、业务代价、同一A01档案的三联成果页、停转齿轮闭合的首尾呼应。叙事依据用户提供的《AI创新大赛_叙事与演讲》，没有使用其中的教学模拟数字。用户明确暂不提供试点数据，本片通过具体成果展示流程价值，不呈现量化提效或已部署范围。

在源码包根目录运行：

```text
python v18/setup.py
node server.mjs --serve
```

访问 http://localhost:8768/v18/index.html 。源码支持任意时间寻址。

```text
python v18/make_audio.py
node v18/render.mjs --mode=final --version=v18-business-story --duration=154 --fps=30 --width=1920
```

依赖：Node、Python（numpy、Pillow、imageio-ffmpeg）、Chrome、Playwright Core、FFmpeg/ffprobe。可通过 FIRMBUDDY_PLAYWRIGHT、FIRMBUDDY_CHROME、FIRMBUDDY_FFMPEG、FIRMBUDDY_FFPROBE 设置本机路径；默认沿用原工程的本地依赖。

绘制源：helpers.js、opening.js、scene-body.js、hall.js、story.js、narrative.js、conductor.js；plan.json 管理字幕、时序与音乐事件。setup.py 同步专家厅并生成 film.js，不直接编辑 film.js。prepare_v18.py 与 prepare_checks.py 是迁移记录，正常重建无需执行。

时钟：实际播放时间为 realTime；原机器保持 filmTime=realTime-6。plan 的 start/end 和字幕/音乐事件均为实际时间；继承站点 reads 文本中18–38秒的数字保留V17基准，对应本版+6秒。

世界坐标、纸张与线条由固定版 Lemo blueprint 引擎实现，来源及许可保留于 vendor 和 source-transfer.json。专家厅与产业图谱参考图保留在 assets。

继承现有交付模式和已使用的审核预算，本次无新增独立审片。工程检查、实际查看范围与限制记录于 CHECKPOINT 和交付 evidence 文件；不把解码成功或音量分析等同于完整视听审核。
