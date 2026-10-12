# 《冰下，宇宙亮了》

成片：`out-final/icecube-news-portrait.mp4`，1080×1920、30fps、15 秒，含原创立体声氛围配乐与事件音，无旁白。

热点依据：2026年10月6日，诺贝尔物理学奖授予 Francis Halzen，表彰他对 IceCube 及高能天体中微子发现的贡献。来源：NobelPrize.org [官方公告](https://www.nobelprize.org/prizes/physics/2026/press-release/)，IceCube [获奖新闻](https://icecube.wisc.edu/news/awards/2026/10/francis-halzen-icecube-principal-investigator-wins-2026-physics-nobel-prize/)。奖项表彰既有发现，影片未将其表述为本周新发现。

首镜为历史南极极光照片，摄影 Keith Vanderlinde / NSF。原件 `assets/antarctica.jpg` 保存，影片做竖屏摄影裁切。图库与使用依据见 `sources/gallery.html`、`sources/press-guide.html`；来源、检索日期、哈希和署名均见 `sources/manifest.json`。按 IceCube 图库的教育/信息性非商业使用条件制作此演示片。

冰下模块、粒子光迹、光锥、5,160模块阵列均为原创 Three.js 艺术化示意。光来自中微子相互作用后的带电次级粒子，而非中微子自身发光；速度、布局、颜色及距离不按物理比例。片中持续标记“探测过程艺术化示意 · 非真实事件重建”。

视觉入口 `film.js`；镜头目的、状态、连接窗口、事实与声音事件见 `production-plan.json`。`news_score.py` 据事件表生成低频氛围、6.9秒光迹音和后续晶体音，无外部音乐或真实探测器录音。

本机重建：
```powershell
node render.mjs --project=. --out=out-final --name=icecube-news-silent.mp4 --three=D:/ai项目/ai动画/node_modules/three --playwright=C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core/index.js --ffmpeg=D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe
& 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 news_score.py --ffmpeg=D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe
```

渲染器可恢复同参数帧序列。若修改视觉源码，先使用新的渲染输出目录，将声音脚本中的 `out` 指向同目录；不要混用旧帧。本机复用 Three.js 0.169.0、playwright-core 1.62.1、Chrome 与 Remotion 随包 FFmpeg；Python 使用 numpy/Pillow。

最终审片记录为 `out-final/visual-review.json`；尺寸、时长、音轨、抽帧与声音技术指标见 `out-final/qa`、`sound-evidence.json`、`render-evidence.json`。实时播放和听音状态独立登记，不以抽帧、响度分析代替。
