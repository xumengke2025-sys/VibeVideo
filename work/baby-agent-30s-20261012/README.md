# 宝宝无字书页冒险 · 30秒

1080×1920竖屏，24fps。画面没有文字、字母、数字、标题或印章。宝宝使用认可的五官素材，移动为爬行，四肢肤色#f8c28b。

## 运行与渲染

Node.js：`node server.mjs 8770`，打开 http://127.0.0.1:8770 。界面播放按钮和时间显示不进入视频画面。
`window.render(seconds)`为30秒可寻址入口，内部以2倍速映射原60秒动作。六处转场采用0.56秒斜向纸页擦拭，不交叉淡化人物。

`node render.mjs --mode=final --version=v2`生成MP4。renderer使用相邻sand-journey工程中的playwright-core、Chrome及Remotion附带FFmpeg；在其他机器可将import路径、Chrome路径和FFmpeg/ffprobe路径改为本机配置。源码变动后使用新版本号，避免复用旧帧。

音频已包含，可直接渲染。重建：Python安装NumPy后运行`python make_audio.py`；先以events-original.json生成原创60秒爵士与拟音，再通过FFmpeg atempo=2输出30秒，保持音高。FFmpeg可由环境变量FFMPEG指定。

## 来源与许可

参考lemomo-ai/lemo-opuscar固定commit e3cb16f63768c68693ff0e15171d6e755457cc32的spy-titles绘制入口、纸边/纸纹、纸偶节拍与摄影机制。许可证在assets/LICENSE-lemo.txt。不声称原片逐像素复现。无外部音乐、字体文件或地图。head-atlas.png为用户认可的形象素材。

## 检查范围

前60秒版本的一轮独立审核已完成预算，本次是用户具体反馈修改，不新增独立审核。30秒成片做画幅、时长、帧数、音轨和完整解码检查；制作查看代表帧与六处转场连续接触表。没有实际听音或正常速度观看的完整视听通过声明。
