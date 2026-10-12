# 一粒沙，看见整片海

原创20秒代码短片。正式文件：`out-final/sand-journey.mp4`，1080×1920、9:16、30fps、600帧、H.264/AAC。全片使用同一世界路径与连续相机，稳定沙粒ID为 `sand-0001`。没有旁白、字幕或原片歌曲。

## 运行

在本目录用 PowerShell 执行：

```powershell
& 'D:/docker/node.exe' server.mjs
```

访问 http://127.0.0.1:4318/ ，点击“播放 20 秒 · 含声音”。预览按音频时间驱动画面；正式捕帧使用绝对时间接口，画幅原生竖屏。预览按窗口高度缩放显示，正式输出固定1080×1920。

依赖已安装在工程内；恢复依赖：

```powershell
& 'D:/docker/npm.cmd' ci
```

重新生成声音、检查寻址、正式渲染：

```powershell
& 'D:/docker/node.exe' audio.mjs
& 'D:/docker/node.exe' render.mjs --prepare=1
& 'D:/docker/node.exe' render.mjs --sub=2
```

渲染保存600张JPEG并可断点续跑。同配置且源文件哈希一致时跳过已有帧；修改源码后请复制为独立版本目录，并移除该新版本的旧 `out-final`，避免混用帧。`--sub=2` 是每帧两个不同时间的采样，180°快门、Halton投影抖动、FXAA及HDR积累。浏览器捕帧只允许本地资源请求。

## 工具与入口

- Node `v24.15.0`：`D:/docker/node.exe`；npm：`D:/docker/npm.cmd`。
- Three `0.169.0`、playwright-core `1.62.1`，版本固定在package及锁文件中。
- Chrome `154.0.8037.98`：`C:/Program Files/Google/Chrome/Application/chrome.exe`，Windows D3D11后端。
- FFmpeg/ffprobe：`D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe`及同目录`ffprobe.exe`；编码限制为2个视频线程。
- `index.html` / `js/journey.js`：完整本片运行入口；`renderAt(seconds)`、`ready`和`__film.stateAt(seconds)`。
- `js/timeline.js`：镜头、主角及相机参数，统一声音事件；`PRODUCTION.md`：镜头目的及参考记录。
- `js/journey-world.js`：主角、微观颗粒、共享高度地形/水面和局部飞沫；`js/post.js`：竖屏后处理。
- `audio.mjs`：固定随机原创风、远近浪、掠过及落沙声；`audio/sand-journey.wav`：48kHz立体声PCM16。
- `render.mjs`：寻址检查、本地捕帧、编码和全片解码；`server.mjs`：预览服务。

## 来源及改写

Particle Beach，作者 Ishu Agrawal（GitHub `ishuagrawal`），MIT；固定commit `92db82255b962acf2930f19bf6e5e7790174a790`。仓库：https://github.com/ishuagrawal/particle-beach 。许可保存在根目录及 `upstream/LICENSE`。完整绘制运行源码与原逐文件哈希保存在 `upstream/`，不是整个站点仓库。

指定原片：`D:/ai项目/ai动画/VibeVideo项目/reference-sources/upstream-videos/particle-beach/trailer-1.mp4`。研究实际查看了2、7、12、17、22、27、32、37、42、47、52、57秒提取图，保存在 `research/`；未宣称实时全片观看或听音。

保留共享点材质、固定随机、世界光照uniforms、实体深度、Field世界锚定LOD、海面/白浪/冲洗/沙面点层、surf CPU/GLSL浪形、breakers、天空与天体/调色、远景及岸边层。完整复制的城市/人群/游乐层仍可编辑，本片不实例化这些状态模拟。对 `core.js` 仅增加本片质量覆盖；对 `site.js` 同时修改CPU与GLSL，新增0.58m局部沙脊与细起伏。重新编写本片入口、路径、沙粒与填充面、音频、捕帧器和预览。借鉴预告后处理中的光条、积累与分色，移除横屏遮幅、标题、UI和macOS录制设置。没有把原片画面用于本片主体，没有生成图像或视频API。

## 验证与边界

`technical/prepare-evidence.json`记录7个关键时刻、乱序与新进程像素哈希及状态一致，运行错误与外网请求均为零。`technical/render-evidence.json`、`ffprobe.json`、`full-decode.log`记录正式输出与完整解码；`out-final/source-inputs.json`记录实际源哈希。技术检查不代表视觉或听音验收，新视频先展示给用户。

沙粒运动、飞沫与风是艺术化路径，非科学风沙流体模拟。沙粒半径固定0.008世界单位，景别变化来自相机距离；共享高度约束保持地形与深度一致。无需外部字体、纹理或音效资产。预览使用音频时钟、单采样以便实时播放；正式输出是全分辨率双采样，性能视本机GPU而定。
