# Style Studio

原创 Canvas 风格验证工具。复制整个目录后使用；输出与依赖不随技能包分发。

## 构建

准备 Node.js、Chrome、FFmpeg、Python，执行 `npm install` 和 `python -m pip install -r requirements.txt`。Windows PowerShell 示例：

```powershell
./build.ps1 -PythonExe python -Chrome 'C:/Program Files/Google/Chrome/Application/chrome.exe' -FFmpeg ffmpeg -Clips blueprint-proof,dataviz-proof,one-way,dataviz-variant
```

已有依赖可用 `-Playwright /absolute/path/to/playwright-core/index.js` 指定，无需重新安装。Node 路径可用 `-NodeExe`，输出目录用 `-OutputRoot`。修改源码后选新输出目录，避免混用旧帧。默认声音目标为 -18 LUFS，可用 `-Lufs` 调整。

`clips/*.json` 统一控制画面、字幕、声音、镜头状态与审查时间。`film.mjs` 以时间直接求值；`timeline.mjs` 提供共享契约；`score.py` 生成原创合成拟音和字幕。浏览器访问本地 HTTP 服务的 index.html 可看无声循环预览，最终音轨在 MP4 中。

先运行 `node check.mjs` 与 `node test-contract.mjs`。构建后用 `python audit.py --clip one-way --out out/one-way` 生成抽帧表；必须实际查看，脚本不会自动作审美判断。能力覆盖和未检查项见 `capabilities.json`。本工具验证二维蓝图与八点数据变化，不证明任意三维、流体模拟、旁白或音乐制作。

来源见 CREDITS.md。跨机器中文字形依赖系统字体，需重新审查文字排版。
