# DeepSeek V4 视频制作环境

探测日期：2026-10-09。适用于同一台 Windows 机器、PowerShell；其他机器需重新探测路径。

## 已验证路径和版本

| 工具 | 版本 | 绝对路径 |
|---|---|---|
| Node.js | 24.15.0 | `D:/docker/node.exe` |
| Python | 3.12.14 | `C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe` |
| FFmpeg | n7.1 | `D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe` |
| ffprobe | n7.1 | `D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe` |
| Chrome | 154.0.8037.98 | `C:/Program Files/Google/Chrome/Application/chrome.exe` |
| Playwright Core | 1.62.1 | `C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core/index.js` |
| Playwright | 1.62.1 | `C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.js` |

Python 环境已安装 NumPy 2.3.5、Pillow 12.3.0，实际导入、数组与图像创建通过。满足 studio/requirements.txt。

在该 Python 环境中未检测到 Python playwright、imageio-ffmpeg、requests、scipy、matplotlib、soundfile。本项目 studio 使用 Node Playwright，现有制作路线不要求这些 Python 包。

项目共享依赖有 Remotion 和 @remotion/renderer 4.0.506。项目 node_modules 是指向 `D:/ai项目/ai动画/node_modules` 的目录联接。Playwright 不在这个依赖树中，必须显式传入上表绝对路径。

PATH 中能解析 node、npm，但不能解析 python、py、ffmpeg、ffprobe。请使用绝对路径；不必修改全局配置。

## 工作入口

- 项目：`D:/ai项目/ai动画/VibeVideo项目`
- 技能：`D:/Codex/skills/vibe-video/SKILL.md`
- 制作流程：项目根目录 `PRODUCTION.md`
- 已有可运行工程：`D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio`
- 时间轴：studio 的 `clips/*.json`
- 画面：`film.mjs`；契约：`timeline.mjs`；渲染：`render.mjs`；音效/字幕：`score.py`

## 可直接执行的现有样片构建

下面重建现有 10 秒数据样片，输出目录使用独立名称，避免覆盖已有视频。若已经使用过该输出目录且修改了源码，请换一个新目录名。

```powershell
Set-Location 'D:/ai项目/ai动画/VibeVideo项目/work/style-production-20261009/studio'
./build.ps1 `
  -NodeExe 'D:/docker/node.exe' `
  -PythonExe 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' `
  -Chrome 'C:/Program Files/Google/Chrome/Application/chrome.exe' `
  -FFmpeg 'D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe' `
  -Playwright 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core/index.js' `
  -Clips dataviz-proof `
  -OutputRoot 'out-deepseek-trial-01'
```

预期最终视频：`out-deepseek-trial-01/dataviz-proof/dataviz-proof.mp4`，相对 studio 目录。

## 探测验证范围

- Node Playwright 实际加载成功，Chrome 无头启动成功，Canvas PNG 数据导出成功。
- FFmpeg 启动成功，编码器列表有 libx264、AAC；这是 Remotion 精简构建，新增滤镜使用前应检查支持情况。
- 本次只做环境探测，没有重建整个样片，没有安装新软件或修改全局环境。
- 修改内容后仍需检查输出帧、动作连续性和文字排版；渲染成功不能代替审片与听音。
