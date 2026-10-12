# 绕过黑暗：黑洞引力透镜

原创 32 秒科普视觉短片，16:9，1920×1080，30fps。以一束光连接吸积盘背面的光源、三维弯曲路径与观察者看到的上拱亮弧。画面、时间轴与合成电子氛围音轨由本项目独立制作；没有使用 pdoom 的场景或歌曲。

成片：`out/around-the-dark.mp4`。

## 编辑入口

- `film.mjs`：镜头时间轴、相机位置、三维结构、光点路径、中文排版及说明文字。
- `lens.frag`：成像光路积分、盘面细纹、颜色和背景星点。
- `make_soundtrack.py`：原创合成声音的音符、事件时间和混响。
- `render.mjs`：本地预览、设定帧与 MP4 渲染。
- `production.md`：分镜、事实来源、科学示意边界。
- `review-evidence.json`：最终成片校验和实际审阅覆盖范围。

所有状态按明确时间计算，可用浏览器中的 `window.__film.renderAt(seconds)` 直接寻址。不依赖前面是否播放过某一帧。全片采用 1.5 倍空间超采样；几何场景另启用 MSAA。字幕单独按输出尺寸绘制。未采用时间子帧累积或原项目的自适应采样。

## 在当前工作区运行

当前已存在所需的 Three.js 和浏览器运行依赖，可在本目录运行：

```powershell
& 'C:\Users\67236\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' render.mjs --serve
```

浏览器打开 `http://127.0.0.1:8926`。播放按钮会同步加载 `soundtrack.wav`；滑块可以逐帧寻址。

```powershell
# 重渲 32 秒成片
& 'C:\Users\67236\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' render.mjs
# 输出代表帧
& 'C:\Users\67236\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' render.mjs --stills
# 8–17 秒动作研究片段，1280×720
& 'C:\Users\67236\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' render.mjs --study --version=new
```

重新生成声音：`python make_soundtrack.py`。独立轨道检查：`python verify_orbits.py`。

## 移到其他目录或机器

安装 package.json 中的 `three` 与 `playwright-core`。设置 `CHROME` 为本机 Chromium/Chrome 可执行文件，`FFMPEG` 为支持 x264/AAC 的 FFmpeg 可执行文件。可通过 `PORT` 修改本地端口；`PLAYWRIGHT_PATH` 可指定已有 playwright-core 包。默认浏览器路径是 Windows Chrome；默认 FFmpeg 路径是当前工作区 Remotion 附带的二进制。

中文使用本机微软雅黑，英文使用本机 Bahnschrift / Segoe UI；商业字体未随源码分发。换机器需要相应字体或在 `film.mjs` 的 `fonts` 中选择已有中文字体，并重新检查排版。音轨可以原样播放，也可从 Python 源码重新生成。

## 科学范围

这是非旋转黑洞的程序化科学示意，采用球对称 Schwarzschild 光子轨道方程的数值积分。有限步长与初始相机映射存在近似；颜色、亮度、盘纹和运动时间经过美术化，未做完整相对论辐射转移。片内的网格用于解释空间，结构到观测图像的插值用于重建转场，不表示真实引力会开关。不是望远镜拍摄，也不是 Kerr 自旋黑洞的精确模拟。

科普依据见 `production.md` 中两篇 NASA 原始资料。音轨是原创合成电子氛围声音，无人声旁白；实际检查方式与限制见最终审阅证据。

## 交付与检查

`out/around-the-dark-source.zip` 是可编辑源码包，含声音、制作说明、最终检查报告、实际查看的接触表与四张原尺寸图片。成片 MP4 单独交付；旧样片和大量单帧导出不放入源码包。`out/delivery-inventory.json` 记录视频和打包文件的 SHA256。

最终视频完整解码通过。视觉检查覆盖 24 张关键帧、114–172 帧和 408–474 帧的连续序列，以及四张原尺寸图片。没有全片实时播放或实际听音；32 秒音频幅度检查只能证明音轨存在且有信号。完整证据与科学限制见 `review-evidence.json`。
