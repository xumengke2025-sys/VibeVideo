# 《只向一个方向》15 秒竖屏

1080×1920、24fps、15 秒。成片 `out-final/one-way-portrait.mp4`。原横版保留在 `work/style-production-20261009/studio`。

沿用已批准的 15 秒动作时序，重新绘制竖向剖面：上游在上、下游在下。阀瓣向下开启并压缩弹簧，复位后阀瓣上表面与阀座下表面贴合。流箭头由同一开启状态控制，完全回座后无通过阀座的流动。剖切、外壳分开和回位用于解释内部结构，不表示真实阀门操作。此图为简化原理示意，无工程尺寸或流体求解。

源码入口 `film.js`；共享事件、声音和字幕时序为 `clips/one-way-portrait.json`；`score.py` 生成合成机械拟音，开启6.3秒、回座接触11秒、结尾章12.832秒。无旁白。复用的时间轴、纸纹/蓝图方法与原声工具来自本项目既有原创工程。

在本目录运行：
```powershell
node render.mjs --project=. --out=out-rebuild --name=one-way-portrait-silent.mp4 --three=D:/ai项目/ai动画/node_modules/three --playwright=C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core/index.js --ffmpeg=D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe
& 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 score.py --clip=one-way-portrait --out=out-rebuild --ffmpeg=D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe
```

代码使用 Canvas，无第三方远程请求；渲染工具需要本机 Chrome、Node 和 playwright-core。`--three` 是共享渲染器的路径参数，本片不调用 Three.js。Python 声音工具需要 numpy，审片工具需要 Pillow。播放/听音与序列观察状态见 `out-final/visual-review.json`，技术结果见 `out-final/qa/media-evidence.json` 和 `out-final/render-evidence.json`。
